"""Getallen, eenheden, datums en tijden herkennen en vergelijken.

Waarden worden met decimal.Decimal uit de oorspronkelijke tekens opgebouwd,
nooit via float. De locale bepaalt welk scheidingsteken decimaal is. Bij een
onbekende locale blijft een notatie als "1.234" dubbelzinnig: dan volgt een
melding in plaats van een stilzwijgende gelijkstelling.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation

DECIMAL_SEP = {"nl": ",", "en": "."}


def locale_family(locale: str | None) -> str:
    """nl-NL, nl-BE, nl -> nl; en-US, en-GB, en -> en; overige -> auto."""
    if not locale:
        return "auto"
    base = locale.lower().split("-")[0].split("_")[0]
    return base if base in DECIMAL_SEP else "auto"


# Eenheden: hoofdlettergevoelig waar dat betekenis heeft (MB tegenover Mb).
UNIT_CANON = {
    "%": "%", "procent": "%", "percent": "%", "‰": "‰", "promille": "‰",
    "procentpunt": "procentpunt", "procentpunten": "procentpunt", "pp": "procentpunt",
    "percentage point": "procentpunt", "percentage points": "procentpunt",
    "€": "EUR", "EUR": "EUR", "euro": "EUR", "euros": "EUR", "$": "USD", "USD": "USD", "dollar": "USD",
    "dollars": "USD", "£": "GBP", "GBP": "GBP",
    "B": "B", "kB": "kB", "KB": "KB", "MB": "MB", "Mb": "Mb", "GB": "GB", "Gb": "Gb", "TB": "TB", "Tb": "Tb",
    "KiB": "KiB", "MiB": "MiB", "GiB": "GiB", "kbit": "kbit", "Mbit": "Mbit", "Gbit": "Gbit",
    "kbps": "kbps", "Mbps": "Mbps", "Gbps": "Gbps",
    "nm": "nm", "µm": "µm", "mm": "mm", "cm": "cm", "m": "m", "km": "km",
    "mg": "mg", "g": "g", "gram": "g", "kg": "kg", "kilo": "kg", "ton": "ton",
    "ml": "ml", "cl": "cl", "l": "l", "L": "l", "liter": "l", "m2": "m2", "m²": "m2", "m3": "m3", "m³": "m3",
    "°C": "°C", "°F": "°F", "graden": "graden", "graad": "graden", "degrees": "graden",
    "ms": "ms", "s": "s", "sec": "s", "seconde": "s", "seconden": "s", "seconds": "s",
    "min": "min", "minuut": "min", "minuten": "min", "minutes": "min",
    "uur": "uur", "u": "uur", "h": "uur", "hour": "uur", "hours": "uur",
    "dag": "dag", "dagen": "dag", "day": "dag", "days": "dag", "calendar days": "dag",
    "kalenderdag": "kalenderdag", "kalenderdagen": "kalenderdag",
    "werkdag": "werkdag", "werkdagen": "werkdag", "business days": "werkdag", "working days": "werkdag",
    "week": "week", "weken": "week", "weeks": "week", "maand": "maand", "maanden": "maand", "months": "maand",
    "kwartaal": "kwartaal", "jaar": "jaar", "jaren": "jaar", "year": "jaar", "years": "jaar",
    "stuks": "stuks", "keer": "keer", "maal": "keer", "times": "keer",
}
_UNIT_ALTS = sorted((re.escape(u) for u in UNIT_CANON if u not in "€$£"), key=len, reverse=True)
UNIT_AFTER = re.compile(r"[  ]?(" + "|".join(_UNIT_ALTS) + r")(?![\w²³])")

NUMBER = re.compile(
    r"(?P<sign>(?<![\w.,])[-−+])?"
    r"(?P<cur>[€$£][  ]?)?"
    r"(?<![\w.,/])(?P<num>\d+(?:[.,  ]\d+)*)"
    r"(?P<pct>[  ]?[%‰])?"
)
NUMBER_WORDS = {
    "één": 1, "twee": 2, "drie": 3, "vier": 4, "vijf": 5, "zes": 6, "zeven": 7, "acht": 8,
    "negen": 9, "tien": 10, "elf": 11, "twaalf": 12, "dertien": 13, "veertien": 14, "vijftien": 15,
    "twintig": 20, "dertig": 30, "veertig": 40, "vijftig": 50, "honderd": 100, "duizend": 1000,
    "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "twenty": 20, "thirty": 30, "hundred": 100, "thousand": 1000,
}
NL_NUMBER_WORDS = ("één", "twee", "drie", "vier", "vijf", "zes", "zeven", "acht", "negen", "tien", "elf", "twaalf",
                   "dertien", "veertien", "vijftien", "twintig", "dertig", "veertig", "vijftig", "honderd", "duizend")
NUMBER_WORD = {
    "nl": re.compile(r"(?<!\w)(" + "|".join(NL_NUMBER_WORDS) + r")(?!\w)", re.I),
    "en": re.compile(r"(?<!\w)(" + "|".join(w for w in NUMBER_WORDS if w not in NL_NUMBER_WORDS) + r")(?!\w)",
                     re.I),
}

OPERATORS = [
    ("max", r"maximaal|max\.|hooguit|ten hoogste|niet meer dan|at most|up to|no more than|maximum"),
    ("min", r"minimaal|min\.|minstens|ten minste|tenminste|op zijn minst|niet minder dan|at least|minimum"),
    ("gt", r"meer dan|ruim|boven de|more than|>"),
    ("lt", r"minder dan|nog geen|onder de|less than|<"),
    ("ge", r"≥|>="),
    ("le", r"≤|<="),
    ("approx", r"ongeveer|circa|ca\.|zo'n|rond de|±|about|approximately|around|roughly"),
]
OPERATOR_BEFORE = re.compile(r"(?:^|(?<=[\s(]))(" + "|".join(p for _, p in OPERATORS) + r")\s*$", re.I)


@dataclass(frozen=True)
class Quantity:
    raw: str
    start: int
    end: int
    value: Decimal | None  # None bij dubbelzinnige notatie
    candidates: tuple[Decimal, ...]
    precision: int
    unit: str  # canonieke eenheid of valuta, "" als er geen is
    operator: str
    status: str  # ok, ambiguous, word
    context: tuple[str, ...] = field(default=(), compare=False)

    @property
    def shown(self) -> str:
        return self.raw


def _parse_number(num: str, family: str) -> tuple[Decimal | None, tuple[Decimal, ...], int, str]:
    num = num.replace(" ", " ").replace(" ", " ")
    has_dot, has_comma = "." in num, "," in num

    def build(int_part: str, frac: str) -> Decimal:
        return Decimal(int_part + ("." + frac if frac else ""))

    def groups_ok(parts: list[str]) -> bool:
        return all(len(p) == 3 for p in parts[1:]) and 1 <= len(parts[0]) <= 3

    try:
        if family in DECIMAL_SEP:
            dec = DECIMAL_SEP[family]
            grp = "." if dec == "," else ","
            int_part, _, frac = num.rpartition(dec) if dec in num else (num, "", "")
            if dec in int_part:
                return None, (), 0, "ambiguous"
            groups = re.split(r"[ " + re.escape(grp) + r"]", int_part)
            if len(groups) > 1 and not groups_ok(groups):
                return None, (), 0, "ambiguous"
            value = build("".join(groups), frac)
            return value, (value,), len(frac), "ok"
        # Onbekende locale.
        if has_dot and has_comma:
            dec = "." if num.rfind(".") > num.rfind(",") else ","
            return _parse_number(num, "en" if dec == "." else "nl")
        sep = "." if has_dot else "," if has_comma else (" " if " " in num else "")
        if not sep:
            value = Decimal(num)
            return value, (value,), 0, "ok"
        parts = num.split(sep)
        if sep == " ":
            if groups_ok(parts):
                value = Decimal("".join(parts))
                return value, (value,), 0, "ok"
            return None, (), 0, "ambiguous"
        if len(parts) == 2 and len(parts[1]) == 3:
            options = (Decimal("".join(parts)), build(parts[0], parts[1]))
            return None, options, 0, "ambiguous"
        if len(parts) == 2:
            value = build(parts[0], parts[1])
            return value, (value,), len(parts[1]), "ok"
        if groups_ok(parts):
            value = Decimal("".join(parts))
            return value, (value,), 0, "ok"
        return None, (), 0, "ambiguous"
    except InvalidOperation:
        return None, (), 0, "ambiguous"


WORD = re.compile(r"[\w'’]+")
FILLER = {"de", "het", "een", "en", "of", "in", "op", "van", "is", "was", "zijn", "maar", "liefst", "bij", "met",
          "voor", "naar", "om", "te", "dat", "die", "er", "nog", "al", "ook", "dan", "the", "a", "an", "of", "and"}


def _context(text: str, start: int, end: int) -> tuple[str, ...]:
    """Woorden direct voor een waarde, vanaf de laatste zinsgrens, komma of nevenschikking."""
    before = text[max(0, start - 80):start]
    before = re.split(r"[.!?;:\n,]|\b(?:en|of|maar|and|or|but)\b", before)[-1]
    words = [w for w in WORD.findall(before.lower()) if w not in FILLER and not w.isdigit()]
    return tuple(words[-4:])


def quantities(text: str, skip: list[tuple[int, int]], family: str, lang: str = "nl") -> list[Quantity]:
    """Alle hoeveelheden in een (gemaskeerde) tekst."""
    skip = sorted(skip)
    found: list[Quantity] = []

    def skipped(s: int, e: int) -> bool:
        return any(s < se and ss < e for ss, se in skip)

    for m in NUMBER.finditer(text):
        s_num, e_num = m.start("num"), m.end("num")
        if skipped(s_num, e_num):
            continue
        after = text[e_num:e_num + 1]
        unit_m = None if m.group("pct") else UNIT_AFTER.match(text, e_num)
        if after.isalpha() and not unit_m:
            continue  # identificatie zoals 2FA of 3D
        line_start = text.rfind("\n", max(0, m.start() - 200), m.start()) + 1
        if not text[line_start:m.start()].strip(" \t>#") and re.match(r"\d+[.)]\s", text[m.start():m.start() + 6]):
            continue  # nummering van een lijst
        num = m.group("num")
        if re.fullmatch(r"\d+\.\d+\.\d+(?:\.\d+)*", num):
            continue  # versienummer: wordt als letterlijke tekst vergeleken
        value, cands, precision, status = _parse_number(num, family)
        sign = m.group("sign")
        if sign and sign in "-−":
            value = -value if value is not None else None
            cands = tuple(-c for c in cands)
        unit = ""
        end = m.end()
        if m.group("cur"):
            unit = UNIT_CANON[m.group("cur").strip()]
        if m.group("pct"):
            unit = UNIT_CANON[m.group("pct").strip()]
        elif unit_m:
            unit = unit or UNIT_CANON[unit_m.group(1)]
            end = unit_m.end()
        op_m = OPERATOR_BEFORE.search(text[max(0, m.start() - 25):m.start()])
        operator = ""
        if op_m:
            word = op_m.group(1).lower()
            operator = next(name for name, pat in OPERATORS if re.fullmatch(pat, word, re.I))
        raw = text[m.start():end]
        found.append(Quantity(raw, m.start(), end, value, cands, precision, unit, operator, status,
                              _context(text, m.start(), end)))
    for m in NUMBER_WORD.get(lang, NUMBER_WORD["nl"]).finditer(text):
        if skipped(m.start(), m.end()):
            continue
        value = Decimal(NUMBER_WORDS[m.group(1).lower()])
        unit_m = UNIT_AFTER.match(text, m.end())
        unit = UNIT_CANON[unit_m.group(1)] if unit_m else ""
        end = unit_m.end() if unit_m else m.end()
        found.append(Quantity(text[m.start():end], m.start(), end, value, (value,), 0, unit, "", "word",
                              _context(text, m.start(), end)))
    found.sort(key=lambda q: q.start)
    return found


VERSION = re.compile(r"(?<![\w.])v?\d+\.\d+\.\d+(?:-[\w.]+)?(?!\w|\.\w)")


def versions(text: str) -> list[tuple[str, int]]:
    return [(m.group(0), m.start()) for m in VERSION.finditer(text)]


# ---------------------------------------------------------------------------
# Datums, tijden, weekdagen
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
_MONTH_RE = "|".join(sorted(MONTHS, key=len, reverse=True))
DATE_PATTERNS = [
    ("iso", re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")),
    ("numeric", re.compile(r"\b(\d{1,2})[-/.](\d{1,2})[-/.](\d{2,4})\b")),
    ("nl", re.compile(rf"\b(\d{{1,2}})\s+({_MONTH_RE})\b\.?(?:\s+(\d{{4}}))?", re.I)),
    ("en", re.compile(rf"\b({_MONTH_RE})\.?\s+(\d{{1,2}})(?:st|nd|rd|th)?\b(?:,?\s+(\d{{4}}))?", re.I)),
    ("time", re.compile(r"\b([01]?\d|2[0-3]):([0-5]\d)\b(?:\s?uur)?")),
    ("time", re.compile(r"\b([01]?\d|2[0-3])\.([0-5]\d)\s?uur\b")),
    ("hour", re.compile(r"\b([01]?\d|2[0-3])\s?uur\b")),
    ("ampm", re.compile(r"\b(1[0-2]|0?[1-9])(?::([0-5]\d))?\s?([ap])\.?m\.?(?!\w)", re.I)),
    ("weekday", re.compile(r"\b(" + "|".join(WEEKDAYS) + r")\b", re.I)),
]


@dataclass(frozen=True)
class DateValue:
    key: str
    shown: str
    start: int
    end: int


def _date_key(kind: str, m: re.Match[str]) -> str:
    g = m.groups()
    if kind == "iso":
        return f"d:{int(g[2])}-{int(g[1])}-{g[0]}"
    if kind == "numeric":
        return f"n:{g[0]}/{g[1]}/{g[2]}"  # letterlijk: dag en maand zijn niet eenduidig
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


def dates_and_times(text: str) -> list[DateValue]:
    found: list[DateValue] = []
    taken: list[tuple[int, int]] = []
    for kind, pattern in DATE_PATTERNS:
        for m in pattern.finditer(text):
            if any(m.start() < e and s < m.end() for s, e in taken):
                continue
            taken.append((m.start(), m.end()))
            found.append(DateValue(_date_key(kind, m), m.group(0).strip(), m.start(), m.end()))
    found.sort(key=lambda d: d.start)
    return found
