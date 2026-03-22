doc_type: "governance"
scope: "evolution-analysis execution playbook index"
status: "active"
owner: "trend-monitor"
source_of_truth: true
upstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-11-evolution-doc-standards.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-12-evolution-worker-playbook.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-12-evolution-skills-design.md"
downstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/01-read-first.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/02-two-week-roadmap.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/03-task-packages.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/04-troubleshooting-and-escalation.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/07-benchmark-data-policy.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/08-math-qa-bootstrap-package.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/09-math-ra-bootstrap-package.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/10-math-data-audit-package.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/11-math-pr-case-surfacing-package.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/12-math-knowledge-graph-package.md"
last_reviewed: "2026-03-18"

# Evolution Ops Docs

## Purpose

这个目录用于承载后续指导 Claude / subagent / 弱模型执行 `evolution-analysis` 工作的操作文档。

目标是让执行者在遇到问题时先读固定文档，而不是自行解释流程、补规则或改变范围。

## Read Order

任何自动化或半自动化执行者，进入数学演化规则工作前，默认按以下顺序阅读：

1. [01-read-first.md](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/01-read-first.md)
2. [02-two-week-roadmap.md](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/02-two-week-roadmap.md)
3. [03-task-packages.md](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/03-task-packages.md)
4. [04-troubleshooting-and-escalation.md](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/04-troubleshooting-and-escalation.md)
5. [05-math-benchmark-design.md](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/05-math-benchmark-design.md)
6. [06-generic-runner-implementation-packages.md](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/06-generic-runner-implementation-packages.md)
7. [07-benchmark-data-policy.md](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/07-benchmark-data-policy.md)
8. [08-math-qa-bootstrap-package.md](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/08-math-qa-bootstrap-package.md)
9. [09-math-ra-bootstrap-package.md](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/09-math-ra-bootstrap-package.md)
10. [10-math-data-audit-package.md](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/10-math-data-audit-package.md)
11. [11-math-pr-case-surfacing-package.md](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/11-math-pr-case-surfacing-package.md)
12. [12-math-knowledge-graph-package.md](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/12-math-knowledge-graph-package.md)

## Directory Role

这个目录不替代：

- registry
- domain review
- benchmark docs
- worker playbook

它的作用是：

- 固定近期推进目标
- 固定任务包
- 固定排障顺序
- 固定升级路径

## Current Strategy

当前总策略固定为：

1. 先稳定 plugin v1.0
2. 再把 `math.AG` 补成与 `math.LO` 同等级 benchmark 子域
3. 再抽象通用 `math_benchmark.py`
4. 先做数学数据完整性与对齐质量审计
5. 审计通过后，沿 `math.PR` 做 case surfacing，同时开始数学历史主题演化知识图谱 v1 设计

## Do Not Use This Directory For

不要把这个目录当作：

- 自由 brainstorming 区
- 临时 scratch notes 区
- 规则 registry 的替代品

如果某条规则已经稳定到需要长期维护，应更新：

- [2026-03-10-evolution-rule-coverage.md](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-10-evolution-rule-coverage.md)
- 对应 review
- 对应 benchmark

## Update Policy

后续每当以下事项发生变化时，应更新这个目录：

- 近两周推进优先级变化
- 新的 task package 被确认
- plugin / skill / benchmark runner 的执行边界变化
- 新的常见失败模式出现
