# Pipeline overview

This workflow combines standard public bioinformatics tools with small custom parsers needed for manuscript-specific coordinate projection and summary tables.

Standard-tool stages are represented as shell recipes in `commands/`. Custom stages are represented as portable Python scripts in `scripts/`; all scripts use command-line arguments rather than local absolute paths.

The final scientific interpretation remains conservative: the workflow supports computational prioritization of AsCEP19-200 and AsCEP20-170, not experimental RNAi/SIGS efficacy.
