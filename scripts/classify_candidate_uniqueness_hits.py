#!/usr/bin/env python3
"""Classify candidate-vs-genome BLASTn hits for candidate-level uniqueness.

Inputs: BLAST outfmt 6 with qseqid, sseqid, pident, length, qlen, qstart, qend,
sstart, send, sstrand, mismatch, gapopen, evalue, bitscore and qcovs.
Outputs: classified hit table and candidate-level summary.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict


FIELDS = ["qseqid", "sseqid", "pident", "length", "qlen", "qstart", "qend", "sstart", "send", "sstrand", "mismatch", "gapopen", "evalue", "bitscore", "qcovs"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-hits", required=True)
    parser.add_argument("--output-hits", required=True)
    parser.add_argument("--output-summary", required=True)
    return parser.parse_args()


def classify(row: dict[str, str]) -> tuple[str, str]:
    pident = float(row["pident"])
    qcov = 100.0 * int(row["length"]) / int(row["qlen"])
    if qcov >= 95 and pident >= 99:
        return "full_length_near_identity", "query coverage >=95% and identity >=99%"
    if qcov >= 95:
        return "full_length_lower_identity", "query coverage >=95% with lower identity"
    if qcov >= 50 and pident >= 95:
        return "partial_high_identity", "partial HSP with identity >=95%"
    if qcov >= 25:
        return "partial_lower_identity", "partial HSP below high-identity threshold"
    return "weak_background", "short or weak HSP"


def main() -> None:
    args = parse_args()
    hits = []
    with open(args.raw_hits, "r", encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            values = line.rstrip("\n").split("\t")
            row = dict(zip(FIELDS, values))
            match_class, rationale = classify(row)
            row["candidate_id"] = row["qseqid"]
            row["hit_id"] = f"{row['sseqid']}:{row['sstart']}-{row['send']}:{row['sstrand']}"
            row["match_class"] = match_class
            row["rationale"] = rationale
            hits.append(row)
    with open(args.output_hits, "w", encoding="utf-8", newline="") as out:
        fields = ["candidate_id", "hit_id"] + FIELDS + ["match_class", "rationale"]
        writer = csv.DictWriter(out, delimiter="\t", fieldnames=fields)
        writer.writeheader()
        writer.writerows(hits)
    grouped = defaultdict(list)
    for row in hits:
        grouped[row["candidate_id"]].append(row)
    with open(args.output_summary, "w", encoding="utf-8", newline="") as out:
        fields = ["candidate_id", "total_hits_detected", "full_length_near_identity_hits", "partial_high_identity_hits", "candidate_level_uniqueness_status"]
        writer = csv.DictWriter(out, delimiter="\t", fieldnames=fields)
        writer.writeheader()
        for candidate_id, rows in sorted(grouped.items()):
            full = sum(1 for row in rows if row["match_class"] == "full_length_near_identity")
            partial = sum(1 for row in rows if row["match_class"] == "partial_high_identity")
            status = "requires_manual_interpretation"
            if full <= 1 and partial == 0:
                status = "supported_unique"
            elif full <= 1:
                status = "mostly_unique_with_minor_partial_background"
            writer.writerow({
                "candidate_id": candidate_id,
                "total_hits_detected": len(rows),
                "full_length_near_identity_hits": full,
                "partial_high_identity_hits": partial,
                "candidate_level_uniqueness_status": status,
            })


if __name__ == "__main__":
    main()
