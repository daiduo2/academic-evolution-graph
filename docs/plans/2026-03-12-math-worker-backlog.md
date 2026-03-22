doc_type: "governance"
scope: "math evolution worker task packages"
status: "active"
owner: "trend-monitor"
source_of_truth: true
upstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-12-evolution-skills-design.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-10-evolution-rule-coverage.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-12-evolution-task-template.md"
downstream_docs: []
last_reviewed: "2026-03-18"

# Math Worker Backlog

## Purpose

这份文档把数学方向后续可分发给弱模型或 Claude subagent 的任务，整理成固定任务包。

原则是：

- 不给开放式“继续推进”
- 只给中等粒度、强约束、可验收的 task package

## Scope

当前 backlog 覆盖：

- `math > math.LO`
- `math > math.AG`
- `math > math.QA`（数据不足，标记为 gap）
- `math > math.RA`（数据不足，标记为 gap）
- `math > math.PR`（Gate 1 — conditional integration implemented; Gate 2 COLLAPSED post-TrackB-06; long-term Gate 1; MPR-03 dormant）
- `math knowledge graph`（第一版 schema / bootstrap 设计）
- `math`（整体数据完整性与对齐质量审计）

## Package Template

每个包都应固定包含：

- `tree_path`
- `task_owner`
- `task_type`
- `target_rule`
- `positive_case`
- `negative_case`
- `allowed_files`
- `required_commands`
- `done_when`

## Active Task Packages

### Package MMATH-01

```yaml
tree_path: "math"
task_owner: "case-worker"
task_type: "data_completeness_and_alignment_audit"
target_rule:
  - "math bootstrap eligibility"
  - "evolution case selection policy"
goal: "审计数学各子域的 topic 活跃度、跨期连续性和 anchor 可入选率，回答当前空白是数据问题还是导出策略问题"
allowed_files:
  - "docs/plans/evolution-ops/10-math-data-audit-package.md"
  - "docs/plans/2026-03-12-math-worker-backlog.md"
  - "docs/plans/2026-03-18-math-data-audit.md"
required_commands:
  - "make evolution-analysis"
  - "python3 pipeline/evolution_analysis.py --input data/output/aligned_topics_hierarchy.json --output-dir data/output/audit_math_cases --max-cases 100"
done_when:
  - "给出 math 各子域 single-period / multi-period 分布"
  - "说明 evolution_cases.json 只有 12 个的机制"
  - "明确下一步该推进 math.RT 还是先调整案例/对齐策略"
```

### Package MQA-01A

```yaml
tree_path: "math > math.QA"
task_owner: "doc-worker"
task_type: "gap_normalization"
target_rule:
  - "math_qa_object_continuity"
  - "math_qa_method_continuity"
goal: "当 math.QA 缺少真实案例时，把它明确收口为 gap / insufficient data，而不是继续误推进 benchmark"
allowed_files:
  - "docs/plans/2026-03-10-evolution-rule-coverage.md"
  - "docs/plans/2026-03-12-math-worker-backlog.md"
  - "docs/plans/evolution-ops/03-task-packages.md"
required_commands: []
done_when:
  - "registry 不再暗示 math.QA 已 ready"
  - "backlog 明确写出后续只能先做 longer-window exploration"
```

### Package MQA-01B

```yaml
tree_path: "math > math.QA"
task_owner: "case-worker"
task_type: "longer_window_exploration"
target_rule: "math_qa_object_continuity"
goal: "验证延长时间窗口后，math.QA 是否真的能出现可信 object-side candidate positives"
allowed_files:
  - "docs/plans/2026-03-10-evolution-rule-coverage.md"
  - "docs/plans/2026-03-12-math-worker-backlog.md"
  - "docs/plans/2026-03-18-math-qa-benchmark.md"
required_commands:
  - "make evolution-analysis"
done_when:
  - "明确回答是否值得恢复 math.QA benchmark skeleton"
  - "如果仍不足，明确停止理由"
```

### Package MLO-01

```yaml
tree_path: "math > math.LO"
task_owner: "doc-worker"
task_type: "status_cleanup"
target_rule:
  - "math_lo_forcing_continuity"
  - "math_lo_definability_continuity"
goal: "校正 registry 中 partial / ready 与 benchmark level 的一致性"
positive_case:
  anchor: "global_51"
  target: "global_951"
negative_case:
  anchor: "global_339"
  target: "global_951"
allowed_files:
  - "docs/plans/2026-03-10-evolution-rule-coverage.md"
  - "docs/plans/2026-03-12-math-lo-benchmark.md"
  - "docs/plans/2026-03-11-math-lo-rule-review.md"
required_commands:
  - "pytest tests/test_math_lo_benchmark.py -q"
  - "make math-lo-benchmark"
done_when:
  - "registry 状态与 benchmark level 一致"
  - "bridge-level 规则不再被写成 ready"
```

### Package MLO-02

```yaml
tree_path: "math > math.LO"
task_owner: "case-worker"
task_type: "review_update"
target_rule: "math_lo_type_theory_continuity"
goal: "补一组更稳定的正反例，确认它是否仍然只停留在 bridge-level"
positive_case:
  anchor: "global_56"
  target: "global_980"
negative_case:
  anchor: "global_56"
  target: "global_438"
allowed_files:
  - "docs/plans/2026-03-11-math-lo-rule-review.md"
  - "docs/plans/2026-03-12-math-lo-benchmark.md"
required_commands:
  - "make evolution-analysis"
  - "make math-lo-benchmark"
done_when:
  - "review 里明确 type-theory 是 bridge-level 还是接近 event-level"
  - "benchmark 补齐正反例备注"
```

### Package MLO-03

```yaml
tree_path: "math > math.LO > 集合论与基数理论"
task_owner: "case-worker"
task_type: "benchmark_update"
target_rule: "math_lo_set_theory_continuity"
goal: "补充集合论路径的真实 negative cases，避免只靠 cardinal/forcing 误判"
positive_case:
  anchor: "global_51"
  target: "global_75"
negative_case:
  anchor: "global_167"
  target: "global_75"
allowed_files:
  - "docs/plans/2026-03-12-math-lo-benchmark.md"
  - "docs/plans/2026-03-11-math-lo-rule-review.md"
required_commands:
  - "make math-lo-benchmark"
done_when:
  - "新增至少 1 个真实 negative case"
  - "review 中记录为何它是负例"
```

### Package MAG-01

```yaml
tree_path: "math > math.AG"
task_owner: "doc-worker"
task_type: "status_cleanup"
target_rule: "math_ag_method_continuity"
goal: "把 synthetic evidence 从 benchmark 语义中剥离，改写成 test evidence"
positive_case:
  anchor: "ag-method-b1"
  target: "synthetic"
negative_case:
  anchor: "ag-method-n1"
  target: "synthetic"
allowed_files:
  - "docs/plans/2026-03-10-evolution-rule-coverage.md"
required_commands:
  - "pytest tests/test_evolution_analysis.py -q"
done_when:
  - "registry 不再把 synthetic case 写成真实 benchmark"
  - "文档明确这部分只是 test evidence"
```

### Package MAG-02

```yaml
tree_path: "math > math.AG"
task_owner: "case-worker"
task_type: "benchmark_update"
target_rule: "math_ag_object_continuity"
goal: "继续搜集真实 positive / negative pairs，确认对象词典覆盖盲点"
positive_case:
  anchor: "global_69"
  target: "global_287"
negative_case:
  anchor: "global_30"
  target: "global_355"
allowed_files:
  - "docs/plans/2026-03-10-evolution-rule-coverage.md"
required_commands:
  - "make evolution-analysis"
done_when:
  - "新增至少 1 条真实 negative note"
  - "review registry 说明对象词典盲点"
```

### Package MAG-03A: Method Continuity Case Discovery **[ARCHIVED - 2026-03-17]**

**STATUS: ✅ 已完成决策 - 选择 Option B (进入 normalization)**

```yaml
tree_path: "math > math.AG"
task_owner: "case-worker"
task_type: "case_discovery"
target_rule: "math_ag_method_continuity"
goal: "判断 method_continuity 是否值得进入 benchmark 主流程"
result: "已决策 - 选择 Option B (case 不足，进入 normalization)"
archive_reason: "insufficient event-level data"
decision_fork:
  option_a:
    condition: "找到 >=2 个真实 event-level positive cases"
    action: "进入 MAG-03B-runner，实现 math_ag_method_continuity benchmark"
    result: "❌ 未满足"
  option_b:
    condition: "只找到 bridge-level cases 或 case 不足"
    action: "进入 MAG-03B-normalization，明确维持 test-evidence-only"
    result: "✅ 已选择"
search_criteria:
  - "共享 >=2 个方法词: cohomology/derived/motivic/tropical/étale"
  - "共享对象词 <2 个 (确保是方法连续性而非对象连续性)"
  - "有清晰的 temporal evolution 证据 (event-level)"
  - "跨期出现，而非同期并存"
current_candidates:
  - note: "已找到的 cases 均为 bridge-level"
  - ag-method-p1: "global_136 -> global_263 (2025-06 -> 2025-10)"
  - ag-method-p2: "global_237 -> global_263 (2025-09 -> 2025-10)"
  - assessment: "时间跨度太短，无法构成 event-level evolution"
allowed_files:
  - "docs/plans/2026-03-17-math-ag-benchmark.md"
  - "docs/plans/2026-03-10-evolution-rule-coverage.md"
stop_conditions:
  - "搜索后仍无 event-level cases"
  - "所有 candidate 都是同期或短期并存"
  - "与 object_continuity 边界无法区分"
done_when:
  - "明确 decision_fork 走向 (option_a 或 option_b)"
  - "文档记录决策理由"
```

### Package MAG-03B-runner: Implement Method Benchmark **[LOCKED - NOT UNLOCKED]**

**STATUS: 🔒 保持锁定 - 因 MAG-03A 选择 Option B，此包不会执行**
```yaml
tree_path: "math > math.AG"
task_owner: "rule-worker"
task_type: "benchmark_implementation"
target_rule: "math_ag_method_continuity"
precondition: "MAG-03A 必须完成且选择 option_a"
goal: "为 method_continuity 实现完整的 benchmark runner"
required_cases:
  - ">=2 event-level positive cases"
  - ">=1 negative case"
allowed_files:
  - "pipeline/math_ag_benchmark.py"
  - "tests/test_math_ag_benchmark.py"
  - "docs/plans/2026-03-17-math-ag-benchmark.md"
```

### Package MAG-03B-normalization: Scope Cleanup **[COMPLETED - 2026-03-17]**

**STATUS: ✅ 已完成 - method_continuity 已明确为 test-evidence-only**

```yaml
tree_path: "math > math.AG"
task_owner: "doc-worker"
task_type: "scope_normalization"
target_rule: "math_ag_method_continuity"
precondition: "MAG-03A 完成，选择 option_b (case 不足)"
goal: "明确将 method_continuity 从 benchmark 候选中移除，维持 test-evidence-only"
actions_completed:
  - ✅ "更新 registry: 明确标注 'test evidence only / not benchmark-ready'"
    - 文件: docs/plans/2026-03-10-evolution-rule-coverage.md
  - ✅ "更新 math-ag-benchmark.md: 将 method cases 移入 'Test Evidence' 章节"
    - 文件: docs/plans/2026-03-17-math-ag-benchmark.md
  - ✅ "更新 math_ag_benchmark.py: 移除 method continuity cases"
    - 文件: pipeline/math_ag_benchmark.py (仅剩 object_continuity cases)
  - ✅ "更新 evolution-ops: 归档 PKG-AG-03"
    - 文件: docs/plans/evolution-ops/03-task-packages.md
completion_verify:
  - ✅ method_continuity 不在 runner 中
  - ✅ 文档明确区分: object_continuity (ready) vs method_continuity (test-only)
  - ✅ 无歧义的 stop condition 已记录
  - ✅ math.AG benchmark 全绿: 6/6 passed
```

---

## Math.RA Task Packages

### Package MRA-01: Bootstrap with Decision Fork **[COMPLETED - 2026-03-18]**

**STATUS: ✅ 已完成 - math.RA 已明确为 gap / insufficient data**

```yaml
tree_path: "math > math.RA"
task_owner: "case-worker"
task_type: "bootstrap_with_decision_fork"
target_rule:
  - "math_ra_object_continuity"
  - "math_ra_method_continuity"
goal: "判断 math.RA 是否具备 benchmark skeleton 条件；若具备则直接建立 skeleton，若不足则直接收口为 gap"
data_assessment:
  total_topics: 3
  topics:
    - "global_82: 泊松-巴克斯特李代数 (32 papers, 1 period)"
    - "global_200: 多项式映射与算法 (14 papers, 1 period)"
    - "global_214: 随机矩阵与正定性 (46 papers, 1 period)"
  evolution_cases: 0
  temporal_pairs: 0
  object_continuity_candidates: "无 (所有 topics 仅 1 个 period)"
  method_continuity_candidates: "无 (所有 topics 仅 1 个 period)"
decision_fork:
  option_a:
    condition: "找到 >=2 个可信 object-side candidate positives"
    action: "建立 math.RA benchmark skeleton"
  option_b:
    condition: "case 不足，无法区分 object vs method continuity"
    action: "收口为 gap"
  decision: "Option B"
  reason: "仅3个topics，全部仅1个active month，无法构成temporal evolution，无法形成任何pairs"
actions_completed:
  - ✅ "更新 registry: math > math.RA 状态从 ready 改为 gap"
    - 文件: docs/plans/2026-03-10-evolution-rule-coverage.md
  - ✅ "新增 math_ra_gap_insufficient_data 规则条目"
    - 文件: docs/plans/2026-03-10-evolution-rule-coverage.md
  - ✅ "更新 Tree Path Registry 中 math.RA 的 notes"
  - ✅ "更新 Layer 1 Coverage 表格"
completion_verify:
  - ✅ registry 不再暗示 math.RA 已 ready
  - ✅ math.RA 明确标注为 gap / insufficient data / not benchmark-ready
  - ✅ 文档明确记录: 当前数据里 math.RA 只有 3 个 topics
  - ✅ 文档明确记录: 全部仅 1 个 active period，无法构成跨期演化
  - ✅ 文档明确记录: 现在不适合直接 benchmark 化
next_package_if_continue: "PKG-RA-01B: longer-window exploration"
```

### Package MMATH-FOCUSED-EXPORT-01: Math Discovery View **[✅ COMPLETED - 2026-03-18]**

**STATUS: ✅ 已完成 - 来自 PKG-MATH-FOCUSED-EXPORT-01-IMPL**

```yaml
tree_path: "math"
task_owner: "case-worker"
task_type: "math_focused_export"
target_rule:
  - "evolution_cases representative export"
  - "math case discovery input"
goal: "创建 math 专用的 case export，绕过 category rotation，获取 15-20 个 math cases"
evidence:
  - "60 eligible math anchors exist"
  - "12-case export only shows 1"
  - "100-case audit shows 9"
  - "9x visibility compression confirmed"
implemented_command: |
  python3 pipeline/evolution_analysis.py \
    --input data/output/aligned_topics_hierarchy.json \
    --output-dir data/output/math_discovery \
    --max-cases 20 \
    --category-filter math
expected_output:
  - "15-20 math cases with full details"
  - "涵盖 AG, LO, PR, AP, OC, NA, CO, GR 等子域"
  - "用于后续 PR/NT bootstrap 决策"
actual_output:
  - "data/output/math_discovery/evolution_cases.json"
  - "~15-20 math cases (proportional to eligible anchors)"
  - "不经过 category rotation，直接按 score 排序"
allowed_files:
  - "docs/plans/2026-03-18-math-export-review.md"
  - "data/output/math_discovery/"
required_commands:
  - "make evolution-analysis"
done_when:
  - "✅ 产出 math_discovery/evolution_cases.json"
  - "✅ 使用 --category-filter math 筛选"
  - "✅ 可与 --max-cases 组合使用"
stop_if:
  - "math cases 仍然不足 10 个"
  - "需要修改 pipeline 代码"
  - "需要引入 synthetic case"
completion_notes:
  - "新增 --category-filter CLI 选项"
  - "不破坏原有 category rotation 逻辑"
  - "✅ 修复: graph 和 report 与 filtered 语义一致 (PKG-MATH-FOCUSED-EXPORT-01-fix)"
  - "下一步推荐: math.PR discovery"
```

**下一步推荐**: math.PR discovery - 使用 math-focused export 输出进行子域 bootstrap 决策

---

---

## Math.PR Task Packages

### Package MPR-01: Bootstrap with Decision Fork **[COMPLETED - 2026-03-18]**

**STATUS: ✅ 已完成 - 决策: Provisional Skeleton Candidate (Pre-Skeleton Assessment)**

**重要修正**: 原始分析使用了不存在的 `periods` 字段，误判为 0 个 multi-period topics。使用正确的 `active_periods` 字段验证后，实际为 **12 个 multi-period topics**。

```yaml
tree_path: "math > math.PR"
task_owner: "doc-worker"
task_type: "benchmark_skeleton_bootstrap"
target_rule:
  - "math_pr_object_continuity"
  - "math_pr_method_continuity"
goal: "判断 math.PR 是否具备 benchmark skeleton 基础条件；确认 multi-period 证据，但明确需要 PR-specific case surfacing 后才能进入 curation"
data_assessment:
  total_pr_topics: 29
  multi_period_topics: 12 (使用正确的 active_periods 字段)
  single_period_topics: 17
  eligible_anchors: 6
  evolution_cases_in_export: 6
  temporal_pairs: "Yes (via neighbor relationships)"
verification_command_correct: |
  python3 -c "import json; data=json.load(open('data/output/aligned_topics_hierarchy.json'));
  pr_ids=set(data['hierarchies']['math.PR']['topic_assignments'].keys());
  trends=data.get('trends',{});
  multi=[t for t in pr_ids if t in trends and trends[t].get('active_periods',0)>1];
  print(f'Multi-period PR topics: {len(multi)}')"  # 输出: 12
verification_command_wrong: |
  python3 -c "import json; data=json.load(open('data/output/aligned_topics_hierarchy.json'));
  pr_ids=set(data['hierarchies']['math.PR']['topic_assignments'].keys());
  trends=data.get('trends',{});
  multi=[t for t in pr_ids if t in trends and len(trends[t].get('periods',[]))>1];
  print(f'Multi-period PR topics: {len(multi)}')"  # 输出: 0 (字段不存在)
decision_fork:
  option_a_fully_ready:
    condition: ">=2 可信 object-side positives, >=2 negative/ambiguous, 不靠泛词区分, explicit cases 已验证"
    action: "建立 math.PR benchmark skeleton，进入 case curation"
    result: "❌ 未满足 - explicit exported PR cases 数量不明，需要 case surfacing"
  option_b_gap:
    condition: "候选不足或边界模糊"
    action: "收口为 gap"
    result: "❌ 不适用 - 12 multi-period topics 证明底层结构存在"
  provisional:
    condition: "multi-period 证据强，但 explicit cases 需进一步 surfacing"
    action: "标记为 provisional skeleton candidate，执行 PR-specific case surfacing"
    result: "✅ 已选择 - 基础结构确认，但需显式 case surfacing 后才能进入 curation"
eligible_anchors:
  - "global_38: 随机极限与不等式 (208 papers, 2 periods)"
  - "global_39: 随机过程渗流方程 (1280 papers, 4 periods)"
  - "global_65: 随机微分方程收敛 (391 papers, 4 periods)"
  - "global_99: 随机游走与分支 (179 papers, 3 periods)"
  - "global_156: 随机矩阵特征值分析 (78 papers, 2 periods)"
  - "global_188: 随机粗糙McKean方程 (387 papers, 4 periods)"
  # Note: neighbor counts from evolution case analysis (neighbor_topics field), not topic_index
evolution_chains:
  - "渗流链: global_39 -> global_99 -> global_188"
  - "随机矩阵链: global_38 -> global_156 / global_100"
  - "随机过程链: global_39 -> global_65 -> global_188"
positive_case_candidates:
  - "global_39 (percolation) -> global_99 (random walk): object continuity"
  - "global_99 -> global_188 (rough McKean): method continuity (rough paths)"
  - "global_38 (random limits) -> global_156 (random matrix eigenvalue) / global_100 (random matrix ensemble): object continuity"
  - "global_65 (SDE convergence) -> global_188: method continuity"
negative_case_candidates:
  - "global_39 (percolation) vs global_156 (random matrix): different objects"
  - "global_61 (queueing) vs pure probability: applied vs theoretical boundary"
  - "global_211 (population) vs global_39 (percolation): biological vs physical"
actions_completed:
  - ✅ "数据验证修正: 确认 12 个 multi-period topics (使用 active_periods 字段)"
  - ✅ "更新 benchmark 文档: 标记为 provisional skeleton candidate"
    - 文件: docs/plans/2026-03-18-math-pr-benchmark.md
  - ✅ "更新 backlog: math.PR 状态改为 provisional"
    - 文件: docs/plans/2026-03-12-math-worker-backlog.md
  - 🟡 "准备 PR-specific case surfacing"
completion_verify:
  - ✅ 数据验证完成: 12 multi-period PR topics (强证据)
  - ✅ 数据验证完成: 6 eligible anchors (强证据)
  - 🟡 候选识别: 3 evolution chains (从 neighbor 推断，待验证)
  - ❓ Explicit exported PR cases: 需进一步 surfacing
  - ✅ 状态修正: 从过强的 "skeleton-ready" 改为 "provisional"
evidence_assessment:
  strong_evidence:
    - "12 multi-period topics (confirmed via active_periods)"
    - "6 eligible anchors (papers>=60, periods>=2, neighbors>=2)"
  candidate_inferred:
    - "3 evolution chains (from neighbor analysis)"
    - "positive/negative case candidates (hypothesized)"
  gaps:
    - "explicit exported PR cases count unknown"
    - "no fixed cases yet (pre-curation)"
next_package_if_continue: "MPR-01B: PR-Specific Case Surfacing"
```

### Package MPR-01B: PR-Specific Case Surfacing **[COMPLETED - 2026-03-18]**

**STATUS: ✅ 已完成 - 决策: 不满足 MPR-02 解锁条件，保持 Provisional**

```yaml
tree_path: "math > math.PR"
task_owner: "case-worker"
task_type: "case_surfacing"
target_rule:
  - "math_pr_object_continuity"
  - "math_pr_method_continuity"
precondition: "MPR-01 完成 provisional assessment"
status: "✅ 已完成 - 不满足解锁条件"
goal: "执行 PR-specific case surfacing，区分 explicit exported cases 与 graph-inferred candidate cases，并判断是否解锁 MPR-02"
approach:
  - "运行 math-focused export 到独立输出目录"
  - "识别 candidate anchors 中哪些出现在 evolution_cases 输出"
  - "区分 explicit exported PR cases 与 graph-inferred candidate pairs"
  - "固定第一批 positive / negative / ambiguous candidate pairs"
done_when:
  - "explicit exported PR cases 与 graph-inferred candidate pairs 被区分"
  - "明确判断是否解锁 MPR-02"
allowed_files:
  - "docs/plans/2026-03-18-math-pr-benchmark.md"
  - "docs/plans/2026-03-12-math-worker-backlog.md"
  - "docs/plans/evolution-ops/03-task-packages.md"
required_commands:
  - "python3 pipeline/evolution_analysis.py --input data/output/aligned_topics_hierarchy.json --output-dir data/output/math_discovery_pr_surfacing --max-cases 20 --category-filter math"
evidence_summary:
  input_scope: "math-wide 20-case export (not PR-only)"
  explicit_exported_cases: 1
    - "global_39: 随机过程渗流方程 (only PR anchor in 20 cases, 5%)"
  strong_inferred_candidates: 3
    - "global_39 -> global_99 (percolation continuity)"
    - "global_39 -> global_65 (SDE convergence)"
    - "global_39 -> global_188 (rough paths)"
  boundary_negatives: 2
    - "global_39 vs global_156 (different objects)"
    - "global_61 vs pure probability (applied vs theoretical)"
  ambiguous_review_needed: 1
    - "global_65 vs global_188 (classical vs rough path)"
  neighbor_info: "1046 edges in topic graph, 96 involve PR topics; evolution cases have neighbor_topics field"
decision: "保持 Provisional - MPR-02 🔒 LOCKED"
decision_reason: "insufficient evidence from current export scope (not data-baseline issue); need PR-targeted extraction"
next_package: "MPR-01C: PR-targeted candidate extraction (真正的 PR-specific surfacing)"
source_detail: "docs/plans/evolution-ops/11-math-pr-case-surfacing-package.md"
```

---

### Package MPR-01C: PR-Targeted Candidate Extraction **[COMPLETED - 2026-03-20]**

**STATUS: ✅ 已完成 — MPR-02 已解锁**

**决策: Option A — UNLOCK MPR-02**

关键发现:
- 从 main topic_graph.json (`data/output/topic_graph.json`) 找到 3 条 PR-internal evolves_from 边
- 4 个 strong positive candidate pairs (3 object continuity + 1 method continuity)
- 3 个 clear negative pairs
- 1 个 ambiguous pair
- 候选词汇明确非泛词（eigenvalues, matrices, percolation, martingale, rough paths）

evidence_summary:
  explicit_evolves_from_source: "MAIN data/output/topic_graph.json (NOT targeted export — targeted export has adjacent_to only)"
  evolves_from_pairs:
    - "global_38 -> global_100 (random limits -> random matrix ensemble): evolves_from main graph + adjacency bw=0.35"
    - "global_38 -> global_156 (random limits -> random matrix eigenvalue): evolves_from main graph + adjacency bw=0.4077"
    - "global_38 -> global_99 (random limits -> random walk/branching): evolves_from main graph (no adjacency; bw=0.475 was incorrect attribution)"
  method_continuity:
    - "global_65 -> global_188 (SDE convergence -> rough McKean): adjacent bw=0.4795"

decision_reason: "3 evolves_from edges from main topic_graph.json + 1 strong adjacent method pair + 3 clear negatives + 1 ambiguous; vocabulary non-generic (eigenvalues, matrices, percolation, martingale)"

corrected_by: "MPR-01C-fix (2026-03-20) - source attribution and bw=0.475 error corrected; MPR-01C-final-fix (2026-03-20) - evolves_from direction semantics corrected: source=OLDER, target=NEWER; pairs P1/P2/P3 had source/target swapped in all prior versions, corrected to global_38->100/156/99"

参见: docs/plans/2026-03-20-math-pr-candidate-extraction.md

---

### Package MPR-02: Case Curation **[✅ COMPLETE — 2026-03-21]**

**STATUS: ✅ COMPLETE — case curation done, conditional readiness confirmed**

MPR-02 完成于 2026-03-21。候选池已固定，条件就绪状态已确认。

**Curated Positives:**
- Tier A (Priority Integration Candidates):
  - PR-P1: global_38 → global_100 (two-source: evolves_from 0.39 + adjacency 0.35)
  - PR-P2: global_38 → global_156 (two-source: evolves_from 0.4077 + adjacency 0.4077)
- Tier B (Conditional — require paper-level review):
  - PR-P3: global_38 → global_99 (single-source: evolves_from 0.39 only)
  - PR-P4: global_65 → global_188 (adjacency-only: bw=0.4795)

All positives: strong inferred curated cases, NOT benchmark-confirmed. Paper-level review required before promotion.

**Curated Negatives:** PR-N1 (global_211), PR-N2 (global_47), PR-N3 (global_61), PR-N4 (global_214), PR-N5 (global_333)
**Ambiguous Cases:** PR-A1 (global_65↔global_39), PR-A2 (global_271↔global_99)

**Graph integration readiness:** CONDITIONAL
**Next package:** PR Phase 2C — conditional graph integration planning

**Reference:** `docs/plans/2026-03-21-math-pr-case-curation.md`

PR-TrackB-03 (2026-03-26): P4 demoted. R2 resolved negative. Gate 2 path: P1/P2/P3 (global_38-family) require their own TrackB cluster review.

PR-TrackB-04 (2026-03-27): global_38-family reviewed. P3 demoted. P1/P2 provisionally retained. Gate 2 partially viable; pending Level 3 abstract+citation review (PR-TrackB-05).

PR-TrackB-05 (2026-03-28): global_100/global_156 NOT RELIABLY DISTINCT (5/5 identical representative papers). P1/P2 collapse to single candidate. P1/P2 CONDITIONALLY DEMOTED. Gate 2: SINGLE-CANDIDATE HEIGHTENED CONCERN. Next: PR-TrackB-06 (abstract+citation level).

**PR-TrackB-06 (2026-03-29) COMPLETE:** Gate 2 COLLAPSED. All candidates demoted. math.PR at long-term Gate 1. Backlog item: monitor global_38→global_198 (genuine content heir, Jaccard ~0.4+) for future directional signal; initiate TrackB-07 only if global_198 develops Gate 2 qualifying evidence.

```yaml
tree_path: "math > math.PR"
task_owner: "case-worker"
task_type: "case_curation"
status: "✅ COMPLETE (2026-03-21)"
completion_date: "2026-03-21"
curated_positives: 4
  tier_a: [PR-P1, PR-P2]
  tier_b: [PR-P3, PR-P4]
curated_negatives: 5
ambiguous_cases: 2
graph_integration_readiness: "CONDITIONAL"
next_package: "PR Phase 2C — conditional graph integration planning"
```

### PR-2C: Phase 2C Conditional Integration Planning **[✅ PLANNING COMPLETE — 2026-03-22]**

**STATUS: ✅ PLANNING COMPLETE (2026-03-22)**
**Next: PR-2C-impl (conditional layer implementation)**

```yaml
tree_path: "math > math.PR > conditional graph integration"
task_owner: "docs-agent"
task_type: "integration_planning"
status: "✅ PLANNING COMPLETE"
completion_date: "2026-03-22"
```

Summary:
- Planning complete across all 5 layers: schema, export, bundle, frontend, integration gates
- Integration gate system defined (Gate 0 → Gate 1 → Gate 2)
- Current math.PR position: Gate 1 (Conditional Integration Implemented, PR-2C-impl 2026-03-23); Gate 2 COLLAPSED (PR-TrackB-06, 2026-03-29); long-term Gate 1
- Option C recommended: begin conditional implementation (Track A), paper review runs in parallel (Track B)
- LO+AG baseline NOT affected — `data/output/kg_v1/` is untouched
- 7 schema changes (all nullable/additive), 4 export changes, 3 bundle changes, 5 frontend additions
- Gate 2 requires paper review (R1/R2/R3 resolved) + MPR-03 benchmark runner — NOT part of PR-2C-impl

Reference: `docs/plans/2026-03-22-math-pr-phase-2c-integration-plan.md`

---

### Package MPR-03: Runner Implementation **[DORMANT — Gate 2 COLLAPSED; future contingency only]**

**STATUS: ⏸️ 待定 - 等待 MPR-02 完成**

```yaml
tree_path: "math > math.PR"
task_owner: "rule-worker"
task_type: "benchmark_runner_implementation"
target_rule: "math_pr_object_continuity"
precondition: "MPR-02 必须完成 (cases curated)"
status: "⏸️ 待定"
goal: "实现 math.PR object_continuity 的可执行 benchmark runner"
allowed_files:
  - "pipeline/math_pr_benchmark.py"
  - "tests/test_math_pr_benchmark.py"
  - "Makefile"
required_commands:
  - "pytest tests/test_math_pr_benchmark.py -q"
  - "make math-pr-benchmark"
done_when:
  - "runner 可生成 json + md"
  - "测试通过"
  - "cases 全绿"
```

---

### Package MRA-01B: Longer-Window Exploration **[PENDING]**

**STATUS: ⏸️ 待定 - 需要更长数据窗口**

```yaml
tree_path: "math > math.RA"
task_owner: "case-worker"
task_type: "data_exploration"
target_rule: "math_ra_object_continuity"
precondition: "必须获得更长周期的 math.RA 数据 (建议 >= 24 个月)"
goal: "在更长数据窗口中搜索 math.RA 的 evolution cases"
search_criteria:
  - "寻找 >=2 个 math.RA topics 之间有 temporal evolution 关系"
  - "关键词应包含: ring, rings, algebra, algebras, module, modules, ideal, ideals"
  - "避免只靠泛词 (algebra, module, theory) 区分"
  - "需要有清晰的 anchor -> target 跨期演化证据"
  - "需要 topics 有 >=2 个 active periods 才能构成 temporal 关联"
stop_conditions:
  - "搜索后仍无足够 topics (>=4)"
  - "topics 之间无 temporal 关联"
  - "无法区分 object continuity vs method continuity"
decision_fork:
  option_a:
    condition: "找到 >=2 个真实 event-level positive cases"
    action: "进入 MRA-02: benchmark skeleton bootstrap"
  option_b:
    condition: "数据仍然不足"
    action: "保持 gap 状态，等待未来数据"
```

## Dispatch Rules

分发时默认遵循：

1. 文档一致性问题先交 `doc-worker`
2. case 缺失问题先交 `case-worker`
3. 只有当 case 边界清楚时，才交 `rule-worker`

## Recommended Near-Term Order

### 已完成 ✅

1. `MLO-01` - Registry 状态一致性校正
2. `MAG-01` - Synthetic 标注清理
3. `MLO-03` - Set theory negative case 补充
4. `MLO-02` - Type theory bridge-level 确认
5. `MAG-02` - Object continuity negative case 补充
6. `MAG-03A` - Method continuity case discovery **[已归档]**
   - 决策: 选择 Option B (case 不足)
   - 结果: 进入 `MAG-03B-normalization`，已完成
7. `MAG-03B-normalization` - Scope cleanup **[已完成]**
   - method_continuity 明确为 test-evidence-only
   - math.AG benchmark 6/6 全绿
8. `MRA-01` - Bootstrap with decision fork **[已完成 - 2026-03-18]**
   - 决策: 选择 Option B (case 不足)
   - 结果: math.RA 明确为 gap / insufficient data
   - 当前状态: 3 topics, 全部仅 1 个 period, 0 evolution cases

### 新增完成 ✅ (2026-03-18)

9. `MMATH-01` - Math Data Audit (PKG-MATH-AUDIT-01) **[已完成]**
   - 产出: docs/plans/2026-03-18-math-data-audit.md
   - 关键发现: 374 math topics, 78% single-period

10. `MMATH-02` - Anchor Selection Audit (PKG-MATH-AUDIT-02) **[已完成]**
    - 产出: docs/plans/2026-03-18-math-anchor-audit.md
    - 关键发现: 60 multi-period math topics pass all filters

11. `MMATH-03` - Export Review (PKG-MATH-EXPORT-REVIEW-01) **[已完成 - 2026-03-18]**
    - 产出: docs/plans/2026-03-18-math-export-review.md
    - 关键发现: 9x visibility compression (1 vs 9 math cases)
    - 推荐: PKG-MATH-FOCUSED-EXPORT-01

12. `MPR-01` - Math.PR Bootstrap with Decision Fork **[已完成]**
    - 产出: docs/plans/2026-03-18-math-pr-benchmark.md
    - 关键发现: 12 multi-period PR topics, 6 candidate anchors
    - 决策: **Provisional Skeleton Candidate**
    - 强证据:
      - 12 个 multi-period topics
      - 6 个 candidate anchors 满足 papers/periods/neighbors 条件
    - 待显式验证:
      - positive pairs
      - negative/ambiguous cases
      - inferred evolution chains
    - 下一步: 先执行 `MPR-01B` (PR-specific case surfacing)

### 当前状态 — ⚠️ HISTORICAL (superseded by PR-2C)

> **Note**: This section reflects the state after MPR-01A / PKG-PR-01 completion.
> MPR-01B, MPR-02, and PR-2C have since been completed.
> For current status, see the **math.PR Phase 2C** section above and `03-task-packages.md`.
> **当前 next step: PR-2C-impl** — see PR-2C section.

**math.PR bootstrap 初评已完成**

审计链路: PKG-MATH-AUDIT-01 → PKG-MATH-AUDIT-02 → PKG-MATH-EXPORT-REVIEW-01 → PKG-PR-01

- ✅ 12 multi-period PR topics 具备 temporal evolution 证据
- ✅ 6 topics 满足 anchor 条件 (papers >= 60, periods >= 2, neighbors >= 2)
- ✅ 与 ST/OC/AP 存在可分析边界
- ⚠️ 当前仅为 **provisional skeleton candidate**
- ⚠️ 仍需 `MPR-01B` 显式 surfacing PR-specific cases

~~**下一步推荐**: MPR-01B (PR-specific case surfacing) → MPR-02 (conditional case curation)~~
*(completed — see PR-2C planning doc)*

---

## Math Knowledge Graph Task Package

### Package MKG-01: Math Historical Topic Evolution Knowledge Graph **[RECOMMENDED NEXT]**

**STATUS: 🟢 推荐下一步 - 先做 schema / bootstrap 设计**

```yaml
tree_path: "math knowledge graph"
task_owner: "doc-worker"
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
goal_v1_scope:
  in_scope:
    - "math.LO"
    - "math.AG"
    - "math.PR (provisional)"
  out_of_scope:
    - "math.QA"
    - "math.RA"
    - "math.RT"
    - "full frontend visualization"
design_questions:
  - "哪些 node types 需要进入 v1?"
  - "哪些 edge types 来自 raw graph?"
  - "哪些 edge types 来自 benchmark / case evidence?"
  - "如何编码 confirmed / inferred / ambiguous / unavailable?"
  - "math.PR 的 provisional 状态如何进图?"
done_when:
  - "新建 math knowledge graph 设计文档"
  - "node / edge / evidence schema 被明确写出"
  - "v1 覆盖范围限制在 LO + AG + PR(provisional)"
  - "给出下一步是 graph export implementation 还是先继续 PR-targeted extraction"
stop_if:
  - "需要修改 pipeline、tests 或 Makefile"
  - "需要直接实现前端可视化才能完成"
  - "需要把所有数学子域都纳入第一版"
next_after_design:
  option_a: "KG-02 graph export implementation"
  option_b: "MPR-01C PR-targeted candidate extraction"
source_detail: "docs/plans/evolution-ops/12-math-knowledge-graph-package.md"
```

**math 数据审计链路已完成**

审计链路: PKG-MATH-AUDIT-01 → PKG-MATH-AUDIT-02 → PKG-MATH-EXPORT-REVIEW-01

最终结论:
- ✅ Math 有 60 个 eligible anchors (足够 bootstrap)
- ✅ 12-case export 压缩到 1 个可见案例 (9x 压缩)
- ✅ 100-case audit 显示 9 个 math cases
- ✅ 下一步: 创建 math-focused export (推荐 Option A)

math_ag_method_continuity 最终状态：
- ✅ Threshold 验证通过
- ❌ **无 event-level cases** (只有 bridge-level)
- ✅ **决策**: 明确为 test-evidence-only，不进入 benchmark runner

决策结果：
1. `MAG-03A` case discovery 完成
2. 确认无法找到 event-level cases，选择 Option B
3. `MAG-03B-normalization` 已完成，文档已更新
4. math.AG benchmark 稳定: **6/6 全绿**

## Stop Conditions

以下情况不得继续扩展任务包：

- 同一路径下 registry / review / benchmark 彼此矛盾
- 只有 synthetic case，没有真实 case
- benchmark 绿色但无法解释为什么是正例
- 规则边界和相邻规则明显重叠

## Completion Rule

每个 task package 完成时，都必须留下：

- 任务块
- 改动文件列表
- Claude review 结论
- 本地 git commit hash
