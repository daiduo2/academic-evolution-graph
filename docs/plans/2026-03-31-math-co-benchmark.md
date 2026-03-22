doc_type: "benchmark"
scope: "math > math.CO"
status: "active"
owner: "trend-monitor"
source_of_truth: true
upstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-11-evolution-doc-standards.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-10-evolution-rule-coverage.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-31-math-co-rule-review.md"
downstream_docs: []
last_reviewed: "2026-03-22"

# Math.CO Benchmark

## Purpose

这份文档固定 `math.CO` 的第一批真实 benchmark cases。

目标不是宣布 `math.CO` 已经有稳定规则，而是回答一个更早的问题：

- 当前数据是否已经足够支撑 benchmark skeleton？

本轮结论是：**足够建立 skeleton，也足够让第一条窄规则以保守 MVP 方式落地；但还不够宣布任何一条规则 ready，也还不够进入 runner-ready。**

## Scope

范围限定为：

- `math > math.CO`
- 固定真实 cases，并记录 `MCO-FILL-01` 已落地的第一条窄规则 contract
- 当前 benchmark skeleton 仍保留两个候选支路：
  - `random graph / percolation`
  - `matroid / polytope / poset`
- `MCO-02` 已选定第一实现分支为：
  - `math_co_matroid_structure_continuity`

## Case List

### Positive Cases

| Case ID | Anchor | Target | Likely Direction | Level |
|---------|--------|--------|------------------|-------|
| `co-b1` | `global_63` 随机图顶点渗流 | `global_308` 随机渗流图马尔可夫 | `math_co_random_process_continuity` (provisional) | bridge-level |
| `co-b2` | `global_16` 拟阵与欧拉多项式 | `global_292` 拟阵停车模式多面体 | `math_co_matroid_structure_continuity` (provisional) | bridge-level |

### Positive Case Notes

- `co-b1`（`global_63 -> global_308`）：这是当前 `math.CO` 中最干净的 `random graph / percolation` 正例。两者同属 `渗流` 深路径，shared keywords 包含 `percolation`, `random`, `graphs`，且存在 `evolves_from`（weight=`0.4235`）。但两者都只有 1 个 active period，因此当前只能固定为 bridge-level，不足以承担 event-level baseline。
- `co-b2`（`global_16 -> global_292`）：这是当前最可信的 `matroid structure` 正例。两者共享 `matroids`, `matroid`, `rank`, `polynomial`，同时有 `adjacent_to`（`0.4333`）与 `evolves_from`（`0.4733`）。target 已经从拟阵多项式扩展到停车模式/多面体方向，结构连续性真实存在；但 target 仍是 single-period，因此同样先记为 bridge-level。

### Negative Cases

| Case ID | Anchor | Target | Expected Relation |
|---------|--------|--------|-------------------|
| `co-n1` | `global_292` 拟阵停车模式多面体 | `global_324` 矩阵置换与积和式 | `not math_co_matroid_structure_continuity` |
| `co-n2` | `global_8` 图与顶点条件研究 | `global_319` 拟阵与多面体格 | `none` |

### Negative Case Notes

- `co-n1`：`global_292 -> global_324`。两者有 `adjacent_to`（`0.3778`）和 `evolves_from`（`0.4178`），也共享 `rank` / `polynomial`。但 target 的核心对象已经转向 `matrices / determinant / permanental`，没有 `matroid / polytopes / poset` 这类核心离散对象延续。这是很有价值的近失负例：测试的是“generic algebraic-combinatorial vocabulary”边界，而不是主题完全错位。
- `co-n2`：`global_8 -> global_319`。两者图邻接（`0.3778`），也共享 `graphs`, `conjecture`, `mathcal` 等宽词，但 anchor 是超宽的图论/顶点条件主题，target 是拟阵-多面体-格结构主题。这个负例的价值在于：它防止后续规则把一般图论热词误拉进拟阵支路。

### Ambiguous Cases

| Case ID | Anchor | Target | Current Status | Note |
|---------|--------|--------|----------------|------|
| `co-a1` | `global_71` 凯莱图与群结构 | `global_365` 图拉普拉斯特征值 | review-needed | graph object continuity 与 spectral method continuity 的边界未定 |

### Ambiguous Case Notes

- `co-a1`：`global_71 -> global_365`。两者共享 `graph`, `graphs`, `vertex`，同时有 `adjacent_to`（`0.3955`）和 `evolves_from`（`0.4355`）。正向理由是：Cayley graph 本来就是谱图理论的重要对象，图拉普拉斯谱可以看成图对象连续性的自然延伸。反向理由是：target 更像一般性的谱方法/矩阵方法主题，而不是 Cayley graph 特有对象延续。当前应保留为真实 ambiguous case，而不是仓促定成 positive。

## MCO-02 First Rule Contract

`MCO-02` 的单一结论固定为：

- 第一实现分支：`math_co_matroid_structure_continuity`
- 暂缓分支：`math_co_random_process_continuity`

原因不是 `random / percolation` 完全没有正例，而是它在当前 `math.CO` 数据里过度依赖 `random`, `graph(s)`, `vertex`, `threshold`, `degree` 这类宽词；如果把它放到第一条规则，false positive 风险高于 `matroid` 支路。

### Selected Contract Cases

| Case ID | Anchor | Target | Expected Relation | Status |
|---------|--------|--------|-------------------|--------|
| `co-m1` | `global_292` 拟阵停车模式多面体 | `global_319` 拟阵与多面体格 | `math_co_matroid_structure_continuity` | positive |
| `co-m2` | `global_118` 拟阵热带偏序集 | `global_204` 拟阵偏序集及提升 | `math_co_matroid_structure_continuity` | positive |
| `co-mn1` | `global_292` 拟阵停车模式多面体 | `global_324` 矩阵置换与积和式 | `not math_co_matroid_structure_continuity` | negative |
| `co-mn2` | `global_8` 图与顶点条件研究 | `global_319` 拟阵与多面体格 | `none` | negative |
| `co-ma1` | `global_220` 凸多胞形邻接性 | `global_292` 拟阵停车模式多面体 | `review-needed / near-miss` | ambiguous |

### Selected Contract Notes

- `co-m1`：`global_292 -> global_319` 是当前最适合做第一实现分支 MVP positive 的 pair。它同时共享 `matroid`, `matroids`, `polytopes`，并且同时存在 `adjacent_to`（`0.3955`）与 `evolves_from`（`0.4355`）。相比 `global_16 -> global_292`，它不必主要依赖 singular/plural 重复来构成两项 exact overlap。
- `co-m2`：`global_118 -> global_204` 是第二个更窄的 matroid-family positive。两者共享 `matroid`, `matroids`, `posets`，target 还进入更深的 `拟阵理论 > 拟阵偏序集` 路径，适合做支持性正例。
- `co-mn1`：`global_292 -> global_324` 必须保持拒绝。共享 `rank / polynomial` 不足以说明拟阵对象连续性；target 已转向 `matrices / determinant / permanental`。
- `co-mn2`：`global_8 -> global_319` 必须保持拒绝。`graphs / vertices / conjecture` 这类一般图论宽词不能把超宽图论主题拉进 matroid 支路。
- `co-ma1`：`global_220 -> global_292` 是本轮最重要的 near-miss。两者共享 `polytope / polytopes` 且有图邻接，但 source 没有 `matroid-family` exact term。第一条规则必须拒绝它；如果未来要吸收它，应通过更宽的 `discrete structure continuity` 或单独 `polytope continuity` 完成。
- `global_16 -> global_292` 仍保留为真实 matroid bridge positive，但**不建议把它当成第一条规则的最小单元测试 pair**，因为它当前更依赖 `matroid / matroids` 这一组 singular-plural exact overlap；在没有先写清楚 normalization 口径前，不如先用 `co-m1` / `co-m2` 做 MVP contract。

### MCO-FILL-01 Landed MVP

`MCO-FILL-01` 实际落地的是一个**比 implementation-ready sketch 更保守**的 MVP gate：

1. `anchor` 与 `target` 都位于 `math.CO`
2. 共享至少 1 个 `matroid-family` exact term
3. 对 `matroid / poset / polytope / lattice` 做 singular/plural family normalization 后，必须覆盖至少 2 个离散结构 family
4. `rank / polynomial / graphs` 只作为背景 overlap，不单独提升 relation

实际结果固定为：

- `co-m1` / `co-m2` 通过
- `co-mn1` / `co-mn2` / `co-ma1` 拒绝
- `global_16 -> global_292` 继续保留为 bridge-level supporting positive，但**不进入当前 MVP gate**

### MCO-FILL-02 Supporting Bridge Review

`MCO-FILL-02` 本轮只审查一个问题：

- `global_16 -> global_292` 能否在**不放宽** `co-mn1` / `co-mn2` / `co-ma1` 边界的前提下安全吸收进当前 gate？

结论固定为：

- **不能安全吸收**
- **当前 gate 保持不变**
- `global_16 -> global_292` 固定为 **supporting bridge outside gate**

决定性原因不是这对 pair 不真实，而是它在当前关键词口径下只共享 1 个离散结构 family：

- shared discrete family 只有 `matroid`
- target 额外带有 `polytope / poset`，但这些是 **target-only structure**
- pair 还共享 `rank / polynomial`，但这类词在当前 contract 中只能当背景 overlap，不能升级成 promotion backbone

也就是说，如果要把它并入当前 `math_co_matroid_structure_continuity`，必须额外引入以下至少一种新 promotion signal：

1. target-only 结构 family
2. `rank / polynomial` 背景词
3. 图边模式（如 `adjacent_to + evolves_from`）作为 rule gate

这三种做法都会把当前规则从“shared structure continuity MVP”推向更宽的 bridge-absorption 口径，因此不应在本轮混入。

### Current Graph-Facing Layers

围绕当前 `math_co_matroid_structure_continuity`，`math.CO` 的 graph-facing 层次应固定为：

- confirmed CO MVP:
  - `co-m1`
  - `co-m2`
- supporting bridge outside gate:
  - `co-b2` / `global_16 -> global_292`
- excluded boundary:
  - `co-mn1`
  - `co-mn2`
  - `co-ma1`

补充说明：

- `co-b1`（`global_63 -> global_308`）仍属于 deferred 的 `random / percolation` 支路，不进入这张 matroid-rule graph-facing 三层图。

## Expected Relations

- `co-b1` 应支持未来的 `math_co_random_process_continuity`
- `co-b2` 应支持未来的 `math_co_matroid_structure_continuity`
- `co-m1` 应作为 `math_co_matroid_structure_continuity` 的首要 MVP positive
- `co-m2` 应作为 `math_co_matroid_structure_continuity` 的第二正例

## Expected Non-Relations

- `co-n1` 不能因为共享 `rank` / `polynomial` 就被提升成 `math_co_matroid_structure_continuity`
- `co-n2` 不能因为共享一般图论宽词（如 `graphs`, `conjecture`）就被提升成 `math.CO` 连续性正例
- `co-a1` 当前不能直接写死成 positive 或 negative；必须保留 review-needed
- `co-mn1` 在第一条规则里必须保持拒绝
- `co-mn2` 在第一条规则里必须保持拒绝
- `co-ma1` 在第一条规则里必须保持拒绝；它是 future broader rule 的 near-miss，不是当前 matroid rule 的 positive

## Review Notes

- 当前 skeleton 已满足最小要求：`2 positive + 2 negative + 1 ambiguous`
- 所有 case 都来自真实 `math.CO` topics 与图边，不依赖 synthetic case
- 当前 positives 主要是 `bridge-level`，还没有 event-level baseline
- `math.CO` 当前最可能的方向更像 **discrete structure continuity**，不是 `combinatorial method continuity`
- 但第一条实现规则大概率要拆成窄支路，而不是直接做一条宽泛 umbrella rule
- hierarchy 仍偏浅（`43/47` topics 只在顶层 `math.CO研究`），因此 benchmark 里应优先相信 exact object / edge evidence，而不是过度依赖 path 标签
- `MCO-02` 已把第一实现分支固定为 `math_co_matroid_structure_continuity`
- `MCO-FILL-01` 已把第一条窄规则落到代码，并通过最小 synthetic + real replay contract
- 当前实际 gate 故意保守：`global_16 -> global_292` 仍在规则外，因为吸收它需要把 target-only structure 或 `rank/polynomial` 背景词升级为 promotion signal
- `MCO-FILL-02` 已完成 supporting bridge 审查：`global_16 -> global_292` 暂不吸收，原因是吸收它需要把 target-only structure 或 `rank/polynomial` 背景词升级为 promotion signal
- `random / percolation` 分支保留为后续候选，但不应在第一条规则里和 matroid 支路一起混写

## Change Log

- `2026-03-22` (MCO-FILL-02)
  - 审查 `global_16 -> global_292` 是否可并入当前 `math_co_matroid_structure_continuity`
  - 结论：当前不能安全吸收；保留为 supporting bridge outside gate
  - 决定性原因：pair 只有 `matroid` shared family；若要升级，必须借用 target-only structure 或 `rank/polynomial` 背景词
  - 固定 graph-facing 三层：confirmed MVP = `co-m1/co-m2`；supporting bridge outside gate = `co-b2`；excluded boundary = `co-mn1/co-mn2/co-ma1`
- `2026-03-22` (MCO-FILL-01)
  - `math_co_matroid_structure_continuity` 已以保守 MVP 方式落地到代码
  - 当前实现采用 family-normalized gate：要求 `matroid-family` + 第二维离散结构 family
  - 验证通过：`co-m1`, `co-m2` positive；`co-mn1`, `co-mn2`, `co-ma1` negative
  - 明确 `global_16 -> global_292` 仍是 bridge-level supporting positive，但不进入当前 MVP gate
- `2026-03-22` (MCO-02)
  - 选定第一实现分支为 `math_co_matroid_structure_continuity`
  - 新增 implementation-ready contract：`co-m1`, `co-m2`, `co-mn1`, `co-mn2`, `co-ma1`
  - 明确 `global_16 -> global_292` 仍是支持性正例，但不作为第一轮最小单元测试 pair
  - 明确 `math_co_random_process_continuity` 作为 deferred candidate 保留
- `2026-03-22` (MCO-01)
  - 初版建立
  - 固定第一批真实 `math.CO` benchmark cases：2P / 2N / 1A
  - 确认 `math.CO` 当前已足够启动 benchmark skeleton
  - 确认当前 positives 仍以 bridge-level 为主，暂无 event-level baseline
