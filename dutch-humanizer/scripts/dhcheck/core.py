"""Kern van de controle: een pure functie zonder bestands- of netwerktoegang.

analyze(output, source, ...) geeft een Report met Findings. Een Finding heeft
een stabiele code, een ernst en de bron- en outputposities.

ERROR    vastgestelde schending van een mechanisch contract: gewijzigde of
         toegevoegde code bij herschrijven, gewijzigde frontmatter, lege
         output, verboden teken bij --style strict.
WARNING  mogelijke betekenisverandering; vraagt een inhoudelijk oordeel.
INFO     stijlobservatie of niet-uitgevoerde controle.

Nul meldingen betekent niet dat de betekenis klopt.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field

from . import markdown, quantities as qty, signals as sig

SCHEMA_VERSION = "1"
TASKS = ("rewrite", "create", "translate", "shorten", "summarize")
LEVELS = ("ERROR", "WARNING", "INFO")
NOTE = "Een WARNING is een signaal om te controleren, geen bewijs dat de betekenis veranderde. " \
       "Geen meldingen betekent niet dat de betekenis klopt."


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str
    message: str
    line: int | None = None
    where: str = "output"
    source_span: tuple[int, int] | None = None
    output_span: tuple[int, int] | None = None

    @property
    def level(self) -> str:  # compatibel met v0.6
        return self.severity

    def format(self) -> str:
        loc = f"{self.where} regel {self.line}: " if self.line else ""
        return f"{self.severity} {loc}[{self.code}] {self.message}"

    def as_dict(self) -> dict:
        return {"code": self.code, "severity": self.severity, "message": self.message, "where": self.where,
                "line": self.line,
                "source_span": list(self.source_span) if self.source_span else None,
                "output_span": list(self.output_span) if self.output_span else None}


@dataclass
class Report:
    task: str
    findings: list[Finding] = field(default_factory=list)
    checks_run: list[str] = field(default_factory=list)
    checks_skipped: dict[str, str] = field(default_factory=dict)

    def counts(self) -> Counter:
        return Counter(f.severity for f in self.findings)

    def as_dict(self) -> dict:
        c = self.counts()
        return {"schema_version": SCHEMA_VERSION, "tool": "dutch-humanizer/check", "task": self.task,
                "summary": {lvl: c.get(lvl, 0) for lvl in LEVELS},
                "checks_run": self.checks_run, "checks_skipped": self.checks_skipped,
                "findings": [f.as_dict() for f in self.findings], "note": NOTE}


# ---------------------------------------------------------------------------
# Taal
# ---------------------------------------------------------------------------

NL_WORDS = {"de", "het", "een", "en", "van", "is", "dat", "niet", "op", "met", "voor", "je", "we", "zijn", "u"}
EN_WORDS = {"the", "and", "to", "that", "not", "for", "with", "it", "this", "are", "you", "your", "our", "will"}


def detect_lang(text: str) -> str:
    words = re.findall(r"[a-zà-ÿ]+", text.lower())
    nl = sum(w in NL_WORDS for w in words)
    en = sum(w in EN_WORDS for w in words)
    # De skill is Nederlandstalig: zonder duidelijk Engels signaal geldt Nederlands.
    return "en" if en >= 2 and en > nl else "nl"


# ---------------------------------------------------------------------------
# Namen
# ---------------------------------------------------------------------------

CAP_WORD = re.compile("(?<![\\w'’-])([A-ZÀ-Ý][\\w'’-]*\\w|[A-Z])")
SALUTATIONS = {"hoi", "hallo", "beste", "geachte", "groet", "groeten", "met", "dag", "hey", "dear", "hi"}
SENTENCE_STARTERS = {
    "hierbij", "graag", "zoals", "wij", "we", "ik", "u", "jij", "je", "het", "de", "een", "dit", "deze", "dat",
    "die", "er", "als", "zodra", "mocht", "indien", "bedankt", "dank", "volgens", "daarom", "daarnaast", "ook",
    "maar", "en", "of", "want", "omdat", "toen", "nu", "vanaf", "sinds", "tot", "op", "in", "bij", "voor", "na",
    "om", "over", "uit", "door", "zie", "let", "lees", "stuur", "maak", "vraag", "kun", "kunt", "kan", "wil",
    "heeft", "hebt", "is", "zijn", "was", "werd", "wordt", "geen", "niet", "alle", "elke", "onze", "ons", "jullie",
    "hun", "hoe", "wat", "wie", "waar", "wanneer", "waarom", "excuus", "sorry", "fijn", "goed", "top", "helaas",
    "klopt", "eens", "the", "this", "it", "please",
}


def proper_names(masked: str) -> dict[str, int]:
    names: dict[str, int] = {}
    for m in CAP_WORD.finditer(masked):
        word = m.group(1)
        low = word.lower()
        if (len(word) < 2 or low in SALUTATIONS or low in SENTENCE_STARTERS or low in qty.WEEKDAYS
                or (low in qty.MONTHS and len(low) > 4)):
            continue
        line_start = masked.rfind("\n", max(0, m.start() - 400), m.start()) + 1
        line_end = masked.find("\n", m.end(), m.end() + 400)
        line = masked[line_start:line_end if line_end != -1 else m.end() + 400]
        before = masked[max(line_start, m.start() - 40):m.start()]
        if line.lstrip().startswith("#"):
            continue
        at_line_start = m.start() - line_start < 40 and not before.strip(" \t>*-+#0123456789.)\"'(“„‘")
        if re.search("[.!?:;]\\s*[\"'(“„‘]?\\s*$", before):
            continue
        # Korte regels zonder slotteken (ondertekening, naam) tellen wel; een korte zin niet.
        if at_line_start and (len(line.split()) > 3 or re.search(r"[.!?]\s*$", line)):
            continue
        names.setdefault(word, m.start())
    return names


def _has_word(word: str, low: str) -> bool:
    return re.search(r"(?<!\w)" + re.escape(word.lower()) + r"(?!\w)", low) is not None


# ---------------------------------------------------------------------------
# Typografie
# ---------------------------------------------------------------------------

TYPO = {
    "em-dash": ("TYPO_DASH", re.compile("—")),
    "en-dash": ("TYPO_DASH", re.compile("–")),
    "spatie-streepje-spatie": ("TYPO_DASH", re.compile(r"(?<=\S) (?:-|--) (?=\S)")),
    "emoji": ("TYPO_EMOJI", re.compile("[\U0001F300-\U0001FAFF\U0001F000-\U0001F2FF☀-➿⭐⬆]")),
    "pijl": ("TYPO_ARROW", re.compile("[←-↙⇒⇔➡➜➔]")),
}
CURLY = re.compile("[“”‘„‚]|(?<!\\w)’|’(?!\\w)")
RANGE_DASH = re.compile("(?<=\\d)\\s?–\\s?(?=\\d)")


def typography(parsed: markdown.Parsed, style: str) -> dict[str, tuple[str, list[int]]]:
    hits: dict[str, tuple[str, list[int]]] = {}
    for kind, (code, pattern) in TYPO.items():
        positions = [m.start() for m in pattern.finditer(parsed.masked_all)]
        if kind == "en-dash" and style != "strict":
            ranges = {m.start() + (1 if parsed.masked_all[m.start()] == " " else 0)
                      for m in RANGE_DASH.finditer(parsed.masked_all)}
            positions = [p for p in positions if p not in ranges]  # 9–17 is correcte typografie
        hits[kind] = (code, positions)
    hits["gekruld aanhalingsteken"] = ("TYPO_QUOTE", [m.start() for m in CURLY.finditer(parsed.masked_code)])
    return hits


# ---------------------------------------------------------------------------
# Analyse
# ---------------------------------------------------------------------------

def analyze(output: str, source: str | None = None, *, task: str | None = None, style: str = "neutral",
            allow_dashes: bool = False, source_lang: str = "auto", source_locale: str | None = None,
            target_locale: str | None = None) -> Report:
    task = task or ("rewrite" if source is not None else "create")
    if task not in TASKS:
        raise ValueError(f"onbekende taak: {task}")
    report = Report(task)
    f = report.findings
    has_source = source is not None and source.strip() != ""
    if source is not None and not has_source:
        report.checks_skipped["vergelijking"] = "lege bron"
    if not output.strip():
        if task == "create" or has_source:
            f.append(Finding("EMPTY_OUTPUT", "ERROR", "de output is leeg; er is geen tekst opgeleverd"
                             if not has_source else "de output is leeg terwijl de input tekst bevat"))
        report.checks_run.append("lege output")
        return report

    out = markdown.parse(output)
    src = markdown.parse(source) if has_source else None
    out_lang = "nl"
    src_lang = "nl"
    if src is not None:
        if source_lang == "nl":
            src_lang = "nl"
        elif source_lang == "other":
            src_lang = "en" if detect_lang(src.masked_all) == "en" else "other"
        else:
            src_lang = detect_lang(src.masked_all)
        if src_lang != "nl":
            f.append(Finding("LANG_SKIPPED", "INFO", "input lijkt niet Nederlands; controles op verdwenen namen "
                             "zijn overgeslagen" + ("" if src_lang == "en" else " en woordsignalen ook")))
    src_family = qty.locale_family(source_locale) if source_locale else ("en" if src_lang == "en" else "nl")
    if source_locale == "auto":
        src_family = "auto"
    out_family = qty.locale_family(target_locale) if target_locale else "nl"

    _typography(report, out, src, style, allow_dashes)
    _style_info(report, out, src)
    if src is None:
        report.checks_skipped["vergelijking met bron"] = "geen bron opgegeven"
        return report

    _protected(report, src, out, task)
    _dates(report, src, out, task)
    _quantities(report, src, out, task, src_family, out_family, src_lang)
    _names(report, src, out, task, src_lang)
    if src_lang in ("nl", "en"):
        _signals(report, src, out, task, src_lang)
    else:
        report.checks_skipped["woordsignalen"] = "brontaal niet Nederlands of Engels"
    src_words, out_words = len(src.masked_all.split()), len(out.masked_all.split())
    if task in ("rewrite", "translate") and src_words >= 40 and out_words < 0.6 * src_words:
        f.append(Finding("LENGTH_SHORT", "INFO", f"output is veel korter dan de input ({out_words} tegen "
                         f"{src_words} woorden); controleer of alleen opvulling is weggevallen"))
    order = {lvl: i for i, lvl in enumerate(LEVELS)}
    report.findings.sort(key=lambda x: order[x.severity])
    return report


def _removal_severity(task: str) -> str:
    """Verdwenen inhoud: WARNING, behalve bij gevraagde selectie of opstellen uit een briefing."""
    return "INFO" if task in ("summarize", "create") else "WARNING"


def _typography(report: Report, out: markdown.Parsed, src: markdown.Parsed | None, style: str,
                allow_dashes: bool) -> None:
    report.checks_run.append("typografie")
    out_t = typography(out, style)
    src_t = typography(src, style) if src else {}
    for kind, (code, positions) in out_t.items():
        if not positions:
            continue
        if style == "strict" and not (allow_dashes and code == "TYPO_DASH"):
            # Strikt: alle bewerkbare output telt, niet alleen nieuwe tekens.
            for p in positions:
                report.findings.append(Finding(code, "ERROR", f"{kind} niet toegestaan in --style strict",
                                               out.line_at(p), output_span=(p, p + 1)))
            continue
        already = len(src_t.get(kind, ("", []))[1])
        if len(positions) > already:
            p = positions[already]
            report.findings.append(Finding(code, "INFO", f"{len(positions) - already}x nieuw: {kind} "
                                           "(controleer of het past bij kanaal en stem)", out.line_at(p),
                                           output_span=(p, p + 1)))


def _style_info(report: Report, out: markdown.Parsed, src: markdown.Parsed | None) -> None:
    report.checks_run.append("stijl")
    known = set(proper_names(out.masked_code)) | (set(proper_names(src.masked_code)) if src else set())
    src_caps = src is not None and re.search(r":[ \t]+[A-Z]", src.masked_all) is not None
    for n, line in enumerate(out.masked_all.split("\n"), 1):
        heading = re.match(r"\s{0,3}#{1,6}\s+(.*)", line)
        if heading:
            words = [w for w in heading.group(1).split()[1:] if len(w) > 3 and w.isalpha()]
            if len(words) >= 2 and all(w[0].isupper() for w in words):
                report.findings.append(Finding("STYLE_TITLE_CASE", "INFO", f"kop in Title Case: {line.strip()}", n))
        if src_caps:
            continue
        for m in re.finditer(r":[ \t]+([A-Z][a-z]+)\b", line):
            if m.group(1) in known:
                continue
            report.findings.append(Finding(
                "STYLE_COLON_CAPITAL", "INFO",
                f"hoofdletter na dubbele punt ('{m.group(0).strip()}'); bij een verklaring volgt volgens "
                "Taaladvies een kleine letter, ook als er een volledige zin volgt. Uitzonderingen: citaat, "
                "eigennaam, opsomming van volledige zinnen", n))


def _protected(report: Report, src: markdown.Parsed, out: markdown.Parsed, task: str) -> None:
    report.checks_run.append("beschermde inhoud")
    f = report.findings
    # Code: letterlijk, met multipliciteit en volgorde.
    src_code = [s for s in src.code()]
    out_code = [s for s in out.code()]
    src_bodies = Counter(s.text for s in src_code if s.text.strip())
    out_bodies = Counter(s.text for s in out_code if s.text.strip())
    missing = src_bodies - out_bodies
    extra = out_bodies - src_bodies
    gone = [s for s in src_code if missing.get(s.text, 0) > 0 and not missing.subtract([s.text])]
    added = [s for s in out_code if extra.get(s.text, 0) > 0 and not extra.subtract([s.text])]
    prose_out = out.masked_code
    for s in list(gone):
        if s.text.strip() and s.text in prose_out:
            gone.remove(s)
            f.append(Finding("CODE_FORM_CHANGED", "WARNING", "code staat er nog, maar niet meer als code: "
                             f"{' '.join(s.text.split())[:60]}", src.line_at(s.start), "input",
                             source_span=(s.start, s.end)))
    strict = task not in ("summarize", "create")
    while gone and added and strict:
        s, o = gone.pop(0), added.pop(0)
        f.append(Finding("CODE_CHANGED", "ERROR", "code gewijzigd of verwijderd: "
                         f"{' '.join(s.text.split())[:50]} (in de output: {o.text.strip()[:50]!r})",
                         out.line_at(o.start), source_span=(s.start, s.end),
                         output_span=(o.start, o.end)))
    for s in gone:
        f.append(Finding("CODE_CHANGED", "ERROR" if strict else "INFO", "code gewijzigd of verwijderd: "
                         f"{' '.join(s.text.split())[:60]}", src.line_at(s.start), "input",
                         source_span=(s.start, s.end)))
    if task != "create":
        for o in added:
            f.append(Finding("CODE_ADDED", "ERROR", f"code staat niet in de input; bij taak '{task}' komt er geen "
                             f"nieuwe code bij: {' '.join(o.text.split())[:60]}", out.line_at(o.start),
                             output_span=(o.start, o.end)))
    missing = src_bodies - out_bodies
    extra = out_bodies - src_bodies
    if not missing and not extra:
        seq_src = [s.text for s in src_code if s.text.strip()]
        seq_out = [s.text for s in out_code if s.text.strip()]
        if seq_src != seq_out:
            f.append(Finding("CODE_ORDER_CHANGED", "WARNING", "codefragmenten staan in een andere volgorde; "
                             "controleer of ze nog bij de juiste instructie horen"))
    for s in src.of_kind("frontmatter"):
        if s.text not in out.text:
            f.append(Finding("FRONTMATTER_CHANGED", "ERROR", "YAML-frontmatter gewijzigd of verwijderd", 1, "input",
                             source_span=(s.start, s.end)))

    # Citaten: letterlijke inhoud, ook van één woord; aanhalingstekenstijl mag verschillen.
    src_q = Counter(s.text for s in src.of_kind("quote"))
    out_q = Counter(s.text for s in out.of_kind("quote"))
    gone_q = src_q - out_q
    for s in src.of_kind("quote"):
        if gone_q.get(s.text, 0) > 0:
            gone_q[s.text] -= 1
            sev = _removal_severity(task)
            f.append(Finding("QUOTE_CHANGED", sev, f"citaat of letterlijke tekst niet ongewijzigd teruggevonden: "
                             f"\"{s.text[:60]}\"", src.line_at(s.start), "input", source_span=(s.start, s.end)))
    new_q = out_q - src_q
    if task != "translate":
        for s in out.of_kind("quote"):
            if new_q.get(s.text, 0) > 0 and len(s.text.split()) > 1:
                new_q[s.text] -= 1
                f.append(Finding("QUOTE_ADDED", "WARNING", f"citaat staat niet in de input: \"{s.text[:60]}\"",
                                 out.line_at(s.start), output_span=(s.start, s.end)))

    # URL's, e-mailadressen, linkdoelen en paden.
    for kinds, label, code in ((("url", "link"), "URL", "URL"), (("email",), "e-mailadres", "EMAIL"),
                               (("path",), "pad", "PATH")):
        sv = Counter(s.text for s in src.of_kind(*kinds))
        ov = Counter(s.text for s in out.of_kind(*kinds))
        gone, new = sv - ov, ov - sv
        for s in src.of_kind(*kinds):
            if gone.get(s.text, 0) > 0:
                gone[s.text] -= 1
                f.append(Finding(f"{code}_REMOVED", _removal_severity(task),
                                 f"{label} uit de input ontbreekt of is gewijzigd: {s.text}",
                                 src.line_at(s.start), "input", source_span=(s.start, s.end)))
        for s in out.of_kind(*kinds):
            if new.get(s.text, 0) > 0:
                new[s.text] -= 1
                f.append(Finding(f"{code}_ADDED", "WARNING", f"{label} staat niet in de input: {s.text}",
                                 out.line_at(s.start), output_span=(s.start, s.end)))

    # Versienummers: letterlijk.
    sv = Counter(v for v, _ in qty.versions(src.masked_code))
    ov = Counter(v for v, _ in qty.versions(out.masked_code))
    for v in (sv - ov):
        f.append(Finding("VERSION_CHANGED", _removal_severity(task), f"versienummer ontbreekt of is gewijzigd: {v}"))
    for v in (ov - sv):
        f.append(Finding("VERSION_ADDED", "WARNING", f"versienummer staat niet in de input: {v}"))


def _without_versions(text: str) -> str:
    return qty.VERSION.sub(lambda m: " " * len(m.group(0)), text)


def _dates(report: Report, src: markdown.Parsed, out: markdown.Parsed, task: str) -> None:
    report.checks_run.append("datums en tijden")
    sd = qty.dates_and_times(_without_versions(src.masked_all))
    od = qty.dates_and_times(_without_versions(out.masked_all))
    sk, ok = Counter(d.key for d in sd), Counter(d.key for d in od)
    missing, extra = sk - ok, ok - sk
    for d in sd:
        if missing.get(d.key, 0) > 0:
            missing[d.key] -= 1
            what = "ontbreekt of is gewijzigd" if ok.get(d.key, 0) == 0 else "komt minder vaak voor"
            report.findings.append(Finding("DATE_REMOVED", _removal_severity(task),
                                           f"datum, tijd of dag {what}: {d.shown}", src.line_at(d.start), "input",
                                           source_span=(d.start, d.end)))
    for d in od:
        if extra.get(d.key, 0) > 0:
            extra[d.key] -= 1
            if sk.get(d.key, 0):
                report.findings.append(Finding("DATE_EXTRA_OCCURRENCE", "INFO",
                                               f"datum, tijd of dag staat vaker in de output: {d.shown}",
                                               out.line_at(d.start), output_span=(d.start, d.end)))
            else:
                report.findings.append(Finding("DATE_ADDED", "WARNING", f"datum, tijd of dag staat niet in de "
                                               f"input: {d.shown}", out.line_at(d.start), output_span=(d.start, d.end)))


def _qkey(q: qty.Quantity):
    return (q.value, q.unit)


def _quantities(report: Report, src: markdown.Parsed, out: markdown.Parsed, task: str,
                src_family: str, out_family: str, src_lang: str = "nl") -> None:
    report.checks_run.append("getallen en eenheden")
    f = report.findings
    s_text, o_text = _without_versions(src.masked_all), _without_versions(out.masked_all)
    sd = [(d.start, d.end) for d in qty.dates_and_times(s_text)]
    od = [(d.start, d.end) for d in qty.dates_and_times(o_text)]
    sq = qty.quantities(s_text, sd, src_family, src_lang)
    oq = qty.quantities(o_text, od, out_family, "nl")

    def kind(q: qty.Quantity) -> str:
        return "percentage" if q.unit in ("%", "procentpunt") else "getal"

    # Dubbelzinnige notatie: alleen melden als de notatie niet letterlijk terugkomt.
    out_raw = Counter(q.raw for q in oq)
    for q in sq:
        if q.status == "ambiguous":
            if out_raw.get(q.raw, 0) > 0:
                out_raw[q.raw] -= 1
                continue
            opts = " of ".join(str(c) for c in q.candidates) or "onbekend"
            f.append(Finding("QTY_AMBIGUOUS", "WARNING", f"notatie '{q.raw}' is dubbelzinnig (mogelijk {opts}); "
                             "de output gebruikt een andere notatie. Controleer de waarde of geef de locale op "
                             "met --source-locale", src.line_at(q.start), "input", source_span=(q.start, q.end)))
    for q in oq:
        if q.status == "ambiguous" and q.raw not in {x.raw for x in sq}:
            f.append(Finding("QTY_AMBIGUOUS", "WARNING", f"notatie '{q.raw}' is dubbelzinnig in de output",
                             out.line_at(q.start), output_span=(q.start, q.end)))

    s_rest = [q for q in sq if q.value is not None]
    o_rest = [q for q in oq if q.value is not None]
    s_amb = {q.raw for q in sq if q.value is None}
    amb_values = {c for q in sq if q.value is None for c in q.candidates}
    o_rest = [q for q in o_rest if not (q.raw in s_amb or q.value in amb_values)]

    # 1. Gelijke waarde en eenheid: koppelen, precisie en operator vergelijken.
    pairs = []
    remaining = list(o_rest)
    unmatched_s = []
    for q in s_rest:
        match = next((o for o in remaining if _qkey(o) == _qkey(q)), None)
        if match is None:
            unmatched_s.append(q)
            continue
        remaining.remove(match)
        pairs.append((q, match))
    for s, o in pairs:
        if s.status != "word" and o.status != "word" and s.precision != o.precision:
            f.append(Finding("QTY_PRECISION_CHANGED", "WARNING", f"weergaveprecisie gewijzigd: {s.raw} werd {o.raw} "
                             "(zelfde numerieke waarde); controleer of de precisie ertoe doet",
                             out.line_at(o.start), source_span=(s.start, s.end), output_span=(o.start, o.end)))
        if s.operator != o.operator:
            f.append(Finding("QTY_OPERATOR_CHANGED", "WARNING", f"begrenzing bij {s.raw} gewijzigd: "
                             f"'{s.operator or 'geen'}' werd '{o.operator or 'geen'}'; controleer maximaal, minimaal "
                             "of ongeveer", out.line_at(o.start), source_span=(s.start, s.end),
                             output_span=(o.start, o.end)))

    # 2. Rest koppelen op teken en eenheid.
    unmatched_o = list(remaining)
    for s in list(unmatched_s):
        o = next((o for o in unmatched_o if o.value == -s.value and o.unit == s.unit and s.value != 0), None)
        code, msg = "QTY_SIGN_CHANGED", f"teken gewijzigd: {s.raw} werd {o.raw if o else ''}"
        if o is None:
            o = next((o for o in unmatched_o if o.value == s.value and o.unit != s.unit), None)
            if o is not None:
                if s.unit and not o.unit:
                    code, msg = "QTY_UNIT_REMOVED", f"eenheid verdwenen: {s.raw} werd {o.raw}"
                elif o.unit and not s.unit:
                    code, msg = "QTY_UNIT_ADDED", f"eenheid toegevoegd: {s.raw} werd {o.raw}"
                else:
                    code, msg = "QTY_UNIT_CHANGED", (f"eenheid of valuta bij {o.raw} wijkt af van de input "
                                                     f"({s.raw})")
        if o is None:
            continue
        unmatched_s.remove(s)
        unmatched_o.remove(o)
        f.append(Finding(code, "WARNING", msg + "; controleer de zin", out.line_at(o.start),
                         source_span=(s.start, s.end), output_span=(o.start, o.end)))

    # 3. Percentages die van waarde veranderden.
    pct_s = [q for q in unmatched_s if q.unit == "%"]
    pct_o = [q for q in unmatched_o if q.unit == "%"]
    if len(pct_s) == 1 and len(pct_o) == 1:
        s, o = pct_s[0], pct_o[0]
        f.append(Finding("QTY_VALUE_CHANGED", "WARNING", f"percentage mogelijk veranderd: {s.raw} wordt {o.raw}",
                         out.line_at(o.start), source_span=(s.start, s.end), output_span=(o.start, o.end)))
        unmatched_s.remove(s)
        unmatched_o.remove(o)

    # 4. Verdwenen en nieuwe waarden, met multipliciteit.
    out_keys = Counter(_qkey(q) for q in oq if q.value is not None)
    src_keys = Counter(_qkey(q) for q in sq if q.value is not None)
    for s in unmatched_s:
        if out_keys.get(_qkey(s)):
            code, msg = "QTY_OCCURRENCE_REMOVED", f"{s.raw} komt minder vaak voor dan in de input"
        else:
            code, msg = "QTY_REMOVED", f"{kind(s)} uit de input ontbreekt: {s.raw}"
        f.append(Finding(code, _removal_severity(task), msg, src.line_at(s.start), "input",
                         source_span=(s.start, s.end)))
    for o in unmatched_o:
        if src_keys.get(_qkey(o)):
            f.append(Finding("QTY_OCCURRENCE_ADDED", "INFO", f"{o.raw} komt vaker voor dan in de input",
                             out.line_at(o.start), output_span=(o.start, o.end)))
        else:
            f.append(Finding("QTY_ADDED", "WARNING", f"{kind(o)} staat niet in de input: {o.raw}",
                             out.line_at(o.start), output_span=(o.start, o.end)))

    # 5. Koppeling tussen waarde en zaak (heuristiek): onderscheidende woorden ervoor.
    uniq_s = {k: q for k, q in ((_qkey(q), q) for q in sq) if src_keys[k] == 1 and k[0] is not None}
    uniq_o = {k: q for k, q in ((_qkey(q), q) for q in oq) if out_keys.get(k) == 1 and k[0] is not None}
    shared = [k for k in uniq_s if k in uniq_o]
    order_src = sorted(shared, key=lambda k: uniq_s[k].start)
    order_out = sorted(shared, key=lambda k: uniq_o[k].start)
    if len(shared) >= 2 and order_src != order_out:
        for k in shared:
            own = set(uniq_s[k].context)
            others = set().union(*(set(uniq_s[j].context) for j in shared if j != k))
            distinct = own - others
            if distinct and not (distinct & set(uniq_o[k].context)):
                o = uniq_o[k]
                f.append(Finding("QTY_ASSOCIATION", "WARNING", f"{o.raw} staat mogelijk bij een andere zaak dan in de "
                                 f"input (daar bij: {', '.join(sorted(distinct))}); controleer de koppeling",
                                 out.line_at(o.start), source_span=(uniq_s[k].start, uniq_s[k].end),
                                 output_span=(o.start, o.end)))


def _names(report: Report, src: markdown.Parsed, out: markdown.Parsed, task: str, src_lang: str) -> None:
    report.checks_run.append("namen")
    src_low, out_low = src.masked_code.lower(), out.masked_code.lower()
    if src_lang != "nl":
        report.checks_skipped["verdwenen namen"] = "brontaal niet Nederlands"
    else:
        for name, pos in proper_names(src.masked_code).items():
            if not _has_word(name, out_low):
                report.findings.append(Finding("NAME_REMOVED", _removal_severity(task),
                                               f"naam uit de input ontbreekt: {name}", src.line_at(pos), "input",
                                               source_span=(pos, pos + len(name))))
    for name, pos in proper_names(out.masked_code).items():
        if not _has_word(name, src_low):
            report.findings.append(Finding("NAME_ADDED", "WARNING", f"naam staat niet in de input: {name}",
                                           out.line_at(pos), output_span=(pos, pos + len(name))))


SIG_CODES = {"ontkenning": "SIG_NEGATION", "verplichting": "SIG_OBLIGATION", "verbod": "SIG_PROHIBITION",
             "toestemming": "SIG_PERMISSION", "mogelijkheid (kunnen)": "SIG_ABILITY",
             "onzekerheid": "SIG_UNCERTAINTY", "voorwaarde of uitzondering": "SIG_CONDITION",
             "termijn of volgorde": "SIG_TEMPORAL"}


def _signals(report: Report, src: markdown.Parsed, out: markdown.Parsed, task: str, src_lang: str) -> None:
    report.checks_run.append("woordsignalen")
    s_sig = sig.signals(src.masked_all, src_lang)
    o_sig = sig.signals(out.masked_all, "nl")
    for label, gone, new, first, families in sig.compare(s_sig, o_sig):
        parts = []
        if gone:
            parts.append(f"'{', '.join(gone)}' komt niet meer voor")
        if new:
            parts.append(("nieuw: " if gone else "nieuw in de output: ") + f"'{', '.join(new)}'")
        notes = [sig.FAMILY_NOTE[x] for x in sorted(families) if x in sig.FAMILY_NOTE]
        cross = " (vergelijking over talen heen, extra onzeker)" if src_lang != "nl" else ""
        msg = f"{label}: " + "; ".join(parts) + ". Mogelijk is de betekenis veranderd; controleer de zin" + cross
        if notes:
            msg += ". Let op: " + "; ".join(notes)
        severity = "INFO" if task == "summarize" and not new else "WARNING"
        if families == {"ABLE"}:
            severity = "INFO"  # "kan/kunnen" wisselt vaak bij correcte parafrases; "kan niet" blijft WARNING
        line = src.line_at(first) if first is not None else None
        report.findings.append(Finding(SIG_CODES[label], severity, msg, line, "input" if line else "output"))


# ---------------------------------------------------------------------------
# Compatibiliteit met de v0.6-API
# ---------------------------------------------------------------------------

def check(output: str, source: str | None = None, style: str = "neutral", allow_dashes: bool = False,
          source_lang: str = "auto", **kwargs) -> list[Finding]:
    return analyze(output, source, style=style, allow_dashes=allow_dashes, source_lang=source_lang,
                   **kwargs).findings
