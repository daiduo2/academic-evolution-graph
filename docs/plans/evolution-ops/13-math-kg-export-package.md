---
doc_type: "task_package_detail"
package_id: "KG-02"
owner: "rule-worker"
tree_path: "math knowledge graph"
task_type: "graph_export_implementation"
target_rule:
  - "math historical topic evolution graph"
  - "benchmark-to-graph export"
goal: "实现 LO + AG confirmed baseline 的 Math KG v1 exporter，输出 nodes/edges split files 与 validation metadata"
status: "completed"
---

# KG-02: Math Knowledge Graph v1 Export Implementation

## Purpose

实现 Math KG v1 的导出器，将已确认的 LO 和 AG benchmark 数据转换为结构化图谱文件，并暴露 graph-facing narrative metadata。

## Scope

### Included
- math.LO (confirmed, hierarchy-scoped baseline) - 4 cases encoded (of 13 documented), with `modal_baseline + bridge_ring + boundary/review` metadata
- math.AG (confirmed, hierarchy-scoped baseline) - 5 cases encoded from the current v2 export contract (`ag-p1 + ag-n1/ag-n2/ag-n3 + ag-amb1`), with `confirmed_core + bridge_ring + excluded_boundary` metadata

### Metadata-Only Narrative Support
- math.CO - no baseline nodes or edges added; `metadata.json` exposes the landed `matroid_mvp` contract, supporting bridge, and boundary/near-miss layers
- math.DS - no baseline nodes or edges added; `metadata.json` exposes the DS benchmark skeleton as graph-facing `bridge + boundary + review` narrative only

### Explicitly Excluded (Deferred to Phase 2C)
- math.PR (provisional, needs MPR-01C first)

### Not in v1
- math.QA (gap)
- math.RA (gap)
- math.RT (not assessed)

## Input Specification

1. `data/output/aligned_topics_hierarchy.json`
   - Topic hierarchy and metadata
   - Period information
   - Topic assignments by subcategory

2. `docs/plans/2026-03-12-math-lo-benchmark.md`
   - 5 positive, 6 negative, 2 ambiguous cases

3. `docs/plans/2026-03-18-math-ag-benchmark.md`
   - 3 positive, 3 negative, 1 ambiguous cases

## Output Specification

Directory: `data/output/kg_v1/`

```
kg_v1/
├── nodes/
│   ├── topics.jsonl         # 32 topics (15 LO + 17 AG)
│   ├── subcategories.jsonl  # math.LO, math.AG
│   └── periods.jsonl        # 2025-02 through 2026-02 (13 periods)
├── edges/
│   ├── contains_topic.jsonl # 32 edges (Subcategory -> Topic)
│   ├── active_in.jsonl      # 55 edges (Topic -> Period)
│   ├── neighbor_of.jsonl    # 63 edges (Topic <-> Topic, real adjacency)
│   ├── parent_of.jsonl      # 22 edges (Topic -> Topic)
│   └── evolves_to.jsonl     # 9 edges with benchmark annotations
├── metadata.json            # Coverage stats + domain_knowledge_layers
└── validation_report.json   # Schema validation
```

## Schema Compliance

### Topic Node Schema
- id, type, name, keywords[]
- category, subcategory
- topic_mode, total_papers, active_periods (int)
- history[], hierarchy_path[], hierarchy_depth

### Edge Schemas
All edges have: source, target, type (UPPERCASE)

EVOLVES_TO edges additionally have:
- evidence_type: "benchmark-confirmed"
- confidence: "confirmed" | "negative" | "ambiguous"
- benchmark_case_id, benchmark_status
- expected_relation, subcategory
- optional graph-facing annotations:
  - `graph_band`
  - `graph_layer`
  - `graph_role`
  - `graph_export_status`

### Metadata Narrative Layer

`metadata.json` additionally exposes `domain_knowledge_layers`:

- `math.LO`
  - `modal_baseline`
  - `bridge_ring`
  - `boundary_negative`
  - `review_boundary`
- `math.AG`
  - `confirmed_core`
  - `bridge_ring` (metadata-only for `ag-p2/ag-p3`)
  - `excluded_boundary`
  - `review_boundary`
- `math.CO`
  - `matroid_mvp`
  - `bridge_support`
  - `excluded_boundary`
  - `review_boundary`
  - `deferred_branch`
- `math.DS`
  - `ergodic_entropy_skeleton`
  - `excluded_boundary`
  - `review_boundary`
- `math.NA`
  - `krylov_iterative_skeleton`
  - `excluded_boundary`
  - `review_boundary`

Each domain block also exposes:

- `baseline_truth_layer_keys`
- `narrative_only_layer_keys`
- `visible_graph_bands`

This narrative layer does not change topology. It only makes the exported bundle thicker and easier to explain.

## Benchmark Case Mapping

### Benchmark Document Counts

| Case Type | Count | Encoding |
|-----------|-------|----------|
| LO positive | 5 | EVOLVES_TO with confidence: confirmed |
| LO negative | 6 | EVOLVES_TO with confidence: negative |
| LO ambiguous | 2 | EVOLVES_TO with confidence: ambiguous |
| AG export-contract positive | 1 | `ag-p1` only |
| AG negative | 3 | EVOLVES_TO with confidence: negative |
| AG ambiguous | 1 | `ag-amb1` review edge |
| **Total** | **18** | 13 LO + 5 AG export-contract cases |

### Actually Encoded (After KG-02-fix)

| Case Type | Count | Notes |
|-----------|-------|-------|
| LO positive | 2 | Only cases where both topics in LO hierarchy topic_assignments |
| LO negative | 1 | lo-n1: global_51 -> global_75 |
| LO ambiguous | 1 | lo-a2: global_339 -> global_51 |
| AG positive | 1 | ag-p1 is the sole baseline positive in the current AG export contract |
| AG negative | 3 | All AG cases have topics in hierarchy |
| AG ambiguous | 1 | ag-amb1 remains visible as review-only boundary metadata and exported ambiguous edge |
| **Total** | **9** | 9 of 18 benchmark cases encodable with current hierarchy |

**Note:** The KG-02-fix changed topic source from `trends[*].subcategory` to `hierarchies[*].topic_assignments`, which reduced LO topics from 29 to 15. Many benchmark cases reference topics that have `subcategory=LO` in trends but are not in the LO hierarchy's topic_assignments. These cases cannot be encoded until the hierarchy is updated to include them.

**AG note:** `ag-p2` / `ag-p3` are graph-facing `bridge_ring` support in the current v2 benchmark, but they remain metadata-only. They are not exported as baseline truth edges.

## Files Created

- `pipeline/math_kg_export.py` - Graph export implementation
- `tests/test_math_kg_export.py` - Test suite (74 tests)
- `docs/plans/evolution-ops/13-math-kg-export-package.md` - This document

## Done When (All Completed)

- [x] `pipeline/math_kg_export.py` implemented
- [x] `tests/test_math_kg_export.py` passes (74/74)
- [x] All 10 output files generated
- [x] LO benchmark cases encoded as edge annotations
- [x] AG current export contract encoded as edge annotations (5 cases from 2026-03-18 v2 benchmark)
- [x] math.PR explicitly excluded from output
- [x] validation_report.json shows 0 schema errors
- [x] metadata.json has accurate counts and domain-layer narrative metadata

## Stop Conditions (None Triggered)

- [ ] Need to modify evolution_analysis.py - NOT NEEDED
- [ ] Need to modify registry - NOT NEEDED
- [ ] Need to include PR provisional data in baseline - CORRECTLY EXCLUDED
- [ ] Need to include QA/RA/RT data - NOT NEEDED

## Run Commands

```bash
# Run exporter
python3 pipeline/math_kg_export.py \
  --input data/output/aligned_topics_hierarchy.json \
  --benchmark-lo docs/plans/2026-03-12-math-lo-benchmark.md \
  --benchmark-ag docs/plans/2026-03-18-math-ag-benchmark.md \
  --output-dir data/output/kg_v1

# Run tests
pytest tests/test_math_kg_export.py -q
```

## Verification Output (After KG-02-fix)

```
Export complete!
Output directory: data/output/kg_v1
Total topics: 32
Total edges: 181
Benchmark cases encoded: 9
  math.AG: 17 topics
  math.LO: 15 topics
```

**Changes from KG-02-fix:**
- LO topics: 29 → 15 (using hierarchy topic_assignments as source-of-truth)
- Total topics: 46 → 32
- Benchmark cases encoded: 18 → 9 (only cases where both topics in hierarchy)
- neighbor_of edges: 241 → 63 (using real graph adjacency, not cliques)

## Validation Report

```json
{
  "schema_version": "kg_v1",
  "validation_timestamp": "2026-03-19T01:35:32.421564",
  "schema_errors": [],
  "missing_files": [],
  "node_count_check": "pass",
  "edge_count_check": "pass",
  "benchmark_alignment_check": "pass",
  "status": "valid"
}
```

## Next Steps After KG-02

### Option A: MPR-01C (Conditional)
Execute PR-targeted candidate extraction to potentially enable PR integration

### Option B: KG-03 (Recommended if PR not ready)
Visualization preparation and conditional PR integration (Phase 2C)

## KG-02-fix Corrections

The following corrections were made to fix data quality issues in the KG-02 export:

### Topic Source Fix

| Aspect | Before | After |
|--------|--------|-------|
| Source | `trends[*].subcategory` | `hierarchies["math.LO"]["topic_assignments"]` |
| LO Count | 29 topics | 15 topics |
| Issue | Included topics not in LO hierarchy | Uses hierarchy as source-of-truth for baseline |

**Why**: The hierarchy's `topic_assignments` is the authoritative source for which topics belong to a subcategory. Using `trends[*].subcategory` incorrectly included topics that were not part of the LO hierarchy.

### Neighbor Adjacency Fix

| Aspect | Before | After |
|--------|--------|-------|
| Method | Generated clique edges from subcategory membership | Uses real graph adjacency from input data |
| Edge Count | 241 edges (artificial) | Actual neighbor relationships |
| Issue | Clique generation creates artificial relationships | Real graph structure preserved |

**Why**: Generating complete subgraphs (cliques) within each subcategory created false relationships between topics that may not actually be neighbors in the underlying graph. Using the actual adjacency data from `input_data["topic_graph"]["edges"]` ensures only real relationships are exported.

### Test Infrastructure Fix

| Aspect | Before | After |
|--------|--------|-------|
| Test Data | Read from fixed workspace path | Uses temporary directory with fresh export |
| Issue | Tests validated old output, not current code | Tests validate actual exporter behavior |

**Why**: Tests were reading from a hardcoded workspace path (`/Users/dchaos/.codex/worktrees/...`), meaning they validated stale output rather than the current code's behavior. Using `tempfile.TemporaryDirectory()` ensures each test run exports fresh data and validates the actual implementation.

## Change Log

- **2026-03-19**: KG-02 completed
  - Exporter implemented with full benchmark case encoding
  - 69 tests passing
  - 0 schema errors
  - math.PR correctly excluded from baseline
- **2026-03-19**: KG-02-fix corrections applied
  - Fixed topic source to use hierarchy topic_assignments (LO=15, was 29)
  - Fixed neighbor adjacency to use real graph edges (removed 241 fake clique edges)
  - Fixed test infrastructure to use temporary directories
- **2026-03-22**: MKG-FILL-01 export-facing narrative sync
  - Switched AG export parsing to the current 2026-03-18 v2 benchmark contract
  - Added `domain_knowledge_layers` to `metadata.json`
  - Added edge-level `graph_band / graph_layer / graph_role / graph_export_status`
  - Exposed LO `modal_baseline + bridge_ring`, AG `confirmed_core + bridge_ring + excluded_boundary`, and docs-only CO `matroid_mvp` support without changing baseline topology
- **2026-03-22**: MKG-FILL-02 bundle thickening sync
  - Added docs-only `math.DS` narrative metadata for the benchmark skeleton (`bridge + boundary + review`)
  - Kept `math.DS` outside baseline topology and outside encoded `EVOLVES_TO` truth
  - Added visualization-facing narrative case stats so metadata-only domains remain visible without changing edge totals
- **2026-03-22**: MKG-FILL-03 graph thickening sync
  - Added docs-only `math.NA` narrative metadata for the Krylov benchmark skeleton (`bridge + boundary + review`)
  - Exposed per-domain `baseline_truth_layer_keys / narrative_only_layer_keys / visible_graph_bands`
  - Extended visualization bundle filters/stats so metadata-only graph bands remain visible without implying baseline expansion
