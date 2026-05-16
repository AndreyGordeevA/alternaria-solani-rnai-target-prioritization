#!/usr/bin/env python3
"""Generate fixed-length candidate windows from coding-model FASTA records.

Inputs: FASTA records representing oriented coding sequences.
Outputs: FASTA and TSV tables of candidate windows.
"""

from __future__ import annotations

import argparse
import csv


def read_fasta(path: str) -> list[tuple[str, str]]:
    records = []
    name = None
    chunks = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if name is not None:
                    records.append((name, "".join(chunks).upper()))
                name = line[1:].split()[0]
                chunks = []
            else:
                chunks.append(line)
        if name is not None:
            records.append((name, "".join(chunks).upper()))
    return records


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--coding-fasta", required=True)
    parser.add_argument("--window-length", type=int, required=True)
    parser.add_argument("--output-fasta", required=True)
    parser.add_argument("--output-tsv", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = []
    with open(args.output_fasta, "w", encoding="utf-8") as fasta:
        for record_id, seq in read_fasta(args.coding_fasta):
            for start0 in range(0, max(0, len(seq) - args.window_length + 1)):
                start = start0 + 1
                end = start0 + args.window_length
                candidate_id = f"{record_id}_window_{start}_{end}"
                subseq = seq[start0:end]
                fasta.write(f">{candidate_id}\n{subseq}\n")
                rows.append({
                    "candidate_id": candidate_id,
                    "source_record": record_id,
                    "window_length": args.window_length,
                    "coding_start": start,
                    "coding_end": end,
                    "sequence": subseq,
                })
    with open(args.output_tsv, "w", encoding="utf-8", newline="") as out:
        writer = csv.DictWriter(out, delimiter="\t", fieldnames=list(rows[0]) if rows else ["candidate_id"])
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
