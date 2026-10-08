"""Woordsignalen voor ontkenning, modaliteit, voorwaarden en termijnen.

Per zin worden signaalwoorden in families ingedeeld. Een modaal werkwoord met
een ontkenning in dezelfde zin wordt als combinatie gelezen: "moet ... niet",
"hoeft ... niet", "mag ... niet". Woorden binnen één familie mogen elkaar
vervangen ("dient" en "moet"); een verschuiving tussen families ("tenzij" naar
"mits", "moet" naar "verboden") levert altijd een WARNING op.

Dit is een heuristiek. "Tenzij het regent" en "mits het niet regent" kunnen
hetzelfde betekenen, "tenzij het regent" en "mits het regent" niet. Het script
kan dat onderscheid niet maken; de inhoudelijke controle beslist.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass

LABELS = {
    "NEG": "ontkenning",
    "OBLIG": "verplichting", "OBLIG_NEG": "verplichting", "NO_OBLIG": "verplichting",
    "PROHIB": "verbod",
    "PERM": "toestemming",
    "ABLE": "mogelijkheid (kunnen)", "ABLE_NEG": "mogelijkheid (kunnen)",
    "POSSIBLE": "onzekerheid", "PROBABLE": "onzekerheid", "EVIDENTIAL": "onzekerheid",
    "IF": "voorwaarde of uitzondering", "ONLYIF": "voorwaarde of uitzondering",
    "EXCEPT": "voorwaarde of uitzondering", "TIMING": "voorwaarde of uitzondering",
    "DEADLINE": "termijn of volgorde", "AFTER": "termijn of volgorde",
}
FAMILY_NOTE = {
    "OBLIG_NEG": "'moet ... niet' is een afraden of verbod",
    "NO_OBLIG": "'hoeft ... niet' heft een verplichting op",
    "EVIDENTIAL": "'lijkt' gaat over aanwijzingen, niet over waarschijnlijkheid",
    "ONLYIF": "'mits' betekent 'alleen als'",
    "EXCEPT": "'tenzij' betekent 'behalve als'",
}

NL_TERMS = [
    ("met uitzondering van", "EXCEPT"), ("op voorwaarde dat", "ONLYIF"), ("alleen als", "ONLYIF"),
    ("alleen indien", "ONLYIF"), ("uitsluitend als", "ONLYIF"), ("enkel als", "ONLYIF"), ("pas als", "ONLYIF"),
    ("tot en met", "DEADLINE"), ("t/m", "DEADLINE"), ("pas na", "AFTER"), ("naar verwachting", "PROBABLE"),
    ("in geval van", "IF"), ("ingeval", "IF"), ("niet verplicht", "NO_OBLIG"), ("geen verplichting", "NO_OBLIG"),
    ("niet toegestaan", "PROHIB"), ("niet nodig", "NO_OBLIG"),
    ("tenzij", "EXCEPT"), ("behalve", "EXCEPT"), ("uitgezonderd", "EXCEPT"), ("behoudens", "EXCEPT"),
    ("mits", "ONLYIF"), ("indien", "IF"), ("zodra", "TIMING"),
    ("uiterlijk", "DEADLINE"), ("vóór", "DEADLINE"), ("voordat", "DEADLINE"),
    ("nadat", "AFTER"), ("vanaf", "AFTER"), ("sinds", "AFTER"), ("na", "AFTER"),
    ("moet", "OBLIG"), ("moeten", "OBLIG"), ("moest", "OBLIG"), ("moesten", "OBLIG"), ("dient", "OBLIG"),
    ("dienen", "OBLIG"), ("diende", "OBLIG"), ("dienden", "OBLIG"), ("verplicht", "OBLIG"),
    ("verplichte", "OBLIG"), ("vereist", "OBLIG"), ("vereiste", "OBLIG"),
    ("hoeft", "NO_OBLIG_VERB"), ("hoeven", "NO_OBLIG_VERB"), ("hoefde", "NO_OBLIG_VERB"),
    ("hoefden", "NO_OBLIG_VERB"), ("hoef", "NO_OBLIG_VERB"),
    ("verboden", "PROHIB"), ("verbod", "PROHIB"),
    ("mag", "PERM"), ("mogen", "PERM"), ("mochten", "PERM"), ("toegestaan", "PERM"), ("mocht", "PERM"),
    ("kan", "ABLE"), ("kunt", "ABLE"), ("kunnen", "ABLE"), ("kon", "ABLE"), ("konden", "ABLE"), ("kun", "ABLE"),
    ("mogelijk", "POSSIBLE"), ("misschien", "POSSIBLE"), ("wellicht", "POSSIBLE"), ("eventueel", "POSSIBLE"),
    ("eventuele", "POSSIBLE"), ("mogelijkerwijs", "POSSIBLE"),
    ("waarschijnlijk", "PROBABLE"), ("waarschijnlijke", "PROBABLE"), ("vermoedelijk", "PROBABLE"),
    ("vermoedelijke", "PROBABLE"), ("verwacht", "PROBABLE"), ("verwachten", "PROBABLE"),
    ("vermoeden", "PROBABLE"),
    ("lijkt", "EVIDENTIAL"), ("lijken", "EVIDENTIAL"), ("leek", "EVIDENTIAL"), ("leken", "EVIDENTIAL"),
    ("schijnt", "EVIDENTIAL"), ("blijkbaar", "EVIDENTIAL"), ("kennelijk", "EVIDENTIAL"),
    ("niet", "NEG"), ("geen", "NEG"), ("nooit", "NEG"), ("niets", "NEG"), ("niemand", "NEG"),
    ("nergens", "NEG"), ("noch", "NEG"), ("zonder", "NEG"),
]
EN_TERMS = [
    ("no later than", "DEADLINE"), ("provided that", "ONLYIF"), ("only if", "ONLYIF"), ("as long as", "ONLYIF"),
    ("as soon as", "TIMING"), ("must not", "PROHIB"), ("mustn't", "PROHIB"), ("may not", "PROHIB"),
    ("shall not", "PROHIB"), ("not allowed", "PROHIB"), ("not permitted", "PROHIB"),
    ("do not have to", "NO_OBLIG"), ("don't have to", "NO_OBLIG"), ("doesn't have to", "NO_OBLIG"),
    ("need not", "NO_OBLIG"), ("needn't", "NO_OBLIG"), ("not required", "NO_OBLIG"),
    ("have to", "OBLIG"), ("has to", "OBLIG"), ("had to", "OBLIG"), ("need to", "OBLIG"), ("needs to", "OBLIG"),
    ("expected to", "PROBABLE"), ("appears to", "EVIDENTIAL"),
    ("unless", "EXCEPT"), ("except", "EXCEPT"), ("within", "DEADLINE"), ("after", "AFTER"), ("since", "AFTER"),
    ("must", "OBLIG"), ("required", "OBLIG"), ("shall", "OBLIG"), ("mandatory", "OBLIG"),
    ("prohibited", "PROHIB"), ("forbidden", "PROHIB"), ("allowed", "PERM"), ("permitted", "PERM"),
    ("might", "POSSIBLE"), ("possibly", "POSSIBLE"), ("perhaps", "POSSIBLE"), ("maybe", "POSSIBLE"),
    ("likely", "PROBABLE"), ("probably", "PROBABLE"), ("presumably", "PROBABLE"),
    ("seems", "EVIDENTIAL"), ("seem", "EVIDENTIAL"), ("apparently", "EVIDENTIAL"),
    ("not", "NEG"), ("never", "NEG"), ("no", "NEG"), ("nothing", "NEG"), ("nobody", "NEG"), ("none", "NEG"),
    ("without", "NEG"), ("n't", "NEG"),
]


def _compile(terms):
    alts = sorted({t for t, _ in terms}, key=len, reverse=True)
    family = dict(terms)
    pattern = re.compile(r"(?<![\w'’])(" + "|".join(re.escape(a) for a in alts) + r")(?![\w'’])")
    return pattern, family


NL = _compile(NL_TERMS)
EN = _compile(EN_TERMS)
EN_NT = re.compile(r"\w+n't\b")
NL_IDIOMS = re.compile(r"\bzo(?:veel| veel| \w+)? mogelijk\b|\bwaar mogelijk\b|\bindien mogelijk\b|\bzo mogelijk\b")
BINNEN = re.compile(r"(?<![\w])binnen(?=\s+(?:\S+\s+){0,2}?(?:\d|een\b|één\b|twee\b|drie\b|vier\b|vijf\b|zes\b|"
                    r"zeven\b|acht\b|tien\b|veertien\b|dertig\b|enkele\b|de termijn|het uur|de week|de maand))")
OBLIG_VERBS = {"moet", "moeten", "moest", "moesten", "dient", "dienen", "diende", "dienden"}
CLAUSE = re.compile(r"[^.!?;:,\n]+")


@dataclass(frozen=True)
class Signal:
    family: str
    term: str
    pos: int


def signals(text: str, lang: str = "nl") -> list[Signal]:
    """Signaalwoorden per familie, met positie in de tekst."""
    pattern, family_of = NL if lang == "nl" else EN
    low = text.lower()
    if lang == "nl":
        low = NL_IDIOMS.sub(lambda m: " " * len(m.group(0)), low)
    found: list[Signal] = []
    for clause in CLAUSE.finditer(low):
        base = clause.start()
        part = clause.group(0)
        items = [(m.group(1), family_of[m.group(1)], base + m.start()) for m in pattern.finditer(part)]
        if lang == "nl":
            items += [("binnen", "DEADLINE", base + m.start()) for m in BINNEN.finditer(part)]
            # "Mocht u ..." aan het begin van een zin is een voorwaarde.
            first = re.match(r"\s*mocht\b", part)
            if first:
                items = [("mocht", "IF", p) if t == "mocht" and p == base + first.end() - 5 else (t, f, p)
                         for t, f, p in items]
        else:
            items += [("n't", "NEG", base + m.start()) for m in EN_NT.finditer(part)
                      if not any(t in ("mustn't", "needn't", "don't have to", "doesn't have to") and p <= base + m.start() < p + len(t)
                                 for t, _, p in items)]
        items.sort(key=lambda x: x[2])
        negs = [i for i, it in enumerate(items) if it[1] == "NEG"]
        used: set[int] = set()
        result: list[Signal] = []
        for i, (term, fam, pos) in enumerate(items):
            if fam == "NEG":
                continue
            if lang == "nl":
                neg = next((n for n in negs if n not in used), None)
                if fam == "NO_OBLIG_VERB":
                    if neg is not None:
                        used.add(neg)
                    fam = "NO_OBLIG"
                elif neg is not None and fam == "OBLIG" and term in OBLIG_VERBS:
                    used.add(neg)
                    fam, term = "OBLIG_NEG", f"{term} ... niet"
                elif neg is not None and fam == "PERM":
                    used.add(neg)
                    fam, term = "PROHIB", f"{term} ... niet"
                elif neg is not None and fam == "ABLE":
                    used.add(neg)
                    fam, term = "ABLE_NEG", f"{term} ... niet"
            result.append(Signal(fam, term, pos))
        result += [Signal("NEG", items[n][0], items[n][2]) for n in negs if n not in used]
        found += result
    return sorted(found, key=lambda s: s.pos)


def compare(src: list[Signal], out: list[Signal]) -> list[tuple[str, list[str], list[str], int | None, set[str]]]:
    """Per label: verdwenen termen, nieuwe termen, eerste bronpositie, betrokken families."""
    results = []
    for label in dict.fromkeys(LABELS.values()):
        fams = [f for f, lab in LABELS.items() if lab == label]
        fs = Counter(s.family for s in src if s.family in fams)
        fo = Counter(s.family for s in out if s.family in fams)
        if fs == fo:
            continue
        changed = {f for f in fams if fs[f] != fo[f]}
        ts = Counter(s.term for s in src if s.family in changed)
        to = Counter(s.term for s in out if s.family in changed)
        gone = list((ts - to).keys())
        new = list((to - ts).keys())
        if not gone and not new:
            # Zelfde termen, ander aantal: tel het verschil per familie.
            gone = [f"{s.term} ({fs[s.family]}x naar {fo[s.family]}x)" for s in src if s.family in changed][:1]
            new = [f"{s.term} ({fs[s.family]}x naar {fo[s.family]}x)" for s in out if s.family in changed and not gone][:1]
        first = next((s.pos for s in src if s.family in changed), None)
        results.append((label, gone, new, first, changed))
    return results
