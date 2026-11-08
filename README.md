# Assignment 4 Kazakh language dataset audit

Open `Assignment4_Report.docx`. It contains the main report, two figures and Appendices A, B and C. `Protocol_Freeze.docx` and `Appendix_C_Verification.docx` are convenient standalone copies of the corresponding appendices. The full issue table is `results/error_analysis.csv`.

## Reproduce

1. Extract the ZIP into a writable directory.
2. Install or use Python 3.10 or later. No third-party analysis dependencies are required.
3. In the extracted package directory run:

```text
python reproduce.py
```

Expected: 29 tests pass, three complete runs produce identical analytical files, 7 resources, 6 tasks, 2 LLM evaluation entries, 4 unknown licence entries. Running again replaces analytical outputs, the environment record and execution/test logs. The recorded execution used Python 3.12.14 on Windows; other Python/OS combinations have not been tested here.

Individual commands are also available:

```text
python analyze_datasets.py --output-dir results
python compare_methods.py --output-dir results
python -m unittest -v test_analyze_datasets test_compare_methods
```

## What was implemented

- Preserved historical seven-record source JSON and supplied originals.
- Rechecked eight official ACL publication abstracts on 2 November 2026; saved paraphrased observations, URLs, locators, decisions and dates.
- Implemented B1 inventory retention and B2 minimal structural checks on the same eight candidates. Both keep 8 candidates; proposed source screening keeps 7.
- Exported 24 candidate-by-method predictions, a comparison table, deterministic summaries and sensitivity results.
- Separated confirmed artifact errors from numerical scope caveats and unresolved licence/release evidence.
- Added eight tests to the inherited 21-test suite and recorded three deterministic runs.

The source-reviewed decisions are also the reference labels. Proposed agreement is 100% by construction. Baseline agreement is 87.5%, with one disputed aggregate study. On the seven undisputed candidates all three methods agree completely. This is a retrospective local ablation, not independent validation, a held-out efficacy test or a model comparison. No unavailable original eight-row CSV or script is represented as recovered.

## Files and evidence

- `sources/source_observations.json`: seven historical records copied unchanged from the supplied ZIP.
- `sources/seed_candidates.csv`: reconstructed candidate identity list, with task/year/link fields; see `sources/PROVENANCE.md`.
- `sources/screening_evidence.csv`: eight current inclusion labels and reasons.
- `sources/source_recheck.csv`: current abstract-level source observations.
- `results/analysis_output.json`: counts and historical-input SHA-256.
- `results/comparison.json`: method metrics, sensitivity and comparison-input hashes.
- `results/baseline_predictions.csv`: per-candidate predictions.
- `results/error_analysis.csv`: seven full issue records.
- `results/reproduction_log.json` and `results/TEST_RESULTS.txt`: actual run evidence.
- `provenance/`: uploaded original DOCX, original ZIP and historical screening log.
- `MANIFEST_SHA256.txt`: final file hashes, excluding itself and transient Python caches.

## Boundaries and pending actions

The audit covers publication metadata, not corpus contents. All seven release versions are unverified. Unknown licence does not mean no licence. The eight-field documentation-completeness metric and broader 15–30-resource search were not completed. No linguistic-quality, training-utility, fairness or model-performance result is claimed. No significance test is used because the paired purposive cases and reference construction do not support a general efficacy claim.

The protocol is retrospective, dated 2 November 2026; instructor acceptance is pending. Appendix C honestly records AI-assisted automated execution and leaves independent reviewer fields pending. Students must review the work and arrange actual independent reproduction before filling those fields. GitHub publication, a remote commit/tag and Moodle submission have not been performed. Do not present this package as satisfying those external requirements.

The package contains publicly described metadata and the user's supplied source artifacts. It contains no downloaded corpus samples. Final documents were checked visually through Microsoft Word page exports; the standard LibreOffice renderer was unavailable on this Windows machine.
