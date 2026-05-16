#!/usr/bin/env python3
"""Summarize per-base depth over a target locus.

Inputs: SAMtools depth output with reference, position and depth columns.
Outputs: One-row TSV with interval length, breadth and depth metrics.
"""

from __future__ import annotations

import argparse
import csv
from statistics import mean, median


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--depth", required=True)
    parser.add_argument("--sample-id", required=True)
    parser.add_argument("--target-region", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    depths = []
    with open(args.depth, "r", encoding="utf-8") as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 3:
                depths.append(int(parts[2]))

    interval_length = len(depths)
    covered = sum(1 for value in depths if value > 0)
    breadth = 100.0 * covered / interval_length if interval_length else 0.0
    mean_depth = mean(depths) if depths else 0.0
    median_depth = median(depths) if depths else 0.0
    support_status = "SUPPORTED" if breadth >= 90.0 and mean_depth >= 5.0 else "NOT_SUPPORTED"

    row = {
        "sample_id": args.sample_id,
        "target_region": args.target_region,
        "interval_length_bp": interval_length,
        "breadth_1x_percent": f"{breadth:.2f}",
        "mean_depth": f"{mean_depth:.2f}",
        "median_depth": f"{median_depth:.2f}",
        "min_depth": min(depths) if depths else 0,
        "max_depth": max(depths) if depths else 0,
        "support_status": support_status,
        "support_rule": "breadth_1x_percent >= 90 and mean_depth >= 5",
    }
    with open(args.output, "w", encoding="utf-8", newline="") as out:
        writer = csv.DictWriter(out, delimiter="\t", fieldnames=list(row))
        writer.writeheader()
        writer.writerow(row)


if __name__ == "__main__":
    main()
