doc_type: "documentation_update_plan"
scope: "PKG-MATH-KG-01-fix doc-agent deliverable"
status: "ready_for_implementation"
owner: "doc-agent"
source_of_truth: true
upstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-19-math-knowledge-graph.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/12-math-knowledge-graph-package.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-19-math-kg-coverage-scope.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-18-math-pr-benchmark.md"
downstream_docs: []
last_reviewed: "2026-03-19"
package_id: "PKG-MATH-KG-01-fix"
---

# PKG-MATH-KG-01-fix Documentation Update Plan

## Summary

This document consolidates corrections from all verification agents and provides a structured update plan for the two primary PKG-MATH-KG-01 documents.

## Documents to Update

1. `docs/plans/2026-03-19-math-knowledge-graph.md` (Design Document)
2. `docs/plans/evolution-ops/12-math-knowledge-graph-package.md` (Package Document)

## Corrections from Verification Agents

### 1. Coverage Correction (coverage-agent)

**Source:** `2026-03-18-math-pr-benchmark.md`, `2026-03-19-math-kg-coverage-scope.md`

| Metric | Current (Wrong) | Corrected | Affected Files |
|--------|-----------------|-----------|----------------|
| math.LO multi-period | 5 | **3** | Both docs |
| math.PR multi-period | 13 | **12** | Both docs |
| math.PR eligible anchors | 11 | **6** | Both docs |
| math.PR total topics | 30 | **29** | Both docs |

**Data Source Note to Add:**
```
Data sourced from `aligned_topics_hierarchy.json` using `active_periods` or `history` fields.
Verification commands available in `2026-03-18-math-pr-benchmark.md`.
```

### 2. Scope Clarification (scope-agent)

**New Section to Add:** "Core Graph vs Background Math Structure"

**Content Outline:**
```markdown
## Core Graph vs Background Math Structure

### Core Graph (v1 Scope)
- Nodes: Topics from LO + AG + PR(subset) with explicit evidence
- Edges: Only evidence-annotated evolution relationships
- Purpose: Demonstrate verified topic evolution patterns

### Background Math Structure
- Full topic_graph.json with all math subdomains
- Includes single-period topics (no evolution evidence)
- Available for future expansion but not part of v1 knowledge graph

### Key Distinction
v1 is NOT a "full-math graph". It is a curated subgraph containing only
topics with temporal evolution evidence at specified confidence levels.
```

### 3. Schema Consistency (schema-agent)

**Verification Required:** Ensure benchmark_case representation is consistent

**Current State:** Documents already specify edge annotation approach
**Action:** Verify no document mentions benchmark_case as standalone nodes

**Consistency Checklist:**
- [ ] All `EVOLVES_TO` edges with benchmark evidence use edge annotations
- [ ] No mention of `BenchmarkCase` or `EvolutionCase` as node types
- [ ] `benchmark_case_id` field only appears on edges, not nodes

### 4. Mapping Verification (mapping-agent)

**New Section to Add:** "Canonical Graph Names vs Source Export Fields"

**Content (already partially in design doc, needs formalization):**

```markdown
## Canonical Graph Names vs Source Export Fields

### Field Name Mapping

| Source Export Field | Canonical Graph Name | Direction Transform |
|--------------------|---------------------|---------------------|
| `belongs_to` | `CONTAINS_TOPIC` | Flip (Subcategory → Topic) |
| `active_in` | `ACTIVE_IN` | Direct (Topic → Period) |
| `adjacent_to` | `NEIGHBOR_OF` | Direct (undirected) |
| `evolves_from` | `EVOLVES_TO` | Flip (Anchor → Target) |
| `hierarchy_path` | `PARENT_OF` | Derive from path depth |
| `cross_category_moves` | `CROSS_CATEGORY_LINK` | Filter cross-category |

### Rationale for Direction Flips

1. **belongs_to → CONTAINS_TOPIC**: Container semantics (Subcategory contains Topic)
2. **evolves_from → EVOLVES_TO**: Temporal flow (Anchor evolves to Target)

### Example Transformations

```yaml
# belongs_to flip
Export:  {source: "global_56", target: "math.LO", type: "belongs_to"}
Graph:   {source: "math.LO", target: "global_56", type: "CONTAINS_TOPIC"}

# evolves_from flip
Export:  {source: "global_27", target: "global_56", type: "evolves_from"}
Graph:   {source: "global_56", target: "global_27", type: "EVOLVES_TO"}
```
```

### 5. Sanity Issues (sanity-agent)

**Confusing Statements to Fix:**

| Location | Current Confusing Text | Correction |
|----------|----------------------|------------|
| Design doc line 46 | "13 cases (5+, 6-, 2~)" | "13 cases total: 5 positive, 6 negative, 2 ambiguous" |
| Design doc line 282-283 | "11 benchmark cases (5+, 6-, 2~)" | "13 benchmark cases: 5 positive, 6 negative, 2 ambiguous" |
| Package doc line 409 | "LO benchmark cases (13 total: 5+, 5-, 2~)" | "LO benchmark cases (13 total: 5 positive, 6 negative, 2 ambiguous)" |

**Note:** math.LO actually has 5 positive + 6 negative + 2 ambiguous = 13 total cases.
The package doc line 409 says "5+, 5-, 2~" which is incorrect (should be 6 negative, not 5).

## Update Implementation Plan

### Phase 1: Coverage Corrections

**Files:** Both documents
**Changes:**
1. Update Scope table (math.LO multi-period: 5 → 3)
2. Update Scope table (math.PR multi-period: 13 → 12)
3. Update Scope table (math.PR eligible anchors: 11 → 6)
4. Update Scope table (math.PR total topics: 30 → 29)
5. Update Data Baseline Reference table
6. Add data source verification note

### Phase 2: Content Additions

**Files:** Design document (2026-03-19-math-knowledge-graph.md)
**Changes:**
1. Add "Core Graph vs Background Math Structure" section after "Scope for v1"
2. Expand "Source-to-Canonical Mapping" section with formal field mapping table

**Files:** Package document (12-math-knowledge-graph-package.md)
**Changes:**
1. Add "Canonical Graph Names vs Source Export Fields" section
2. Reference design doc for detailed transformation rules

### Phase 3: Consistency Fixes

**Files:** Both documents
**Changes:**
1. Fix case count notation (use "positive/negative/ambiguous" instead of "+/-/~")
2. Verify benchmark_case representation consistency
3. Align PR data between documents

### Phase 4: Cross-Document Alignment

**Verification:**
1. Ensure both documents use same numbers for:
   - math.LO: 3 multi-period, 13 benchmark cases
   - math.AG: 3 multi-period, 6 benchmark cases (2+ 4-)
   - math.PR: 12 multi-period, 6 eligible anchors, 29 topics
2. Ensure both documents use same terminology:
   - "provisional" not "pre-skeleton"
   - "edge annotation" not "standalone node"
   - "inferred" not "candidate" (for evidence level)

## Document-Specific Changes

### Design Document (2026-03-19-math-knowledge-graph.md)

#### Section: Scope for v1 (lines 40-58)
**Current:**
```
| math.LO   | 29     | 5                 | 5                | ✅ Ready         | 13 cases (5+, 6-, 2~) |
| math.AG   | 17     | 3                 | 3                | ✅ Ready         | 5 cases (2+, 3-) |
| math.PR   | 30     | 13                | 11               | ⚠️ Provisional   | Structure confirmed, cases inferred |
```

**Updated:**
```
| math.LO   | 29     | 3                 | 3                | ✅ Ready         | 13 cases: 5 positive, 6 negative, 2 ambiguous |
| math.AG   | 17     | 3                 | 3                | ✅ Ready         | 6 cases: 2 positive, 4 negative |
| math.PR   | 29     | 12                | 6                | ⚠️ Provisional   | Structure confirmed, cases inferred |
```

#### Section: Data Baseline Reference (lines 573-583)
**Current:**
```
| math.LO   | 29     | 5            | 5                | ready |
| math.AG   | 17     | 3            | 3                | ready |
| math.PR   | 30     | 13           | 11               | provisional |
```

**Updated:**
```
| math.LO   | 29     | 3            | 3                | ready |
| math.AG   | 17     | 3            | 3                | ready |
| math.PR   | 29     | 12           | 6                | provisional |
```

#### New Section: After line 58
Insert "Core Graph vs Background Math Structure" section

### Package Document (12-math-knowledge-graph-package.md)

#### Section: KG-02 Prerequisites Summary / Success Criteria (lines 407-413)
**Current:**
```
- [ ] LO benchmark cases (13 total: 5+, 5-, 2~) encoded as edge annotations
```

**Updated:**
```
- [ ] LO benchmark cases (13 total: 5 positive, 6 negative, 2 ambiguous) encoded as edge annotations
```

#### New Section: After line 377
Insert "Canonical Graph Names vs Source Export Fields" section

## Verification Checklist

After updates, verify:

- [ ] Both documents have consistent coverage numbers
- [ ] math.LO multi-period = 3 (not 5)
- [ ] math.PR multi-period = 12 (not 13)
- [ ] math.PR eligible anchors = 6 (not 11)
- [ ] math.PR total topics = 29 (not 30)
- [ ] "Core Graph vs Background Math Structure" section exists in design doc
- [ ] "Canonical Graph Names vs Source Export Fields" section exists in both docs
- [ ] Case counts use "positive/negative/ambiguous" terminology
- [ ] No benchmark_case standalone node references
- [ ] Data source note added

## Out of Scope (Explicitly Excluded)

Per PKG-MATH-KG-01-fix requirements, DO NOT:
- Modify pipeline code
- Modify tests
- Modify backlog
- Modify registry
- Expand scope to KG-02 implementation

## References

- Coverage data source: `2026-03-18-math-pr-benchmark.md`
- Coverage scope: `2026-03-19-math-kg-coverage-scope.md`
- LO benchmark: `2026-03-12-math-lo-benchmark.md`
- AG benchmark: `2026-03-17-math-ag-benchmark.md`
