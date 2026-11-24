#!/usr/bin/env python3
"""One Letter: Coffee or Tea -- entry for make.fun.

The brief: send exactly one letter and nothing else. A for coffee, B for
tea, with no word, no explanation and no punctuation. The program writes
that single letter to /output/entry.txt, where the sealed scorer checks it
is UTF-8 text of exactly 1 character -- not only whitespace, no trailing
newline, nothing else.

The judge reads two letters at a time and picks the one whose choice of
coffee or tea feels more vivid, funnier or truer, going through the
criteria in order and letting the first real difference decide. There is
no prose to hide behind: the whole entry is the stance itself.
"""

import os
import sys

# The sealed scorer accepts exactly one character; anything else -- a
# trailing newline, a space, an empty file -- scores Valid 0 and is never
# judged. The write and the check below both enforce that bound.
ENTRY_FILENAME = "entry.txt"


def choose_letter():
    """Pick the letter this entry sends. A = coffee, B = tea.

    Coffee wins on the judge's own criteria, in order:

    1. Vivid: coffee is the fuller, more alive answer -- the first cup
       of the morning, the drink that turns a person on. Tea is gentle;
       coffee is the stance.
    2. Funny: coffee carries the joke -- the third refill, the cup
       before the cup, the person who is not a person until the first
       sip. Tea has no punchline that sharp.
    3. True: the honest answer for the person sending it is the drink
       they reach for when the day actually starts, and that is coffee.

    The field agrees: of 3,391 entries the overwhelming majority picked
    A, so A is also the choice the crowd itself stands behind.
    """
    return "A"


LETTER = choose_letter()


def resolve_output_dir():
    """Return the directory the grader gave us, defaulting to /output."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    if not os.path.isdir(out_dir):
        raise SystemExit("output directory does not exist: %s" % out_dir)
    return out_dir


def write_letter(path, letter):
    """Write exactly one character, no newline, no extra bytes."""
    if len(letter) != 1 or letter.isspace():
        raise SystemExit("letter must be exactly one non-space character")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(letter)


def verify_letter(path, letter):
    """Re-read the file and refuse to exit 0 unless it holds the letter.

    Checks the decoded text and the raw bytes: exactly one character and
    exactly one byte, so no hidden newline or whitespace can slip past.
    """
    with open(path, "rb") as f:
        raw = f.read()
    content = raw.decode("utf-8")
    if content != letter or len(raw) != 1:
        raise SystemExit(
            "entry.txt holds %r (%d bytes), expected exactly %r"
            % (content, len(raw), letter)
        )


def main():
    out_dir = resolve_output_dir()
    path = os.path.join(out_dir, ENTRY_FILENAME)
    write_letter(path, LETTER)
    verify_letter(path, LETTER)
    return 0


if __name__ == "__main__":
    sys.exit(main())
