#!/usr/bin/env python3
"""Mechanische controle van dutch-humanizer-output (CLI-adapter rond dhcheck).

Gebruik:
    python3 scripts/check.py OUTPUT.txt [--input INPUT.txt] [opties]
    python3 scripts/check.py --stdin [opties] < data.json

--stdin leest JSON {"output": "...", "source": "..."} van standaardinvoer, zodat
er geen tekstbestanden nodig zijn. "source" mag ontbreken of null zijn.

Opties:
    --input PAD            brontekst; nodig voor alle vergelijkende controles
    --task TAAK            rewrite (standaard met bron), create (standaard zonder
                           bron), translate, shorten, summarize
    --style neutral|strict neutral: nieuwe streepjes, emoji, pijlen en gekrulde
                           aanhalingstekens zijn INFO. strict: elk zulk teken in
                           bewerkbare output is ERROR; citaten en code tellen niet mee
    --allow-dashes         bij --style strict: streepjes toch toestaan
    --source-lang auto|nl|other
                           taal van de bron. auto: herkent Nederlands of Engels.
                           other: niet-Nederlands; Engels wordt dan nog steeds
                           herkend en vergeleken, andere talen slaan woordsignalen over
    --source-locale L      notatie van getallen in de bron (nl-NL, nl-BE, en-US,
                           en-GB, auto). Standaard nl, of en bij Engelse bron;
                           auto laat "1.234" dubbelzinnig
    --target-locale L      notatie van getallen in de output (standaard nl)
    --format text|json     json: machineleesbaar, schema_version 1
    --fail-on-warning      exit 1 ook bij WARNING

Exitcodes: 0 = geen ERROR, 1 = ERROR (of WARNING met --fail-on-warning),
2 = gebruiksfout of onleesbaar bestand.

Het script vergelijkt tekens, getallen, beschermde fragmenten en signaalwoorden.
Het kan niet vaststellen dat de betekenis gelijk is gebleven. Het voert de
geanalyseerde code nooit uit en gebruikt geen netwerk.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from dhcheck import Finding, Report, analyze, TASKS  # noqa: E402
from dhcheck import markdown as _md  # noqa: E402
from dhcheck.core import NOTE  # noqa: E402

EXIT_OK, EXIT_FAIL, EXIT_USAGE = 0, 1, 2


def check(output: str, source: str | None = None, style: str = "neutral", allow_dashes: bool = False,
          source_lang: str = "auto", **kwargs) -> list[Finding]:
    """Compatibel met v0.6: lijst met findings (f.level, f.message, f.line, f.where)."""
    return analyze(output, source, style=style, allow_dashes=allow_dashes, source_lang=source_lang,
                   **kwargs).findings


def block_spans(text: str):
    """Compatibel met v0.6: blokken met kind 'code' of 'frontmatter'."""
    return [_md.Span(s.start, s.end, "code" if s.is_code else s.kind, s.text) for s in _md.block_spans(text)]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("output", type=Path, nargs="?")
    parser.add_argument("--input", type=Path)
    parser.add_argument("--stdin", action="store_true", help="lees JSON {output, source} van standaardinvoer")
    parser.add_argument("--task", choices=TASKS)
    parser.add_argument("--style", choices=("neutral", "strict"), default="neutral")
    parser.add_argument("--allow-dashes", action="store_true")
    parser.add_argument("--source-lang", choices=("auto", "nl", "other"), default="auto")
    parser.add_argument("--source-locale")
    parser.add_argument("--target-locale")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--fail-on-warning", action="store_true")
    args = parser.parse_args(argv)

    try:
        if args.stdin:
            data = json.loads(sys.stdin.read())
            output, source = data["output"], data.get("source")
        elif args.output is None:
            parser.error("geef een outputbestand of --stdin")
        else:
            output = args.output.read_text(encoding="utf-8")
            source = args.input.read_text(encoding="utf-8") if args.input else None
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError) as exc:
        print(f"ERROR kan invoer niet lezen: {exc}", file=sys.stderr)
        return EXIT_USAGE

    try:
        report: Report = analyze(output, source, task=args.task, style=args.style, allow_dashes=args.allow_dashes,
                                 source_lang=args.source_lang, source_locale=args.source_locale,
                                 target_locale=args.target_locale)
    except ValueError as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return EXIT_USAGE

    counts: Counter = report.counts()
    if args.format == "json":
        print(json.dumps(report.as_dict(), ensure_ascii=False, indent=2))
    else:
        for f in report.findings:
            print(f.format())
        skipped = "; ".join(f"{k} ({v})" for k, v in report.checks_skipped.items())
        print(f"Samenvatting: {counts['ERROR']} ERROR, {counts['WARNING']} WARNING, {counts['INFO']} INFO. "
              f"Taak: {report.task}. Uitgevoerd: {', '.join(report.checks_run)}."
              + (f" Overgeslagen: {skipped}." if skipped else ""))
        print(NOTE)
    if counts["ERROR"] or (args.fail_on_warning and counts["WARNING"]):
        return EXIT_FAIL
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
