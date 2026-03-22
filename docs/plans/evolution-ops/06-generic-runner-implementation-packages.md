doc_type: "governance"
scope: "generic math benchmark runner implementation packages"
status: "active"
owner: "trend-monitor"
source_of_truth: true
upstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/05-math-benchmark-design.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/03-task-packages.md"
downstream_docs: []
last_reviewed: "2026-03-18"

# Generic Runner Implementation Packages

## Purpose

这份文档把原本过于粗粒度的 `PKG-UNI-02` 拆成更适合 Claude / subagent 执行的实现包。

原则：

- 不让弱模型在一个包里同时做抽象、迁移、测试、CLI
- 每个包只完成一个可以验证的实现步骤
- 每一步都保持 `math.LO` 和 `math.AG` 可回退

## Why Split PKG-UNI-02

原始 `PKG-UNI-02` 过大，包含了：

- 抽象通用 runner
- 改写 `math_lo_benchmark.py`
- 改写 `math_ag_benchmark.py`
- 新增统一测试
- 跑两个 domain benchmark

这对弱模型不够稳，容易出现：

- 一边抽象一边改行为
- wrapper 和底层一起坏
- benchmark 回归时难定位

因此，默认改成以下 4 个子包。

## Package UNI-02A

```yaml
package_id: "PKG-UNI-02A"
owner: "rule-worker"
tree_path: "math benchmark architecture"
task_type: "core_extraction"
target_rule: "math_benchmark.py"
goal: "抽取 LO / AG 共享逻辑到通用 core，但不改现有 wrapper 外部行为"
allowed_files:
  - "pipeline/math_benchmark.py"
  - "tests/test_math_benchmark.py"
required_commands:
  - "pytest tests/test_math_benchmark.py -q"
done_when:
  - "通用 core 文件存在"
  - "至少覆盖 evaluate_expected / build_neighbor_map / report builder 的共享逻辑"
  - "不要求 math_lo/math_ag wrapper 立刻迁移"
stop_if:
  - "需要修改 domain case 定义"
  - "需要改动 benchmark 文档语义"
```

## Package UNI-02B

```yaml
package_id: "PKG-UNI-02B"
owner: "rule-worker"
tree_path: "math benchmark architecture"
task_type: "wrapper_migration_lo"
target_rule: "math_lo_benchmark.py"
goal: "让 math_lo_benchmark.py 改为调用通用 core，保持输出兼容"
allowed_files:
  - "pipeline/math_benchmark.py"
  - "pipeline/math_lo_benchmark.py"
  - "tests/test_math_benchmark.py"
  - "tests/test_math_lo_benchmark.py"
required_commands:
  - "pytest tests/test_math_benchmark.py tests/test_math_lo_benchmark.py -q"
  - "make math-lo-benchmark"
done_when:
  - "math_lo wrapper 改为复用通用 core"
  - "math_lo benchmark 输出文件名和目录不变"
  - "math_lo benchmark 通过"
stop_if:
  - "math_lo case 语义发生变化"
```

## Package UNI-02C

```yaml
package_id: "PKG-UNI-02C"
owner: "rule-worker"
tree_path: "math benchmark architecture"
task_type: "wrapper_migration_ag"
target_rule: "math_ag_benchmark.py"
goal: "让 math_ag_benchmark.py 改为调用通用 core，保持 object-only contract 不变"
allowed_files:
  - "pipeline/math_benchmark.py"
  - "pipeline/math_ag_benchmark.py"
  - "tests/test_math_benchmark.py"
  - "tests/test_math_ag_benchmark.py"
required_commands:
  - "pytest tests/test_math_benchmark.py tests/test_math_ag_benchmark.py -q"
  - "make math-ag-benchmark"
done_when:
  - "math_ag wrapper 改为复用通用 core"
  - "method continuity 仍不进入 runner"
  - "math_ag benchmark 通过"
stop_if:
  - "需要把 method continuity 重新放回 runner"
```

## Package UNI-02D

```yaml
package_id: "PKG-UNI-02D"
owner: "rule-worker"
tree_path: "math benchmark architecture"
task_type: "unified_cli"
target_rule: "math_benchmark.py"
goal: "新增统一 CLI 入口，但不破坏现有 make 命令"
allowed_files:
  - "pipeline/math_benchmark.py"
  - "Makefile"
  - "tests/test_math_benchmark.py"
required_commands:
  - "pytest tests/test_math_benchmark.py -q"
  - "make math-lo-benchmark"
  - "make math-ag-benchmark"
done_when:
  - "支持 --domain math_lo"
  - "支持 --domain math_ag"
  - "现有 make 命令不变"
stop_if:
  - "LO 或 AG 任一 benchmark 回归"
```

## Post-UNI-02D Note

`PKG-UNI-02D-fix` 的结论已经明确：

- `math.AG` unified CLI 与 wrapper 结果一致
- worktree 2124 中的 `2/6 passed` 来自旧版 `data/output/aligned_topics_hierarchy.json`
- 这属于 **data-baseline issue**，不是 unified CLI regression

因此在继续推进前，不要再对 `math_benchmark.py` 做额外修复；若 benchmark 数字异常，先查输入数据版本。

## Package UNI-02E: Data Baseline Closure **[已完成 - 2026-03-18]**

```yaml
package_id: "PKG-UNI-02E"
owner: "doc-worker"
tree_path: "math benchmark architecture"
task_type: "data_baseline_closure"
target_rule: "math_benchmark.py | math_ag_benchmark.py"
goal: "记录 PKG-UNI-02D-fix 的结论：AG unified CLI 与 wrapper 一致，差异来自数据版本而非代码 regression"
evidence_collected:
  - timestamp: "2026-03-10 21:15:21"
    file: "data/output/aligned_topics_hierarchy.json"
    note: "当前 worktree 数据文件时间戳 (旧版本，与主目录 2026-03-17 不同)"
  - test_wrapper: "python3 pipeline/math_ag_benchmark.py"
    result: "2/6 passed"
  - test_unified_cli: "python3 pipeline/math_benchmark.py --domain math_ag"
    result: "2/6 passed"
  - consistency_check: "wrapper 与 unified CLI 结果完全一致"
conclusion: |
  1. wrapper 和 unified CLI 产生完全相同的 benchmark 结果
  2. 2/6 vs 6/6 的差异源于数据文件版本不同（2026-03-10 vs 2026-03-17）
  3. 这是 data-baseline issue，不是代码 regression
  4. 后续若 benchmark 数字异常，应先查数据时间戳
actions_completed:
  - ✅ "收集证据：数据文件时间戳"
  - ✅ "验证 wrapper benchmark 结果"
  - ✅ "验证 unified CLI benchmark 结果"
  - ✅ "确认两条路径结果一致"
  - ✅ "更新本文档记录结论"
completion_verify:
  - ✅ 本文档已更新 Post-UNI-02E Note
  - ✅ 结论可被后续 worker 直接复用
  - ✅ 无需修改 benchmark 文档语义或 case 定义
status: "✅ 已完成"
```

## Execution Order

固定顺序：

1. `PKG-UNI-02A`
2. `PKG-UNI-02B`
3. `PKG-UNI-02C`
4. `PKG-UNI-02D`
5. `PKG-UNI-02E`

不得跳步。

## Validation Rule

每做完一个包，都必须：

- 单独 commit
- 单独汇报
- 单独跑对应 domain 的 benchmark

不要把四个包揉成一轮执行。

## Non-Goals

这些包不负责：

- 引入第三个数学子域
- 重新定义 score 语义
- 修改 benchmark 文档里的规则状态
- 把 method continuity 加回 `math.AG` runner
