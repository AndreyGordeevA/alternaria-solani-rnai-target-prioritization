# Rebuild supplementary outputs recipe

This recipe documents how to rebuild the publication-facing supplementary package from curated pipeline outputs. It is intentionally a procedure rather than a single command because several source tables are scientific summaries produced by upstream stages.

1. Generate or update the stage outputs listed in `supplementary_links/supplementary_output_map.tsv`.
2. Validate each table against `configs/expected_output_schemas.md`.
3. Copy the selected final tables into a clean supplementary output directory with publication-neutral filenames.
4. Copy the final candidate FASTA as `Supplementary_File_S6_candidate_fragments.fa`.
5. Run:

```bash
python3 scripts/assemble_supplementary_manifest.py \
  --supplementary-dir outputs/supplementary_materials \
  --manifest outputs/supplementary_materials/MANIFEST_supplementary_package.tsv \
  --checksums outputs/supplementary_materials/SHA256SUMS_supplementary_package.txt
```

6. Compare the generated manifest and checksums to the frozen publication package before submission.
