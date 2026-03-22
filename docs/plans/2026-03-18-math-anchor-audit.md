doc_type: "governance"
scope: "math anchor selection criteria review"
status: "completed"
owner: "trend-monitor"
source_of_truth: true
upstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-18-math-data-audit.md"
downstream_docs: []
last_reviewed: "2026-03-18"

# Math Anchor Selection Audit Report

## Executive Summary

**Audit Date**: 2026-03-18
**Package**: PKG-MATH-AUDIT-02
**Status**: ✅ Completed

**Critical Finding**: The current worktree does not support a "graph has 0 edges" diagnosis. Math already has a meaningful eligible anchor pool, but representative export and remaining filters still compress math visibility.

- **84 multi-period math topics** exist in the current worktree
- **60 multi-period math topics pass the current anchor filters**
- **Primary visibility bottleneck**: representative export (`--max-cases=12`) plus category rotation
- **Secondary bottleneck**: `papers >= 60` excludes 19 of the 84 multi-period math topics

**Note on totals**: PKG-MATH-AUDIT-01 reported 374/81 topics (26 subcats). This audit found 394/84 (29 subcats). The difference is 3 subcategories (AC, AT, CA) that were excluded from the representative table but exist in the data.

## Anchor Selection Criteria

Default criteria in `select_anchor_topics()`:

1. `total_papers >= 60`
2. `active_periods >= 2`
3. `neighbors >= 2`
4. `_eligible_start_period()` - must leave room for 4-month horizon

## Criteria Breakdown

### All Math Topics (394 total)

| Criteria | Passing | Percentage |
|----------|---------|------------|
| Papers >= 60 | 50 | 12.7% |
| Periods >= 2 | 84 | 21.3% |
| **Neighbors >= 2** | **368** | **93.4%** |
| Eligible start | 394 | 100.0% |
| **ALL criteria** | **60** | **15.2%** |

### Multi-Period Math Topics (84 total)

| Criteria | Passing | Percentage |
|----------|---------|------------|
| Papers >= 60 | 31 | 36.9% |
| Periods >= 2 | 84 | 100.0% |
| **Neighbors >= 2** | **84** | **100.0%** |
| Eligible start | 79 | **94.0%** |
| **ALL criteria** | **60** | **71.4%** |

## Multi-Period Loss Breakdown

Of 84 multi-period math topics:

- **60 pass all current filters**
- **19 fail paper count** (`papers < 60`)
- **5 fail eligible start period** (cannot leave room for the 4-month horizon)
- **0 fail because of neighbors** in the current worktree graph

### Filter Breakdown (Multi-Period Topics)

| Range | Count | Status |
|-------|-------|--------|
| Pass all filters | 60 | Eligible |
| Fail `papers >= 60` | 19 | Blocked by paper threshold |
| Fail `eligible_start_period` | 5 | Blocked by horizon/start-period requirement |

### Topics Just Below Paper Threshold (Top 10)

| Topic ID | Subcat | Papers | Would Qualify If... |
|----------|--------|--------|---------------------|
| global_51 | LO | 59 | paper threshold relaxed slightly |
| global_34 | GT | 59 | paper threshold relaxed slightly |
| global_12 | DS | 55 | paper threshold relaxed |
| global_271 | PR | 55 | paper threshold relaxed |
| global_72 | OC | 53 | paper threshold relaxed |
| global_211 | PR | 52 | paper threshold relaxed |
| global_94 | ST | 52 | paper threshold relaxed |
| global_56 | LO | 50 | paper threshold relaxed |
| global_156 | PR | 50 | paper threshold relaxed |
| global_50 | AP | 48 | paper threshold relaxed |

## Category Rotation Impact

Even when `max_cases=100` allows more math representation:

| Metric | Value |
|--------|-------|
| Math topics passing all criteria | 60 |
| Math cases in 100-case audit | 9 |
| Math cases in 12-case default | ~1 |

Math gets fair representation (~9%) in the expanded audit, but the default 12-case export still compresses math to roughly one visible representative.

The key effect of category rotation is:

- many math anchors are already eligible
- but the summary export intentionally spreads visibility across top-level categories
- so math is underrepresented in `evolution_cases.json` relative to its internal eligible anchor pool

## Subcategory Anchor Analysis

| Subcat | Total | Multi-Period | Pass All | Anchors in 100-case |
|--------|-------|--------------|----------|---------------------|
| AG | 17 | 3 | 3 | 1 |
| AP | 37 | 9 | 6 | 2 |
| CO | 47 | 7 | 1 | 1 |
| GR | 9 | 2 | 1 | 1 |
| NA | 36 | 7 | 5 | 1 |
| OC | 48 | 7 | 4 | 1 |
| PR | 29 | 12 | 8 | 1 |
| QA | 2 | 1 | 1 | 1 |
| ... | ... | ... | ... | ... |

**Note**: This is a representative slice. The current worktree data does not support the claim that neighbor filtering eliminates all math anchors.

## Root Cause Analysis

### The Real Problem: Export Compression, Not Empty Graph

**Critical finding**: The current worktree graph is not empty. It has adjacency edges, and math topics are already connected well enough to satisfy the neighbor requirement.

What is happening instead:

```
Math topics exist
         ↓
Many are single-period and therefore unusable for evolution
         ↓
A substantial subset of multi-period math topics still passes anchor filters
         ↓
Representative export uses max_cases=12 with category rotation
         ↓
Default visible math cases collapse to ~1 in evolution_cases.json
```

### Why 9 Math Cases Still Appear in 100-case Audit

The 9 math anchors in the 100-case audit show that math already has an eligible anchor pool.

What changes between 100-case and 12-case export is mainly visibility budget, not basic graph connectivity.

### Paper Count is the Real Filter

Among multi-period math topics:
- 60 pass all current filters
- 19 fail because of `papers < 60`
- 5 fail because of `eligible_start_period`

So if we want to explain why some promising math topics remain absent, `papers >= 60` is a more plausible next target than `neighbors >= 2`.

## Decision Fork

### Option A: Review Representative Export / Category Rotation

**Status**: ✅ Recommended first

Evidence:

1. math already has eligible anchors
2. 100-case audit yields 9 math cases
3. default 12-case export yields only ~1 math case

**Action**: Review how representative cases are sampled and whether math needs a richer export view than the top-level balanced summary.

### Option B: Review Paper Threshold

**Status**: ✅ Plausible second step

Evidence:

1. 19 multi-period math topics miss only `papers >= 60`
2. several near-miss topics sit just below the threshold

**Action**: Evaluate whether math should use a lower or category-aware paper threshold for case discovery.

### Option C: Review Topic Alignment

**Status**: ⚠️ Longer-term fix

The earlier data audit still suggests persistence fragmentation may matter, but this package does not support a graph-empty diagnosis.

## Recommended Next Step

**PKG-MATH-EXPORT-REVIEW-01**: Representative Export and Case Selection Review

```yaml
package_id: "PKG-MATH-EXPORT-REVIEW-01"
owner: "case-worker"
tree_path: "math"
task_type: "representative_export_review"
goal: "分析 default evolution_cases 导出为何将 math 从 eligible anchor pool 压缩到约 1 个展示案例"
evidence:
  - "60 multi-period math topics pass current filters"
  - "100-case audit has 9 math cases"
  - "12-case default export has ~1 math case"
questions:
  - "category rotation 对 math 的压缩效应有多大？"
  - "default --max-cases=12 是否只适合展示层，不适合作为子域判断输入？"
  - "是否需要单独的 math-focused case export 视图？"
expected_outcome: "区分展示层 summary 与子域 case-discovery 输入"
```

If export review confirms summary compression is the main issue:

**PKG-MATH-ANCHOR-ADJUST-01**: Anchor Selection Policy Adjustment (Workaround)

```yaml
package_id: "PKG-MATH-ANCHOR-ADJUST-01"
owner: "case-worker"
tree_path: "math"
task_type: "anchor_policy_adjustment"
goal: "审视 paper threshold 或 category-aware anchor policy，而不是默认改 neighbor threshold"
evidence:
  - "60 multi-period math topics already pass current filters"
  - "19 additional multi-period math topics are mainly blocked by papers >= 60"
  - "default summary export compresses math visibility"
proposed_change: "Review paper threshold or category-aware export before changing neighbor threshold"
```

## Files Generated

| File | Purpose |
|------|---------|
| `data/output/audit_math_cases/evolution_cases.json` | 100-case audit |
| `docs/plans/2026-03-18-math-anchor-audit.md` | This document |

## Constraints Followed

✅ Did not modify pipeline code
✅ Did not modify tests or Makefile
✅ Did not modify registry or benchmark docs
✅ Audit output written to separate directory
✅ No synthetic cases introduced

## Conclusion

**Primary finding**: The current worktree does not support a “graph has 0 edges” diagnosis. Math already has a nontrivial eligible anchor pool.

- **60 multi-period math topics pass current filters**
- **19 additional multi-period topics are filtered mainly by `papers >= 60`**
- **The biggest visibility compression appears in representative export, not neighbor filtering**

**Next step**:
1. **First**: Review representative export / category rotation (`PKG-MATH-EXPORT-REVIEW-01`)
2. **Then if needed**: Review paper threshold or category-aware anchor policy

The math domain has sufficient multi-period topics to justify deeper review, but the next bottleneck to study is summary/export policy rather than a nonexistent empty graph.
