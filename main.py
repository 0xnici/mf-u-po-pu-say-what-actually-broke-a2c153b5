#!/usr/bin/env python3
"""Write the winning one-line error copy to the make.fun output directory."""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

MAX_CHARS = 200


def fail(message: str) -> None:
    """Print a clear diagnostic to stderr and exit non-zero."""
    print(f"main.py: {message}", file=sys.stderr)
    sys.exit(1)


def load_answer() -> str:
    """Read and validate the single-line answer from answer.txt at repo root."""
    root = Path(__file__).resolve().parent
    path = root / "answer.txt"
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        fail(f"cannot read {path}: {exc}")

    if not text:
        fail("answer.txt is empty")
    if len(text) > MAX_CHARS:
        fail(f"answer.txt is {len(text)} chars; max is {MAX_CHARS}")
    if "\n" in text or "\r" in text:
        fail("answer.txt must be a single line (no newlines)")
    if not text.strip():
        fail("answer.txt is only whitespace")
    # Reject embedded control characters (including NUL) that would corrupt output
    if any(ord(ch) < 32 for ch in text):
        fail("answer.txt contains control characters")
    return text


def write_entry(text: str) -> None:
    """
    Atomically write the UTF-8 payload to entry.txt in the output directory.

    Atomicity matters because the grader may read the file while we write it.
    We create a temp file in the SAME directory, set permissions on its fd
    (os.fchmod — no TOCTOU), flush to disk, then os.replace into place.
    The replace is atomic on POSIX and never touches other files.
    """
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = text.encode("utf-8")

    with tempfile.NamedTemporaryFile(dir=out_dir, prefix=".entry-", delete=False) as tmp:
        tmp.write(payload)
        tmp.flush()
        os.fsync(tmp.fileno())
        # Set 0644 on the open fd — no window for chmod race.
        os.fchmod(tmp.fileno(), 0o644)
        tmp_path = tmp.name

    try:
        os.replace(tmp_path, out_dir / "entry.txt")
    except BaseException:
        # Cleanup ONLY our own temp file on any error.
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise

    # Verify byte-for-byte: grader compares exact bytes.
    written = (out_dir / "entry.txt").read_bytes()
    if written != payload:
        fail("entry.txt failed byte-for-byte verification")


def main() -> None:
    write_entry(load_answer())


if __name__ == "__main__":
    main()