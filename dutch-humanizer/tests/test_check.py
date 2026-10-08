"""Unittests voor scripts/check.py.

Draaien vanuit de skillmap:
    python3 -m unittest discover -s tests -v

Deze tests controleren de mechanische signalen. Ze bewijzen niet dat een
herschrijving dezelfde betekenis heeft; de redactionele evaluatie staat in de
repository onder evals/dutch-humanizer/.
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
SCRIPT = SKILL_DIR / "scripts" / "check.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "check"

spec = importlib.util.spec_from_file_location("check", SCRIPT)
check_mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["check"] = check_mod
spec.loader.exec_module(check_mod)
check = check_mod.check


def msgs(findings, level):
    return [f.message for f in findings if f.level == level]


def joined(findings, level):
    return " | ".join(msgs(findings, level))


class NumbersAndQuantities(unittest.TestCase):
    def test_01_new_number(self):
        f = check("We leveren binnen 5 dagen.", "We leveren binnen 3 dagen.")
        self.assertIn("staat niet in de input: 5", joined(f, "WARNING"))

    def test_02_removed_number(self):
        f = check("Er gingen imports mis.", "Van de 120 imports gingen er 6 mis.")
        w = joined(f, "WARNING")
        self.assertIn("ontbreekt: 120", w)
        self.assertIn("ontbreekt: 6", w)

    def test_03_changed_percentage(self):
        f = check("Volgens studies doet 37% van de bedrijven dit.", "Volgens studies doet 73% van de bedrijven dit.")
        self.assertIn("percentage mogelijk veranderd: 73% wordt 37%", joined(f, "WARNING"))

    def test_03b_removed_percentage(self):
        f = check("Veel bedrijven doen dit.", "Studies tonen aan dat 73% van de bedrijven dit doet.")
        self.assertIn("percentage uit de input ontbreekt: 73%", joined(f, "WARNING"))

    def test_04_exact_dates_preserved(self):
        f = check("De deadline is 5 maart 2026 om 14:30.", "Uiterlijk op 5 maart 2026 om 14:30 is de deadline.")
        self.assertNotIn("datum", joined(f, "WARNING"))

    def test_04b_translated_date_matches(self):
        f = check("De kickoff is op donderdag 5 maart.", "The kickoff is on Thursday, March 5.")
        self.assertNotIn("datum", joined(f, "WARNING"))

    def test_05_suspicious_date_change(self):
        f = check("De koppeling komt vóór 15 november.", "De koppeling komt vóór 14 november.")
        w = joined(f, "WARNING")
        self.assertIn("ontbreekt of is gewijzigd: 14 november", w)
        self.assertIn("staat niet in de input: 15 november", w)

    def test_unit_change(self):
        f = check("Indienen binnen 30 weken.", "Indienen binnen 30 dagen.")
        self.assertIn("eenheid of valuta bij 30 weken", joined(f, "WARNING"))

    def test_number_words_match_digits(self):
        f = check("We storten het binnen tien werkdagen terug.", "We storten het binnen 10 werkdagen terug.")
        self.assertNotIn("getal", joined(f, "WARNING"))

    def test_16_legitimate_ranges(self):
        f = check("Support is bereikbaar van 9 tot 17 uur.", "Support is bereikbaar van 9-17 uur.")
        self.assertEqual(msgs(f, "WARNING"), [])
        f = check("Bereikbaar 9–17 uur.", "Bereikbaar 9-17 uur.")
        self.assertEqual([m for m in msgs(f, "INFO") if "en-dash" in m], [])

    def test_17_markdown_numbering_is_not_a_number(self):
        f = check("Twee opties:\n\n1. Doorgaan.\n2. Inkrimpen.", "Twee opties: doorgaan of inkrimpen.")
        self.assertNotIn("getal", joined(f, "WARNING"))


class ProtectedContent(unittest.TestCase):
    def test_06_changed_url(self):
        f = check("Zie https://docs.example.org/cli#run.", "Zie https://docs.example.org/cli#dry-run.")
        w = joined(f, "WARNING")
        self.assertIn("URL uit de input ontbreekt of is gewijzigd: https://docs.example.org/cli#dry-run", w)
        self.assertIn("URL staat niet in de input", w)

    def test_markdown_link_target_preserved(self):
        f = check("Lees [de handleiding](https://x.nl/a).", "Lees eerst [deze handleiding](https://x.nl/a).")
        self.assertNotIn("URL", joined(f, "WARNING"))

    def test_07_changed_email(self):
        f = check("Mail support@voorbeeld.nl.", "Mail helpdesk@voorbeeld.nl.")
        self.assertIn("e-mailadres uit de input ontbreekt", joined(f, "WARNING"))

    def test_08_literal_quotation(self):
        src = 'De CTO zei: "Dit is de release waar we op wachtten — eindelijk." Dat klopt.'
        good = 'Onze CTO zei het zo: "Dit is de release waar we op wachtten — eindelijk."'
        f = check(good, src, style="strict")
        self.assertEqual(msgs(f, "ERROR"), [])
        self.assertNotIn("citaat", joined(f, "WARNING"))
        bad = 'De CTO zei: "Dit is de release waar we lang op wachtten."'
        self.assertIn("citaat", joined(check(bad, src), "WARNING"))

    def test_09_inline_code_protected(self):
        src = "Gebruik `--dry-run` om wijzigingen te bekijken."
        f = check("Met `--dry-run` bekijk je de wijzigingen.", src, style="strict")
        self.assertEqual(msgs(f, "ERROR"), [])
        f = check("Met `--dryrun` bekijk je de wijzigingen.", src)
        self.assertIn("code gewijzigd of verwijderd: --dry-run", joined(f, "ERROR"))

    def test_10_fenced_code_protected(self):
        src = "Stuur de header mee:\n\n```\nAuthorization: Bearer TOKEN — 1\n```\n"
        good = "Stuur deze header mee:\n\n```\nAuthorization: Bearer TOKEN — 1\n```\n"
        self.assertEqual(msgs(check(good, src, style="strict"), "ERROR"), [])
        bad = "Stuur deze header mee:\n\n```\nAuthorization: Token TOKEN\n```\n"
        self.assertIn("code gewijzigd", joined(check(bad, src), "ERROR"))

    def test_11_tilde_fences(self):
        src = "Voorbeeld:\n\n~~~bash\ncurl -X POST https://api.example.org/v1 -- —\n~~~\n"
        f = check(src.replace("Voorbeeld", "Zo werkt het"), src, style="strict")
        self.assertEqual(msgs(f, "ERROR"), [])
        self.assertNotIn("URL", joined(f, "WARNING"))

    def test_12_indented_code(self):
        src = "Draai dit:\n\n    make test — snel\n\nKlaar."
        f = check("Draai het volgende:\n\n    make test — snel\n\nDan ben je klaar.", src, style="strict")
        self.assertEqual(msgs(f, "ERROR"), [])
        f = check("Draai het volgende:\n\n    make check\n\nKlaar.", src)
        self.assertIn("code gewijzigd", joined(f, "ERROR"))

    def test_indented_list_continuation_is_not_code(self):
        text = "- punt een\n\n    vervolg van het punt\n"
        spans = check_mod.block_spans(text)
        self.assertEqual([s for s in spans if s.kind == "code"], [])

    def test_frontmatter_changed(self):
        src = "---\ntitle: Test\n---\nTekst."
        self.assertIn("frontmatter", joined(check("---\ntitle: Ander\n---\nTekst.", src), "ERROR"))
        self.assertEqual(msgs(check("---\ntitle: Test\n---\nDe tekst.", src), "ERROR"), [])

    def test_escaped_characters_are_not_dashes(self):
        f = check("Kies a \\- b.", None, style="strict")
        self.assertEqual(msgs(f, "ERROR"), [])


class Typography(unittest.TestCase):
    def test_13_line_numbers(self):
        out = "Regel een.\nRegel twee.\nRegel drie — met streepje."
        f = check(out, None, style="strict")
        self.assertEqual([x.line for x in f if x.level == "ERROR"], [3])

    def test_14_dash_configuration(self):
        out, src = "Het werkt — meestal.", "Het werkt meestal."
        self.assertTrue(msgs(check(out, src, style="strict"), "ERROR"))
        self.assertEqual(msgs(check(out, src, style="strict", allow_dashes=True), "ERROR"), [])
        neutral = check(out, src)
        self.assertEqual(msgs(neutral, "ERROR"), [])
        self.assertIn("em-dash", joined(neutral, "INFO"))

    def test_dash_already_in_input_is_checked_in_strict(self):
        # Gewijzigd in v0.7.0. Deze test heette test_dash_already_in_input_is_not_new en eiste dat
        # --style strict een streepje uit de input negeerde. De strikte huisstijl geldt voor alle
        # bewerkbare output; alleen citaten en code zijn uitgezonderd (opdracht v0.7.0, 6D).
        src = "Het werkt \u2014 meestal."
        self.assertTrue(msgs(check("Dit werkt \u2014 meestal.", src, style="strict"), "ERROR"))
        self.assertEqual(msgs(check("Dit werkt \u2014 meestal.", src), "ERROR"), [])

    def test_15_unicode_quotation_marks(self):
        src = "Hij zei „het project ligt op schema” en vertrok."
        f = check('Hij zei "het project ligt op schema" en vertrok.', src)
        self.assertNotIn("citaat", joined(f, "WARNING"))
        f = check("Hij zei “het project ligt op schema”.", "Hij zei: het project ligt op schema.",
                  style="strict")
        self.assertIn("gekruld", joined(f, "ERROR"))

    def test_apostrophe_is_not_a_quote(self):
        f = check("Zo’n KPI’s-overzicht helpt.", None, style="strict")
        self.assertEqual(msgs(f, "ERROR"), [])

    def test_capital_after_colon_is_info_only(self):
        f = check("Let op: Dit kan.", "Let op, dit kan.")
        self.assertIn("hoofdletter na dubbele punt", joined(f, "INFO"))
        self.assertEqual(msgs(f, "ERROR") + msgs(f, "WARNING"), [])
        f = check("Let op: Jan komt.", "Let op, Jan komt.")
        self.assertNotIn("hoofdletter", joined(f, "INFO"))


class MeaningSignals(unittest.TestCase):
    def test_18_negation_removed(self):
        f = check("De exportfunctie wordt meegenomen.", "De exportfunctie wordt niet meegenomen.")
        self.assertIn("ontkenning: 'niet'", joined(f, "WARNING"))

    def test_19_modality_changed(self):
        f = check("De synchronisatie is mislukt.", "Het lijkt erop dat de synchronisatie is mislukt.")
        self.assertIn("onzekerheid: 'lijkt'", joined(f, "WARNING"))

    def test_19b_within_becomes_after(self):
        f = check("De aanvraag moet na 30 dagen worden ingediend.",
                  "De aanvraag moet binnen 30 dagen worden ingediend.")
        w = joined(f, "WARNING")
        self.assertIn("'binnen' komt niet meer voor; nieuw: 'na'", w)

    def test_condition_removed(self):
        f = check("De klant ontvangt de bestanden.", "De klant ontvangt de bestanden zodra de goedkeuring binnen is.")
        self.assertIn("voorwaarde of uitzondering: 'zodra'", joined(f, "WARNING"))

    def test_tenzij_removed(self):
        f = check("We leveren op maandag.", "We leveren op maandag, tenzij de klant uitstel vraagt.")
        self.assertIn("'tenzij'", joined(f, "WARNING"))

    def test_deadline_removed(self):
        src = (FIXTURES / "deadline-input.txt").read_text(encoding="utf-8")
        out = (FIXTURES / "deadline-output.txt").read_text(encoding="utf-8")
        w = joined(check(out, src), "WARNING")
        self.assertIn("17.00 uur", w)
        self.assertIn("'uiterlijk'", w)

    def test_attribution_removed(self):
        f = check("De nieuwe versie is de enige optie.", "Volgens Joost is de nieuwe versie de enige optie.")
        self.assertIn("naam uit de input ontbreekt: Joost", joined(f, "WARNING"))

    def test_invented_signature_name(self):
        f = check("Groet,\nSanne", "Met vriendelijke groet,\nHet supportteam")
        self.assertIn("naam staat niet in de input: Sanne", joined(f, "WARNING"))

    def test_inflected_uncertainty_counts(self):
        f = check("Om 09:40 was de vermoedelijke oorzaak gevonden.", "Om 09:40 bleek de oorzaak vermoedelijk gevonden.")
        self.assertNotIn("onzekerheid", joined(f, "WARNING"))

    def test_mits_to_als_is_reviewed(self):
        # Gewijzigd in v0.7.0. Deze test heette test_condition_synonym_is_info en eiste dat "mits" naar
        # "als" alleen INFO gaf ("meestal gelijkwaardig"). "Mits" betekent "alleen als"; "als" is
        # zwakker. De gelijkwaardigheidsgroepen zijn verwijderd (opdracht v0.7.0, 6C).
        f = check("Zondag kan wel, als jij dan tijd hebt.", "Zondag zou wel kunnen, mits jij dan tijd hebt.")
        self.assertIn("voorwaarde", joined(f, "WARNING"))
        self.assertNotIn("gelijkwaardig", joined(f, "WARNING") + joined(f, "INFO"))

    def test_obligation_synonym_is_info(self):
        f = check("Alle teamleads moeten deelnemen.", "Deelname is verplicht voor alle teamleads.")
        self.assertNotIn("verplichting", joined(f, "WARNING"))

    def test_sentence_start_words_are_not_names(self):
        f = check("Beste Anouk, hierbij laat ik u weten dat het klaar is.",
                  "Beste Anouk, Hierbij wil ik u informeren dat het klaar is. Zoals gezegd.")
        self.assertNotIn("naam", joined(f, "WARNING"))

    def test_repeated_date_is_not_new(self):
        src = "De release staat gepland voor 03/04/2026."
        out = "De release staat gepland voor 03/04/2026.\nLet op: 03/04/2026 is dubbelzinnig."
        self.assertNotIn("datum", joined(check(out, src), "WARNING"))

    def test_20_warnings_do_not_claim_certainty(self):
        f = check("De export wordt meegenomen.", "De export wordt niet meegenomen.")
        for m in msgs(f, "WARNING"):
            self.assertRegex(m, r"[Mm]ogelijk|controleer")
        result = subprocess.run([sys.executable, str(SCRIPT), str(FIXTURES / "deadline-output.txt"),
                                 "--input", str(FIXTURES / "deadline-input.txt")],
                                capture_output=True, text=True, check=False)
        self.assertIn("geen bewijs", result.stdout)
        self.assertEqual(result.returncode, 0)

    def test_faithful_rewrite_has_no_meaning_warnings(self):
        src = (FIXTURES / "deadline-input.txt").read_text(encoding="utf-8")
        out = (FIXTURES / "deadline-output-goed.txt").read_text(encoding="utf-8")
        self.assertEqual(msgs(check(out, src), "WARNING"), [])

    def test_translation_skips_lexical_checks(self):
        f = check("Voor Q1 hebben we €12.500. Het is logisch om klein te beginnen.",
                  "It makes sense to start small. We have €12,500 for Q1.")
        self.assertIn("niet Nederlands", joined(f, "INFO"))
        self.assertNotIn("getal", joined(f, "WARNING"))


class InputHandling(unittest.TestCase):
    def test_21_empty_input(self):
        self.assertEqual(check("", ""), [])
        self.assertIn("leeg", joined(check("", "Er staat tekst."), "ERROR"))
        check("Tekst.", "")  # mag niet crashen

    def test_22_unicode_dutch(self):
        src = "Café Brûlé in Zwolle opent vóór de zomer een tweede vestiging, zegt eigenaar Anaïs."
        out = "Café Brûlé in Zwolle opent vóór de zomer een tweede vestiging, zegt eigenaar Anaïs."
        self.assertEqual(msgs(check(out, src), "WARNING"), [])

    def test_23_multiline_line_numbers_point_to_input(self):
        src = "Regel een.\nRegel twee.\nLever uiterlijk 7 november."
        f = check("Regel een.\nRegel twee.\nLever snel.", src)
        lines = [x.line for x in f if x.level == "WARNING" and "7 november" in x.message]
        self.assertEqual(lines, [3])
        self.assertTrue(all(x.where == "input" for x in f if "7 november" in x.message))


class CommandLine(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, check=False)

    def test_24_cli_compatibility(self):
        dash = str(FIXTURES / "dash-output.txt")
        self.assertEqual(self.run_cli(dash).returncode, 0)
        self.assertEqual(self.run_cli(dash, "--style", "strict").returncode, 1)
        self.assertEqual(self.run_cli(dash, "--style", "strict", "--allow-dashes").returncode, 0)
        res = self.run_cli(str(FIXTURES / "deadline-output.txt"), "--input", str(FIXTURES / "deadline-input.txt"),
                           "--allow-dashes")
        self.assertEqual(res.returncode, 0)
        self.assertIn("WARNING", res.stdout)

    def test_fail_on_warning(self):
        res = self.run_cli(str(FIXTURES / "deadline-output.txt"), "--input", str(FIXTURES / "deadline-input.txt"),
                           "--fail-on-warning")
        self.assertEqual(res.returncode, 1)

    def test_missing_file_is_usage_error(self):
        self.assertEqual(self.run_cli(str(FIXTURES / "bestaat-niet.txt")).returncode, 2)


if __name__ == "__main__":
    unittest.main()
