#!/usr/bin/env python3
"""Validate and emit the Absurd Micro-Startup Pitch-Off entry.

Reads entry.txt next to this script, validates the contest gate
(UTF-8 text, 1-200 characters, not only whitespace, no embedded
newline/CR), and writes the exact normalized bytes to
$MAKEFUN_OUTPUT_DIR/entry.txt (default "output/").

Pure Python standard library only.
"""

import os
import sys


def fail(message):
    print("error: " + message, file=sys.stderr)
    sys.exit(1)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(here, "entry.txt")

    try:
        with open(source_path, "rb") as handle:
            raw = handle.read()
    except OSError as exc:
        fail("cannot read entry.txt: %s" % exc)

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        fail("entry.txt is not valid UTF-8: %s" % exc)

    # Strip at most one trailing newline, then at most one trailing CR.
    if text.endswith("\n"):
        text = text[:-1]
    if text.endswith("\r"):
        text = text[:-1]

    if "\n" in text or "\r" in text:
        fail("entry.txt must be a single line (no newline/CR inside)")

    count = len(text)
    if count < 1:
        fail("entry.txt is empty (gate requires 1-200 characters)")
    if count > 200:
        fail("entry.txt is %d characters (gate allows at most 200)" % count)
    if not text.strip():
        fail("entry.txt contains only whitespace")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output/")
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as exc:
        fail("cannot create output dir %r: %s" % (out_dir, exc))

    out_path = os.path.join(out_dir, "entry.txt")
    data = text.encode("utf-8")
    try:
        with open(out_path, "wb") as handle:
            handle.write(data)
        os.chmod(out_path, 0o644)
    except OSError as exc:
        fail("cannot write %r: %s" % (out_path, exc))

    print("entry.txt: %d characters" % count)


if __name__ == "__main__":
    main()
