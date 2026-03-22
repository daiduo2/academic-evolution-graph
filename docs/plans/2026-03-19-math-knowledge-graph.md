doc_type: "knowledge_graph_design"
scope: "math historical topic evolution knowledge graph"
status: "design_v1"
owner: "doc-worker"
source_of_truth: true
upstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-12-math-worker-backlog.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/03-task-packages.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-12-math-lo-benchmark.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-18-math-ag-benchmark.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-18-math-pr-benchmark.md"
downstream_docs: []
last_reviewed: "2026-03-19"
package_id: "PKG-MATH-KG-01"
---

# Math Historical Topic Evolution Knowledge Graph v1

## Executive Summary

This document defines the first version of the Math Historical Topic Evolution Knowledge Graph (Math KG v1). It establishes the schema, coverage scope, evidence model, and bootstrap plan for representing mathematical topic evolution as a structured knowledge graph.

**Key Design Decisions:**
- v1 covers **math.LO + math.AG + math.PR(provisional)** only
- Schema distinguishes **data-derived edges** from **evidence-derived edges**
- Benchmark cases are represented as **edge annotations**, not standalone nodes
- math.PR enters the graph with **provisional status** (structure confirmed, cases inferred)
- Gap subdomains (math.QA, math.RA) are explicitly excluded from v1

## Core Graph vs Background Math Structure

### Understanding the Scope

This knowledge graph operates at two levels:

**Core Graph (v1)**
- **Confirmed core subgraphs:** `math.LO`, `math.AG`
- **Provisional core subgraph:** `math.PR`
- **Total topics:** 61 (LO: 15, AG: 17, PR: 29)
- **Evidence quality:** Benchmark-verified (LO/AG), Inferred (PR)
- **Use case:** Temporal evolution analysis, benchmark validation

**Background Math Structure**
- **Purpose:** Provides disciplinary context for core subgraphs
- **Included:** All math topics from `topic_graph.json` (394 total nodes)
- **Role:** Enables cross-disciplinary linking and navigation
- **Evidence quality:** Data-derived (hierarchy, neighbors, activity)
- **Not in v1 core:** `math.QA`, `math.RA`, `math.RT`, and other subdomains

### Why This Distinction Matters

The Background Math Structure ensures topics are not isolated:
- Topics in LO/AG/PR can link to topics in QA/RA/RT via `NEIGHBOR_OF` edges
- Cross-disciplinary paths can traverse through background structure
- Future v2 expansion can promote background topics to core status

### Visual Representation

```
Math Knowledge Graph v1
├── CORE GRAPH (Validated Evolution Subgraphs)
│   ├── math.LO [ready] ──────── 15 topics, 13 benchmark cases
│   ├── math.AG [ready] ──────── 17 topics, 6 benchmark cases
│   └── math.PR [provisional] ── 29 topics, inferred chains
│
└── BACKGROUND STRUCTURE (Contextual Topics)
    ├── math.QA [gap] ────────── 0 topics in current snapshot
    ├── math.RA [gap] ────────── 3 topics, single-period only
    ├── math.RT [not assessed] ─ 5 topics, no multi-period data
    └── Other math subdomains ── ~337 topics, data-derived edges only
```

### Evidence Level by Scope

| Scope | Evidence Type | Use in Graph |
|-------|--------------|--------------|
| Core (LO/AG) | `benchmark-confirmed` | Primary evolution edges |
| Core (PR) | `provisional` + `inferred` | Candidate chains, review flagged |
| Background | `data-derived` | Context, navigation, neighbor links |

## Problem Statement

We need to organize the following into a coherent graph model:
- Topic graph from `topic_graph.json` (394 nodes, temporal relationships)
- Evolution cases from `evolution_cases.json` (20 cases in bootstrap export)
- Benchmark evidence from `math.LO` (13 documented benchmark cases; 4 encodable in KG-02 baseline) and `math.AG` (6 documented benchmark cases; 5 encodable in KG-02 baseline)
- Provisional candidate data from `math.PR` (12 multi-period topics, 11 eligible anchors)

The challenge is to represent these at different evidence levels without conflating confirmed benchmark results with inferred candidates.

## Scope for v1: Core Graph Definition

**⚠️ Important:** v1 is a **Core Graph** (closed/near-closed subdomain evolution subgraphs), NOT a full-math knowledge graph. See [Core Graph vs Background Math Structure](#core-graph-vs-background-math-structure) for details.

### In Scope: Core Graph Subgraphs

| Subdomain | Topics | Multi-period Topics | Eligible Anchors | Benchmark Status | Evidence Quality[^1] |
|-----------|--------|-------------------|------------------|------------------|---------------------|
| math.LO   | 15     | 3                 | 3                | ✅ Ready         | 13 cases (5+, 6-, 2~) |
| math.AG   | 17     | 3                 | 3                | ✅ Ready         | 6 documented benchmark cases; 5 encodable in KG-02 baseline |
| math.PR   | 29     | 12                | 11               | ⚠️ Provisional   | Structure confirmed, cases inferred |

### Out of Scope: Background Structure Only

| Subdomain | Topics | Multi-period Topics | Eligible Anchors | Status | Exclusion Reason |
|-----------|--------|-------------------|------------------|--------|------------------|
| math.QA   | 0      | 0                 | 0                | ❌ Gap | No surviving aligned topics in current worktree snapshot |
| math.RA   | 3      | 0                 | 0                | ❌ Gap | All topics single-period, no evolution cases |
| math.RT   | 5      | 0                 | 0                | ❌ Not Assessed | Not yet evaluated |
| Other     | ~337   | -                 | -                | ❌ Not Assessed | Outside current data window |

[^1]: Data sourced from `topic_graph.json` (generated 2026-03-12) and benchmark docs (2026-03-12 to 2026-03-18). Counts verified against worktree 2124 at 2026-03-19.

### Why This Scope?

**math.LO and math.AG** have:
- Multiple multi-period topics enabling temporal evolution analysis
- Fixed benchmark cases with positive/negative/ambiguous classification
- Verified through benchmark runner; KG-02 baseline currently encodes only hierarchy-scoped benchmark pairs (LO: 4 of 13, AG: 5 of 6)

**math.PR** has:
- Strong structural evidence (12 multi-period topics, 11 eligible anchors)
- Inferred evolution chains (percolation → random walk → rough paths)
- Only 1 explicit case in current export (needs PR-targeted extraction)
- **Provisional status**: structure confirmed, explicit cases pending

**math.QA and math.RA** lack:
- Sufficient multi-period topics for temporal analysis
- Clear evolution case candidates
- Cannot form anchor-target pairs for benchmark

## Node Schema

### Node Types

| Node Type | Description | Required Fields |
|-----------|-------------|-----------------|
| `Topic` | Individual research topic from topic model | `id`, `name`, `keywords`, `category`, `subcategory`, `topic_mode`, `total_papers`, `active_periods`, `history[]` |
| `Subcategory` | arXiv subcategory (e.g., math.LO) | `code`, `name`, `discipline`, `topic_count`, `multi_period_count` |
| `Period` | Time period (month) | `id`, `start_date`, `end_date` |

**Note:** v1 starts at the `Subcategory` layer. We do not model a standalone `Discipline` node in KG v1; the discipline is carried as a field on each `Subcategory` node.

### Topic Node Fields

```yaml
Topic:
  id: string                    # global_XXX identifier
  name: string                  # Topic name in Chinese
  keywords: string[]            # Extracted keywords
  category: string              # arXiv category (e.g., "math")
  subcategory: string           # arXiv subcategory (e.g., "LO")
  topic_mode: enum              # "theory" | "method" | "problem"
  topic_profile:                # Mode scores
    primary_mode: string
    secondary_mode: string|null
    theory_score: int
    method_score: int
    problem_score: int
  total_papers: int
  active_periods: int           # Number of periods with papers
  history:                      # Temporal paper distribution
    - period: string
      paper_count: int
  hierarchy_path: string[]      # LLM-built hierarchy
  hierarchy_depth: int
  related_paths: string[]       # Cross-disciplinary paths
  representative_evidence: string[]  # Paper titles
```

### Subcategory Node Fields

```yaml
Subcategory:
  code: string                  # e.g., "math.LO"
  name: string                  # Human-readable name
  discipline: string            # Layer 1 (e.g., "math")
  topic_count: int              # Total topics in subcategory
  multi_period_count: int       # Topics with >1 active period
  single_period_count: int      # Topics with 1 active period
  eligible_anchor_count: int    # Topics meeting anchor criteria
  status: enum                  # "ready" | "provisional" | "gap"
  evidence_quality: enum        # "benchmark-verified" | "inferred" | "insufficient"
```

## Edge Schema

### Edge Types

| Edge Type | Source | Target | Evidence Source |
|-----------|--------|--------|-----------------|
| `CONTAINS_TOPIC` | Subcategory | Topic | Data-derived (hierarchy) |
| `ACTIVE_IN` | Topic | Period | Data-derived (paper counts) |
| `NEIGHBOR_OF` | Topic | Topic | Data-derived (topic_graph.json) |
| `PARENT_OF` | Topic | Topic | Data-derived (hierarchy_path) |
| `EVOLVES_TO` | Topic | Topic | Evidence-derived (benchmark/cases) |
| `CROSS_CATEGORY_LINK` | Topic | Topic | Evidence-derived (cross_category_moves) |

### Evolution Edge Fields

```yaml
EVOLVES_TO:
  source: string                # Source topic ID
  target: string                # Target topic ID
  evidence_type: enum           # "benchmark-confirmed" | "inferred" | "provisional" | "ambiguous"
  evidence_source: string[]     # ["benchmark", "evolution_case", "neighbor_inference"]

  # Evidence level annotation (required)
  confidence: enum              # "confirmed" | "inferred" | "ambiguous" | "unavailable"

  # For benchmark-confirmed edges
  benchmark_case_id: string     # e.g., "lo-b1"
  benchmark_status: enum        # "positive" | "negative" | "ambiguous"
  expected_relation: string     # e.g., "math_lo_modal_continuity"

  # For case-derived edges
  case_id: string               # evolution case ID
  event_types: string[]         # ["diffused_to_neighbor", "expanded", ...]

  # For inferred edges
  inference_basis: string       # Description of inference method
  bridge_strength: float        # 0.0 - 1.0
  shared_keywords: string[]     # Keywords supporting inference

  # Temporal metadata
  anchor_period: string         # Start period
  observation_horizon: int      # Months observed

  # Review status
  review_flags: string[]        # Flags for human review
  last_reviewed: date
```

## Evidence Model

### Evidence Levels

| Level | Description | Encoding | Example |
|-------|-------------|----------|---------|
| **confirmed** | Verified by benchmark runner | `evidence_type: "benchmark-confirmed"` | math.LO object continuity cases |
| **inferred** | Derived from graph structure | `evidence_type: "inferred"` | PR candidate chains from neighbors |
| **ambiguous** | Needs expert review | `evidence_type: "ambiguous"` | math.LO cases under review |
| **unavailable** | No data to assess | `excluded from graph` | math.RA topics |

### Evidence-to-Graph Mapping

| Source Data | Graph Representation | Evidence Level |
|-------------|---------------------|----------------|
| `topic_graph.json` edges | `NEIGHBOR_OF` edges | data-derived |
| `hierarchy_path` | `PARENT_OF` edges | data-derived |
| `evolution_cases.json` | `EvolutionCase` nodes + `EVOLVES_TO` edges | replay evidence |
| Benchmark positive cases | `EVOLVES_TO` edges with `confidence: confirmed` | benchmark-verified |
| Benchmark negative cases | Explicit `confidence: negative` or excluded | benchmark-verified |
| PR neighbor analysis | `EVOLVES_TO` edges with `confidence: inferred` | provisional |

## Source-to-Canonical Mapping

### Export Schema to Graph Schema Mapping

The pipeline exports edges using lowercase snake_case types. These map to canonical graph edge types as follows:

| Source Export Field | Canonical Graph Edge | Direction | Transformation Rule |
|--------------------|----------------------|-----------|---------------------|
| `belongs_to` | `CONTAINS_TOPIC` | Subcategory → Topic | Flip direction[^2] |
| `active_in` | `ACTIVE_IN` | Topic → Period | Direct mapping |
| `adjacent_to` | `NEIGHBOR_OF` | Topic ↔ Topic | Undirected (symmetric) |
| `evolves_from` | `EVOLVES_TO` | Topic → Topic | Flip direction[^3] |
| `hierarchy_path` | `PARENT_OF` | Topic → Topic | Derive from path depth |
| `cross_category_moves` | `CROSS_CATEGORY_LINK` | Topic → Topic | Filter cross-category only |

[^2]: `belongs_to` in export goes Topic → Subcategory. In the graph, we use Subcategory → Topic (`CONTAINS_TOPIC`) to follow "container contains item" semantics.

[^3]: `evolves_from` in export goes Target → Anchor (looking backward). In the graph, we use Anchor → Target (`EVOLVES_TO`) to follow temporal flow direction.

### Field-Level Transformations

```yaml
# belongs_to edge transformation
Export:  {source: "global_56", target: "math.LO", type: "belongs_to"}
Graph:   {source: "math.LO", target: "global_56", type: "CONTAINS_TOPIC"}

# evolves_from edge transformation
Export:  {source: "global_27", target: "global_56", type: "evolves_from"}
Graph:   {source: "global_56", target: "global_27", type: "EVOLVES_TO"}

# active_in edge (direct mapping)
Export:  {source: "global_56", target: "2025-02", type: "active_in"}
Graph:   {source: "global_56", target: "2025-02", type: "ACTIVE_IN"}

# adjacent_to edge (direct mapping, undirected)
Export:  {source: "global_56", target: "global_27", type: "adjacent_to"}
Graph:   {source: "global_56", target: "global_27", type: "NEIGHBOR_OF"}
```

### Evidence Type Mapping

| Source Evidence | Graph `evidence_type` | Graph `confidence` |
|-----------------|----------------------|-------------------|
| Benchmark positive | `benchmark-confirmed` | `confirmed` |
| Benchmark negative | `benchmark-confirmed` | `negative` |
| Benchmark ambiguous | `benchmark-confirmed` | `ambiguous` |
| Evolution case | `case-derived` | `confirmed` |
| Neighbor inference | `inferred` | `inferred` |
| PR provisional | `provisional` | `inferred` |

### Benchmark Case Representation

**Decision: Edge Annotation (Not Node)**

Benchmark cases are represented as **edge annotations**, not standalone nodes. This keeps the graph topology clean while preserving all benchmark metadata.

```yaml
# Example: math.LO positive case lo-b1
Edge: global_56 -> global_27
  evidence_type: "benchmark-confirmed"
  confidence: "confirmed"
  benchmark_case_id: "lo-b1"
  benchmark_status: "positive"
  expected_relation: "math_lo_modal_continuity"
  level: "event-level"
  graph_band: "baseline"
  graph_layer: "modal_baseline"
  graph_role: "event_baseline"
  graph_export_status: "encoded_as_evolves_to"
```

**Rationale:**
- A benchmark case is fundamentally a claim about a relationship between two topics
- Edge annotation avoids node proliferation
- Simplifies graph traversal (no intermediate benchmark nodes to traverse)
- Aligns with how evidence is actually used (to weight/qualify edges)

**Note:** Evolution cases from `evolution_cases.json` are similarly represented as edge annotations with `evidence_type: "case-derived"`, not as standalone nodes. The `EvolutionCase` node type mentioned in early drafts has been removed to maintain schema consistency.

### Export-Facing Narrative Metadata (MKG-FILL-01)

`MKG-FILL-01` adds a graph-facing annotation layer on top of the existing topology:

- `metadata.json` now carries `domain_knowledge_layers`
- Each domain metadata block now exposes:
  - `baseline_truth_layer_keys`
  - `narrative_only_layer_keys`
  - `visible_graph_bands`
- `EVOLVES_TO` edges may carry:
  - `graph_band`
  - `graph_layer`
  - `graph_role`
  - `graph_export_status`

This layer is intentionally interpretive metadata, not new baseline truth:

- `math.LO`: `modal_baseline` stays the only event-level baseline; `type-theory / set theory / forcing / definability` are exposed as a bridge-level ring
- `math.AG`: `ag-p1` stays the only confirmed core edge in baseline topology; `ag-p2/ag-p3` are metadata-only `bridge_ring` support, and `ag-n1/ag-n2/ag-n3` stay `excluded_boundary`
- `math.CO`: no topics or edges are added to baseline topology; only docs-backed contract metadata is exposed (`matroid_mvp`, supporting bridge, boundary, near-miss)
- `math.DS`: benchmark-skeleton-ready narrative may be exposed as metadata-only `bridge / boundary / review` layers, but it must stay outside baseline topology until DS has a real event-level or runner-ready contract
- `math.NA`: benchmark-skeleton-ready Krylov narrative may be exposed as metadata-only `bridge / boundary / review` layers, but it must stay outside baseline topology until NA has a real event-level or runner-ready contract

The key rule is unchanged: bridge / boundary / contract layers can become easier to narrate, but they must not be promoted into baseline truth unless the underlying export contract changes.

This does not expand the core graph. `math.DS` and `math.NA` can be visible in `metadata.domain_knowledge_layers`, but they are not baseline topology and must not be counted as confirmed baseline truth.

## Coverage Decision

### math.LO (Included - Ready)

**Evidence:**
- 5 multi-period topics
- 11 benchmark cases (5 positive, 6 negative, 2 ambiguous)
- All cases verified through `pytest tests/test_math_lo_benchmark.py`

**Graph Entry:**
- All multi-period topics as Topic nodes
- Benchmark-confirmed edges for positive cases
- Explicit negative annotations for negative cases

### math.AG (Included - Ready)

**Evidence:**
- 3 multi-period topics
- 6 benchmark cases (object_continuity only)
- method_continuity explicitly marked as test-evidence-only

**Graph Entry:**
- All multi-period topics as Topic nodes
- Benchmark-confirmed edges for verified cases

### math.PR (Included - Provisional)

**Evidence:**
- 12 multi-period topics (strong structural evidence)
- 11 eligible anchors (papers >= 60, periods >= 2)
- 1 explicit exported case (global_39)
- 3 inferred evolution chains (global_39 → global_99 → global_188)

**Graph Entry:**
- All multi-period topics as Topic nodes
- Edges marked with `confidence: inferred`
- Explicit provisional status annotation

math.PR is on the conditional planning path (PR-2C); it will not enter the baseline graph until Gate 2 conditions are met.

**Critical Distinction:**
```yaml
math.PR provisional encoding:
  subcategory.status: "provisional"
  subcategory.evidence_quality: "inferred"
  edge.evidence_type: "provisional"
  edge.confidence: "inferred"
  edge.inference_basis: "neighbor relationship from global_39 evolution case"
```

### math.QA (Excluded - Gap)

**Exclusion Reason:**
- 0 surviving aligned topics in the current worktree snapshot
- Cannot form temporal evolution pairs
- No clear anchor-target candidates

**Graph Entry:** Not included in v1

### math.RA (Excluded - Gap)

**Exclusion Reason:**
- 0 multi-period topics
- All 3 topics are single-period
- No evolution cases possible

**Graph Entry:** Not included in v1

## Example Subgraphs

### Example 1: math.LO Confirmed Path

```
Subcategory: math.LO (status: ready)
├── Topic: global_56 (直觉主义逻辑证明)
│   ├── ACTIVE_IN → Period: 2025-02
│   ├── ACTIVE_IN → Period: 2025-03
│   └── EVOLVES_TO → Topic: global_27
│       ├── evidence_type: "benchmark-confirmed"
│       ├── confidence: "confirmed"
│       ├── benchmark_case_id: "lo-b1"
│       └── expected_relation: "math_lo_modal_continuity"
│
└── Topic: global_27 (概率逻辑与自动机语义)
    └── ACTIVE_IN → Period: 2025-05
```

### Example 2: math.AG Confirmed Benchmark Path

```
Subcategory: math.AG (status: ready)
├── Topic: global_69 (椭圆曲线模性)
│   ├── ACTIVE_IN → Period: 2025-06
│   ├── ACTIVE_IN → Period: 2025-09
│   └── EVOLVES_TO → Topic: global_287
│       ├── evidence_type: "benchmark-confirmed"
│       ├── confidence: "confirmed"
│       └── expected_relation: "math_ag_object_continuity"
│
└── Topic: global_287 (志村簇与阿贝尔簇)
    └── ACTIVE_IN → Period: 2025-10
```

### Example 3: math.PR Provisional / Inferred-Heavy Path

```
Subcategory: math.PR (status: provisional)
├── Topic: global_39 (随机过程渗流方程)
│   ├── ACTIVE_IN → Period: 2025-02
│   ├── ACTIVE_IN → Period: 2025-06
│   ├── ACTIVE_IN → Period: 2025-10
│   ├── ACTIVE_IN → Period: 2025-11
│   ├── NEIGHBOR_OF → Topic: global_99 (bridge_strength: 0.8)
│   └── EVOLVES_TO → Topic: global_99
│       ├── evidence_type: "provisional"
│       ├── confidence: "inferred"
│       ├── inference_basis: "neighbor relationship + shared keywords"
│       ├── shared_keywords: ["brownian", "convergence", "equations", "stochastic"]
│       └── review_flags: ["needs_curation"]
│
├── Topic: global_99 (随机游走与分支)
│   ├── ACTIVE_IN → Period: 2025-06
│   ├── ACTIVE_IN → Period: 2025-09
│   └── EVOLVES_TO → Topic: global_188
│       ├── evidence_type: "provisional"
│       └── confidence: "inferred"
│
└── Topic: global_188 (随机粗糙McKean方程)
    ├── ACTIVE_IN → Period: 2025-02
    ├── ACTIVE_IN → Period: 2025-06
    ├── ACTIVE_IN → Period: 2025-10
    └── ACTIVE_IN → Period: 2025-11
```

## Non-Goals

This schema design explicitly does NOT include:

1. **Frontend visualization implementation** - Schema only, no UI
2. **Graph database deployment** - JSON-based graph representation
3. **Real-time updates** - Batch export from existing data
4. **All math subdomains** - v1 limited to LO + AG + PR(provisional)
5. **External ontology alignment** - Math KG is standalone
6. **Paper-level nodes** - Topic-level aggregation only

## Bootstrap Plan

### Phase 1: Schema Finalization (Current)

**Status:** ✅ Complete

**Deliverables:**
- [x] Node schema defined
- [x] Edge schema defined
- [x] Evidence model specified
- [x] Coverage scope decided

### Phase 2: Next Implementation Decision

**Decision Required:** Choose between Option A and Option B

#### Option A: KG-02 Graph Export Implementation

**Description:** Implement graph export based on current schema using confirmed data only

**Scope:**
- Export math.LO and math.AG confirmed data
- math.PR excluded until cases curated
- JSON graph format compatible with visualization libraries

**Prerequisites:**
- Schema finalized ✅
- LO benchmark ready ✅
- AG benchmark ready ✅

**Pros:**
- Immediate usable graph output
- Clean separation of confirmed vs inferred
- Lower risk

**Cons:**
- math.PR not included
- Graph incomplete for probability subdomain

#### Option B: MPR-01C PR-Targeted Candidate Extraction

**Description:** Execute PR-specific case surfacing before graph construction

**Scope:**
- Implement PR-targeted export (hierarchy filter or subcategory filter)
- Surface explicit PR evolution cases
- Curate positive/negative/ambiguous cases

**Prerequisites:**
- Schema finalized ✅
- Export filter implementation needed

**Pros:**
- math.PR can enter graph with higher confidence
- More complete graph
- Enables PR benchmark runner (MPR-03)

**Cons:**
- Additional development work
- Delayed graph export
- Risk of still insufficient PR cases

### Recommendation: Option A (KG-02)

**Rationale:**
1. **Risk management:** Confirmed data (LO + AG) provides a clean first export baseline
2. **Incremental progress:** Get the exporter working on benchmark-confirmed subgraphs before adding provisional data
3. **Parallel paths:** MPR-01C can proceed in parallel without blocking KG-02
4. **Evidence separation:** PR remains represented in the schema, but is integrated only after its candidate extraction is stronger

**Phase Roadmap:**

| Phase | Task | Deliverable | Decision Gate |
|-------|------|-------------|---------------|
| 2A | KG-02: Graph Export Implementation | JSON graph files for LO + AG confirmed graph | Proceed if export successful |
| 2B | MPR-01C: PR-Targeted Extraction (parallel) | PR-specific cases | If >=3 explicit cases, proceed to 2C |
| 2C | Conditional: PR Graph Integration | Add PR to graph with proper provisional encoding | Only if 2B successful |
| 3 | KG-03: Visualization Preparation | Graph formatted for D3/Cytoscape | - |

### KG-02 Output Specification

KG-02 must produce the following files:

```
data/output/kg_v1/
├── nodes/
│   ├── topics.jsonl          # Topic nodes (LO + AG only for KG-02 baseline)
│   ├── subcategories.jsonl   # Subcategory nodes (math.LO, math.AG)
│   └── periods.jsonl         # Period nodes
├── edges/
│   ├── contains_topic.jsonl  # CONTAINS_TOPIC edges
│   ├── active_in.jsonl       # ACTIVE_IN edges
│   ├── neighbor_of.jsonl     # NEIGHBOR_OF edges
│   ├── parent_of.jsonl       # PARENT_OF edges (from hierarchy)
│   └── evolves_to.jsonl      # EVOLVES_TO edges with evidence annotations
├── metadata.json             # Graph metadata (version, coverage, stats)
└── validation_report.json    # Schema validation results
```

**KG-02 "Done" Definition:**
- [x] All node files validate against Node Schema
- [x] All edge files validate against Edge Schema
- [x] LO benchmark cases correctly encoded as edge annotations (4 encodable of 13 documented)
- [x] AG benchmark cases correctly encoded as edge annotations (5 of 5 encodable)
- [x] `metadata.json` contains accurate coverage statistics (32 topics, 181 edges)
- [x] Validation report shows 0 schema errors
- [x] At least one example subgraph can be extracted and verified

**Evidence Level Verification:**
- Confirmed edges (LO/AG benchmark): Must have `benchmark_case_id` and `benchmark_status`
- Data-derived edges: Must have `evidence_type: "data-derived"` (no benchmark metadata)
- **Post-fix note**: 9 evolves_to edges encoded (not 18) - this is the hierarchy-scoped baseline, not a regression. Only cases where both topics are in the hierarchy's topic_assignments can be encoded.

**Deferred to 2C (Conditional PR Integration):**
- PR topic nodes and provisional subcategory metadata
- PR inferred `EVOLVES_TO` edges with `inference_basis`
- PR-specific `review_flags: ["needs_curation"]`

**Exit Criteria:**
- Graph export produces valid JSONL + metadata files under `data/output/kg_v1/`
- All encodable LO/AG benchmark cases correctly encoded (9 total: 4 LO + 5 AG)
- 63 neighbor_of edges using real graph adjacency (not clique-generated)
- PR is explicitly excluded from KG-02 baseline output and reserved for conditional Phase 2C
- 74 tests passing

## Residual Risk

| Risk | Mitigation |
|------|------------|
| Evidence level confusion | Explicit `confidence` field on all edges |
| Provisional data treated as confirmed | Subcategory status check required |
| PR cases never materialize | Can remain provisional or be excluded |
| Schema too complex for visualization | Keep v1 simple, iterate based on needs |
| QA/RA data improves | Can add to v2 with clear version distinction |

## Next Recommendation

### Phase 2 Status Update

| Phase | Task | Status | Deliverable |
|-------|------|--------|-------------|
| 2A | KG-02: Graph Export Implementation | ✅ Complete | JSON graph files for LO + AG confirmed graph |
| 2B | MPR-01C: PR-Targeted Extraction | ⏸️ On Hold | PR-specific cases (conditional) |
| 2C | Conditional: PR Graph Integration | 🟡 Planning Complete (PR-2C) | Add PR to graph — conditional layer only; Gate 2 required for baseline |
| 3 | KG-03: Visualization Preparation | ✅ Complete | Frontend-ready bundle format (5 files, 56 tests) |

### Immediate Next Step: KG-04 Frontend Integration

**Options:**

#### Option A: KG-04 Frontend Integration (Recommended)
Implement frontend data loading and visualization components using the KG-03 bundle format.

**Prerequisites:**
- KG-03 bundle format documented ✅
- Frontend framework selected (D3.js/Cytoscape.js)

**Deliverables:**
- `pipeline/math_kg_viz_bundle.py` - Bundle creation script
- `data/output/kg_v1_visualization/` - Frontend-ready bundles
- Frontend components for graph visualization

#### Option B: MPR-01C PR-Targeted Extraction (Conditional)
Execute PR-specific candidate extraction to potentially enable PR integration in Phase 2C.

**Prerequisites:**
- PR extraction prioritized over frontend
- Resource available for parallel track

**Deliverables:**
- PR-specific evolution cases (>=3 for integration)
- Phase 2C integration plan

### Decision Criteria

| Condition | Recommendation |
|-----------|---------------|
| Frontend team ready | **KG-04** - Proceed with visualization |
| Need PR for completeness | **MPR-01C** - Parallel extraction |
| PR extraction successful | **Phase 2C** - Conditional integration |
| Bundle validation issues | **KG-02-fix** - Fix export first |

### Files Reference

| Package | File | Purpose |
|---------|------|---------|
| KG-02 | `pipeline/math_kg_export.py` | Graph export implementation |
| KG-02 | `docs/plans/evolution-ops/13-math-kg-export-package.md` | KG-02 task package |
| KG-03 | `docs/plans/evolution-ops/14-math-kg-visualization-package.md` | KG-03 task package |

## Data Baseline Reference

**Math Subdomain Summary (from worktree 2124, verified 2026-03-19):**

| Subdomain | Topics | Multi-period | Eligible Anchors | Status |
|-----------|--------|--------------|------------------|--------|
| math.LO   | 15     | 3            | 3                | ready |
| math.AG   | 17     | 3            | 3                | ready |
| math.PR   | 29     | 12           | 11               | provisional |
| math.QA   | 0      | 0            | 0                | gap |
| math.RA   | 3      | 0            | 0                | gap |
| math.RT   | 5      | 0            | 0                | not assessed |
| **Total** | **69** | **18**       | **17**           | - |

**KG-02 Export Baseline (Post-Fix):**

| Metric | Count | Notes |
|--------|-------|-------|
| Total topics exported | 32 | 15 LO + 17 AG (hierarchy topic_assignments as source-of-truth) |
| neighbor_of edges | 63 | Real graph adjacency (not clique-generated) |
| evolves_to edges | 9 | Hierarchy-scoped baseline: 4 LO + 5 AG cases |
| Tests passing | 74 | Full test coverage |

**Note:** Previous documentation incorrectly listed math.LO as 29 topics/5 multi-period and math.PR as 30 topics/13 multi-period. The corrected counts above are verified from the current worktree snapshot, using `aligned_topics_hierarchy.json` for subdomain assignment and `active_periods` counts. The KG-02 export uses hierarchy `topic_assignments` as the authoritative source, which yields 15 LO topics (not 29 from trends subcategory).

**Bootstrap Export Results:**
- Command: `python3 pipeline/evolution_analysis.py --input data/output/aligned_topics_hierarchy.json --output-dir data/output/math_kg_bootstrap --max-cases 20 --category-filter math`
- Output: 20 math cases
- PR cases: 1 explicit (global_39)

## Change Log

- **2026-03-19**: PKG-MATH-KG-01 complete - Schema and bootstrap design finalized
- **2026-03-19**: Updated coverage table with verified counts from topic_graph.json
- **2026-03-19**: Added Source-to-Canonical Mapping section
- **2026-03-19**: Clarified benchmark case representation (edge annotation only)
- **2026-03-19**: Added KG-02 output specification and "done" definition
- **2026-03-19**: KG-02 complete - Graph export implementation with 32 topics, 181 edges, 9 benchmark cases
- **2026-03-19**: KG-02-fix applied - Fixed topic source, neighbor adjacency, test infrastructure
- **2026-03-19**: KG-03 complete - Visualization preparation layer with 5 bundle files
- **2026-03-19**: KG-03-fix applied - Exporter coverage corrected, canonical `code` preserved, 56 tests passing
