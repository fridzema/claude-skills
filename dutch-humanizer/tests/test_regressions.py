"""Tabelgestuurde regressies, invariantie, perturbaties, vals-positieven en randgevallen.

Draaien vanuit de skillmap:
    python3 -m unittest discover -s tests -v

Deze tests toetsen het mechanische contract van scripts/check.py. Een geslaagde
test bewijst niet dat een herschrijving dezelfde betekenis heeft.
"""

from __future__ import annotations

import json
import random
import sys
import time
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from dhcheck import analyze  # noqa: E402
from dhcheck.markdown import parse  # noqa: E402

FIXTURES = Path(__file__).resolve().parent / "fixtures"
SEED = 20261008


def codes(report, *levels):
    levels = levels or ("ERROR", "WARNING", "INFO")
    return {f.code for f in report.findings if f.severity in levels}


def serious(report):
    return codes(report, "ERROR", "WARNING")


class Regressions(unittest.TestCase):
    """De gevallen uit sectie 8 van de opdracht v0.7.0."""

    def test_table(self):
        cases = json.loads((FIXTURES / "regressions.json").read_text(encoding="utf-8"))["cases"]
        for c in cases:
            with self.subTest(case=c["id"] + " " + c["case"]):
                r = analyze(c["output"], c["source"], **c.get("options", {}))
                for code in c.get("require", []):
                    self.assertIn(code, serious(r))
                for code in c.get("require_error", []):
                    self.assertIn(code, codes(r, "ERROR"))
                for code in c.get("forbid", []):
                    self.assertNotIn(code, codes(r))
                if c.get("max_severity") == "INFO":
                    self.assertEqual(serious(r), set())
                if c.get("max_severity") == "WARNING":
                    self.assertEqual(codes(r, "ERROR"), set())
                if c.get("no_equivalence_claim"):
                    self.assertFalse(any("gelijkwaardig" in f.message for f in r.findings))
                if c.get("no_findings"):
                    self.assertEqual(r.findings, [])


class FalsePositives(unittest.TestCase):
    """Correcte parafrases: alleen gedocumenteerde vals-positieven zijn toegestaan."""

    def test_equivalence_set(self):
        cases = json.loads((FIXTURES / "equivalence.json").read_text(encoding="utf-8"))["cases"]
        for c in cases:
            with self.subTest(case=c["id"]):
                r = analyze(c["output"], c["source"], **c.get("options", {}))
                self.assertEqual(serious(r), set(c.get("known_fp", [])), [f.format() for f in r.findings])

    def test_known_false_positive_rate_is_bounded(self):
        cases = json.loads((FIXTURES / "equivalence.json").read_text(encoding="utf-8"))["cases"]
        with_fp = [c for c in cases if c.get("known_fp")]
        self.assertLessEqual(len(with_fp) / len(cases), 0.15)


BASES = [
    "Lever de wijziging uiterlijk vrijdag om 17.00 uur in.",
    "Wij storten het bedrag binnen 10 werkdagen terug.",
    "De export wordt niet meegenomen, tenzij de klant erom vraagt.",
    "De temperatuur mag maximaal 25 graden zijn.",
    "Het lijkt erop dat 3 van de 120 imports zijn mislukt.",
    "Je moet het formulier ondertekenen voordat je het verstuurt.",
    "De korting bedraagt 1,5% op orders boven € 500.",
    "Gebruik `make deploy` en daarna `make test`.",
]
PERTURBATIONS = [
    ("cijfer", lambda t: t.replace("1", "7", 1) if "1" in t else None),
    ("ontkenning weg", lambda t: t.replace(" niet", "", 1) if " niet" in t else None),
    ("binnen wordt na", lambda t: t.replace("binnen", "na", 1) if "binnen" in t else None),
    ("tenzij wordt mits", lambda t: t.replace("tenzij", "mits", 1) if "tenzij" in t else None),
    ("uiterlijk weg", lambda t: t.replace("uiterlijk ", "", 1) if "uiterlijk" in t else None),
    ("maximaal wordt minimaal", lambda t: t.replace("maximaal", "minimaal", 1) if "maximaal" in t else None),
    ("lijkt weg", lambda t: t.replace("Het lijkt erop dat 3", "3", 1) if "lijkt" in t else None),
    ("moet wordt kunt", lambda t: t.replace("moet", "kunt", 1) if "moet" in t else None),
    ("komma wordt punt", lambda t: t.replace("1,5", "1.5", 1) if "1,5" in t else None),
    ("code gewijzigd", lambda t: t.replace("make deploy", "make deploy-all", 1) if "make deploy" in t else None),
    ("eenheid weg", lambda t: t.replace(" graden", "", 1) if " graden" in t else None),
]


class Perturbations(unittest.TestCase):
    def test_self_comparison_has_no_findings(self):
        for base in BASES:
            with self.subTest(base=base):
                self.assertEqual(serious(analyze(base, base)), set())

    def test_targeted_perturbations_are_detected(self):
        rng = random.Random(SEED)
        applied = 0
        for base in BASES:
            for name, fn in rng.sample(PERTURBATIONS, len(PERTURBATIONS)):
                out = fn(base)
                if out is None or out == base:
                    continue
                applied += 1
                with self.subTest(base=base, perturbation=name):
                    self.assertTrue(serious(analyze(out, base)), out)
        self.assertGreaterEqual(applied, 12)

    def test_extra_space_prose_vs_code(self):
        src = "Draai dit:\n\n```\nprint(\"a b\")\n```\n\nDan ben je klaar."
        prose = src.replace("Dan ben je", "Dan  ben je")
        code = src.replace('print("a b")', 'print("a  b")')
        self.assertEqual(serious(analyze(prose, src)), set())
        self.assertIn("CODE_CHANGED", codes(analyze(code, src), "ERROR"))


class EdgeCases(unittest.TestCase):
    def test_dates_times_and_ranges(self):
        self.assertIn("DATE_REMOVED", serious(analyze("De koppeling komt vóór 15 november.",
                                                      "De koppeling komt vóór 14 november.")))
        self.assertEqual(serious(analyze("Om 14:30 begint het.", "Het begint om 14.30 uur.")), set())
        self.assertEqual(serious(analyze("Open van 9–17 uur.", "Open van 9-17 uur.")), set())

    def test_comparison_operators(self):
        r = analyze("De levertijd is minimaal 10 dagen.", "De levertijd is maximaal 10 dagen.")
        self.assertIn("QTY_OPERATOR_CHANGED", serious(r))
        r = analyze("Er waren 5 meldingen.", "Er waren meer dan 5 meldingen.")
        self.assertIn("QTY_OPERATOR_CHANGED", serious(r))

    def test_commas_in_prose(self):
        self.assertEqual(serious(analyze("Ik kocht 3, 4 en 5 appels.", "Ik kocht 3, 4 en 5 appels.")), set())
        self.assertTrue(serious(analyze("Ik kocht 3,4 appels.", "Ik kocht 3, 4 appels.")))

    def test_list_numbering(self):
        r = analyze("Twee opties:\n\n1. Doorgaan.\n2. Stoppen.", "Twee opties: doorgaan of stoppen.")
        self.assertNotIn("QTY_ADDED", codes(r))

    def test_unclosed_fence_runs_to_end(self):
        src = "Tekst.\n\n```\nrm -rf build/\nnog een regel"
        spans = [s for s in parse(src).spans if s.is_code]
        self.assertEqual(len(spans), 1)
        self.assertIn("nog een regel", spans[0].text)

    def test_backticks_of_different_length(self):
        spans = [s.text for s in parse("Gebruik ``a`b`` en `c`.").spans if s.is_code]
        self.assertEqual(spans, ["a`b", "c"])

    def test_tilde_fence_not_closed_by_backticks(self):
        src = "~~~\ncode\n```\nnog code\n~~~\nTekst."
        spans = [s for s in parse(src).spans if s.is_code]
        self.assertEqual(len(spans), 1)
        self.assertIn("nog code", spans[0].text)

    def test_nested_link_brackets(self):
        r = analyze("Zie [de [nieuwe] gids](https://x.nl/a_(b)).", "Zie [de [nieuwe] gids](https://x.nl/a_(b)).")
        self.assertEqual(r.findings, [])
        self.assertIn("https://x.nl/a_(b)", [s.text for s in parse("[a [b]](https://x.nl/a_(b))").spans])

    def test_compound_units(self):
        self.assertIn("QTY_UNIT_CHANGED", serious(analyze("Binnen 3 kalenderdagen.", "Binnen 3 werkdagen.")))
        self.assertIn("QTY_UNIT_CHANGED", serious(analyze("Een stijging van 2 procent.",
                                                          "Een stijging van 2 procentpunt.")))

    def test_unicode_and_emoji(self):
        src = "Café Brûlé in Zwolle opent vóór de zomer 🎉"
        self.assertEqual(serious(analyze(src, src)), set())

    def test_empty_and_whitespace(self):
        self.assertEqual(analyze("", "").findings, [])
        self.assertIn("EMPTY_OUTPUT", codes(analyze("   \n", "Er staat tekst."), "ERROR"))
        self.assertIn("EMPTY_OUTPUT", codes(analyze("", None, task="create"), "ERROR"))
        self.assertEqual(codes(analyze("Tekst.", "", task="rewrite"), "ERROR"), set())

    def test_large_input_is_linear_enough(self):
        chunk = "Regel met `code` en \"citaat\" en 12,5% en https://x.nl/a. "
        big = chunk * 15000  # ongeveer 900 kB
        start = time.monotonic()
        analyze(big, big)
        self.assertLess(time.monotonic() - start, 30)

    def test_repeated_quotes(self):
        r = analyze('Hij zei "ja" en zij zei ook "nee".', 'Hij zei "ja" en zij zei ook "ja".')
        self.assertIn("QUOTE_CHANGED", serious(r))

    def test_escaped_quotes_are_not_delimiters(self):
        quotes = [s.text for s in parse('Typ \\"niet\\" en "wel".').spans if s.kind == "quote"]
        self.assertEqual(quotes, ["wel"])

    def test_apostrophes_and_delimiting_quotes(self):
        self.assertEqual([s for s in parse("Zo'n KPI's-overzicht, 's avonds.").spans if s.kind == "quote"], [])
        delimited = '"Eerste zin. Tweede zin met een "citaat" erin. Derde zin."'
        quotes = [s.text for s in parse(delimited).spans if s.kind == "quote"]
        self.assertEqual(quotes, ["citaat"])

    def test_protected_versus_plain_typography(self):
        src = 'Hij zei: "Klaar — eindelijk." Dat klopt.'
        self.assertEqual(codes(analyze('Hij zei: "Klaar — eindelijk." Klopt.', src, style="strict"), "ERROR"),
                         set())
        self.assertIn("TYPO_DASH", codes(analyze("Klaar — eindelijk.", "Klaar, eindelijk.", style="strict"),
                                         "ERROR"))

    def test_stable_line_numbers(self):
        src = "Een.\nTwee.\nDrie.\nVier.\nLever uiterlijk 7 november."
        r = analyze("Een.\nTwee.\nDrie.\nVier.\nLever snel.", src)
        lines = {f.line for f in r.findings if f.code == "DATE_REMOVED"}
        self.assertEqual(lines, {5})

    def test_short_imperative_is_not_a_name(self):
        r = analyze("Wacht 3 dagen.", "Over 3 dagen kun je het opnieuw proberen.")
        self.assertNotIn("NAME_ADDED", codes(r))
        r = analyze("Groet,\nSanne", "Met vriendelijke groet,\nHet supportteam")
        self.assertIn("NAME_ADDED", codes(r))

    def test_create_allows_requested_code(self):
        r = analyze("Draai `make test`.", "Schrijf een korte instructie om de tests te draaien met make.",
                    task="create")
        self.assertNotIn("CODE_ADDED", codes(r))

    def test_summarize_downgrades_removals(self):
        r = analyze("Het project is klaar.", "Het project is op 3 maart klaar, met 12 deelnemers.", task="summarize")
        self.assertEqual(codes(r, "ERROR", "WARNING"), set())

    def test_shorten_does_not_permit_dropping_facts(self):
        r = analyze("Het project is klaar.", "Het project is op 3 maart klaar, met 12 deelnemers.", task="shorten")
        self.assertIn("QTY_REMOVED", serious(r))

    def test_version_numbers_are_literal(self):
        self.assertIn("VERSION_CHANGED", serious(analyze("Werk bij naar 2.4.0.", "Werk bij naar 2.4.1.")))

    def test_explicit_locales(self):
        r = analyze("Het totaal is 1.234,50 euro.", "The total is 1,234.50 euros.", source_lang="other",
                    source_locale="en-US", target_locale="nl-NL")
        self.assertEqual(serious(r), set())
        r = analyze("Het bedrag is 1234.", "Het bedrag is 1.234.", source_locale="auto")
        self.assertIn("QTY_AMBIGUOUS", serious(r))
        r = analyze("Het bedrag is 1234.", "Het bedrag is 1.234.", source_locale="nl-NL")
        self.assertEqual(serious(r), set())


if __name__ == "__main__":
    unittest.main()
