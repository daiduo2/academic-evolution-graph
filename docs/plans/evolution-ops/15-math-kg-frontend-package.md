# KG-04: Math Knowledge Graph Frontend Integration Package

## Status: COMPLETED ✅

**Commit**: `bfcc6e9` on `codex/topic-evolution-analysis`
**Date**: 2026-03-19

---

## Package Goal

First version of Math Knowledge Graph v1 visualization page — browsable LO+AG baseline graph in the existing React frontend.

## Scope

- New route `/knowledge-graph` added to existing React app
- Data loaded from `data/output/kg_v1_visualization/graph_bundle.json`
- D3 force-directed graph with filters and topic detail panel
- Timeline summary view (Recharts bar chart)
- No PR, no backend, no graph database

## Files Created

| File | Purpose |
|------|---------|
| `frontend/src/hooks/useKnowledgeGraph.js` | Data loader hook — fetches graph_bundle.json |
| `frontend/src/views/KnowledgeGraph.jsx` | Main page — 3-column layout |
| `frontend/src/components/GraphVisualization.jsx` | D3 force-directed graph |
| `frontend/src/components/GraphFilters.jsx` | Filter panel (subcategory / edge kind / confidence) |
| `frontend/src/components/TopicDetail.jsx` | Topic detail sidebar |
| `frontend/src/components/TimelineSummary.jsx` | Timeline bar chart (Recharts) |

## Files Modified

| File | Change |
|------|--------|
| `frontend/src/App.jsx` | Added import, NavLink, and Route for `/knowledge-graph` |

## Data Contract

Frontend loads `graph_bundle.json` from:
```
frontend/public/data/output/kg_v1_visualization/graph_bundle.json
```

> Note: `frontend/public/data/` is in `.gitignore` (generated data).
> Run `make pipeline` or manually copy from `data/output/kg_v1_visualization/` before serving.

### Raw KG-03 bundle shape

```json
{
  "nodes": {
    "topics": [...],         // topic nodes with subcategory, keywords, display_size, etc.
    "subcategories": [...],  // subcategory nodes with code field (math.LO, math.AG)
    "periods": [...]         // time period nodes
  },
  "edges": {
    "by_kind": {
      "NEIGHBOR_OF": [...],
      "PARENT_OF": [...],
      "EVOLVES_TO": [...]
    }
  },
  "filters": {
    "subcategories": ["math.LO", "math.AG"],
    "edge_kinds": ["NEIGHBOR_OF", "PARENT_OF", "EVOLVES_TO"],
    "confidence_levels": ["confirmed", "ambiguous", "negative", "data-derived"]
  },
  "stats": { "totalTopics": N, "subcategoryCount": N, ... }
}
```

### Frontend adapter shape

`useKnowledgeGraph()` normalizes the raw KG-03 filter arrays into UI-friendly option objects before passing them to React components:

```json
{
  "filters": {
    "subcategories": [
      { "value": "math.LO", "code": "math.LO", "label": "Logic" },
      { "value": "math.AG", "code": "math.AG", "label": "Algebraic Geometry" }
    ],
    "edgeKinds": [
      { "value": "NEIGHBOR_OF", "label": "相邻主题" },
      { "value": "PARENT_OF", "label": "层级关系" },
      { "value": "EVOLVES_TO", "label": "演化关系" }
    ],
    "confidenceLevels": [
      { "value": "confirmed", "label": "已确认", "color": "#22c55e" },
      { "value": "ambiguous", "label": "模糊", "color": "#f59e0b" },
      { "value": "negative", "label": "否定", "color": "#ef4444" }
    ]
  }
}
```

## Feature Summary

### Graph Visualization (D3)
- Force-directed layout with zoom/pan/drag
- Node color = subcategory (LO=blue, AG=green, NT=pink, RA=purple, ...)
- Node size = `display_size` field from bundle
- Edge width = edge kind (EVOLVES_TO=3px, PARENT_OF=2px, NEIGHBOR_OF=1px dashed)
- Edge color = confidence (confirmed=green, ambiguous=amber, negative=red)
- Labels shown for nodes with `display_size > 25` or selected

### Filters
- Subcategory: all / LO / AG / ...
- Edge kinds: NEIGHBOR_OF / PARENT_OF / EVOLVES_TO (checkboxes)
- Confidence: confirmed / ambiguous / negative (checkboxes)
- Reset button

### Topic Detail Panel
- Label, ID, subcategory badge
- active_periods, total_papers stats
- Keywords (up to 10, with "+N more")
- Hierarchy path
- Outgoing/incoming edges (up to 5 each)

### Timeline Summary
- BarChart with active_topic_count and benchmark_edge_count per period
- Summary stats: total topics, total edges, period count

## Verification

```bash
# Tests pass
npm --prefix frontend test -- --run
# → 4 passed

# Build passes
npm --prefix frontend run build
# → ✓ built in ~1.3s (chunk size warning is non-blocking)
```

## Done Criteria — All Met ✅

- [x] 前端可加载 KG-03 bundle (`useKnowledgeGraph` fetches graph_bundle.json)
- [x] 页面可展示 LO+AG 图谱 (D3 GraphVisualization)
- [x] 至少支持 subcategory / edge kind / confidence 的过滤 (GraphFilters)
- [x] 至少支持 topic 选中后的详情查看 (TopicDetail)
- [x] 构建通过 (vitest 4/4, vite build success)

## Post-Fix Notes (KG-04-fix)

Three issues discovered after initial KG-04 commit were resolved in the `KG-04-fix` branch:

### 1. Filter contract normalization (`useKnowledgeGraph.js`)

KG-03 bundle ships raw filter arrays (`subcategories: string[]`, `edge_kinds: string[]`, `confidence_levels: string[]`). The hook now normalizes these in-place before returning:

- `filters.subcategories` → `[{value, code, label}]`
- `filters.edgeKinds` → `[{value, label}]`
- `filters.confidenceLevels` → `[{value, label, color}]`

Components (`GraphFilters`, `GraphVisualization`) consume the normalized shape; no raw string arrays are passed to the view layer.

### 2. `useSubcategory` canonical code fix (`useKnowledgeGraph.js`)

`useSubcategory("math.LO")` was returning no topics because topic records store the short-form code (`"LO"`, `"AG"`) in `t.subcategory`, but the hook was comparing against the full `"math.LO"` string. Fix: normalize the input by stripping the `"math."` prefix before comparison.

### 3. `TimelineSummary` mounted (`KnowledgeGraph.jsx`)

`TimelineSummary` component existed but was never rendered. Fix:

- Added `TimelineSummary` import
- Added `useEffect` + `useState` to load `timeline_summary.json` from the public data path
- Mounted `<TimelineSummary>` as a full-width row after the 3-column graph grid, before the help text

### Verification

All 4 vitest tests pass. Vite build passes (chunk size warning is non-blocking).
