# Evolution Rule Coverage Matrix

## 目的

这份文档用于维护 `trend-monitor` 历史演化分析器中“自然演化规则”的适配状态。

从现在开始，这张表 **强制复用项目已有的层次化主题树视角**。

维护单位不再只是 `Layer 1` / `Layer 2`，而是完整的 **`tree_path`**：

- `Layer 1`：固定学科
- `Layer 2`：固定 arXiv 子类
- `Layer 3+`：动态主题树节点

也就是说，后续规则登记的首选主键应为：

- `tree_path`
- 或者某个明确的路径前缀

例如：

- `cs`
- `cs > cs.CV`
- `math > math.AG`
- `math > math.AG > 代数簇与模空间`
- `hep > hep-th > 量子场论与弦论`

这样做的原因很直接：

1. 规则开发应该沿现有树结构逐步下钻，而不是按零散案例漂移。
2. 同一个 `Layer 2` 下，不同动态主题分支也可能有不同演化规律。
3. 增量更新后，规则可以继续挂在相同路径或路径前缀上，而不是重新命名领域。

## 维护约定

- 每次新增或明显修改演化解释规则后，都要更新这张表。
- 新规则必须优先登记到某个 `tree_path` 或路径前缀。
- 如果当前只确认到上层范围，可以先挂到 `Layer 1` / `Layer 2` 路径前缀。
- 如果已经明确适用于某个动态分支，应直接写完整路径，而不是只写泛领域名。
- 如果规则只是少量案例验证，状态必须写 `partial`。
- 如果某个 `Layer 1` / `Layer 2` 还没有规则，不要留空，明确写 `gap`。
- 新增规则时，必须先按下方“规则登记模板”登记，再更新主表。
- 新增关系后，必须挑选代表性案例做一次 Claude 评估，并把结论写回开发记录或汇总说明。
- 如果在 Claude 环境中执行，优先使用 subagent 完成评估；只有在当前环境支持 CLI 自调用时才使用 `claude -p`。
- 每次完成规则写入后，必须创建一次本地 git commit，即使不推送到远程仓库。
- 对于纯理论领域，优先补 `math` / `hep` / `math-ph` 等路径，再扩展到应用或交叉路径。

## 规则登记模板

每次新增规则时，先按这个模板补一条记录，再决定要不要把它提升到主表。

```yaml
rule_name: ""
tree_path: ""
path_scope: "exact | prefix"
status: "ready | partial | gap"
rule_type: "general | domain_specific"
trigger_sketch:
  - ""
positive_examples:
  - ""
counter_examples:
  - ""
implemented_in:
  - "pipeline/evolution_analysis.py"
notes:
  - ""
claude_evaluation:
  required: true
  representative_cases:
    - ""
  conclusion: ""
```

字段说明：

- `rule_name`
  - 规则内部名称，例如 `formal_structure_same_lineage`
- `tree_path`
  - 规则挂载的主题树路径或路径前缀
- `path_scope`
  - `exact` 表示只适用于当前路径
  - `prefix` 表示适用于当前路径及其后代分支
- `status`
  - 当前成熟度
- `rule_type`
  - 通用规则还是领域特化规则
- `trigger_sketch`
  - 最小触发逻辑，不写实现细节
- `positive_examples`
  - 当前支持这条规则的案例
- `counter_examples`
  - 容易误判或尚未解决的反例
- `implemented_in`
  - 代码落点
- `notes`
  - 任何需要提醒后续维护者的信息
- `claude_evaluation`
  - 新增关系后必须补
  - 至少包含代表案例和一句总结结论

## 已登记规则

```yaml
rule_name: "math_ag_object_continuity"
tree_path: "math > math.AG"
path_scope: "prefix"
status: "partial"
rule_type: "domain_specific"
trigger_sketch:
  - "anchor 与 target 都位于 math.AG 路径"
  - "共享至少 2 个 exact 代数几何对象词，如 varieties / curves / moduli / stacks / sheaves"
  - "taxonomy overlap 仅作为诊断证据，不单独提升 relation"
positive_examples:
  - "math > math.AG > 代数簇与模空间 邻域内的对象连续演化"
  - "global_69 (代数叠与层理论) -> global_287 (导出代数叠范畴): 共享 stacks/stack (2个对象词); current sole runner-positive"
  - "global_30 -> global_355 (ag-p2, bridge-level semantic positive; bridge ring case, not promoted by current exact-term gate or runner baseline)"
  - "global_355 -> global_117 (ag-p3, bridge-level semantic positive; bridge ring case, not promoted by current exact-term gate or runner baseline)"
counter_examples:
  - "仅共享一个泛词，如 projective，不应直接触发"
  - "global_69 (代数叠与层理论) -> global_136 (动机层与亨泽尔层): 仅共享 sheaves (1个对象词)，不满足 >=2 阈值"
  - "global_69 -> global_136 (ag-n1: domain mismatch, sheaves shared but stack vs. motivic/henselian domains differ)"
  - "global_30 (法诺簇模空间曲线) -> global_215 (霍奇商上同调猜想): 仅共享 hodge/rational/adic 等泛词，无共享对象词"
  - "global_107 (仿射代数群挠子) -> global_117 (志村簇与Theta积分): 虽都在代数几何领域，但无共享对象词 (torsors vs varieties)"
  - "global_134 (凸体与薄饼多面体) -> global_349 (热带几何与曲线热带化): 无共享对象词 (polytopes vs tropical curves)"
benchmark_cases:
  - case_id: "ag-p1"
    type: "positive"
    anchor: "global_69"
    target: "global_287"
    note: "代数叠与层理论 -> 导出代数叠范畴，保持 positive；shared exact objects >= 2；MAG-04 后为唯一 canonical runner-positive (legacy ag-b1/ag-e2 retired)"
  - case_id: "ag-n1"
    type: "negative"
    anchor: "global_69"
    target: "global_136"
    note: "仅共享 sheaves (1个对象词)；MAG-02 后应拒绝"
  - case_id: "ag-n2"
    type: "negative"
    anchor: "global_30"
    target: "global_287"
    note: "class-overlap-only false positive；MAG-02 后应拒绝"
  - case_id: "ag-p2"
    type: "bridge-level"
    anchor: "global_30"
    target: "global_355"
    note: "共享 curves (1 exact term)；作为 bridge ring 保留，不升级"
  - case_id: "ag-p3"
    type: "bridge-level"
    anchor: "global_355"
    target: "global_117"
    note: "共享 varieties (1 generic exact term)；作为 bridge ring 外圈保留，不升级"
  - case_id: "ag-n3"
    type: "negative"
    anchor: "global_134"
    target: "global_30"
    note: "domain boundary negative；作为 excluded boundary 继续保持拒绝"
implemented_in:
  - "pipeline/evolution_analysis.py"
notes:
  - "用于把对象层面的连续演化与一般形式结构连续性拆开"
  - "当前已加入对象 taxonomy 与层次权重，开始区分 exact overlap / same-class overlap / related-class overlap"
  - "2026-03-12: 基于当前数据集分析，仅发现 1 个正例对满足 >=2 共享对象词条件 (global_69 -> global_287)"
  - "当前 Math.AG 数据集中对象词覆盖率较低，大部分 topic 仅包含 8 个关键词，限制了正例数量"
  - "2026-03-21: Benchmark v2 at docs/plans/2026-03-18-math-ag-benchmark.md"
  - "2026-03-22 MAG-02: runtime gate tightened to >=2 exact shared AG object terms; taxonomy overlap remains diagnostic-only"
  - "2026-03-22 MAG-04: benchmark runner contract canonicalized to ag-p1 + ag-n1/ag-n2/ag-n3; legacy ag-b1/ag-e2 removed from active runner IDs"
  - "2026-03-22 MAG-FILL-01: graph/export narrative fixed as confirmed core (ag-p1) + bridge ring (ag-p2/ag-p3) + excluded boundary (ag-n1/ag-n2/ag-n3); runner contract unchanged"
claude_evaluation:
  required: true
  representative_cases:
    - "global_30-2025-02"
    - "global_69 -> global_287 (ag-p1, positive)"
    - "global_69 -> global_136 (ag-n1, negative - 仅1个共享对象词)"
    - "global_30 -> global_355 (ag-p2, positive bridge-level - curves shared)"
  conclusion: "2026-03-22 MAG-FILL-01: object continuity gate, review baseline, runner contract, and graph narrative are aligned. ag-p1 is the sole runner-positive event-level case; ag-p2/ag-p3 are fixed as bridge-ring semantic positives outside the exact-term gate; ag-n1/ag-n2/ag-n3 form the excluded boundary; ag-b1/ag-e2 are retired legacy aliases."
```

```yaml
rule_name: "math_ag_method_continuity"
tree_path: "math > math.AG"
path_scope: "prefix"
status: "partial"
rule_type: "domain_specific"
trigger_sketch:
  - "anchor 与 target 都位于 math.AG 路径"
  - "共享至少 2 个方法词，如 cohomology / derived / motivic / tropical / étale"
positive_examples:
  - "cohomology + motivic: 母题上同调理论之间的方法连续性 (ag-method-b1)"
  - "tropical + tropicalization: 热带几何方法链路 (ag-method-b2)"
  - "derived + categories: 导出范畴方法链路 (ag-method-b3)"
counter_examples:
  - "仅共享 1 个方法词 (如仅 cohomology) 不应触发 (ag-method-n1)"
  - "仅共享 1 个方法词 (如仅 categories) 不应触发 (ag-method-n2)"
  - "对象连续性更强时，不应误标成 method continuity"
notes:
  - "用于把 math.AG 中的方法迁移和对象迁移分开建模"
  - "⚠️ TEST EVIDENCE ONLY / NOT BENCHMARK-READY"
  - "原因: 虽有2个真实bridge-level cases，但无event-level cases"
  - "现状: cases时间跨度太短(2025-06->2025-10, 2025-09->2025-10)，不足以构成evolution事件"
  - "决策: 维持test-evidence-only状态，不进入benchmark runner"
  - "未来: 只有当找到event-level cases后才考虑benchmark化"
claude_evaluation:
  required: true
  representative_cases:
    - "global_30-2025-02 (synthetic validation only)"
    - "ag-method-p1: global_136 -> global_263 (positive, bridge-level)"
    - "ag-method-p2: global_237 -> global_263 (positive, bridge-level)"
    - "ag-method-n1: global_215 -> global_237 (negative, only 1 method word)"
  conclusion: "math_ag_object/method_continuity 拆分方向合理。2026-03-17重要更新: ⚠️ 将method_continuity明确降级为TEST EVIDENCE ONLY。原因: 找到的cases(ag-method-p1/p2)均为bridge-level，时间跨度不足(仅1-4个月)，无法构成event-level evolution。这些cases验证阈值有效性，但不足以支持benchmark runner。决策: method_continuity维持test-evidence-only状态，不进入math_ag_benchmark.py主流程。只有当未来找到event-level cases(跨期明显evolution信号)后才考虑重新评估。"
```

```yaml
rule_name: "math_lo_formal_system_continuity"
tree_path: "math > math.LO"
path_scope: "prefix"
status: "partial"
rule_type: "domain_specific"
trigger_sketch:
  - "anchor 与 target 都位于 math.LO 路径"
  - "共享至少 2 个核心形式对象，如 modal / automata / model / satisfiability / semantics"
  - "且至少共享 1 个方法词，如 intuitionistic / definable / sequent / computable"
positive_examples:
  - "模态逻辑、模型论、类型论、集合论之间的形式系统连续演化 (test_build_bridge_evidence_accepts_math_lo_formal_system_continuity)"
counter_examples:
  - "仅因通用词如 theory / sets 命中而误判"
  - "共享 core objects < 2 或 methods < 1"
benchmark_cases:
  - case_id: "test_formal_system_fallback"
    type: "positive"
    note: "验证规则作为 fallback 正确触发，当满足 core>=2 + method>=1 但不满足更具体子规则时"
    status: "pass"
    test_ref: "test_build_bridge_evidence_accepts_math_lo_formal_system_continuity"
implemented_in:
  - "pipeline/evolution_analysis.py"
  - "tests/test_evolution_analysis.py"
notes:
  - "第一版规则，先覆盖逻辑、模型论、集合论、类型论等结构对象"
  - "已根据 Claude 反馈收紧阈值，避免仅靠 logic / semantics 这类宽泛词误判"
  - "当前作为 fallback 规则，已被 modal/set/forcing/type/definability 子规则细分覆盖"
  - "验证方式：单元测试 test_build_bridge_evidence_accepts_math_lo_formal_system_continuity"
claude_evaluation:
  required: true
  representative_cases:
    - "test_build_bridge_evidence_accepts_math_lo_formal_system_continuity (synthetic)"
  conclusion: "math_lo_formal_system_continuity 作为 fallback 规则，以 '>=2 个核心对象 + >=1 个方法' 为阈值。单元测试验证通过。子规则细分后，此规则主要作为兜底使用。"
```

```yaml
rule_name: "math_lo_modal_continuity"
tree_path: "math > math.LO > 数理逻辑 > 模态逻辑 / 非经典逻辑"
path_scope: "prefix"
status: "partial"
rule_type: "domain_specific"
trigger_sketch:
  - "anchor 与 target 都位于 math.LO 的模态逻辑 / 非经典逻辑 / 直觉主义逻辑 / 概率逻辑路径"
  - "共享至少 2 个 modal object，如 modal / logic / semantics / proof / satisfiability / calculus"
  - "且至少共享 1 个 modal method，如 intuitionistic / probabilistic / sequent / hoare / smt"
positive_examples:
  - "直觉主义逻辑 -> 概率逻辑"
  - "模态逻辑 -> 非经典逻辑"
counter_examples:
  - "集合论 / 力迫法 / 大基数等形式对象，不应被 modal 规则误伤"
benchmark_cases:
  - case_id: "lo-b1"
    type: "positive"
    anchor: "global_56"
    target: "global_27"
    level: "event-level"
    status: "pass"
implemented_in:
  - "pipeline/evolution_analysis.py"
notes:
  - "作为 math.LO 的第一条子域规则，优先覆盖 modal / non-classical logic 这条更稳定的连续性支路"
  - "当前真实正例集中在 global_56 与 global_27 附近；若只共享 modal 词而没有方法词，不触发该关系"
  - "当前自动选出的 12 个主案例尚未覆盖到这条规则，现阶段主要依赖手动 replay 做局部验证"
  - "当前是 math.LO 中唯一具备 event-level 证据的子规则：`global_56 <-> global_27` 同时具备词典级桥接、图邻接（0.4025）和 multi-period 支撑（两者 active_periods=3）"
  - "在后续 benchmark / demo 叙事中，它应作为 event-level baseline，而不是与 bridge-level 规则并排处理"
claude_evaluation:
  required: true
  representative_cases:
    - "global_56-2025-03"
    - "global_51-2025-03"
  conclusion: "规则值得保留；`global_56-2025-03` 作为直觉主义逻辑向概率逻辑/自动机语义的 theory spillover 正例可信。MLO-03 收紧口径后，应把它明确视为 math.LO 当前唯一成熟的 event-level baseline：词典级桥接已被 `global_56 <-> global_27` 的图邻接（0.4025）、multi-period 支撑和 replay 命中共同加固。当前阈值应继续保持“shared_math_lo_core_objects >= 2 且 shared_math_lo_modal_methods >= 1”的必要条件。"
```

```yaml
rule_name: "math_lo_set_theory_continuity"
tree_path: "math > math.LO > 集合论与基数理论"
path_scope: "prefix"
status: "partial"
rule_type: "domain_specific"
trigger_sketch:
  - "anchor 与 target 都位于 math.LO 的集合论与基数理论 / 力迫法路径"
  - "共享至少 3 个 set object，如 cardinal / cardinals / forcing / axiom / ultrafilter / zf / choice"
  - "或者共享至少 2 个 set object 且共享至少 1 个 set method，如 definable / iterable / constructive / realizability"
positive_examples:
  - "基数与超滤子公理 -> ZF基数选择公理"
  - "基数与波莱尔公理 -> 基数迭代强制法"
counter_examples:
  - "只共享 cardinal + forcing 的弱重叠"
  - "只共享 cardinals + definable 的可定义性弱联系"
benchmark_cases:
  - case_id: "lo-b3"
    type: "positive"
    anchor: "global_313"
    target: "global_360"
    level: "bridge-level"
    status: "pass"
  - case_id: "lo-a2"
    type: "ambiguous"
    anchor: "global_339"
    target: "global_51"
    status: "review-needed"
implemented_in:
  - "pipeline/evolution_analysis.py"
notes:
  - "这条规则偏对象连续性，不像 modal/non-classical logic 那样依赖方法词"
  - "当前在 math.LO bridge-level ring 中更适合承担 inner backbone，而不是 forcing 的宽松上位替代"
  - "`global_313 -> global_360` 同时具备 adjacent_to（0.4235）和 evolves_from（0.4435），是 ring 内部图结构最完整的正例"
  - "`global_51 -> global_75` 的意义主要是边界校准：带有 forcing 词的 case 仍可能更适合留在 set-theory backbone"
  - "自动 replay 主事件还未稳定覆盖到这条规则，且主正例多为 single-period topic，因此仍保持 partial / bridge-level"
claude_evaluation:
  required: true
  representative_cases:
    - "global_313 -> global_360 (lo-b3, positive)"
    - "global_51 -> global_75 (supporting boundary positive)"
    - "global_339 -> global_51 (lo-a2, near-miss / ambiguous)"
    - "global_167 -> global_75 (negative)"
  conclusion: "规则值得保留，并应明确承担 math.LO bridge-level ring 的 inner backbone。`global_313 -> global_360` 提供当前最完整的内部图结构正例（adjacent_to 0.4235 + evolves_from 0.4435）；`global_51 -> global_75` 则说明 shared forcing vocabulary 的 case 仍可能更适合留在 set-theory backbone。`global_339 -> global_51` / `global_167 -> global_75` 保持了边界。由于这些正例尚无 replay event-level 命中，且主要 topic 多为 single-period，当前应继续维持 bridge-level / partial。"
```

```yaml
rule_name: "math_lo_forcing_continuity"
tree_path: "math > math.LO > 集合论与基数理论 > 力迫法"
path_scope: "prefix"
status: "partial"
rule_type: "domain_specific"
trigger_sketch:
  - "anchor 与 target 位于力迫法 / 大基数与力迫法 / 集合论与数理逻辑相关路径，允许 math.LO 与 cs.LO 跨顶层触发"
  - "shared_math_lo_forcing_objects 必须包含 axiom"
  - "且共享至少 4 个 forcing object，或共享至少 3 个 forcing object 并共享至少 1 个 forcing method"
positive_examples:
  - "基数与波莱尔公理 -> 基数与力迫法 (global_51 -> global_951)"
counter_examples:
  - "基数迭代强制法 -> 基数与力迫法 (global_75 -> global_951)"
  - "基数、理想与力迫法 -> 基数与力迫法 (global_339 -> global_951)"
benchmark_cases:
  - case_id: "lo-b4"
    type: "positive"
    anchor: "global_51"
    target: "global_951"
    level: "bridge-level"
    status: "pass"
  - case_id: "lo-n1"
    type: "negative"
    anchor: "global_51"
    target: "global_75"
    status: "pass"
  - case_id: "lo-n2"
    type: "negative"
    anchor: "global_339"
    target: "global_951"
    status: "pass"
  - case_id: "lo-a1"
    type: "ambiguous"
    anchor: "global_75"
    target: "global_951"
    status: "review-needed"
implemented_in:
  - "pipeline/evolution_analysis.py"
notes:
  - "这条规则的目标是识别 forcing / large-cardinal 逻辑族在 math.LO 与 cs.LO 之间的跨路径连续性"
  - "当前在 math.LO bridge-level ring 中更适合承担 outer cross-path branch，而不是集合论主干"
  - "`global_51 -> global_951` 的语义桥接成立，但该 pair 本身无 direct adjacent_to / evolves_from；它值得保留，是因为 target `global_951` 嵌在 `global_360` / `global_778` / `global_1155` 的邻接小簇里"
  - "`lo-n1` / `lo-a1` / `lo-n2` 的组合负责把 forcing 外支与 set-theory backbone 及泛 cardinal+forcing near-miss 分开"
  - "当前为 bridge-level 解释层，尚未进入 event-level 主案例筛选层"
claude_evaluation:
  required: true
  representative_cases:
    - "global_51 -> global_951 (lo-b4, positive)"
    - "global_51 -> global_75 (lo-n1, negative boundary for forcing / supporting boundary positive for set-theory backbone)"
    - "global_339 -> global_951 (lo-n2, negative)"
    - "global_75 -> global_951 (lo-a1, ambiguous / near-miss)"
  conclusion: "规则值得保留，并应明确承担 math.LO bridge-level ring 的 outer cross-path branch。`global_51 -> global_951` 保留了从 math.LO 集合论簇通向 cs.LO 大基数/力迫法邻域的外环解释，但该 pair 本身无 direct adjacent_to/evolves_from，因此不能上升为 event-level。`lo-n1` / `lo-a1` / `lo-n2` 共同说明：forcing 词汇或 cluster proximity 本身都不足以过线，`axiom` gate 仍是必要边界。"
```

```yaml
rule_name: "math_lo_type_theory_continuity"
tree_path: "math > math.LO > 数理逻辑 > 直觉主义逻辑"
path_scope: "prefix"
status: "partial"
rule_type: "domain_specific"
trigger_sketch:
  - "anchor 位于 math.LO 的数理逻辑 / 非经典逻辑 / 直觉主义逻辑路径"
  - "target 位于 cs.LO 的逻辑与形式化方法 / 自动推理与证明路径"
  - "共享至少 2 个 type object，目前只保留 type / types / typed"
  - "anchor 侧还需出现 proof / calculus / intuitionistic 等 source term，target 侧需出现 program / languages / subtyping / correctness 等 target term"
positive_examples:
  - "直觉主义逻辑证明 -> 程序线性化与类型"
counter_examples:
  - "直觉主义逻辑证明 -> 大语言模型数学推理"
  - "程序线性化与类型 -> 大语言模型数学推理"
benchmark_cases:
  - case_id: "lo-b2"
    type: "positive"
    anchor: "global_56"
    target: "global_980"
    level: "bridge-level"
    status: "pass"
  - case_id: "lo-n5"
    type: "negative"
    anchor: "global_56"
    target: "global_438"
    status: "pass"
  - case_id: "lo-n6"
    type: "negative"
    anchor: "global_980"
    target: "global_438"
    status: "pass"
  - case_id: "lo-n7"
    type: "negative"
    anchor: "global_56"
    target: "global_977"
    status: "pass"
  - case_id: "lo-n8"
    type: "negative"
    anchor: "global_56"
    target: "global_1155"
    status: "pass"
implemented_in:
  - "pipeline/evolution_analysis.py"
notes:
  - "这条规则捕捉的是 proof/calculus 到 type/programming-logic 的跨路径连续性，而不是泛化的模型论规则"
  - "当前共享对象层已刻意收窄到 type / types / typed，proof / calculus / program 只作为 source/target 辅助证据"
  - "MLO-03 后应把它稳定描述为 bridge-level contrast case：词典级桥接成立，但图结构支持和 event-level readiness 都缺失"
  - "与 `math_lo_modal_continuity` 的差异不在于逻辑学重要性，而在于证据结构不同：modal 有图邻接 + multi-period + replay，type-theory 没有"
claude_evaluation:
  required: true
  representative_cases:
    - "global_56 -> global_980 (lo-b2, positive, bridge-level)"
    - "global_56 -> global_438 (lo-n5, negative)"
    - "global_980 -> global_438 (lo-n6, negative)"
    - "global_56 -> global_977 (lo-n7, negative near-miss — 图邻接 0.225，无 type object)"
    - "global_56 -> global_1155 (lo-n8, negative near-miss — 图邻接 0.2711，无 type object)"
  conclusion: "规则值得保留；`global_56 -> global_980` 体现 proof-to-type-system 词面桥接（Curry-Howard）。MLO-03 统一口径后，应明确按三层边界描述它：词典级桥接成立，但图结构支持缺失（无 adjacent_to/evolves_from，global_980 active_periods=1 且拓扑孤立），event-level readiness 也缺失（无 replay 命中）。`global_56` 的实际演化方向仍是 `global_27`（modal）。因此它应稳定停留在 bridge-level；lo-n7/lo-n8 作为更精准的近失负例（图邻接但无 type object），验证 type object 阈值是有效边界。"
```

```yaml
rule_name: "math_lo_definability_continuity"
tree_path: "math > math.LO > 集合论与基数理论"
path_scope: "prefix"
status: "partial"
rule_type: "domain_specific"
trigger_sketch:
  - "anchor 与 target 位于 math.LO / cs.LO 的集合论与基数理论 / 逻辑与形式化方法相关路径"
  - "必须共享 definable 这一方法词"
  - "共享对象里必须同时出现 cardinal/cardinals 与至少一个 special object，如 woodin / axiom / reals / uniformization"
positive_examples:
  - "基数迭代强制法 -> 武丁公理与可定义性 (global_75 -> global_778)"
counter_examples:
  - "可定义基数塔基序 -> 武丁公理与可定义性 (global_167 -> global_778)"
  - "亨泽尔域存在可定义性 -> 武丁公理与可定义性 (global_361 -> global_778)"
benchmark_cases:
  - case_id: "lo-b5"
    type: "positive"
    anchor: "global_75"
    target: "global_778"
    level: "bridge-level"
    status: "pass"
  - case_id: "lo-n3"
    type: "negative"
    anchor: "global_167"
    target: "global_778"
    status: "pass"
  - case_id: "lo-n4"
    type: "negative"
    anchor: "global_361"
    target: "global_778"
    status: "pass"
implemented_in:
  - "pipeline/evolution_analysis.py"
notes:
  - "这是比 model-theory 更窄的一条 definability 支路，只覆盖 set-theoretic definability 的跨路径连续性"
  - "当前在 math.LO bridge-level ring 中更适合承担 narrow capstone branch"
  - "`global_75 -> global_778` 有 adjacent_to（0.225），说明它不是纯词面拼接，而是从 forcing/cardinal 邻域向 `woodin + definable` 方向的窄支收束"
  - "`lo-n3` / `lo-n4` 说明 `definable` 不是自由通行证，仍要保留 `cardinal/cardinals + special object` 的组合要求"
  - "当前为 bridge-level 解释层，尚未进入 event-level 主案例筛选层"
claude_evaluation:
  required: true
  representative_cases:
    - "global_75 -> global_778 (lo-b5, positive)"
    - "global_167 -> global_778 (lo-n3, negative)"
    - "global_361 -> global_778 (lo-n4, negative)"
  conclusion: "规则值得保留，并应明确承担 math.LO bridge-level ring 的 narrow capstone。`global_75 -> global_778` 给出了当前最干净的 definability bridge-level 正例：有 direct adjacency（0.225），也保留了 `definable + cardinal/cardinals + special object` 的 set-theoretic 约束。`lo-n3` / `lo-n4` 说明 definable 单词本身或弱 cardinal overlap 都不足以触发，因此这条支路应继续保持窄而可解释。"
```

```yaml
rule_name: "math_ra_gap_insufficient_data"
tree_path: "math > math.RA"
path_scope: "exact"
status: "gap"
rule_type: "domain_specific"
assessment_date: "2026-03-18"
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
stop_conditions_met:
  - "找不到 >=2 个可信 object-side candidate positives"
  - "所有 topics 仅 1 个 active period，无法构成 temporal evolution"
  - "无法区分 object continuity vs method continuity"
decision: "Option B (Gap)"
next_step_if_continue: "PKG-RA-01B: longer-window exploration (requires >=24 months data)"
notes:
  - "math.RA 当前数据不足以支持 benchmark skeleton 建立"
  - "所有 3 个 topics 都只有 1 个 active period，无法形成跨期演化对"
  - "若未来获得 >=24 个月数据，可重新评估是否启动 MRA-01B"
  - "当前明确标记为 gap / insufficient data / not benchmark-ready"
```

```yaml
rule_name: "math_qa_gap_no_data"
tree_path: "math > math.QA"
path_scope: "exact"
status: "gap"
rule_type: "domain_specific"
assessment_date: "2026-03-21"
data_assessment:
  total_topics: 0
  hierarchy_present: false
  evolution_cases: 0
  temporal_pairs: 0
  graph_edges: 0
  notes: "math.QA hierarchy key entirely absent from aligned_topics_hierarchy.json"
stop_conditions_met:
  - "0 topics — no data substrate of any kind"
  - "hierarchy key missing — gap begins at topic modeling / ingestion layer"
  - "cannot form even a single temporal pair"
decision: "Gap — no data"
next_step_if_continue: "MQA-01A: gap normalization re-check (requires >=10 topics, >=3 multi-period)"
notes:
  - "math.QA 当前数据完全缺失，hierarchy key 不存在"
  - "不同于 math.RA（有 3 个 single-period topics），math.QA 连 topic 都没有"
  - "gap 起始于最早层：topic modeling / data ingestion，而非演化分析层"
  - "可能原因：数据摄取过滤、arXiv 分类稀疏、或当前采集窗口内 math.QA 论文极少"
  - "当前明确标记为 gap / no data / not benchmark-ready"
```

```yaml
rule_name: "math_rt_gap_insufficient_data"
tree_path: "math > math.RT"
path_scope: "exact"
status: "gap"
rule_type: "domain_specific"
assessment_date: "2026-03-22"
data_assessment:
  total_topics: 5
  multi_period_topics: 0
  internal_adjacent_edges: 4
  internal_evolves_from_edges: 1
  candidate_positive_watchlist:
    - "global_193 -> global_358: shared lusztig/hecke, adjacent_to=0.2778, but no evolves_from and no second corroborating positive"
  candidate_boundary_pairs:
    - "global_177 -> global_358: adjacent_to/evolves_from=0.2868, but only generic algebra overlap"
    - "global_36 -> global_193: adjacent_to=0.2368, but only shared sheaves"
    - "global_356 -> global_358: same-period pair (2026-02 -> 2026-02), not suitable as bootstrap backbone"
stop_conditions_met:
  - "0 multi-period topics; no within-topic temporal persistence"
  - "only 1 internal evolves_from edge, and it is supported only by generic algebra overlap"
  - "cannot fix 2 credible real positives without lowering standards to generic or same-period pairs"
decision: "Option B (Gap)"
next_step_if_continue: "Re-evaluate after longer window or improved alignment; require >=3 multi-period topics and >=2 credible internal positives"
notes:
  - "math.RT 当前不具备 benchmark skeleton ready 的最低证据"
  - "域内并非完全没边，但当前图只足够支持 gap 诊断，不足以固定 2 positive + 2 negative + 1 ambiguous 的真实案例集"
  - "唯一接近第一条窄方向的种子是 Lusztig / Hecke continuity，但今天还不能把它升格成 planned rule"
  - "当前明确标记为 gap / insufficient data / not benchmark-ready"
```

```yaml
rule_name: "math_co_bootstrap_case_curation"
tree_path: "math > math.CO"
path_scope: "exact"
status: "partial"
rule_type: "domain_specific"
assessment_date: "2026-03-22"
data_assessment:
  total_topics: 47
  multi_period_topics: 7
  internal_adjacent_edges: 138
  internal_evolves_from_edges: 38
  main_evolution_cases: 0
  hierarchy_depth_distribution:
    depth_1: 43
    depth_3: 1
    depth_4: 3
candidate_positive_families:
  - "random graph / percolation: global_63 -> global_308, global_130 -> global_187"
  - "matroid / polytope / poset: global_16 -> global_292, global_292 -> global_319"
candidate_failure_modes:
  - "generic graph vocabulary overlap (`graph/graphs/conjecture`) across unrelated branches"
  - "generic algebraic-combinatorial vocabulary overlap (`rank/polynomial`) without shared discrete object"
decision: "MCO-FILL-02 boundary preserved (first narrow rule implemented; supporting bridge kept outside gate)"
next_step_if_continue: "MCO-FILL-02 complete: keep current matroid-family gate unchanged and stabilize graph-facing layers as confirmed MVP + supporting bridge outside gate + excluded boundary"
notes:
  - "math.CO 已有足够真实案例启动第一版 benchmark skeleton"
  - "当前固定的 positives 都是 bridge-level；还没有 event-level baseline"
  - "当前最可能的方向是 discrete structure continuity，而不是 combinatorial method continuity"
  - "hierarchy 仍偏浅：43/47 topics 只挂在顶层 `math.CO研究`，因此不要过早把 path label 当成强证据"
  - "MCO-FILL-01 已把第一条窄规则落到代码；MCO-FILL-02 已确认 global_16 -> global_292 仍应停留在 supporting bridge outside gate"
```

```yaml
rule_name: "math_co_matroid_structure_continuity"
tree_path: "math > math.CO"
path_scope: "exact"
status: "partial"
rule_type: "domain_specific"
trigger_sketch:
  - "anchor 与 target 都位于 math.CO 路径"
  - "共享至少 1 个 matroid-family exact term，如 matroid / matroids / polymatroid"
  - "且共享至少 2 个离散结构 exact terms，如 matroid / matroids / poset / posets / polytope / polytopes / lattice / lattices"
  - "generic overlap (`rank`, `polynomial`, `graphs`) 只作背景，不单独提升 relation"
positive_examples:
  - "global_292 -> global_319 (co-m1, MVP positive): 共享 matroid / matroids / polytopes"
  - "global_118 -> global_204 (co-m2, supporting positive): 共享 matroid / matroids / posets"
  - "global_16 -> global_292 (supporting bridge outside gate；不并入当前 rule，因为它只有 `matroid` shared family，若要升级必须借用 target-only structure 或 `rank/polynomial` 背景词)"
counter_examples:
  - "global_292 -> global_324 (co-mn1): rank / polynomial overlap only，不应触发"
  - "global_8 -> global_319 (co-mn2): generic graph vocabulary mismatch，不应触发"
  - "global_220 -> global_292 (co-ma1): polytope-only near-miss；第一条规则必须拒绝"
benchmark_cases:
  - case_id: "co-m1"
    type: "positive"
    anchor: "global_292"
    target: "global_319"
    note: "拟阵停车模式多面体 -> 拟阵与多面体格；MCO-02 选定的 MVP positive"
  - case_id: "co-m2"
    type: "positive"
    anchor: "global_118"
    target: "global_204"
    note: "拟阵热带偏序集 -> 拟阵偏序集及提升；supporting positive"
  - case_id: "co-mn1"
    type: "negative"
    anchor: "global_292"
    target: "global_324"
    note: "rank/polynomial overlap only；matrix/permanental boundary negative"
  - case_id: "co-mn2"
    type: "negative"
    anchor: "global_8"
    target: "global_319"
    note: "generic graph vocabulary negative；不能误拉进拟阵支路"
  - case_id: "co-ma1"
    type: "ambiguous"
    anchor: "global_220"
    target: "global_292"
    note: "polytope-only near-miss；未来 broader rule 候选，但第一条 matroid rule 应拒绝"
notes:
  - "MCO-02 已把它选为 math.CO 的第一实现分支；MCO-FILL-01 已将保守 MVP 落地到代码"
  - "当前实现/contract 文档见 docs/plans/2026-04-01-math-co-first-rule-plan.md"
  - "random graph / percolation 暂缓，原因是 generic graph/process vocabulary overlap 误判风险更高"
  - "MCO-FILL-02 已单独复审 global_16 -> global_292：当前边界保持不变，graph-facing 口径固定为 confirmed MVP + supporting bridge outside gate + excluded boundary"
claude_evaluation:
  required: true
  representative_cases:
    - "global_292 -> global_319 (co-m1, positive)"
    - "global_292 -> global_324 (co-mn1, negative)"
    - "global_220 -> global_292 (co-ma1, near-miss)"
  conclusion: "2026-03-22 MCO-FILL-02: current MVP boundary should be preserved. co-m1/co-m2 remain the confirmed positives; co-mn1/co-mn2/co-ma1 remain the excluded boundary; global_16 -> global_292 is valuable bridge evidence but stays outside the current gate because absorbing it would require target-only structure or rank/polynomial background to become promotion signals."
```

```yaml
rule_name: "math_ds_bootstrap_case_curation"
tree_path: "math > math.DS"
path_scope: "exact"
status: "partial"
rule_type: "domain_specific"
assessment_date: "2026-03-22"
data_assessment:
  total_topics: 22
  multi_period_topics: 3
  internal_adjacent_edges: 49
  internal_evolves_from_edges: 12
  main_evolution_cases: 0
  hierarchy_depth_distribution:
    depth_2: 17
    depth_3: 3
    depth_4: 2
candidate_positive_families:
  - "ergodic / entropy: global_154 -> global_186, global_154 -> global_367"
  - "complex dynamics: global_234 -> global_266"
  - "hyperbolic systems: global_254 -> global_288"
candidate_failure_modes:
  - "generic topological vocabulary overlap (`topological`) across unrelated branches"
  - "generic measure / metric overlap (`measure`, `metric`) across transport vs ergodic themes"
  - "generic systems / maps overlap (`systems`, `maps`) across unrelated DS subfields"
decision: "MDS-FILL-02 complete (benchmark skeleton established and first conservative MVP landed)"
next_step_if_continue: "Preserve the current ergodic/entropy MVP boundary; only revisit if future work can broaden DS coverage without letting generic systems/maps/random vocabulary become promotion signals"
notes:
  - "math.DS 已有足够真实案例启动第一版 benchmark skeleton"
  - "当前固定的 positives 仍是 bridge-level；还没有 event-level baseline"
  - "当前最可能的第一条方向已收敛并落地为 `math_ds_ergodic_entropy_continuity`，而不是泛化 dynamical-system continuity"
  - "complex dynamics / hyperbolic systems 也有 clean positives，但各自暂时只有 1 对强正例，更适合留作第二阶段扩展支路"
```

```yaml
rule_name: "math_ds_ergodic_entropy_continuity"
tree_path: "math > math.DS"
path_scope: "exact"
status: "partial"
rule_type: "domain_specific"
trigger_sketch:
  - "anchor 与 target 都位于 math.DS 路径"
  - "共享 `entropy`，并且同时有 `ergodic` 或 `topological` 这类更窄 DS object/method 词"
  - "同时保留 `measure` / `measures` 作为 supporting evidence，而不是把 `systems` / `maps` 当作 promotion signal"
positive_examples:
  - "global_154 -> global_186 (ds-b1): entropy + ergodic + measures"
  - "global_154 -> global_367 (ds-b2): entropy + topological + measure"
counter_examples:
  - "global_119 -> global_367 (ds-n1): only `topological` overlap，不应触发"
  - "global_12 -> global_154 (ds-n2): `measure(s)` / `metric` overlap 不能把最优输运拉进遍历熵支路"
  - "global_49 -> global_154 (ds-a1): entropy/measure overlap 边界未定，应先保留 ambiguous"
benchmark_cases:
  - case_id: "ds-b1"
    type: "positive"
    anchor: "global_154"
    target: "global_186"
    note: "遍历动力系统定理 -> 遍历测度不等式；shared entropy/ergodic/measures/theorem；bridge-level positive"
  - case_id: "ds-b2"
    type: "positive"
    anchor: "global_154"
    target: "global_367"
    note: "遍历动力系统定理 -> 奥野贝西科维奇拓扑熵；shared entropy/measure/topological；bridge-level positive"
  - case_id: "ds-n1"
    type: "negative"
    anchor: "global_119"
    target: "global_367"
    note: "topological-only overlap；persistent homology 不能直接并入 topological entropy continuity"
  - case_id: "ds-n2"
    type: "negative"
    anchor: "global_12"
    target: "global_154"
    note: "measure/metric overlap only；transport vs ergodic boundary negative"
  - case_id: "ds-a1"
    type: "ambiguous"
    anchor: "global_49"
    target: "global_154"
    note: "fractal entropy / measure 与 ergodic entropy 的边界未定"
implemented_in:
  - "pipeline/evolution_analysis.py"
  - "tests/test_evolution_analysis.py"
notes:
  - "这是 math.DS 当前最可能的第一条窄方向，现已以 conservative MVP 代码落地"
  - "当前 runtime gate = shared `entropy` + shared `ergodic/topological`"
  - "`measure` / `measures` 仅作为 supporting evidence 输出，不单独升格 relation"
  - "当前最重要的是守住 `entropy` 线的边界，不要把 generic `systems` / `maps` / `random` 提前放进来"
  - "当前 positives 都仍是 bridge-level；尚无 runner baseline"
claude_evaluation:
  required: true
  representative_cases:
    - "global_154 -> global_186 (ds-b1, positive)"
    - "global_154 -> global_367 (ds-b2, positive)"
    - "global_119 -> global_367 (ds-n1, negative)"
    - "global_49 -> global_154 (ds-a1, ambiguous)"
  conclusion: "2026-03-22 MDS-FILL-02: local contract is now implemented as a conservative partial rule around shared entropy plus shared ergodic/topological terms. ds-b1/ds-b2 are admitted; ds-n1/ds-n2 remain rejected; ds-a1 remains an ambiguous boundary outside the current gate. Follow-up Claude review is still required before any broader promotion."
```

```yaml
rule_name: "math_na_bootstrap_case_curation"
tree_path: "math > math.NA"
path_scope: "exact"
status: "planned"
rule_type: "domain_specific"
assessment_date: "2026-03-22"
data_assessment:
  total_topics: 36
  multi_period_topics: 7
  internal_adjacent_edges: 86
  internal_evolves_from_edges: 18
  main_evolution_cases: 0
  hierarchy_depth_distribution:
    depth_2: 25
    depth_3: 1
    depth_4: 9
    depth_5: 1
candidate_positive_families:
  - "matrix / Krylov iterative: global_105 -> global_140, global_140 -> global_9"
  - "tensor / low-rank: global_13 -> global_149, global_149 -> global_264"
  - "inverse / regularization: global_124 -> global_255"
candidate_failure_modes:
  - "generic solver words (`convergence`, `approximation`, `matrix`) across unrelated NA branches"
  - "duplicate-topic risk signaled by 5/5 representative-title overlap in several attractive pairs (for example global_23 -> global_62, global_9 -> global_251/391, global_236 -> global_258)"
  - "shallow hierarchy makes exact method-family terms more reliable than path labels"
decision: "Option A (benchmark skeleton ready; follow-up conservative MVP now landed in MNA-FILL-02)"
next_step_if_continue: "Keep the na-b1/na-b2/na-n1/na-n2/na-a1 contract stable, monitor the gmres-only fallback, and do not widen to generic solver vocabulary before new positives exist"
notes:
  - "math.NA 已有足够真实案例启动第一版 benchmark skeleton"
  - "当前固定的 positives 仍是 bridge-level；还没有 event-level baseline"
  - "当前最可能的第一条方向更像 matrix / Krylov iterative continuity，而不是泛化 numerical-method continuity"
  - "PDE / Galerkin / polynomial 分支当前存在更明显的 duplicate-topic 风险，不适合作为第一条 rule contract"
  - "MNA-FILL-02 已将 follow-up conservative MVP 落地到 math_na_krylov_iterative_continuity"
```

```yaml
rule_name: "math_na_krylov_iterative_continuity"
tree_path: "math > math.NA"
path_scope: "exact"
status: "partial"
rule_type: "domain_specific"
trigger_sketch:
  - "anchor 与 target 都位于 math.NA 路径"
  - "promotion core 只认 `gmres` / `krylov` / `lanczos` / `arnoldi` 这 4 个 exact method-family terms"
  - "若 shared core terms >= 2，则允许命中"
  - "若只 shared `gmres`，仅当 target 暴露完整 `arnoldi + gmres + krylov + lanczos` 四词束时允许 fallback 命中"
  - "`matrix` / `block` / `numerical` / `convergence` / `approximation` 只作为 supporting evidence 或边界诊断，不单独升格 relation"
positive_examples:
  - "global_105 -> global_140 (na-b1): GMRES -> Krylov family broadening"
  - "global_140 -> global_9 (na-b2): Krylov / Lanczos / block matrix iterative chain"
counter_examples:
  - "global_105 -> global_378 (na-n1): only `approximation` overlap"
  - "global_140 -> global_90 (na-n2): only `convergence` overlap"
  - "global_86 -> global_307 (na-a1): `krylov` overlap with application shift; keep ambiguous for now"
benchmark_cases:
  - case_id: "na-b1"
    type: "positive"
    anchor: "global_105"
    target: "global_140"
    status: "pass"
    note: "GMRES数值近似法 -> 块特征值与Krylov方法；shared exact term `gmres`；依赖 target full four-term bundle fallback；bridge-level positive"
  - case_id: "na-b2"
    type: "positive"
    anchor: "global_140"
    target: "global_9"
    status: "pass"
    note: "块特征值与Krylov方法 -> 块矩阵迭代算法加速；shared core `gmres/krylov/lanczos`；`block/matrix` 仅 supporting；bridge-level positive"
  - case_id: "na-n1"
    type: "negative"
    anchor: "global_105"
    target: "global_378"
    status: "pass"
    note: "approximation-only overlap；kernel interpolation 不应并入 Krylov continuity"
  - case_id: "na-n2"
    type: "negative"
    anchor: "global_140"
    target: "global_90"
    status: "pass"
    note: "convergence-only overlap；Krylov eigenvalue methods vs MCMC boundary negative"
  - case_id: "na-a1"
    type: "ambiguous"
    anchor: "global_86"
    target: "global_307"
    status: "review-needed"
    note: "`krylov` overlap exists, but target shifts to quantum/tensor application side"
implemented_in:
  - "pipeline/evolution_analysis.py"
  - "tests/test_evolution_analysis.py"
notes:
  - "MNA-01 已确认 math.NA 足够启动第一版 benchmark skeleton"
  - "MNA-FILL-02 已将第一条 conservative MVP 代码落地"
  - "当前最值得先落的不是泛 `numerical-method continuity`，而是更窄的 matrix / Krylov iterative chain"
  - "当前所有 fixed positives 仍是 bridge-level；尚无 runner-ready event baseline"
  - "当前 runtime footprint 只命中 3 条 directed pair：global_105 -> global_140、global_140 -> global_9、global_9 -> global_140"
  - "单共享 `gmres` fallback 已刻意收窄到 target full four-term bundle，避免把 `global_105 -> global_9` 之类更宽的 chain 一起吸进第一轮 contract"
  - "多条 attractive pair 存在 5/5 representative-title overlap，第一条规则应暂避这些 duplicate-prone branches"
claude_evaluation:
  required: true
  representative_cases:
    - "global_105 -> global_140 (na-b1, positive)"
    - "global_140 -> global_9 (na-b2, positive)"
    - "global_105 -> global_378 (na-n1, negative)"
    - "global_140 -> global_90 (na-n2, negative)"
    - "global_86 -> global_307 (na-a1, ambiguous boundary)"
  conclusion: "2026-03-22 MNA-FILL-02: Claude review judges the gate to be a credible conservative MVP for math.NA. na-b1/na-b2 are accepted positives under the exact-term contract; na-n1/na-n2 remain correctly rejected because approximation/convergence do not promote; na-a1 stays outside the first positive set because single-word krylov overlap is too weak. Main residual risk: the gmres-only fallback may need an extra anchor-side guard later if survey-like targets start exposing the full four-term bundle."
```

## 状态定义

| 状态 | 含义 |
|------|------|
| `ready` | 已进入主流程，且当前有回放案例支持 |
| `partial` | 已实现，但只覆盖少量子场景或案例 |
| `planned` | 已完成 benchmark/review 与 implementation-ready 设计，但代码尚未落地 |
| `gap` | 当前尚无专门适配 |

## 通用骨架

这些规则不绑定具体学科层级，属于全局基础设施。

| Rule | Scope | Status | Implemented In | Notes |
|------|-------|--------|----------------|-------|
| topic temporal graph | 全领域 | `ready` | `pipeline/evolution_analysis.py` | 基础图状态层，包含 `belongs_to` / `active_in` / `adjacent_to` / `evolves_from` |
| event extraction | 全领域 | `ready` | `pipeline/evolution_analysis.py` | 提取 `emerged` / `expanded` / `diffused_to_neighbor` / `specialized_into_child` / `merged_into_parent` / `migrated_to_new_category` / `weakened` / `stabilized` |
| topic profile | 全领域 | `ready` | `pipeline/evolution_analysis.py` | `method` / `problem` / `hybrid` / `theory` 解释层 |
| bridge evidence | 全领域 | `ready` | `pipeline/evolution_analysis.py` | 输出 `shared_keywords` / `bridge_topics` / `target_evidence_titles` / `category_flow` / `pipeline_relation` / `bridge_strength` |
| alias risk | 全领域 | `partial` | `pipeline/evolution_analysis.py` | 当前主要覆盖中英文别名与高关键词重叠 |
| persistence checks | 全领域 | `ready` | `pipeline/evolution_analysis.py` | 包含 target / anchor / relative persistence |
| consistency check | 全领域 | `partial` | `pipeline/evolution_analysis.py` | 当前主要识别“高桥接但弱承接”的矛盾，需要更多 Layer 2 特化规则支持 |

## Tree Path Registry

这是后续维护的主登记表。`Layer 1` / `Layer 2` 只是它的上层前缀。

| Tree Path | Layer Span | Coverage | Status | Current Rule | Notes |
|-----------|------------|----------|--------|--------------|-------|
| `cs` | L1 | 中 | `partial` | 通用规则 | 当前只有部分分支开始特化 |
| `cs > cs.CV` | L1-L2 | 中 | `partial` | `representation_to_perception_same_pipeline` | 目前主要覆盖 3D 视觉方向 |
| `eess > eess.IV` | L1-L2 | 中 | `partial` | `imaging_to_analysis_same_pipeline` | 作为医学影像链路上游来源域 |
| `math` | L1 | 低到中 | `partial` | `formal_structure_same_lineage` | 仅代表“数学已纳入考虑”，不代表所有子域已适配 |
| `math > math.AG` | L1-L2 | 中 | `partial` | `math_ag_object_continuity`, `math_ag_method_continuity`, `formal_structure_same_lineage` | 当前数学里最先开始适配的分支 |
| `math > math.CO` | L1-L2 | 中 | `partial` | `math_co_matroid_structure_continuity` | 第一条窄规则已以保守 MVP 落地；graph-facing 口径固定为 confirmed MVP（`co-m1/co-m2`）+ supporting bridge outside gate（`global_16 -> global_292`）+ excluded boundary（`co-mn1/co-mn2/co-ma1`）；`random / percolation` 暂缓 |
| `math > math.DS` | L1-L2 | 中 | `partial` | `math_ds_ergodic_entropy_continuity` | `22` topics / `3` multi-period / `49` internal adjacent / `12` internal evolves；第一条 conservative MVP 已落地，gate 固定为 `entropy` + `ergodic/topological`，当前 positives 仍全是 bridge-level |
| `math > math.NA` | L1-L2 | 中 | `partial` | `math_na_krylov_iterative_continuity` | `36` topics / `7` multi-period / `86` internal adjacent / `18` internal evolves；第一条 conservative MVP 已落地，gate 固定为 exact `gmres/krylov/lanczos/arnoldi` core；`na-b1/na-b2` 命中，`na-n1/na-n2` 与 `na-a1` 保持门外，positives 仍 bridge-level only |
| `math > math.LO` | L1-L2 | 中 | `partial` | `math_lo_formal_system_continuity`, `math_lo_modal_continuity`, `math_lo_type_theory_continuity`, `math_lo_set_theory_continuity`, `math_lo_forcing_continuity`, `math_lo_definability_continuity` | 已从通用形式系统连续性下钻到 modal、type-theory、set theory、forcing、definability 五条子路径；当前口径应固定为“1 条 event-level baseline（modal）+ 1 个 bridge-level ring（type-theory contrast / set-theory backbone / forcing outer branch / definability capstone）” |
| `math > math.RT` | L1-L2 | 低 | `gap` | - | `5` topics / `0` multi-period / `4` internal adjacent / `1` internal evolves；唯一接近正例的是 `global_193 -> global_358`（Lusztig / Hecke），但不足以固定 `2P/2N/1A` skeleton |
| `math > math.RA` | L1-L2 | 低 | `gap` | - | 当前仅 3 topics，全部仅 1 个 period，0 evolution cases，数据不足 |
| `math > math.QA` | L1-L2 | 低 | `gap` | - | 当前 0 topics，hierarchy 完全缺失，无数据基础；需 >=10 topics 且 >=3 multi-period 才能重新评估 |
| `hep` | L1 | 中 | `partial` | `formal_structure_same_lineage` | 当前更多偏 `hep-th` |
| `hep > hep-th` | L1-L2 | 中 | `partial` | `formal_structure_same_lineage` | 规范理论 / 圈振幅 / 弦论邻域 |
| `stat` | L1 | 低 | `gap` | - | 尚无专门特化 |
| `econ` | L1 | 低 | `gap` | - | 尚无专门特化 |
| `q-bio` | L1 | 低 | `gap` | - | 尚无专门特化 |
| `astro-ph` | L1 | 低 | `gap` | - | 尚无专门特化 |

## Layer 1 Coverage

这是面向全局规划的压缩视图。实际登记以后以上面的 `Tree Path Registry` 为准。

| Layer 1 | Coverage | Current State | Layer 2 Focus | Notes |
|---------|----------|---------------|---------------|-------|
| `cs` | 中 | `partial` | `cs.CV` | 当前只有计算机视觉相关规则，NLP / systems / security 仍是空白 |
| `math` | 低到中 | `partial` | `math.AG` / `math.CO` / `math.DS` / `math.NA` 起步 | 已纳入理论结构连续性，并开始拆到数学内部子域；当前 `AG` 已实现、`CO` 已落地第一条保守 MVP 规则、`DS` 已将第一条 `ergodic / entropy` conservative MVP 落地、`NA` 已把第一条 `matrix / Krylov iterative` conservative MVP 代码落地 |
| `hep` | 中 | `partial` | `hep-th` 起步 | 当前与数学共用理论结构连续性规则，仍然偏粗 |
| `eess` | 中 | `partial` | 与医学影像链路有关 | 当前更多是作为医学影像上游来源域出现 |
| `stat` | 低 | `gap` | 可优先考虑 `stat.ML` / `stat.ME` | 目前没有独立规则 |
| `econ` | 低 | `gap` | 可优先考虑因果推断与实验设计 | 目前没有独立规则 |
| `q-bio` | 低 | `gap` | 可优先考虑 `q-bio.QM` / `q-bio.BM` | 目前没有独立规则 |
| `astro-ph` | 低 | `gap` | 可优先考虑 survey / observation / ML 分析链路 | 目前只有通用规则 |
| `quant-ph` | 低 | `gap` | 待定 | 目前只有通用规则 |
| `cond-mat` | 低 | `gap` | 待定 | 目前只有通用规则 |
| `physics` | 低 | `gap` | 待定 | 目前只有通用规则 |
| `gr-qc` | 低 | `gap` | 待定 | 目前只有通用规则 |
| `nucl` | 低 | `gap` | 待定 | 目前只有通用规则 |
| `q-fin` | 低 | `gap` | 待定 | 目前只有通用规则 |
| `nlin` | 低 | `gap` | 待定 | 目前只有通用规则 |
| `math-ph` | 低 | `gap` | 待定 | 目前只有通用规则 |

## Layer 2 Coverage

这一层只记录“已经开始特化”或“下一步明确要做”的固定子类。

| Layer 1 | Layer 2 | Coverage | Status | Current Rule | Notes |
|---------|---------|----------|--------|--------------|-------|
| `cs` | `cs.CV` | 中 | `partial` | `representation_to_perception_same_pipeline` | 当前主要覆盖 3D 视觉 / 表示到感知的链路 |
| `math` | `math.AG` | 中 | `partial` | `math_ag_object_continuity`, `math_ag_method_continuity`, `formal_structure_same_lineage` | 已开始区分对象连续性与方法连续性 |
| `hep` | `hep-th` | 中 | `partial` | `formal_structure_same_lineage` | 当前能覆盖部分规范理论 / 圈振幅 / 弦论邻域 |
| `eess` + `cs` | `eess.IV` / `cs.CV` | 中到高 | `ready` | `imaging_to_analysis_same_pipeline` | 当前医学影像链路实际跨多个 Layer 1/2，需要保留联合记录 |
| `stat` | `stat.ML` | 低 | `gap` | - | 可优先考虑因果估计、实验设计、推断流程链路 |
| `econ` | `econ.EM` / `econ.TH` / `econ.GN` | 低 | `gap` | - | 需要先梳理当前实际出现频繁的子类 |
| `math` | `math.CO` | 中 | `partial` | `math_co_matroid_structure_continuity` | 第一条 matroid-family gate 已以保守 MVP 落地；`MCO-FILL-02` 之后当前结论固定为“守边界，不吸收 `global_16 -> global_292`，但把它登记为 supporting bridge outside gate” |
| `math` | `math.DS` | 中 | `partial` | `math_ds_ergodic_entropy_continuity` | `22` topics，`3` multi-period；第一条 conservative MVP 已落地，但 current positives 仍 bridge-level only；`complex dynamics` / `hyperbolic systems` 保留为 secondary candidates |
| `math` | `math.LO` | 中 | `partial` | `math_lo_formal_system_continuity`, `math_lo_modal_continuity`, `math_lo_type_theory_continuity`, `math_lo_set_theory_continuity`, `math_lo_forcing_continuity`, `math_lo_definability_continuity` | `modal` 已形成 event-level baseline；其余 4 条支路当前更适合作为一个 bridge-level ring 来讲述：type-theory 对照、set theory 主干、forcing 外支、definability 收束支路 |
| `math` | `math.PR` | 低 | `gap` | - | 当前仍不应直接复用 `math.AG` 的结构词逻辑 |
| `math` | `math.NA` | 中 | `partial` | `math_na_krylov_iterative_continuity` | `36` topics，`7` multi-period；第一版真实 skeleton 已固定，且首条 conservative MVP 已落地；当前 gate 只认 exact `gmres/krylov/lanczos/arnoldi` core，仍需继续回避 duplicate-prone pairs 与 generic solver words |
| `math` | `math.RT` | 低 | `gap` | - | `5` topics，`0` multi-period，`4` internal adjacent，`1` internal evolves_from；当前只能固定 1 个弱 positive watchlist（`global_193 -> global_358`），不足以起第一版 skeleton |
| `math` | `math.RA` | 低 | `gap` | - | 当前仅 3 topics，全部仅 1 个 period，0 evolution cases；需要更长数据窗口 (>=24 个月) 重新评估 |
| `math` | `math.QA` | 低 | `gap` | - | 当前 0 topics，hierarchy 完全缺失；需 >=10 topics 且 >=3 multi-period 才能重新评估 |

## 当前已落地的特化规则

| Rule | Preferred Tree Path | Status | Notes |
|------|---------------------|--------|-------|
| `imaging_to_analysis_same_pipeline` | `eess > eess.IV` and `cs > cs.CV` | `ready` | 对应“成像/重建 -> 分割/诊断/分析” |
| `representation_to_perception_same_pipeline` | `cs > cs.CV` | `partial` | 对应“表示/渲染 -> 感知/重建” |
| `math_ag_object_continuity` | `math > math.AG` | `partial` | 对应代数几何里对象层面的连续演化 |
| `math_ag_method_continuity` | `math > math.AG` | `partial` | 对应代数几何里方法层面的连续演化 |
| `math_co_matroid_structure_continuity` | `math > math.CO` | `partial` | 第一条已落地的 math.CO 窄规则；当前为保守 MVP，要求 matroid-family term + 至少 2 个离散结构 family，并明确拒绝 rank/polynomial-only 与 polytope-only near-miss；`global_16 -> global_292` 固定为 supporting bridge outside gate |
| `math_ds_ergodic_entropy_continuity` | `math > math.DS` | `partial` | 第一条已落地的 math.DS 窄规则；当前为保守 MVP，要求 shared `entropy` + shared `ergodic/topological`，并明确把 `measure(s)` 限定为 supporting evidence only；`ds-a1` 固定保留为 ambiguous boundary |
| `math_na_krylov_iterative_continuity` | `math > math.NA` | `partial` | 第一条已落地的 math.NA 窄规则；当前为保守 MVP，promotion core 只认 exact `gmres/krylov/lanczos/arnoldi`，并只允许 `shared core >= 2` 或 `shared gmres + target full four-term bundle`；`matrix/block` 仅 supporting，`na-a1` 固定保留为 ambiguous boundary |
| `math_lo_formal_system_continuity` | `math > math.LO` | `partial` | 对应逻辑 / 模型论 / 类型论 / 集合论的形式系统连续性；作为 fallback 规则，被子规则细分覆盖；单元测试验证通过 |
| `math_lo_modal_continuity` | `math > math.LO > 数理逻辑 > 模态逻辑 / 非经典逻辑` | `partial` | 对应模态逻辑、非经典逻辑、直觉主义逻辑、概率逻辑之间的局部连续性；当前是 math.LO 中唯一成熟的 event-level baseline |
| `math_lo_type_theory_continuity` | `math > math.LO > 数理逻辑 > 直觉主义逻辑` | `partial` | 对应 proof/calculus 到 type/programming-logic 的跨路径连续性；当前稳定停留在 bridge-level，承担 ring 中的 contrast branch：词典级桥接成立，但图结构支持与 event-level readiness 缺失 |
| `math_lo_set_theory_continuity` | `math > math.LO > 集合论与基数理论` | `partial` | 对应基数理论、超滤子、公理、力迫法之间的对象连续性；当前是 math.LO bridge-level ring 的 inner backbone，图结构支持强于其他 bridge-level 支路，但尚无 replay event-level 命中 |
| `math_lo_forcing_continuity` | `math > math.LO > 集合论与基数理论 > 力迫法` | `partial` | 对应 forcing / large-cardinal 邻域在 `math.LO` 与 `cs.LO` 之间的跨路径连续性；当前承担 ring 的 outer cross-path branch，语义桥接成立，但 benchmark 正例 pair 本身无 direct graph edge |
| `math_lo_definability_continuity` | `math > math.LO > 集合论与基数理论` | `partial` | 对应 set-theoretic definability 在 `math.LO` 与 `cs.LO` 之间的跨路径连续性；当前承担 ring 的 narrow capstone，有轻量 direct adjacency 支持，但尚无 replay event-level 命中 |
| `formal_structure_same_lineage` | `math > math.AG` and `hep > hep-th` 起步 | `partial` | 对应数学/理论主题的形式结构连续性 |

## 数学方向的当前判断

数学现在已经纳入主表，但仍然只是 **第一版 tree-path 适配**。

当前状态：

- `tree_path = math` 已有专门规则，不再是完全空白
- 更细的路径目前已在 `math > math.AG`、`math > math.CO` 与 `math > math.DS` 三个分支开始起步
- `math > math.NA` 已完成第一轮真实 benchmark skeleton bootstrap，并已把 `math_na_krylov_iterative_continuity` 以保守 MVP 落地
- `math > math.DS` 已完成第一轮真实 benchmark skeleton bootstrap，并已把第一条最可能方向收敛到 `math_ds_ergodic_entropy_continuity`
- `math > math.CO` 已完成第一轮真实 benchmark skeleton bootstrap，并已把 `math_co_matroid_structure_continuity` 以保守 MVP 落地
- `MCO-FILL-02` 已把 `math.CO` 当前图叙事固定成三层：confirmed MVP / supporting bridge outside gate / excluded boundary
- `math.AG` 现在已经开始区分对象连续性和方法连续性
- `math.AG` 的对象连续性已加入 taxonomy 与层次权重，但真实案例词典仍偏弱
- 其他数学子类还不能套用同一逻辑

这意味着：

- 现在可以说“数学已纳入考虑”
- 但不能说“数学内部各子域已经适配”

## 理论领域优先级

从规则开发顺序上，当前优先级建议明确向纯理论领域倾斜。

原因：

1. 纯理论领域的发展脉络通常更稳定，语义对象更清晰。
2. 这类领域更适合先验证“结构连续性”而不是“热点 carryover”。
3. 数学与理论物理可以作为方法论试验场，再把经验迁移到应用领域。

当前建议的优先顺序：

1. `math`
2. `hep`
3. `math-ph`
4. `cs > cs.CV`
5. 其他应用与交叉路径

## 数学方向下一步建议

建议严格沿 `Layer 2` 推进，而不是继续用一个泛化数学规则覆盖全部纯数。

| Priority | Tree Path | Suggested Rule |
|----------|-----------|----------------|
| P1 | `math > math.AG` | 区分“对象连续性”与“方法连续性” |
| P1 | `math > math.CO`, `math > math.DS` | `math.CO` 已把第一实现分支收敛到 `math_co_matroid_structure_continuity`；`math.DS` 第一条 conservative MVP 已落地到 `math_ds_ergodic_entropy_continuity`，下一步重点是守住边界，不要从 generic systems/maps/random 词开门 |
| P1 | `math > math.PR`, `math > math.AP` | 概率对象 -> 分析方法 -> 极限行为的链路 |
| P1 | `math > math.LO` | 模型论 / 类型论 / 范畴论的形式系统连续性 |
| P2 | `math > math.NA` | 第一条方向现已收敛到 `matrix / Krylov iterative continuity`；先守住 `gmres / krylov / lanczos / arnoldi` 这类 method-family 词，再看是否扩到更宽 solver continuity |
| — | `math > math.RT` | **当前标记为 gap** / insufficient data；仅 `5` topics、`0` multi-period、`1` 条内部 evolves_from；唯一接近的 `Lusztig / Hecke` 支路还不足以固定第一版 skeleton |
| — | `math > math.QA`, `math > math.RA` | **当前标记为 gap** / insufficient data；需要更长数据窗口 (>=24 个月) 重新评估 |

## 下一批优先级

| Priority | Tree Path | Suggested Rule |
|----------|-----------|----------------|
| P1 | `math > math.LO` | 先落第一条形式系统连续性规则 |
| P1 | `math > math.AG`, `math > math.CO`，再扩到 `math > math.PR` | 拆分数学内部子域规则 |
| P1 | `cs > cs.CV` | 细化 `representation -> perception -> planning` 的阶段 taxonomy |
| P2 | `stat > stat.ML`, `stat > stat.ME` | 因果推断、实验设计、识别策略之间的自然演化链路 |
| P2 | `econ > *` | 先从实际样本中归纳活跃路径，再定义规则 |
| P2 | `q-bio > q-bio.QM`, `q-bio > q-bio.BM` | 分子表示 -> 结合预测 -> 下游设计 |

## 更新清单

### 2026-03-22 (math.RT)

- **MRT-01**: 完成 `math.RT` bootstrap readiness 评估
- 新增 gap assessment 条目 `math_rt_gap_insufficient_data`
- Tree Path Registry 新增 `math > math.RT` 条目，状态为 `gap`
- Layer 2 Coverage 新增 `math > math.RT` 条目，状态为 `gap`
- 新建 `docs/plans/2026-04-03-math-rt-rule-review.md`
- 数据扫描结论：`5` topics，`0` 个 multi-period topics，`4` 条域内邻接边，`1` 条域内 evolves_from 边
- 当前判断：`math.RT` 还不是 benchmark-skeleton-ready；不能安全固定 `2 positive + 2 negative + 1 ambiguous`
- 证据核心：`global_193 -> global_358` 是唯一接近 positive 的 `Lusztig / Hecke` watchlist，但没有第二个同级正例；唯一内部 `evolves_from`（`global_177 -> global_358`）只共享泛词 `algebra`
- 决策：Option B (Gap)，本轮不创建 benchmark skeleton
- 风险提示：`global_356 -> global_358` 虽同属 `p-adic / reductive` 邻域，但为同月 pair（`2026-02 -> 2026-02`），不能作为 bootstrap backbone

### 2026-03-22 (math.NA)

- **MNA-01**: 正式启动 `math.NA` 第一轮 benchmark case curation
- 新增 bootstrap assessment 条目 `math_na_bootstrap_case_curation`
- 新增 planned rule 条目 `math_na_krylov_iterative_continuity`
- Tree Path Registry 新增 `math > math.NA` 条目，状态为 `planned`
- Layer 2 Coverage 将 `math.NA` 从 `math.PR / math.NA` 混合 gap 行中拆出，单独标记为 `planned`
- 新建 `docs/plans/2026-04-03-math-na-benchmark.md` 和 `docs/plans/2026-04-03-math-na-rule-review.md`
- 数据扫描结论：`36` topics，`7` 个 multi-period topics，`86` 条域内邻接边，`18` 条域内 evolves_from 边，足以固定第一版真实 benchmark skeleton
- 当前判断：`math.NA` 已是 benchmark-skeleton-ready，但还没有 event-level baseline，也还没有代码落地的特化规则
- 第一批 fixed cases：`na-b1/na-b2` positive，`na-n1/na-n2` negative，`na-a1` ambiguous
- 当前最可能的第一条 rule direction：`math_na_krylov_iterative_continuity`
- 额外风险提示：`global_23 -> global_62`、`global_9 -> global_251/391`、`global_236 -> global_258` 等 attractive pairs 存在 `5/5` representative-title overlap，当前不应作为第一条 rule contract 主干
- **MNA-FILL-02**: 将 `math_na_krylov_iterative_continuity` 以保守 MVP 代码落地
- Tree Path Registry 与 Layer 2 Coverage 中 `math > math.NA` 状态从 `planned` 更新为 `partial`
- runtime gate 固定为：
  - shared exact core `gmres/krylov/lanczos/arnoldi >= 2`
  - 或 shared `gmres` 且 target 暴露完整 `arnoldi + gmres + krylov + lanczos` 四词束
- `matrix / block` 被明确降级为 supporting evidence only，generic `numerical / convergence / approximation` 不参与 promotion
- benchmark contract 已验证：
  - `na-b1/na-b2` 通过
  - `na-n1/na-n2` 拒绝
  - `na-a1` 继续保持 ambiguous boundary
- Claude review 结论：当前实现是可信的 conservative MVP；主要残余风险集中在单共享 `gmres` fallback，后续若出现综述型 target 需再加 anchor-side guard

### 2026-03-22 (math.DS)

- **MDS-01**: 正式启动 `math.DS` 第一轮 benchmark case curation
- 新增 bootstrap assessment 条目 `math_ds_bootstrap_case_curation`
- 新增 planned rule 条目 `math_ds_ergodic_entropy_continuity`
- Tree Path Registry 新增 `math > math.DS` 条目，状态为 `planned`
- Layer 2 Coverage 新增 `math > math.DS` 条目，状态为 `planned`
- 新建 `docs/plans/2026-04-02-math-ds-benchmark.md` 和 `docs/plans/2026-04-02-math-ds-rule-review.md`
- 数据扫描结论：`22` topics，`3` 个 multi-period topics，`49` 条域内邻接边，`12` 条域内 evolves_from 边，足以固定第一版真实 benchmark skeleton
- 当前判断：`math.DS` 已是 benchmark-skeleton-ready，但还没有 event-level baseline，也还没有代码落地的特化规则
- 当前最可能的第一条 rule direction：`math_ds_ergodic_entropy_continuity`
- **MDS-FILL-02**: 将 `math_ds_ergodic_entropy_continuity` 落地为 conservative MVP
- 规则状态从 `planned` 更新为 `partial`
- Tree Path Registry / Layer 2 Coverage 中的 `math > math.DS` 状态同步更新为 `partial`
- runtime gate 固定为 shared `entropy` + shared `ergodic/topological`
- `measure(s)` 明确降为 supporting evidence only；`systems` / `maps` / `random` 不进入 promotion signal
- benchmark contract 当前固定为：`ds-b1/ds-b2` 通过，`ds-n1/ds-n2` 拒绝，`ds-a1` 保持 ambiguous boundary

### 2026-03-21

- **MQAR-01**: math.QA 和 math.RA gap 状态收口
- 新增规则条目 `math_qa_gap_no_data`，记录 math.QA 完全缺失数据
- Tree Path Registry 新增 `math > math.QA` 条目，状态为 `gap`
- Layer 2 Coverage 新增 `math > math.QA` 条目，状态为 `gap`
- math.RA 状态已于 2026-03-18 完成收口，本次确认无误
- 创建 gap 文档：`docs/plans/2026-03-18-math-qa-gap.md` 和 `docs/plans/2026-03-18-math-ra-gap.md`
- math.QA 评估：0 topics，hierarchy 完全缺失，gap 起始于 topic modeling / data ingestion 层
- math.RA 评估：3 topics，全部仅 1 个 period，0 evolves_from edges，域内无边，含跨域噪声

### 2026-03-22 (math.CO)

- **MCO-FILL-02**: 审查 `global_16 -> global_292` 是否可安全并入当前 `math_co_matroid_structure_continuity`
- 结论：当前不能安全吸收；维持 rule gate 不变
- 决定性原因：pair 仅有 `matroid` shared family；若要升级，必须借用 target-only structure、`rank/polynomial` 背景词或图边模式
- `math.CO` graph-facing 口径固定为：confirmed MVP = `co-m1/co-m2`，supporting bridge outside gate = `global_16 -> global_292`，excluded boundary = `co-mn1/co-mn2/co-ma1`
- **MCO-02**: `math.CO` 第一实现分支收敛到 `math_co_matroid_structure_continuity`
- 新增 rule registry 条目 `math_co_matroid_structure_continuity`
- `math.CO` Tree Path Registry 从 “benchmark skeleton only” 更新为 “selected first branch: matroid”
- 新建 implementation-ready 计划文档：`docs/plans/2026-04-01-math-co-first-rule-plan.md`
- 明确 `random / percolation` 暂缓，原因是 generic graph/process vocabulary 误判风险更高
- 固定 implementation-ready contract：`co-m1`, `co-m2`, `co-mn1`, `co-mn2`, `co-ma1`
- **MCO-01**: 正式启动 `math.CO` 第一轮 benchmark case curation
- 新增 bootstrap assessment 条目 `math_co_bootstrap_case_curation`
- Tree Path Registry 新增 `math > math.CO` 条目，状态为 `partial`
- Layer 2 Coverage 将 `math.CO` 从 `math.CO / math.PR / math.NA` 混合 gap 行中拆出，单独标记为 `partial`
- 新建 `docs/plans/2026-03-31-math-co-benchmark.md` 和 `docs/plans/2026-03-31-math-co-rule-review.md`
- 数据扫描结论：47 topics，7 个 multi-period topics，138 条域内邻接边，38 条域内 evolves_from 边，足以固定第一版真实 benchmark skeleton
- 当前判断：`math.CO` 已是 benchmark-skeleton-ready，并已有保守 MVP 特化规则；但仍没有 event-level baseline
- 当前最可能的 rule direction：`discrete structure continuity`，优先关注 `matroid structure` 与 `random graph / percolation` 两个子支路

### 2026-03-12

- 为 `math_ag_object_continuity` 规则添加 benchmark cases
- 基于当前 Math.AG 数据集分析 (17个topics):
  - 仅发现 1 个正例对满足 >=2 共享对象词条件: `global_69 -> global_287` (共享 stacks/stack)
  - 当前数据集中对象词覆盖率较低，大部分 topic 仅包含 8 个关键词
- 正例 (1个):
  - `ag-b1` (legacy runner ID, later canonicalized as `ag-p1`): global_69 (代数叠与层理论) -> global_287 (导出代数叠范畴)，共享 stacks/stack (2个对象词)
- 负例 (5个):
  - `ag-n1`: global_69 -> global_136，仅共享 sheaves (1个对象词)，不满足 >=2 阈值
  - `ag-n2`: global_30 -> global_355，无直接共享对象词
  - `ag-n3`: global_30 -> global_215，仅共享 hodge/rational/adic 等泛词
  - `ag-n4`: global_107 (仿射代数群挠子) -> global_117 (志村簇)，无共享对象词 (torsors vs varieties)
  - `ag-n5`: global_134 (凸体与薄饼多面体) -> global_349 (热带几何)，无共享对象词 (polytopes vs tropical curves)
- 更新文件: `docs/plans/2026-03-10-evolution-rule-coverage.md`
- 关键发现: 当前数据集中对象词覆盖率限制了正例数量，建议扩充关键词词典

### 2026-03-18

- **PKG-RA-01-registry-fix**: 同步 math.RA 为 gap 状态
- Tree Path Registry 新增 `math > math.RA` 条目，状态为 `gap`
- Layer 2 Coverage 新增 `math > math.RA` 条目，状态为 `gap`
- 新增规则条目 `math_ra_gap_insufficient_data`，记录数据评估详情
- 更新”数学方向下一步建议”表：math.QA 和 math.RA 明确标记为 gap
- 当前数据评估：3 topics，全部仅 1 个 period，0 evolution cases
- 决策：Option B (Gap)，后续需 >=24 个月数据重新评估

### 2026-03-10

- 新增文档并建立规则覆盖矩阵
- 重构为”主题树路径优先”的视图，`Layer 1 -> Layer 2` 仅作为上层摘要
- 记录当前已落地的 3 条领域特化规则：
  - `imaging_to_analysis_same_pipeline`
  - `representation_to_perception_same_pipeline`
  - `formal_structure_same_lineage`
- 明确把数学标记为：
  - `tree_path = math` 为 `partial`
  - 更细路径仅 `math > math.AG` 起步，不是全数学适配
