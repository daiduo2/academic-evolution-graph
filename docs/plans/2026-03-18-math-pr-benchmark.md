doc_type: "benchmark_skeleton"
scope: "math > math.PR"
status: "provisional_skeleton_candidate"
owner: "doc-agent"
source_of_truth: true
upstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-12-math-worker-backlog.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/03-task-packages.md"
downstream_docs: []
last_reviewed: "2026-03-18"
package_id: "PKG-PR-01-provisional"
decision: "Provisional - Pre-Skeleton Assessment"
---

# Math.PR (Probability) Benchmark Skeleton

## Decision

**Provisional Skeleton Candidate - Pre-Skeleton Assessment Stage**

math.PR 在当前数据窗口中显示出潜在的 benchmark skeleton 条件，但需要进一步验证 explicit exported PR cases 后才能确认。

**⚠️ PKG-PR-01B Scope Correction**: 本轮 PKG-PR-01B 使用的是 **math-wide export** (`--category-filter math`)，而非 PR-specific extraction。虽然数据结构显示 12 个 multi-period topics 和 6 个 eligible anchors，但 math-wide export 对 PR-specific surfacing **不够聚焦**（仅 ~10% PR-related 内容）。**PKG-PR-01B 不能作为锁死 MPR-02 的最终证据**。下一步需要执行 **真正的 PR-specific candidate extraction**（使用 hierarchy filter 或 subcategory filter）。

## PKG-PR-01B Evidence Summary (2026-03-18)

### Evidence Buckets

基于 PR-specific case surfacing 的结果，证据分为以下四类：

#### 1. Confirmed/Export-Supported (显式导出确认)

| Case ID | Anchor | Name | Evidence Type | Status |
|---------|--------|------|---------------|--------|
| 1 | global_39 | 随机过程渗流方程 | Explicit exported case | ✅ Confirmed |

**Count: 1** - 仅 1 个显式导出的 PR evolution case。

**⚠️ Scope Correction**: 实际上，math-wide export 中 PR-related anchors 有 11 个 (global_2,3,4,8,14,15,19,21,23,24,25)，但这些是 **math-wide 采样**（来自 AG/NT/AP/CO/PR 等混合子域），不是 PR-specific extraction。因此不能作为 MPR-02 的锁定证据。

#### 2. Strong Inferred (强推断候选)

从 global_39 的 evolution case detail 中识别出的 neighbor relationships：

| Anchor | Target | Relation | Inference Basis | Confidence |
|--------|--------|----------|-----------------|------------|
| global_39 | global_99 | Object continuity (percolation → random walk) | Shared keywords: brownian, convergence, equations, stochastic | Medium |
| global_39 | global_65 | Method continuity (percolation → SDE convergence) | Bridge strength: 0.833, shared: brownian, convergence, equations, stochastic | Medium |
| global_39 | global_188 | Method continuity (via rough paths) | Neighbor in evolution path | Low-Medium |

**Count: 3** - 从 global_39 的 neighbor relationships 推断。

#### 3. Boundary Negatives (边界负例)

| Case | Anchor | Target | Reason |
|------|--------|--------|--------|
| n1 | global_39 (percolation) | global_156 (random matrix) | Different objects, no continuity |
| n2 | global_61 (queueing) | any pure probability | Applied vs theoretical boundary |

**Count: 2** - 基于领域知识推断的负例。

#### 4. Ambiguous/Review-Needed (待审查)

| Case | Anchor | Target | Ambiguity |
|------|--------|--------|-----------|
| a1 | global_65 (classical SDE) | global_188 (rough McKean) | Classical vs rough path methods |

**Count: 1** - 需要进一步审查的模糊案例。

### Evidence Scope Limitation (Corrected)

**输入数据范围说明**:
- 当前输入为 math-wide 20-case export (`--max-cases 20 --category-filter math`)
- **不是 PR-only candidate surfacing** — 这是 math category filter，不是 math.PR hierarchy filter
- 20 cases 中仅 ~10% 是 PR-related (global_39, global_3)，其余来自 AG/AP/NA/DG/GR/CO 等子域

**Schema 状态修正**:
- ✅ **neighbor_topics 字段**: 存在于 100% cases (98 total references, avg 4.9/case)
- ✅ **key_supporting_topics 字段**: 存在于 100% cases (62 total references, avg 3.1/case)
- ✅ **topic_graph.json**: 是有效的 meta-graph 结构，不是 "0 edges"
- ❌ **之前错误**: "0 topics have neighbor_topic_ids (data-baseline issue)" — **此说法不正确**

**结论修正**:
- 当前 export **范围太宽**（math-wide），而非 data 问题
- 对 PR-specific surfacing 不够聚焦 — 包含太多 AG/NT/AP/CO 内容
- 需要 **PR-specific candidate extraction**（使用 `--hierarchy-filter math.PR` 或 subcategory filter）

### Decision: MPR-02 Status (Corrected 2026-03-18)

**MPR-02 Status: 🔒 LOCKED — Cannot be unlocked by PKG-PR-01B**

**锁定原因**: PKG-PR-01B 使用的是 **math-wide export** (`--category-filter math`)，而非 **PR-specific extraction**。该输入对 PR-specific surfacing 不够聚焦。

当前状态修正：
1. **Scope Mismatch**: math-wide 20-case export 中仅 ~10% PR-related content
2. **Explicit PR anchors**: 11 (global_2,3,4,8,14,15,19,21,23,24,25) — 但这些是 math-wide 采样，非 PR-specific
3. **Schema intact**: neighbor_topics (98 refs) 和 key_supporting_topics (62 refs) 存在且健康
4. **Data quality**: ✅ 无 data-baseline issue，"0 neighbors" 说法错误

**修正后结论**:
- PKG-PR-01B **不能**作为锁死 MPR-02 的最终证据
- 当前 export 过于宽泛（math-wide），对 PR-specific surfacing 不够聚焦
- 下一步：**真正的 PR-specific candidate extraction**（使用 hierarchy filter 或 subcategory filter）

---

## Data Verification

### Corrected Verification Logic

**之前错误的方法**（使用不存在的 `periods` 字段）：
```python
# ❌ WRONG - 字段不存在
trends[tid].get("periods", [])
```

**正确的方法**（使用 `active_periods` 或 `history` 字段）：
```python
# ✅ CORRECT - 使用 active_periods
trends[tid].get("active_periods", 0) > 1

# 或等价地，使用 history 长度
len(trends[tid].get("history", [])) > 1
```

### Corrected Verification Commands

```bash
# Method 1: Using active_periods field
python3 -c "
import json
with open('data/output/aligned_topics_hierarchy.json') as f:
    data = json.load(f)

pr_ids = set(data['hierarchies']['math.PR']['topic_assignments'].keys())
trends = data.get('trends', {})

# Using correct field: active_periods
multi = [t for t in pr_ids if t in trends and trends[t].get('active_periods', 0) > 1]
print(f'Multi-period PR topics: {len(multi)}')  # Output: 12
"

# Method 2: Using history field (equivalent)
python3 -c "
import json
with open('data/output/aligned_topics_hierarchy.json') as f:
    data = json.load(f)

pr_ids = set(data['hierarchies']['math.PR']['topic_assignments'].keys())
trends = data.get('trends', {})

# Using correct field: history
multi = [t for t in pr_ids if t in trends and len(trends[t].get('history', [])) > 1]
print(f'Multi-period PR topics: {len(multi)}')  # Output: 12
"
```

### Verification Result

| Metric | Original (Wrong) | Corrected |
|--------|------------------|-----------|
| Total PR topics | 29 | 29 ✅ |
| Multi-period topics | **0** (using wrong field) | **12** ✅ |
| Evolution cases | 0 | 6 ✅ |
| Eligible anchors | 0 | **6** ✅ |

### Data Assessment

#### math.PR Topics Overview

| Metric | Value |
|--------|-------|
| Total PR topics | 29 |
| Multi-period topics | **12** |
| Single-period topics | 17 |
| Evolution cases | 6 |
| Eligible anchors | **6** |

#### Multi-Period PR Topics (12)

| Topic ID | Name | Papers | Periods | History |
|----------|------|--------|---------|---------|
| global_38 | 随机极限与不等式 | 208 | 2 | 2025-02, 2025-03 |
| global_39 | 随机过程渗流方程 | 1280 | 4 | 2025-02, 2025-06, 2025-12, 2026-01 |
| global_47 | 伊辛相变与临界 | 96 | 2 | (checked via export) |
| global_61 | 重交通环形排队 | 27 | 2 | (papers < 60) |
| global_65 | 随机微分方程收敛 | 391 | 4 | 2025-03, 2025-05, 2025-08, 2025-10 |
| global_99 | 随机游走与分支 | 179 | 3 | 2025-04, 2025-09, 2026-02 |
| global_100 | 随机矩阵系综累积量 | 78 | 2 | (checked via export) |
| global_116 | 强化随机游走渗流 | 65 | 2 | (checked via export) |
| global_156 | 随机矩阵特征值分析 | 78 | 2 | 2025-06, 2025-09 |
| global_188 | 随机粗糙McKean方程 | 387 | 4 | 2025-07, 2025-09, 2025-11, 2026-02 |
| global_211 | 种群适应与生态进化 | 94 | 2 | (checked via export) |
| global_271 | 渗流与随机行走临界性 | 118 | 2 | (checked via export) |

#### Eligible Anchors (6)

All satisfy: papers >= 60, periods >= 2

1. **global_38**: 随机极限与不等式 (208 papers, 2 periods)
2. **global_39**: 随机过程渗流方程 (1280 papers, 4 periods)
3. **global_65**: 随机微分方程收敛 (391 papers, 4 periods)
4. **global_99**: 随机游走与分支 (179 papers, 3 periods)
5. **global_156**: 随机矩阵特征值分析 (78 papers, 2 periods)
6. **global_188**: 随机粗糙McKean方程 (387 papers, 4 periods)

**注**: neighbor 信息来自 evolution case analysis (neighbor_topics 字段) 和 topic_graph.json edges，非 topic_index.neighbor_topic_ids 字段

### Evolution Chains Identified

Based on neighbor relationships between eligible anchors:

```
Percolation chain (渗流链):
  global_39 (渗流方程) -> global_99 (随机游走) -> global_188 (粗糙McKean方程)

Random matrix chain (随机矩阵链):
  global_38 (随机极限与不等式) -> global_156 (随机矩阵特征值) / global_100 (随机矩阵系综累积量)

Stochastic process chain (随机过程链):
  global_39 (渗流方程) -> global_65 (微分方程收敛) -> global_188 (粗糙McKean方程)
```

## Why Option A (Not Option B)

### Option A Conditions Check

| Condition | Status | Evidence |
|-----------|--------|----------|
| >= 2 object-side candidate positives | ⚠️ PARTIAL | 3 candidate evolution chains (inferred from neighbor relationships) |
| >= 2 negative/ambiguous cases | ⚠️ PARTIAL | Candidate boundary cases identified (not yet verified) |
| Not relying on generic words | ✅ PASS | Specific objects: percolation, random matrices, SDEs |
| Clear advantage over math.RA/QA | ✅ PASS | 12 multi-period vs 0 for RA/QA |

**Note**: "candidate" indicates these are inferred from topic metadata and neighbor relationships, not yet confirmed through explicit exported evolution cases.

### Positive Case Candidates (Inferred)

| Chain | Anchor | Target | Relation Type | Status |
|-------|--------|--------|---------------|--------|
| Percolation | global_39 | global_99 | object_continuity (percolation theory) | candidate |
| Percolation | global_99 | global_188 | method_continuity (rough path theory) | candidate |
| Random matrix | global_38 | global_156 | object_continuity (random matrix theory) | candidate |
| SDE | global_65 | global_188 | method_continuity (SDE convergence -> rough paths) | candidate |

**Note**: These are candidate positives inferred from topic metadata and neighbor relationships. Explicit exported PR cases are still limited and need verification through case surfacing.

### Negative Case Candidates

| Case | Anchor | Target | Reason |
|------|--------|--------|--------|
| n1 | global_39 (percolation) | global_156 (random matrix) | Different objects, no continuity |
| n2 | global_61 (queueing) | any pure probability | Applied vs theoretical boundary |
| n3 | global_211 (population) | global_39 (percolation) | Biological vs physical stochastic |

### Ambiguous Case Candidates

| Case | Anchor | Target | Ambiguity |
|------|--------|--------|-----------|
| a1 | global_65 (classical SDE) | global_188 (rough McKean) | Classical vs rough path methods |

## Comparison with Other Math Subdomains

| Subdomain | Multi-period Topics | Eligible Anchors | Benchmark Status |
|-----------|---------------------|------------------|------------------|
| math.LO | 11 | 6 | ✅ Ready |
| math.AG | 6 | 6 | ✅ Ready |
| **math.PR** | **12** | **6** | ⚠️ **Provisional** (pending case surfacing) |
| math.RA | 0 | 0 | ❌ Gap (insufficient data) |
| math.QA | 0 | 0 | ❌ Gap (insufficient data) |

## Conclusion (Corrected)

math.PR 在当前 12 个月数据窗口中:
- 有 29 个 topics，其中 **12 个 multi-period** (strong evidence)
- 有 **6 个 eligible anchors** 满足所有条件
- **Schema 健康**: neighbor_topics (98 refs) 和 key_supporting_topics (62 refs) 完整存在
- **Data quality**: ✅ 无 data-baseline issue

**⚠️ PKG-PR-01B 局限性**:
- 使用的是 **math-wide export** (`--category-filter math`)，而非 PR-specific extraction
- Export 中仅 ~10% PR-related 内容，过于宽泛
- **不能**作为锁死 MPR-02 的最终证据

**修正后结论**:
当前 math-wide export 对 PR-specific surfacing **仍然不够聚焦**。需要真正的 **PR-specific candidate extraction**（使用 hierarchy filter 或 subcategory filter）才能获取足够的 explicit PR cases 来支持 MPR-02。

**Recommendation:**
执行 **MPR-01C: PR-targeted candidate extraction** — 使用 `--hierarchy-filter math.PR` 或添加 subcategory 过滤，获取真正 PR-specific 的 export 后再评估 MPR-02 解锁条件。

## Next Steps (Revised)

1. **MPR-01C: PR-targeted candidate extraction** ⭐ PRIORITY
   - **目标**: 执行真正的 PR-specific extraction，而非 math-wide sample
   - **方法**: 使用 `--hierarchy-filter math.PR` 或添加 subcategory 过滤
   - **成功标准**: 获取 >=5 PR-specific evolution cases 且 neighbor relationships 清晰

2. **Schema enhancement** (optional but recommended)
   - 在 evolution_cases.json 中添加 `subcategory` 字段 (e.g., "PR", "AG", "NT")
   - 或添加 `hierarchy_path` 字段 (e.g., "math.PR", "math.AG")

3. **Registry update**: 在 MPR-01C 完成后，在 evolution-rule-coverage.md 中标记 math.PR 状态

4. **Backlog update**: 根据 MPR-01C 结果，决定是否解锁 MPR-02

5. **Case curation** (conditional): 如果 MPR-01C 验证通过，执行 MPR-02 固定第一批真实 benchmark cases

**⚠️ Important**:
- PKG-PR-01B **不能**解锁 MPR-02 — 需要真正的 PR-specific extraction
- 在 PR-targeted export 验证之前，不要将 math.PR 标记为 skeleton-ready

## References

- Data source: `/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/data/output/aligned_topics_hierarchy.json`
- Verification: Using `active_periods` or `history` fields (not the non-existent `periods` field)
- Related gaps: math.RA (03-task-packages.md#PKG-RA-01), math.QA (03-task-packages.md#PKG-QA-01A)

## MPR-02 Case Curation Results (2026-03-21)

**Status:** COMPLETE — Conditional graph integration readiness confirmed

**Curated Positives:**
- PR-P1: global_38→global_100 (Tier A) — two-source: evolves_from 0.39 + adjacency 0.35
- PR-P2: global_38→global_156 (Tier A) — two-source: evolves_from 0.4077 + adjacency 0.4077
- PR-P3: global_38→global_99 (Tier B) — single-source: evolves_from 0.39 only
- PR-P4: global_65→global_188 (Tier B) — adjacency-only: bw=0.4795

All positives: strong inferred curated cases, NOT benchmark-confirmed. Paper-level review required.

**Curated Negatives (core):** PR-N1 (global_211), PR-N2 (global_47), PR-N3 (global_61)
**Additional Negatives:** PR-N4 (global_214), PR-N5 (global_333 — spurious evolves_from from global_65)
**Ambiguous Cases:** PR-A1 (global_65↔global_39), PR-A2 (global_271↔global_99)

**Next:** PR Phase 2C — conditional graph integration planning

**Reference:** `docs/plans/2026-03-21-math-pr-case-curation.md`

**PR-TrackB-03 (2026-03-26):** PR-P4 demoted from Gate 2 directional candidate. Cluster-level review confirmed parallel development (not sequential evolution) for global_65→global_188. R2 resolved in the negative. P4 retained as adjacency calibration case only.

**PR-TrackB-04 (2026-03-27):** P3 (global_38→global_99) demoted — identical representative papers with global_38, no adjacency corroboration, single-source only. P1 (global_38→global_100) and P2 (global_38→global_156) provisionally retained at title-level; Gate 2 path partially viable pending Level 3 review.

**PR-TrackB-05 (2026-03-28):** global_100 and global_156 confirmed NOT RELIABLY DISTINCT (5/5 identical representative papers; inter-cluster bw=0.475). P1 (global_38→global_100) and P2 (global_38→global_156) collapse to single candidate. P1/P2 CONDITIONALLY DEMOTED — founding-date pressure (RMT fields 30-70 years old vs global_38's 2025 cluster), category mismatch concern (global_38 is classical random walks, not RMT), citation signal absent at title-level. Gate 2 path: SINGLE-CANDIDATE HEIGHTENED CONCERN pending PR-TrackB-06.

---

## MPR-01C Update (2026-03-20)

**MPR-01C completed — Decision: Option A — MPR-02 UNLOCKED**

MPR-01C (PR-Targeted Candidate Extraction) was executed on 2026-03-20. The PR-specific extraction produced a candidate pool that satisfies the MPR-02 unlock conditions.

**Note (MPR-01C-fix)**: Corrected by MPR-01C-fix: evolves_from evidence is from MAIN topic_graph.json, not targeted export. The targeted export (`data/output/math_discovery_pr_targeted/topic_graph.json`) only has `adjacent_to` edges — no `evolves_from`. The 3 evolves_from edges come from `data/output/topic_graph.json` (main graph).

**Direction correction (MPR-01C-final-fix)**: pairs P1/P2/P3 source/target were reversed in prior version. Corrected per pipeline semantics: source=older, target=newer. global_38 (active 2025-02/03) is the OLDER source; global_100/156/99 (active 2025-04+) are the NEWER targets. The evolution chain and positive case candidates table above have been updated accordingly.

**Reference**: `docs/plans/2026-03-20-math-pr-candidate-extraction.md`

### Key Evidence Summary

**Positive Pairs (graph-derived from topic_graph.json):**

| Source | Target | Type | Basis |
|--------|--------|------|-------|
| global_38 (random limits) | global_100 (random matrix ensemble) | object continuity | evolves_from main topic_graph.json + adjacency bw=0.35 |
| global_38 (random limits) | global_156 (random matrix eigenvalue) | object continuity | evolves_from main topic_graph.json + adjacency bw=0.4077 |
| global_38 (random limits) | global_99 (random walk/branching) | object continuity | evolves_from main graph only (no adjacency) |
| global_65 (SDE convergence) | global_188 (rough McKean) | method continuity | Strongest adjacent pair (bw=0.4795) |

3 evolves_from edges from main topic_graph.json + 1 strong inferred method continuity pair.

**Clear Negatives (3):**
- global_211 (population ecology) — wrong domain
- global_47 (Ising) — math.MP crossover, not PR object
- global_61 (queueing) — applied, not theoretical PR

**Ambiguous (1):**
- global_65 vs global_39 (both stochastic but different objects)

**Vocabulary check**: Candidate pairs use specific keywords (eigenvalues, matrices, percolation, martingale, rough paths) — NOT generic "stochastic/random".

### MPR-02 Status Update

**MPR-02: 🔓 UNLOCKED** (was 🔒 LOCKED as of PKG-PR-01B)

The candidate pool satisfies the >= 2 positive pairs and >= 2 negatives requirement.

**Important caveat**: All positive pairs remain "strong inferred" status (graph-derived from topic_graph.json), NOT benchmark-confirmed. MPR-02 case curation was the next step — it has now been completed (2026-03-21), and all positive pairs remain strong inferred curated cases, not benchmark-confirmed. Paper-level review is required before any pair is promoted to benchmark-confirmed status.

Evidence source correction noted (MPR-01C-fix, 2026-03-20). Direction correction (MPR-01C-final-fix, 2026-03-20): pairs P1/P2/P3 source/target were reversed in prior version. Corrected per pipeline semantics: source=older, target=newer.

## Data Quality & Schema Corrections

### Correction 1: Multi-Period Topics Verification
**重要**: 本文档修正了 PKG-PR-01 原始分析中的严重数据错误。原始分析使用了不存在的 `periods` 字段，导致误判为 0 multi-period topics。正确的验证使用 `active_periods` 或 `history` 字段，实际结果为 **12 multi-period topics** 和 **6 eligible anchors**。

### Correction 2: "0 Neighbors" Misconception (2026-03-18)
**同样重要**: 之前 claim 的 "0 topics have neighbor_topic_ids (data-baseline issue)" 是 **错误的**。

**实际情况**:
- ✅ `neighbor_topics` 字段存在于 **100% 的 cases** (20/20)
- ✅ 总计 **98 个 neighbor references** (平均 4.9/case)
- ✅ `key_supporting_topics` 字段存在于 **100% 的 cases**
- ✅ 总计 **62 个 supporting topic references** (平均 3.1/case)
- ✅ `topic_graph.json` 是有效的 meta-graph 结构，不是 "0 edges"

**结论**: 没有 data-baseline issue。问题是 **scope**（math-wide vs PR-specific），不是 data quality。

### Summary of Corrections

| Issue | Original Claim | Corrected Finding |
|-------|---------------|-------------------|
| Multi-period topics | 0 (wrong field) | 12 (using `active_periods`) |
| Neighbor data | 0 (data-baseline issue) | 98 refs in 100% cases |
| Supporting topics | Not checked | 62 refs in 100% cases |
| Export scope | Assumed PR-specific | Actually math-wide |
| MPR-02 readiness | Almost ready | Historical note: this was corrected by MPR-01C; current state is **completed with conditional graph-integration readiness** |

---

**Updated by PR-TrackB-06 (2026-03-29):** Gate 2 COLLAPSED. All Track B candidates demoted: P4 (TrackB-03), P3 (TrackB-04), P1/P2 final (TrackB-06, 2026-03-29). Positive pairs PR-P1 and PR-P2 are DEMOTED — category mismatch confirmed at abstract level, founding-date inversion confirmed (temporally impossible), citation signal absent, BERTopic edge confirmed as taxonomy artifact. These pairs remain as calibration cases only, not benchmark-confirmable candidates. math.PR at long-term Gate 1. MPR-03 (PR benchmark runner) is unblocked from Track B but Gate 2 passage is not achievable without new directional evidence.
