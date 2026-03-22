doc_type: "design"
scope: "math > math.CO first implementation-ready rule plan"
status: "active"
owner: "trend-monitor"
source_of_truth: true
upstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-10-evolution-rule-coverage.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-31-math-co-rule-review.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-31-math-co-benchmark.md"
downstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/pipeline/evolution_analysis.py"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/tests/test_evolution_analysis.py"
last_reviewed: "2026-03-22"

# Math.CO First Rule Plan

## Purpose

这份文档把 `math.CO` 的第一条窄规则收敛成 implementation-ready 计划，并记录 `MCO-FILL-01` 的实际落地口径。

当前目标不是继续讨论“要不要实现”，而是固定已经落地的保守 MVP 边界，并说明哪些 supporting cases 仍暂留在 gate 外。

## Scope

本计划只覆盖：

- `tree_path = math > math.CO`
- 第一条窄规则：`math_co_matroid_structure_continuity`
- 最小实现边界、最小测试边界、以及本轮明确拒绝的 overlap

本计划不覆盖：

- `math_co_random_process_continuity`
- 宽泛的 `math_co_general_continuity`
- 任何 benchmark runner / frontend / cross-domain 逻辑

## Branch Selection

单一结论固定为：

- 先实现 `math_co_matroid_structure_continuity`
- 暂缓 `math_co_random_process_continuity`

理由：

1. `matroid` 支路已经有多组真实 exact-object positives，可写成窄 contract。
2. `matroid` 支路已有直接可用的 negatives，能防住 `rank / polynomial` 和 `graphs` 这两类宽词误判。
3. `random / percolation` 支路当前太依赖 `random`, `graph(s)`, `vertex`, `threshold`, `degree`，容易和一般图论 pair 混淆。
4. 第一条规则应优先验证“对象 gate 是否能守住边界”，而不是先去处理 process-family 的泛词噪声。

## Landed MVP Decision

`MCO-FILL-01` 最终选择**直接落代码，但只落保守 MVP**。原因有两个：

1. 当前最早的 matroid 正例 `global_16 -> global_292`，在 exact-keyword 口径下较依赖 `matroid / matroids` 这一组 singular-plural 重复；因此实际实现不把 singular/plural 当作两个独立 family。
2. `global_220 -> global_292` 这样的 polytope-only near-miss 已经存在；如果不把第二维结构 family 写死，第一条规则会直接做宽。

因此，当前落地口径固定为：

- `co-m1` / `co-m2` 通过
- `co-mn1` / `co-mn2` / `co-ma1` 拒绝
- `global_16 -> global_292` 暂保留为 supporting bridge，不进入当前 MVP gate

## MCO-FILL-02 Boundary Decision

`MCO-FILL-02` 对 `global_16 -> global_292` 的单独复审结论固定为：

- **不扩当前 gate**
- **不改代码**
- `global_16 -> global_292` 固定为 supporting bridge outside gate

决定性原因：

1. 当前 pair 只共享 `matroid` 这 1 个离散结构 family。
2. 想把它并入 current rule，必须额外借用 target-only 的 `polytope / poset`，或者借用 `rank / polynomial` 这类背景词。
3. 这会把当前规则从 shared-structure continuity 推向 bridge-absorption 逻辑，不再是 `MCO-FILL-01` 固定的 MVP contract。

因此，`MCO-FILL-02` 的正确产物不是“补一个特判 positive”，而是把它在 graph-facing 叙事里稳定登记出来。

## Implementation Contract

### Positive Cases

| Case ID | Pair | Required Outcome | Why It Matters |
|---------|------|------------------|----------------|
| `co-m1` | `global_292 -> global_319` | `math_co_matroid_structure_continuity` | MVP positive；共享 `matroid / matroids / polytopes`，同时有 `adjacent_to` 和 `evolves_from` |
| `co-m2` | `global_118 -> global_204` | `math_co_matroid_structure_continuity` | supporting positive；共享 `matroid / matroids / posets`，体现 matroid-family 内部结构延续 |

### Negative Cases

| Case ID | Pair | Required Outcome | Rejection Reason |
|---------|------|------------------|------------------|
| `co-mn1` | `global_292 -> global_324` | `none` | `rank / polynomial` overlap 不能当作 matroid continuity |
| `co-mn2` | `global_8 -> global_319` | `none` | 一般图论宽词不能把超宽 graph topic 拉进 matroid 支路 |

### Ambiguous / Near-Miss

| Case ID | Pair | Required Outcome For First Rule | Why It Stays Near-Miss |
|---------|------|---------------------------------|------------------------|
| `co-ma1` | `global_220 -> global_292` | `none` | 共享 `polytope / polytopes`，但 source 不在 matroid-family；若未来要吸收，应由更宽的 rule 负责 |

### Supportive But Not MVP

| Pair | Current Role | Note |
|------|--------------|------|
| `global_16 -> global_292` | supporting bridge outside gate | 真实 matroid bridge evidence 保留；但它只有 `matroid` shared family。若并入当前 gate，必须借用 target-only structure 或 `rank/polynomial` 背景词，因此不纳入第一轮 MVP contract |

## Trigger Sketch

`MCO-FILL-01` 实际实现使用以下最小 gate：

1. `anchor` 与 `target` 都位于 `math.CO`。
2. 共享至少 1 个 `matroid-family` exact term：
   - `matroid`
   - `matroids`
   - `polymatroid`
3. 对以下 `math.CO` discrete-structure terms 做 family normalization 后，必须覆盖至少 2 个 family：
   - `matroid`
   - `matroids`
   - `polymatroid`
   - `poset`
   - `posets`
   - `polytope`
   - `polytopes`
   - `lattice`
   - `lattices`
4. 以下词不能单独作为 promotion signal：
   - `rank`
   - `polynomial`
   - `polynomials`
   - `permutations`
   - `graph`
   - `graphs`

实现含义：

- `co-m1` / `co-m2` 应通过
- `co-mn1` / `co-mn2` / `co-ma1` 应拒绝
- `global_16 -> global_292` 当前应继续停留在 gate 外；`MCO-FILL-02` 已确认不应靠 target-only structure 或 `rank/polynomial` 背景词把它抬进来

## Minimal Test Plan

`MCO-FILL-01` 已落地的最小测试集分成两层。

### Synthetic Unit Tests

1. positive:
   - shared `matroid`, `matroids`, `polytopes`
   - 期望 relation = `math_co_matroid_structure_continuity`
2. negative:
   - shared `rank`, `polynomial`
   - 期望 relation = `none`
3. negative:
   - shared `graphs`
   - target 带 matroid 词，anchor 不带
   - 期望 relation = `none`
4. near-miss:
   - shared `polytope`, `polytopes`
   - 无 shared matroid-family term
   - 期望 relation = `none`

### Real Replay Test

已增加一组 replay contract，最少覆盖：

- `co-m1`
- `co-m2`
- `co-mn1`
- `co-mn2`
- `co-ma1`

另加一个 supporting boundary test：

- `global_16 -> global_292` 当前保持 `none`

## Files Changed In MCO-FILL-01

- `pipeline/evolution_analysis.py`
- `tests/test_evolution_analysis.py`
- `docs/plans/2026-03-10-evolution-rule-coverage.md`
- `docs/plans/2026-03-31-math-co-rule-review.md`
- `docs/plans/2026-03-31-math-co-benchmark.md`
 - `docs/plans/2026-04-01-math-co-first-rule-plan.md`

## Implementation Checklist

```yaml
task_type: "new_rule"
tree_path: "math > math.CO"
target_rule: "math_co_matroid_structure_continuity"
change_goal: "Implement a narrow matroid-family continuity gate and reject rank/polynomial-only and polytope-only overlaps"
positive_case:
  anchor: "global_292"
  target: "global_319"
  expected_relation: "math_co_matroid_structure_continuity"
negative_case:
  anchor: "global_292"
  target: "global_324"
  expected_relation: "none"
benchmark_case_ids:
  - "co-m1"
  - "co-m2"
  - "co-mn1"
  - "co-mn2"
  - "co-ma1"
code_files:
  - "pipeline/evolution_analysis.py"
test_files:
  - "tests/test_evolution_analysis.py"
doc_files:
  - "docs/plans/2026-03-10-evolution-rule-coverage.md"
  - "docs/plans/2026-03-31-math-co-rule-review.md"
  - "docs/plans/2026-03-31-math-co-benchmark.md"
commands_to_run:
  - "pytest tests/test_evolution_analysis.py -q"
  - "make test"
claude_review_mode: "pending"
claude_prompt_summary: "Evaluate co-m1 positive, co-mn1 negative, co-ma1 near-miss after first code implementation lands"
git_commit_message: "feat(math-co): add first matroid continuity rule"
completion_status: "implemented_partial"
```

## Stop Conditions

后续如果出现以下情况，应停止继续放宽这条规则：

- 只能靠 `rank` 或 `polynomial` 才能让正例通过
- 需要把 `polytope-only` pair 一并吸收才能维持正例数量
- `random / graph` 宽词开始进入 trigger sketch
- real replay 中 `co-mn1` 或 `co-ma1` 任何一个被误判成 positive

## Next Step

下一轮不需要再重复第一轮实现；更合理的是：

1. 保持当前 family-normalized gate，不要为了补图把 `polytope-only` 或 `rank/polynomial` overlap 放进来
2. 用代表 case 继续校准 `co-m1`, `co-mn1`, `co-ma1` 的边界描述，但不要把 supporting bridge 误写成 current rule positive
3. 把 `global_16 -> global_292` 固定放在 graph-facing 的 supporting bridge outside gate 层
4. 如果未来要吸收它，应单独设计 bridge-level gate 或更宽的结构连续性规则，而不是回改当前 MVP
5. `random / percolation` 分支继续 deferred，直到有更窄 object vocabulary 和负例
