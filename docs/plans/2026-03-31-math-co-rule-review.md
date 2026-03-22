doc_type: "domain_review"
scope: "math > math.CO"
status: "active"
owner: "trend-monitor"
source_of_truth: true
upstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-11-evolution-doc-standards.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-10-evolution-rule-coverage.md"
downstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-31-math-co-benchmark.md"
last_reviewed: "2026-03-22"

# Math.CO Rule Review

## Summary

`math.CO` 当前已经**足够启动第一版 benchmark skeleton**，并且已经**落地第一条窄规则 `math_co_matroid_structure_continuity` 的保守 MVP**，但**还不够进入 runner-ready / wide-rule-ready** 阶段。

这轮扫描的结论不是“已经找到稳定规则”，而是：

- 域内真实数据量已明显高于 `math.RA` / `math.QA`
- 可以固定第一批真实 cases（至少 2P / 2N / 1A）
- `math_co_matroid_structure_continuity` 已完成第一次窄实现并通过最小 replay contract
- `math_co_random_process_continuity` 暂不适合作为第一实现分支
- 当前 positives 主要停留在 `bridge-level`
- `math.CO` 还没有像 `math.LO modal` 那样的 `event-level baseline`

## Scope

本轮 review 只覆盖：

- `math > math.CO`
- 使用 `aligned_topics_hierarchy.json` 与 `topic_graph.json` 的真实 topic / edge 证据
- 目标是同步第一轮 benchmark / review 判断与 `MCO-FILL-01` 的实际落地结果

## Rule Inventory

当前 `math.CO` 已有 1 条**已实现但仍属 partial 的特化规则**：

1. `math_co_matroid_structure_continuity`

在此基础上，后续最可能的方向不是 `combinatorial method continuity`，而是更接近：

1. `math_co_matroid_structure_continuity`（已落地保守 MVP）
2. `math_co_random_process_continuity`（保留为第二候选，当前暂缓）
3. `discrete structure continuity`（总 umbrella，当前仍不建议直接宽实现）

## Main Case Coverage

当前主产物 [evolution_cases.json](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/data/output/evolution_cases.json) 的 12 个自动案例里，`math.CO` 当前**没有命中**。

这说明：

- `math.CO` 目前还没有进入主事件叙事层
- 第一轮更适合先固定 benchmark skeleton，而不是直接做 baseline demo

## Manual Replay Signals

### 1. Random Graph / Percolation Family

当前最可信的一组真实正例：

- `global_63 -> global_308`
  - `随机图顶点渗流 -> 随机渗流图马尔可夫`
  - shared keywords: `percolation`, `random`, `graphs`
  - same deep path: `math.CO研究 > 图论 > 随机图与过程 > 渗流`
  - `evolves_from` weight = `0.4235`

辅助支持：

- `global_130 -> global_187`
  - `随机图顶点分布 -> 随机图顶点概率模型`
  - shared keywords: `graph`, `graphs`, `random`
  - `adjacent_to` = `0.4235`
  - `evolves_from` = `0.4435`

判断：

- 这组 evidence 支持 `random graph / percolation continuity` 是可信候选支路
- 但当前最强 pair 仍主要是 `bridge-level`
- 原因不是语义太弱，而是 target 多为 single-period，且主案例层无 replay 命中
- 更关键的问题是 shared evidence 过度依赖 `random`, `graph(s)`, `vertex`, `threshold`, `degree` 这类高频图论词
- 在真实图边里，`global_63 -> global_71`、`global_187 -> global_365`、`global_130 -> global_8` 这类非目标 pair 也会共享同一批宽词
- 这意味着它更适合作为第二条规则，在第一条规则稳定后再补专门负例与 object gate

### 2. Matroid / Polytope / Poset Family

当前最可信的一组真实正例：

- `global_16 -> global_292`
  - `拟阵与欧拉多项式 -> 拟阵停车模式多面体`
  - shared keywords: `matroids`, `matroid`, `rank`, `polynomial`
  - `adjacent_to` = `0.4333`
  - `evolves_from` = `0.4733`

辅助支持：

- `global_292 -> global_319`
  - `拟阵停车模式多面体 -> 拟阵与多面体格`
  - shared keywords: `matroids`, `matroid`, `polytopes`, `poset`
  - `adjacent_to` = `0.3955`
  - `evolves_from` = `0.4355`

判断：

- 这组 evidence 说明 `math.CO` 的第一条窄规则更可能从 `matroid structure continuity` 起步
- 它更像对象/结构连续性，而不像方法迁移
- 相比 `random graph / percolation`，它的正例和负例都更容易写成 exact-object contract
- 当前也还没有 event-level baseline，但已经足够支撑第一条窄规则的保守 MVP 实现

### 3. MCO-02 Branch Decision

本轮必须在两个候选方向里做单一收敛判断。结论固定为：

- **第一实现分支选 `math_co_matroid_structure_continuity`**
- **`math_co_random_process_continuity` 暂缓**

原因：

1. `matroid` 支路有不止一个真实正例对，且 overlap 可以落在较窄的对象词上：
   - `global_292 -> global_319`: `matroid / matroids / polytopes`
   - `global_118 -> global_204`: `matroid / matroids / posets`
2. `matroid` 支路已经有直接可用的近失负例：
   - `global_292 -> global_324`: `rank / polynomial` overlap 不能提升成对象连续性
   - `global_8 -> global_319`: 一般图论宽词不能误拉进拟阵支路
3. `random / percolation` 支路虽然也有真实正例，但第一轮实现如果靠 `random + graph(s)` 起步，几乎一定会和一般图论 pair 混淆。
4. `matroid` 支路仍有一个需要先写清楚的边界：
   - `global_220 -> global_292` 只共享 `polytope / polytopes`，应保留为第一条规则的 near-miss，而不是仓促并入 matroid continuity。

### 4. MCO-FILL-01 Implementation Outcome

`MCO-FILL-01` 实际采用的是保守 family-normalized gate，而不是最宽的 exact-term 解释：

1. `anchor` 与 `target` 都必须位于 `math.CO`
2. 必须共享至少 1 个 `matroid-family` exact term
3. 对 `matroid / poset / polytope / lattice` 做 family normalization 后，必须覆盖至少 2 个离散结构 family
4. `rank / polynomial / graphs` 不作为 promotion signal

当前 replay 结果：

- positive: `global_292 -> global_319`, `global_118 -> global_204`
- negative: `global_292 -> global_324`, `global_8 -> global_319`
- near-miss rejected: `global_220 -> global_292`
- supporting bridge but still outside current gate: `global_16 -> global_292`

## Failure Modes

### 1. Generic Graph Vocabulary Overlap

例如：

- `global_8 -> global_319`

问题不是完全没联系，而是 shared terms 主要是 `graphs`, `conjecture`, `mathcal` 这类宽词。

这类 pair 很容易把一般图论主题误拉进拟阵/多面体支路，适合做第一批近失负例。

### 2. Generic Algebraic-Combinatorial Vocabulary Overlap

例如：

- `global_292 -> global_324`

两者有图边，也共享 `rank` / `polynomial`，但 target 已经进入 `matrices / determinant / permanental` 方向，不应被 matroid continuity 直接吸收。

这说明：

- `rank`
- `polynomial`
- `permutation`

这类词在 `math.CO` 里都过于宽泛，不能单独当作 promotion signal。

### 3. Polytope-Only Overlap Is Not Yet Matroid Continuity

例如：

- `global_220 -> global_292`

两者共享 `polytope / polytopes`，也有图邻接，但 source 没有 `matroid-family` exact term。

这类 pair 的价值在于：

- 它们可能属于未来更宽的 `discrete structure continuity`
- 但在第一条 `math_co_matroid_structure_continuity` 里应明确保持拒绝
- 否则第一条规则会从“拟阵对象连续性”滑成“任何多面体都算”

### 4. Hierarchy Is Still Too Shallow

当前 `math.CO` 的 hierarchy 深度分布是：

- depth 1: `43`
- depth 3: `1`
- depth 4: `3`

也就是说，`43/47` 个 topics 仍只挂在顶层 `math.CO研究`。

这意味着：

- deep path 可以作为加分证据
- 但不能像 `math.LO` 那样强依赖 tree_path 分支来切 rule

### 5. No Event-Level Baseline Yet

当前 `math.CO` 的真实正例足以启动 benchmark skeleton，但还没有任何一个 pair 能像 `math.LO modal` 那样稳定承担 event-level baseline 叙事。

### 6. MCO-FILL-02 Boundary Review

`MCO-FILL-02` 本轮单独复审了 `global_16 -> global_292` 是否值得并入当前 `math_co_matroid_structure_continuity`。

复审结论是：**不应并入当前 gate**。

决定性原因：

1. 当前 pair 的 shared discrete family 只有 `matroid`，并不满足现行 MVP 的“shared second structure family”口径。
2. target 虽然带有 `polytope / poset`，但这些都是 **target-only structure**，不是 shared structure continuity。
3. pair 还共享 `rank / polynomial`，但这类词当前只允许做背景 overlap；如果把它们抬成 promotion signal，会直接碰到 `co-mn1` 这条边界类型。
4. 当前 `pipeline_relation` 层并不以图边模式做 gate；若为了这一个 pair 把 `adjacent_to + evolves_from` 变成特判，也会把规则语义改成 bridge-absorption，而不是共享对象连续性。

因此，本轮更合理的做法不是“加厚 gate”，而是把它稳定登记为：

- supporting bridge outside gate

## Current Assessment

当前结论应固定为：

- `math.CO` 是 **benchmark-skeleton-ready**
- `math.CO` 已经进入 **first narrow rule implemented / partial**
- `math.CO` 还不是 **runner-ready / wide-rule-ready**
- 当前最可能的方向是 **discrete structure continuity**
- 但第一条实现规则应先收窄成 `math_co_matroid_structure_continuity`
- `math_co_random_process_continuity` 保留为下一候选，不在本轮先落代码
- `global_16 -> global_292` 经 `MCO-FILL-02` 复审后，固定为 supporting bridge outside gate，而不是 current rule positive

更务实的排序是：

1. 先守住当前 `math_co_matroid_structure_continuity` 的窄边界，不要回头把 `rank / polynomial` 或 `polytope-only` 放进来
2. 把 `global_16 -> global_292` 稳定记为 supporting bridge，不要在当前 rule 里混入 target-only structure 或 `rank/polynomial` 提升逻辑
3. `graph object vs spectral method` 与 `random / percolation` 继续保持 review-needed / deferred

## Graph-Facing Layers

围绕当前已落地的 matroid rule，`math.CO` 的 graph-facing 层次应明确拆成三层：

1. confirmed CO MVP
   - `co-m1`
   - `co-m2`
2. supporting bridge outside gate
   - `co-b2` / `global_16 -> global_292`
3. excluded boundary
   - `co-mn1`
   - `co-mn2`
   - `co-ma1`

这三层的含义分别是：

- 第一层：当前代码 gate 已确认吸收
- 第二层：语义上有价值，但不能靠 current rule contract 直接吸收
- 第三层：当前必须明确拒绝，避免 rule 语义滑宽

## Recommended Next Step

下一步不建议直接写一条宽泛的 `math.CO` 总规则，也不建议立刻把当前 gate 放宽。

更合理的是：

1. 保持 `co-m1`, `co-m2`, `co-mn1`, `co-mn2`, `co-ma1` 作为当前 active contract
2. 把 `global_16 -> global_292` 明确维持为 supporting bridge outside gate，不再把它描述成“只差 singular/plural normalization”
3. 根据已完成的代表 case 评估，优先审查 matroid alias coverage 与 single-structure false negative 风险，但不要把 target-only structure / `rank/polynomial` background 混进当前 gate
4. `random / percolation` 分支在补齐更窄 object vocabulary 和负例前，不进入下一轮实现

当前 Claude 代表 case 评估结论是：

- 当前边界作为 first MVP 是合理的
- 主要残余风险是 matroid 近义词/别名覆盖不足，以及 single-structure continuity 可能被 `>=2 family` gate 压掉

## Change Log

- `2026-03-22` (MCO-FILL-02)
  - 单独复审 `global_16 -> global_292`
  - 结论：当前不能安全吸收进 `math_co_matroid_structure_continuity`
  - 决定性原因：吸收它需要把 target-only structure、`rank/polynomial` 背景词或图边模式升级为 promotion signal
  - graph-facing 口径固定为：confirmed MVP / supporting bridge outside gate / excluded boundary
- `2026-03-22` (MCO-FILL-01)
  - `math_co_matroid_structure_continuity` 已按保守 MVP 落地
  - 当前实现采用 family-normalized gate：`matroid-family` + 第二维离散结构 family
  - replay contract 已通过：`co-m1`, `co-m2`, `co-mn1`, `co-mn2`, `co-ma1`
  - `global_16 -> global_292` 暂保留为 supporting bridge，不进入当前 gate
  - Claude 代表 case 评估支持当前 MVP 边界；主要残余风险是 vocabulary alias coverage 与 single-structure false negatives
- `2026-03-22` (MCO-02)
  - 明确收敛判断：第一实现分支选 `math_co_matroid_structure_continuity`
  - 明确 `math_co_random_process_continuity` 暂缓，原因是 generic graph/process vocabulary 误判风险更高
  - 固定 implementation-ready case contract：2P / 2N / 1 near-miss
  - 明确 `global_220 -> global_292` 为 polytope-only near-miss，不纳入第一条 matroid 规则
- `2026-03-22` (MCO-01)
  - 初版建立
  - 确认 `math.CO` 已足够启动 benchmark skeleton
  - 固定当前最可能的 rule direction 为 `discrete structure continuity`
  - 明确当前仍无 event-level baseline，不应直接进入宽规则实现
