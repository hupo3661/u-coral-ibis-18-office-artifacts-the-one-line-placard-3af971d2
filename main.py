#!/usr/bin/env python3
"""Office Artifacts: The One-Line Placard Contest — a one-line entry.

In the museum of the future, an ordinary office stapler is an
ancient ritual object. Its placard names the artifact, dates it,
lists its materials, credits its donor, and states its sacred use —
all in one line of at most 180 characters. This program curates
that placard from its catalogue fields and mounts it in the entry
file.
"""

import os
import sys
from pathlib import Path

CHAR_LIMIT = 180
DEFAULT_OUTPUT = "/output/entry.txt"

# Catalogue record for exhibit OA-2019-001. The placard is rendered
# from these fields; the rendered line is the entry, verbatim.
EXHIBIT = {
    "object": "Ritual Stapler",
    "date": "c. 2019",
    "material": "pressed steel and quiet resentment",
    "provenance": "donated by the Accounts Department",
    "purpose": "used to bind offerings no one ever read",
}


def render_placard(record):
    """Assemble the one-line placard from the catalogue record."""
    head = ", ".join(
        [record["object"], record["date"], record["material"], record["provenance"]]
    )
    return f"{head}; {record['purpose']}."


PLACARD = render_placard(EXHIBIT)


def audit(line):
    """Return every contest rule the placard breaks (empty if none)."""
    broken = []
    if not line.strip():
        broken.append("placard is empty")
    if line != line.strip():
        broken.append("placard has leading or trailing whitespace")
    if len(line) > CHAR_LIMIT:
        broken.append(f"placard is {len(line)} characters, over {CHAR_LIMIT}")
    if "\n" in line or "\r" in line:
        broken.append("placard must be a single line")
    if line.count(".") != 1:
        broken.append("placard must be a single sentence")
    return broken


def choose_output(argv):
    """Where to mount the placard: --output, OUTPUT_PATH, or default."""
    for index, flag in enumerate(argv):
        if flag == "--output" and index + 1 < len(argv):
            return argv[index + 1]
        if flag.startswith("--output="):
            return flag.split("=", 1)[1]
    return os.environ.get("OUTPUT_PATH", DEFAULT_OUTPUT)


def mount(line, destination):
    """Mount the placard and verify the mounted copy matches."""
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(line, encoding="utf-8")
    if path.read_text(encoding="utf-8") != line:
        raise SystemExit("mounted placard differs from the catalogue text")
    return path


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    broken = audit(PLACARD)
    if broken:
        print("placard fails: " + "; ".join(broken), file=sys.stderr)
        return 1
    if "--audit" in argv:
        print(f"placard OK: {len(PLACARD)} characters, one line")
        return 0
    target = mount(PLACARD, choose_output(argv))
    if "--quiet" not in argv:
        print(PLACARD)
        print(f"mounted at {target}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
