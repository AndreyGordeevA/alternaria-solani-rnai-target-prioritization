# AsCEP19/AsCEP20 computational target-prioritization pipeline

This repository provides a reproducible computational workflow for reproducing the core analyses supporting prioritization of AsCEP19-200 and AsCEP20-170.

## What this repository reproduces

- Public reference/resource inventory used in the study.
- Locus and public-assembly evidence summaries.
- Mapping-based support for the NL03003-like locus in the PRJNA746421 read panel.
- Positive-control validation summaries.
- CDS/candidate projection logic.
- Variability projection and internal/external candidate-window classification.
- 21-nt candidate-window retention metrics.
- Host-reference off-target screening summaries.
- Expanded mismatch-aware 19-21 nt host-reference screening.
- Direct final-candidate uniqueness BLASTn rerun against the NL03003 genome.
- Supplementary-table assembly checks and manifest generation.
- Figure-regeneration inputs and documented plotting entry points where applicable.


## Pipeline stages

1. **Input/resource inventory**: record public accessions, reference versions, local input filenames and checksums.
2. **Locus/reference preparation**: prepare FASTA references and BLAST databases using standard tools.
3. **Mapping-based locus support**: map PRJNA746421 reads to the NL03003 genome with BWA-MEM and summarize locus coverage with SAMtools.
4. **Positive-control validation**: apply the same mapping/coverage summaries to representative positive controls.
5. **CDS/candidate projection**: use documented projection scripts to map exon-derived coding intervals and candidate boundaries.
6. **Variability filtering**: project variant positions onto coding/candidate coordinates and count internal/external variable positions.
7. **21-nt window analysis**: enumerate overlapping windows and retain windows that avoid projected internal variable positions.
8. **Host off-target screening**: run BLASTn and k-mer based host-reference screens against potato and tomato references.
9. **Expanded mismatch-aware 19-21 nt screen**: enumerate forward and reverse-complement windows and summarize exact, one-mismatch and two-mismatch matches.
10. **Candidate-level uniqueness rerun**: run BLASTn for final candidate fragments against the NL03003 genome and classify HSPs.
11. **Supplementary output generation**: assemble publication-facing supplementary tables, README, manifest and checksums from curated outputs.
12. **Figure regeneration**: rebuild figure data inputs and, where plotting code is available, regenerate figure panels from documented inputs.

## Recommended run order

1. Edit `configs/input_paths.example.env` or create a local copy named `input_paths.env`.
2. Run the command recipes in `commands/` in numeric order.
3. Run the Python scripts in `scripts/` where a stage requires custom projection, parsing or summarization.
4. Compare generated outputs to the schema notes in `configs/expected_output_schemas.md`.
5. Update manifests and checksums with `scripts/assemble_supplementary_manifest.py`.

## Environment

The workflow expects a POSIX shell, Python 3.10 or later, BLAST+, BWA-MEM, SAMtools and seqkit. Optional plotting can use Python with matplotlib/pandas or an equivalent local plotting environment.

## Manuscript and supplementary links

The `supplementary_links/` directory maps pipeline outputs to Supplementary Tables S1-S10 and Supplementary File S6. The `expected_outputs/` directory contains schema-level examples and selected expected-output references, not a replacement for running the workflow.

## Quick functional test

The archive includes a small toy dataset that is independent of the article results. To run it:

```bash
cd examples/demo_workflow
bash run_demo.sh
```

The expected result is a completed run with outputs under `examples/demo_workflow/outputs/`.
