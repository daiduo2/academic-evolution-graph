---
doc_type: "domain_review"
scope: "math > math.NA"
status: "active"
owner: "trend-monitor"
source_of_truth: true
upstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-11-evolution-doc-standards.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-10-evolution-rule-coverage.md"
downstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-04-03-math-na-benchmark.md"
last_reviewed: "2026-03-22"
---

# Math.NA Rule Review

## Summary

`math.NA` 当前已经足够启动第一版 benchmark skeleton，也已经足够落第一条保守 MVP，但还不够进入 runner-ready / event-level-baseline-ready 阶段。

这轮扫描的结论不是“已经找到可直接实现的宽规则”，而是：

- 域内真实数据量已经明显高于 `math.QA` / `math.RA` 这类 gap 子域
- 可以固定第一批真实 cases（至少 `2 positive + 2 negative + 1 ambiguous`）
- 当前最可能的第一条窄方向不是泛 `numerical-method continuity`
- 更像是：
  - `math_na_krylov_iterative_continuity`（implemented / partial）
- 但 `math.NA` 内部仍有明显 duplicate-topic 风险，第一条规则必须避开这些脆弱 pair

## Scope

本轮 review 只覆盖：

- `math > math.NA`
- 使用 `aligned_topics_hierarchy.json` 与 `topic_graph.json` 的真实 topic / edge 证据
- 目标是回答：
  - `math.NA` 是否足够启动第一版 benchmark skeleton
  - 如果足够，第一条最可能的窄方向是什么

## Rule Inventory

当前已落地 1 条 `partial` 规则：

1. `math_na_krylov_iterative_continuity`

同时保留 3 个 supporting families，但不建议在第一条规则里一起混写：

1. `tensor / low-rank continuity`
   - `global_13 -> global_149`
   - `global_149 -> global_264`
2. `inverse / regularization continuity`
   - `global_124 -> global_255`
3. `Wasserstein sampling continuity`
   - `global_207 -> global_359`

## Main Case Coverage

当前主产物 [evolution_cases.json](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/data/output/evolution_cases.json) 的 12 个自动案例里，`math.NA` 当前 **没有命中**。

这说明：

- `math.NA` 目前还没有进入主事件叙事层
- 第一轮更适合先固定 benchmark skeleton，而不是直接讲 event-level baseline

## Manual Replay Signals

### 1. Data Sufficiency Snapshot

当前 `math.NA` 的基础量化证据是：

- `36` 个真实 topics
- `7` 个 multi-period topics
- `86` 条域内 `adjacent_to`
- `18` 条域内 `evolves_from`

层级深度分布：

- depth 2: `25`
- depth 3: `1`
- depth 4: `9`
- depth 5: `1`

判断：

- 这组数字已经明显超过 `gap / insufficient-data` 阶段
- 即使当前没有 event-level baseline，也已经足够固定第一版真实 skeleton

### 2. Matrix / Krylov Iterative Family

当前最干净的一组 real cases 是：

- `global_105 -> global_140`
  - `GMRES数值近似法 -> 块特征值与Krylov方法`
  - `adjacent_to = 0.3292`
  - `evolves_from = 0.3692`
  - exact shared term: `gmres`
- `global_140 -> global_9`
  - `块特征值与Krylov方法 -> 块矩阵迭代算法加速`
  - `adjacent_to = 0.4400`
  - shared exact terms:
    - `block`
    - `gmres`
    - `krylov`
    - `lanczos`
    - `matrix`

判断：

- 这是当前最适合固定成第一版 benchmark skeleton 主干的一组 evidence
- 原因不是它“最宽”，恰恰相反，是它最容易写成窄的 method-family contract
- `gmres / krylov / lanczos / arnoldi` 这类 exact method 词比 `matrix` / `numerical` / `convergence` 更安全
- `MNA-FILL-02` 后当前 runtime gate 已固定为：
  - shared core terms `>= 2`
  - 或 shared `gmres` 且 target 暴露完整 `arnoldi + gmres + krylov + lanczos` 四词束
  - `block / matrix` 只作 supporting evidence，不单独升格 relation
- 当前 real-data runtime footprint 只命中 `3` 条 directed pair：
  - `global_105 -> global_140`
  - `global_140 -> global_9`
  - `global_9 -> global_140`

### 3. Supporting Branches Not Chosen First

#### Tensor / Low-Rank

- `global_13 -> global_149`
  - shared: `matrix`, `matrices`, `rank`, `tensor`
- `global_149 -> global_264`
  - shared: `algorithm`, `matrix`, `rank`, `tensor`

判断：

- 这是当前第二干净的一支
- 但比 Krylov 分支更容易和广义矩阵/低秩词混在一起
- 更适合作为第二阶段扩展，而不是第一条 rule contract

#### Inverse / Regularization

- `global_124 -> global_255`
  - `adjacent_to = 0.3860`
  - `evolves_from = 0.3860`
  - shared: `inverse`, `problems`, `regularization`

判断：

- 这是一个很干净的正例
- 但目前只有 1 对足够强的 pair，不足以单独承担第一条规则

### 4. Why Not Start From PDE / Galerkin / Polynomial Branches

几个“看起来很顺”的 pair 当前反而不适合做第一条规则主干：

- `global_23 -> global_62`
- `global_9 -> global_251`
- `global_9 -> global_391`
- `global_236 -> global_258`

共同问题是：

- representative evidence 出现 `5/5` identical title overlap
- 这更像 BERTopic split / duplicate-topic 风险，而不是稳定的 benchmark positive

判断：

- 这些 pair 不是“永远不能用”
- 但在第一轮 skeleton 里，把它们放进 active contract 风险高于收益

## Failure Modes

### 1. Duplicate-Topic Risk

`math.NA` 当前最明显的风险不是“完全没边”，而是若干 attractive pairs 可能只是近重复 split：

- `global_23 -> global_62`
- `global_9 -> global_251`
- `global_9 -> global_391`
- `global_236 -> global_258`

如果第一条规则建立在这些 pair 上，benchmark 会很脆。

### 2. Generic Solver Vocabulary Overlap

例如：

- `global_105 -> global_378`
- `global_140 -> global_90`

问题不是完全无关，而是 shared signal 只有：

- `approximation`
- `convergence`

这类词在 `math.NA` 里太宽，不能单独当 promotion signal。

### 3. Shallow Hierarchy

当前 `25/36` 个 topics 仍只挂在：

- `math.NA研究 > 偏微分方程数值方法`

这意味着：

- `tree_path` 可以作为弱证据
- 但第一条规则仍应优先依赖 exact method-family terms + edge evidence

### 4. No Event-Level Baseline Yet

当前 fixed positives 都更适合写成 `bridge-level`。

`global_140 -> global_9` 是最接近 event-level 的 case，但当前仍缺：

- 更稳定的 replay 命中
- 更明确的时间层基线

## Current Assessment

当前结论固定为：

- `math.NA` **benchmark-skeleton-ready**
- `math_na_krylov_iterative_continuity` 已作为保守 MVP 落地，状态应记为 `partial`
- 还不是 `runner-ready`
- 还没有 event-level baseline
- graph export 当前最多只应暴露 `bridge / boundary / review` narrative metadata；不应生成 NA baseline topology
- 当前 bridge-level contract 应固定为：
  - `na-b1 / na-b2` 为正例
  - `na-n1 / na-n2` 为负例
  - `na-a1` 保留 ambiguous，不进入第一轮 positive
- Claude review 结论支持当前口径：这是一条可信的保守 MVP；主要残余风险集中在单共享 `gmres` fallback，未来若遇到综述型 target 仍需复核

这轮不应说：

- `math.NA` 已经 ready
- `math.NA` 已经有稳定宽规则
- `PDE / approximation / solver` 整片都能统一处理

## Recommended Next Step

下一步更合理的工作包应是继续守住当前 contract，而不是立刻放宽。

目标：

- 先保持 `na-b1 / na-b2 / na-n1 / na-n2 / na-a1` 这一组 benchmark contract 稳定
- 继续观察单共享 `gmres` fallback 是否出现综述型误命中
- 在新增真实 positives 前，不要把 generic solver vocabulary 升成 promotion signal

额外约束：

- 不要从 generic `matrix` / `numerical` / `convergence` / `approximation` 开门
- 先回避 5/5 representative-title overlap 的 duplicate-prone pairs
