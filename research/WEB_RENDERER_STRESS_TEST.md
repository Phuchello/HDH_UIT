# Web Renderer Stress Test

**Result:** **PASS**

`scripts/stress_test_web_renderer.py` builds temporary canonical fixtures containing nested lists, tables with inline-code pipes, multiple fenced code blocks, Vietnamese headings, inline/block LaTeX, wikilink aliases, callouts, StudyCard, and cross-page links. It parses every generated HTML fixture with the standard-library HTML parser and deletes the temporary fixture tree afterward.

The test is deterministic and does not modify `content/`.
