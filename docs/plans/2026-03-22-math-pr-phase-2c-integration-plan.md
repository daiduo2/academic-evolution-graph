doc_type: "integration_plan"
scope: "math.PR conditional graph integration — Phase 2C"
status: "PLANNING COMPLETE — Implementation can begin (conditional layer only)"
owner: "docs-agent"
package_id: "PR-2C"
date: "2026-03-22"
---

# math.PR Phase 2C — Conditional Graph Integration Plan
Date: 2026-03-22
Package: PR-2C
Status: PLANNING COMPLETE — Implementation can begin (conditional layer only)

## 1. Executive Summary

MPR-01C and MPR-02 are complete: curation produced 4 positives (P1/P2 Tier A dual-source, P3/P4 Tier B single-source), 5 negatives, and 2 ambiguous cases. Technical analysis across all five layers (schema, export, bundle, frontend, and integration gates) is complete. The recommended decision is Option C (split path): begin conditional implementation now on a separate output layer, while blocking Gate 2 on paper-level review that runs in parallel. The LO+AG baseline remains fully protected throughout — math.PR does not enter `data/output/kg_v1/` at any point under this plan.

## 2. Current State of math.PR

### Package History

- MPR-01C-final-fix (2026-03-20): PR-targeted extraction complete, evolves_from direction corrected; MPR-02 unlocked
- MPR-02 (2026-03-21): Case curation complete; 4 positives, 5 negatives, 2 ambiguous; conditional readiness confirmed

### Current Gate

**Gate 0: Curated, Not Integrated** — math.PR is HERE.

### Curated Case Summary

| Case ID | Pair | Tier | Evidence Source | Status |
|---------|------|------|-----------------|--------|
| PR-P1 | global_38 → global_100 | Tier A | evolves_from (main graph) + adjacency bw=0.35 | Conditional |
| PR-P2 | global_38 → global_156 | Tier A | evolves_from (main graph) + adjacency bw=0.4077 | Conditional |
| PR-P3 | global_38 → global_99  | Tier B | evolves_from (main graph) only | Conditional |
| PR-P4 | global_65 → global_188 | Tier B | adjacency-only bw=0.4795 | Conditional |
| PR-N1 | global_211 | — | boundary negative (biology/physics) | Negative |
| PR-N2 | global_47  | — | boundary negative (math.MP crossover) | Negative |
| PR-N3 | global_61  | — | boundary negative (applied vs theoretical) | Negative |
| PR-N4 | global_214 | — | boundary negative | Negative |
| PR-N5 | global_333 | — | boundary negative | Negative |
| PR-A1 | global_65 ↔ global_39 | — | ambiguous (shared stochastic domain) | Ambiguous |
| PR-A2 | global_271 ↔ global_99 | — | ambiguous | Ambiguous |

### What "Conditional" Means Here

"Conditional graph-visible" is not the same as "baseline-included." A math.PR edge can appear in a separate PR conditional output layer (`data/output/kg_v1_pr_conditional/`) and in an opt-in frontend preset — but it does NOT enter `data/output/kg_v1/` and does NOT appear on the default `/knowledge-graph` page. Baseline-included status requires Gate 2 passage.

## 3. Integration Gates

### Gate 0: Curated, Not Integrated (CURRENT — math.PR is HERE)

**Entry conditions (already met):**
- Case curation complete (MPR-02)
- Positives, negatives, and ambiguous cases documented
- At least 2 Tier A positives with dual-source evidence

**Allowed operations at Gate 0:**
- Document planning (PR-2C — this document)
- Schema analysis, export analysis, bundle analysis, frontend analysis
- Risk documentation

**Blocked operations at Gate 0:**
- Writing any PR data to `data/output/kg_v1/`
- Adding PR pairs to the production graph bundle
- Exposing PR edges on the default frontend

**Exit conditions (Gate 0 → Gate 1):**
- PR-2C planning document complete (this document)
- Paper-level review of global_38, global_65, global_188 initiated
- PR-2C-impl scope approved (Option C — conditional layer; see Section 10)

---

### Gate 1: Conditional Graph-Visible (Provisional) — math.PR is BELOW this gate

**Entry conditions:**
- Gate 0 exit conditions met
- Schema fields (7) added as nullable/optional
- PR conditional export to `data/output/kg_v1_pr_conditional/` implemented
- `subgraph_pr.json` generated
- `legend.json` updated with "provisional" entry
- Frontend filter preset "PR conditional" added (hidden by default)
- Tests for all new conditional paths passing

**Allowed operations at Gate 1:**
- Serving `subgraph_pr.json` as an opt-in overlay
- Displaying PR edges under the "PR conditional" frontend preset (hidden by default)
- Running paper-level review in parallel

**Blocked operations at Gate 1:**
- Merging PR data into `data/output/kg_v1/`
- Enabling PR edges by default on the frontend
- Promoting any PR pair to baseline-included status

**Exit conditions (Gate 1 → Gate 2) — ALL required:**
- Paper-level review of global_38 (>=5 papers from 2025-02/03 periods sampled)
- Paper-level review confirms P1/P2 as genuine evolution events (not transient co-occurrence)
- global_38 confirmed as durable topic (not transient) — resolves R1
- math.PR classification of global_65 and global_188 verified (not dual-assigned AP/PR) — resolves R3
- PR benchmark runner implemented and passing (MPR-03 or equivalent)

---

### Gate 2: Baseline Inclusion Eligible — math.PR is WELL BELOW this gate

**Entry conditions:**
- All Gate 1 exit conditions met
- Benchmark runner (MPR-03) passing for PR positives
- R1, R2, R3 risks resolved (documented, not assumed)
- PR data validated against KG schema with 0 errors

**Allowed operations at Gate 2:**
- Writing PR topics and EVOLVES_TO edges to `data/output/kg_v1/`
- Including PR in the default graph bundle
- Enabling PR visibility by default on the frontend

**Blocked operations at Gate 2:**
- Removing the `integration_scope` field from PR edges (must remain for audit trail)
- Retroactively changing Tier B cases to Tier A without new evidence

**Exit conditions:** Full PR integration complete, KG v1 coverage updated from LO+AG to LO+AG+PR.

## 4. Schema Implications

The following 7 schema changes are minimum-necessary and all backward-compatible. All new fields are nullable or additive.

| # | Field | Node/Edge | Type | Status | Source |
|---|-------|-----------|------|--------|--------|
| 1 | `integration_scope` | Topic nodes | enum: "baseline" \| "conditional" \| "excluded" | NEW | PR-2C planning |
| 2 | `integration_scope` | EVOLVES_TO edges | enum: "baseline" \| "conditional" \| "excluded" | NEW | PR-2C planning |
| 3 | `curation_tier` | EVOLVES_TO edges | enum: "A" \| "B" \| null | NEW | MPR-02 curation |
| 4 | `curation_status` | EVOLVES_TO edges | enum: "positive" \| "negative" \| "ambiguous" \| null | EXTENSION of existing `benchmark_status` pattern |
| 5 | `human_review_required` | EVOLVES_TO edges | bool (nullable) | NEW | PR-2C risk register |
| 6 | `graph_integration_candidate` | EVOLVES_TO edges | enum: "gate1_eligible" \| "gate2_blocked" \| "excluded" \| null | NEW | PR-2C gate system |
| 7 | `source_period_first` / `source_period_last` | Topic nodes | string (nullable, ISO period) | NEW | MPR-01C extraction data |

Schema validation must treat all new fields as optional/nullable — existing LO+AG records carry none of these fields and must remain valid.

Existing analogues in the schema that confirm this pattern is established: `benchmark_status`, `confidence`, `evidence_type`, `review_flags[]`.

## 5. Export-Layer Plan

### Changes to `pipeline/math_kg_export.py`

4 minimum changes required:

1. **Parameterize `target_subcategories`** — currently hardcoded as `{'LO', 'AG'}` at line 438. Change to accept a parameter so PR can be included conditionally without modifying the baseline path. LO+AG default is preserved exactly.

2. **Add `hierarchies["math.PR"]["topic_assignments"]` as optional ID source** — when `--benchmark-pr` flag is active, the exporter reads PR topic IDs from the hierarchy metadata. This is the same lookup pattern used for LO and AG.

3. **Add `--benchmark-pr` CLI argument + PR case ID parsing** — parses case IDs in `pr-p*`, `pr-n*`, `pr-a*` format. When this flag is absent, the exporter behaves identically to the current production baseline.

4. **Update `validate_output()` to allow PR under a conditional flag** — the current `validate_output()` actively blocks PR. Add a conditional path: if `--benchmark-pr` is active and output dir is `kg_v1_pr_conditional/`, PR records are valid. If output dir is `kg_v1/`, PR records remain blocked.

**New output directory:** `data/output/kg_v1_pr_conditional/`

**Isolation guarantee:** `data/output/kg_v1/` is NEVER touched by any PR operation. The PR exporter writes only to `kg_v1_pr_conditional/`. These are separate directories with no shared write paths.

### Change to `pipeline/math_kg_visualization_export.py`

- Add `build_subgraph(bundle, 'PR')` call, conditional on PR being present in the input bundle. When called without a PR bundle, behavior is identical to current production. This generates `subgraph_pr.json` alongside the existing `subgraph_lo.json` and `subgraph_ag.json`.

## 6. Bundle / Contract Plan

### Changes to `data/output/kg_v1_visualization/`

3 minimum bundle changes:

1. **Add "provisional" to `legend.json` evidence_types registry** — "provisional" is already used as an `evidence_type` value in the schema design (see `2026-03-19-math-knowledge-graph.md`). It must be registered in the legend for frontend consumers to correctly interpret PR edges. This is a pure addition — existing entries are not modified.

2. **Generate `subgraph_pr.json`** alongside existing `subgraph_lo.json` and `subgraph_ag.json` — same format, same schema, PR-scoped. This file is written to `kg_v1_pr_conditional/` not `kg_v1_visualization/` for isolation.

3. **Add "pr_conditional" preset to frontend filter dimensions** — the preset is hidden by default (opt-in only). It enables: subcategory=PR, confidence=inferred, evidence_type=provisional.

### Backward Compatibility

Three isolation mechanisms guarantee no regression to LO+AG baseline:

1. **Separate output directories** — `kg_v1/` and `kg_v1_pr_conditional/` are independent. No shared write path.
2. **Explicit inclusion lists** — `target_subcategories` parameter must explicitly include 'PR'; the default `{'LO', 'AG'}` never changes.
3. **Validation gate** — `validate_output()` enforces directory-level rules. PR records in `kg_v1/` are a validation error regardless of other flags.

## 7. Frontend Impact

5 minimum UI additions (all additive, none modifying existing behavior):

1. **"inferred/conditional" EVOLVES_TO edge stroke style** — dashed stroke pattern for edges where `evidence_type == "provisional"`. Confirmed edges retain solid stroke. This distinguishes PR provisional edges visually without requiring new components.

2. **"PR conditional" filter preset** — hidden by default; MUST be opt-in. The preset sets `subcategory=PR, confidence=inferred, evidence_type=provisional`. No default filter state is modified. Users see only LO+AG unless they explicitly activate this preset.

3. **math.PR subcategory label in `SUBCATEGORY_LABELS`** (`frontend/src/hooks/useKnowledgeGraph.js`, approximately 1 line) — adds "math.PR" → "Probability Theory" to the label map. The color (#84cc16 lime) is ALREADY pre-mapped in `SUBCATEGORY_COLORS` — no color change needed.

4. **"evidence quality" / "review pending" indicator in TopicDetail panel** — when a topic or edge carries `human_review_required: true`, show a "Review Pending" badge. This is additive to the existing detail panel.

5. **PR data isolation mechanism** — the frontend loads `subgraph_pr.json` only when the "PR conditional" preset is active, via a separate `useEffect` or source flag guard in `useKnowledgeGraph.js`. The default page load does NOT fetch PR data.

**Deferrable to implementation phase:** All 5 changes can be deferred until PR-2C-impl. No frontend changes are required to complete PR-2C planning.

## 8. Non-Goals (this round)

This planning document and its associated implementation (PR-2C-impl) explicitly DO NOT:

- Modify `data/output/kg_v1/` in any way (LO+AG production baseline is untouched)
- Promote any PR pair to baseline-included status
- Write PR data to the production KG bundle
- Ship PR edges to the current `/knowledge-graph` page by default
- Resolve R1, R2, or R3 risks (they are documented and tracked, not resolved here)
- Run paper-level review (this is a human task that runs in parallel as Track B)
- Create a PR benchmark runner (MPR-03 — this is a Gate 2 requirement, not Gate 1)
- Assess or modify math.QA, math.RA, or math.RT status

## 9. Risk Register

Three residual risks carried forward from MPR-02:

### R1: global_38 Transience
**Description:** global_38 is the source of P1, P2, and P3 — the three Tier A and Tier B object-continuity pairs that depend on it. global_38 has only 2 active periods (2025-02 and 2025-03). A topic with only 2 closely-spaced periods may be transient rather than a durable research thread.

**Mitigation:** Paper-level sampling of global_38 papers (5+ papers from the 2025-02/03 periods). This is a Gate 1 exit condition and runs as Track B.

**KG impact if unresolved:** If global_38 is confirmed transient, P1, P2, and P3 all downgrade simultaneously. Only P4 would remain as a Gate 2 candidate (subject to R2). This would reduce Tier A to 0 and require reassessment of Gate 2 eligibility.

### R2: P4 Adjacency-Only Fragility
**Description:** PR-P4 (global_65 → global_188) has no `evolves_from` edge in the main topic graph. It is supported only by adjacency bandwidth (bw=0.4795). Additionally, global_65 and global_188 appear in concurrent periods, which weakens the temporal directionality of the evolution claim.

**Mitigation:** Paper-level review for global_65 and global_188 to find directional evidence (e.g., papers citing both topics in a temporally ordered way). This is a Gate 1 exit condition.

**KG impact if unresolved:** P4 stays Tier B in the KG even after Gate 1 passage. It can only reach Gate 2 eligibility after R2 is resolved. P4 will carry `human_review_required: true` at all times until resolved.

### R3: PR/AP Boundary for global_65 and global_188
**Description:** global_65 (随机微分方程收敛) and global_188 (随机粗糙McKean方程) are assigned to math.PR in the hierarchy metadata. However, these topics may be dual-assigned or better classified under math.AP (analysis of PDEs / applied probability). If they are primarily math.AP, encoding them as math.PR-only in the KG would be misleading.

**Mitigation:** Verify math.PR classification for global_65 and global_188 in `aligned_topics_hierarchy.json` before encoding in the KG. Cross-check against math.AP assignment lists. This is a Gate 1 exit condition.

**KG impact if unresolved:** If global_65 or global_188 are dual-assigned, they must be encoded as multi-subcategory topics with appropriate `integration_scope` restrictions. P4 may need to be re-labeled or excluded.

## 10. Recommendation for Implementation

**Decision: Option C — Split path.**

Two parallel tracks:

### Track A — Begins Now (Code Work)
Conditional layer implementation. This track is not blocked on Track B.

**PR-2C-impl scope (precise):**
- Schema fields: 7 additions to `math_kg_export.py` (all nullable, all backward-compatible)
- PR conditional export: write PR topics and EVOLVES_TO edges to `data/output/kg_v1_pr_conditional/` only
- `subgraph_pr.json` generation via `math_kg_visualization_export.py`
- `legend.json` "provisional" evidence_type entry
- Frontend filter preset "PR conditional" (hidden by default, opt-in only)
- SUBCATEGORY_LABELS entry for math.PR (1 line)
- Tests for all new conditional paths

### Track B — Runs in Parallel (Human Work, No Code Dependency)
Paper-level review of global_38, global_65, and global_188. This is a human research task. Track A implementation proceeds regardless of Track B timeline.

**Track B tasks:**
- Sample >=5 papers from global_38 (2025-02/03 periods) — resolves R1
- Sample papers from global_65 and global_188 for directional evolution evidence — resolves R2
- Verify math.PR classification for global_65 and global_188 vs math.AP — resolves R3

### Gate Advancement Boundary

**PR-2C-impl COMPLETE does NOT advance math.PR to Gate 2.** Completing PR-2C-impl advances math.PR from Gate 0 to Gate 1 (Conditional Graph-Visible). Gate 2 requires:

1. Paper-level confirmation from Track B (R1, R2, R3 resolved)
2. PR benchmark runner (MPR-03) implemented and passing
3. These are separate work items from PR-2C-impl and must not be conflated with it.
