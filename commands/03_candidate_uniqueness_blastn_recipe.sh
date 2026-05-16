#!/usr/bin/env bash
set -euo pipefail

: "${OUTPUT_DIR:?Set OUTPUT_DIR}"
: "${CANDIDATE_FASTA:?Set CANDIDATE_FASTA}"
: "${NL03003_GENOME_FASTA:?Set NL03003_GENOME_FASTA}"

mkdir -p "${OUTPUT_DIR}/candidate_uniqueness/blastdb"

makeblastdb \
  -in "${NL03003_GENOME_FASTA}" \
  -dbtype nucl \
  -parse_seqids \
  -out "${OUTPUT_DIR}/candidate_uniqueness/blastdb/NL03003_genome"

blastn \
  -query "${CANDIDATE_FASTA}" \
  -db "${OUTPUT_DIR}/candidate_uniqueness/blastdb/NL03003_genome" \
  -task blastn \
  -dust no \
  -soft_masking false \
  -word_size 7 \
  -evalue 1000 \
  -max_target_seqs 100000 \
  -outfmt "6 qseqid sseqid pident length qlen qstart qend sstart send sstrand mismatch gapopen evalue bitscore qcovs" \
  -out "${OUTPUT_DIR}/candidate_uniqueness/raw_hits.tsv"

python3 scripts/classify_candidate_uniqueness_hits.py \
  --raw-hits "${OUTPUT_DIR}/candidate_uniqueness/raw_hits.tsv" \
  --output-hits "${OUTPUT_DIR}/candidate_uniqueness/classified_hits.tsv" \
  --output-summary "${OUTPUT_DIR}/candidate_uniqueness/summary.tsv"
