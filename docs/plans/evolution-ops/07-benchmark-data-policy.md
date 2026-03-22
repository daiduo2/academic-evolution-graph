doc_type: "governance"
scope: "benchmark data baseline and evidence policy"
status: "active"
owner: "trend-monitor"
source_of_truth: true
upstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/04-troubleshooting-and-escalation.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/06-generic-runner-implementation-packages.md"
downstream_docs: []
last_reviewed: "2026-03-18"

# Benchmark Data Policy

## Purpose

这份文档规定 benchmark 相关工作的数据基线、证据采集和结论书写方式。

目标是避免把：

- 数据版本变化
- worktree 与主目录的数据不一致
- 诊断性输出目录

误判成代码 regression。

## Core Principle

对 benchmark 数字变化，默认先问：

1. 输入数据是否相同
2. wrapper 与 unified CLI 的结果是否一致

只有在：

- 输入数据一致
- 且 wrapper 与 unified CLI 的结果不一致

时，才优先怀疑代码 regression。

## Baseline Types

### 1. Worktree Baseline

指当前执行目录中的输入数据与输出结果。

对本仓库，优先检查：

- `data/output/aligned_topics_hierarchy.json`
- `data/output/benchmarks/<domain>/`

worktree baseline 用于：

- 当前任务包验证
- 当前分支的局部回归判断

### 2. Reference Baseline

指主目录、主分支或最近稳定目录中的输入数据与 benchmark 结果。

例如：

- `/Users/daiduo2/claude-code-offline/academic-trend-monitor/data/output/aligned_topics_hierarchy.json`

reference baseline 用于：

- 判断当前 worktree 的数字差异是否来自旧数据
- 判断某次 benchmark 数字异常是否只是数据滞后

### 3. Policy Baseline

指文档中承认的“当前有效结论”。

例如：

- `math.AG unified CLI 与 wrapper 一致`
- `2/6 vs 6/6` 的差异来自数据版本不同

policy baseline 用于：

- 避免后续 worker 反复重新定位同一问题

## Required Evidence For Benchmark Diagnosis

当 benchmark 数字与预期不一致时，至少收集以下证据：

1. 当前 worktree 数据文件时间戳
2. 参考目录数据文件时间戳
3. wrapper 命令结果
4. unified CLI 命令结果
5. 是否存在额外诊断输出目录

推荐命令：

```bash
stat -f '%Sm %N' -t '%Y-%m-%d %H:%M:%S' data/output/aligned_topics_hierarchy.json
stat -f '%Sm %N' -t '%Y-%m-%d %H:%M:%S' /path/to/reference/data/output/aligned_topics_hierarchy.json
python3 pipeline/math_xx_benchmark.py
python3 pipeline/math_benchmark.py --domain math_xx
```

## Interpretation Rules

### Case A: Wrapper == Unified CLI, but numbers differ from reference

结论：

- 优先判定为 `data-baseline issue`
- 不要修改 runner 代码
- 需要记录数据时间戳差异

### Case B: Wrapper != Unified CLI, with same input data

结论：

- 优先怀疑 unified CLI 或 wrapper regression
- 可以进入代码排查

### Case C: Wrapper == Unified CLI, tests also pass, but benchmark not green

结论：

- 先看 benchmark 是否本来就不是 green baseline
- 不要自动假设是新回归

### Case D: 诊断时创建了额外 benchmark 输出目录

结论：

- 这些目录只属于临时证据
- 在结论写回文档后，应删除或明确忽略

## Writing Rule

写文档结论时，必须明确区分：

- `code regression`
- `data-baseline issue`
- `benchmark not yet green by design`

禁止使用模糊表述，例如：

- “benchmark 有点问题”
- “可能是 runner 造成的”

应写成可复用结论，例如：

- `wrapper 与 unified CLI 结果一致，差异来自数据版本`
- `当前 worktree 仍使用旧版 aligned_topics_hierarchy.json`

## Output Directory Policy

以下目录默认可保留：

- `data/output/benchmarks/math_lo/`
- `data/output/benchmarks/math_ag/`

以下目录若只用于临时诊断，应在结论确认后清理：

- `data/output/benchmarks/*_wrapper/`
- `data/output/benchmarks/*_unified/`
- 其他非正式 benchmark 证据目录

## Commit Policy

如果本轮结论是：

- 无需改代码
- 只需固化数据基线结论

则应创建一次 doc-only commit，并在提交说明中明确：

- 这不是 regression fix
- 这是 baseline closure / evidence closure

## Current Applied Example

`math.AG` 在 `PKG-UNI-02D-fix / PKG-UNI-02E` 中的结论是：

- worktree baseline 的 `aligned_topics_hierarchy.json` 较旧
- reference baseline 的数据较新
- wrapper 与 unified CLI 结果一致
- 因此 `2/6 passed` 属于 `data-baseline issue`，不是 unified CLI regression

## Non-Goals

这份文档不负责：

- 定义 benchmark case 本身
- 决定规则成熟度升级
- 决定是否引入新数学子域
