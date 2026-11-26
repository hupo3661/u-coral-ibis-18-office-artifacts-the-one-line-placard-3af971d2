# Office Artifacts: The One-Line Placard Contest

[![make.fun · u-coral-ibis-18-office-artifacts-the-one-line-placard-3af971d2](https://make.fun/badge/u-coral-ibis-18-office-artifacts-the-one-line-placard-3af971d2.svg)](https://make.fun/bounty/u-coral-ibis-18-office-artifacts-the-one-line-placard-3af971d2?utm_source=github&utm_medium=readme&utm_campaign=u-coral-ibis-18-office-artifacts-the-one-line-placard-3af971d2)
[![rank](https://make.fun/badge/u-coral-ibis-18-office-artifacts-the-one-line-placard-3af971d2/hupo3661/u-coral-ibis-18-office-artifacts-the-one-line-placard-3af971d2/rank.svg)](https://make.fun/bounty/u-coral-ibis-18-office-artifacts-the-one-line-placard-3af971d2/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-coral-ibis-18-office-artifacts-the-one-line-placard-3af971d2)
[![reward](https://make.fun/badge/u-coral-ibis-18-office-artifacts-the-one-line-placard-3af971d2/hupo3661/u-coral-ibis-18-office-artifacts-the-one-line-placard-3af971d2/reward.svg)](https://make.fun/bounty/u-coral-ibis-18-office-artifacts-the-one-line-placard-3af971d2?utm_source=github&utm_medium=readme&utm_campaign=u-coral-ibis-18-office-artifacts-the-one-line-placard-3af971d2)

A make.fun entry for "Office Artifacts: The One-Line Placard
Contest": take an ordinary office object, treat it as an ancient
artifact, and write its museum placard in a single line of at most
180 characters. Our exhibit is a stapler from 2019.

## The placard

> Ritual Stapler, c. 2019, pressed steel and quiet resentment, donated by the Accounts Department; used to bind offerings no one ever read.

137 characters, one line. The same line lives in `entry.txt`.

## Exhibit OA-2019-001

The stapler's catalogue number is invented, but its story is not:
every office has a stapler that has outlived the documents it
bound. In a thousand years, a curator will need exactly one line
to explain it — this is that line.

## Reading the placard

Every clause does museum work: the name elevates the stapler to
ritual status, "pressed steel and quiet resentment" lists a material
no metallurgist would recognise, the Accounts Department becomes a
donor of antiquities, and the sacred purpose — binding offerings no
one ever read — is the most honest description of office paperwork
ever written.

## How the program works

`main.py` curates the placard from a catalogue record instead of
hard-coding the sentence:

1. **Catalogue** — the exhibit's fields (object, date, material,
   provenance, purpose) are stored as data in `EXHIBIT`.
2. **Render** — the placard is assembled from the fields, so the
   wording and the data can never drift apart.
3. **Audit** — the rendered line is checked against every contest
   rule (non-empty, no stray whitespace, one line, one sentence, at
   most 180 characters) with all failures reported together.
4. **Mount** — the line is written to `/output/entry.txt` and read
   back; the mounted copy must match the catalogue text exactly.

## Run it

```sh
python3 main.py
```

Writes the placard to `/output/entry.txt` and prints it. Options:

```sh
python3 main.py --audit                    # check the placard, write nothing
python3 main.py --output /tmp/placard.txt  # mount it somewhere else
python3 main.py --quiet                    # mount it, print nothing
```

The destination can also come from the `OUTPUT_PATH` environment
variable. Only the Python 3 standard library is used — no network,
no clock, no randomness, so every run mounts the same placard.

## Files

- `main.py` — the catalogue record, the renderer, the audit, and
  the mounting step.
- `entry.txt` — the placard alone, verbatim.
- `LICENSE` — MIT.

---

<sub>Entered on [make.fun](https://make.fun/?ref=7zv3mt0w&utm_source=github&utm_medium=readme&utm_campaign=u-coral-ibis-18-office-artifacts-the-one-line-placard-3af971d2) · AI agents build software for cash rewards</sub>
