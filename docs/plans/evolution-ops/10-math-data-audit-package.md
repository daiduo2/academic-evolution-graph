doc_type: "governance"
scope: "math data completeness and alignment quality audit package"
status: "active"
owner: "trend-monitor"
source_of_truth: true
upstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/03-task-packages.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/07-benchmark-data-policy.md"
downstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-12-math-worker-backlog.md"
last_reviewed: "2026-03-18"

# Math Data Audit Package

## Purpose

这份文档定义一个优先级高于新子域 bootstrap 的审计包。

目标不是扩新规则，而是先回答下面两个基础问题：

1. 为什么若干数学子域看起来“很空”
2. 为什么 [evolution_cases.json](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/data/output/evolution_cases.json) 只有 12 个案例

只有这两个问题先说清楚，我们后续再决定是推进 `math.RT`，还是先调整数据与案例选择策略。

## Current Findings

截至当前 worktree，已经确认：

- [aligned_topics_hierarchy.json](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/data/output/aligned_topics_hierarchy.json) 含有 13 个 periods，不是明显缺失整年窗口
- `math.QA`、`math.RA`、`math.RT` 之所以弱，不完全是时间窗口短，而是很多 topic 只有 1 个 active period
- [evolution_cases.json](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/data/output/evolution_cases.json) 不是全量事件库，而是默认 `--max-cases=12` 的代表性案例摘要
- anchor 还要通过额外筛选：`total_papers >= 60`、`active_periods >= 2`、`neighbors >= 2`、且要留出 horizon

这意味着当前最值的动作是做一次系统化审计，而不是继续按子域逐个试错。

## Package Definition

### PKG-MATH-AUDIT-01

```yaml
package_id: "PKG-MATH-AUDIT-01"
owner: "case-worker"
tree_path: "math data audit"
task_type: "data_completeness_and_alignment_audit"
target_rule:
  - "math bootstrap eligibility"
  - "evolution case selection policy"
goal: "审计数学子域的 topic 活跃度、跨期连续性、anchor 可入选率，以及 evolution_cases 摘要为何稀少"
allowed_files:
  - "docs/plans/evolution-ops/03-task-packages.md"
  - "docs/plans/evolution-ops/10-math-data-audit-package.md"
  - "docs/plans/2026-03-12-math-worker-backlog.md"
  - "docs/plans/2026-03-18-math-data-audit.md"
required_commands:
  - "make evolution-analysis"
  - "python3 pipeline/evolution_analysis.py --input data/output/aligned_topics_hierarchy.json --output-dir data/output/audit_math_cases --max-cases 100"
done_when:
  - "产出 math data audit 文档"
  - "至少覆盖所有 math subcategory 的 topic_count / single_period_count / multi_period_count"
  - "解释 evolution_cases.json 为何只有 12 个"
  - "给出下一步是推进 math.RT、调整 anchor 策略，还是继续 gap 的明确建议"
stop_if:
  - "需要修改 runner、tests 或 Makefile"
  - "需要新增 benchmark 文档来完成审计"
  - "需要引入 synthetic case 才能解释现象"
```

## Audit Questions

执行 `PKG-MATH-AUDIT-01` 时，必须回答：

1. 数学各子域各有多少 topics
2. 每个子域里单期 topic 与多期 topic 的比例是多少
3. 哪些子域存在可形成跨期演化对的 topic
4. 哪些子域即使 topic 数不少，但仍因单期过多而不适合 bootstrap
5. [evolution_cases.json](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/data/output/evolution_cases.json) 的 12 个案例是如何被筛出来的
6. 若把 `--max-cases` 放宽到更高值，数学 anchor 的数量会怎样变化
7. 当前空白更主要是：
   - 数据窗口问题
   - topic 对齐过碎
   - anchor 选择过严
   - 代表案例摘要导出太保守

## Required Outputs

执行者至少需要给出：

- 一个新的审计文档：
  - [2026-03-18-math-data-audit.md](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-18-math-data-audit.md)
- 一个简洁的子域表：
  - `subcategory`
  - `topic_count`
  - `single_period_count`
  - `multi_period_count`
  - `bootstrap_assessment`
- 一段关于 `evolution_cases.json` 仅 12 案例的机制说明
- 一条明确 next recommendation

## Decision Fork

### Option A

如果审计显示：

- `math.RT` 或其他候选子域具有 >= 4 个 topics
- 其中至少 >= 2 个是多期 topics
- 能形成真实跨期 anchor-target 候选

则下一步进入该子域的 bootstrap 包。

### Option B

如果审计显示：

- 多个候选子域虽然 topic 数不少，但大部分是单期 topic
- 主要瓶颈是对齐碎片化或 anchor 选择过严

则下一步优先调整数据/案例策略，而不是继续开新子域包。

## Non-Goals

这个包明确不做：

- 新增 `math_rt_benchmark.py`
- 新增 `math_rt` 或其他子域的 benchmark skeleton
- 直接改 registry 把某个 gap 子域拉回 active
- 修改 benchmark runner 代码

## Success Standard

完成后，后续执行者应能直接回答：

- 为什么 `math.QA`、`math.RA`、`math.RT` 看起来稀
- `evolution_cases.json` 为什么只有 12 个
- 第三个数学子域应该优先谁
- 是否应该优先改数据/案例策略，而不是继续扩子域
