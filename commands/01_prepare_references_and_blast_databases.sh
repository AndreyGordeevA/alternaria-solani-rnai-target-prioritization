#!/usr/bin/env bash
set -euo pipefail

: "${INPUT_DIR:?Set INPUT_DIR}"
: "${OUTPUT_DIR:?Set OUTPUT_DIR}"
: "${NL03003_GENOME_FASTA:?Set NL03003_GENOME_FASTA}"
: "${THREADS:=4}"

mkdir -p "${OUTPUT_DIR}/references" "${OUTPUT_DIR}/blastdb"

seqkit stats "${NL03003_GENOME_FASTA}" > "${OUTPUT_DIR}/references/NL03003_seqkit_stats.tsv"
samtools faidx "${NL03003_GENOME_FASTA}"

makeblastdb \
  -in "${NL03003_GENOME_FASTA}" \
  -dbtype nucl \
  -parse_seqids \
  -out "${OUTPUT_DIR}/blastdb/NL03003_genome"
