---
doc_type: "implementation_report"
scope: "math.PR conditional graph integration — Phase 2C implementation"
status: "COMPLETE — Gate 1 conditions met (PR-2C-impl-fix applied 2026-03-21)"
owner: "rule-worker"
package_id: "PR-2C-impl"
date: "2026-03-23"
fix_package: "PR-2C-impl-fix"
fix_date: "2026-03-21"
upstream_docs:
  - "docs/plans/2026-03-22-math-pr-phase-2c-integration-plan.md"
  - "docs/plans/2026-03-21-math-pr-case-curation.md"
  - "docs/plans/2026-03-20-math-pr-candidate-extraction.md"
downstream_docs: []
last_reviewed: "2026-03-23"
---

# math.PR Phase 2C — Implementation Report

**Date:** 2026-03-23
**Package:** PR-2C-impl
**Status:** COMPLETE — Gate 1 conditions met
**Branch:** codex/topic-evolution-analysis

---

## 1. Executive Summary

PR-2C-impl is complete. A conditional, isolated, opt-in graph integration layer for math.PR has been implemented across four layers: backend export, visualization bundle, frontend hook, and test coverage. The LO+AG production baseline (`data/output/kg_v1/`) remains completely unmodified. math.PR is now accessible under a separate conditional output path (`data/output/kg_v1_pr_conditional/`) and an opt-in frontend route (`/knowledge-graph?pr_preview=1`).

This implementation completes the Gate 0 → Gate 1 transition for math.PR. Gate 2 (baseline inclusion) remains blocked pending paper-level review (Track B).

---

## 2. Implementation Scope

### What was implemented

| Layer | Change | File |
|-------|--------|------|
| Backend: Export | `parse_pr_cases()` — parses PR curation doc for graph-visible positive cases | `pipeline/math_kg_export.py` |
| Backend: Export | `--benchmark-pr` CLI flag — enables conditional PR export path | `pipeline/math_kg_export.py` |
| Backend: Export | Parameterized `target_subcategories` — `{'LO', 'AG', 'PR'}` when conditional | `pipeline/math_kg_export.py` |
| Backend: Export | `build_topic_nodes()` — adds PR topic ID lookup from hierarchy | `pipeline/math_kg_export.py` |
| Backend: Export | `build_subcategory_nodes()` — adds PR → 'Probability Theory' | `pipeline/math_kg_export.py` |
| Backend: Export | `build_evolves_to_edges()` — adds conditional metadata fields for PR edges | `pipeline/math_kg_export.py` |
| Backend: Export | `validate_output()` — conditional mode allows PR, uses `evolves_to >= 9` check | `pipeline/math_kg_export.py` |
| Backend: Export | `export_kg_v1()` wrapper — adds optional `benchmark_pr` param | `pipeline/math_kg_export.py` |
| Backend: Export | `parse_pr_docs()` — convenience wrapper for test imports | `pipeline/math_kg_export.py` |
| Backend: Viz | `build_legend()` — adds `provisional` evidence_type and `integration_scopes` | `pipeline/math_kg_visualization_export.py` |
| Backend: Viz | `main()` — detects PR topics, conditionally generates `subgraph_pr.json` | `pipeline/math_kg_visualization_export.py` |
| Frontend: Hook | `useKnowledgeGraph` — adds `sourceMode` param, math.PR label, inferred confidence | `frontend/src/hooks/useKnowledgeGraph.js` |
| Frontend: Filters | `GraphFilters` — adds hidden PR conditional preset (opt-in via `enablePRPreset`) | `frontend/src/components/GraphFilters.jsx` |
| Frontend: View | `KnowledgeGraph` — checks `?pr_preview=1`, activates sourceMode + preset | `frontend/src/views/KnowledgeGraph.jsx` |
| Frontend: Detail | `TopicDetail` — adds `inferred` confidence label, `human_review_required` badge, PR color | `frontend/src/components/TopicDetail.jsx` |
| Tests | `TestConditionalPRExport` — 13 tests covering conditional export path | `tests/test_math_kg_export.py` |
| Tests | `TestConditionalPRVisualizationBundle` — 6 tests covering PR bundle and legend | `tests/test_math_kg_visualization_export.py` |
| Tests | `TestConditionalVisualizationEntrypoint` — 5 tests covering `main()` entrypoint disk-write path (PR-2C-impl-fix) | `tests/test_math_kg_visualization_export.py` |
| Docs | This document | `docs/plans/2026-03-23-math-pr-phase-2c-implementation.md` |
| Docs | PR-2C-impl package entry | `docs/plans/evolution-ops/03-task-packages.md` |

### PR-2C-impl-fix corrections (2026-03-21)

Three consistency/hygiene issues were corrected after initial implementation:

| Issue | Fix | File |
|-------|-----|------|
| Timeline source hardcoded to baseline path in PR preview | `useEffect` now reads `kg_v1_pr_conditional_visualization/timeline_summary.json` when `prPreviewEnabled=true` | `frontend/src/views/KnowledgeGraph.jsx` |
| Viz exporter tests only covered helper functions, not `main()` entrypoint | Added `TestConditionalVisualizationEntrypoint` (5 tests) calling `main()` via `sys.argv` patch | `tests/test_math_kg_visualization_export.py` |
| `kg_v1_pr_conditional/` and `kg_v1_pr_conditional_visualization/` untracked in git | Added both to `.gitignore` as generated artifacts (same policy as `kg_v1/`, `kg_v1_visualization/`) | `.gitignore` |

After fix: 67 visualization export tests pass, 4 frontend tests pass, frontend build clean.

### What was NOT implemented

- `data/output/kg_v1/` was not touched in any way
- `data/output/kg_v1_visualization/graph_bundle.json` does not contain PR
- math.PR does not appear on the default `/knowledge-graph` page
- No Gate 2 conditions were implemented (PR benchmark runner, baseline integration)
- No changes to `pipeline/evolution_analysis.py`, `Makefile`, or benchmark docs

---

## 3. Baseline Isolation Guarantee

Three isolation mechanisms ensure the LO+AG baseline cannot be contaminated:

### 3.1 Separate output directories

```
Baseline (unchanged):
  data/output/kg_v1/
  data/output/kg_v1_visualization/

PR conditional (new, separate):
  data/output/kg_v1_pr_conditional/
  data/output/kg_v1_pr_conditional_visualization/
```

These directories share no write paths. The exporter never writes to `kg_v1/` when `--benchmark-pr` is active.

### 3.2 Explicit inclusion gate

`target_subcategories` defaults to `{'LO', 'AG'}`. PR is only included when `--benchmark-pr` is explicitly provided. The flag's absence is equivalent to the current production baseline.

### 3.3 Validation gate

`validate_output()` with `is_conditional=False` (default) explicitly flags any PR topic found in output as a schema error:

```python
if node.get('subcategory') == 'PR':
    schema_errors.append(f"PR topic found in output: {node.get('id')}")
```

This check runs every time baseline export is called and will fail validation if PR is accidentally included.

---

## 4. Conditional Export Output

### Output directory: `data/output/kg_v1_pr_conditional/`

Generated by:
```bash
python3 pipeline/math_kg_export.py \
  --input data/output/aligned_topics_hierarchy.json \
  --benchmark-lo docs/plans/2026-03-12-math-lo-benchmark.md \
  --benchmark-ag docs/plans/2026-03-18-math-ag-benchmark.md \
  --benchmark-pr docs/plans/2026-03-21-math-pr-case-curation.md \
  --output-dir data/output/kg_v1_pr_conditional
```

### Contents

Same directory structure as `kg_v1/`:
```
nodes/
  topics.jsonl      — LO + AG + PR topics
  subcategories.jsonl — math.LO, math.AG, math.PR
  periods.jsonl
edges/
  evolves_to.jsonl  — 9 LO+AG baseline edges + N PR conditional edges
  contains_topic.jsonl
  active_in.jsonl
  neighbor_of.jsonl
  parent_of.jsonl
metadata.json       — version: "kg_v1_pr_conditional", scope includes math.PR
validation_report.json
```

### PR cases in graph-visible layer

Only curated positive cases enter the conditional graph-visible layer:

| Case ID | Source | Target | Tier | Rule |
|---------|--------|--------|------|------|
| PR-P1 | global_38 | global_100 | A | math_pr_object_continuity |
| PR-P2 | global_38 | global_156 | A | math_pr_object_continuity |
| PR-P3 | global_38 | global_99  | B | math_pr_object_continuity |
| PR-P4 | global_65 | global_188 | B | math_pr_method_continuity |

**Negative and ambiguous cases (PR-N1..N5, PR-A1..A2): NOT included in graph edges.** They are documented in the curation doc as calibration anchors only.

### PR edge metadata

Each PR conditional EVOLVES_TO edge carries:

```json
{
  "evidence_type": "provisional",
  "confidence": "inferred",
  "integration_scope": "conditional",
  "curation_tier": "A",
  "curation_status": "positive",
  "human_review_required": true,
  "graph_integration_candidate": "gate1_eligible",
  "continuity_type": "object"
}
```

These fields are ADDITIVE. LO/AG baseline edges carry none of them.

---

## 5. Conditional Bundle Output

### Output directory: `data/output/kg_v1_pr_conditional_visualization/`

Generated by:
```bash
python3 pipeline/math_kg_visualization_export.py \
  --input-dir data/output/kg_v1_pr_conditional \
  --output-dir data/output/kg_v1_pr_conditional_visualization
```

### Contents

```
graph_bundle.json         — LO + AG + PR topics, all edges
subgraph_lo.json          — LO subgraph (unchanged from baseline)
subgraph_ag.json          — AG subgraph (unchanged from baseline)
subgraph_pr.json          — PR conditional subgraph (new)
timeline_summary.json
legend.json               — now includes "provisional" evidence_type
```

### legend.json additions

```json
{
  "evidence_types": {
    "provisional": {
      "description": "Curated inferred relation (conditional, requires paper review)",
      "badge": "⚑",
      "color": "#a855f7"
    }
  },
  "integration_scopes": {
    "baseline": {
      "description": "Included in production baseline (LO+AG benchmark-verified)",
      "color": "#22c55e"
    },
    "conditional": {
      "description": "Conditional layer only (math.PR curated, not baseline-included)",
      "color": "#a855f7"
    }
  }
}
```

---

## 6. Frontend Opt-In Behavior

### Activation mechanism: URL query parameter

The opt-in mechanism is a URL query parameter:

```
Default (baseline only):  /knowledge-graph
PR conditional (opt-in):  /knowledge-graph?pr_preview=1
```

Regular users see only the LO+AG baseline. The `?pr_preview=1` parameter is not exposed in any UI element — it must be entered manually in the URL bar.

### Implementation

`KnowledgeGraph.jsx` detects the query param:
```javascript
const urlParams = new URLSearchParams(window.location.search);
const prPreviewEnabled = urlParams.get('pr_preview') === '1';
```

When `prPreviewEnabled`:
1. `useKnowledgeGraph({ sourceMode: 'pr_conditional' })` loads from `kg_v1_pr_conditional_visualization/graph_bundle.json`
2. `GraphFilters` receives `enablePRPreset={true}` → shows hidden "PR 条件层 (实验性 · 需人工审核)" preset button
3. Header badge shows "LO + AG + PR (条件层)" instead of "LO + AG · v1"

When NOT `prPreviewEnabled` (default):
1. `useKnowledgeGraph({ sourceMode: 'baseline' })` loads from `kg_v1_visualization/graph_bundle.json`
2. No PR preset shown in filters
3. No PR topics rendered
4. Header shows "LO + AG · v1"

### Supporting changes

- `TopicDetail.jsx`: Added `inferred` confidence label (purple) and `⚑ 待人工审核` badge for edges with `human_review_required: true`
- `useKnowledgeGraph.js`: Added `'math.PR': 'Probability Theory'` to `SUBCATEGORY_LABELS` and `inferred` to `CONFIDENCE_CONFIG`

---

## 7. Gate 2 Blocker Record (Historical — Gate 2 COLLAPSED post-TrackB-06)

The following were required for Gate 2 (baseline inclusion) and were NOT implemented by PR-2C-impl. **Post-TrackB-06 (2026-03-29): Gate 2 is COLLAPSED — all candidates demoted, no open blockers remain.**

| Blocker | Type | Final Status |
|---------|------|-------------|
| Paper-level review of global_38 (≥5 papers, 2025-02/03) | Human (Track B) | RESOLVED (negative, PR-TrackB-06 2026-03-29) — DEMOTED FINAL; category mismatch, founding-date impossible, citation absent |
| Paper-level review of global_65 and global_188 for directional evidence | Human (Track B) | RESOLVED (negative, PR-TrackB-03 2026-03-26) — P4 demoted; calibration anchor only |
| Math.PR classification verification for global_65 and global_188 vs math.AP | Human (Track B) | RESOLVED — both PR-dominant (PR-TrackB-01 2026-03-24) |
| PR benchmark runner (MPR-03) | Code | DORMANT — Gate 2 COLLAPSED; future contingency only if new directional evidence reopens path |
| R1 resolution (global_38 transience) | Research | RESOLVED (negative, PR-TrackB-06 2026-03-29) |
| R2 resolution (P4 adjacency-only fragility) | Research | RESOLVED (negative, PR-TrackB-03 2026-03-26) |
| R3 resolution (PR/AP boundary) | Research | RESOLVED (PR-TrackB-01 2026-03-24) |

**Post-collapse status (2026-03-29):** Gate 2 is COLLAPSED. All blockers are either resolved or dormant. math.PR remains at long-term Gate 1. Baseline inclusion (`data/output/kg_v1/`) requires new directional evidence — no current path is open.

---

## 8. Validation Results

All required commands from PR-2C-impl spec:

```bash
# Baseline export (unchanged behavior)
python3 pipeline/math_kg_export.py \
  --input data/output/aligned_topics_hierarchy.json \
  --benchmark-lo docs/plans/2026-03-12-math-lo-benchmark.md \
  --benchmark-ag docs/plans/2026-03-18-math-ag-benchmark.md \
  --output-dir data/output/kg_v1
# Expected: 32 topics, 9 EVOLVES_TO edges, no PR

# Conditional PR export
python3 pipeline/math_kg_export.py \
  --input data/output/aligned_topics_hierarchy.json \
  --benchmark-lo docs/plans/2026-03-12-math-lo-benchmark.md \
  --benchmark-ag docs/plans/2026-03-18-math-ag-benchmark.md \
  --benchmark-pr docs/plans/2026-03-21-math-pr-case-curation.md \
  --output-dir data/output/kg_v1_pr_conditional
# Expected: 32 + N PR topics, 9 + M PR edges

# Baseline visualization (unchanged)
python3 pipeline/math_kg_visualization_export.py \
  --input-dir data/output/kg_v1 \
  --output-dir data/output/kg_v1_visualization
# Expected: graph_bundle.json, subgraph_lo.json, subgraph_ag.json

# Conditional visualization
python3 pipeline/math_kg_visualization_export.py \
  --input-dir data/output/kg_v1_pr_conditional \
  --output-dir data/output/kg_v1_pr_conditional_visualization
# Expected: above + subgraph_pr.json

# Tests
pytest tests/test_math_kg_export.py -q
pytest tests/test_math_kg_visualization_export.py -q
npm --prefix frontend run test
npm --prefix frontend run build
```

---

## 9. Residual Risk

Track B review (PR-TrackB-01) has updated the status of all three risks. No new risks were introduced by this implementation.

| Risk | Status | Impact if unresolved |
|------|--------|----------------------|
| R1: global_38 transience | RESOLVED (negative, PR-TrackB-06 2026-03-29) — global_38 does not evolve into RMT/concentration cluster; category mismatch confirmed at abstract level; Gate 2 COLLAPSED | Risk closed. No active Gate 2 candidates depend on global_38. |
| R2: P4 adjacency-only fragility | RESOLVED (negative) — PR-TrackB-03 (2026-03-26): cluster-level directionality absent; P4 demoted from Gate 2 directional set; retained as calibration anchor | Risk closed. P4 remains calibration-only; Gate 2 later collapsed after PR-TrackB-06 demoted the remaining candidates. |
| R3: PR/AP boundary for global_65 and global_188 | RESOLVED — both PR-dominant; dual-class caveat for global_188 | Not blocking |

The conditional layer deliberately carries `human_review_required: true` on all PR edges to surface these risks to any frontend consumer.

---

## 10. Recommendation

**PR-TrackB-06 COMPLETE (2026-03-29): DEMOTED. Gate 2 COLLAPSED.**

Track B review status as of 2026-03-29 (FINAL):
- R1 (global_38 transience / global_38-family viability): RESOLVED (negative, PR-TrackB-06 2026-03-29) — global_38 does not evolve into RMT/concentration cluster; category mismatch confirmed at abstract level; all Gate 2 candidates demoted.
- R2 (P4 directionality): RESOLVED (negative, PR-TrackB-03 2026-03-26) — P4 demoted; calibration anchor only.
- R3 (PR/AP boundary): RESOLVED (PR-TrackB-01 2026-03-24) — both topics PR-dominant.

**Post-collapse status:** No active Gate 2 blockers. Gate 2 is COLLAPSED — all 4 candidates demoted across PR-TrackB-03 through PR-TrackB-06. The conditional integration layer implemented by PR-2C-impl remains in place as a Gate 1 artifact (`data/output/kg_v1_pr_conditional/`, `?pr_preview=1`). No engineering work is required or expected until new directional evidence reopens the Gate 2 path.

**Future contingency (not a current blocker):** If new directional evidence emerges from the global_38→global_198 line (Jaccard ~0.4+, genuine content heir identified in PR-TrackB-06), a new TrackB review series (TrackB-07+) may be initiated. Only then would MPR-03 (PR benchmark runner) become a relevant next engineering step. MPR-03 is not a current blocker because there are no Gate 2 candidates to benchmark.

---

**Updated by PR-TrackB-04 (2026-03-27):** P3 demoted. P1 (global_38→global_100) and P2 (global_38→global_156) provisionally retained at title-level resolution — neither confirmed nor demoted at abstract+citation level. Gate 2 path PARTIALLY VIABLE. Next step: Level 3 abstract+citation review of P1/P2 (PR-TrackB-05).

**Updated by PR-TrackB-05 (2026-03-28):** global_100 and global_156 confirmed not reliably distinct (5/5 identical representative papers). P1 (global_38→global_100) and P2 (global_38→global_156) collapse to single candidate pointing to merged RMT/concentration cluster. P1/P2 CONDITIONALLY DEMOTED. Gate 2 path reduced to single-candidate heightened concern. Next step: PR-TrackB-06 (abstract+citation review of merged candidate; founding-date and category mismatch testing; citation linkage audit).

**Updated by PR-TrackB-06 (2026-03-29):** All PR-TrackB-05 conditional concerns confirmed at abstract+citation level. global_38 → merged(global_100, global_156) DEMOTED (FINAL). Gate 2 COLLAPSED — all 4 candidates demoted (P4 at TrackB-03, P3 at TrackB-04, P1/P2 at TrackB-05/06). math.PR Track B at long-term Gate 1. R1 RESOLVED (negative at abstract+citation level): global_38 does not evolve into RMT/concentration cluster. R2 remains RESOLVED negative. No further Track B review work needed.

## Answers to Required Questions

1. **Is baseline kg_v1 completely free of PR?** YES. The baseline `data/output/kg_v1/` is not touched by any change in this implementation. `validate_output()` with `is_conditional=False` explicitly rejects PR topics as schema errors.

2. **What files does the PR conditional output directory generate?**
   - `nodes/topics.jsonl`, `nodes/subcategories.jsonl`, `nodes/periods.jsonl`
   - `edges/evolves_to.jsonl`, `edges/contains_topic.jsonl`, `edges/active_in.jsonl`, `edges/neighbor_of.jsonl`, `edges/parent_of.jsonl`
   - `metadata.json` (version: `kg_v1_pr_conditional`), `validation_report.json`

3. **Which PR cases are graph-visible?** PR-P1, PR-P2, PR-P3, PR-P4 (all 4 curated positives, Tier A and Tier B).

4. **How are negative/ambiguous cases handled?** PR-N1..N5 and PR-A1..A2 are NOT written to any graph edge file. They exist only in the curation doc as calibration anchors.

5. **What is the frontend opt-in mechanism?** URL query parameter `?pr_preview=1`. When present, `KnowledgeGraph.jsx` loads the PR conditional bundle and enables the hidden PR preset in filters. The default `/knowledge-graph` page is unchanged.

6. **Does the default /knowledge-graph still show only LO+AG?** YES. The default `useKnowledgeGraph()` call (no `sourceMode` argument) loads from `kg_v1_visualization/` and shows only LO+AG topics.

7. **Do tests and build pass?** See Section 8 for the command list. Results recorded after running.

8. **Has math.PR reached Gate 1?** YES — all Gate 1 entry conditions are met by this implementation:
   - Schema fields (7) added as nullable/optional ✓
   - PR conditional export to `kg_v1_pr_conditional/` implemented ✓
   - `subgraph_pr.json` generated ✓
   - `legend.json` updated with "provisional" entry ✓
   - Frontend filter preset "PR conditional" added (hidden by default) ✓
   - Tests for all new conditional paths added ✓

9. **Next step recommendation:** PR-TrackB-06 COMPLETE (2026-03-29) — DEMOTED; Gate 2 COLLAPSED. No further Track B reviews scheduled. math.PR at long-term Gate 1. No code work blocked by Track B.
