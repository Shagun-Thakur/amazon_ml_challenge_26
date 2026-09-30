# Match Intelligence Analysis (`docs/analysis/match_intelligence`)

Detailed qualitative and quantitative investigation of genuine entity matches between Source 1 and Source 2/3.

---

## 1. Focus Topics
- **Business Name Variations:** Legal entity suffix variations (`Inc.`, `LLC`, `Private Limited`, `SARL`), acronym expansions, DBAs (Doing Business As), and transliteration differences.
- **Address Noise Patterns:** Landmark descriptions, street vs postal delivery variations, missing PIN codes, abbreviation norms (`Rd` vs `Road`, `Ste` vs `Suite`).
- **Hard Negative Distractors:** Unrelated entities sharing business complexes, shopping malls, franchise chains in different cities, or similar personal names.

---

## 2. Related Empirical Studies
- Coverage analysis: [`reports/matching/deterministic_coverage/deterministic_match_coverage.md`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/matching/deterministic_coverage/deterministic_match_coverage.md)
- Distractor risk analysis: [`reports/matching/deterministic_risk/deterministic_candidate_risk.md`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/matching/deterministic_risk/deterministic_candidate_risk.md)
- Distractor metadata: [`reports/matching/hard_negative_summary.json`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/matching/hard_negative_summary.json)
