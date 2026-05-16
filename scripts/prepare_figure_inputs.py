#!/usr/bin/env python3
"""Collect figure input tables and record plotting provenance.

Inputs: a TSV mapping figure IDs to source table paths.
Outputs: a normalized figure-input manifest.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--figure-map", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    with open(args.figure_map, "r", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    out_rows = []
    for row in rows:
        source = Path(row["source_table"])
        out_rows.append({
            "figure_id": row["figure_id"],
            "source_table": row["source_table"],
            "source_exists": "YES" if source.exists() else "NO",
            "plotting_note": row.get("plotting_note", "Use manuscript figure style and journal formatting."),
        })
    with open(args.output, "w", encoding="utf-8", newline="") as out:
        writer = csv.DictWriter(out, delimiter="\t", fieldnames=["figure_id", "source_table", "source_exists", "plotting_note"])
        writer.writeheader()
        writer.writerows(out_rows)


if __name__ == "__main__":
    main()
