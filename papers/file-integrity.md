# File integrity and analysis snapshot

Primary-image SHA-256 digests from the provenance manifest:

| Product | SHA-256 |
| --- | --- |
| DRXX | `45a3d5e5d32ed823e8a3e2ff0dc0f5ffeb5bd546c81be8d51e06c9f241b5e1fd` |
| DRLX | `911e661c99a4453f4b3d4bd13a3d35f049c5df965fcb3c91b014a47c38c7605f` |
| DRCX | `8aec700e07d61123151c0811332f76e10f13d1e3fb361de5b10476b4961c473f` |
| DRCL | `761c9c1774cfe5152ca7d5cb729de285d08fa78c3df05af8720cbd9599b37592` |

The original base revision identifies the reconstruction history. The [evidence manifest](paper-evidence-manifest.json) identifies the exact files used in the synthesis. The [typeset principal-hash list](paper-evidence-hashes.tex) is retained separately from the paper. Later replacements should be recorded as new revisions.

The journal revision starts from commit `0ba7b986dbf84afe5483991dc9330edbab3cc0fb` on `paper/nov13-journal-revision`. The verified starting manuscript and PDF hashes are in [journal-revision-baseline.json](journal-revision-baseline.json). Current source and compiled-PDF hashes, retained-result checks and the full manifest verification are recorded in [journal-numerical-verification.json](journal-numerical-verification.json). The two distributed PDF copies are identical. Figure source products, display transforms and coordinates are recorded in [figure-provenance.json](figure-provenance.json).
