#!/usr/bin/env python3
"""Count projected variable positions and retained 21-nt windows for candidates.

Inputs: candidate interval table and projected variable-position table.
Outputs: candidate-level variability and 21-nt retention metrics.
"""

from __future__ import annotations

import argparse
import csv


def parse_range(text: str) -> tuple[int, int]:
    start, end = text.replace(":", "-").split("-")[-2:]
    return int(start), int(end)


def read_rows(path: str) -> list[dict[str, str]]:
    with open(path, "r", encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-table", required=True)
    parser.add_argument("--variable-position-table", required=True)
    parser.add_argument("--candidate-id-column", default="candidate_id")
    parser.add_argument("--interval-column", default="coding_model_interval")
    parser.add_argument("--variable-position-column", default="coding_position")
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    candidates = read_rows(args.candidate_table)
    variables = read_rows(args.variable_position_table)
    variable_positions = {int(row[args.variable_position_column]) for row in variables if row.get(args.variable_position_column, "").isdigit()}
    output_rows = []
    for row in candidates:
        start, end = parse_range(row[args.interval_column])
        inside = sorted(pos for pos in variable_positions if start <= pos <= end)
        length = end - start + 1
        total_windows = max(0, length - 21 + 1)
        retained = 0
        for offset in range(total_windows):
            w_start = start + offset
            w_end = w_start + 20
            if not any(w_start <= pos <= w_end for pos in inside):
                retained += 1
        output_rows.append({
            "candidate_id": row[args.candidate_id_column],
            "candidate_interval": f"{start}-{end}",
            "projected_variable_positions_inside_candidate": len(inside),
            "total_21nt_windows": total_windows,
            "retained_21nt_windows": retained,
            "retained_21nt_percent": f"{(100.0 * retained / total_windows if total_windows else 0):.2f}",
        })
    with open(args.output, "w", encoding="utf-8", newline="") as out:
        writer = csv.DictWriter(out, delimiter="\t", fieldnames=list(output_rows[0]) if output_rows else ["candidate_id"])
        writer.writeheader()
        writer.writerows(output_rows)


if __name__ == "__main__":
    main()
