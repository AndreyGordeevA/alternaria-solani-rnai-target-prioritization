#!/usr/bin/env bash
set -euo pipefail

: "${OUTPUT_DIR:?Set OUTPUT_DIR}"
: "${NL03003_GENOME_FASTA:?Set NL03003_GENOME_FASTA}"
: "${READS_R1:?Set READS_R1}"
: "${READS_R2:?Set READS_R2}"
: "${SAMPLE_ID:?Set SAMPLE_ID}"
: "${TARGET_REGION:=CP022026.1:240000-248000}"
: "${THREADS:=4}"

mkdir -p "${OUTPUT_DIR}/mapping"

bwa index "${NL03003_GENOME_FASTA}"

bwa mem -t "${THREADS}" "${NL03003_GENOME_FASTA}" "${READS_R1}" "${READS_R2}" \
  | samtools view -b -F 4 -q 20 - \
  | samtools sort -@ "${THREADS}" -o "${OUTPUT_DIR}/mapping/${SAMPLE_ID}.mapq20.sorted.bam"

samtools index "${OUTPUT_DIR}/mapping/${SAMPLE_ID}.mapq20.sorted.bam"
samtools depth -aa -r "${TARGET_REGION}" "${OUTPUT_DIR}/mapping/${SAMPLE_ID}.mapq20.sorted.bam" \
  > "${OUTPUT_DIR}/mapping/${SAMPLE_ID}.target_depth.tsv"

python3 scripts/summarize_locus_depth.py \
  --depth "${OUTPUT_DIR}/mapping/${SAMPLE_ID}.target_depth.tsv" \
  --sample-id "${SAMPLE_ID}" \
  --target-region "${TARGET_REGION}" \
  --output "${OUTPUT_DIR}/mapping/${SAMPLE_ID}.locus_support_summary.tsv"
