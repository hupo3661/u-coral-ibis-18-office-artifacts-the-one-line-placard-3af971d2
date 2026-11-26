#!/usr/bin/env python3
"""Office Artifacts: The One-Line Placard Contest.

A museum of the future has acquired an ordinary office stapler and
must explain it to visitors in a single line. The curator's placard
names the object, dates it, lists its materials, credits its donor,
and states its sacred purpose — all in one sentence of at most 180
characters. This program keeps the exhibit as a catalogue record,
renders the placard from that record, audits the finished line
against the contest rules, and mounts it in the entry file.

The placard is fixed. Nothing here reads the clock, the network or
a random number, so every run mounts the same line.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

# Contest rules, kept as numbers instead of remembered in prose.
MAX_CHARS = 180
ABBREVIATIONS = ("c.", "e.g.", "i.e.", "Dr.", "Mr.", "Mrs.")
DEFAULT_ENTRY_PATH = "/output/entry.txt"


@dataclass(frozen=True)
class CatalogueEntry:
    """One museum exhibit, stored as data rather than as a sentence."""

    accession: str
    name: str
    date: str
    material: str
    donor: str
    purpose: str

    def head_fields(self) -> list[str]:
        """The comma-joined fields that open the placard."""
        return [self.name, self.date, self.material, self.donor]


THE_STAPLER = CatalogueEntry(
    accession="OA-2019-001",
    name="Ritual Stapler",
    date="c. 2019",
    material="pressed steel and quiet resentment",
    donor="donated by the Accounts Department",
    purpose="used to bind offerings no one ever read",
)


class PlacardRenderer:
    """Turns a catalogue record into the one-line placard."""

    def __init__(self, entry: CatalogueEntry) -> None:
        self.entry = entry

    def render(self) -> str:
        head = ", ".join(self.entry.head_fields())
        return f"{head}; {self.entry.purpose}."

    def clause_count(self) -> int:
        """Commas plus the semicolon: how many clauses the line holds."""
        line = self.render()
        return line.count(",") + line.count(";")

    def field_table(self) -> str:
        """The catalogue record as a readable label, for --catalogue."""
        entry = self.entry
        rows = [
            ("accession", entry.accession),
            ("object", entry.name),
            ("date", entry.date),
            ("material", entry.material),
            ("donor", entry.donor),
            ("purpose", entry.purpose),
        ]
        width = max(len(label) for label, _ in rows)
        return "\n".join(f"{label:<{width}}: {value}" for label, value in rows)


def sentence_stops(line: str) -> int:
    """Count sentence-ending full stops, ignoring known abbreviations."""
    masked = line
    for mark in ABBREVIATIONS:
        masked = masked.replace(mark, mark.replace(".", ""))
    return masked.count(".")


@dataclass
class AuditFinding:
    """One contest rule the placard breaks."""

    rule: str
    detail: str

    def __str__(self) -> str:
        return f"{self.rule}: {self.detail}"


def audit_placard(line: str) -> list[AuditFinding]:
    """Audit a placard against every contest rule, all at once."""
    findings: list[AuditFinding] = []
    if not line.strip():
        findings.append(AuditFinding("empty", "the placard says nothing"))
    if line != line.strip():
        findings.append(
            AuditFinding("whitespace", "leading or trailing space around the line")
        )
    if len(line) > MAX_CHARS:
        findings.append(
            AuditFinding(
                "length", f"{len(line)} characters, over the {MAX_CHARS} limit"
            )
        )
    if "\n" in line or "\r" in line:
        findings.append(AuditFinding("one line", "the placard wraps onto more lines"))
    if sentence_stops(line) != 1 or not line.endswith("."):
        findings.append(
            AuditFinding(
                "one sentence",
                "must be exactly one sentence, ending with a full stop",
            )
        )
    if ";" not in line:
        findings.append(
            AuditFinding("semicolon", "the purpose clause needs its semicolon")
        )
    if not re.search(r"\bc\. \d{4}\b", line):
        findings.append(
            AuditFinding("date", "the circa date (for example 'c. 2019') is missing")
        )
    return findings


class Curator:
    """Checks a placard and mounts it where the judges will read it."""

    def __init__(self, renderer: PlacardRenderer) -> None:
        self.renderer = renderer

    def approved_line(self) -> str:
        line = self.renderer.render()
        findings = audit_placard(line)
        if findings:
            raise ValueError("; ".join(str(f) for f in findings))
        return line

    def mount(self, destination: str) -> Path:
        line = self.approved_line()
        target = Path(destination)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(line, encoding="utf-8")
        mounted = target.read_text(encoding="utf-8")
        if mounted != line:
            raise ValueError("mounted placard differs from the catalogue text")
        return target


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Mount the one-line placard for the Ritual Stapler."
    )
    parser.add_argument(
        "--output",
        default=None,
        help="where to mount the placard (default: OUTPUT_PATH or /output/entry.txt)",
    )
    parser.add_argument(
        "--audit",
        action="store_true",
        help="audit the placard and mount nothing",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="mount the placard without printing it",
    )
    parser.add_argument(
        "--catalogue",
        action="store_true",
        help="print the catalogue record and mount nothing",
    )
    return parser


def resolve_output(explicit: str | None) -> str:
    if explicit:
        return explicit
    return os.environ.get("OUTPUT_PATH", DEFAULT_ENTRY_PATH)


def run(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    curator = Curator(PlacardRenderer(THE_STAPLER))
    try:
        line = curator.approved_line()
    except ValueError as problem:
        print(f"placard fails: {problem}", file=sys.stderr)
        return 1
    if args.audit:
        print(
            f"placard OK: {len(line)} characters, one line, "
            f"{curator.renderer.clause_count()} clauses"
        )
        return 0
    if args.catalogue:
        print(curator.renderer.field_table())
        return 0
    try:
        target = curator.mount(resolve_output(args.output))
    except ValueError as problem:
        print(f"mounting failed: {problem}", file=sys.stderr)
        return 1
    if not args.quiet:
        print(line)
    print(f"mounted at {target}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
