# Pilot metadata dictionary

## Assignment 4 comparison extension

The historical resource fields below remain unchanged. `sources/seed_candidates.csv` adds one row per candidate with `candidate_id`, `candidate`, `year`, `primary_task` and `source_url`. This eight-row input reconstructs the named seed list; it is not a recovered old inventory. Baseline 2 intentionally uses a fixed 2026 upper year bound for this dated comparison.

`sources/screening_evidence.csv` records include/exclude labels, reasons, evidence URLs, abstract locator, current review date and reviewer type. These are current AI-assisted decisions, with no independent coder. `sources/source_recheck.csv` separates current access from inherited historical dates.

`baseline_predictions.csv` contains 24 records: candidate ID and name, method, binary included decision and binary reference decision. `baseline_metrics.csv` contains each method's included count, TP, FP, FN, TN, agreement percentage, inclusion precision and inclusion recall. The reference is the source-reviewed screening itself, so the proposed method's perfect agreement is by construction. This is a retrospective descriptive ablation, not independent accuracy validation.

`comparison.json` also contains the seven-retained-candidate sensitivity analysis and exact comparison-input hashes. `error_analysis.csv` records case ID, classification, resource, artifact/source location, observation, evidence, action and resolution status. Existing numerical caveats and unresolved evidence are not coded as newly discovered dataset errors.

Unit: one named dataset/benchmark resource, pending canonical release and overlap checks. Excludes the unresolved evaluation-study candidate. All values are strings in the source JSON and derived inventory. Blank values are invalid. `unknown` and `not verified` are explicit missing-evidence states.

| Field | Meaning and coding |
|---|---|
| resource_id | Stable local identifier; unique, case insensitive. |
| resource | Resource name; duplicate check collapses whitespace and case. |
| anthology_id | Official publication identifier; unique in this pilot. Future many-to-many resource/publication relations require a separate evidence table. |
| year | Publication year, not necessarily first dataset release; integer from 1900 to runtime current year, no later than access year. |
| primary_task | One of the six task labels in the script. Manually assigned from the publication description. Multiple purposes can exist; one label is a simplification. |
| modality | text, speech, or multimodal; manually coded. Speech resources can include transcripts. |
| scale_value | Positive finite decimal; no cross-unit addition. For an upper bound, this is the bound, not an observed count. |
| scale_precision | exact (explicit number), approximate (rounded), reported (publication figure without recount), less_than (strict upper bound). Even exact means publication-reported, not independently recounted. |
| scale_unit | Original unit with scope, including multilingual totals. |
| license_status | CC BY 4.0, CC BY-SA version unspecified, or unknown. Only explicit dataset-related statements in the inspected abstract support a licence label; publisher website footers never do. Unknown means not established from this inspection, not no licence. |
| source_url | Official ACL publication URL matching anthology_id. Applies to extracted size and scope; task and modality are reviewer coding. |
| accessed_on | Actual inspection date, YYYY-MM-DD. The recorded pilot review is 2026-10-20. |
| evidence_level | publication_metadata_checked; does not mean repository, release, corpus contents or permissions independently verified. |
| scope_note | Paraphrased source observation and any language/count caveat. |
| kazakh_only_count | Explicit publication-reported Kazakh subset count or unknown. Bound checked against scale_value. Only KazMMLU has this field populated. |
| dataset_version | not verified in this pilot. Publication year is not a release identifier. |
| provenance | Manual structured extraction method and limits; source JSON is not an HTML snapshot. |

## Planned main-review instrument

Maintain a separate field-evidence table: resource_id, release_id, field_name, extracted_value, evidence_url, source_locator, access_date, status, coder. For each of the eight documentation fields below use `verified`, `reported_unverified`, or `unknown`. Preserve exact source terms where necessary and inspect repository licence files separately.

The eight fields are domain, script/language variety, origin, annotation method, preprocessing description, access constraints, licence terms, and release/version. Completeness = verified fields / 8. A field needs directly inspected evidence to enter the numerator. No pilot completeness values have been fabricated or computed.

Suitability: potential training use requires appropriate modality/content plus checked reuse terms; evaluation relevance requires an identifiable benchmark protocol and split; otherwise conditional/uncertain. These are reviewer interpretations, not automated scores or endorsements. Main-review screening must log actual search queries and all inclusion/exclusion decisions. Pilot screening covers only the eight supplied seed candidates.
