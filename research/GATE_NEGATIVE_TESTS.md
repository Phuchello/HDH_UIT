# Gate Negative Tests

**Result:** **PASS** (11 requested injected defects are rejected by non-zero validators)

| Injected defect | Validator |
|---|---|
| Duplicate source ID | `validate_sources.py` |
| Unknown source reference | `validate_sources.py` |
| Malformed source hash | `validate_sources.py` |
| Unmapped slide page | `verify_research_gates.py` |
| Forbidden workstation path | `check_public_hygiene.py` |
| Broken internal wikilink | `validate_v2_content.py` |
| Unsupported OFFICIAL_RUBRIC | `validate_v2_content.py` |
| Duplicate document ID | `validate_v2_content.py` |
| Malformed exam classification | `validate_v2_content.py` |
| Duplicate slide/page coverage | `verify_research_gates.py` |
| Missing slide/page coverage | `verify_research_gates.py` |

`scripts/run_negative_tests.py` injects one defect at a time and restores each mutation in a `finally` block before continuing.
