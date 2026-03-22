---
doc_type: "benchmark"
scope: "math > math.DS"
status: "active"
owner: "trend-monitor"
source_of_truth: true
upstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-11-evolution-doc-standards.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-10-evolution-rule-coverage.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-04-02-math-ds-rule-review.md"
downstream_docs: []
last_reviewed: "2026-03-22"
---

# Math.DS Benchmark

## Purpose

这份文档固定 `math.DS` 的第一批真实 benchmark cases。

本轮目标不是宣布 `math.DS` 已经进入稳定 runner 阶段，而是把已经收敛出的第一条窄方向落成保守 MVP，并继续守住 benchmark contract。

本轮结论是：**足够启动 skeleton，也足够落第一条 conservative MVP；但还不够进入 runner-ready / event-level-baseline-ready 阶段。**

更具体地说：

- `math.DS` 当前有 `22` 个真实 topics
- 其中只有 `3` 个 multi-period topics
- 但域内图并不稀薄：`49` 条内部 `adjacent_to`，`12` 条内部 `evolves_from`
- 因此已经足够固定 `2 positive + 2 negative + 1 ambiguous`
- 当前最可能的第一条窄方向不是宽泛的 `dynamical-system continuity`，而是更窄的：
  - `math_ds_ergodic_entropy_continuity`（implemented / partial / conservative MVP）

## Scope

范围限定为：

- `math > math.DS`
- 当前 benchmark 继续固定第一批真实 cases，并同步约束第一条 conservative MVP gate
- 当前 benchmark skeleton 以 `遍历理论与熵` 邻域为主
- `复动力系统` 与 `双曲动力系统` 只作为 secondary supporting clusters 记录

## Case List

### Positive Cases

| Case ID | Anchor | Target | Likely Direction | Level |
|---------|--------|--------|------------------|-------|
| `ds-b1` | `global_154` 遍历动力系统定理 | `global_186` 遍历测度不等式 | `math_ds_ergodic_entropy_continuity` (partial MVP) | bridge-level |
| `ds-b2` | `global_154` 遍历动力系统定理 | `global_367` 奥野贝西科维奇拓扑熵 | `math_ds_ergodic_entropy_continuity` (partial MVP) | bridge-level |

### Positive Case Notes

- `ds-b1`（`global_154 -> global_186`）：
  - shared keywords: `entropy`, `ergodic`, `measures`, `theorem`
  - same path: `math.DS研究 > 遍历理论与熵`
  - internal `adjacent_to = 0.4333`
  - anchor 是当前少数 multi-period DS topics（`active_periods = 3`），target 仍是 single-period，因此当前先固定为 bridge-level positive，而不是 event-level baseline。

- `ds-b2`（`global_154 -> global_367`）：
  - shared keywords: `entropy`, `measure`, `topological`
  - same path: `math.DS研究 > 遍历理论与熵`
  - internal `adjacent_to = 0.3955`
  - internal `evolves_from = 0.4355`
  - 这个 pair 比 `ds-b1` 更像 “遍历/熵 -> 拓扑熵” 的局部伸展，因此很适合作为第一版 skeleton 的第二正例；但 target 同样只有 1 个 active period，仍应停留在 bridge-level。

### Negative Cases

| Case ID | Anchor | Target | Expected Relation |
|---------|--------|--------|-------------------|
| `ds-n1` | `global_119` 持续同调拓扑分析 | `global_367` 奥野贝西科维奇拓扑熵 | `none` |
| `ds-n2` | `global_12` 康托罗维奇最优输运 | `global_154` 遍历动力系统定理 | `none` |

### Negative Case Notes

- `ds-n1`（`global_119 -> global_367`）：
  - shared keyword 只有 `topological`
  - internal `adjacent_to = 0.3368`
  - 问题不在于完全没联系，而在于 source 是持续同调 / TDA 邻域，target 是拓扑熵邻域；`topological` 这种单个宽词不应被提升成 `math.DS` 连续性正例。

- `ds-n2`（`global_12 -> global_154`）：
  - shared keywords: `measures`, `metric`
  - internal `adjacent_to = 0.35`
  - 两者都还是 multi-period topic，但 source 的核心对象是最优输运 / Wasserstein / Kantorovich，target 的核心对象是遍历系统 / mixing / entropy；`measure` / `metric` 这类宽词和 broad-path 共处，不足以支撑对象连续性。

### Ambiguous Cases

| Case ID | Anchor | Target | Current Status | Note |
|---------|--------|--------|----------------|------|
| `ds-a1` | `global_49` 分形熵测度 | `global_154` 遍历动力系统定理 | review-needed | fractal/measure branch 与 ergodic-entropy branch 的边界未定 |

### Ambiguous Case Notes

- `ds-a1`（`global_49 -> global_154`）：
  - shared keywords: `entropy`, `maps`, `measure`
  - internal `adjacent_to = 0.3955`
  - internal `evolves_from = 0.3955`
  - 正向理由是：fractal measure / expansive attractor 研究与 ergodic entropy 理论确实共享熵与测度对象。
  - 反向理由是：source 更像分形/几何测度邻域，target 更像遍历理论/符号动力系统邻域；如果第一条规则直接把这类 pair 收进来，`entropy + measure` 会变得过宽。
  - 当前更适合保留为真实 ambiguous case，而不是仓促定成 positive。

## Expected Relations

- `ds-b1` 应支持当前 conservative MVP gate `math_ds_ergodic_entropy_continuity`
- `ds-b2` 应支持当前 conservative MVP gate `math_ds_ergodic_entropy_continuity`
- `math.DS` 当前可以说是 benchmark-skeleton-ready，但不能说有 runner-ready baseline

## Expected Non-Relations

- `ds-n1` 不能因为共享 `topological` 就被提升成 `math.DS` 连续性
- `ds-n2` 不能因为共享 `measure(s)` / `metric` 就被提升成 `math.DS` 连续性
- `ds-a1` 当前不能直接写死成 positive 或 negative；必须保留 review-needed

## Review Notes

- 当前 skeleton 已满足最小要求：`2 positive + 2 negative + 1 ambiguous`
- 所有 case 都来自真实 `math.DS` topics 与图边，不依赖 synthetic case
- 当前 positives 都是 `bridge-level`
- `math.DS` 还没有像 `math.LO modal` 那样的 event-level baseline
- 图谱导出层当前最多只应把这些 case 暴露成 graph-facing narrative metadata：`bridge + boundary + review`；不应写成 baseline topology
- 当前最可能的第一条方向更像 **ergodic / entropy continuity**，不是宽泛的 `dynamical-system continuity`
- 当前实际 gate 已固定为：共享 `entropy` 且同时共享 `ergodic` 或 `topological`
- `measure` / `measures` 当前只作为 supporting evidence 输出，不参与单独升格
- `ds-a1` 继续保留为 benchmark 内的真实 ambiguous boundary，不进入第一轮 positive
- `复动力系统` 与 `双曲动力系统` 也各自有一组很干净的正例：
  - `global_234 -> global_266`
  - `global_254 -> global_288`
- 但它们目前都只各自提供 1 对强正例；相比之下，`遍历理论与熵` 邻域更容易先固定成一个最小 `2P/2N/1A` contract

## Change Log

- `2026-03-22` (MDS-01)
  - 初版建立
  - 固定第一批真实 `math.DS` benchmark cases：`2P / 2N / 1A`
  - 确认 `math.DS` 当前已足够启动 benchmark skeleton
  - 确认当前 positives 仍以 bridge-level 为主，暂无 event-level baseline
  - 将第一条最可能方向收敛到 `math_ds_ergodic_entropy_continuity`（provisional / not implemented）
- `2026-03-22` (MDS-FILL-02)
  - 明确 graph export 语义：可进 metadata-only narrative，不进 baseline topology
  - 将 `math_ds_ergodic_entropy_continuity` 落地为 conservative MVP
  - runtime gate 固定为 shared `entropy` + shared `ergodic/topological`
  - `measure(s)` 固定为 supporting evidence only
  - 验证 `ds-b1/ds-b2` 通过，`ds-n1/ds-n2` 拒绝，`ds-a1` 保持 boundary ambiguous
