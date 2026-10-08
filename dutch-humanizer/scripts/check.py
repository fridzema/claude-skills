#!/usr/bin/env python3
"""Mechanische controle van dutch-humanizer-output.

Gebruik:
    python3 scripts/check.py OUTPUT.txt [--input INPUT.txt] [opties]

Opties:
    --input PAD           brontekst; nodig voor alle vergelijkende controles
    --style neutral|strict
                          neutral (standaard): nieuwe streepjes, emoji, pijlen en
                          gekrulde aanhalingstekens zijn INFO.
                          strict: ze zijn ERROR (de strikte huisstijl).
    --allow-dashes        bij --style strict: streepjes toch toestaan
    --source-lang auto|nl|other
                          taal van de input; bij een niet-Nederlandse input
                          (vertaling) slaat het script woordgebonden controles over
    --fail-on-warning     exit 1 ook bij WARNING (handig in CI)

Niveaus:
    ERROR    zekere mechanische fout: gewijzigde code, verdwenen frontmatter,
             lege output, verboden teken onder --style strict
    WARNING  mogelijke betekenisverandering; lees de passage en beoordeel zelf
    INFO     stijlopmerking zonder oordeel

Exitcodes: 0 = geen ERROR, 1 = ERROR (of WARNING met --fail-on-warning),
2 = gebruiksfout of onleesbaar bestand.

Dit script vergelijkt tekens, getallen en woorden. Het kan niet vaststellen of
de betekenis gelijk is gebleven; dat blijft een redactionele beoordeling.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

EXIT_OK, EXIT_FAIL, EXIT_USAGE = 0, 1, 2
LEVELS = ("ERROR", "WARNING", "INFO")


@dataclass(frozen=True)
class Finding:
    level: str
    message: str
    line: int | None = None
    where: str = "output"

    def format(self) -> str:
        loc = f"{self.where} regel {self.line}: " if self.line else ""
        return f"{self.level} {loc}{self.message}"


@dataclass(frozen=True)
class Span:
    start: int
    end: int
    kind: str  # frontmatter, code, url, email, quote, escape
    text: str


def line_at(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


# ---------------------------------------------------------------------------
# Beschermde inhoud herkennen. Alles werkt met offsets in de oorspronkelijke
# tekst, zodat regelnummers kloppen.
# ---------------------------------------------------------------------------

FENCE = re.compile(r"^[ ]{0,3}(`{3,}|~{3,})(.*)$")
LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s")
INLINE_CODE = re.compile(r"(`+)(?!`)(.+?)(?<!`)\1(?!`)")
MD_LINK_TARGET = re.compile(r"\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
URL = re.compile(r"(?:https?://|www\.)[^\s<>()\"'\]]+")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
ESCAPE = re.compile(r"\\[\\`*_{}\[\]()#+\-.!|\"'<>~]")
QUOTES = [
    re.compile("“([^”\n]+)”"),
    re.compile("„([^“”\n]+)[“”]"),
    re.compile("‘([^’\n]*\\s[^’\n]*)’"),
    re.compile(r"\"([^\"\n]+)\""),
    re.compile(r"(?:(?<=^)|(?<=[\s(]))'([^'\n]*\s[^'\n]*)'(?=$|[\s.,;:!?)])", re.M),
]


def _lines_with_offsets(text: str) -> list[tuple[int, str]]:
    out, pos = [], 0
    for line in text.split("\n"):
        out.append((pos, line))
        pos += len(line) + 1
    return out


def _overlaps(start: int, end: int, spans: list[Span]) -> bool:
    return any(start < s.end and s.start < end for s in spans)


def block_spans(text: str) -> list[Span]:
    """Frontmatter, fenced code (``` en ~~~) en ingesprongen code."""
    spans: list[Span] = []
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            close = text.find("\n", end + 4)
            close = len(text) if close == -1 else close
            spans.append(Span(0, close, "frontmatter", text[:close]))

    lines = _lines_with_offsets(text)
    i = 0
    prev_blank = True
    last_text_is_list = False
    while i < len(lines):
        start, line = lines[i]
        if _overlaps(start, start + len(line), spans):
            i += 1
            continue
        fence = FENCE.match(line)
        if fence:
            marker = fence.group(1)
            j = i + 1
            while j < len(lines):
                close = FENCE.match(lines[j][1])
                if (close and close.group(1)[0] == marker[0] and len(close.group(1)) >= len(marker)
                        and not close.group(2).strip()):
                    break
                j += 1
            j = min(j, len(lines) - 1)
            end = lines[j][0] + len(lines[j][1])
            body = "\n".join(l for _, l in lines[i + 1:j])
            spans.append(Span(start, end, "code", body))
            i = j + 1
            prev_blank = False
            continue
        if re.match(r"^( {4}|\t)", line) and line.strip() and prev_blank and not last_text_is_list:
            j = i
            while j + 1 < len(lines) and (re.match(r"^( {4}|\t)", lines[j + 1][1]) or not lines[j + 1][1].strip()):
                j += 1
            while j > i and not lines[j][1].strip():
                j -= 1
            end = lines[j][0] + len(lines[j][1])
            body = "\n".join(re.sub(r"^( {4}|\t)", "", l) for _, l in lines[i:j + 1])
            spans.append(Span(start, end, "code", body))
            i = j + 1
            prev_blank = False
            continue
        if line.strip():
            last_text_is_list = bool(LIST_ITEM.match(line)) or (last_text_is_list and line.startswith((" ", "\t")))
        prev_blank = not line.strip()
        i += 1
    return spans


def inline_spans(text: str, taken: list[Span]) -> list[Span]:
    spans: list[Span] = []

    def add(start: int, end: int, kind: str, value: str) -> None:
        if not _overlaps(start, end, taken + spans):
            spans.append(Span(start, end, kind, value))

    for m in INLINE_CODE.finditer(text):
        if "\n\n" not in m.group(0):
            add(m.start(), m.end(), "code", m.group(2).strip())
    for m in MD_LINK_TARGET.finditer(text):
        add(m.start(1), m.end(1), "url", m.group(1))
    for m in URL.finditer(text):
        value = m.group(0).rstrip(".,;:!?")
        add(m.start(), m.start() + len(value), "url", value)
    for m in EMAIL.finditer(text):
        value = m.group(0).rstrip(".")
        add(m.start(), m.start() + len(value), "email", value)
    for m in ESCAPE.finditer(text):
        add(m.start(), m.end(), "escape", m.group(0))
    return spans


def quote_spans(text: str, taken: list[Span]) -> list[Span]:
    spans: list[Span] = []
    for pattern in QUOTES:
        for m in pattern.finditer(text):
            if not _overlaps(m.start(), m.end(), taken + spans):
                spans.append(Span(m.start(), m.end(), "quote", m.group(1)))
    return spans


@dataclass
class Parsed:
    text: str
    spans: list[Span]
    masked_code: str  # code, frontmatter, URL's, e-mail en escapes vervangen door spaties
    masked_all: str  # idem, plus citaten

    def of_kind(self, *kinds: str) -> list[Span]:
        return [s for s in self.spans if s.kind in kinds]


def mask(text: str, spans: list[Span]) -> str:
    chars = list(text)
    for s in spans:
        for k in range(s.start, s.end):
            if chars[k] != "\n":
                chars[k] = " "
    return "".join(chars)


def parse(text: str) -> Parsed:
    blocks = block_spans(text)
    inline = inline_spans(text, blocks)
    quotes = quote_spans(text, blocks + inline)
    code_like = blocks + inline
    return Parsed(text, code_like + quotes, mask(text, code_like), mask(text, code_like + quotes))


# ---------------------------------------------------------------------------
# Getallen, datums, tijden
# ---------------------------------------------------------------------------

MONTHS = {
    "januari": 1, "februari": 2, "maart": 3, "april": 4, "mei": 5, "juni": 6, "juli": 7,
    "augustus": 8, "september": 9, "oktober": 10, "november": 11, "december": 12,
    "jan": 1, "feb": 2, "mrt": 3, "apr": 4, "jun": 6, "jul": 7, "aug": 8, "sep": 9,
    "sept": 9, "okt": 10, "nov": 11, "dec": 12,
    "january": 1, "february": 2, "march": 3, "may": 5, "june": 6, "july": 7, "august": 8,
    "october": 10, "mar": 3, "oct": 10,
}
WEEKDAYS = {
    "maandag": "maandag", "dinsdag": "dinsdag", "woensdag": "woensdag", "donderdag": "donderdag",
    "vrijdag": "vrijdag", "zaterdag": "zaterdag", "zondag": "zondag",
    "monday": "maandag", "tuesday": "dinsdag", "wednesday": "woensdag", "thursday": "donderdag",
    "friday": "vrijdag", "saturday": "zaterdag", "sunday": "zondag",
}
MONTH_RE = "|".join(sorted(MONTHS, key=len, reverse=True))
DATE_PATTERNS = [
    ("iso", re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")),
    ("numeric", re.compile(r"\b(\d{1,2})[-/.](\d{1,2})[-/.](\d{2,4})\b")),
    ("nl", re.compile(rf"\b(\d{{1,2}})\s+({MONTH_RE})\b\.?(?:\s+(\d{{4}}))?", re.I)),
    ("en", re.compile(rf"\b({MONTH_RE})\.?\s+(\d{{1,2}})(?:st|nd|rd|th)?\b(?:,?\s+(\d{{4}}))?", re.I)),
    ("time", re.compile(r"\b([01]?\d|2[0-3]):([0-5]\d)\b(?:\s?uur)?")),
    ("time", re.compile(r"\b([01]?\d|2[0-3])\.([0-5]\d)\s?uur\b")),
    ("hour", re.compile(r"\b([01]?\d|2[0-3])\s?uur\b")),
    ("ampm", re.compile(r"\b(1[0-2]|0?[1-9])(?::([0-5]\d))?\s?([ap])\.?m\.?(?!\w)", re.I)),
    ("weekday", re.compile(r"\b(" + "|".join(WEEKDAYS) + r")\b", re.I)),
]
NUMBER_WORDS = {
    "één": 1, "twee": 2, "drie": 3, "vier": 4, "vijf": 5, "zes": 6, "zeven": 7, "acht": 8,
    "negen": 9, "tien": 10, "elf": 11, "twaalf": 12, "dertien": 13, "veertien": 14,
    "vijftien": 15, "twintig": 20, "dertig": 30, "veertig": 40, "vijftig": 50,
    "honderd": 100, "duizend": 1000,
    "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
    "ten": 10, "eleven": 11, "twelve": 12, "twenty": 20, "thirty": 30, "hundred": 100,
    "thousand": 1000,
}
UNIT_SYNONYMS = {
    "%": "%", "procent": "%", "percent": "%",
    "€": "€", "euro": "€", "eur": "€", "$": "$", "dollar": "$", "£": "£",
    "uur": "uur", "u": "uur", "hour": "uur", "hours": "uur",
    "min": "min", "minuut": "min", "minuten": "min", "minutes": "min",
    "sec": "s", "seconde": "s", "seconden": "s", "s": "s", "ms": "ms",
    "dag": "dag", "dagen": "dag", "days": "dag", "day": "dag",
    "werkdag": "werkdag", "werkdagen": "werkdag",
    "week": "week", "weken": "week", "weeks": "week",
    "maand": "maand", "maanden": "maand", "months": "maand",
    "jaar": "jaar", "jaren": "jaar", "years": "jaar",
    "km": "km", "m": "m", "cm": "cm", "mm": "mm", "kg": "kg", "g": "g",
    "kb": "kb", "mb": "mb", "gb": "gb", "tb": "tb", "keer": "keer", "stuks": "stuks",
}
UNIT_RE = "|".join(sorted((re.escape(u) for u in UNIT_SYNONYMS if u not in "€$£"), key=len, reverse=True))
NUMBER = re.compile(
    r"(?<![\w.,])([€$£]\s?)?(\d+(?:[.,]\d+)*)(?![\w])(?:\s?(" + UNIT_RE + r")(?![\w]))?", re.I)
NUMBER_WORD = re.compile(r"(?<!\w)(" + "|".join(NUMBER_WORDS) + r")(?!\w)", re.I)


@dataclass(frozen=True)
class Value:
    key: str
    shown: str
    unit: str
    pos: int


def _date_key(kind: str, m: re.Match[str]) -> str:
    g = m.groups()
    if kind == "iso":
        return f"d:{int(g[2])}-{int(g[1])}-{g[0]}"
    if kind == "numeric":
        return f"n:{int(g[0])}/{int(g[1])}/{g[2]}"
    if kind == "nl":
        return f"d:{int(g[0])}-{MONTHS[g[1].lower()]}" + (f"-{g[2]}" if g[2] else "")
    if kind == "en":
        return f"d:{int(g[1])}-{MONTHS[g[0].lower()]}" + (f"-{g[2]}" if g[2] else "")
    if kind == "time":
        return f"t:{int(g[0])}:{g[1]}"
    if kind == "hour":
        return f"t:{int(g[0])}:00"
    if kind == "ampm":
        hour = int(g[0]) % 12 + (12 if g[2].lower() == "p" else 0)
        return f"t:{hour}:{g[1] or '00'}"
    return f"w:{WEEKDAYS[g[0].lower()]}"


def dates_and_times(text: str) -> list[Value]:
    found: list[Value] = []
    taken: list[tuple[int, int]] = []
    for kind, pattern in DATE_PATTERNS:
        for m in pattern.finditer(text):
            if any(m.start() < e and s < m.end() for s, e in taken):
                continue
            taken.append((m.start(), m.end()))
            found.append(Value(_date_key(kind, m), m.group(0).strip(), "", m.start()))
    return found


def numbers(text: str, skip: list[Value]) -> list[Value]:
    skip_ranges = [(v.pos, v.pos + len(v.shown)) for v in skip]
    found: list[Value] = []
    for m in NUMBER.finditer(text):
        if any(m.start(2) < e and s < m.end(2) for s, e in skip_ranges):
            continue
        line_start = text.rfind("\n", 0, m.start()) + 1
        if not text[line_start:m.start()].strip(" \t>#") and re.match(r"\d+[.)]\s", text[m.start():]):
            continue  # nummering van een lijst
        digits = re.sub(r"\D", "", m.group(2)).lstrip("0") or "0"
        unit = ""
        if m.group(1):
            unit = UNIT_SYNONYMS[m.group(1).strip()]
        elif m.group(3):
            unit = UNIT_SYNONYMS.get(m.group(3).lower(), "")
        found.append(Value(digits, m.group(0).strip(), unit, m.start()))
    for m in NUMBER_WORD.finditer(text):
        if any(m.start() < e and s < m.end() for s, e in skip_ranges):
            continue
        found.append(Value(str(NUMBER_WORDS[m.group(1).lower()]), m.group(1), "", m.start()))
    return found


# ---------------------------------------------------------------------------
# Woordgebonden signalen voor betekenis
# ---------------------------------------------------------------------------

TERM_GROUPS = {
    "ontkenning": ["niet", "geen", "nooit", "niets", "niemand", "nergens", "noch", "zonder"],
    "voorwaarde of uitzondering": ["tenzij", "mits", "indien", "zodra", "alleen als", "uitsluitend als",
                                   "op voorwaarde dat", "behalve", "met uitzondering van"],
    "onzekerheid": ["mogelijk", "misschien", "wellicht", "waarschijnlijk", "vermoedelijk", "lijkt",
                    "lijken", "schijnt", "eventueel", "naar verwachting", "vermoeden"],
    "verplichting": ["moet", "moeten", "verplicht", "dient", "dienen", "vereist", "verboden"],
    "termijn of volgorde": ["uiterlijk", "vóór", "voordat", "binnen", "na", "nadat", "vanaf", "sinds",
                            "tot en met", "t/m"],
}


# Groepen waarin een signaalwoord meestal door een ander uit dezelfde groep vervangen kan worden
# ("mits" door "alleen als", "verplicht" door "moet"). Bij ontkenning, onzekerheid en termijn
# kan zo'n vervanging de betekenis veranderen ("binnen" wordt "na"), dus daar blijft het WARNING.
INTERCHANGEABLE = {"voorwaarde of uitzondering", "verplichting"}


def term_counts(text: str) -> dict[str, Counter[str]]:
    low = text.lower()
    result: dict[str, Counter[str]] = {}
    for group, terms in TERM_GROUPS.items():
        counter: Counter[str] = Counter()
        for term in terms:
            # Bijvoeglijke vormen tellen mee: "vermoedelijke", "waarschijnlijke", "eventuele".
            suffix = r"e?" if term.endswith(("lijk", "eel")) else ""
            n = len(re.findall(r"(?<![\w])" + re.escape(term) + suffix + r"(?![\w])", low))
            if n:
                counter[term] = n
        result[group] = counter
    return result


def looks_dutch(text: str) -> bool:
    words = re.findall(r"[a-zà-ÿ]+", text.lower())
    nl = sum(w in {"de", "het", "een", "en", "van", "is", "dat", "niet", "op", "met", "voor", "je", "we", "zijn"}
             for w in words)
    en = sum(w in {"the", "and", "of", "is", "to", "that", "not", "for", "with", "it", "we", "this", "are"}
             for w in words)
    return nl >= en


# ---------------------------------------------------------------------------
# Namen
# ---------------------------------------------------------------------------

CAP_WORD = re.compile("(?<![\\w'’-])([A-ZÀ-Ý][\\w'’-]*\\w|[A-Z])")
SALUTATIONS = {"hoi", "hallo", "beste", "geachte", "groet", "groeten", "met", "dag", "hey", "dear", "hi"}
# Woorden die vaak een zin openen; met hoofdletter zijn ze zelden een naam.
SENTENCE_STARTERS = {
    "hierbij", "graag", "zoals", "wij", "we", "ik", "u", "jij", "je", "het", "de", "een", "dit", "deze", "dat",
    "die", "er", "als", "zodra", "mocht", "indien", "bedankt", "dank", "volgens", "daarom", "daarnaast", "ook",
    "maar", "en", "of", "want", "omdat", "toen", "nu", "vanaf", "sinds", "tot", "op", "in", "bij", "voor", "na",
    "om", "over", "uit", "door", "zie", "let", "lees", "stuur", "maak", "vraag", "kun", "kunt", "kan", "wil",
    "heeft", "hebt", "is", "zijn", "was", "werd", "wordt", "geen", "niet", "alle", "elke", "onze", "ons", "jullie",
    "hun", "hoe", "wat", "wie", "waar", "wanneer", "waarom", "excuus", "sorry", "fijn", "goed", "top", "helaas",
    "klopt", "eens", "the", "this", "it", "we", "please",
}


def proper_names(masked: str) -> dict[str, int]:
    """Woorden met hoofdletter die niet aan het begin van een zin staan."""
    names: dict[str, int] = {}
    for m in CAP_WORD.finditer(masked):
        word = m.group(1)
        low = word.lower()
        if (len(word) < 2 or low in SALUTATIONS or low in SENTENCE_STARTERS or low in WEEKDAYS
                or (low in MONTHS and len(low) > 4)):
            continue
        line_start = masked.rfind("\n", 0, m.start()) + 1
        line = masked[line_start:].split("\n", 1)[0]
        before = masked[line_start:m.start()]
        if line.lstrip().startswith("#"):
            continue
        at_line_start = not before.strip(" \t>*-+#0123456789.)\"'(“„‘")
        after_punct = re.search("[.!?:;]\\s*[\"'(“„‘]?\\s*$", before) is not None
        if after_punct:
            continue
        if at_line_start and len(line.split()) > 3:
            continue
        names.setdefault(word, m.start())
    return names


# ---------------------------------------------------------------------------
# Typografie
# ---------------------------------------------------------------------------

TYPO = {
    "em-dash": re.compile("—"),
    "en-dash": re.compile("(?<![\\d\\s])\\s?–|–(?!\\s?\\d)"),
    "spatie-streepje-spatie": re.compile(r"(?<=\S) (?:-|--) (?=\S)"),
    "emoji": re.compile("[\U0001F300-\U0001FAFF\U0001F000-\U0001F2FF☀-➿⭐⬆]"),
    "pijl": re.compile("[←-↙⇒⇔➡➜➔]"),
    "gekruld aanhalingsteken": re.compile("[“”‘„‚]|(?<!\\w)’|’(?!\\w)"),
}
DASH_KINDS = {"em-dash", "en-dash", "spatie-streepje-spatie"}
RANGE_EN_DASH = re.compile("(?<=\\d)\\s?–\\s?(?=\\d)")


def typography(parsed: Parsed, style: str) -> dict[str, list[int]]:
    # Aanhalingstekens zelf staan buiten de citaatmasker; de inhoud van citaten niet.
    hits = {kind: [m.start() for m in p.finditer(parsed.masked_code if kind == "gekruld aanhalingsteken"
                                                 else parsed.masked_all)]
            for kind, p in TYPO.items()}
    if style == "strict":
        hits["en-dash"] = sorted(set(hits["en-dash"]) | {m.start() for m in RANGE_EN_DASH.finditer(parsed.masked_all)})
    return hits


# ---------------------------------------------------------------------------
# Controle
# ---------------------------------------------------------------------------

def _norm_ws(text: str) -> str:
    return " ".join(text.split())


def _norm_quotes(text: str) -> str:
    return _norm_ws(re.sub("[“”„‚‘’\"']", "", text))


def _has_word(word: str, text_low: str) -> bool:
    return re.search(r"(?<!\w)" + re.escape(word.lower()) + r"(?!\w)", text_low) is not None


def check(output: str, source: str | None = None, style: str = "neutral",
          allow_dashes: bool = False, source_lang: str = "auto") -> list[Finding]:
    if source is not None and source.strip() and not output.strip():
        return [Finding("ERROR", "de output is leeg terwijl de input tekst bevat")]

    findings: list[Finding] = []
    out = parse(output)
    src = parse(source) if source is not None else None
    dutch_source = True
    if src is not None:
        dutch_source = source_lang == "nl" or (source_lang == "auto" and looks_dutch(src.masked_all))
        if not dutch_source:
            findings.append(Finding("INFO", "input lijkt niet Nederlands; controles op ontkenning, voorwaarden, "
                                            "onzekerheid, termijnen en verdwenen namen zijn overgeslagen"))

    # Typografie, alleen wat nieuw is ten opzichte van de input.
    out_typo = typography(out, style)
    src_typo = typography(src, style) if src else {k: [] for k in out_typo}
    for kind, positions in out_typo.items():
        already = len(src_typo.get(kind, []))
        if len(positions) <= already:
            continue
        forbidden = style == "strict" and not (allow_dashes and kind in DASH_KINDS)
        level = "ERROR" if forbidden else "INFO"
        reason = "niet toegestaan in --style strict" if forbidden else "controleer of het past bij kanaal en stem"
        findings.append(Finding(level, f"{len(positions) - already}x nieuw: {kind} ({reason})",
                                line_at(output, positions[already])))

    out_names_all = proper_names(out.masked_code)
    known_names = set(out_names_all) | (set(proper_names(src.masked_code)) if src else set())
    src_has_colon_caps = src is not None and re.search(r":\s+[A-Z]", src.masked_all) is not None
    for n, line in enumerate(out.masked_all.split("\n"), 1):
        heading = re.match(r"\s{0,3}#{1,6}\s+(.*)", line)
        if heading:
            words = [w for w in heading.group(1).split()[1:] if len(w) > 3 and w.isalpha()]
            if len(words) >= 2 and all(w[0].isupper() for w in words):
                findings.append(Finding("INFO", f"kop in Title Case: {line.strip()}", n))
        if src_has_colon_caps:
            continue  # de input doet het ook; volg de input
        for m in re.finditer(r":[ \t]+([A-Z][a-z]+)\b", line):
            if m.group(1) in known_names:
                continue
            findings.append(Finding("INFO", f"hoofdletter na dubbele punt ('{m.group(0).strip()}'); "
                                            "gangbaar is een kleine letter, behalve bij een citaat, een eigennaam "
                                            "of een zelfstandige zin", n))

    if src is None:
        return findings

    # Beschermde inhoud.
    out_code = {_norm_ws(s.text) for s in out.of_kind("code")}
    out_plain = _norm_ws(output)
    for s in src.of_kind("code"):
        body = _norm_ws(s.text)
        if not body or body in out_code:
            continue
        if body in out_plain:
            findings.append(Finding("WARNING", f"code staat er nog, maar niet meer als code: {body[:60]}",
                                    line_at(source, s.start), "input"))
        else:
            findings.append(Finding("ERROR", f"code gewijzigd of verwijderd: {body[:60]}",
                                    line_at(source, s.start), "input"))
    for s in src.of_kind("frontmatter"):
        if s.text not in output:
            findings.append(Finding("ERROR", "YAML-frontmatter gewijzigd of verwijderd", 1, "input"))
    out_quotes_plain = _norm_quotes(output)
    for s in src.of_kind("quote"):
        inner = _norm_quotes(s.text)
        if len(inner.split()) >= 2 and inner not in out_quotes_plain:
            findings.append(Finding("WARNING", f"citaat of letterlijke tekst niet ongewijzigd teruggevonden: "
                                               f"\"{inner[:60]}\"", line_at(source, s.start), "input"))
    for kind, label in (("url", "URL"), ("email", "e-mailadres")):
        src_vals = {s.text: s.start for s in src.of_kind(kind)}
        out_vals = {s.text: s.start for s in out.of_kind(kind)}
        for value, pos in src_vals.items():
            if value not in out_vals:
                findings.append(Finding("WARNING", f"{label} uit de input ontbreekt of is gewijzigd: {value}",
                                        line_at(source, pos), "input"))
        for value, pos in out_vals.items():
            if value not in src_vals:
                findings.append(Finding("WARNING", f"{label} staat niet in de input: {value}",
                                        line_at(output, pos)))

    # Datums, tijden en weekdagen.
    src_dates = dates_and_times(src.masked_code)
    out_dates = dates_and_times(out.masked_code)
    src_keys = {v.key for v in src_dates}
    out_keys = {v.key for v in out_dates}
    reported: set[str] = set()
    for v in src_dates:
        if v.key not in out_keys and v.key not in reported:
            reported.add(v.key)
            findings.append(Finding("WARNING", f"datum, tijd of dag ontbreekt of is gewijzigd: {v.shown}",
                                    line_at(source, v.pos), "input"))
    for v in out_dates:
        if v.key not in src_keys and v.key not in reported:
            reported.add(v.key)
            findings.append(Finding("WARNING", f"datum, tijd of dag staat niet in de input: {v.shown}",
                                    line_at(output, v.pos)))

    # Getallen, percentages, eenheden.
    src_nums = numbers(src.masked_code, src_dates)
    out_nums = numbers(out.masked_code, out_dates)
    src_num_keys = {v.key for v in src_nums}
    out_num_keys = {v.key for v in out_nums}
    removed = [v for v in src_nums if v.key not in out_num_keys]
    added = [v for v in out_nums if v.key not in src_num_keys]
    removed_pct = [v for v in removed if v.unit == "%"]
    added_pct = [v for v in added if v.unit == "%"]
    if removed_pct and added_pct:
        findings.append(Finding("WARNING", f"percentage mogelijk veranderd: {removed_pct[0].shown} wordt "
                                           f"{added_pct[0].shown}", line_at(output, added_pct[0].pos)))
        removed.remove(removed_pct[0])
        added.remove(added_pct[0])
    for v in removed:
        kind = "percentage" if v.unit == "%" else "getal"
        findings.append(Finding("WARNING", f"{kind} uit de input ontbreekt: {v.shown}",
                                line_at(source, v.pos), "input"))
    for v in added:
        kind = "percentage" if v.unit == "%" else "getal"
        findings.append(Finding("WARNING", f"{kind} staat niet in de input: {v.shown}", line_at(output, v.pos)))
    src_units: dict[str, set[str]] = {}
    for v in src_nums:
        if v.unit:
            src_units.setdefault(v.key, set()).add(v.unit)
    for v in out_nums:
        if v.unit and v.key in src_units and v.unit not in src_units[v.key]:
            findings.append(Finding("WARNING", f"eenheid of valuta bij {v.shown} wijkt af van de input "
                                               f"({', '.join(sorted(src_units[v.key]))})", line_at(output, v.pos)))

    # Namen.
    src_low, out_low = src.masked_code.lower(), out.masked_code.lower()
    if dutch_source:
        for name, pos in proper_names(src.masked_code).items():
            if not _has_word(name, out_low):
                findings.append(Finding("WARNING", f"naam uit de input ontbreekt: {name}",
                                        line_at(source, pos), "input"))
    for name, pos in out_names_all.items():
        if not _has_word(name, src_low):
            findings.append(Finding("WARNING", f"naam staat niet in de input: {name}", line_at(output, pos)))

    # Ontkenning, voorwaarde, onzekerheid, verplichting, termijn.
    if dutch_source:
        src_terms, out_terms = term_counts(src.masked_code), term_counts(out.masked_code)
        src_als = len(re.findall(r"(?<!\w)als(?!\w)", src.masked_code.lower()))
        out_als = len(re.findall(r"(?<!\w)als(?!\w)", out.masked_code.lower()))
        for group in TERM_GROUPS:
            before, after = src_terms[group], out_terms[group]
            gone = [t for t in before if t not in after]
            new = [t for t in after if t not in before]
            replaced = sum(after.values()) >= sum(before.values()) and new
            if group == "voorwaarde of uitzondering" and gone and out_als - src_als >= len(gone):
                replaced = True
                new = new or ["als"]
            if gone and replaced and group in INTERCHANGEABLE:
                findings.append(Finding("INFO", f"{group}: '{', '.join(gone)}' vervangen door '{', '.join(new)}'; "
                                                "meestal gelijkwaardig, controleer de zin"))
            elif gone:
                tail = f"; nieuw: '{', '.join(new)}'" if new else ""
                findings.append(Finding("WARNING", f"{group}: '{', '.join(gone)}' komt niet meer voor{tail}. "
                                                   "Mogelijk is de betekenis veranderd; controleer de zin"))
            elif sum(after.values()) < sum(before.values()):
                findings.append(Finding("WARNING", f"{group}: minder signaalwoorden dan in de input "
                                                   f"({sum(before.values())} naar {sum(after.values())}); "
                                                   "controleer of niets is weggevallen"))
            elif group in ("ontkenning", "voorwaarde of uitzondering") and new:
                findings.append(Finding("WARNING", f"{group}: nieuw in de output: '{', '.join(new)}'; "
                                                   "controleer of geen bewering is omgedraaid"))

    src_words, out_words = len(src.masked_all.split()), len(out.masked_all.split())
    if src_words >= 40 and out_words < 0.6 * src_words:
        findings.append(Finding("INFO", f"output is veel korter dan de input ({out_words} tegen {src_words} "
                                        "woorden); controleer of alleen opvulling is weggevallen"))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Mechanische controle van dutch-humanizer-output.")
    parser.add_argument("output", type=Path)
    parser.add_argument("--input", type=Path, help="brontekst, voor de vergelijkende controles")
    parser.add_argument("--style", choices=("neutral", "strict"), default="neutral")
    parser.add_argument("--allow-dashes", action="store_true",
                        help="bij --style strict: em-, en- en gedachtestreepjes toestaan")
    parser.add_argument("--source-lang", choices=("auto", "nl", "other"), default="auto")
    parser.add_argument("--fail-on-warning", action="store_true")
    args = parser.parse_args(argv)

    try:
        output = args.output.read_text(encoding="utf-8")
        source = args.input.read_text(encoding="utf-8") if args.input else None
    except (OSError, UnicodeDecodeError) as exc:
        print(f"ERROR kan bestand niet lezen: {exc}", file=sys.stderr)
        return EXIT_USAGE

    findings = check(output, source, args.style, args.allow_dashes, args.source_lang)
    findings.sort(key=lambda f: LEVELS.index(f.level))
    for f in findings:
        print(f.format())
    counts = Counter(f.level for f in findings)
    print(f"Samenvatting: {counts['ERROR']} ERROR, {counts['WARNING']} WARNING, {counts['INFO']} INFO. "
          "Een WARNING is een signaal om te controleren, geen bewijs dat de betekenis veranderde.")
    if counts["ERROR"] or (args.fail_on_warning and counts["WARNING"]):
        return EXIT_FAIL
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
