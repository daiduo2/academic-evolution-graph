doc_type: "governance"
scope: "detailed task packages for Claude and subagents"
status: "active"
owner: "trend-monitor"
source_of_truth: true
upstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/02-two-week-roadmap.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-12-evolution-task-template.md"
downstream_docs: []
last_reviewed: "2026-03-18"

# Task Packages

## Purpose

这份文档把近期任务拆成 Claude / subagent 可直接执行的任务包。

使用原则：

- 一次只发 1 个包
- 不要发“继续推进”
- 不要把两个 worker 类型混在一个包里

## Package Format

每个任务包都包含：

- `package_id`
- `owner`
- `tree_path`
- `task_type`
- `target_rule`
- `goal`
- `allowed_files`
- `required_commands`
- `must_update_docs`
- `done_when`
- `stop_if`

## Data Baseline Rule

对于 benchmark 相关任务，先区分：

- 代码 regression
- 数据版本差异

如果：

- wrapper 和 unified CLI 的结果一致
- 测试通过
- benchmark 结果只因 `data/output/aligned_topics_hierarchy.json` 或其他输入数据版本不同而变化

则默认判定为 **data-baseline issue**，不要继续修改 runner 代码。

## Completed Packages

### PR-TrackB-01

**package_id:** PR-TrackB-01
**date:** 2026-03-24
**owner:** review-worker
**type:** track_b_evidence_strengthening
**status:** COMPLETE — title-level review; Gate 2 still blocked on R2

**Summary:**
Track B paper review for math.PR Gate 2. Three risks reviewed at title-level:
- R1 (global_38 transience): PARTIALLY_MITIGATED — 5-descendant generativity, global_99 confirmed; risk reduced to moderate.
- R2 (global_65→global_188 directionality): NOT_MITIGATED — identical representative papers, no evolves_from edge, concurrent periods. Gate 2 BLOCKED on R2.
- R3 (PR/AP boundary): RESOLVED — both topics PR-dominant. global_188 dual-class caveat noted.

**Evidence ceiling:** title-level (no abstracts, no arXiv IDs, no citation data).
**Upstream docs:** docs/plans/2026-03-24-math-pr-track-b-paper-review.md
**Next step:** PR-TrackB-02 (external evidence for R2) OR accept Gate 1 as stable state.

---

### PR-TrackB-02

- **Package ID:** PR-TrackB-02
- **Date:** 2026-03-25
- **Type:** External evidence review
- **Scope:** R2 external arXiv evidence for global_65→global_188 directionality
- **Status:** COMPLETE — R2 PARTIALLY_MITIGATED
- **Owner:** rule-worker
- **Result:** Abstract+citation evidence confirms field-level mathematical lineage (classical McKean-Vlasov → rough McKean-Vlasov). Cluster-level directionality for P4 not confirmed (parallel 2025 communities, zero cross-citation). Gate 2 still blocked.
- **Key evidence:** arXiv:2507.13149, 2507.17469, 1907.00578, 2507.02449; counter: arXiv:1802.05882, 2510.16427, 2502.20786
- **Upstream:** PR-TrackB-01
- **Downstream:** None (blocked pending cluster-level evidence)

---

### PR-TrackB-03

- **Package ID:** PR-TrackB-03
- **Date:** 2026-03-26
- **Type:** Cluster-level evidence review
- **Scope:** R2 cluster-level directionality for global_65→global_188 (P4)
- **Status:** COMPLETE — P4 DEMOTED; R2 RESOLVED (negative)
- **Owner:** review-worker
- **Result:** Cluster-level evidence confirms global_65 and global_188 are parallel 2025 research communities, not sequential evolution. Zero cross-citation in 2025 overlap window. Rough McKean field predates global_65 by 7 years. Shared representative papers not McKean-Vlasov. P4 demoted from Gate 2 directional candidate; retained as calibration anchor. R2 resolved negative. Gate 2 path: P1/P2/P3 (global_38-family) require independent TrackB review.
- **Key evidence FOR:** adjacency bw=0.4795 (BERTopic vocabulary proximity)
- **Key evidence AGAINST:** arXiv:2510.16427, 2502.20786, 2601.20350 (zero rough path cites); arXiv:2507.02449, 2507.17469 (zero 2025 global_65 cites); arXiv:1802.05882 (2018 founding date)
- **Upstream:** PR-TrackB-02
- **Downstream:** PR-TrackB-04 (P1/P2/P3 cluster-level review, pending)

---

### PR-TrackB-04

- **Package ID:** PR-TrackB-04
- **Date:** 2026-03-27
- **Type:** Cluster-level evidence review (title-level + graph-structural)
- **Scope:** global_38-family P1/P2/P3 cluster-level directionality and predecessor identity
- **Status:** COMPLETE — P3 DEMOTED; P1/P2 PROVISIONALLY RETAINED; Gate 2 PARTIALLY VIABLE
- **Owner:** review-worker
- **Result:** global_38 confirmed as genuine_predecessor (HIGH confidence). P1 (global_38→global_100): provisionally retained, label reclassification from object_continuity to domain_bridge recommended; P2 (global_38→global_156): provisionally retained as primary Gate 2 candidate, equal-weight caveat; P3 (global_38→global_99): DEMOTED — identical representative papers, no adjacency, single-source. Gate 2 path partially viable via P1+P2. Evidence level: title-level + graph-structural (NOT abstract+citation level). Level 3 review required before Gate 2 promotion.
- **Key evidence FOR P1/P2:** evolves_from edges (independent temporal algorithm); distinct representative paper sets; strict succession; domain-specific vocabulary ("matrices", "eigenvalues") less artifact-prone than P4's generic vocabulary
- **Key evidence AGAINST P3:** identical representative papers to global_38; absence of adjacency edge; single-source only
- **Upstream:** PR-TrackB-03
- **Downstream:** PR-TrackB-05 (P1/P2 Level 3 abstract+citation review, pending)

---

### PR-TrackB-05

**package_id:** PR-TrackB-05
**date:** 2026-03-28
**type:** abstract_citation_evidence_review (title-level + graph-structural)
**scope:** P1/P2 Level 3 review — global_38-family final evidence strengthening
**status:** COMPLETE — P1/P2 CONDITIONALLY DEMOTED; global_100/global_156 NOT RELIABLY DISTINCT; Gate 2 SINGLE-CANDIDATE HEIGHTENED CONCERN
**owner:** review-worker
**result:** global_100 and global_156 confirmed NOT RELIABLY DISTINCT (5/5 identical representative papers, bw=0.475 inter-cluster adjacency). P1 (global_38→global_100): CONDITIONALLY DEMOTED — founding-date pressure (RMT fields 30-70 years old), category mismatch concern (global_38 is classical random walks; "matrices" keyword may be Markov chain notation), citation signal absent at title-level. P2 (global_38→global_156): MERGED INTO P1, CONDITIONALLY DEMOTED by merger. P2 equal-weight concern (0.4077 = 0.4077): SUSPICIOUS — 1.5 effective sources. Gate 2 collapses from two-candidate to single-candidate path. Evidence ceiling: title-level + graph-structural (NOT abstract+citation). Verdicts are CONDITIONAL pending PR-TrackB-06 abstract+citation review.
**downstream:** PR-TrackB-06 (P1/P2 abstract+citation review — founding-date, category, citation linkage, equal-weight computational audit)

---

### PR-2C-impl (COMPLETE 2026-03-23, fix applied 2026-03-21)

```yaml
package_id: "PR-2C-impl"
owner: "rule-worker"
tree_path: "math > math.PR > conditional graph integration > implementation"
task_type: "conditional_layer_implementation"
status: "COMPLETE"
completed_date: "2026-03-23"
fix_package: "PR-2C-impl-fix"
fix_date: "2026-03-21"
gate_advanced: "Gate 0 → Gate 1"
summary: >
  Implemented math.PR conditional graph integration layer. LO+AG baseline unchanged.
  PR conditional export: data/output/kg_v1_pr_conditional/ (61 topics, 13 evolves_to).
  PR conditional viz: data/output/kg_v1_pr_conditional_visualization/ (subgraph_pr.json).
  Frontend opt-in: /knowledge-graph?pr_preview=1 activates PR conditional layer.
  All 4 curated positive cases (PR-P1..P4) are graph-visible with provisional evidence.
  PR-2C-impl-fix (2026-03-21): timeline now follows sourceMode (pr_conditional → kg_v1_pr_conditional_visualization);
  viz exporter main() entrypoint covered by TestConditionalVisualizationEntrypoint (5 tests);
  kg_v1_pr_conditional/ and kg_v1_pr_conditional_visualization/ added to .gitignore.
  67 viz export tests + 4 frontend tests passing.
next_step: "PR-TrackB-06 COMPLETE (2026-03-29) — DEMOTED; Gate 2 COLLAPSED; long-term Gate 1"
gate_2_collapsed: true
gate_2_blocked_by:
  open: []
  future_contingency:
    - "MPR-03 (PR benchmark runner) — dormant; becomes relevant only if new directional evidence reopens Gate 2 (e.g., TrackB-07 initiated for global_38→global_198 line)"
  closed:
    - "P1/P2 abstract+citation review (PR-TrackB-06, 2026-03-29) — RESOLVED (negative): DEMOTED FINAL; category mismatch confirmed, founding-date impossible, citation absent, cluster incoherent; Gate 2 COLLAPSED"
    - "Directional evidence for global_65 → global_188 (R2) — RESOLVED (negative, PR-TrackB-03 2026-03-26): P4 demoted; Gate 2 path via P1/P2/P3"
    - "math.PR vs math.AP classification for global_65 and global_188 (R3) — RESOLVED (PR-TrackB-01 2026-03-24)"
```

---

## Active Packages

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
must_update_docs:
  - "docs/plans/2026-03-18-math-data-audit.md"
  - "docs/plans/2026-03-12-math-worker-backlog.md"
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

### PKG-PLG-01

```yaml
package_id: "PKG-PLG-01"
owner: "doc-worker"
tree_path: "plugin.v1"
task_type: "consistency_cleanup"
target_rule: "evolution-delegation plugin"
goal: "校验 plugin、guardrails、templates、skills 与当前仓库 runner 现状一致"
allowed_files:
  - ".claude/plugins/evolution-delegation/plugin.yaml"
  - ".claude/plugins/evolution-delegation/config/guardrails.yaml"
  - ".claude/plugins/evolution-delegation/config/templates.yaml"
  - ".claude/skills/case-worker/SKILL.md"
  - ".claude/skills/rule-worker/SKILL.md"
  - ".claude/skills/doc-worker/SKILL.md"
  - ".claude/skills/delegate-evolution/SKILL.md"
required_commands:
  - "git status --short"
must_update_docs:
  - "docs/plans/evolution-ops/02-two-week-roadmap.md"
done_when:
  - "supported_domains 与真实 runner 一致"
  - "completion gate 与 task_type 分支一致"
stop_if:
  - "plugin 仍引用不存在文件"
```

### PKG-PLG-02

```yaml
package_id: "PKG-PLG-02"
owner: "doc-worker"
tree_path: "plugin.v1"
task_type: "operator_doc"
target_rule: "evolution-delegation plugin"
goal: "补一份给人工操作者和 Claude subagent 的 operator checklist"
allowed_files:
  - "docs/plans/evolution-ops/README.md"
  - "docs/plans/evolution-ops/04-troubleshooting-and-escalation.md"
required_commands: []
must_update_docs:
  - "README.md"
  - "AGENTS.md"
done_when:
  - "能回答如何开始一次委派"
  - "能回答何时应停止自动推进"
stop_if:
  - "需要改动 benchmark runner 代码"
```

### PKG-AG-01

```yaml
package_id: "PKG-AG-01"
owner: "case-worker"
tree_path: "math > math.AG"
task_type: "benchmark_case_curation"
target_rule: "math_ag_object_continuity"
goal: "为 math.AG 固定第一批真实 benchmark case"
positive_case_hint: "global_69 -> global_287"
negative_case_hint: "global_69 -> global_136"
allowed_files:
  - "docs/plans/2026-03-10-evolution-rule-coverage.md"
  - "docs/plans/evolution-ops/03-task-packages.md"
required_commands:
  - "make evolution-analysis"
must_update_docs:
  - "math.AG benchmark 文档（新建）"
done_when:
  - "至少 3 positive / 3 negative / 1 ambiguous"
  - "每个 case 都有一句为什么它成立或不成立"
stop_if:
  - "只有 synthetic case，没有真实 case"
```

### PKG-AG-02

```yaml
package_id: "PKG-AG-02"
owner: "doc-worker"
tree_path: "math > math.AG"
task_type: "benchmark_doc_creation"
target_rule: "math_ag_object_continuity | math_ag_method_continuity"
goal: "创建 math.AG benchmark 文档，并与 registry 对齐"
allowed_files:
  - "docs/plans/2026-03-10-evolution-rule-coverage.md"
  - "docs/plans/2026-03-xx-math-ag-benchmark.md"
required_commands: []
must_update_docs:
  - "registry"
  - "math.AG benchmark doc"
done_when:
  - "文档结构与 math.LO benchmark 对齐"
  - "synthetic case 明确降级为 test evidence"
stop_if:
  - "case list 尚未确认"
```

### PKG-AG-03 (已归档)

**状态**: 已拆分为 PKG-AG-03A / PKG-AG-03B-runner / PKG-AG-03B-normalization

**归档原因**: 原设计为单一 benchmark_runner 包，但实际需要先进行 case discovery 决策。

---

### PKG-AG-03A: Method Continuity Case Discovery **[已归档 - 2026-03-17]**

```yaml
package_id: "PKG-AG-03A"
owner: "case-worker"
tree_path: "math > math.AG"
task_type: "case_discovery"
target_rule: "math_ag_method_continuity"
goal: "判断 method_continuity 是否值得进入 benchmark 主流程"
decision_fork:
  option_a:
    condition: "找到 >=2 个真实 event-level positive cases"
    action: "进入 PKG-AG-03B-runner"
    result: "❌ 未满足"
  option_b:
    condition: "只找到 bridge-level cases 或 case 不足"
    action: "进入 PKG-AG-03B-normalization"
    result: "✅ 已选择"
current_candidates:
  - note: "已找到的 cases 均为 bridge-level"
  - ag-method-p1: "global_136 -> global_263 (2025-06 -> 2025-10)"
  - ag-method-p2: "global_237 -> global_263 (2025-09 -> 2025-10)"
  - assessment: "时间跨度太短，无法构成 event-level evolution"
allowed_files:
  - "docs/plans/2026-03-17-math-ag-benchmark.md"
  - "docs/plans/2026-03-10-evolution-rule-coverage.md"
done_when:
  - "明确 decision_fork 走向 (option_a 或 option_b)"
  - "文档记录决策理由"
archive_reason: "insufficient event-level data"
```

### PKG-AG-03B-runner: Implement Method Benchmark **[LOCKED]**

```yaml
package_id: "PKG-AG-03B-runner"
owner: "rule-worker"
tree_path: "math > math.AG"
task_type: "benchmark_implementation"
target_rule: "math_ag_method_continuity"
precondition: "MAG-03A 必须完成且选择 option_a"
goal: "为 method_continuity 实现完整的 benchmark runner"
status: "🔒 锁定 - 因 MAG-03A 选择 Option B，此包不会执行"
required_cases:
  - ">=2 event-level positive cases"
  - ">=1 negative case"
allowed_files:
  - "pipeline/math_ag_benchmark.py"
  - "tests/test_math_ag_benchmark.py"
  - "docs/plans/2026-03-17-math-ag-benchmark.md"
```

### PKG-AG-03B-normalization: Scope Cleanup **[已完成 - 2026-03-17]**

```yaml
package_id: "PKG-AG-03B-normalization"
owner: "doc-worker"
tree_path: "math > math.AG"
task_type: "scope_normalization"
target_rule: "math_ag_method_continuity"
precondition: "MAG-03A 完成，选择 option_b (case 不足)"
goal: "明确将 method_continuity 维持 test-evidence-only"
actions_completed:
  - ✅ "更新 registry: 明确标注 '⚠️ TEST EVIDENCE ONLY / NOT BENCHMARK-READY'"
  - ✅ "更新 math-ag-benchmark.md: 将 method cases 移入 'Test Evidence' 章节"
  - ✅ "更新 math_ag_benchmark.py: 移除 method continuity cases"
  - ✅ "创建 test_math_ag_benchmark.py 测试文件"
  - ✅ "更新 Makefile: 添加 math-ag-benchmark 目标"
completion_verify:
  - ✅ method_continuity 不在 runner 中
  - ✅ 文档明确区分: object (ready) vs method (test-only)
  - ✅ 无歧义的 stop condition 已记录
  - ✅ math.AG benchmark 全绿: 6/6 passed
  - ✅ make math-ag-benchmark 可执行
  - ✅ pytest tests/test_math_ag_benchmark.py 通过
```

### PKG-AG-04: Object Continuity Benchmark Runner **[已完成]**

```yaml
package_id: "PKG-AG-04"
owner: "rule-worker"
tree_path: "math > math.AG"
task_type: "benchmark_runner"
target_rule: "math_ag_object_continuity"
goal: "实现 math.AG object_continuity 的可执行 benchmark runner 与测试"
allowed_files:
  - "pipeline/math_ag_benchmark.py"
  - "tests/test_math_ag_benchmark.py"
  - "Makefile"
required_commands:
  - "pytest tests/test_math_ag_benchmark.py -q"
  - "make math-ag-benchmark"
must_update_docs:
  - "math.AG benchmark doc"
done_when:
  - "runner 可生成 json + md"
  - "测试通过"
  - "6/6 cases 全绿"
status: "✅ 已完成"
```

### PKG-UNI-01: Generic Benchmark Runner Design **[ACTIVE - 2026-03-17]**

**前置条件检查**: LO 与 AG benchmark 输出结构已对齐 ✅

```yaml
package_id: "PKG-UNI-01"
owner: "doc-worker"
tree_path: "math benchmark architecture"
task_type: "design_doc"
target_rule: "math_benchmark.py"
goal: "写通用 benchmark runner 的设计稿"
context:
  - "math_lo_benchmark.py: 11 cases (5+6+2), supports ambiguous section"
  - "math_ag_benchmark.py: 6 cases (2+4), no ambiguous section"
  - "Both use identical evaluate_expected/build_neighbor_map/evaluate_case logic"
  - "Both output json + markdown reports"
analysis_required:
  - "提取公共逻辑到 base runner"
  - "设计 domain-specific case loader"
  - "统一 score 计算策略"
  - "设计 wrapper/adapter 模式"
allowed_files:
  - "docs/plans/evolution-ops/02-two-week-roadmap.md"
  - "docs/plans/evolution-ops/05-math-benchmark-design.md" (新建)
required_commands: []
must_update_docs:
  - "docs/plans/evolution-ops/05-math-benchmark-design.md"
done_when:
  - "明确输入 spec / 输出 report / score 字段"
  - "明确 class/function 抽象层次"
  - "明确 math_lo/math_ag wrapper 实现方式"
  - "设计文档通过 review"
deliverables:
  - "抽象基类/接口设计"
  - "CaseLoader 策略"
  - "ReportFormatter 策略"
  - "ScoreCalculator 策略"
  - "Domain-specific wrapper 示例"
```

### PKG-UNI-02

```yaml
package_id: "PKG-UNI-02"
owner: "rule-worker"
tree_path: "math benchmark architecture"
task_type: "runner_implementation"
target_rule: "math_benchmark.py"
goal: "让通用 runner 至少支持 math_lo 与 math_ag"
allowed_files:
  - "pipeline/math_benchmark.py"
  - "pipeline/math_lo_benchmark.py"
  - "pipeline/math_ag_benchmark.py"
  - "tests/test_math_benchmark.py"
required_commands:
  - "pytest tests/test_math_benchmark.py -q"
  - "make math-lo-benchmark"
  - "make math-ag-benchmark"
must_update_docs:
  - "通用 runner 设计文档"
done_when:
  - "LO 与 AG 共用同一底层 runner"
stop_if:
  - "math_ag runner 还不存在"
status: "⚠️ 过于粗粒度，不建议直接分发"
see_also:
  - "docs/plans/evolution-ops/06-generic-runner-implementation-packages.md"
```

### PKG-UNI-02E: Data Baseline Closure **[已完成 - 2026-03-18]**

```yaml
package_id: "PKG-UNI-02E"
owner: "doc-worker"
tree_path: "math benchmark architecture"
task_type: "data_baseline_closure"
target_rule: "math_benchmark.py | math_ag_benchmark.py"
goal: "记录 PKG-UNI-02D-fix 的结论：AG unified CLI 与 wrapper 一致，差异来自数据版本而非代码 regression"
context:
  - "worktree 2124 data/output/aligned_topics_hierarchy.json 时间戳为 2026-03-10 21:15:21"
  - "主目录对应数据时间戳为 2026-03-17 01:51:00"
  - "python3 pipeline/math_ag_benchmark.py 与 python3 pipeline/math_benchmark.py --domain math_ag 结果一致 (均为 2/6 passed)"
evidence_verified:
  - "数据文件时间戳: 2026-03-10 21:15:21"
  - "wrapper 结果: 2/6 passed"
  - "unified CLI 结果: 2/6 passed"
  - "两条路径结果完全一致"
allowed_files:
  - "docs/plans/evolution-ops/03-task-packages.md"
  - "docs/plans/evolution-ops/04-troubleshooting-and-escalation.md"
  - "docs/plans/evolution-ops/06-generic-runner-implementation-packages.md"
required_commands:
  - "stat -f '%Sm %N' -t '%Y-%m-%d %H:%M:%S' data/output/aligned_topics_hierarchy.json"
  - "python3 pipeline/math_ag_benchmark.py"
  - "python3 pipeline/math_benchmark.py --domain math_ag"
must_update_docs:
  - "记录 data-baseline issue 与 regression 的区分"
done_when:
  - "ops 文档明确说明 AG 的 2/6 来自数据版本差异"
  - "排障文档加入 benchmark 结果异常时先查数据时间戳"
  - "PKG-UNI-02D-fix 的结论可以被后续 worker 直接复用"
stop_if:
  - "发现 unified CLI 与 wrapper 结果不一致"
  - "需要修改 benchmark 文档语义或 case 定义"
conclusion: |
  ✅ wrapper 与 unified CLI 结果完全一致（均为 2/6 passed）
  ✅ 差异源于数据版本，非代码 regression
  ✅ 06-generic-runner-implementation-packages.md 已更新 Post-UNI-02E Note
  ✅ 本文档已标记为已完成
status: "✅ 已完成"
```

### PKG-QA-01: Math.QA Benchmark Skeleton Bootstrap **[已归档 - 2026-03-18]**

```yaml
package_id: "PKG-QA-01"
owner: "case-worker"
tree_path: "math > math.QA"
task_type: "benchmark_skeleton_bootstrap"
target_rule:
  - "math_qa_object_continuity"
  - "math_qa_method_continuity"
goal: "建立 math.QA benchmark skeleton，并固定第一批真实候选正负例与边界说明"
allowed_files:
  - "docs/plans/2026-03-10-evolution-rule-coverage.md"
  - "docs/plans/2026-03-12-math-worker-backlog.md"
  - "docs/plans/evolution-ops/03-task-packages.md"
  - "docs/plans/evolution-ops/08-math-qa-bootstrap-package.md"
  - "docs/plans/2026-03-18-math-qa-benchmark.md"
required_commands:
  - "make evolution-analysis"
  - "rg -n \"math\\.QA|quantum|representation|crystal|categor\" data/output/aligned_topics_hierarchy.json data/output/evolution_cases.json"
must_update_docs:
  - "math.QA benchmark 文档（新建）"
  - "registry"
  - "math worker backlog"
done_when:
  - "新建 math.QA benchmark 文档骨架"
  - "至少整理 3 个 candidate positive"
  - "至少整理 3 个 candidate negative 或 ambiguous"
  - "registry 出现 math.QA 路径与当前状态"
  - "文档明确哪些候选只是 test evidence"
stop_if:
  - "找不到 >=2 个可信的 object-side candidate positives"
  - "所有候选都只能靠泛词 quantum / representation 区分"
  - "需要引入 synthetic case"
status: "🟡 下一阶段推荐起点"
see_also:
  - "docs/plans/evolution-ops/08-math-qa-bootstrap-package.md"
archive_reason: "insufficient real math.QA data in current worktree; use PKG-QA-01A/01B instead"
```

### PKG-QA-01A: Math.QA Gap Normalization **[ACTIVE - 2026-03-18]**

```yaml
package_id: "PKG-QA-01A"
owner: "doc-worker"
tree_path: "math > math.QA"
task_type: "gap_normalization"
target_rule:
  - "math_qa_object_continuity"
  - "math_qa_method_continuity"
goal: "把 math.QA 在当前数据中的不足状态收口为 gap / insufficient real data，避免继续误判为可直接 benchmark 化"
allowed_files:
  - "docs/plans/2026-03-10-evolution-rule-coverage.md"
  - "docs/plans/2026-03-12-math-worker-backlog.md"
  - "docs/plans/evolution-ops/03-task-packages.md"
  - "docs/plans/evolution-ops/08-math-qa-bootstrap-package.md"
required_commands: []
must_update_docs:
  - "registry"
  - "math worker backlog"
done_when:
  - "registry 不再暗示 math.QA 已 ready"
  - "math.QA 明确标注为 gap / insufficient data / not benchmark-ready"
  - "task packages 明确要求先做 exploration，再决定是否恢复 bootstrap"
stop_if:
  - "需要修改 runner、测试或 benchmark 文档"
status: "🟡 当前推荐先做"
```

### PKG-QA-01B: Math.QA Longer-Window Exploration **[PLANNED - 2026-03-18]**

```yaml
package_id: "PKG-QA-01B"
owner: "case-worker"
tree_path: "math > math.QA"
task_type: "longer_window_exploration"
target_rule: "math_qa_object_continuity"
goal: "在更长历史窗口内验证 math.QA 是否能出现 >=2 个可信 object-side candidate positives"
allowed_files:
  - "docs/plans/2026-03-10-evolution-rule-coverage.md"
  - "docs/plans/2026-03-12-math-worker-backlog.md"
  - "docs/plans/evolution-ops/03-task-packages.md"
  - "docs/plans/evolution-ops/08-math-qa-bootstrap-package.md"
  - "docs/plans/2026-03-18-math-qa-benchmark.md"
required_commands:
  - "make evolution-analysis"
  - "rg -n \"math\\.QA|quantum|representation|crystal|categor\" data/output/aligned_topics_hierarchy.json data/output/evolution_cases.json"
must_update_docs:
  - "记录 longer-window exploration 的结论"
done_when:
  - "明确回答更长窗口后是否出现 >=2 个可信 object-side candidate positives"
  - "明确回答是否值得恢复 PKG-QA-01 skeleton 流程"
  - "若仍不足，写明继续停止的原因"
stop_if:
  - "探索后仍只有泛词 quantum / representation 级别重叠"
  - "需要引入 synthetic case"
  - "需要改代码或新增 runner"
status: "🟡 仅在 QA 继续探索时执行"
```

### PKG-RA-01: Math.RA Bootstrap With Decision Fork **[ACTIVE - 2026-03-18]**

```yaml
package_id: "PKG-RA-01"
owner: "case-worker"
tree_path: "math > math.RA"
task_type: "bootstrap_with_decision_fork"
target_rule:
  - "math_ra_object_continuity"
  - "math_ra_method_continuity"
goal: "判断 math.RA 是否具备 benchmark skeleton 条件；若具备则直接建立 skeleton，若不足则直接收口为 gap"
allowed_files:
  - "docs/plans/2026-03-10-evolution-rule-coverage.md"
  - "docs/plans/2026-03-12-math-worker-backlog.md"
  - "docs/plans/evolution-ops/03-task-packages.md"
  - "docs/plans/evolution-ops/09-math-ra-bootstrap-package.md"
  - "docs/plans/2026-03-18-math-ra-benchmark.md"
required_commands:
  - "make evolution-analysis"
  - "rg -n \"math\\.RA|ring|rings|module|modules|ideal|ideals|algebra|algebras|homological|derived\" data/output/aligned_topics_hierarchy.json data/output/evolution_cases.json"
must_update_docs:
  - "registry"
  - "math worker backlog"
  - "若 Option A：math.RA benchmark 文档（新建）"
done_when:
  - "完成 candidate harvest 与 boundary classification"
  - "明确给出 Option A 或 Option B"
  - "若 Option A：新建 math.RA benchmark 文档骨架"
  - "若 Option B：完成 gap 收口"
stop_if:
  - "所有候选都只能靠 algebra / module / representation 这类泛词区分"
  - "需要引入 synthetic case"
  - "需要修改 runner、tests 或 Makefile"
status: "🟡 若转向新方向，推荐从这里开始"
see_also:
  - "docs/plans/evolution-ops/09-math-ra-bootstrap-package.md"
```

### PKG-PR-01: Math.PR Bootstrap With Decision Fork **[COMPLETED - 2026-03-18]**

```yaml
package_id: "PKG-PR-01"
owner: "case-worker"
tree_path: "math > math.PR"
task_type: "bootstrap_with_decision_fork"
target_rule:
  - "math_pr_object_continuity"
  - "math_pr_method_continuity"
goal: "利用 math-focused export 判断 math.PR 是否具备 benchmark skeleton 条件；若具备则直接建立 skeleton，若不足则直接收口为 gap"
allowed_files:
  - "docs/plans/2026-03-10-evolution-rule-coverage.md"
  - "docs/plans/2026-03-12-math-worker-backlog.md"
  - "docs/plans/evolution-ops/03-task-packages.md"
  - "docs/plans/2026-03-18-math-pr-benchmark.md"
required_commands:
  - "python3 pipeline/evolution_analysis.py --input data/output/aligned_topics_hierarchy.json --output-dir data/output/math_discovery_pr --max-cases 20 --category-filter math"
must_update_docs:
  - "docs/plans/2026-03-18-math-pr-benchmark.md"
  - "docs/plans/2026-03-12-math-worker-backlog.md"
  - "docs/plans/evolution-ops/03-task-packages.md"
done_when:
  - "完成 math-focused candidate harvest"
  - "完成 boundary classification"
  - "明确给出 Option A 或 Option B"
  - "若 Option A：建立 math.PR benchmark skeleton 文档"
  - "若 Option B：完成 gap 收口"
stop_if:
  - "所有候选都只能靠 generic probability / stochastic / random 区分"
  - "需要修改 pipeline、tests 或 Makefile"
  - "需要引入 synthetic case"
decision: "Provisional Skeleton Candidate (修正: 从过强的 'Option A skeleton-ready' 收成稳态)"
result: "Pre-Skeleton Assessment Complete / Needs PR-Specific Case Surfacing Before Curation"
verification:
  corrected_command: "python3 -c 'import json; data=json.load(open(\"data/output/aligned_topics_hierarchy.json\")); pr_ids=set(data[\"hierarchies\"][\"math.PR\"][\"topic_assignments\"].keys()); trends=data.get(\"trends\",{}); multi=[t for t in pr_ids if t in trends and trends[t].get(\"active_periods\",0)>1]; print(f\"Multi-period PR topics: {len(multi)}\")'"
  corrected_result: "12 multi-period PR topics"
  wrong_command: "python3 -c 'import json; data=json.load(open(\"data/output/aligned_topics_hierarchy.json\")); pr_ids=set(data[\"hierarchies\"][\"math.PR\"][\"topic_assignments\"].keys()); trends=data.get(\"trends\",{}); multi=[t for t in pr_ids if t in trends and len(trends[t].get(\"periods\",[]))>1]; print(f\"Multi-period PR topics: {len(multi)}\")'"
  wrong_result: "0 multi-period PR topics (field 'periods' does not exist)"
key_findings:
  strong_evidence:
    - "29 PR topics total"
    - "12 multi-period topics (confirmed via active_periods)"
    - "6 eligible anchors (papers>=60, periods>=2, neighbors>=2)"
  inferred_candidates:
    - "3 evolution chains (from neighbor analysis, not yet explicit cases)"
    - "positive/negative case candidates (hypothesized, not yet fixed)"
  evidence_gaps:
    - "explicit exported PR cases count unknown"
    - "neighbor relationships != verified evolution cases"
    - "pre-curation: no fixed cases yet"
assessment: "底层结构证据强 (multi-period topics)，但 explicit cases 需专门 surfacing"
corrected_assessment:
  multi_period_topics: 12
  single_period_topics: 17
  eligible_anchors: 6
  evidence_strength: "multi-period structure confirmed"
  candidate_chains: 3
  candidate_source: "neighbor relationship inference"
  explicit_cases_status: "requires PR-specific case surfacing"
  temporal_pairs_available: "potential (via neighbor relationships), not yet explicit"
positive_case_candidates:
  - "global_39 -> global_99 (percolation continuity)"
  - "global_99 -> global_188 (rough path evolution)"
  - "global_38 -> global_156 (random matrix continuity, global_38 is older source)"
negative_case_candidates:
  - "global_39 (percolation) vs global_156 (random matrix): different objects"
  - "global_61 (queueing) vs pure probability: applied vs theoretical boundary"
  - "global_211 (population) vs global_39 (percolation): biological vs physical"
next_package: "MPR-01B: PR-Specific Case Surfacing (conditional to MPR-02)"
```

### PKG-PR-01B: Math.PR PR-Specific Case Surfacing **[COMPLETED - 2026-03-18]**

**STATUS: ✅ 已完成 - 决策: 不满足 MPR-02 解锁条件，保持 Provisional**

```yaml
package_id: "PKG-PR-01B"
owner: "case-worker"
tree_path: "math > math.PR"
task_type: "pr_specific_case_surfacing"
target_rule:
  - "math_pr_object_continuity"
  - "math_pr_method_continuity"
goal: "把 math.PR 的底层结构证据显式 surfacing 成 candidate cases，并判断是否足以解锁 MPR-02 curation"
allowed_files:
  - "docs/plans/2026-03-18-math-pr-benchmark.md"
  - "docs/plans/2026-03-12-math-worker-backlog.md"
  - "docs/plans/evolution-ops/03-task-packages.md"
  - "docs/plans/evolution-ops/11-math-pr-case-surfacing-package.md"
required_commands:
  - "python3 pipeline/evolution_analysis.py --input data/output/aligned_topics_hierarchy.json --output-dir data/output/math_discovery_pr_surfacing --max-cases 20 --category-filter math"
done_when:
  - "explicit exported PR cases 与 graph-inferred candidate cases 被区分"
  - "明确判断是否解锁 MPR-02"
evidence_summary:
  input_scope: "math-wide 20-case export (not PR-only surfacing)"
  explicit_exported_cases:
    count: 1
    cases:
      - "global_39: 随机过程渗流方程 (5% of 20 cases)"
  strong_inferred_candidates:
    count: 3
    cases:
      - "global_39 -> global_99 (percolation continuity)"
      - "global_39 -> global_65 (SDE convergence)"
      - "global_39 -> global_188 (rough paths)"
  boundary_negatives:
    count: 2
    cases:
      - "global_39 vs global_156 (different objects)"
      - "global_61 vs pure probability (applied vs theoretical)"
  ambiguous_review_needed:
    count: 1
    cases:
      - "global_65 vs global_188 (classical vs rough path)"
  neighbor_schema: "1046 edges in topic graph, 96 involve PR topics; evolution cases have neighbor_topics field"
decision: "保持 Provisional - MPR-02 🔒 LOCKED"
decision_reason: "insufficient evidence from current export scope (not data-baseline issue); need PR-targeted extraction"
stop_if:
  - "所有候选都只能靠 generic probability / stochastic / random 区分"
  - "需要修改 pipeline、tests 或 Makefile"
  - "需要引入 synthetic case"
must_update_docs:
  - "docs/plans/2026-03-18-math-pr-benchmark.md"
  - "docs/plans/2026-03-12-math-worker-backlog.md"
  - "docs/plans/evolution-ops/03-task-packages.md"
status: "✅ 已完成 - 不满足解锁条件"
next_package: "MPR-01C: PR-targeted candidate extraction"
next_package_goal: "真正的 PR-specific surfacing (非 math-wide sample)"
see_also:
  - "docs/plans/evolution-ops/11-math-pr-case-surfacing-package.md"
```

### PKG-PR-01C: Math.PR PR-Targeted Candidate Extraction **[COMPLETED - 2026-03-20]**

**STATUS: ✅ 已完成 — MPR-02 已解锁 (Option A)**

```yaml
package_id: "PKG-PR-01C"
owner: "case-worker"
tree_path: "math > math.PR"
task_type: "pr_targeted_candidate_extraction"
target_rule:
  - "math_pr_object_continuity"
  - "math_pr_method_continuity"
precondition: "MPR-01B 完成，保持 Provisional"
goal: "做一次真正的 PR-targeted candidate extraction，从 hierarchy-scoped PR topic universe 和 topic_graph.json 边中提取候选对，判断 MPR-02 是否解锁"
approach:
  - "直接从 aligned_topics_hierarchy.json 提取 math.PR 的 29 个 topic 及 11 个 eligible anchors"
  - "从 topic_graph.json 提取 PR-internal evolves_from 和 adjacent 边"
  - "区分 explicit graph evidence vs neighbor inference"
  - "执行 boundary analysis (PR vs math.ST/AP/MP/NA)"
evidence_summary:
  pr_universe: "29 topics, 12 multi-period, 11 eligible anchors"
  evolves_from_source: "3 PR-internal evolves_from edges from MAIN data/output/topic_graph.json (NOT from targeted export which has adjacent_to only)"
  explicit_evolves_from_internal: 3
    - "global_38 -> global_100 (random limits -> random matrix ensemble): evolves_from main graph + adjacency bw=0.35"
    - "global_38 -> global_156 (random limits -> random matrix eigenvalue): evolves_from main graph + adjacency bw=0.4077"
    - "global_38 -> global_99 (random limits -> random walk/branching): evolves_from main graph, no adjacency"
  strong_inferred_method: 1
    - "global_65 -> global_188 (SDE convergence -> rough McKean, bw=0.4795)"
  boundary_negatives: 3
    - "global_211 (population ecology, wrong domain)"
    - "global_47 (Ising/Potts, math.MP crossover)"
    - "global_61 (queueing, applied vs theoretical)"
  ambiguous: 1
    - "global_65 vs global_39 (both stochastic, different objects)"
decision: "Option A — MPR-02 UNLOCKED"
decision_reason: "3 evolves_from edges from main topic_graph.json + strong adjacent evidence + 3 clear negatives + 1 ambiguous; NOT relying on generic words (eigenvalues, matrices, percolation, martingale)"
caveat: "All positive pairs are strong inferred (graph-derived), NOT benchmark-confirmed. MPR-02 curation is needed to fix benchmark cases."
correction: "MPR-01C-fix corrected source attribution and bw error; MPR-01C-final-fix (2026-03-20) corrected evolves_from direction semantics: source=OLDER topic, target=NEWER topic (confirmed from pipeline/evolution_analysis.py build_evolves_edges). Pairs P1/P2/P3 had source/target swapped in all prior MPR-01C versions. Corrected to global_38->100/156/99 (global_38 is older, active 2025-02/03). Task type: semantic_correction / direction_correction. MPR-02 remains UNLOCKED (Option A). Decision unchanged after direction correction."
allowed_files:
  - "docs/plans/2026-03-18-math-pr-benchmark.md"
  - "docs/plans/2026-03-12-math-worker-backlog.md"
  - "docs/plans/evolution-ops/03-task-packages.md"
  - "docs/plans/2026-03-20-math-pr-candidate-extraction.md"
required_commands:
  - "python3 pipeline/evolution_analysis.py --input data/output/aligned_topics_hierarchy.json --output-dir data/output/math_discovery_pr_targeted --max-cases 20 --category-filter math"
done_when:
  - "✅ 完成 PR-targeted candidate extraction 文档"
  - "✅ 明确区分 explicit / strong inferred / negative / ambiguous"
  - "✅ 固定 4 个 positive candidate pairs (3 object + 1 method)"
  - "✅ MPR-02 解锁判断: Option A"
new_doc: "docs/plans/2026-03-20-math-pr-candidate-extraction.md"
status: "✅ 已完成"
next_package: "MPR-02: Case Curation (NOW UNLOCKED)"
```

### MPR-02: Math.PR Case Curation **[COMPLETED - 2026-03-21]**

**STATUS: ✅ COMPLETE — case curation done, conditional graph integration readiness confirmed**

```yaml
package_id: "MPR-02"
owner: "case-worker"
tree_path: "math > math.PR"
task_type: "case_curation"
status: "✅ COMPLETE"
completion_date: "2026-03-21"

summary:
  curated_positives: 4
  tier_a_count: 2
  tier_b_count: 2
  curated_negatives: 5
  ambiguous_cases: 2

tier_a_pairs:
  - "global_38 -> global_100 (PR-P1)"
  - "global_38 -> global_156 (PR-P2)"

tier_b_pairs:
  - "global_38 -> global_99 (PR-P3)"
  - "global_65 -> global_188 (PR-P4)"

graph_integration_readiness: "CONDITIONAL"
next_package: "PR Phase 2C — conditional graph integration planning"

residual_risks:
  - "R1: global_38 transience (2 periods only)"
  - "R2: P4 adjacency-only, no evolves_from"
  - "R3: PR/AP boundary for P4 nodes"

decision: "Option 2C — proceed to conditional graph integration planning"

reference: "docs/plans/2026-03-21-math-pr-case-curation.md"
```

---

### PR-2C: math.PR Phase 2C Conditional Integration Planning **[✅ PLANNING COMPLETE — 2026-03-22]**

**STATUS: ✅ PLANNING COMPLETE**

```yaml
package_id: "PR-2C"
owner: "planner-worker"
tree_path: "math > math.PR > conditional graph integration"
task_type: "integration_planning"
status: "✅ PLANNING COMPLETE"
completion_date: "2026-03-22"

integration_gate_current: "Gate 0 — Curated, Not Integrated"
integration_gate_next: "Gate 1 — Conditional Graph-Visible"

schema_changes_required:
  count: 7
  all_backward_compatible: true

export_changes_required:
  count: 4
  breaks_baseline: false
  new_output_dir: "data/output/kg_v1_pr_conditional/"

bundle_changes_required:
  count: 3
  backward_compatible: true

frontend_changes_required:
  count: 5
  risk: "LOW"
  pr_color_already_mapped: true

decision: "Option C — begin conditional implementation (Track A); paper review runs in parallel (Track B)"
next_package: "PR-2C-impl — conditional layer implementation"

residual_risks:
  - "R1: global_38 transience"
  - "R2: P4 adjacency-only fragility"
  - "R3: PR/AP boundary for P4 nodes"
```

Reference: `docs/plans/2026-03-22-math-pr-phase-2c-integration-plan.md`

---

### PR-2C-impl: math.PR Conditional Layer Implementation **[NEXT — UNLOCKED]**

**STATUS: 🔓 NEXT — unlocked by PR-2C**

```yaml
package_id: "PR-2C-impl"
owner: "tbd"
tree_path: "math > math.PR > conditional graph integration > implementation"
task_type: "implementation"
gate: "Gate 0 → Gate 1 (conditional graph-visible)"
unlocked_by: "PR-2C"

scope:
  track_a_code:
    - "Add 7 nullable schema fields to topic node/edge models"
    - "Add PR conditional export path in math_kg_export.py (flag-gated, target_subcategories unchanged)"
    - "Write integration tests: LO+AG baseline isolation must pass"
    - "Write unit tests: new schema fields serialize correctly"
  track_b_parallel:
    - "Paper-level review: global_38, global_65, global_188 (no code dependency)"

out_of_scope:
  - "Removing target_subcategories = {'LO', 'AG'} guard"
  - "Exposing PR on default frontend"
  - "Baseline inclusion (Gate 2)"

reference: "docs/plans/2026-03-22-math-pr-phase-2c-integration-plan.md (Section 3 — Integration Gates)"
```

---

### PKG-MATH-KG-01: Math Historical Topic Evolution Knowledge Graph **[HISTORICAL PACKAGE]**

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
status: "✅ 已完成 - 2026-03-19"
see_also:
  - "docs/plans/evolution-ops/12-math-knowledge-graph-package.md"
```

### KG-02: Math KG v1 Export Implementation **[COMPLETED - 2026-03-19]**

```yaml
package_id: "KG-02"
owner: "rule-worker"
tree_path: "math knowledge graph"
task_type: "graph_export_implementation"
target_rule:
  - "math historical topic evolution graph"
  - "benchmark-to-graph export"
goal: "实现 LO + AG confirmed baseline 的 Math KG v1 exporter，输出 nodes/edges split files 与 validation metadata"
allowed_files:
  - "pipeline/math_kg_export.py"
  - "tests/test_math_kg_export.py"
  - "docs/plans/evolution-ops/13-math-kg-export-package.md"
  - "docs/plans/evolution-ops/03-task-packages.md"
required_commands:
  - "pytest tests/test_math_kg_export.py -q"
  - "python3 pipeline/math_kg_export.py --input data/output/aligned_topics_hierarchy.json --benchmark-lo docs/plans/2026-03-12-math-lo-benchmark.md --benchmark-ag docs/plans/2026-03-18-math-ag-benchmark.md --output-dir data/output/kg_v1"
done_when:
  - "KG v1 directory structure created with 10 files"
  - "Hierarchy-scoped LO+AG baseline encoded (9 of 18 cases: 4 LO + 5 AG)"
  - "math.PR explicitly excluded from baseline"
  - "74 tests passing"
  - "Validation report shows 0 schema errors, status: valid"
completion_verify:
  - ✅ "pipeline/math_kg_export.py implemented (18.4KB)"
  - ✅ "tests/test_math_kg_export.py created (74 tests)"
  - ✅ "32 topics exported (15 LO + 17 AG) - hierarchy topic_assignments scope"
  - ✅ "9 evolves_to edges with benchmark annotations (hierarchy-scoped baseline)"
  - ✅ "63 neighbor_of edges using real graph adjacency (not clique-generated)"
  - ✅ "metadata.json with correct scope and counts"
  - ✅ "validation_report.json: status=valid, 0 errors"
  - ✅ "math.PR not in output (correctly excluded)"
stop_if:
  - "需要修改 evolution_analysis.py"
  - "需要把 PR provisional 数据强行塞进 baseline"
  - "需要把 QA/RA/RT 混进输出"
next_recommended: "KG-03 visualization prep OR MPR-01C PR extraction"
```

### KG-02-fix: Math KG Export Corrections **[COMPLETED - 2026-03-19]**

```yaml
package_id: "KG-02-fix"
owner: "rule-worker"
tree_path: "math knowledge graph"
task_type: "data_quality_fix"
target_rule:
  - "math historical topic evolution graph"
  - "benchmark-to-graph export"
goal: "修复 KG-02 导出中的三个数据质量问题：topic source、neighbor adjacency、test infrastructure"
allowed_files:
  - "docs/plans/evolution-ops/13-math-kg-export-package.md"
  - "docs/plans/evolution-ops/03-task-packages.md"
required_commands: []
must_update_docs:
  - "docs/plans/evolution-ops/13-math-kg-export-package.md"
done_when:
  - "Topic Source Fix documented: hierarchy topic_assignments is source-of-truth"
  - "Neighbor Adjacency Fix documented: real graph edges vs clique generation"
  - "Test Infrastructure Fix documented: temporary directory vs fixed path"
fixes:
  - topic_source:
      was: "Used trends[*].subcategory (gave LO=29)"
      now: "Uses hierarchies['math.LO']['topic_assignments'] (correct LO=15)"
      why: "hierarchy topic_assignments is the source-of-truth for baseline"
  - neighbor_adjacency:
      was: "Generated clique edges from subcategory membership (241 fake edges)"
      now: "Uses real graph adjacency from input data"
      why: "Clique generation creates artificial relationships"
  - test_infrastructure:
      was: "Tests read from fixed workspace path"
      now: "Tests use temporary directory with fresh export"
      why: "Ensures tests validate current code, not old output"
status: "✅ 已完成"
```

### KG-03: Math KG Visualization Preparation **[COMPLETED - 2026-03-19]**

```yaml
package_id: "KG-03"
owner: "docs-agent"
tree_path: "math knowledge graph"
task_type: "visualization_preparation_layer"
target_rule:
  - "math historical topic evolution graph"
  - "visualization data bundle"
goal: "Create visualization-preparation layer for Math KG v1: transform kg_v1/ into frontend-ready bundle format"
scope:
  included:
    - "math.LO (15 topics, ready)"
    - "math.AG (17 topics, ready)"
  excluded:
    - "math.PR (deferred to Phase 2C)"
    - "math.QA (gap)"
    - "math.RA (gap)"
input_contract: "data/output/kg_v1/"
output_contract: "data/output/kg_v1_visualization/"
bundle_format:
  - "graph_bundle.json - Consolidated graph bundle"
  - "subgraph_lo.json - LO-only subgraph"
  - "subgraph_ag.json - AG-only subgraph"
  - "timeline_summary.json - Period-based summary"
  - "legend.json - Schema definitions"
allowed_files:
  - "pipeline/math_kg_visualization_export.py"
  - "tests/test_math_kg_visualization_export.py"
  - "docs/plans/evolution-ops/14-math-kg-visualization-package.md"
  - "docs/plans/evolution-ops/03-task-packages.md"
  - "docs/plans/2026-03-19-math-knowledge-graph.md"
required_commands:
  - "python3 pipeline/math_kg_visualization_export.py --input-dir data/output/kg_v1 --output-dir data/output/kg_v1_visualization"
  - "pytest tests/test_math_kg_visualization_export.py -q"
must_update_docs:
  - "docs/plans/evolution-ops/14-math-kg-visualization-package.md"
done_when:
  - "✅ pipeline/math_kg_visualization_export.py implemented"
  - "✅ tests/test_math_kg_visualization_export.py created (56 tests)"
  - "✅ 5 bundle files generated in data/output/kg_v1_visualization/"
  - "✅ Frontend contract documented with field clarifications"
  - "✅ Input/output contracts defined"
  - "✅ Next recommendation documented (KG-04 vs MPR-01C)"
completion_verify:
  - ✅ "graph_bundle.json: 32 topics, 181 edges"
  - ✅ "subgraph_lo.json: 15 topics, 4 evolves_to edges"
  - ✅ "subgraph_ag.json: 17 topics, 5 evolves_to edges"
  - ✅ "timeline_summary.json: 13 periods"
  - ✅ "legend.json: schema definitions"
  - ✅ "56 tests passing"
  - ✅ "Frontend contract: code field documented as canonical for filtering"
stop_if:
  - "需要修改 pipeline/math_kg_export.py"
  - "需要把 PR 数据加入输出"
  - "需要实现 D3/Cytoscape 渲染"
next_recommendation:
  option_a:
    name: "KG-04 Frontend Integration"
    condition: "Bundle validation passes"
    action: "Implement frontend data loading and D3/Cytoscape visualization"
  option_b:
    name: "MPR-01C PR-Targeted Extraction"
    condition: "PR integration prioritized"
    action: "Execute PR-specific candidate extraction in parallel"
status: "✅ 已完成"
```

---

### KG-04: Math KG Frontend Integration **[COMPLETED - 2026-03-19]**

```yaml
package_id: "KG-04"
owner: "orchestrator"
tree_path: "frontend"
task_type: "frontend_integration"
target_rule: "knowledge-graph visualization page"
goal: "First version of Math KG v1 visualization page in existing React frontend"
commit: "bfcc6e9 feat(kg): KG-04 - Math Knowledge Graph v1 frontend integration"
files_created:
  - "frontend/src/hooks/useKnowledgeGraph.js"
  - "frontend/src/views/KnowledgeGraph.jsx"
  - "frontend/src/components/GraphVisualization.jsx"
  - "frontend/src/components/GraphFilters.jsx"
  - "frontend/src/components/TopicDetail.jsx"
  - "frontend/src/components/TimelineSummary.jsx"
files_modified:
  - "frontend/src/App.jsx: added /knowledge-graph route and NavLink"
features:
  - "D3 force-directed graph with zoom/pan/drag"
  - "Subcategory/edge-kind/confidence filters"
  - "Topic detail sidebar"
  - "Recharts timeline bar chart"
done_criteria:
  - ✅ "前端可加载 KG-03 bundle"
  - ✅ "页面可展示 LO+AG 图谱"
  - ✅ "支持 subcategory / edge kind / confidence 过滤"
  - ✅ "支持 topic 选中后的详情查看"
  - ✅ "构建通过 (vitest 4/4, vite build success)"
reference: "docs/plans/evolution-ops/15-math-kg-frontend-package.md"
status: "✅ 已完成"
```

### KG-04-fix: Math KG Frontend Bug Fixes **[COMPLETED - 2026-03-20]**

```yaml
package_id: "KG-04-fix"
owner: "orchestrator"
tree_path: "frontend"
task_type: "frontend_bug_fix"
target_rule: "knowledge-graph visualization page"
goal: "Fix three post-KG-04 issues: filter contract normalization, useSubcategory code lookup, TimelineSummary mount"
fixes:
  - filter_contract_normalization:
      file: "frontend/src/hooks/useKnowledgeGraph.js"
      was: "Raw KG-03 bundle filter arrays passed directly to components"
      now: "Hook normalizes to [{value, code, label}] / [{value, label}] / [{value, label, color}] before return"
  - use_subcategory_canonical_code:
      file: "frontend/src/hooks/useKnowledgeGraph.js"
      was: "useSubcategory('math.LO') returned no topics (compared full form vs short form)"
      now: "Strips 'math.' prefix before comparing with t.subcategory (which stores 'LO', 'AG', etc.)"
  - timeline_summary_mount:
      file: "frontend/src/views/KnowledgeGraph.jsx"
      was: "TimelineSummary component existed but was never imported or rendered"
      now: "Imported, timeline_summary.json loaded via useEffect, rendered as full-width row after graph grid"
done_criteria:
  - ✅ "Filter normalization in hook layer — components receive [{value, label, ...}] not raw strings"
  - ✅ "useSubcategory('math.LO') correctly returns LO topics"
  - ✅ "TimelineSummary visible on /knowledge-graph page"
  - ✅ "vitest 4/4 pass, vite build success"
status: "✅ 已完成"
see_also: "docs/plans/evolution-ops/15-math-kg-frontend-package.md (Post-Fix Notes section)"
```

---

### KG-05: Math KG Visualization Enhancement **[COMPLETED - 2026-03-20]**

```yaml
package_id: "KG-05"
owner: "frontend-worker"
tree_path: "math knowledge graph"
task_type: "frontend_enhancement"
target_rule:
  - "kg visualization exploration experience"
  - "evidence-aware graph interaction"
goal: "在 KG-04 稳定基线之上，增强知识图谱页面的可探索性、视觉层次和交互体验"
baseline: "KG-04-fix (d9a4bae)"
enhancements:
  graph_visualization:
    - "Hover highlight with neighbor dimming"
    - "EVOLVES_TO edge arrow markers"
    - "Selection ring for selected node"
    - "Reset view button"
  topic_detail:
    - "Edge type badges with colors"
    - "Priority sort (EVOLVES_TO confirmed first)"
    - "Evidence summary stats"
    - "Benchmark evidence indicator"
  graph_filters:
    - "Active filter summary badge"
    - "One-click preset buttons"
    - "Smart reset with count"
  timeline:
    - "Trend analysis insight text"
    - "Localized labels"
    - "Period range display"
  page:
    - "Baseline scope badge (LO + AG · v1)"
    - "Selection context strip"
    - "Improved help text"
constraints_maintained:
  - "LO + AG only, no math.PR"
  - "No KG-03 bundle schema changes"
  - "No new backend"
done_criteria:
  - ✅ "hover/select interaction enhancement"
  - ✅ "evidence-aware visual language"
  - ✅ "better detail panel analysis value"
  - ✅ "timeline trend insight"
  - ✅ "vitest pass, vite build pass"
status: "✅ 已完成"
see_also: "docs/plans/evolution-ops/16-math-kg-enhancement-package.md"
```

---

### KG-05-fix: GraphFilters "全部显示" Preset Correction **[COMPLETED - 2026-03-20]**

```yaml
package_id: "KG-05-fix"
owner: "frontend-worker"
tree_path: "frontend"
task_type: "frontend_bug_fix"
target_rule: "knowledge-graph visualization page"
goal: "修正 GraphFilters.jsx 中 '全部显示' preset 语义，confidence 重置为 ['confirmed', 'ambiguous', 'negative', 'data-derived']（全量），同步 DEFAULT_CONFIDENCE"
fixes:
  - show_all_preset:
      file: "frontend/src/components/GraphFilters.jsx"
      was: "confidence: ['confirmed', 'ambiguous']（漏掉 negative）"
      now: "confidence: ['confirmed', 'ambiguous', 'negative', 'data-derived']（全量）"
  - default_confidence:
      file: "frontend/src/components/GraphFilters.jsx"
      was: "DEFAULT_CONFIDENCE = ['confirmed', 'ambiguous']"
      now: "DEFAULT_CONFIDENCE = ['confirmed', 'ambiguous', 'negative', 'data-derived']"
status: "✅ 已完成"
```

---

### PKG-MATH-FOCUSED-EXPORT-01-IMPL: Math-Focused Export Implementation **[COMPLETED - 2026-03-18]**

```yaml
package_id: "PKG-MATH-FOCUSED-EXPORT-01-IMPL"
owner: "docs-agent"
tree_path: "math"
task_type: "cli_implementation"
target_rule:
  - "evolution_cases representative export"
  - "math case discovery input"
goal: "实现 --category-filter CLI 选项，支持 math-focused export"
implementation:
  - "新增 --category-filter 参数"
  - "支持按类别筛选 topics"
  - "不破坏原有 category rotation 逻辑"
  - "可与 --max-cases 组合使用"
command_example: |
  python3 pipeline/evolution_analysis.py \
    --input data/output/aligned_topics_hierarchy.json \
    --output-dir data/output/math_discovery \
    --max-cases 20 \
    --category-filter math
expected_output:
  - "data/output/math_discovery/evolution_cases.json"
  - "15-20 math cases with full details"
  - "涵盖 AG, LO, PR, AP, OC, NA, CO, GR 等子域"
completion_verify:
  - ✅ "--category-filter CLI 选项可用"
  - ✅ "math-focused export 产出正确"
  - ✅ "不破坏原有功能"
  - ✅ "文档已更新"
status: "completed"
next_recommended: "math.PR discovery using math-focused export output"
```

---

## Dispatch Rules

默认 dispatch 顺序：

1. `PKG-PLG-01`
2. `PKG-PLG-02`
3. `PKG-AG-01` ✅ 已完成
4. `PKG-AG-02` ✅ 已完成
5. `PKG-AG-03A` ✅ 已归档 (选择 Option B)
6. `PKG-AG-03B-normalization` ✅ 已完成
7. `PKG-AG-04` ✅ 已完成 (object_continuity runner)
8. `PKG-UNI-01` ✅ 已完成 (设计文档)
9. `PKG-UNI-02`（仅作占位，不直接分发）
10. `PKG-UNI-02A` ✅ 已完成
11. `PKG-UNI-02B` ✅ 已完成
12. `PKG-UNI-02C` ✅ 已完成
13. `PKG-UNI-02D` ✅ 已完成
14. `PKG-UNI-02E` ✅ 已完成
15. `PKG-QA-01` ✅ 已归档
16. `PKG-QA-01A` 🟡 推荐下一步
17. `PKG-QA-01B` ⏸️ 仅在需要更长窗口探索时执行
18. `PKG-RA-01` 🟡 若转向其他方向，推荐从这里开始
19. `KG-04` ✅ 已完成 (Math KG v1 frontend integration)
20. `KG-04-fix` ✅ 已完成 (filter normalization, useSubcategory fix, TimelineSummary mount)
21. `KG-05` ✅ 已完成 (Math KG visualization enhancement)
22. `KG-05-fix` ✅ 已完成 ("全部显示" preset confidence 修正为全量，同步 DEFAULT_CONFIDENCE)
23. `PKG-PR-01C` ✅ 已完成 (PR-targeted candidate extraction, MPR-02 解锁)
24. `MPR-02` ✅ 已完成 (case curation, 4 positives / 5 negatives / 2 ambiguous, conditional graph integration readiness confirmed)
25. `PR-2C` ✅ 已完成 (conditional integration planning — Gate system defined, Option C selected, PR-2C-impl scope locked)

## Assignment Rule

如果是 Claude / subagent：

- 每次只发 1 个 package
- 先把 package 内容复制到 task template 中
- 然后再进入 worker

## Forbidden Dispatch Pattern

不要这样分发：

- “继续推进 math.AG”
- “把全数学 benchmark 都补上”
- “顺手把 runner 抽象了”

这些指令都过于开放，会让弱模型打转。
