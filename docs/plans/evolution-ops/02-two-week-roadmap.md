doc_type: "governance"
scope: "two-week execution roadmap for math evolution"
status: "active"
owner: "trend-monitor"
source_of_truth: true
upstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/README.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-12-math-worker-backlog.md"
downstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/03-task-packages.md"
last_reviewed: "2026-03-18"

# Two-Week Roadmap

## Goal

未来两周的目标不是横向增加更多数学规则，而是打通：

`math.LO -> math.AG -> 通用 runner`

只有这条复制链打通，后面才值得扩展到整个数学领域。

## Phase Summary

### Week 1

目标：

- 稳定 plugin v1.0
- 把 `math.AG` 补成和 `math.LO` 同级 benchmark 子域

### Week 2

目标：

- 抽象通用 `math_benchmark.py`
- 用 `LO + AG` 验证通用 runner
- 准备第三个数学子域 skeleton

## Detailed Plan

### Day 1

主题：plugin v1.0 收尾

任务：

- 校验 `.claude` 当前文件和 `supported_domains` 一致
- 补一份 operator checklist
- 演练一个 `doc-worker` 任务包
- 演练一个 `rule-worker` 任务包

完成标准：

- plugin 不再引用不存在 runner
- operator checklist 落地
- 至少 1 次本地 commit 演练

### Day 2

主题：`math.AG` benchmark 文档闭环

任务：

- 新建 `math.AG` benchmark 文档
- 固定 positive / negative / ambiguous case
- 明确 object continuity 与 method continuity 的边界

完成标准：

- `math.AG` benchmark 文档可单独使用
- synthetic evidence 不再被写成真实 benchmark

### Day 3

主题：`math.AG` benchmark spec

任务：

- 新建 `config/benchmarks/math_ag.yaml`
- 将文档中的 case 转为结构化 spec
- 补 `expected_relation / level / weight`

完成标准：

- spec 与 benchmark 文档一致
- 至少 3 positive、3 negative、1 ambiguous

### Day 4

主题：`math.AG` 可执行 benchmark runner

任务：

- 新建 `pipeline/math_ag_benchmark.py`
- 新建 `tests/test_math_ag_benchmark.py`
- 新增 `make math-ag-benchmark`

完成标准：

- `pytest tests/test_math_ag_benchmark.py -q` 通过
- `make math-ag-benchmark` 可生成报告

### Day 5

主题：`LO + AG` 双域对齐 review

任务：

- 对齐 benchmark 输出格式
- 对齐 score 语义
- 对齐报告结构

完成标准：

- `LO` 和 `AG` 的 benchmark 产物结构一致
- 文档、spec、runner 同步

### Day 6

主题：通用 runner 设计

任务：

- 设计 `pipeline/math_benchmark.py`
- 明确输入 / 输出 / score 字段
- 明确与 domain-specific runner 的关系

完成标准：

- 通用 runner 设计可直接开发

### Day 7

主题：通用 runner 初版

任务：

- 实现 `math_benchmark.py --domain math_lo`
- 实现 `math_benchmark.py --domain math_ag`

完成标准：

- 通用 runner 至少支持 `LO` 与 `AG`

### Day 8

主题：wrapper 收敛

任务：

- 让 `math_lo_benchmark.py` 成为 wrapper
- 让 `math_ag_benchmark.py` 成为 wrapper

完成标准：

- 旧命令不变
- 底层已统一

### Day 9

主题：数学数据完整性与对齐质量审计

任务：

- 审计各数学子域的 `topic_count / single_period_count / multi_period_count`
- 审计当前 anchor 选择门槛对数学子域的影响
- 解释 [evolution_cases.json](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/data/output/evolution_cases.json) 为什么只有 12 个代表案例
- 给出第三个数学子域是否值得 bootstrap 的明确建议

当前补充说明：

- `math.QA` 已因当前数据不足进入 gap 路径
- `math.RA` 已因当前数据不足进入 gap 路径
- 在继续推进 `math.RT` 之前，先做数据审计更稳

完成标准：

- 产出 math data audit 文档
- 明确区分：
  - 数据窗口问题
  - topic 对齐碎片化
  - anchor 选择过严
  - 代表案例摘要过少

### Day 10

主题：基于审计结果转入 `math.PR` case surfacing

任务：

- 不再推进 `math.RT`
- 先执行 `math.PR` 的 case surfacing
- 判断 `math.PR` 是否足以进入 curation
- 更新 task backlog 与 task packages

完成标准：

- `MPR-01B` 包已定义清楚
- `math.PR` 的下一步不是 runner，而是 explicit case surfacing
- `math knowledge graph v1` 设计包已启动

## Operational Rule

如果 Day 1-5 没完成，不要进入 Day 6-10。

也就是说，**没有 `math.AG` benchmark 闭环，就不要提前做全数学抽象。**

## Non-Goals During These Two Weeks

这两周不优先做：

- 新数学领域 ontology 顶层设计
- 新规则数量扩张
- `partial -> ready` 升级冲刺
- 非数学领域 benchmark

## Handoff Rule

任何一天的工作结束时，都应留下：

- 当前完成项
- 当前阻塞项
- 当前 git commit
- 明确下一步任务包编号
