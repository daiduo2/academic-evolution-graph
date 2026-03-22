---
doc_type: "domain_review"
scope: "math > math.DS"
status: "active"
owner: "trend-monitor"
source_of_truth: true
upstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-10-evolution-rule-coverage.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-04-02-math-ds-benchmark.md"
downstream_docs: []
last_reviewed: "2026-03-22"
---

# Math.DS Rule Review

## Summary

`math.DS` 当前已经**足够启动第一版 benchmark skeleton**，并且**足够落地第一条 conservative MVP 规则**；但**还不够进入 runner-ready 阶段**。

这轮扫描的关键结论是：

- 域内真实 topic 数量已经足够：`22`
- multi-period topic 数量仍偏低：`3`
- 但内部图边并不稀薄：`49` 条 `adjacent_to`、`12` 条 `evolves_from`
- 可以固定一组真实 `2P / 2N / 1A`
- 当前最可能的第一条窄方向是：
  - `math_ds_ergodic_entropy_continuity`
- 它当前可以落地为 `partial / conservative MVP`，但不能跳成 `ready`

## Scope

本轮 review 只覆盖：

- `math > math.DS`
- 使用 `aligned_topics_hierarchy.json` 与 `topic_graph.json` 的真实 topic / edge 证据
- 目标是回答：
  - `math.DS` 能不能启动 benchmark skeleton？
  - 如果能，第一条最可能从哪条窄方向开始？

## Rule Inventory

当前 `math.DS` 已有 `1` 条已落地规则：

- `math_ds_ergodic_entropy_continuity`
  - status: `partial`
  - shape: conservative MVP
  - current gate: shared `entropy` + shared `ergodic` or `topological`
  - supporting-only evidence: `measure` / `measures`
  - excluded boundary: `ds-n1`, `ds-n2`, `ds-a1`

当前最可能的候选方向排序是：

1. `math_ds_ergodic_entropy_continuity`（implemented conservative MVP）
2. `math_ds_complex_dynamics_continuity`（secondary candidate）
3. `math_ds_hyperbolic_system_continuity`（secondary candidate）
4. `random / discrete process continuity`（deferred candidate）

判断依据不是“哪条数学上最重要”，而是哪条更适合先写成**窄而可防误判**的 benchmark contract。

## Main Case Coverage

当前主产物 [evolution_cases.json](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/data/output/evolution_cases.json) 里，`math.DS` 当前**没有自动命中的主事件案例**。

这说明：

- `math.DS` 目前还没有进入主事件叙事层
- 第一轮更适合先固定 benchmark skeleton，而不是直接尝试 runner baseline

## Manual Replay Signals

### 1. Data Substrate Is Thin But Usable

当前 `math.DS` 的基础统计是：

- total topics: `22`
- multi-period topics: `3`
- internal `adjacent_to`: `49`
- internal `evolves_from`: `12`
- hierarchy depth distribution:
  - depth 2: `17`
  - depth 3: `3`
  - depth 4: `2`
- with at least one internal `adjacent_to`: `21 / 22`
- with at least one internal `evolves_from`: `18 / 22`

判断：

- 这不是 `math.QA` / `math.RA` 那种“数据基底不成立”的 gap
- 但也不是 `math.CO` 那种已经有 7 个 multi-period topics 的更宽松状态
- 当前更适合走 “possible with care / benchmark skeleton first” 路径

### 2. Ergodic / Entropy Family Is The Best First Contract

当前最可信的一组真实 cases：

- `global_154 -> global_186`
  - shared keywords: `entropy`, `ergodic`, `measures`, `theorem`
  - same path: `math.DS研究 > 遍历理论与熵`
  - `adjacent_to = 0.4333`

- `global_154 -> global_367`
  - shared keywords: `entropy`, `measure`, `topological`
  - same path: `math.DS研究 > 遍历理论与熵`
  - `adjacent_to = 0.3955`
  - `evolves_from = 0.4355`

配套边界 cases：

- `global_119 -> global_367`
  - only shared `topological`
  - `adjacent_to = 0.3368`

- `global_12 -> global_154`
  - shared `measures`, `metric`
  - `adjacent_to = 0.35`

- `global_49 -> global_154`
  - shared `entropy`, `maps`, `measure`
  - `adjacent_to = 0.3955`
  - `evolves_from = 0.3955`

判断：

- 这组 evidence 已经足够支撑一个真实的 `2P / 2N / 1A`
- 它也给出一个很清楚的 first-rule intuition：
  - 不要从宽泛 `systems / maps` 起步
  - 应收窄到 `entropy` + `ergodic/topological` + `measure(s)` 这条线
- 本轮实际实现也已固定在这条最窄 gate 上：
  - promotion signal = shared `entropy` + shared `ergodic/topological`
  - supporting signal only = shared `measure(s)`
  - excluded from promotion = `systems`, `maps`, `random`, `process`

### 3. Secondary Clusters Exist, But Each Only Has One Clean Pair

当前还存在两组非常干净的 supporting positives：

- `global_234 -> global_266`
  - `复动力系统 > 有理映射与Julia集`
  - shared: `julia`, `maps`, `rational`, `set`
  - `adjacent_to = 0.475`
  - `evolves_from = 0.515`

- `global_254 -> global_288`
  - `光滑动力系统与双曲理论 > 双曲动力系统 > 双曲流与Anosov系统`
  - shared: `anosov`, `flows`
  - `adjacent_to = 0.3778`
  - `evolves_from = 0.4178`

这两组信号说明：

- `math.DS` 不只是一个单线子域
- 但如果今天就要选“第一条最可能方向”，它们各自都只有 1 对 clean positive
- 相比之下，`遍历理论与熵` 邻域更容易先固定为一个最小可解释 contract

### 4. Random / Discrete Process Is Present But Not Best As First Rule

例如：

- `global_37 -> global_289`
  - `随机最优控制 -> 强相互作用粒子过程`
  - shared: `particle`
  - `adjacent_to = 0.3292`
  - `evolves_from = 0.3292`

这类 pair 说明 `random / process` 支路不是完全没有信号。

但当前问题是：

- 证据过度依赖 `particle`, `process`, `stochastic`, `random` 这类宽词
- 很容易和概率/控制/相互作用粒子系统混写
- 因此更适合作为 deferred candidate，而不是第一条规则

## Failure Modes

### 1. Topological-Only Overlap

例如：

- `global_119 -> global_367`

`topological` 在 `math.DS` 里太宽，不能单独当作 promotion signal。

### 2. Measure / Metric Broad Overlap

例如：

- `global_12 -> global_154`

`measure(s)` / `metric` 这种词会把最优输运错误拉进遍历熵邻域。

### 3. Generic Systems / Maps Overlap

例如：

- `global_154 -> global_234`
- `global_234 -> global_323`

`systems` / `maps` 在 `math.DS` 里出现太广，适合做诊断信息，不适合第一条规则的准入条件。

### 4. Only Three Multi-Period Topics

当前 multi-period topics 只有：

- `global_12`
- `global_37`
- `global_154`

这意味着：

- `math.DS` 可以建立 skeleton
- 但很难像 `math.LO modal` 那样快速形成 event-level baseline

## Current Assessment

当前结论应固定为：

- `math.DS` 是 **benchmark-skeleton-ready**
- `math.DS` 不是 **gap**
- `math.DS` 还不是 **runner-ready**
- `math.DS` 当前最可能的第一条窄方向是：
  - `math_ds_ergodic_entropy_continuity`
- 该方向当前应标记为 `partial`
- 当前实际 runtime gate 是：shared `entropy` + shared `ergodic/topological`
- `measure(s)` 当前仅作 supporting evidence，不单独升格 relation
- 当前 positives 更适合统一描述为 `bridge-level`
- graph export 当前最多只应暴露 `bridge / boundary / review` narrative metadata；不应生成 DS baseline topology

## Recommended Next Step

如果下一包继续推进，建议严格按以下顺序：

1. 继续围绕 `ds-b1 / ds-b2 / ds-n1 / ds-n2 / ds-a1` 守住当前最小 contract
2. 不要为吸收 `ds-a1` 去放宽 `entropy + measure` 边界
3. 不要从 `systems`, `maps`, `random`, `process` 这类宽词开门
4. `global_234 -> global_266` 与 `global_254 -> global_288` 保留为第二阶段扩展支路，而不是并进当前 MVP gate

## Change Log

- `2026-03-22` (MDS-01)
  - 初版建立
  - 确认 `math.DS` 当前不是 gap，而是 benchmark-skeleton-ready
  - 固定第一批真实 DS cases：`2P / 2N / 1A`
  - 将第一条最可能方向收敛到 `math_ds_ergodic_entropy_continuity`
  - 明确 `complex dynamics` 与 `hyperbolic systems` 作为 secondary candidates 保留
- `2026-03-22` (MDS-FILL-02)
  - 将 `math_ds_ergodic_entropy_continuity` 落地为 conservative MVP
  - 当前 gate 固定为 shared `entropy` + shared `ergodic/topological`
  - `measure(s)` 明确降为 supporting evidence only
  - `ds-b1/ds-b2` 命中，`ds-n1/ds-n2` 拒绝，`ds-a1` 保持 ambiguous boundary
