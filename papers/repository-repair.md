# Repository and documentation repair, 13 November 2026

The repair integrates the completed journal revision into `master`. The pre-repair master commit is `116609107a0a1d666f64f78e164a8af92c06f4c2`, retained on `backup/master-before-repair-20261113`. The completed journal manuscript is preserved at `664d7eb`; its branch was integrated with a normal merge so both histories remain reachable.

## Current documents

The active technical paper is `papers/martian-cylinder-technical-paper.tex` with its matching 18-page PDF, dated 13 November 2026. The root PDF is identical. The active essay is revision 16. README, the agent summary, citation/deposit metadata and the reconstruction summaries now point to those versions and report their current results. The technical manuscript itself was imported intact from the journal revision.

Twenty-five superseded documents and bundles are preserved under `archive/superseded-docs-2026-11-13/`, including older README/agent summaries, reconstruction prose, essay revisions 10-13, historical research drafts, the earlier paper-verification narrative, the older technical source/PDF, retired schematic figures and the earlier research ZIP. `provenance.json` records their source commits, original locations and hashes. The obsolete research drafts and verification narrative were removed from active locations after archive copies were checked. Historical numerical analyses, protocols and original measurements remain available as evidence.

## Merge and path corrections

The earlier source relocation moved nine implementation files into `independent-reconstruction/scripts/` while leaving their `OUT_DIR` expressions one directory too deep. The repair restores `independent-reconstruction/` as their output root and `data/` as their image root. Old audit, comparison and validation imports now select the canonical scripts directory. The reproduction audit invokes the relocated pipeline entry point. Analytical expressions and the stored result arrays were preserved. `merge-path-repairs.json` lists affected scripts.

The finite-model provenance test now checks the frozen pre-journal paper through its retained Git snapshot. It accepts documented path-only substitutions and LF/CRLF conversion when validating historical source hashes. It continues to verify numerical inputs and reject unrelated source changes.

The verification workflow installs the paper dependencies, runs the existing comparison, audit and physical-model tests, regenerates figures, and checks current document/data paths. Full Git history is available for the historical provenance assertions. `papers/check_repository.py` checks the latest paper/essay, matching PDF distribution, evidence hashes, native image decoding, script roots and active navigation links.

## Temporary files and repository size

The accidentally tracked `tmp/` environment and build snapshots were removed from the Git index. Their local files remain available and `tmp/` is ignored. This removes about 288 MiB and more than six thousand temporary files from the current tracked tree. It does not rewrite existing Git history or reduce already stored historical packs. The local 514 MiB temporary directory and the existing virtual environment were preserved.

## Verification

All six comparison tests, fifteen independent audit tests and fifteen finite-geometry/provenance tests passed. The audit suite required normal Windows temporary-file access because the sandbox denied temporary log creation. An isolated predictive replay and rebuilt manuscript are checked against the imported journal results. The figure/data build and repository-path checks verify the final active tree. Current numerical and PDF hashes are recorded in `journal-numerical-verification.json`.

The scientific limits of the paper remain documented in the manuscript: complete physical-scene validation, ambiguous partial geological boundaries and origin remain unresolved. These are separate from the repaired repository/documentation issues.
