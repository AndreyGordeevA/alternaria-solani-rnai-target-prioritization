#!/usr/bin/env bash
set -euo pipefail

: "${OUTPUT_DIR:?Set OUTPUT_DIR}"
: "${CANDIDATE_FASTA:?Set CANDIDATE_FASTA}"
: "${HOST_REFERENCE_FASTA:?Set HOST_REFERENCE_FASTA}"
: "${HOST_REFERENCE_NAME:?Set HOST_REFERENCE_NAME}"

mkdir -p "${OUTPUT_DIR}/host_offtarget/blastdb" "${OUTPUT_DIR}/host_offtarget/windows"

makeblastdb \
  -in "${HOST_REFERENCE_FASTA}" \
  -dbtype nucl \
  -parse_seqids \
  -out "${OUTPUT_DIR}/host_offtarget/blastdb/${HOST_REFERENCE_NAME}"

blastn \
  -query "${CANDIDATE_FASTA}" \
  -db "${OUTPUT_DIR}/host_offtarget/blastdb/${HOST_REFERENCE_NAME}" \
  -task blastn \
  -word_size 7 \
  -dust no \
  -evalue 1000 \
  -perc_identity 70 \
  -outfmt "6 qseqid sseqid pident length qlen qstart qend sstart send sstrand mismatch gapopen evalue bitscore qcovs" \
  -out "${OUTPUT_DIR}/host_offtarget/${HOST_REFERENCE_NAME}.candidate_blastn.tsv"

python3 scripts/mismatch_aware_kmer_screen.py \
  --query-fasta "${CANDIDATE_FASTA}" \
  --reference-fasta "${HOST_REFERENCE_FASTA}" \
  --reference-name "${HOST_REFERENCE_NAME}" \
  --output-summary "${OUTPUT_DIR}/host_offtarget/${HOST_REFERENCE_NAME}.mismatch_summary.tsv" \
  --output-detail "${OUTPUT_DIR}/host_offtarget/${HOST_REFERENCE_NAME}.mismatch_detail.tsv"
