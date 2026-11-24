"""Real-Life Patch Notes: The Comedy Changelog — entry program.

Writes one single-line patch note to ``entry.txt`` inside the output
directory: ``$MAKEFUN_OUTPUT_DIR`` when set, otherwise a repo-local
``output/`` directory. The text is written as UTF-8 with no trailing
newline, exactly as the sealed gate scorer expects it.
"""

import os
import re

LINE = (
    "v1.9.3: Fixed a bug where the brain replayed your most embarrassing "
    "moment from 2014 at 3 a.m. instead of sleeping."
)

_VERSION_RE = re.compile(r"\bv\d+\.\d+\.\d+\b")
_CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def validate(text: str) -> None:
    """Enforce the competition gate and the release-note shape.

    Gate: 1-160 characters, valid single-line text, not only whitespace.
    Shape: a real release note carries a version number and no control
    characters, so a line missing either is rejected before it is written.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if len(text) < 1:
        raise ValueError("entry must be at least 1 character")
    if not text.strip():
        raise ValueError("entry must not be empty or whitespace only")
    if len(text) > 160:
        raise ValueError("entry exceeds 160 characters")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if _CONTROL_RE.search(text):
        raise ValueError("entry must not contain control characters")
    if not _VERSION_RE.search(text):
        raise ValueError("entry must carry a version number like v1.9.3")


def main() -> None:
    validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "output"
    )
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)


if __name__ == "__main__":
    main()
