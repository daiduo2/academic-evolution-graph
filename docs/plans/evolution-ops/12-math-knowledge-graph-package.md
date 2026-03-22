doc_type: "task_package_detail"
scope: "math historical topic evolution knowledge graph"
status: "active"
owner: "trend-monitor"
source_of_truth: true
upstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/03-task-packages.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-18-math-data-audit.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-18-math-pr-benchmark.md"
downstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-12-math-worker-backlog.md"
last_reviewed: "2026-03-19"
package_id: "PKG-MATH-KG-01"
---

# Math Knowledge Graph Package

## Purpose

这个包不再把重点放在“继续扩数学 benchmark 子域”，而是转向你的真实目标：

**构建数学领域的历史主题演化知识图谱（Math Historical Topic Evolution Knowledge Graph）。**

当前我们已经有足够的前置条件来开始第一版图谱设计：

- `math.LO` benchmark / runner 已完成
- `math.AG` benchmark / runner 已完成
- `math.PR` 已确认不是 gap，处于 provisional 状态
- 全局 [topic_graph.json](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/data/output/topic_graph.json) 已包含：
  - `belongs_to`
  - `active_in`
  - `adjacent_to`
  - `evolves_from`
- `evolution_cases.json` 与 case detail 已能提供 retrospection evidence

换句话说，**我们不必等全数学 benchmark 全部完成，才开始第一版知识图谱。**

## Goal

设计并落地第一版 `math knowledge graph` 的 schema / bootstrap 文档，回答以下问题：

1. 图谱里有哪些 node types
2. 图谱里有哪些 edge types
3. 哪些 edge 是事实层（data-derived）
4. 哪些 edge 是证据层（benchmark / case / inferred）
5. 如何表达：
   - confirmed
   - inferred
   - ambiguous
   - gap / unavailable
6. 第一版图谱应覆盖哪些数学子域：
   - `math.LO`
   - `math.AG`
   - `math.PR`（provisional）
7. 第一版输出格式是什么
8. 后续如何从 schema 进入真正的 graph export/build

## Why Now

如果继续只做 benchmark 子域，会有两个问题：

- 你真正想要的知识图谱会被无限推迟
- Claude 会继续在子域判断上反复打转

而当前最有价值的动作，是把已有成果抽成一个**可积累的图谱表达层**：

- benchmark 作为验证层
- graph 作为知识表达层

这能让后续所有子域工作都更有方向感。

## Package Definition

```yaml
package_id: "PKG-MATH-KG-01"
owner: "doc-worker"
tree_path: "math knowledge graph"
task_type: "schema_and_bootstrap_design"
target_rule:
  - "math historical topic evolution graph"
  - "benchmark-to-graph evidence mapping"
goal: "设计第一版数学历史主题演化知识图谱的 schema、coverage scope、evidence model 和 bootstrap plan"
allowed_files:
  - "docs/plans/evolution-ops/12-math-knowledge-graph-package.md"
  - "docs/plans/evolution-ops/03-task-packages.md"
  - "docs/plans/2026-03-12-math-worker-backlog.md"
  - "docs/plans/2026-03-19-math-knowledge-graph.md"
required_commands:
  - "python3 pipeline/evolution_analysis.py --input data/output/aligned_topics_hierarchy.json --output-dir data/output/math_kg_bootstrap --max-cases 20 --category-filter math"
done_when:
  - "新建 math knowledge graph 设计文档"
  - "node / edge / evidence schema 被明确写出"
  - "第一版覆盖范围被明确限制在 LO + AG + PR(provisional)"
  - "区分 data-derived edges 与 benchmark/evidence edges"
  - "给出下一步是 graph export implementation 还是 PR-targeted extraction 的明确建议"
stop_if:
  - "需要修改 pipeline、tests 或 Makefile"
  - "需要直接实现前端可视化才能完成"
  - "需要把所有 math 子域都纳入第一版"
```

## Strong Scope Rule

### This Package Is About

- 图谱 schema
- 图谱证据层级
- 图谱第一版覆盖范围
- 图谱 bootstrap plan

### This Package Is Not About

- 新 benchmark runner
- 完整前端可视化
- 全数学子域一次性纳入
- registry 大规模升级

## Recommended Agent Team Split

这个包适合并行推进，建议至少 4 个 agent。

### Agent 1: schema-agent

职责：

- 设计 graph schema
- 明确 node / edge / attributes
- 区分：
  - topic-level
  - category-level
  - period-level
  - evidence-level

重点回答：

- 一个 `topic` node 至少要有什么字段
- 一个 `evolution edge` 至少要有什么字段
- `confirmed / inferred / ambiguous` 怎么编码

禁止：

- 改 pipeline
- 改 tests

### Agent 2: evidence-agent

职责：

- 盘点现有证据来源
- 把现有数据源映射到图谱：
  - `aligned_topics_hierarchy.json`
  - `topic_graph.json`
  - `evolution_cases.json`
  - benchmark docs
- 明确哪些是：
  - raw graph edge
  - replay case evidence
  - benchmark-confirmed relation
  - provisional candidate

禁止：

- 改代码
- 改 registry

### Agent 3: coverage-agent

职责：

- 定义第一版图谱覆盖范围
- 明确第一版只覆盖：
  - `math.LO`
  - `math.AG`
  - `math.PR`（provisional）
- 说明为什么：
  - `QA / RA` 不进第一版
  - `RT` 暂不进第一版

禁止：

- 擅自把更多子域写进 v1
- 改代码

### Agent 4: bootstrap-agent

职责：

- 设计从 schema 走向 implementation 的最小路径
- 回答下一步应该是：
  - graph export implementation
  - 还是先完成 `PR-targeted extraction`
- 给出分阶段路线：
  - KG-02
  - KG-03

禁止：

- 直接写实现代码
- 直接启动前端任务

如果你想加第 5 个 agent，也可以：

### Agent 5: sanity-agent

职责：

- 专门审查是否把“已验证 benchmark”与“推断候选”混写
- 防止图谱 schema 一开始就把证据层级弄混

## Working Model

### Node Types

建议第一版至少包含：

1. `topic`
   - 全局 topic
2. `subcategory`
   - 如 `math.LO`, `math.AG`, `math.PR`
3. `period`
   - 月度时间点

**Note:** `case` and `benchmark_case` are NOT standalone nodes. Evolution cases and benchmark cases are represented as **edge annotations** on `EVOLVES_TO` edges. This design decision keeps the graph topology clean and aligns with the fundamental nature of these entities as relationship evidence rather than independent nodes.

### Edge Types

建议第一版至少包含：

1. `CONTAINS_TOPIC`
   - subcategory -> topic (canonical name for `belongs_to`)
2. `ACTIVE_IN`
   - topic -> period (direct mapping from `active_in`)
3. `NEIGHBOR_OF`
   - topic -> topic (canonical name for `adjacent_to`)
4. `PARENT_OF`
   - topic -> topic (derived from `hierarchy_path`)
5. `EVOLVES_TO`
   - topic -> topic (canonical name for `evolves_from`, direction flipped)
   - Evidence annotations: `benchmark_case_id`, `benchmark_status`, `evidence_type`, `case_id`, `inference_basis`
6. `CROSS_CATEGORY_LINK`
   - topic -> topic (from `cross_category_moves`)

## Evidence Levels

这是本包最关键的一点：图谱不能只表达结构，还必须表达**证据强度**。

建议第一版固定四级：

1. `confirmed`
   - 已被 benchmark / curated cases 确认
2. `inferred`
   - 来自 graph / export / neighbor / metadata 推断
3. `ambiguous`
   - 候选存在，但边界不稳
4. `unavailable`
   - 当前子域数据不足或未进入图谱

## Version 1 Coverage

### In Scope

- `math.LO`
- `math.AG`
- `math.PR`（明确标记为 `provisional` / `inferred-heavy`）

### Out of Scope

- `math.QA`
- `math.RA`
- `math.RT`
- 其他未评估数学子域

### Why

因为第一版目标不是“全数学”，而是“可信的第一版图谱原型”。

## Expected Design Decisions

执行本包时，必须明确回答：

1. 图谱是 topic-centric 还是 case-centric？
   - **Answer:** Topic-centric. Cases are edge annotations, not nodes.
2. benchmark case 在图谱里是 node 还是 edge annotation？
   - **Answer:** Edge annotation on `EVOLVES_TO` edges. See design doc Section "Benchmark Case Representation".
3. `math.PR` 的 provisional 状态应该如何编码？
   - **Answer:** `edge.evidence_type: "provisional"` + `edge.confidence: "inferred"` + `subcategory.status: "provisional"`
4. `gap` 子域是否进图谱？
   - **Answer:** No. math.QA and math.RA are explicitly excluded from v1.
5. 图谱导出第一版是：
   - **Answer:** Nodes/edges split files (see KG-02 Output Specification in design doc)
   - `nodes/{topics,subcategories,periods}.jsonl`
   - `edges/{contains_topic,active_in,neighbor_of,parent_of,evolves_to}.jsonl`
   - `metadata.json` + `validation_report.json`
   - **KG-02 baseline scope:** `math.LO + math.AG` only; `math.PR` is deferred to conditional PR integration after `MPR-01C`
6. benchmark / review 里已经确认的 graph-facing narrative 应如何进入导出层？
   - **Answer:** As metadata and edge annotations, not as new topology.
   - `metadata.domain_knowledge_layers` should expose baseline / bridge / boundary / review / contract layers.
   - `metadata.domain_knowledge_layers` should also expose which layers can count as baseline truth vs narrative-only (`baseline_truth_layer_keys`, `narrative_only_layer_keys`).
   - `EVOLVES_TO` edges may expose `graph_band`, `graph_layer`, `graph_role`, `graph_export_status`.
   - `math.CO` may appear as docs-only contract metadata without adding CO nodes or baseline edges.
   - `math.DS` may appear as docs-only narrative metadata once its benchmark skeleton is stable, but bridge/review layers must not be upgraded to baseline topology.
   - `math.NA` may appear as docs-only narrative metadata once its Krylov benchmark skeleton is stable, but bridge/review layers must not be upgraded to baseline topology.

## Suggested Output Sections

最终设计文档至少应包含：

1. Executive Summary
2. Problem Statement
3. Scope for v1
4. Node Schema
5. Edge Schema
6. Evidence Model
7. Coverage Decision
8. Example Subgraphs
9. Non-Goals
10. Bootstrap Plan
11. Next Implementation Package

## Recommended Example Subgraphs

第一版文档里最好至少画出 3 个例子：

1. `math.LO`
   - confirmed path
2. `math.AG`
   - confirmed + benchmark-ready path
3. `math.PR`
   - provisional / inferred-heavy path

## Decision Fork

### Option A

如果 schema 足够清楚，且第一版 coverage 边界稳定：

- 下一步进入 `KG-02 graph export implementation`

### Option B

如果 schema 清楚，但 `math.PR` 的证据层仍太松：

- 下一步先执行 `MPR-01C PR-targeted candidate extraction`
- 再进入 `KG-02`

## Non-Goals

这个包明确不做：

- 前端图谱视图
- Neo4j / graph DB 部署
- 全数学本体清洗
- 自动生成所有 confirmed edges

## Source-to-Canonical Mapping Reference

### Export Schema to Graph Schema

| Source Export Field | Canonical Graph Edge | Direction | Transformation Rule |
|--------------------|----------------------|-----------|---------------------|
| `belongs_to` | `CONTAINS_TOPIC` | Subcategory → Topic | Flip direction |
| `active_in` | `ACTIVE_IN` | Topic → Period | Direct mapping |
| `adjacent_to` | `NEIGHBOR_OF` | Topic ↔ Topic | Undirected (symmetric) |
| `evolves_from` | `EVOLVES_TO` | Topic → Topic | Flip direction (temporal flow) |
| `hierarchy_path` | `PARENT_OF` | Topic → Topic | Derive from path depth |
| `cross_category_moves` | `CROSS_CATEGORY_LINK` | Topic → Topic | Filter cross-category only |

### Transformation Details

```yaml
# belongs_to: Flip direction for "container contains item" semantics
Export:  {source: "global_56", target: "math.LO", type: "belongs_to"}
Graph:   {source: "math.LO", target: "global_56", type: "CONTAINS_TOPIC"}

# evolves_from: Flip for temporal flow (anchor → target)
Export:  {source: "global_27", target: "global_56", type: "evolves_from"}
Graph:   {source: "global_56", target: "global_27", type: "EVOLVES_TO"}

# active_in: Direct mapping
Export:  {source: "global_56", target: "2025-02", type: "active_in"}
Graph:   {source: "global_56", target: "2025-02", type: "ACTIVE_IN"}

# adjacent_to: Direct mapping (undirected)
Export:  {source: "global_56", target: "global_27", type: "adjacent_to"}
Graph:   {source: "global_56", target: "global_27", type: "NEIGHBOR_OF"}
```

## KG-02 Prerequisites Summary

KG-02 (Graph Export Implementation) requires:

### Input Files
- `data/output/aligned_topics_hierarchy.json` - Topic hierarchy and metadata
- `data/output/topic_graph.json` - Graph structure with edges
- `docs/plans/2026-03-12-math-lo-benchmark.md` - LO benchmark cases
- `docs/plans/2026-03-18-math-ag-benchmark.md` - AG benchmark cases

### Output Files (KG-02 "Done" Definition)
```
data/output/kg_v1/
├── nodes/
│   ├── topics.jsonl          # KG-02 baseline topics (LO + AG only)
│   ├── subcategories.jsonl   # math.LO, math.AG
│   └── periods.jsonl         # 2025-02 through 2026-02
├── edges/
│   ├── contains_topic.jsonl  # CONTAINS_TOPIC edges
│   ├── active_in.jsonl       # ACTIVE_IN edges
│   ├── neighbor_of.jsonl     # NEIGHBOR_OF edges
│   ├── parent_of.jsonl       # PARENT_OF (from hierarchy)
│   └── evolves_to.jsonl      # EVOLVES_TO with evidence annotations
├── metadata.json             # Version, coverage stats, timestamp
└── validation_report.json    # Schema validation results
```

### Success Criteria
- [ ] All node files validate against Node Schema
- [ ] All edge files validate against Edge Schema
- [ ] LO benchmark cases (13 total: 5+, 6-, 2~) encoded as edge annotations
- [ ] AG benchmark cases encoded according to the hierarchy-scoped KG-02 baseline (currently 5 of 6 documented cases)
- [ ] PR is not included in KG-02 baseline output; PR provisional integration is deferred to conditional follow-up
- [ ] `metadata.json` contains accurate coverage statistics
- [ ] Validation report shows 0 schema errors

## Success Standard

完成后，你应能直接回答：

- 数学历史主题演化知识图谱 v1 要表达什么
- 它和 benchmark 的关系是什么
- 它第一版覆盖哪些子域
- `math.PR` 在图谱里如何表达
- 下一步该先做 graph export，还是先补 PR-targeted extraction
- **新增:** Source export schema 如何映射到 canonical graph schema
- **新增:** KG-02 的输入、输出和完成标准是什么
