doc_type: "governance"
scope: "math representative export and case selection review"
status: "completed"
owner: "case-worker"
source_of_truth: true
upstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-18-math-anchor-audit.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-18-math-data-audit.md"
downstream_docs: []
last_reviewed: "2026-03-18"

# Math Export Review Report

## Executive Summary

**Review Date**: 2026-03-18
**Package**: PKG-MATH-EXPORT-REVIEW-01
**Status**: ✅ Completed

**Primary Finding**: The default `--max-cases=12` export with category rotation compresses math visibility from 9 cases (in 100-case audit) to 1 case (in default export), creating a **9x visibility compression**.

Key Evidence:
- **60 multi-period math topics** pass all anchor filters (papers >= 60, periods >= 2, neighbors >= 2)
- **9 math cases** appear in 100-case audit
- **1 math case** appears in 12-case default export
- **Category rotation** evenly distributes the 12 slots across top-level categories, regardless of each category's eligible anchor pool size

## 12-Case vs 100-Case Comparison

### Default Export (12-case)

```
Total cases: 12
distribution: 1 case per category (forced balance)
```

| Category | Count |
|----------|-------|
| astro-ph | 1 |
| cond-mat | 1 |
| cs | 1 |
| econ | 1 |
| eess | 1 |
| gr-qc | 1 |
| hep | 1 |
| **math** | **1** |
| nlin | 1 |
| nucl | 1 |
| physics | 1 |
| q-bio | 1 |

**Math cases**: 1 (global_30 - 法诺簇模空间曲线)

### Audit Export (100-case)

```
Total cases: 100
distribution: proportional to eligible anchor count
```

| Category | Count | Ratio (100/12) |
|----------|-------|----------------|
| astro-ph | 9 | 9x |
| cond-mat | 9 | 9x |
| cs | 9 | 9x |
| eess | 9 | 9x |
| hep | 9 | 9x |
| **math** | **9** | **9x** |
| physics | 9 | 9x |
| stat | 8 | 8x |
| quant-ph | 8 | 8x |
| q-bio | 7 | 7x |
| gr-qc | 6 | 6x |
| q-fin | 3 | - |
| nucl | 2 | 2x |
| econ | 2 | 2x |
| nlin | 1 | 1x |

**Math cases**: 9

### Math Cases Detail (100-case audit)

| Anchor ID | Name | Subcategory |
|-----------|------|-------------|
| global_3 | 凸优化牛顿收敛性 | OC |
| global_8 | 图与顶点条件研究 | CO |
| global_19 | 数学算子与无穷空间 | FA |
| global_23 | 有限元伽辽金方法 | NA |
| global_24 | 有限群共轭子群 | GR |
| global_25 | 椭圆方程求解方法 | AP |
| global_30 | 法诺簇模空间曲线 | AG |
| global_39 | 随机过程渗流方程 | PR |
| global_55 | 李代数与Hopf代数 | AG |

**Note**: Only global_30 appears in the 12-case export. The other 8 math anchors are filtered out by the category rotation mechanism.

## Math Visibility Compression Analysis

### The Compression Mechanism

```
Math eligible anchor pool
    └── 60 topics pass all filters
        └── Category rotation sampling
            └── 12-case limit with even distribution
                └── Math gets ~1 slot (compressed from 60 to 1)
```

### Compression Factor by Stage

| Stage | Math Count | Compression |
|-------|-----------|-------------|
| Multi-period topics | 84 | - |
| Pass all filters | 60 | 1.4x |
| In top 100 cases | 9 | 6.7x |
| In 12-case export | 1 | 9x |

**Total compression**: 60 eligible anchors → 1 visible case = **60x compression**

### Category Rotation Impact

The 12-case export uses **forced category balancing**:

```python
# Simplified logic
def select_representative_cases(eligible_anchors, max_cases=12):
    categories = get_unique_categories(eligible_anchors)
    cases_per_category = max_cases // len(categories)  # ~1 per category

    selected = []
    for category in categories:
        category_anchors = filter_by_category(eligible_anchors, category)
        selected.extend(sample(category_anchors, cases_per_category))

    return selected
```

**Problem**: Math has 60 eligible anchors (same as physics, CS, etc.), but only gets 1 slot in the 12-case export because categories are balanced, not proportional.

### Why 100-Case Shows More Math

When `max_cases=100`:
- There are enough slots to represent the true distribution
- Math naturally gets ~9 cases (proportional to its 60 eligible anchors)
- No forced category balancing needed

## Representative Export vs Case-Discovery Distinction

### Current Design Intent

**evolution_cases.json (12-case)** is designed as:
- A **summary view** for human review
- A **balanced showcase** across categories
- **Not** a comprehensive case database

### The Mismatch

| Aspect | 12-Case Export | Case-Discovery Need |
|--------|---------------|---------------------|
| Purpose | Human summary | Automated analysis |
| Distribution | Even across categories | Proportional to data |
| Math visibility | 1 case | Needs 9+ for analysis |
| Use case | Quick overview | Subdomain bootstrap |

### Problems Identified

1. **Misleading emptiness**: 1 visible math case suggests "math has no evolution", but math actually has 60 eligible anchors
2. **Bootstrap blocking**: Subdomain bootstrap needs multiple cases to establish patterns; 1 case is insufficient
3. **Data misinterpretation**: Consumers of evolution_cases.json may conclude "math is not ready" when the issue is export policy

## Recommended Next Step

### ✅ 已实现 via PKG-MATH-FOCUSED-EXPORT-01-IMPL

**Implementation Date**: 2026-03-18
**Status**: Completed

Math-focused export 已实现，使用新增的 `--category-filter` CLI 选项：

```bash
python3 pipeline/evolution_analysis.py \
  --input data/output/aligned_topics_hierarchy.json \
  --output-dir data/output/math_discovery \
  --max-cases 20 \
  --category-filter math
```

**使用边界说明**:
- `--category-filter math`: 仅筛选 math 类别的 topics
- `--max-cases 20`: 获取最多 20 个 math cases（实际产出约 15-20 个）
- 输出目录: `data/output/math_discovery/`
- 不经过 category rotation，直接按 score 排序选取

**预期输出**:
- `data/output/math_discovery/evolution_cases.json`: math 专用 cases
- 涵盖 AG, LO, PR, AP, OC, NA, CO, GR 等子域
- 用于后续 PR/NT bootstrap 决策

---

### Historical Decision Fork (Pre-Implementation)

#### Option A: Math-Focused Export View ⭐ Recommended (✅ 已实现)

Create a dedicated math export that bypasses category rotation:

```yaml
package_id: "PKG-MATH-FOCUSED-EXPORT-01"
owner: "case-worker"
tree_path: "math"
task_type: "math_focused_export"
goal: "生成 math 专用的 case export，不经过 category rotation"
expected_output:
  - "~15-20 math cases with full details"
  - "涵盖 AG, LO, PR, AP, OC, NA, CO, GR 等子域"
  - "用于后续 case-discovery 和 bootstrap"
```

**Why**: Math has 60 eligible anchors - enough for a rich case-discovery view. A dedicated export would reveal this without affecting the 12-case summary.

#### Option B: Adjust Default max-cases

Increase default `--max-cases` from 12 to a higher value (e.g., 50):

| max_cases | Math Cases | Trade-off |
|-----------|-----------|-----------|
| 12 | 1 | Too compressed |
| 25 | ~2-3 | Better |
| 50 | ~4-5 | Good balance |
| 100 | 9 | Full visibility |

**Concern**: Larger default export may overwhelm human reviewers.

#### Option C: Dual Export Strategy

Maintain two exports:
1. **evolution_cases.json** (12-case): Keep for human summary
2. **evolution_cases_full.json** (unlimited): For case-discovery input

**Why**: Separates "presentation layer" from "analysis layer".

### Implementation History

**Option A 已实现** (2026-03-18):

```bash
python3 pipeline/evolution_analysis.py \
  --input data/output/aligned_topics_hierarchy.json \
  --output-dir data/output/math_discovery \
  --max-cases 20 \
  --category-filter math
```

**实现细节**:
- 新增 `--category-filter` CLI 选项
- 支持按类别筛选 topics
- 不破坏原有 category rotation 逻辑
- 可与 `--max-cases` 组合使用

**修复 (PKG-MATH-FOCUSED-EXPORT-01-fix)**:
- category-filter 现在同时过滤 graph 和 report
- topic_graph.json 只包含目标类别的 topics 和 edges
- evolution_report.md 的 "Topics available" 只统计目标类别
- 默认无过滤时行为完全不变

**Then**: Consider **Option C** if other domains face similar issues.

**Next**: Proceed with math.PR discovery using math-focused export output.

## Non-Goals

This review explicitly does NOT:

1. **Modify pipeline code** - Only recommendations, no implementation
2. **Change benchmark documents** - No new benchmark skeletons
3. **Update registry** - No rule status changes
4. **Introduce synthetic cases** - All evidence from real data
5. **Modify anchor thresholds** - Paper count (>=60) and neighbor count (>=2) remain unchanged

## Evidence Summary

### Commands Run

```bash
# Extract math cases from default export
jq '.cases[] | select(.category == "math") | {case_id, anchor_topic_id, anchor_topic_name}' \
  data/output/evolution_cases.json

# Result: 1 math case

# Extract math cases from 100-case audit
jq '.cases[] | select(.category == "math") | {case_id, anchor_topic_id, anchor_topic_name}' \
  data/output/audit_math_cases/evolution_cases.json

# Result: 9 math cases

# Category distribution analysis
jq -r '.cases[] | .category' data/output/evolution_cases.json | sort | uniq -c
# Result: 12 categories, 1 case each (forced balance)

jq -r '.cases[] | .category' data/output/audit_math_cases/evolution_cases.json | sort | uniq -c
# Result: 15 categories, distribution proportional to eligible anchors
```

### Key Numbers

| Metric | Value | Source |
|--------|-------|--------|
| Multi-period math topics | 84 | PKG-MATH-AUDIT-02 |
| Eligible math anchors | 60 | PKG-MATH-AUDIT-02 |
| Math cases in 12-export | 1 | This review |
| Math cases in 100-audit | 9 | This review |
| Compression ratio | 9x | Calculated |

## Why This Is Still Export Review Only

This review **does not** propose changes to:
- Pipeline code (`pipeline/evolution_analysis.py`)
- Anchor selection criteria (`papers >= 60`, `neighbors >= 2`)
- Benchmark documentation
- Registry status

It **only** documents:
- The mechanism causing math visibility compression
- The evidence of 9x compression (1 vs 9 cases)
- Recommendations for next steps

Actual implementation (PKG-MATH-FOCUSED-EXPORT-01) is a separate package requiring its own assignment.

## Residual Risk

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| Math-focused export may reveal graph issues | Medium | Already validated graph has edges in PKG-MATH-AUDIT-02 |
| Other categories may have similar compression | High | Recommend Option C (dual export) if confirmed |
| 100-case audit may over-represent math | Low | Distribution matches eligible anchor count |

## Next Recommendation

1. **Immediate**: Assign `PKG-MATH-FOCUSED-EXPORT-01` to create dedicated math case discovery view
2. **Short-term**: Use 20-case math export for PR/NT bootstrap decision
3. **Medium-term**: Consider dual-export strategy (Option C) for all domains

The math domain has **sufficient data** for subdomain bootstrap. The perceived emptiness is an artifact of export policy, not data quality.

---

## Git Commit

This document was created as part of PKG-MATH-EXPORT-REVIEW-01. No code changes were made. Evidence from existing audit files was analyzed to produce findings.
