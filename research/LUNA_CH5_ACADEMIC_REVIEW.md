# LUNA CH5 — INDEPENDENT ACADEMIC REVIEW

**Review date:** 2026-09-01  
**Reviewer scope:** Chapter 5 theory and the 18 structured QBank units only.  
**Review rule:** source fidelity and technical correctness were audited without
restarting authoring or changing the renderer/build architecture.

## REVIEWED REMOTE HEAD

`d62682abab8c2ea5ce1aac879e69ae8f8f0806df` on `v2/complete-theory-labs`.

## SOURCE BINARIES AVAILABLE

The exact canonical binaries are not present in this clean review workspace,
so no new page-image or byte-level wording comparison is claimed here. The
previous verified source-map evidence is retained in the repository, including
the immutable filenames, SHA-256 values, page counts, and XML/question counts.
The local 58-page/55-page slide variants and the 55,931-byte Drive QBank
variant were treated as non-canonical and were not used to rewrite content.

## CANONICAL SOURCE IDENTITY

| Source ID | Canonical identity | SHA-256 | Physical pages / count |
| --- | --- | --- | --- |
| `UIT-SLIDE-CH05-1-2024` | `#Week06-Chapter5-1 2024.pdf` | `2ef4be67449ea22aada6e8bd69b49b781bbcb8c6f0eb601b16e9f18a004c7416` | 67 (63 content + 4 non-content) |
| `UIT-SLIDE-CH05-2-2024` | `#Week07-Chapter5-2 2024.pdf` | `f7e9fc9eb9a35f3a02eb60b2c8e01fa134342d0c5256f47deef4247a0db141d2` | 72 (68 content + 4 non-content) |
| `UIT-QBANK-CH05-2024` | `Bai tap chuong 5 HDH.docx` | `503cd8fdb619bcfd664cfaa198915bc50d0ba6bb910c74d14ccff5252e646186` | 129 XML paragraphs; 128 content paragraphs; 18 verified units |

Registry and coverage keep every local variant under a separate immutable
`source_variant` ID. The source-map report's earlier `+3` typo for exercise 4
was corrected to the canonical `n_b \le n_a \le n_b+10` wording.

## THEORY COVERAGE

The reviewed theory file covers the complete canonical ranges without Chapter
6 intrusion:

- Part 1: race/interleaving and PID allocation (slides 4–16); critical section
  and the three requirements (17–30); turn/flag/Peterson (31–51); memory
  barrier and page-56 self-study primitives (52–56); mutex and blocking
  implementation (57–65).
- Part 2: semaphore definition, types, implementation and uses (4–32);
  monitor/condition variables (33–40); liveness including Deadlock,
  Starvation, Priority Inversion and Priority Inheritance (41–43);
  bounded-buffer (44–53); first readers-writers (54–60); dining philosophers
  and avoidance strategies (61–70).

## QBANK COVERAGE

All 18 structured units are present with the required schema and canonical
XML locators. Units 1–9 now follow the nine source records in XML 3–11:
race condition, critical section, solution classification, solution features,
busy-waiting trade-offs, semaphore, monitor/critical region, and classic
synchronization problems. Units 10–18 cover the nine exercises in XML 12–129:
Dekker, the Peterson variant, Swap, the A/B inequality, the fork/join graph,
the shared-X race, two-process rendezvous, the 100-step barrier, and the
expression DAG.

The QBank distinguishes source question occurrences from the canonical count:
the 129 XML paragraphs include 128 content paragraphs, while the 18 complete
question/exercise units are the deduplicated study units. No local Drive
variant is counted as an additional official question.

## SOURCE LOCATOR AUDIT

Every theory section cites either `UIT-SLIDE-CH05-1-2024` or
`UIT-SLIDE-CH05-2-2024` with the canonical page range. Every QBank unit cites
`UIT-QBANK-CH05-2024` and XML 3–129. No legacy Part-2 source ID or unregistered
Chapter-5 Part-3 identity is used in the authored files or generated output.

## TIER-A FIDELITY

The canonical slide claims are preserved: the producer/consumer and PID race
traces, the three critical-section requirements, the turn/flag/Peterson
comparisons, disable-interrupt limitations, semaphore source model, monitor
wait/signal behavior, liveness vocabulary, and the three classical problems.
Page 56 remains explicitly `source_depth: SELF_STUDY`; it is not presented as a
new official slide section. The QBank prompts and exercise statements remain
source-located rather than being replaced by invented exam claims.

## TIER-B TECHNICAL ACCURACY

The review checked the standards-facing enrichment against C/C++ memory-model
and synchronization semantics. Generic `memory_barrier()` wording is now
qualified: portable implementations require atomics or lock primitives with a
specified ordering; a fence alone is not a universal correctness proof.
The semaphore negative-value description is explicitly the UIT slide's
internal model, while POSIX behavior remains a separate Tier-B note. Monitor
signaling is intentionally neutral about Hoare versus Mesa scheduling.

## EXERCISE RE-DERIVATION

- **Dekker and Peterson variant:** the mutual-exclusion/progress/bounded-waiting
  arguments and the `turn = i` counterexample were replayed under sequential
  consistency.
- **Swap:** atomic swap yields one owner when `lock` is false; contenders keep
  their local key true until a later swap succeeds.
- **A/B inequality:** with `sem_a=10`, `sem_b=0`, each A step consumes one
  lead token and creates one B token; each B step returns one A token. Hence
  `0 \le n_a-n_b \le 10`; separate mutexes are required for multiple producers
  or consumers updating the counters.
- **Fork/join and barriers:** signal/wait multiplicities were checked against
  the graph and the two-phase rendezvous invariants.
- **Shared X:** the 19→20→21 interleaving demonstrates why the increment and
  equality test must share one critical section.
- **Expression DAG:** the original draft's thread 2 self-wait and thread 3
  self-signal could expose `y` before it was ready and did not establish the
  required joins. The answer now uses one semaphore per cross-thread
  dependency (including separate consumers for `w` and `y`) and computes
  `ans` only after both `y` and the final `z` are signaled.

## CHAPTER-6 BOUNDARY

Chapter 5 uses Deadlock only as a liveness/synchronization failure mode. It
does not teach Chapter 6's Coffman conditions, resource-allocation graphs,
Banker's algorithm, detection, or recovery. The related link to Chapter 6 is
navigation only.

## PEDAGOGICAL QUALITY

The chapter retains a coherent progression from race traces to correctness
criteria, algorithms, primitives, liveness, and classical problems. Each QBank
unit has minimum-answer requirements, key points, common omissions/wrong
claims, and a self-check rubric. Tier-B additions are visibly labeled, and
worked traces/invariants are kept where they prevent a common exam error.

## FINDINGS

Findings are recorded open first and then resolved by the surgical patches in
this review; no broad rewrite was performed.

### ACAD-CH5-001 — MAJOR — RESOLVED

- **File/section:** `content/questions/subjective/ch05.md`, units 4–6.
- **Claim:** The draft labeled XML 6–8 as disable-interrupts, hardware
  primitives, and mutex questions.
- **Source evidence:** canonical extracted QBank records XML 6–8 are the
  solution-classification, solution-features, and busy-waiting prompts.
- **Technical analysis:** the displaced topics are valid Tier-B/slide topics,
  but the locator-to-prompt mapping was not source-faithful.
- **Required fix:** restore the three source prompts and retain the useful
  disable-interrupt/mutex examples inside their answers.
- **Status:** resolved; units 4–6 now match XML 6–8.

### ACAD-CH5-002 — MAJOR — RESOLVED

- **File/section:** theory §1.1, §3.4, §4.1; QBank units 1 and 5.
- **Claim:** `count++` was described as exactly three hardware operations and a
  generic memory barrier as a complete compiler/CPU guarantee.
- **Technical analysis:** compiler/ISA lowering is implementation-dependent;
  ordinary C/C++ shared flags can be a data race, and a fence alone is not a
  portable lock algorithm.
- **Required fix:** keep the teaching trace but qualify the model and direct
  portable implementations to atomics/lock primitives with ordering.
- **Status:** resolved.

### ACAD-CH5-003 — MAJOR — RESOLVED

- **File/section:** QBank unit 18 (expression DAG).
- **Claim:** the draft used a self-wait/self-signal pattern and could compute
  `ans` without a happens-before edge from `y`.
- **Technical analysis:** the proposed schedule was not a valid semaphore
  realization of the stated DAG.
- **Required fix:** re-derive the dependency graph and provide explicit
  producer-to-consumer semaphores.
- **Status:** resolved; the corrected three-thread schedule has no self-wait
  and joins both operands before `ans`.

### ACAD-CH5-004 — MINOR — RESOLVED

- **File/section:** theory §7.2 and QBank unit 8.
- **Claim:** condition signaling was presented without naming the scheduling
  model.
- **Technical analysis:** Hoare and Mesa monitors differ in when a signaled
  thread runs; the slide does not select one.
- **Required fix:** state the model-neutral rule and require predicate
  re-checking in a concrete runtime.
- **Status:** resolved with a Tier-B note.

### ACAD-CH5-005 — MINOR — RESOLVED

- **File/section:** `research/LUNA_CH5_SOURCE_MAP_REPORT.md`, exercise 4.
- **Claim:** the report said `n_b < n_a \le n_b+3`.
- **Source evidence:** canonical QBank wording is `n_b \le n_a \le n_b+10`.
- **Required fix:** correct the report's stale arithmetic summary.
- **Status:** resolved.

### ACAD-CH5-006 — MINOR — OPEN (EVIDENCE LIMITATION)

- **File/section:** review evidence chain.
- **Claim:** the exact canonical binaries could be freshly re-opened during
  this review.
- **Technical analysis:** only the registry/hash/page-map evidence is present
  in the clean workspace; local variants are intentionally different files.
- **Required fix:** none to authored content. Re-run byte/page verification when
  the user re-attaches the exact binaries.
- **Status:** open evidence limitation; it does not block the content gate.

## REVIEW DECISION

No unresolved Chapter 5 content BLOCKER or MAJOR remains. The single open item
is the explicitly documented inability to re-open the exact canonical binaries
in this workspace; provenance and page-map evidence remain locked. Chapter 5
may be marked `CONTENT_VERIFIED` only after the required deterministic
validation suite passes.

## VALIDATION RESULTS

The final post-review run passed:

- `validate_ch05_source_map.py`
- `validate_ch05_content.py` (18/18 QBank schemas and 131 canonical content
  destinations)
- `validate_batch1_canonical.py`
- `check_batch1_numeric.py`
- `stress_test_web_renderer.py`
- `npm test` / foundation gate
- `npm run web:build`

The generated Chapter 5 theory and QBank HTML were rebuilt from the corrected
Markdown. No Chapter 6 source or authoring work was started.
