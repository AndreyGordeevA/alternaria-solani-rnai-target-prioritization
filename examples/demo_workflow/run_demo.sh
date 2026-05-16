#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
OUT="${SCRIPT_DIR}/outputs"
mkdir -p "${OUT}/uniqueness" "${OUT}/host" "${OUT}/windows"

cat > "${OUT}/windows/demo_candidate_intervals.tsv" <<'TSV'
candidate_id	coding_model_interval
Candidate_A_180	1-180
Candidate_B_160	1-160
TSV

printf "coding_position\n" > "${OUT}/windows/empty_variable_positions.tsv"

python3 "${REPO_ROOT}/scripts/project_variability_and_count_windows.py" \
  --candidate-table "${OUT}/windows/demo_candidate_intervals.tsv" \
  --variable-position-table "${OUT}/windows/empty_variable_positions.tsv" \
  --candidate-id-column candidate_id \
  --interval-column coding_model_interval \
  --variable-position-column coding_position \
  --output "${OUT}/windows/demo_window_metrics.tsv"

makeblastdb \
  -in "${SCRIPT_DIR}/inputs/toy_reference_genome.fa" \
  -dbtype nucl \
  -parse_seqids \
  -out "${OUT}/uniqueness/toy_reference" >/dev/null

blastn \
  -query "${SCRIPT_DIR}/inputs/demo_candidates.fa" \
  -db "${OUT}/uniqueness/toy_reference" \
  -task blastn \
  -dust no \
  -soft_masking false \
  -word_size 7 \
  -evalue 1000 \
  -max_target_seqs 100000 \
  -outfmt "6 qseqid sseqid pident length qlen qstart qend sstart send sstrand mismatch gapopen evalue bitscore qcovs" \
  -out "${OUT}/uniqueness/demo_uniqueness_raw_hits.tsv"

python3 "${REPO_ROOT}/scripts/classify_candidate_uniqueness_hits.py" \
  --raw-hits "${OUT}/uniqueness/demo_uniqueness_raw_hits.tsv" \
  --output-hits "${OUT}/uniqueness/demo_uniqueness_classified_hits.tsv" \
  --output-summary "${OUT}/uniqueness/demo_uniqueness_summary.tsv"

python3 "${REPO_ROOT}/scripts/mismatch_aware_kmer_screen.py" \
  --query-fasta "${SCRIPT_DIR}/inputs/demo_candidates.fa" \
  --reference-fasta "${SCRIPT_DIR}/inputs/toy_host_reference.fa" \
  --reference-name toy_host \
  --output-summary "${OUT}/host/demo_host_mismatch_summary.tsv" \
  --output-detail "${OUT}/host/demo_host_mismatch_detail.tsv"

python3 - <<PY
from pathlib import Path
expected = Path("${SCRIPT_DIR}/expected_outputs/demo_window_metrics.tsv").read_text().splitlines()
observed = Path("${OUT}/windows/demo_window_metrics.tsv").read_text().splitlines()
if expected != observed:
    raise SystemExit("demo_window_metrics.tsv differs from expected output")
PY
test -s "${OUT}/uniqueness/demo_uniqueness_summary.tsv"
test -s "${OUT}/host/demo_host_mismatch_summary.tsv"

echo "Demo workflow completed"
