---
doc_type: "task_package_detail"
package_id: "KG-03"
owner: "rule-worker"
tree_path: "math knowledge graph"
task_type: "visualization_preparation_layer"
target_rule:
  - "math historical topic evolution graph"
  - "visualization data bundle"
goal: "Create visualization-preparation layer for Math KG v1: transform kg_v1/ into frontend-ready bundle format"
status: "completed"
---

# KG-03: Math Knowledge Graph Visualization Preparation

## Purpose

KG-03 is the **visualization-preparation layer** that transforms the raw KG v1 export (`data/output/kg_v1/`) into a frontend-ready bundle format. It is **NOT** the final visualization implementation, but rather the data transformation step that prepares optimized, validated data bundles for frontend consumption.

## Critical Distinctions

### What KG-03 IS
- A **data transformation layer** that converts raw graph files into optimized bundles
- A **validation gate** ensuring data integrity before frontend handoff
- A **contract definition** specifying input/output formats for the visualization pipeline

### What KG-03 IS NOT
- **NOT** the final visualization implementation (no D3/Cytoscape rendering code)
- **NOT** a graph database layer (no Neo4j/PostgreSQL persistence)
- **NOT** a real-time update system (batch processing only)

## Scope

### Included Subdomains
| Subdomain | Status | Topics | Rationale |
|-----------|--------|--------|-----------|
| math.LO | ready | 15 | Confirmed baseline with benchmark annotations |
| math.AG | ready | 17 | Confirmed baseline with benchmark annotations |

### Explicitly Excluded
| Subdomain | Status | Rationale |
|-----------|--------|-----------|
| math.PR | provisional | **Deferred to Phase 2C** - requires MPR-01C PR-targeted extraction first |
| math.QA | gap | No multi-period topics available |
| math.RA | gap | No multi-period topics available |
| math.RT | not assessed | Not evaluated yet |

**Note:** PR is intentionally excluded from KG-03. The decision to integrate PR is conditional on MPR-01C completion and will be handled in Phase 2C, not here.

## Input Contract

### Source Directory: `data/output/kg_v1/`

```
kg_v1/
├── nodes/
│   ├── topics.jsonl         # 32 topics (15 LO + 17 AG)
│   ├── subcategories.jsonl  # math.LO, math.AG
│   └── periods.jsonl        # 13 periods (2025-02 to 2026-02)
├── edges/
│   ├── contains_topic.jsonl # 32 edges
│   ├── active_in.jsonl      # 55 edges
│   ├── neighbor_of.jsonl    # 63 edges
│   ├── parent_of.jsonl      # 22 edges
│   └── evolves_to.jsonl     # 9 edges with benchmark annotations
├── metadata.json            # Coverage stats and version info
└── validation_report.json   # Schema validation results
```

### Input Validation Requirements
- [ ] `metadata.json` exists and has `status: "valid"`
- [ ] `validation_report.json` has `schema_errors: []`
- [ ] All 10 expected files are present
- [ ] Topic count matches metadata (32)
- [ ] Edge counts match metadata (181 total)

## Output Contract

### Target Directory: `data/output/kg_v1_visualization/`

```
kg_v1_visualization/
├── graph_bundle.json        # Main aggregated bundle (optimized for frontend)
├── subgraph_lo.json         # LO-only subgraph
├── subgraph_ag.json         # AG-only subgraph
├── timeline_summary.json    # Period-based activity summary
└── legend.json              # Schema definitions for frontend
```

### Bundle Format Specification

#### graph_bundle.json Structure
```json
{
  "version": "kg_v1_visualization",
  "generated_at": "ISO-8601 timestamp",
  "source": "data/output/kg_v1",
  "nodes": {
    "topics": [...],           # 32 topics with display attrs
    "subcategories": [...],    # 2 subcategories
    "periods": [...],          # 13 periods
    "total": 47
  },
  "edges": {
    "all": [...],              # 181 edges with display attrs
    "by_kind": {
      "CONTAINS_TOPIC": [...], # 32 edges
      "ACTIVE_IN": [...],      # 55 edges
      "NEIGHBOR_OF": [...],    # 63 edges
      "PARENT_OF": [...],      # 22 edges
      "EVOLVES_TO": [...]      # 9 edges
    },
    "total": 181
  },
  "filters": {
    "subcategories": ["math.LO", "math.AG"],
    "edge_kinds": [...],
    "confidence_levels": ["confirmed", "negative", "ambiguous"],
    "periods": ["2025-02", ...]
  },
  "stats": {
    "topic_count": 32,
    "subcategory_count": 2,
    "period_count": 13,
    "edge_count": 181,
    "evolves_to_count": 9,
    "evolves_to_by_confidence": {
      "confirmed": 4,
      "negative": 4,
      "ambiguous": 1
    }
  }
}
```

#### Node Display Attrs
```json
{
  "id": "global_56",
  "label": "直觉主义逻辑证明",
  "kind": "topic",
  "subcategory": "LO",
  "status": "persistent",
  "display_size": 18.5,
  "active_periods": 4,
  "total_papers": 42,
  "keywords": ["直觉主义", "证明论", ...],
  "hierarchy_depth": 2
}
```

#### Edge Display Attrs
```json
{
  "source": "global_56",
  "target": "global_27",
  "kind": "EVOLVES_TO",
  "evidence_type": "benchmark-confirmed",
  "confidence": "confirmed",
  "benchmark_status": "positive",
  "benchmark_case_id": "lo-b1",
  "expected_relation": "math_lo_modal_continuity",
  "subcategory": "math.LO",
  "display_weight": 3.0
}
```

#### Subgraph Files

**math_lo.json** (LO-only subgraph):
```json
{
  "subcategory": "math.LO",
  "topics": [...],           // 15 LO topics
  "evolution_edges": [...],  // LO evolves_to edges
  "neighbor_edges": [...],   // LO-LO neighbor edges
  "cross_subcategory_edges": [...] // LO-AG neighbor edges
}
```

**evolution_paths.json** (Benchmark-confirmed paths):
```json
{
  "paths": [
    {
      "path_id": "lo-b1-path",
      "source": "global_56",
      "target": "global_27",
      "edges": ["global_56 -> global_27"],
      "benchmark_case_id": "lo-b1",
      "confidence": "confirmed"
    }
  ]
}
```

## Transformation Operations

### 1. Data Consolidation
- Merge split JSONL files into unified bundle structure
- Deduplicate any overlapping entries
- Preserve all metadata from source files

### 2. Index Generation
- Create topic ID -> file location mapping
- Build subcategory -> topic list index
- Generate period -> active topics index

### 3. Subgraph Extraction
- Extract LO-only subgraph
- Extract AG-only subgraph
- Identify cross-subcategory neighbor edges

### 4. Evolution Path Compilation
- Compile all benchmark-confirmed evolution paths
- Annotate with confidence levels
- Flag provisional/inferred edges (none in KG-03 baseline)

### 5. Validation
- Verify bundle integrity against source
- Check all references resolve
- Validate JSON schema compliance

## Done When

- [x] `graph_bundle.json` created with consolidated graph data
- [x] `subgraph_lo.json` created with LO-only subgraph
- [x] `subgraph_ag.json` created with AG-only subgraph
- [x] `timeline_summary.json` created with period-based summary
- [x] `legend.json` created with schema definitions
- [x] All benchmark cases from kg_v1 preserved in bundle
- [x] No PR data accidentally included (LO + AG only)
- [x] Documentation updated with bundle format spec
- [x] `pipeline/math_kg_visualization_export.py` implemented
- [x] `tests/test_math_kg_visualization_export.py` created (42 tests)
- [x] Frontend contract documented with field clarifications

## Stop Conditions

- [ ] Need to modify `pipeline/math_kg_export.py` - STOP, belongs in KG-02
- [ ] Need to add PR data to output - STOP, belongs in Phase 2C
- [ ] Need to implement D3/Cytoscape rendering - STOP, belongs in frontend
- [ ] Source kg_v1 data fails validation - STOP, fix KG-02 first

## Verification Commands

```bash
# Step 1: Ensure KG-02 baseline exists
python3 pipeline/math_kg_export.py \
  --input data/output/aligned_topics_hierarchy.json \
  --benchmark-lo docs/plans/2026-03-12-math-lo-benchmark.md \
  --benchmark-ag docs/plans/2026-03-18-math-ag-benchmark.md \
  --output-dir data/output/kg_v1

# Step 2: Generate visualization bundle
python3 pipeline/math_kg_visualization_export.py \
  --input-dir data/output/kg_v1 \
  --output-dir data/output/kg_v1_visualization

# Step 3: Run tests
pytest tests/test_math_kg_visualization_export.py -q
```

## Verification Output

```
Building visualization bundle...
  Created graph_bundle.json (32 topics, 181 edges)
  Created subgraph_lo.json (15 topics, 4 evolves_to)
  Created subgraph_ag.json (17 topics, 5 evolves_to)
  Created timeline_summary.json (13 periods)
  Created legend.json

Visualization export complete!
Output directory: data/output/kg_v1_visualization
Total nodes: 47
Total edges: 181
EVOLVES_TO edges: 9
```

## Next Recommendation

### Option A: KG-04 Frontend Integration (Recommended)
If bundle creation is successful and validated:
- Implement frontend data loading from bundle format
- Create D3/Cytoscape visualization components
- Build interactive evolution path explorer

### Option B: MPR-01C PR-Targeted Extraction (Conditional)
If PR integration is prioritized:
- Execute PR-specific candidate extraction
- Surface explicit PR evolution cases
- Enable Phase 2C conditional PR integration

### Decision Criteria

| Condition | Recommendation |
|-----------|---------------|
| Bundle validation passes | Proceed to KG-04 |
| Frontend team ready | Proceed to KG-04 |
| PR cases needed for completeness | Execute MPR-01C in parallel |
| PR extraction successful (>=3 cases) | Phase 2C: PR Graph Integration |

## Relationship to Other Packages

```
KG-01 (Schema Design)
    ↓
KG-02 (Export Implementation) → data/output/kg_v1/
    ↓
KG-03 (Visualization Prep)   → data/output/kg_v1_visualization/  [YOU ARE HERE]
    ↓
KG-04 (Frontend Integration) → D3/Cytoscape visualization

Parallel Track:
MPR-01C (PR Extraction) → Phase 2C (Conditional PR Integration)
```

## Frontend Bridge Recommendation

### Current Frontend Pattern
The frontend uses `useData.js` and `useDomainData.js` to load data:
- Multiple JSON files fetched separately
- Client-side data merging

### KG-03 Recommendation

**Use `graph_bundle.json` as single entry point:**

```javascript
// Recommended: hooks/useKnowledgeGraph.js
export function useKnowledgeGraph() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch(`${basePath}data/output/kg_v1_visualization/graph_bundle.json`)
      .then(r => r.json())
      .then(setData);
  }, []);

  return {
    topics: data?.nodes?.topics,
    subcategories: data?.nodes?.subcategories,
    edges: data?.edges?.by_kind?.EVOLVES_TO,
    filters: data?.filters,
    stats: data?.stats
  };
}
```

**Advantages:**
- Single HTTP request
- Pre-computed display attrs
- Filter metadata included
- Subgraph files available for focused views

### Files for Frontend

| File | Purpose | Size |
|------|---------|------|
| `graph_bundle.json` | Main entry - all data | ~110KB |
| `subgraph_lo.json` | LO-focused view | ~19KB |
| `subgraph_ag.json` | AG-focused view | ~22KB |
| `legend.json` | Schema reference | ~3KB |

### Extended View-Model Specifications

#### Display Size Calculation

Topics are sized based on paper count with multipliers for anchor/benchmark status:

```javascript
// Base size from paper count (logarithmic scale)
const baseSize = Math.log10(total_papers + 1) * 5 + 5;  // Range: 5-25px

// Multipliers
const anchorMultiplier = status.is_anchor ? 1.3 : 1.0;
const benchmarkMultiplier = status.is_benchmark ? 1.2 : 1.0;

// Final size
const display_size = Math.round(baseSize * anchorMultiplier * benchmarkMultiplier);
```

**Size Categories:**
| Papers | Base Size | +Anchor | +Benchmark | Both |
|--------|-----------|---------|------------|------|
| 1-10   | 10px      | 13px    | 12px       | 16px |
| 11-50  | 15px      | 20px    | 18px       | 23px |
| 51-100 | 20px      | 26px    | 24px       | 31px |
| 100+   | 25px      | 33px    | 30px       | 39px |

#### Color Scheme

```javascript
const COLOR_SCHEME = {
  subcategories: {
    "math.LO": "#3b82f6",    // Blue
    "math.AG": "#10b981"     // Green
  },
  status: {
    anchor: "#f59e0b",        // Amber border for anchors
    benchmark: "#ef4444",     // Red badge for benchmark
    evolution_source: "#8b5cf6", // Purple for evolution source
    evolution_target: "#ec4899"  // Pink for evolution target
  }
};
```

#### Edge Display Weights

**NEIGHBOR_OF Weight:**
```javascript
const normalizedWeight = Math.ceil(source_weight * 5);
const displayWeight = Math.max(1, Math.min(5, normalizedWeight));
const opacity = 0.3 + (displayWeight / 5) * 0.5;  // 0.3-0.8 range
```

**EVOLVES_TO Weight:**
```javascript
const CONFIDENCE_WEIGHTS = {
  "confirmed": 5,
  "ambiguous": 3,
  "negative": 2
};
const displayWeight = CONFIDENCE_WEIGHTS[evidence.confidence];
```

#### Evidence Badge Specification

| Case Type | Prefix | Badge | Shape | Color |
|-----------|--------|-------|-------|-------|
| Positive | lo-b1, ag-b1 | B1, B2 | Circle | Green (#10b981) |
| Negative | lo-n1, ag-n1 | N1, N2 | Circle | Red (#ef4444) |
| Ambiguous | lo-a1, ag-a1 | A1, A2 | Diamond | Amber (#f59e0b) |

#### Filter Dimensions

The bundle includes pre-defined filter dimensions:

```javascript
{
  dimensions: [
    { id: "subcategory", type: "select", options: ["math.LO", "math.AG"], multi: true },
    { id: "topic_mode", type: "select", options: ["persistent", "transient"], multi: true },
    { id: "benchmark_status", type: "select", options: ["positive", "negative", "ambiguous", "none"], multi: true },
    { id: "anchor_status", type: "boolean", default: false },
    { id: "period", type: "range", range: { min: "2025-01", max: "2025-12" } },
    { id: "paper_count", type: "range", range: { min: 0, max: 500 } },
    { id: "edge_types", type: "select", options: ["PARENT_OF", "NEIGHBOR_OF", "EVOLVES_TO"], multi: true }
  ],
  presets: [
    { id: "all", label: "Show All" },
    { id: "benchmark_only", label: "Benchmark Cases Only" },
    { id: "anchors_only", label: "Anchor Topics" },
    { id: "evolution_positive", label: "Positive Evolution" }
  ]
}
```

#### Performance Considerations

**Bundle Size Estimates:**
| Component | Estimated Size | Gzipped |
|-----------|---------------|---------|
| Nodes (32 topics) | ~15KB | ~3KB |
| Edges (~400) | ~30KB | ~6KB |
| Indices | ~10KB | ~2KB |
| Views | ~5KB | ~1KB |
| **Total** | **~65KB** | **~12KB** |

**Rendering Optimization:**
```javascript
// Level-of-detail rendering
function getNodeDetailLevel(zoom) {
  if (zoom < 0.5) return 'minimal';    // Just dots
  if (zoom < 1.0) return 'basic';      // Name only
  return 'full';                        // Name + badges
}

// Edge visibility threshold
const visibleEdges = edges.filter(e => e.display.weight >= minWeightThreshold);
```

## Frontend Contract (Fixed)

### Subcategory Node Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `id` | string | Unique identifier | "math.LO" |
| `code` | string | **Canonical code (use this for filtering)** | "math.LO" |
| `subcategory` | string | Short code | "LO" |
| `label` | string | Display name | "Logic" |
| `name` | string | Full name | "Logic in Computer Science" |
| `discipline` | string | Parent discipline | "math" |
| `topic_count` | int | Total topics | 15 |
| `multi_period_count` | int | Multi-period topics | 3 |
| `status` | string | "ready" \| "provisional" \| "gap" | "ready" |

### Field Usage Guide for Frontend

**For filtering by subcategory:**
```javascript
// CORRECT: Use 'code' field for filtering
const loTopics = topics.filter(t => t.subcategory_code === "math.LO");

// INCORRECT: Do not use 'id' for filtering logic
// (id may have different format in some contexts)
```

**For display purposes:**
```javascript
// Use 'label' for short display
// Use 'name' for full display
const displayName = subcategory.label; // "Logic"
const fullName = subcategory.name;     // "Logic in Computer Science"
```

**Relationship between fields:**
- `id` and `code` are typically the same (e.g., "math.LO")
- `subcategory` is the short form (e.g., "LO")
- `code` is the canonical field for all filtering operations
- `id` is the unique identifier for node references

### Topic Node Fields (Relevant for Subcategory)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `subcategory` | string | Short subcategory code | "LO" |
| `subcategory_code` | string | **Full canonical code** | "math.LO" |
| `category` | string | Parent category | "math" |

## Change Log

- **2026-03-19**: KG-03 completed
  - `pipeline/math_kg_visualization_export.py` implemented
  - `tests/test_math_kg_visualization_export.py` (42 tests) created
  - 5 bundle files generated
  - PR correctly excluded from bundle
  - Documentation updated with actual format spec
- **2026-03-19 (fix)**: Frontend contract documented
  - Clarified `code` is the canonical field for filtering
  - Documented relationship between `id`/`code`/`subcategory` fields
  - Added field usage guide for frontend developers
