# Input provenance

`source_observations.json` is copied byte for byte from the uploaded RMT ZIP. Its historical inspection dates and claims are inherited metadata, not independently authenticated historical actions. The current AI-assisted recheck was performed on 2 November 2026 and is separately logged in `source_recheck.csv` and `screening_evidence.csv`.

`seed_candidates.csv` reconstructs only candidate identity, task, publication year and source link for the eight named candidates listed in the original DOCX. Seven rows use the corresponding identifiers and links from the ZIP; the unresolved study row uses its cited publication. This is not a recovered original eight-row CSV or an execution of an unavailable old script. No original size or licence values were invented. Baseline 1 is the implemented inventory-retention rule, and Baseline 2 is the implemented minimal structural validator.

The reference decisions are eight current source-reviewed inclusion labels. The proposed method consumes those same labels. Therefore its agreement with this reference is tautological and describes the correction process only. No independent gold standard or held-out benchmark exists.

Public source observations are paraphrases, not archived full pages. Each row includes a URL, locator and date. Exact source bytes are not preserved, so source change cannot be ruled out. The supplied original DOCX and ZIP are retained in `provenance/` for comparison.
