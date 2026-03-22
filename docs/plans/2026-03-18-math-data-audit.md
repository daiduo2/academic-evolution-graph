doc_type: "governance"
scope: "math data completeness and alignment quality audit"
status: "completed"
owner: "trend-monitor"
source_of_truth: true
upstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/10-math-data-audit-package.md"
downstream_docs: []
last_reviewed: "2026-03-18"

# Math Data Audit Report

## Executive Summary

**Audit Date**: 2026-03-18
**Package**: PKG-MATH-AUDIT-01
**Status**: ✅ Completed

**Key Finding**: The math domain is NOT empty - it has **374 topics** across 26 subcategories. The perceived "emptiness" comes from three factors:

1. **78.3% of math topics are single-period** (cannot form evolution pairs)
2. **Default `--max-cases=12`** only exports 12 representative cases globally
3. **Strict anchor selection criteria** filter out many potential candidates

## Math Subcategory Analysis

### Representative Table

**Note**: This table shows the 26 most relevant subcategories for evolution analysis. The full dataset contains 29 subcategories (including AC, AT, CA which have minimal topic counts).

| Subcategory | Topics | Single-period | Multi-period | Bootstrap Assessment |
|-------------|--------|---------------|--------------|---------------------|
| math.PR (Probability) | 29 | 17 | **12** | ✅ Good candidate |
| math.AP (Analysis) | 37 | 28 | **9** | ✅ Good candidate |
| math.CO (Combinatorics) | 47 | 40 | **7** | ✅ Good candidate |
| math.NA (Numerical Analysis) | 36 | 29 | **7** | ✅ Good candidate |
| math.NT (Number Theory) | 16 | 9 | **7** | ✅ Good candidate |
| math.OC (Optimization) | 48 | 41 | **7** | ✅ Good candidate |
| math.DG (Differential Geometry) | 19 | 14 | **5** | ✅ Good candidate |
| math.AG (Algebraic Geometry) | 17 | 14 | **3** | ⚠️ Possible with care |
| math.DS (Dynamical Systems) | 22 | 19 | **3** | ⚠️ Possible with care |
| math.FA (Functional Analysis) | 11 | 8 | **3** | ⚠️ Possible with care |
| math.LO (Logic) | 15 | 12 | **3** | ⚠️ Possible with care |
| math.GR (Group Theory) | 9 | 7 | **2** | ⚠️ Possible with care |
| math.GT (Geometric Topology) | 9 | 7 | **2** | ⚠️ Possible with care |
| math.MG (Metric Geometry) | 5 | 3 | **2** | ⚠️ Possible with care |
| math.OA (Operator Algebras) | 4 | 2 | **2** | ⚠️ Possible with care |
| math.ST (Statistics Theory) | 16 | 14 | **2** | ⚠️ Possible with care |
| math.RT (Representation Theory) | 5 | **5** | **0** | ❌ Mostly single-period |
| math.HO (Homotopy) | 6 | **6** | **0** | ❌ Mostly single-period |
| math.RA (Rings & Algebras) | 3 | **3** | **0** | ❌ Insufficient data |
| math.QA (Quantum Algebra) | 2 | **1** | **1** | ❌ Insufficient data |
| math.CT (Category Theory) | 3 | 2 | 1 | ❌ Insufficient data |
| math.CV (Complex Variables) | 5 | 4 | 1 | ❌ Mostly single-period |
| math.GM (General Math) | 3 | 2 | 1 | ❌ Insufficient data |
| math.SG (Symplectic Geometry) | 5 | 4 | 1 | ❌ Mostly single-period |
| math.KT | 1 | 1 | 0 | ❌ Insufficient data |
| math.SP (Spectral Theory) | 1 | 1 | 0 | ❌ Insufficient data |

### Summary Statistics

- **Total math topics**: 374
- **Single-period topics**: 293 (78.3%)
- **Multi-period topics**: 81 (21.7%)

## Why evolution_cases.json Only Has 12 Cases

### Reason 1: Default `--max-cases=12`

The default export limits to 12 representative cases **globally across all categories**:

| Version | `--max-cases` | Total Cases | Math Cases |
|---------|--------------|-------------|------------|
| Default | 12 | 12 | 1 |
| Audit | 100 | 100 | 9 |

**The 12 cases are distributed evenly across categories**, not concentrated in math.

### Reason 2: Strict Anchor Selection Criteria

To be selected as an anchor, a topic must pass ALL of:

1. `total_papers >= 60`
2. `active_periods >= 2`
3. `neighbors >= 2`
4. Must leave room for `observation_horizon` (4 months)

These filters exclude many math topics, especially those with:
- Short active periods (many math topics are active 1-3 months)
- Lower paper counts
- Sparse neighbor connections

### Reason 3: Single-Period Dominance

With 78.3% of math topics being single-period, they **cannot form evolution pairs** regardless of other criteria.

## QA / RA / RT Reassessment

### math.QA (Quantum Algebra)

| Metric | Value | Assessment |
|--------|-------|------------|
| Total topics | 2 | Very small |
| Single-period | 1 | 50% |
| Multi-period | 1 | 50% |

**Verdict**: ❌ Still gap. Only 2 topics total, cannot form meaningful evolution cases.

### math.RA (Rings & Algebras)

| Metric | Value | Assessment |
|--------|-------|------------|
| Total topics | 3 | Very small |
| Single-period | 3 | 100% |
| Multi-period | 0 | 0% |

**Verdict**: ❌ Still gap. All topics are single-period, no temporal evolution possible.

### math.RT (Representation Theory)

| Metric | Value | Assessment |
|--------|-------|------------|
| Total topics | 5 | Small |
| Single-period | 5 | 100% |
| Multi-period | 0 | 0% |

**Verdict**: ❌ **Surprising finding** - RT has 5 topics but ALL are single-period. Despite being conceptually related to AG, the current alignment produces no multi-period topics.

**Key insight**: math.RT is NOT a better candidate than QA/RA in the current data window.

## Top Bootstrap Candidates (Better Than RT)

Based on multi-period topic count:

1. **math.PR** (Probability): 12 multi-period / 29 total
2. **math.AP** (Analysis): 9 multi-period / 37 total
3. **math.CO** (Combinatorics): 7 multi-period / 47 total
4. **math.NA** (Numerical Analysis): 7 multi-period / 36 total
5. **math.NT** (Number Theory): 7 multi-period / 16 total
6. **math.OC** (Optimization): 7 multi-period / 48 total
7. **math.DG** (Differential Geometry): 5 multi-period / 19 total

## Root Cause Analysis

### What's Really Happening

```
Problem: "Math subdomains look empty"
         ↓
Reality: 374 math topics exist
         ↓
Issue 1: 78% are single-period (can't evolve)
         ↓
Issue 2: Default export only shows 12 cases globally
         ↓
Issue 3: Anchor criteria are strict
         ↓
Underlying: Alignment may be too fragmented (topics split across periods)
         ↓
Result:  Few math topics make it to evolution_cases.json
```

### The Real Bottleneck

**NOT** data window length - we have 13 periods (2025-02 to 2026-02).

**LIKELY** topic alignment fragmentation - alignment output exists, but the resulting topics may be too fragmented for effective evolution analysis. The 78% single-period rate suggests topics are being split across periods rather than unified.

**IS** topic persistence pattern - math topics tend to be:
- Short-lived (1-3 months active)
- Sparsely connected
- Lower paper counts compared to CS/Physics

## Decision Fork Recommendation

### Option A: Bootstrap New Subdomain

**Condition**: Find subcategory with >=4 multi-period topics AND cross-period evolution potential.

**Candidates**:
- ✅ math.PR, math.AP, math.CO, math.NA, math.NT, math.OC, math.DG

**Action**: Create bootstrap package for top candidate (math.PR or math.NT).

### Option B: Adjust Data/Case Strategy

**Condition**: Most topics are single-period due to alignment fragmentation.

**Evidence**: 78.3% single-period suggests alignment may be too fine-grained, splitting related research across period boundaries instead of maintaining topic continuity.

**Action**:
1. Review topic alignment parameters (keyword threshold, similarity cutoff)
2. Consider merging fragmented topics across periods
3. Relax anchor selection criteria for math domain

### Current Assessment

**Recommendation: Option B first, then Option A**

1. **Audit shows sufficient multi-period topics exist** (81 total)
2. **But they're not forming evolution cases** - suggests alignment/criteria issue
3. **Before opening new subdomains**, verify why existing multi-period topics aren't selected
4. **If alignment is correct**, then proceed with math.PR or math.NT bootstrap

## Next Recommendation

### Immediate Next Step

**PKG-MATH-AUDIT-02**: Anchor Selection Criteria Review

Investigate why the 81 multi-period math topics aren't being selected as anchors:

```yaml
package_id: "PKG-MATH-AUDIT-02"
tree_path: "math data audit"
task_type: "anchor_selection_criteria_review"
goal: "分析81个multi-period math topics为何很少被选中为anchor"
questions:
  - "paper count threshold (>=60) 是否对math太严格？"
  - "neighbor count threshold (>=2) 是否过滤了合理的math topics？"
  - "horizon限制是否让短周期math topics无法入选？"
deliverable: "调整anchor策略或确认当前对齐质量的建议"
```

### Alternative Next Step

If criteria review confirms alignment is correct:

**PKG-PR-01**: Bootstrap math.PR (Probability)

- 12 multi-period topics
- 29 total topics
- Strongest candidate among unexamined subdomains

## Files Generated

| File | Purpose |
|------|---------|
| `data/output/audit_math_cases/evolution_cases.json` | 100-case audit version |
| `data/output/audit_math_cases/evolution_report.md` | Audit report |
| `docs/plans/2026-03-18-math-data-audit.md` | This document |

## Constraints Followed

✅ Did not modify pipeline code
✅ Did not modify tests or Makefile
✅ Did not modify existing benchmark docs
✅ Did not modify registry
✅ Audit output written to separate directory
✅ No synthetic cases introduced

## Conclusion

The math domain has **ample data** (374 topics) but **poor persistence characteristics** (78% single-period). The evolution_cases.json 12-case limit is due to:

1. Default export limit (12 cases globally)
2. Strict anchor criteria
3. Math topics' natural short-lived pattern

**math.QA, math.RA, and math.RT remain gap status** - none have sufficient multi-period topics.

**Better candidates exist**: math.PR, math.AP, math.CO, math.NA, math.NT, math.OC, math.DG all have 5+ multi-period topics.

**Next step**: Review anchor selection criteria before proceeding with new subdomain bootstrap.
