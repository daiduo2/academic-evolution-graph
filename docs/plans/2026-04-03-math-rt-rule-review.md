---
doc_type: "domain_review"
scope: "math > math.RT"
status: "active"
owner: "trend-monitor"
source_of_truth: true
upstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-11-evolution-doc-standards.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-10-evolution-rule-coverage.md"
downstream_docs: []
last_reviewed: "2026-03-22"
---

# Math.RT Rule Review

## Summary

`math.RT` 当前**不够启动第一版 benchmark skeleton**。

这轮扫描的结论不是“RT 完全没有任何候选”，而是：

- 当前数据里确实有一个窄支路看起来像起点：
  - `global_193 -> global_358`（`Lusztig / Hecke`）
- 但整个子域只有 `5` 个 topics，而且 `0` 个 multi-period topics
- 域内只有 `4` 条 `adjacent_to` 和 `1` 条 `evolves_from`
- 唯一内部 `evolves_from`（`global_177 -> global_358`）只共享泛词 `algebra`
- 因此今天还不能安全固定 `2 positive + 2 negative + 1 ambiguous` 的真实 case 集

本轮结论固定为：

- `math.RT` = `gap / insufficient data / not benchmark-ready`
- 本轮**不创建** benchmark skeleton

## Scope

本轮 review 只覆盖：

- `math > math.RT`
- 使用 [aligned_topics_hierarchy.json](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/data/output/aligned_topics_hierarchy.json) 与 [topic_graph.json](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/data/output/topic_graph.json) 的真实 topic / edge 证据
- 目标是回答：
  - `math.RT` 是否足够启动第一版 benchmark skeleton
  - 如果不够，短板主要卡在哪一层

## Rule Inventory

当前 `math.RT` 还没有已落地的 domain-specific 规则。

今天唯一接近“第一条窄方向种子”的分支是：

1. `Lusztig / Hecke continuity`（watchlist only）

但它现在还不能升格成 `planned`，原因很简单：

- 只有 1 个接近 positive 的 pair
- 没有第二个同级正例能支撑 skeleton
- 也没有足够干净的 ambiguous boundary 能稳定守边界

## Main Case Coverage

当前主产物 [evolution_cases.json](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/data/output/evolution_cases.json) 的自动案例里，`math.RT` 当前**没有命中**。

这说明：

- `math.RT` 还没有进入主事件叙事层
- 当前更适合做 gap closure，而不是 benchmark 固定

## Manual Replay Signals

### 1. Data Sufficiency Snapshot

当前 `math.RT` 的基础量化证据是：

- `5` 个真实 topics
- `0` 个 multi-period topics
- `4` 条域内 `adjacent_to`
- `1` 条域内 `evolves_from`

5 个 topics 分别是：

| Topic | Name | Period | active_periods | Path |
|-------|------|--------|----------------|------|
| `global_36` | 舒伯特上同调与幂零 | `2025-02` | `1` | `math.RT研究 > 李群与李代数的表示论` |
| `global_177` | 约当代数恒等式 | `2025-07` | `1` | `math.RT研究 > 李群与李代数的表示论` |
| `global_193` | Lusztig层与幺正范畴 | `2025-08` | `1` | `math.RT研究 > 几何表示论 > Lusztig理论` |
| `global_356` | Harish-Chandra GL(n) | `2026-02` | `1` | `math.RT研究 > 李群与李代数的表示论 > 约化群与p-adic群的表示 > Harish-Chandra理论` |
| `global_358` | Lusztig簇与Hecke表 | `2026-02` | `1` | `math.RT研究 > 李群与李代数的表示论 > 约化群与p-adic群的表示` |

判断：

- 这个规模仍明显低于 `math.CO / math.DS / math.NA`
- `0` 个 multi-period topics 意味着连最基本的“topic persistence”都还没出现
- 所以 RT 的问题不是“边太少”这么简单，而是**时间层完全撑不起来**

### 2. The Only Plausible Positive Watchlist

当前唯一接近正例的 pair 是：

- `global_193 -> global_358`
  - `Lusztig层与幺正范畴 -> Lusztig簇与Hecke表`
  - shared exact terms:
    - `lusztig`
    - `hecke`
  - internal `adjacent_to = 0.2778`
  - periods:
    - `2025-08 -> 2026-02`

这条 pair 的正向理由是：

- 它确实不像 generic representation overlap
- `Lusztig / Hecke` 已经是可命名的窄对象族
- 如果未来 RT 能重新打开，这大概率会是最先被重看的 seed branch

但它今天还不能承担 skeleton backbone，原因是：

- 没有 `evolves_from`
- 没有第二个同级正例
- target 所在的 `p-adic / reductive` 分支与 source 的 `几何表示论` 分支之间，当前还缺一个更稳的中间桥

### 3. Why the Only Internal evolves_from Is Not Usable as Positive

唯一内部 `evolves_from` 是：

- `global_177 -> global_358`
  - `约当代数恒等式 -> Lusztig簇与Hecke表`
  - `adjacent_to = 0.2868`
  - `evolves_from = 0.2868`
  - shared exact term only:
    - `algebra`

这条 pair 不能拿来当正例，原因是：

- `algebra` 在这个层级太宽
- source 核心对象是 `Jordan / Lie algebra identities`
- target 核心对象是 `Lusztig / Hecke / tableaux / p-adic`
- 这更像 graph noise 或 generic algebra spillover，而不是 representation-family continuity

它更适合作为一个**负向边界信号**：

- 提醒后续不要把 `algebra` 这类背景词升级成 promotion signal

### 4. Why Same-Period Structure Is Not Enough

`global_356 -> global_358` 看起来也很顺：

- 同属 `约化群与p-adic群的表示`
- internal `adjacent_to = 0.2993`
- shared exact term:
  - `adic`

但它仍不适合拿来做第一版骨架主干，因为：

- source / target 都只出现在 `2026-02`
- 这更像同月共现或并列邻域
- 不能承担“自然演化” bootstrap 所需的最小时间结构

### 5. Boundary Cases Exist, But Skeleton Still Fails

当前可以固定一些边界判断：

- `global_177 -> global_358`
  - 应拒绝作为 positive
  - 原因：只有 `algebra` 宽词
- `global_36 -> global_193`
  - 最多是 ambiguous watchlist
  - 原因：只有 `sheaves` overlap，且 `Schubert / nilpotent` 到 `Lusztig / perverse sheaf` 的跨支路解释仍偏宽
- `global_356 -> global_358`
  - 不能作为 bootstrap positive
  - 原因：same-period

问题在于：

- 这些边界信号并不能自动拼出 `2P/2N/1A`
- 当前最缺的是**第二个可信 positive**

## Failure Modes

### 1. Zero Multi-Period Persistence

`math.RT` 的 `5` 个 topics 全部只有 `1` 个 active period。

这意味着：

- 无法观察同一 topic 的跨期延续
- 无法提供 event-level baseline 的任何前体
- 任意 positive 都只能依赖 topic-to-topic graph inference

### 2. Sparse and Weak Internal Lineage

域内虽然有 `4` 条 `adjacent_to`，但只有 `1` 条 `evolves_from`。

而这唯一的 `evolves_from` 还只共享 `algebra` 这种宽词。

这说明：

- 图里不是完全没有连接
- 但当前连接强度不足以支撑 bootstrap skeleton

### 3. Branch Fragmentation

当前 `math.RT` 的 5 个 topics 分散在几种不同支路：

- `Schubert / nilpotent`
- `Jordan / Lie identities`
- `Lusztig / Hecke / character sheaf`
- `Harish-Chandra / p-adic GL(n)`

这些支路彼此之间还没有形成足够稳定的单一连续主干。

### 4. Representative Evidence Is Noisy

部分 topic 的 representative titles 与 RT 主对象并不稳定对齐，例如：

- `global_36` 的代表标题更像一般群论或有限群内容
- `global_193` 的代表标题更偏广义范畴 / 导出范畴语境

这进一步削弱了“今天就固定窄规则”的可信度。

## Current Assessment

当前结论固定为：

- `math.RT` = `gap / insufficient data`
- 不是 `benchmark-skeleton-ready`
- 本轮不应创建 benchmark 文档

更具体地说：

- topic 数量偏少，但还不是唯一问题
- 真正致命的是：
  - `0` 个 multi-period topics
  - 只有 `1` 条内部 `evolves_from`
  - 只有 `1` 个接近 positive 的窄支路

所以今天不能说：

- “RT 已经可以开始 benchmark”
- “第一条方向已经稳定”

今天最多只能说：

- 若未来 RT 重新打开，最值得重看的 seed 可能是：
  - `Lusztig / Hecke continuity`
- 但它目前仍只是 watchlist，不是 planned rule

## Recommended Next Step

当前不建议继续扩写 RT benchmark。

更合适的 reopen 条件是：

1. `math.RT` topics >= `8`
2. multi-period topics >= `3`
3. internal `evolves_from` >= `2`
4. 至少出现 `2` 个可信的跨期 positive pairs，且不能只靠 `algebra`, `representation`, `adic` 这类宽词区分
5. `Lusztig / Hecke` 或 `Harish-Chandra / character` 之类支路中，至少有 1 条能形成两段式链条，而不是孤立单对

在这些条件出现前：

- 不要创建 RT benchmark skeleton
- 不要把 RT 提升到 `planned`
- 保持 coverage 为 `gap`
