---
doc_type: "benchmark"
scope: "math > math.NA"
status: "active"
owner: "trend-monitor"
source_of_truth: true
upstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-11-evolution-doc-standards.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-10-evolution-rule-coverage.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-04-03-math-na-rule-review.md"
downstream_docs: []
last_reviewed: "2026-03-22"
---

# Math.NA Benchmark

## Purpose

这份文档固定 `math.NA` 的第一批真实 benchmark cases。

本轮目标不是宣布 `math.NA` 已经有稳定规则，而是先回答一个更早的问题：

- 当前数据是否已经足够支撑第一版 benchmark skeleton？

本轮结论是：**足够启动 skeleton，也足够落第一条保守 MVP，但还不够进入 runner-ready / event-level-baseline-ready 阶段。**

更具体地说：

- `math.NA` 当前有 `36` 个真实 topics
- 其中有 `7` 个 multi-period topics
- 域内图并不稀薄：`86` 条内部 `adjacent_to`，`18` 条内部 `evolves_from`
- 因此已经足够固定 `2 positive + 2 negative + 1 ambiguous`
- 当前最可能的第一条窄方向不是泛 `numerical-method continuity`
- 更像：
  - `math_na_krylov_iterative_continuity`（implemented / partial）
  - 当前 runtime gate 只允许两类命中：
    - shared `gmres / krylov / lanczos / arnoldi` `>= 2`
    - 或 shared `gmres`，且 target 暴露完整 `arnoldi + gmres + krylov + lanczos` 四词束

## Scope

范围限定为：

- `math > math.NA`
- 当前既固定第一批真实 benchmark cases，也同步首条 conservative MVP gate
- 当前 benchmark skeleton 以 `matrix / Krylov iterative` 邻域为主
- `tensor / low-rank` 与 `inverse / regularization` 只作为 secondary supporting clusters 记录

## Case List

### Positive Cases

| Case ID | Anchor | Target | Likely Direction | Level |
|---------|--------|--------|------------------|-------|
| `na-b1` | `global_105` GMRES数值近似法 | `global_140` 块特征值与Krylov方法 | `math_na_krylov_iterative_continuity` | bridge-level |
| `na-b2` | `global_140` 块特征值与Krylov方法 | `global_9` 块矩阵迭代算法加速 | `math_na_krylov_iterative_continuity` | bridge-level |

### Positive Case Notes

- `na-b1`（`global_105 -> global_140`）：
  - shared exact term: `gmres`
  - `adjacent_to = 0.3292`
  - `evolves_from = 0.3692`
  - current gate reason: 单共享词 fallback 只在 target 暴露完整 `arnoldi + gmres + krylov + lanczos` 四词束时放行
  - Why positive: `GMRES` 本身就是 `Krylov subspace` 迭代法的具体成员，这条 pair 反映的是“单一迭代法 -> 更一般 Krylov family” 的窄连续性，而不是 generic numerical-method overlap。

- `na-b2`（`global_140 -> global_9`）：
  - shared exact terms: `block`, `gmres`, `krylov`, `lanczos`, `matrix`
  - `adjacent_to = 0.4400`
  - source / target 均为 multi-period
  - current gate reason: 共享 core terms `gmres + krylov + lanczos`，已经满足 `shared core >= 2`
  - Why positive: 这条 pair 是当前 `math.NA` 里最强的 `matrix / Krylov iterative` 主干，方法族从 block eigenvalue / Krylov 扩展到 block matrix acceleration，连续性明显，但当前仍缺 event-level baseline 证据，因此先固定为 bridge-level。
  - note: `block / matrix` 仍只作为 supporting evidence 输出，不单独升格 relation。

### Negative Cases

| Case ID | Anchor | Target | Expected Relation |
|---------|--------|--------|-------------------|
| `na-n1` | `global_105` GMRES数值近似法 | `global_378` 核插值与逼近方法 | `not math_na_krylov_iterative_continuity` |
| `na-n2` | `global_140` 块特征值与Krylov方法 | `global_90` 蒙特卡洛马尔可夫链 | `none` |

### Negative Case Notes

- `na-n1`（`global_105 -> global_378`）：
  - shared keyword 只有 `approximation`
  - `adjacent_to = 0.3368`
  - `evolves_from = 0.3368`
  - Why negative: `GMRES` 迭代法与 kernel interpolation 虽都属于数值方法，但 `approximation` 是过宽的 NA 背景词，不能把插值/核逼近直接拉进 Krylov 连续性。

- `na-n2`（`global_140 -> global_90`）：
  - shared keyword 只有 `convergence`
  - `adjacent_to = 0.3250`
  - source / target 均为 multi-period
  - Why negative: Krylov / eigenvalue 迭代法与 MCMC / Hamiltonian sampling 是不同的算法族；`convergence` 只能说明都讨论数值行为，不能说明 method lineage。

### Ambiguous Cases

| Case ID | Anchor | Target | Current Status | Note |
|---------|--------|--------|----------------|------|
| `na-a1` | `global_86` 矩阵范数与平方 | `global_307` 量子张量基态算法 | review-needed | `krylov` overlap 是否足以跨到量子张量应用侧，边界未定 |

### Ambiguous Case Notes

- `na-a1`（`global_86 -> global_307`）：
  - shared keyword: `krylov`
  - `adjacent_to = 0.3368`
  - `evolves_from = 0.3368`
  - 正向理由是：target 仍显式保留 `krylov`，说明 Krylov subspace 技术可能确实在应用侧延续。
  - 反向理由是：target 的核心对象已经转向 `quantum / tensor / hamiltonian / ground state`，如果第一条规则直接吸收它，`krylov` 单词本身会被放得过宽。
  - current gate reason: 单共享 `krylov` 不足以过线；首轮 MVP 不允许因为单个非 `gmres` core term 就放行。
  - 当前更适合保留为真实 ambiguous case，而不是仓促定成 positive。

## Expected Relations

- `na-b1` 应命中当前已实现的 `math_na_krylov_iterative_continuity`
- `na-b2` 应命中当前已实现的 `math_na_krylov_iterative_continuity`
- 当前 gate 必须继续保持：
  - `gmres / krylov / lanczos / arnoldi` 是唯一 promotion core
  - `matrix / block` 只作为 supporting evidence
- `math.NA` 当前可以说是 benchmark-skeleton-ready，但不能说已有 runner-ready baseline

## Expected Non-Relations

- `na-n1` 不能因为共享 `approximation` 就被提升成 `math.NA` 连续性
- `na-n2` 不能因为共享 `convergence` 就被提升成 `math.NA` 连续性
- `na-a1` 当前不能因为共享单个 `krylov` 就被提升成 positive；必须保留 review-needed

## Review Notes

- 当前 skeleton 已满足最小要求：`2 positive + 2 negative + 1 ambiguous`
- 所有 case 都来自真实 `math.NA` topics 与图边，不依赖 synthetic case
- 当前 positives 都更适合写成 `bridge-level`
- `math.NA` 还没有像 `math.LO modal` 那样的 event-level baseline
- 图谱导出层当前最多只应把这些 case 暴露成 graph-facing narrative metadata：`bridge + boundary + review`；不应写成 baseline topology
- 当前最可能的第一条方向更像 **matrix / Krylov iterative continuity**，不是泛 `PDE solver continuity` 或 `approximation / discretization continuity`
- `MNA-FILL-02` 后的 runtime footprint 目前只命中 `3` 条 directed pair：
  - `global_105 -> global_140`
  - `global_140 -> global_9`
  - `global_9 -> global_140`
- `tensor / low-rank` 与 `inverse / regularization` 也各自有 clean positives：
  - `global_13 -> global_149`
  - `global_149 -> global_264`
  - `global_124 -> global_255`
- 但它们当前更适合作为 supporting clusters，而不是第一条 rule contract
- 当前应明确回避几组 duplicate-prone pair，它们出现 `5/5` representative-title overlap：
  - `global_23 -> global_62`
  - `global_9 -> global_251`
  - `global_9 -> global_391`
  - `global_236 -> global_258`
- Claude review 结论：当前 gate 是可信的保守 MVP；`na-b1/na-b2` 应保留为正例，`na-n1/na-n2/na-a1` 应继续留在门外；主要残余风险是单共享 `gmres` fallback 在未来遇到综述型 target 时可能需要再加 anchor-side 限制。

## Change Log

- `2026-03-22` (MNA-FILL-02)
  - 落地 `math_na_krylov_iterative_continuity` 的保守 MVP
  - 固定 runtime gate：`shared core >= 2`，或 `shared gmres + target full four-term bundle`
  - 明确 `matrix / block` 仅作 supporting evidence，不参与 promotion
  - 单元测试与 real replay contract 确认：
    - `na-b1/na-b2` 通过
    - `na-n1/na-n2` 拒绝
    - `na-a1` 仍保留在第一轮 positive 之外
  - 记录 Claude case review 结论与 fallback residual risk

- `2026-03-22` (MNA-01)
  - 初版建立
  - 固定第一批真实 `math.NA` benchmark cases：`2P / 2N / 1A`
  - 确认 `math.NA` 当前已足够启动 benchmark skeleton
  - 确认当前 positives 仍以 bridge-level 为主，暂无 event-level baseline
  - 将第一条最可能方向收敛到 `math_na_krylov_iterative_continuity`（planned / not implemented）
