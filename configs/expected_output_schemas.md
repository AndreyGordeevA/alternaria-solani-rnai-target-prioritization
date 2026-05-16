# Expected output schema notes

## mapping_locus_support.tsv

Required columns: sample_id, run_accession, mapping_target, target_interval, mapping_mode, aligner, mapq_filter, interval_length_bp, breadth_1x_percent, breadth_mapq20_percent, mean_depth, median_depth, min_depth, max_depth, support_status, support_rule, notes.

## candidate_projection.tsv

Required columns: candidate_id, gene, candidate_length, coding_model_interval, compound_genomic_projection, strand, candidate_sequence_source, notes.

## variability_21nt_metrics.tsv

Required columns: candidate_id, gene, candidate_length, candidate_interval, projected_variable_positions_inside_candidate, projected_variable_positions_outside_candidate, total_21nt_windows, retained_21nt_windows, retained_21nt_percent, notes.

## mismatch_aware_host_screen.tsv

Required columns: candidate_id, host, reference_name, reference_type, window_size, mismatch_count, orientation, query_window_id, hit_count, interpretation.

## candidate_uniqueness_hits.tsv

Required columns: qseqid, sseqid, pident, length, qlen, qstart, qend, sstart, send, sstrand, mismatch, gapopen, evalue, bitscore, qcovs, match_class, rationale.
