doc_type: "governance"
scope: "detailed bootstrap package for math.RA benchmark skeleton"
status: "active"
owner: "trend-monitor"
source_of_truth: true
upstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/03-task-packages.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/07-benchmark-data-policy.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-10-evolution-rule-coverage.md"
downstream_docs: []
last_reviewed: "2026-03-18"

# Math.RA Bootstrap Package

## Purpose

这份文档为 `math > math.RA` 提供一个较长、但仍然强约束的启动包。

它的设计目标和 `math.QA` 不同：

- `math.QA` 先收口为 `gap`
- `math.RA` 作为更稳的第三数学子域候选，允许在一个包内完成：
  - 候选搜索
  - 边界分类
  - benchmark skeleton 初稿
  - 如果失败，则直接降级成 gap 结论

也就是说，`math.RA` 采用 **“single package with decision fork”** 的策略，减少 review 往返次数。

## Package Identity

```yaml
package_id: "PKG-RA-01"
owner: "case-worker"
tree_path: "math > math.RA"
task_type: "bootstrap_with_decision_fork"
target_rule:
  - "math_ra_object_continuity"
  - "math_ra_method_continuity"
goal: "判断 math.RA 是否具备 benchmark skeleton 条件；若具备则直接建立 skeleton，若不足则直接收口为 gap"
```

## Why This Package Can Be Longer

`LO / AG / UNI-02 / QA-gap` 这几轮已经把方法论跑清楚了：

- benchmark 不应在 case 不清晰时继续推进
- runner 不应早于 skeleton
- 数据不足时要先收口为 gap
- 文档必须能复用结论，而不是重复探索

因此 `math.RA` 不必再拆成过多碎包，而是可以在一个较长任务内完成“发现 -> 判断 -> 分叉”。

## Decision Fork

`PKG-RA-01` 必须在同一轮内给出明确分叉结论：

### Option A: Bootstrap

满足以下条件时进入：

- 至少找到 3 个可信 candidate positives
- 至少找到 3 个可信 negative / ambiguous
- 能区分 `object_continuity` 与 `method_continuity`
- 不需要 synthetic case

结果：

- 新建 `math.RA` benchmark skeleton 文档
- 在 registry 中把 `math.RA` 标成 `partial` 或 `bootstrap-ready`
- 在 backlog / task package 中登记下一步 runner 前置包

### Option B: Gap

若以下任一成立：

- 找不到 >=2 个可信 object-side positives
- 候选只能靠泛词 `algebra / module / representation` 区分
- object / method 边界不清
- 当前数据中没有足够跨期演化样本

结果：

- 不创建正式 benchmark skeleton
- 直接在 registry / backlog / ops docs 中把 `math.RA` 收口为：
  - `gap`
  - `insufficient data`
  - `not benchmark-ready`

## Allowed Files

```yaml
allowed_files:
  - "docs/plans/2026-03-10-evolution-rule-coverage.md"
  - "docs/plans/2026-03-12-math-worker-backlog.md"
  - "docs/plans/evolution-ops/03-task-packages.md"
  - "docs/plans/evolution-ops/09-math-ra-bootstrap-package.md"
  - "docs/plans/2026-03-18-math-ra-benchmark.md"
```

## Out Of Scope

- 不实现 `math_ra_benchmark.py`
- 不新增 `make math-ra-benchmark`
- 不新增 `config/benchmarks/math_ra.yaml`
- 不改 `pipeline/` 或 `tests/`
- 不定义最终 score

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
  - "rg -n \"math\\.RA|ring|rings|module|modules|ideal|ideals|algebra|algebras|homological|derived\" data/output/aligned_topics_hierarchy.json data/output/evolution_cases.json"
```

## Suggested RA Ontology Hints

这不是最终 ontology，只是第一轮搜索提示。

### Candidate Object Hints

- ring / rings
- module / modules
- ideal / ideals
- algebra / algebras
- algebra representation
- Lie algebra / associative algebra
- graded algebra
- commutative algebra
- local ring / valuation ring

### Candidate Method Hints

- homological
- derived
- categorical
- deformation
- syzygy / resolution
- cohomological
- representation-theoretic

### Negative-Side Confusers

- 只共享 `algebra`
- 只共享 `representation`
- 只共享 `category`
- 明显更接近 `math.RT` 或 `math.AG`，而不是 `math.RA`

## Work Phases

### Phase 1: Candidate Harvest

目标：

- 收集 `math.RA` 子树内及其邻近路径的候选 pairs

要求：

- 至少列出 8 个候选 pairs
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
- 不允许只用泛词重叠做正例

### Phase 3: Decision Fork

目标：

- 明确给出 `Option A` 或 `Option B`

要求：

- 必须写出选择理由
- 不允许模糊停在“可能可以继续”

### Phase 4A: Skeleton Draft (only if Option A)

新建：

- `docs/plans/2026-03-18-math-ra-benchmark.md`

至少包含：

- Scope
- Candidate object continuity cases
- Candidate method continuity cases
- Negative cases
- Ambiguous / unclear cases
- Current status
- What is not benchmark-ready yet

### Phase 4B: Gap Closure (only if Option B)

要求：

- registry 明确标注 `gap / insufficient data`
- backlog / ops docs 明确写出后续只能先做 longer-window exploration 或转其他子域

## Done When

```yaml
done_when:
  - "已完成 candidate harvest 与 boundary classification"
  - "已明确给出 Option A 或 Option B"
  - "若 Option A：math.RA benchmark skeleton 文档已创建"
  - "若 Option B：registry / backlog / ops docs 已完成 gap 收口"
  - "文档中明确哪些候选只是 test evidence"
```

## Stop Conditions

```yaml
stop_if:
  - "所有候选都只能靠 algebra / module / representation 这类泛词区分"
  - "找不到 >=2 个可信 object-side candidate positives"
  - "需要引入 synthetic case"
  - "需要修改 runner、tests 或 Makefile"
  - "无法在本轮内明确决定 Option A 或 Option B"
```

## Expected Output Format

1. Selected Package
2. What I Read
3. Candidate Set Summary
4. Boundary Decisions
5. Decision Fork Result
6. Docs Updated
7. Why This Is Still Pre-Runner
8. Commands Run
9. Residual Risk
10. Next Package Recommendation
11. Git Commit

## PKG-RA-01 Completion Record **[COMPLETED - 2026-03-18]**

### Decision Fork Result

**选择: Option B (Gap)**

### Data Assessment

```yaml
total_topics: 3
topics:
  - "global_82: 泊松-巴克斯特李代数 (32 papers, 1 period)"
  - "global_200: 多项式映射与算法 (14 papers, 1 period)"
  - "global_214: 随机矩阵与正定性 (46 papers, 1 period)"
evolution_cases: 0
temporal_pairs: 0
object_continuity_candidates: "无 (所有 topics 仅 1 个 period)"
method_continuity_candidates: "无 (所有 topics 仅 1 个 period)"
```

### Decision Reason

仅3个topics，全部仅1个active month，无法构成temporal evolution，无法形成任何pairs。

不满足 Option A 条件：
- ❌ 找不到 >=2 个可信 object-side positives
- ❌ 候选只能靠泛词区分
- ❌ 当前数据中没有足够跨期演化样本

### Actions Completed

- ✅ 更新 registry: math > math.RA 状态标记为 `gap`
- ✅ 新增 math_ra_gap_insufficient_data 规则条目
- ✅ 更新 Tree Path Registry 中 math.RA 的 notes
- ✅ 更新 Layer 1 Coverage 表格
- ✅ math-worker-backlog 记录 MRA-01 已完成

### Current State

- **math.RA 状态**: gap / insufficient data / not benchmark-ready
- **当前数据**: 3 topics, 全部仅 1 个 period, 0 evolution cases
- **无法区分**: object continuity vs method continuity

### Next Package (Conditional)

**PKG-RA-01B / MRA-01B**: Longer-Window Exploration

触发条件: 获得 >=24 个月 math.RA 数据

---

## Recommended Next Packages

若 `Option A`：

1. `PKG-RA-02`
   - benchmark doc refinement
2. `PKG-RA-03A`
   - method continuity case discovery
3. `PKG-RA-04`
   - object continuity runner candidate

若 `Option B` (**已选择**)：

1. `PKG-RA-01B` / `MRA-01B`
   - longer-window exploration (需要 >=24 个月数据)
2. 或直接转向 `math.RT`

禁止在 `PKG-RA-01` 之后直接进入 runner，除非已经明确走 `Option A`。
