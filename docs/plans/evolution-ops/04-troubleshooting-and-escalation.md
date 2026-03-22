doc_type: "governance"
scope: "troubleshooting and escalation order for evolution-analysis work"
status: "active"
owner: "trend-monitor"
source_of_truth: true
upstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/README.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/.claude/plugins/evolution-delegation/config/guardrails.yaml"
downstream_docs: []
last_reviewed: "2026-03-18"

# Troubleshooting And Escalation

## Purpose

这份文档规定当 Claude / subagent 在执行演化规则任务时遇到问题，应该先检查什么、什么时候停止、什么时候升级给更强模型或人工。

## Golden Rule

默认顺序是：

1. 先查文档
2. 再查 benchmark
3. 再查 runner / code
4. 最后才 escalate

不要一遇到问题就自行改任务目标。

## Common Problem Types

### 1. Plugin / Skill 问题

症状：

- slash command 找不到 skill
- plugin 引用了不存在的 config
- completion gate 与当前任务类型不一致

检查顺序：

1. `.claude/plugins/evolution-delegation/plugin.yaml`
2. `.claude/plugins/evolution-delegation/config/guardrails.yaml`
3. `.claude/plugins/evolution-delegation/config/templates.yaml`
4. `.claude/skills/*/SKILL.md`

如果这 4 处有任何一处不存在或不一致，先修 plugin，不要继续动领域规则。

### 2. Benchmark 文档问题

症状：

- benchmark 文档与 registry 不一致
- benchmark 只有 synthetic case
- benchmark case 不够

检查顺序：

1. registry
2. review
3. benchmark 文档
4. 对应 benchmark spec

如果文档和 spec 不一致，优先交给 `doc-worker`。

### 3. Runner 问题

症状：

- `make math-xx-benchmark` 不存在
- runner 输出格式不一致
- runner 依赖不存在文件

检查顺序：

1. `Makefile`
2. `pipeline/math_xx_benchmark.py`
3. 相关测试
4. 输出目录

如果 domain 没有 runner，就不要把该 domain 放入 `supported_domains`。

### 3A. Data Baseline 问题

症状：

- wrapper 与 unified CLI 都能运行
- benchmark 测试通过
- 但 benchmark 报告中的 passed/failed 数量与另一个 worktree 或主目录不同

检查顺序：

1. 比较当前 worktree 与参考目录的 `data/output/aligned_topics_hierarchy.json` 时间戳
2. 分别运行 wrapper 与 unified CLI，确认两条路径结果是否一致
3. 只有在两条路径结果不一致时，才继续怀疑代码 regression

如果 wrapper 和 unified CLI 结果一致，默认优先判定为 **data-baseline issue**，不要继续修改 runner 代码。

### 4. 规则问题

症状：

- 正例打不准
- 负例误伤
- 规则和相邻规则重叠

检查顺序：

1. case 是否真实且边界清楚
2. benchmark 是否足够
3. review 是否解释了当前层级
4. 再看 rule 实现

如果 case 本身不清楚，不要先改规则。

## Stop Conditions

以下情况必须停止自动推进：

1. 找不到可信 positive case
2. 正例和负例只能靠一个泛词区分
3. benchmark 失败但原因不明
4. 新规则与已有规则边界明显重叠
5. 当前任务需要改动 `allowed_files` 之外的文件
6. 文档、benchmark、runner 三者严重不一致
7. benchmark 数字变化但尚未确认是否由数据版本差异导致

## Escalation Targets

### 升级给更强模型

适用情况：

- 需要重新定义数学对象 taxonomy
- 需要判断 bridge-level 是否应升级为 event-level
- 需要决定新子域优先级

### 升级给人工

适用情况：

- case 是否成立本身存在领域争议
- 当前数据源不足以支撑判断
- 需要决定项目策略，而不是局部规则实现

## What Not To Do When Blocked

阻塞时不要：

- 擅自改任务目标
- 擅自横向开新领域
- 擅自把 partial 写成 ready
- 用 synthetic case 代替真实 benchmark

## Minimal Recovery Procedure

如果某个任务包失败，恢复顺序固定为：

1. 记录失败命令
2. 记录失败 case
3. 记录已改文件
4. 回到 task package
5. 判断是否还能继续原包
6. 若不能，明确写出新的阻塞说明并停止

## Operator Shortcut

如果人工需要快速判断是否继续推进，只问这 4 个问题：

1. 这个任务包的 case 是否清楚
2. 这个任务包的 benchmark 是否存在
3. 这个任务包的 runner 是否存在
4. 这个任务包是否只改允许的文件

只要有 1 个答案是否，就不要继续自动推进。
