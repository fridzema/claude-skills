"""Beschermde spans in Markdown-achtige tekst, met stabiele offsets.

Begrensde scanner, geen volledige CommonMark-parser. Wel ondersteund: YAML-
frontmatter, fenced code (``` en ~~~, ongesloten tot het einde), ingesprongen
code, inline code met backtickreeksen van gelijke lengte, linkbestemmingen
(ook met geneste haken in de linktekst), autolinks, URL's, e-mailadressen,
API- en bestandspaden, en citaten tussen aanhalingstekens.

Niet ondersteund en gedocumenteerd: containerblokken (code in blockquotes of
diep geneste lijsten), HTML-blokken, setext-koppen. Alle scans zijn lineair of
n log n, zodat grote invoer geen kwadratische tijd kost.
"""

from __future__ import annotations

import bisect
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Span:
    start: int
    end: int
    kind: str  # frontmatter, fence, indented, inline, link, url, email, path, quote
    text: str  # letterlijke beschermde inhoud (bij code: de body)

    @property
    def is_code(self) -> bool:
        return self.kind in ("fence", "indented", "inline")


class Intervals:
    """Niet-overlappende intervallen met overlapcontrole in O(log n)."""

    def __init__(self) -> None:
        self.starts: list[int] = []
        self.ends: list[int] = []

    def overlaps(self, start: int, end: int) -> bool:
        i = bisect.bisect_right(self.starts, start)
        if i and self.ends[i - 1] > start:
            return True
        return i < len(self.starts) and self.starts[i] < end

    def add(self, start: int, end: int) -> None:
        i = bisect.bisect_right(self.starts, start)
        self.starts.insert(i, start)
        self.ends.insert(i, end)


def _lines(text: str) -> list[tuple[int, str]]:
    out, pos = [], 0
    for line in text.split("\n"):
        out.append((pos, line))
        pos += len(line) + 1
    return out


FENCE_OPEN = re.compile(r"^( {0,3})(`{3,}|~{3,})(.*)$")
FENCE_CLOSE = re.compile(r"^ {0,3}(`{3,}|~{3,})[ \t]*$")
LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s")
INDENT = re.compile(r"^( {4}|\t)")


def block_spans(text: str) -> list[Span]:
    """Frontmatter, fenced en ingesprongen code."""
    spans: list[Span] = []
    lines = _lines(text)
    i = 0
    if text.startswith("---\n") or text.startswith("---\r\n"):
        for j in range(1, len(lines)):
            if lines[j][1].rstrip("\r") in ("---", "..."):
                end = lines[j][0] + len(lines[j][1])
                spans.append(Span(0, end, "frontmatter", text[:end]))
                i = j + 1
                break

    prev_blank = True
    in_list = False
    while i < len(lines):
        start, line = lines[i]
        fence = FENCE_OPEN.match(line)
        if fence and not (fence.group(2)[0] == "`" and "`" in fence.group(3)):
            marker = fence.group(2)
            j = i + 1
            closed = False
            while j < len(lines):
                close = FENCE_CLOSE.match(lines[j][1])
                if close and close.group(1)[0] == marker[0] and len(close.group(1)) >= len(marker):
                    closed = True
                    break
                j += 1
            last = j if closed else len(lines) - 1
            end = lines[last][0] + len(lines[last][1])
            body = "\n".join(l for _, l in lines[i + 1:j])
            spans.append(Span(start, end, "fence", body))
            i = last + 1
            prev_blank = False
            continue
        if INDENT.match(line) and line.strip() and prev_blank and not in_list:
            j = i
            while j + 1 < len(lines) and (INDENT.match(lines[j + 1][1]) or not lines[j + 1][1].strip()):
                j += 1
            while j > i and not lines[j][1].strip():
                j -= 1
            end = lines[j][0] + len(lines[j][1])
            body = "\n".join(INDENT.sub("", l, count=1) for _, l in lines[i:j + 1])
            spans.append(Span(start, end, "indented", body))
            i = j + 1
            prev_blank = False
            continue
        if line.strip():
            in_list = bool(LIST_ITEM.match(line)) or (in_list and line[:1] in (" ", "\t"))
        prev_blank = not line.strip()
        i += 1
    return spans


BACKTICKS = re.compile(r"`+")


def _escaped(text: str, pos: int) -> bool:
    n = 0
    while pos - n - 1 >= 0 and text[pos - n - 1] == "\\":
        n += 1
    return n % 2 == 1


def inline_code_spans(text: str, taken: Intervals) -> list[Span]:
    runs: list[tuple[int, int]] = []
    for m in BACKTICKS.finditer(text):
        start, end = m.start(), m.end()
        if taken.overlaps(start, end):
            continue
        if _escaped(text, start):
            start += 1
            if start == end:
                continue
        runs.append((start, end))
    by_len: dict[int, list[int]] = {}
    for idx, (s, e) in enumerate(runs):
        by_len.setdefault(e - s, []).append(idx)
    spans: list[Span] = []
    used: set[int] = set()
    covered_until = -1
    for idx, (s, e) in enumerate(runs):
        if idx in used or s < covered_until:
            continue
        candidates = by_len[e - s]
        k = bisect.bisect_right(candidates, idx)
        while k < len(candidates):
            j = candidates[k]
            k += 1
            if j in used:
                continue
            cs, ce = runs[j]
            if "\n\n" in text[e:cs]:
                break  # een code span loopt niet over een witregel
            used.update((idx, j))
            spans.append(Span(s, ce, "inline", text[e:cs]))
            covered_until = ce
            break
    return spans


URL = re.compile(r"(?:(?:https?|ftp)://|www\.)[^\s<>\"'`]+")
AUTOLINK = re.compile(r"<((?:https?|ftp|mailto):[^\s<>]+)>")
EMAIL = re.compile(r"(?<![\w.@+-])[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+")
REF_DEF = re.compile(r"^ {0,3}\[[^\]\n]+\]:[ \t]*<?([^\s>]+)>?", re.M)
PATH = re.compile(
    r"(?<![\w/.:@-])"
    r"(?:(?:~|\.{1,2})?/(?:[\w.{}:@-]+/)*[\w.{}:@-]*[\w}]"  # begint met /, ./, ../ of ~/
    r"|(?:[\w.-]+/)+[\w-]+\.[A-Za-z0-9]{1,6})"  # relatief pad met bestandsextensie
    r"(?![\w/])"
)


def _trim_url(value: str) -> str:
    while value and value[-1] in ".,;:!?":
        value = value[:-1]
    while value.endswith(")") and value.count(")") > value.count("("):
        value = value[:-1]
    return value


def _link_destinations(text: str):
    """Bestemming van [tekst](bestemming "titel"), ook bij geneste haken."""
    for m in re.finditer(r"\]\(", text):
        i = m.end()
        while i < len(text) and text[i] in " \t":
            i += 1
        if i < len(text) and text[i] == "<":
            close = text.find(">", i + 1)
            if close != -1 and "\n" not in text[i + 1:close]:
                yield i + 1, close
            continue
        depth, j = 0, i
        while j < len(text):
            c = text[j]
            if c in " \t\n":
                break
            if c == "\\":
                j += 2
                continue
            if c == "(":
                depth += 1
            elif c == ")":
                if depth == 0:
                    break
                depth -= 1
            j += 1
        if j > i:
            yield i, j


def reference_spans(text: str, taken: Intervals) -> list[Span]:
    spans: list[Span] = []

    def add(start: int, end: int, kind: str) -> None:
        if end > start and not taken.overlaps(start, end):
            spans.append(Span(start, end, kind, text[start:end]))
            taken.add(start, end)

    for s, e in _link_destinations(text):
        add(s, e, "link")
    for m in REF_DEF.finditer(text):
        add(m.start(1), m.end(1), "link")
    for m in AUTOLINK.finditer(text):
        add(m.start(1), m.end(1), "url")
    for m in URL.finditer(text):
        value = _trim_url(m.group(0))
        add(m.start(), m.start() + len(value), "url")
    for m in EMAIL.finditer(text):
        value = m.group(0).rstrip(".")
        add(m.start(), m.start() + len(value), "email")
    for m in PATH.finditer(text):
        value = m.group(0)
        segments = [s for s in value.split("/") if s]
        if not segments or all(s.isdigit() for s in segments):
            continue
        if not value.startswith(("/", "./", "../", "~/")) and len(segments) < 2:
            continue
        add(m.start(), m.end(), "path")
    return spans


QUOTE_PAIRS = {"“": "”", "„": "”“", "‘": "’"}
CONTRACTION = re.compile(r"^[stnk]\b", re.I)


def delimiter_quotes(text: str) -> tuple[int, int] | None:
    """Aanhalingstekens die de hele invoer afbakenen, geen citaat."""
    stripped = text.strip()
    if len(stripped) < 2:
        return None
    first, last = stripped[0], stripped[-1]
    closes = {'"': '"', "“": "”", "„": "”“", "'": "'", "‘": "’"}
    if first not in closes or last not in closes[first]:
        return None
    inner = stripped[1:-1]
    if "\n" not in inner and len(re.findall(r"[.!?](?:\s|$)", inner)) < 2:
        return None  # een enkele zin tussen aanhalingstekens kan een citaat zijn
    start = text.index(first)
    return start, text.rindex(last)


def quote_spans(text: str, taken: Intervals) -> tuple[list[Span], list[int]]:
    """Citaten (inhoud) en de posities van hun aanhalingstekens."""
    spans: list[Span] = []
    marks: list[int] = []
    skip = set(delimiter_quotes(text) or ())

    def add(open_pos: int, close_pos: int) -> None:
        if close_pos <= open_pos + 1 or taken.overlaps(open_pos, close_pos + 1):
            return
        spans.append(Span(open_pos + 1, close_pos, "quote", text[open_pos + 1:close_pos]))
        taken.add(open_pos, close_pos + 1)
        marks.extend((open_pos, close_pos))

    # Gekrulde en lage aanhalingstekens.
    for opener, closers in QUOTE_PAIRS.items():
        pos = 0
        while True:
            o = text.find(opener, pos)
            if o == -1:
                break
            pos = o + 1
            if o in skip:
                continue
            if opener == "‘" and (o > 0 and text[o - 1].isalnum()):
                continue
            end = min((c for c in (text.find(ch, o + 1) for ch in closers) if c != -1), default=-1)
            if end == -1 or "\n\n" in text[o:end]:
                continue
            if opener == "‘" and end + 1 < len(text) and text[end + 1].isalnum():
                continue  # apostrof binnen een woord
            add(o, end)
            pos = end + 1

    # Rechte dubbele aanhalingstekens: paarsgewijs per alinea, escapes overslaan.
    open_pos = None
    for m in re.finditer(r'"|\n\s*\n', text):
        p = m.start()
        if m.group(0) != '"':
            open_pos = None
            continue
        if p in skip or _escaped(text, p) or taken.overlaps(p, p + 1):
            continue
        if open_pos is None:
            open_pos = p
        else:
            add(open_pos, p)
            open_pos = None

    # Rechte enkele aanhalingstekens, niet als apostrof of samentrekking.
    for m in re.finditer(r"(?:(?<=^)|(?<=[\s(\[]))'(?=\S)([^'\n]{1,300}?)(?<=\S)'(?=$|[\s.,;:!?)\]])", text, re.M):
        if m.start() in skip or CONTRACTION.match(m.group(1)):
            continue
        add(m.start(), m.end() - 1)
    return spans, marks


@dataclass
class Parsed:
    text: str
    spans: list[Span]
    quote_marks: list[int]
    masked_code: str  # code, frontmatter, links, URL's, e-mail en paden vervangen door spaties
    masked_all: str  # idem, plus de inhoud van citaten
    line_starts: list[int]

    def of_kind(self, *kinds: str) -> list[Span]:
        return [s for s in self.spans if s.kind in kinds]

    def code(self) -> list[Span]:
        return [s for s in self.spans if s.is_code]

    def line_at(self, pos: int) -> int:
        return bisect.bisect_right(self.line_starts, pos)


def mask(text: str, spans: list[Span]) -> str:
    chars = list(text)
    for s in spans:
        for k in range(s.start, s.end):
            if chars[k] != "\n":
                chars[k] = " "
    return "".join(chars)


def parse(text: str) -> Parsed:
    taken = Intervals()
    blocks = block_spans(text)
    for s in blocks:
        taken.add(s.start, s.end)
    inline = inline_code_spans(text, taken)
    for s in inline:
        taken.add(s.start, s.end)
    refs = reference_spans(text, taken)
    quotes, marks = quote_spans(text, taken)
    code_like = blocks + inline + refs
    spans = sorted(code_like + quotes, key=lambda s: s.start)
    line_starts = [0] + [m.end() for m in re.finditer(r"\n", text)]
    return Parsed(text, spans, sorted(marks), mask(text, code_like), mask(text, code_like + quotes), line_starts)
