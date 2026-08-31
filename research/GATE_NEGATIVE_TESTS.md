# Gate Negative Tests

**Result:** **PASS** (11/11 defects rejected)

| Injected defect | Exit | Result | Evidence |
|---|---:|:---:|---|
| NEG-01 duplicate source ID | exit 1 | PASS | >>> Validating Global Source Registry... Found 68 registered source IDs; verified 54 content references. SOURCE VALIDATION FAILED:   - Duplicate source ID in registry   - Source UIT-SLIDE-CH01-2024 missing title   - Source UIT-SLIDE-CH01-20 |
| NEG-02 unknown source reference | exit 1 | PASS | >>> Validating Global Source Registry... Found 67 registered source IDs; verified 53 content references. SOURCE VALIDATION FAILED:   - Unknown source ID 'NO-SUCH-SOURCE' in content/theory/ch01-overview.md |
| NEG-03 malformed source hash | exit 1 | PASS | >>> Validating Global Source Registry... Found 67 registered source IDs; verified 54 content references. SOURCE VALIDATION FAILED:   - VERIFIED_LOCAL source UIT-SLIDE-CH01-2024 has invalid sha256 |
| NEG-04 unmapped slide page | exit 1 | PASS | >>> Executing Evidence-Driven Research Gate Verification... Generated <REPO_ROOT>\research\RESEARCH_GATE_QA.md with status: FAIL |
| NEG-05 forbidden workstation path | exit 1 | PASS | >>> Running Public Hygiene & Path Leak Audit... Scanned 129 tracked files.  ============================================================ PUBLIC HYGIENE AUDIT FAILED with 1 leaked paths:   - content/theory/ch01-overview.md:131 [Pattern: '<LO |
| NEG-06 broken wikilink | exit 1 | PASS | >>> Validating Canonical Content & Exam Models... Discovered 15 unique canonical document IDs.  ============================================================ CONTENT VALIDATION FAILED with 1 errors:   - Broken wikilink [[missing-document]] i |
| NEG-07 unsupported OFFICIAL_RUBRIC | exit 1 | PASS | >>> Validating Canonical Content & Exam Models... Discovered 15 unique canonical document IDs.  ============================================================ CONTENT VALIDATION FAILED with 1 errors:   - Unverified 'Barem chÃ­nh thá»©c' claim |
| NEG-08 duplicate document ID | exit 1 | PASS | >>> Validating Canonical Content & Exam Models... Discovered 15 unique canonical document IDs.  ============================================================ CONTENT VALIDATION FAILED with 1 errors:   - Duplicate document ID 'theory-ch01-ove |
| NEG-09 malformed exam classification | exit 1 | PASS | >>> Validating Canonical Content & Exam Models... Discovered 15 unique canonical document IDs.  ============================================================ CONTENT VALIDATION FAILED with 1 errors:   - Exam file content/exams/midterm/2023-2 |
| NEG-10 duplicate slide page | exit 1 | PASS | >>> Executing Evidence-Driven Research Gate Verification... Generated <REPO_ROOT>\research\RESEARCH_GATE_QA.md with status: FAIL |
| NEG-11 missing slide page | exit 1 | PASS | >>> Executing Evidence-Driven Research Gate Verification... Generated <REPO_ROOT>\research\RESEARCH_GATE_QA.md with status: FAIL |

Each mutation is restored in a `finally` block before the next case.
