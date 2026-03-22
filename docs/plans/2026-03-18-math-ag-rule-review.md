---
doc_type: "domain_review"
scope: "math > math.AG"
status: "active"
owner: "trend-monitor"
source_of_truth: true
upstream_docs:
  - "docs/plans/2026-03-10-evolution-rule-coverage.md"
  - "docs/plans/2026-03-18-math-ag-benchmark.md"
downstream_docs: []
last_reviewed: "2026-03-22"
---

# Math.AG Rule Review

## Rule: math_ag_object_continuity

### Summary

| Field | Value |
|-------|-------|
| rule_name | `math_ag_object_continuity` |
| tree_path | `math > math.AG` |
| status | `partial` |
| trigger | ≥2 shared exact AG object terms; taxonomy overlap is diagnostic only |
| implemented_in | `pipeline/evolution_analysis.py` |

### Object Taxonomy

| Class | Terms |
|-------|-------|
| variety_family | curves, k3, surfaces, threefolds, toric, varieties |
| moduli_and_stack | moduli, spaces, stacks, stack |
| sheaf_and_bundle | sheaf, sheaves, bundles |
| scheme_level | algebraic, scheme, projective |

### Known Issues

#### 1. Taxonomy-Backed False Positives

**Problem**: The pre-MAG-02 gate let `object_overlap["score"] >= 1.5` independently promote `math_ag_object_continuity`. That created two different false-positive modes:

- `ag-n2`: score `2.25` via class overlap with **0 exact shared terms**
- `ag-n1`: score `1.75` with only **1 exact shared term** (`sheaves`)

**Evidence**: MAG-02 replay showed both pairs as false positives before the gate tightening. Post-fix replay now keeps `ag-n1` / `ag-n2` at `none`, while `ag-p2` and `ag-p3` still remain `none`.

**Current implementation**: Promote object continuity only when `len(shared_math_ag_objects) >= 2`. Keep taxonomy overlap output as diagnostic evidence, but do not let score alone upgrade the relation.

#### 2. Generic Vocabulary Blind Spots

| Term | Problem |
|------|---------|
| varieties | Too generic — shimura/abelian/Fano/toric varieties all share this word across different AG subdisciplines |
| hodge | Ambiguous: AG object (Hodge structure) OR method (Hodge theory); current classification may be inconsistent |
| motivic | Same ambiguity: motivic cohomology (method) vs motivic motive (object) |
| adic | Typically a method qualifier (p-adic, adic spaces), not a primary AG object |

#### 3. Categorical Vocabulary Boundary

**Problem**: Terms like "categories", "derived", "homotopy" span both pure category theory and derived algebraic geometry. Current object taxonomy does not distinguish these.

**Example**: ag-amb1 (global_4 → global_287) — "categories" shared but objects are fundamentally different (representation-theoretic vs. geometric stacks).

### Benchmark Status

Reference: `docs/plans/2026-03-18-math-ag-benchmark.md`

| Category | Count | Notes |
|----------|-------|-------|
| Positive | 3 | ag-p1 is the only runner-positive; ag-p2/p3 are bridge-level semantic positives |
| Negative | 3 | cover 3 distinct failure modes |
| Ambiguous | 1 | ag-amb1: categorical vocabulary boundary |

**Assessment**: First real benchmark batch complete (PKG-AG-01). MAG-02 confirms the smallest safe fix: `>=2` exact shared AG object terms. Current stable partial baseline is: one runner-positive event-level case (`ag-p1`), three fixed negatives (`ag-n1/ag-n2/ag-n3`), and two semantic bridge-level positives (`ag-p2/ag-p3`) that are explicitly not runner promotions. MAG-04 cleans the runner-facing contract so the active benchmark runner now exposes only `ag-p1` on the positive side and no longer carries legacy aliases `ag-b1/ag-e2`.

### Graph-Ready Interpretation

- `ag-p1` should be narrated as the `confirmed core`: it is the only event-level pair that both the rule and the runner currently promote.
- `ag-p2` / `ag-p3` should be narrated as the `bridge ring`: they thicken the AG neighborhood semantically, but they remain intentionally below the exact-term promotion threshold.
- `ag-n1` / `ag-n2` / `ag-n3` should be narrated as the `excluded boundary`: they explain where single-term or taxonomy-only overlap must stop.
- The point of this package is therefore not “more AG positives”, but a cleaner three-band reading that downstream graph/export layers can reuse without weakening the guard.

### Next Steps

1. Keep `math_ag_object_continuity` at `>=2` exact shared AG object terms in `pipeline/evolution_analysis.py`.
2. Keep verifying the active runner contract stays `ag-p1` + `ag-n1/ag-n2/ag-n3`, `ag-p1` stays positive, and `ag-p2` / `ag-p3` remain non-runner bridge-level cases.
3. Keep the curated graph/export split aligned to `confirmed core` / `bridge ring` / `excluded boundary`; do not let implementation or docs drift into a flat positive-vs-negative story.
4. Do not frame `ag-p2/ag-p3` as pending runner promotions; revisit them only if a separate bridge-level benchmark contract is introduced.
5. Resolve ag-amb1 by clarifying whether categorical vocabulary is AG-object-level.

## Change Log

- `2026-03-21`: 初版建立 (PKG-AG-01 产出)
- `2026-03-22`: MAG-02 — exact-term guard tightened to `>=2` exact shared AG object terms; taxonomy overlap downgraded to diagnostic-only
- `2026-03-22`: MAG-03 — partial baseline stabilized: ag-p1 only runner-positive; ag-p2/ag-p3 fixed as bridge-level semantic positives
- `2026-03-22`: MAG-04 — runner contract canonicalized to `ag-p1` + `ag-n1/ag-n2/ag-n3`; legacy positive aliases `ag-b1/ag-e2` removed
- `2026-03-22`: MAG-FILL-01 — graph-ready interpretation fixed as `confirmed core` / `bridge ring` / `excluded boundary`; no gate relaxation
