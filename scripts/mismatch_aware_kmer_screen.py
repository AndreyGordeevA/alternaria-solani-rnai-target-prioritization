#!/usr/bin/env python3
"""Screen 19-21 nt candidate windows against a host reference with up to two mismatches.

Inputs: candidate FASTA and host-reference FASTA.
Outputs: detailed retained-window matches and a compact summary table.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict


def read_fasta(path: str) -> list[tuple[str, str]]:
    records = []
    name = None
    chunks = []
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
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


def revcomp(seq: str) -> str:
    return seq.translate(str.maketrans("ACGTNacgtn", "TGCANtgcan"))[::-1].upper()


def mismatches(a: str, b: str) -> int:
    return sum(x != y for x, y in zip(a, b))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query-fasta", required=True)
    parser.add_argument("--reference-fasta", required=True)
    parser.add_argument("--reference-name", required=True)
    parser.add_argument("--output-summary", required=True)
    parser.add_argument("--output-detail", required=True)
    parser.add_argument("--max-mismatches", type=int, default=2)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    references = read_fasta(args.reference_fasta)
    queries = read_fasta(args.query_fasta)
    summary = defaultdict(int)
    details = []
    for qid, qseq in queries:
        for size in (19, 20, 21):
            for start0 in range(0, max(0, len(qseq) - size + 1)):
                window = qseq[start0:start0 + size]
                for orientation, query_window in (("forward", window), ("reverse_complement", revcomp(window))):
                    for rid, rseq in references:
                        for rstart0 in range(0, max(0, len(rseq) - size + 1)):
                            ref_window = rseq[rstart0:rstart0 + size]
                            mm = mismatches(query_window, ref_window)
                            if mm <= args.max_mismatches:
                                summary[(qid, size, mm, orientation)] += 1
                                details.append({
                                    "candidate_id": qid,
                                    "reference_name": args.reference_name,
                                    "reference_record": rid,
                                    "window_size": size,
                                    "mismatch_count": mm,
                                    "orientation": orientation,
                                    "query_start": start0 + 1,
                                    "reference_start": rstart0 + 1,
                                })
    with open(args.output_detail, "w", encoding="utf-8", newline="") as out:
        fields = ["candidate_id", "reference_name", "reference_record", "window_size", "mismatch_count", "orientation", "query_start", "reference_start"]
        writer = csv.DictWriter(out, delimiter="\t", fieldnames=fields)
        writer.writeheader()
        writer.writerows(details)
    with open(args.output_summary, "w", encoding="utf-8", newline="") as out:
        fields = ["candidate_id", "reference_name", "window_size", "mismatch_count", "orientation", "hit_count"]
        writer = csv.DictWriter(out, delimiter="\t", fieldnames=fields)
        writer.writeheader()
        for (qid, size, mm, orientation), count in sorted(summary.items()):
            writer.writerow({
                "candidate_id": qid,
                "reference_name": args.reference_name,
                "window_size": size,
                "mismatch_count": mm,
                "orientation": orientation,
                "hit_count": count,
            })


if __name__ == "__main__":
    main()
