#!/usr/bin/env python3
"""Create a manifest and SHA256 checksum file for a supplementary package.

Inputs: supplementary package directory.
Outputs: manifest TSV and SHA256SUMS text file.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--supplementary-dir", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--checksums", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.supplementary_dir)
    rows = []
    checksum_lines = []
    for path in sorted(root.rglob("*")):
        if path.is_file():
            relative = path.relative_to(root).as_posix()
            digest = sha256(path)
            rows.append({"relative_path": relative, "size_bytes": path.stat().st_size, "sha256": digest})
            checksum_lines.append(f"{digest}  {relative}")
    with open(args.manifest, "w", encoding="utf-8", newline="") as out:
        writer = csv.DictWriter(out, delimiter="\t", fieldnames=["relative_path", "size_bytes", "sha256"])
        writer.writeheader()
        writer.writerows(rows)
    Path(args.checksums).write_text("\n".join(checksum_lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
