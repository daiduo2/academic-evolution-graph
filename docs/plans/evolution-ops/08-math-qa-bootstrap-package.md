doc_type: "governance"
scope: "detailed bootstrap package for math.QA benchmark skeleton"
status: "active"
owner: "trend-monitor"
source_of_truth: true
upstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/03-task-packages.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/07-benchmark-data-policy.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-10-evolution-rule-coverage.md"
downstream_docs: []
last_reviewed: "2026-03-18"

# Math.QA Bootstrap Package

> Current note:
> `PKG-QA-01` 已因当前 worktree 中 `math.QA` 数据过稀而触发 stop condition。
> 继续工作时，优先执行：
> - `PKG-QA-01A` gap normalization
> - `PKG-QA-01B` longer-window exploration
> 只有在 `01B` 证明值得恢复时，才重新回到 bootstrap skeleton。

## Purpose

这份文档为 `math > math.QA` 提供第一个较长但仍然强约束的任务包。

与早期 `LO / AG` 不同，这个包不要求一步到位实现 runner。它的目标是：

1. 建立 `math.QA` 的 benchmark skeleton
2. 固定第一批真实候选 case
3. 明确哪些候选只是 test evidence
4. 为后续 spec / runner 留下稳定接口

## Why This Package Is Intentionally Longer

`math.LO` 和 `math.AG` 已经帮我们跑通了：

- registry
- review
- benchmark
- runner
- data-baseline closure

因此 `math.QA` 不必再用非常碎的小包去试错。  
但这不意味着开放式推进。这个包仍然必须：

- 只改文档与 skeleton
- 不新增 runner
- 不新增统一 CLI 逻辑
- 不自行宣布 `ready`

## Current Decision Status

根据当前 worktree 的探索结果：

- `math.QA` 只发现 2 个 topics
- 其中只有 1 个 topic 具有较长 period history
- `evolution_cases` 中没有 `math.QA` 相关样例

因此当前默认结论是：

- 先做 `gap normalization`
- 再决定是否值得做 `longer-window exploration`
- 暂不直接重跑 bootstrap skeleton

## Package Identity

```yaml
package_id: "PKG-QA-01"
owner: "case-worker"
tree_path: "math > math.QA"
task_type: "benchmark_skeleton_bootstrap"
target_rule:
  - "math_qa_object_continuity"
  - "math_qa_method_continuity"
goal: "建立 math.QA benchmark skeleton，并固定第一批候选正负例与边界说明"
```

## Scope

### In Scope

- 初步整理 `math.QA` 的对象连续性候选
- 初步整理 `math.QA` 的方法连续性候选
- 新建 `math.QA` benchmark 文档骨架
- 在 registry 中为 `math.QA` 留出位置
- 记录 benchmark-ready / test-evidence-only / unclear 的边界

### Out Of Scope

- 不实现 `math_qa_benchmark.py`
- 不新增 `make math-qa-benchmark`
- 不新增 `config/benchmarks/math_qa.yaml`
- 不定义最终 score
- 不把 `math.QA` 直接升成 `ready`

## Allowed Files

```yaml
allowed_files:
  - "docs/plans/2026-03-10-evolution-rule-coverage.md"
  - "docs/plans/2026-03-12-math-worker-backlog.md"
  - "docs/plans/evolution-ops/03-task-packages.md"
  - "docs/plans/evolution-ops/08-math-qa-bootstrap-package.md"
  - "docs/plans/2026-03-18-math-qa-benchmark.md"
```

## Required Reading

执行前必须阅读：

1. `AGENTS.md`
2. `docs/plans/evolution-ops/01-read-first.md`
3. `docs/plans/evolution-ops/03-task-packages.md`
4. `docs/plans/evolution-ops/04-troubleshooting-and-escalation.md`
5. `docs/plans/evolution-ops/07-benchmark-data-policy.md`
6. `docs/plans/2026-03-10-evolution-rule-coverage.md`
7. `docs/plans/2026-03-12-math-worker-backlog.md`

## Required Commands

```yaml
required_commands:
  - "make evolution-analysis"
  - "rg -n \"math\\.QA|quantum|representation|crystal|categor\" data/output/aligned_topics_hierarchy.json data/output/evolution_cases.json"
```

说明：

- `make evolution-analysis` 用于刷新当前可见的 topic / evolution 上下文
- `rg` 只用于帮助定位 QA 候选，不构成 benchmark 证据本身

## Suggested QA Ontology Hints

这不是最终 ontology，只是第一轮搜索提示。

### Candidate Object Hints

- quantum group / quantum groups
- affine algebra / quantum affine
- representation / representations
- crystal / crystal basis
- Hall algebra
- cluster algebra / cluster structure
- vertex algebra / VOA
- quiver / quiver variety

### Candidate Method Hints

- categorification
- crystal / canonical basis
- braid / tensor category
- q-deformation
- geometric representation
- cluster / mutation
- Hall algebra methods

### Negative-Side Confusers

以下情况优先作为 negative 或 ambiguous：

- 只共享 `representation`
- 只共享 `quantum`
- 只是在 `math.QA` 子树内，但没有清楚的对象或方法连续性

## Work Phases

### Phase 1: Candidate Harvest

目标：

- 收集 `math.QA` 子树下的候选 topic pair

要求：

- 至少列出 6 个候选 pair
- 分成：
  - candidate positive
  - candidate negative
  - candidate ambiguous

### Phase 2: Boundary Classification

目标：

- 判断每个候选更像：
  - `object_continuity`
  - `method_continuity`
  - `test_evidence_only`
  - `unclear`

要求：

- 每个候选必须写一句理由
- 不允许只写“感觉像”

### Phase 3: Benchmark Skeleton Draft

目标：

- 新建 `docs/plans/2026-03-18-math-qa-benchmark.md`

要求至少包含：

- Scope
- Candidate object continuity cases
- Candidate method continuity cases
- Negative cases
- Ambiguous / unclear cases
- Current status
- What is not benchmark-ready yet

### Phase 4: Registry and Backlog Sync

目标：

- 在 registry 中留下 `math.QA` 入口
- 在 math backlog / task package 中登记后续路径

要求：

- 明确 `math.QA` 当前只是 skeleton
- 不要暗示已经具备 runner

## Done When

```yaml
done_when:
  - "新建 math.QA benchmark 文档骨架"
  - "至少整理 3 个 candidate positive"
  - "至少整理 3 个 candidate negative 或 ambiguous"
  - "registry 已出现 math.QA 路径与当前状态"
  - "math-worker-backlog 或 task-packages 已写明后续子包方向"
  - "文档明确哪些候选只是 test evidence"
```

## Stop Conditions

```yaml
stop_if:
  - "找不到 >=2 个可信的 object-side candidate positives"
  - "所有候选都只能靠泛词 quantum / representation 区分"
  - "无法区分 object continuity 与 method continuity"
  - "需要为了凑案例而引入 synthetic case"
  - "需要修改 runner 或 benchmark 代码"
```

## Expected Output Format

执行者完成后，应按以下格式汇报：

1. Selected Package
2. What I Read
3. Candidate Set Summary
4. Boundary Decisions
5. Docs Updated
6. Why This Is Still Skeleton Only
7. Commands Run
8. Residual Risk
9. Next Package Recommendation
10. Git Commit

## Recommended Next Packages

在当前阶段，只允许进入以下方向之一：

1. `PKG-QA-01A`
   - gap normalization
2. `PKG-QA-01B`
   - longer-window exploration
3. 只有在 `01B` 成功后，才重新进入：
   - benchmark doc refinement
   - method continuity case discovery
   - object continuity runner candidate

禁止在当前阶段直接进入 runner 实现，除非 longer-window exploration 已证明 benchmark skeleton 足够清楚。
