# Gate Negative Tests

**Result:** **PASS** (15/15 defects rejected)

| Injected defect | Exit | Result | Evidence |
|---|---:|:---:|---|
| NEG-01 duplicate source ID | exit 1 | PASS | >>> Validating Global Source Registry... Found 75 registered source IDs; verified 66 content references. SOURCE VALIDATION FAILED:   - Duplicate source ID in registry   - Source UIT-SLIDE-CH01-2024 missing title   - Source UIT-SLIDE-CH01-20 |
| NEG-02 unknown source reference | exit 1 | PASS | >>> Validating Global Source Registry... Found 74 registered source IDs; verified 65 content references. SOURCE VALIDATION FAILED:   - Unknown source ID 'NO-SUCH-SOURCE' in content/theory/ch01-overview.md |
| NEG-03 malformed source hash | exit 1 | PASS | >>> Validating Global Source Registry... Found 74 registered source IDs; verified 66 content references. SOURCE VALIDATION FAILED:   - VERIFIED_LOCAL source UIT-SLIDE-CH01-2024 has invalid sha256 |
| NEG-04 unmapped slide page | exit 1 | PASS | >>> Executing Evidence-Driven Research Gate Verification... Generated <REPO_ROOT>\research\RESEARCH_GATE_QA.md with status: FAIL |
| NEG-05 forbidden workstation path | exit 1 | PASS | >>> Running Public Hygiene & Path Leak Audit... Scanned 164 tracked files.  ============================================================ PUBLIC HYGIENE AUDIT FAILED with 1 leaked paths:   - content/theory/ch01-overview.md:131 [Pattern: '<LO |
| NEG-06 broken wikilink | exit 1 | PASS | >>> Validating Canonical Content & Exam Models... Discovered 17 unique canonical document IDs.  ============================================================ CONTENT VALIDATION FAILED with 1 errors:   - Broken wikilink [[missing-document]] i |
| NEG-07 unsupported OFFICIAL_RUBRIC | exit 1 | PASS | >>> Validating Canonical Content & Exam Models... Discovered 17 unique canonical document IDs.  ============================================================ CONTENT VALIDATION FAILED with 1 errors:   - Unverified 'Barem chính thức' claim in |
| NEG-08 duplicate document ID | exit 1 | PASS | >>> Validating Canonical Content & Exam Models... Discovered 17 unique canonical document IDs.  ============================================================ CONTENT VALIDATION FAILED with 1 errors:   - Duplicate document ID 'theory-ch01-ove |
| NEG-09 malformed exam classification | exit 1 | PASS | >>> Validating Canonical Content & Exam Models... Discovered 17 unique canonical document IDs.  ============================================================ CONTENT VALIDATION FAILED with 1 errors:   - Exam file content/exams/midterm/2023-2 |
| NEG-10 duplicate slide page | exit 1 | PASS | >>> Executing Evidence-Driven Research Gate Verification... Generated <REPO_ROOT>\research\RESEARCH_GATE_QA.md with status: FAIL |
| NEG-11 missing slide page | exit 1 | PASS | >>> Executing Evidence-Driven Research Gate Verification... Generated <REPO_ROOT>\research\RESEARCH_GATE_QA.md with status: FAIL |
| NEG-12 corrupted Q15 calculation (9398 -> 9999) | exit 1 | PASS | >>> Validating Chapter 7 Content, Structure & Numerical Invariants... CHAPTER 7 CONTENT VALIDATION: FAIL with 1 errors:   - [FAIL] Authored unit QBANK-CH07-15 missing required canonical term/result: '9398' |
| NEG-13 corrupted Q18 calculation (75.2% -> 57.2%) | exit 1 | PASS | >>> Validating Chapter 7 Content, Structure & Numerical Invariants... CHAPTER 7 CONTENT VALIDATION: FAIL with 1 errors:   - [FAIL] Authored unit QBANK-CH07-18 missing required canonical term/result: '75.2%' |
| NEG-14 corrupted Q20 calculation (45 entries -> 64 entries) | exit 1 | PASS | >>> Validating Chapter 7 Content, Structure & Numerical Invariants... CHAPTER 7 CONTENT VALIDATION: FAIL with 2 errors:   - [FAIL] Authored unit QBANK-CH07-20 missing required canonical term/result: '45'   - [FAIL] Authored unit QBANK-CH07- |
| NEG-15 missing required subsection in QBank unit | exit 1 | PASS | >>> Validating Chapter 7 Content, Structure & Numerical Invariants... CHAPTER 7 CONTENT VALIDATION: FAIL with 1 errors:   - [FAIL] Unit QBANK-CH07-01 must contain exactly ONE occurrence of '#### 4. Bẫy đề thi & Lưu ý thực chiến (Exam Traps) |

Each mutation is restored in a `finally` block before the next case.
