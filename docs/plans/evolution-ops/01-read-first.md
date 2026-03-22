doc_type: "governance"
scope: "evolution-analysis mandatory reading order"
status: "active"
owner: "trend-monitor"
source_of_truth: true
upstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/README.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/AGENTS.md"
downstream_docs: []
last_reviewed: "2026-03-18"

# Read First

## Purpose

这份文档定义 Claude / subagent 在开始任何数学演化规则工作前，必须先阅读和确认的内容。

## Mandatory Reading Order

开始工作前，按顺序阅读：

1. [AGENTS.md](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/AGENTS.md)
2. [2026-03-11-evolution-doc-standards.md](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-11-evolution-doc-standards.md)
3. [2026-03-10-evolution-rule-coverage.md](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-10-evolution-rule-coverage.md)
4. 对应 `tree_path` 的 review 文档
5. 对应 `tree_path` 的 benchmark 文档
6. [2026-03-12-evolution-worker-playbook.md](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-12-evolution-worker-playbook.md)
7. [2026-03-12-evolution-task-template.md](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-12-evolution-task-template.md)
8. [2026-03-12-evolution-skills-design.md](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-12-evolution-skills-design.md)
9. [2026-03-12-math-worker-backlog.md](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-12-math-worker-backlog.md)
10. 当前目录下的 [02-two-week-roadmap.md](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/02-two-week-roadmap.md) 与 [03-task-packages.md](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/03-task-packages.md)
11. 如果任务涉及 benchmark 数字差异或 baseline 判断，阅读 [07-benchmark-data-policy.md](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/07-benchmark-data-policy.md)
12. 如果任务是 `math.QA` skeleton/bootstrap，阅读 [08-math-qa-bootstrap-package.md](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/08-math-qa-bootstrap-package.md)
13. 如果任务是 `math.RA` bootstrap，阅读 [09-math-ra-bootstrap-package.md](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/09-math-ra-bootstrap-package.md)
14. 如果任务涉及“为什么数学子域很空”或“为什么 evolution_cases 这么少”，阅读 [10-math-data-audit-package.md](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/10-math-data-audit-package.md)
15. 如果任务涉及 `math.PR` 的 case surfacing / curation 前置判断，阅读 [11-math-pr-case-surfacing-package.md](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/11-math-pr-case-surfacing-package.md)
16. 如果任务涉及数学历史主题演化知识图谱，阅读 [12-math-knowledge-graph-package.md](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/12-math-knowledge-graph-package.md)

## Required Confirmation Before Work

开始动手前，执行者应能回答：

1. 当前任务属于哪个 `tree_path`
2. 当前任务属于哪种 worker 类型
3. 当前任务允许改哪些文件
4. 当前任务必须跑哪些命令
5. 当前任务最多能把状态推进到哪里
6. 当前任务完成后必须更新哪些文档

如果不能回答以上 6 个问题，应停止并回到 task package，而不是自行继续。

## Current Global Priorities

当前优先级固定为：

1. 稳定 plugin v1.0
2. 把 `math.AG` 补成和 `math.LO` 同级 benchmark 子域
3. 抽象 `math_benchmark.py`
4. 只在 `LO + AG` 跑通后，先审计数学数据完整性与对齐质量
5. 审计通过后，再决定第三个数学子域

## Global Non-Goals

当前明确不做：

- 全数学领域同时铺开
- 没有 benchmark 的新领域自动扩张
- 自动系统自行决定规则成熟度升级
- 让弱模型定义新的数学本体顶层结构

## Required Working Style

执行者应默认遵守：

- 不使用开放式“继续推进”
- 不自己重新定义任务边界
- 不在没有真实 case 的情况下写出“规则已稳定”
- 不把 bridge-level 当 event-level
- 不在未 commit 的情况下宣称任务完成

## If Unsure

如果遇到不确定情况，默认顺序是：

1. 查 task package
2. 查 benchmark 文档
3. 查 review 文档
4. 查 troubleshooting 文档
5. 仍不清楚再 escalate
