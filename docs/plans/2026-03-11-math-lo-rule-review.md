# Math.LO Rule Review

## Summary

截至当前版本，`math.LO` 相关自然演化规则已经拆成 6 条：

- `math_lo_formal_system_continuity`
- `math_lo_modal_continuity`
- `math_lo_type_theory_continuity`
- `math_lo_set_theory_continuity`
- `math_lo_forcing_continuity`
- `math_lo_definability_continuity`

这些规则整体上仍更适合作为 `bridge-level` 解释层，而不是主案例筛选层。

更准确地说：

- `math_lo_modal_continuity` 是当前唯一已经具备 `event-level` 证据的 `math.LO` 子规则
- 其余 `type / set / forcing / definability` 仍主要停留在 `bridge-level`
- 后续 benchmark / demo 叙事应以 `modal` 作为 baseline，以 `type-theory` 作为 bridge-level 对照，而不是把它们并排当成同层级正例

## Bridge-Level Ring View

如果把 `math.LO` 放进图谱讲述层，当前最稳定的说法不是“modal 外还有几条零散正例”，而是：

- `modal` = event-level baseline 主线
- `type-theory` = bridge-level contrast branch
- `set theory` = bridge-level inner backbone
- `forcing` = bridge-level outer cross-path branch
- `definability` = bridge-level narrow capstone branch

也就是说，`math.LO` 更适合被讲成“1 条 baseline 主线 + 1 个 bridge-level ring”。

这个 ring 的入图标准也应固定为：

- 能稳定代表一条独立的解释支路
- 能用正例 + near-miss/negative 说清边界
- 即使还没有 event-level readiness，也不误写成事件

## Main Case Coverage

当前主产物 [evolution_cases.json](/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/data/output/evolution_cases.json) 的 12 个自动案例里，出现过的规则只有：

- `representation_to_perception_same_pipeline`: 1
- `imaging_to_analysis_same_pipeline`: 2
- `formal_structure_same_lineage`: 1
- `math_ag_object_continuity`: 1

`math.LO` 六条规则在主 12 案例中当前都没有命中。

这说明：

- `math.LO` 规则已经能解释局部邻接关系
- 但当前 anchor 自动选择与事件主路径仍然偏向高热度案例
- 理论逻辑类规则更多停留在局部 replay / bridge evidence 层

## Manual Replay Signals

### 1. `math_lo_modal_continuity`

最稳定的真实正例：

- `global_56-2025-03`
  - `直觉主义逻辑证明 -> 概率逻辑与自动机语义`

判断：

- 当前最成熟的 `math.LO` 子规则
- 已在手动 replay 的事件层命中
- `global_56 <-> global_27` 有 `adjacent_to` 边（weight=0.4025），且两者都具备 multi-period 支撑（`active_periods=3`）
- 可以视作 `math.LO` 中唯一进入“事件级有效”的规则
- 它之所以是 `event-level`，不只是因为词典重叠，而是“词典级桥接 + 图结构支持 + event-level readiness”三层同时成立
- 这也是后续 demo/baseline 最应优先展示的 `math.LO` case

### 2. `math_lo_type_theory_continuity`

当前桥接正例：

- `global_56 -> global_980`
  - `直觉主义逻辑证明 -> 程序线性化与类型`
  - 共享 type object：`type`, `types`, `typed`（3 个）
  - anchor source terms：`proof`, `calculus`, `intuitionistic` ✓
  - target terms：`program`, `languages`, `subtyping`, `correctness` ✓
  - **图结构**：两者无 `adjacent_to` 边，无 `evolves_from` 边
  - `global_980`：`active_periods=1`，全图仅 1 条邻接边（→ `global_1031`）

当前负例：

- `global_56 -> global_438`（主题完全错位，AI 推理）
- `global_980 -> global_438`（方向错位）
- `global_56 -> global_977`（lo-n7）：图邻接（0.225），但 `global_977` 无 `type/types/typed`，只触发 modal 规则
- `global_56 -> global_1155`（lo-n8）：图邻接（0.2711），`global_1155` 无 `type` 对象词，相似性来自 modal/semantics 方向

判断（MLO-02 更新）：

- 这条规则的结构是合理的，词面桥接（Curry-Howard 对应）真实存在
- **明确停留在 bridge-level，不接近 event-level**
- 三层边界应写死为：
  - `词典级桥接`：成立。`global_56 -> global_980` 的 proof/calculus/intuitionistic 到 type/programming-logic 连接可解释
  - `图结构支持`：缺失。两者无 `adjacent_to` 边，无 `evolves_from` 边；`global_980` 拓扑孤立且仅单期活跃
  - `event-level readiness`：缺失。当前无 replay 事件层命中，也没有可复现的多期扩散信号
- 图结构证据与 modal_continuity 形成强对比：global_56↔global_27 有 adjacent_to（weight=0.4025）且已进入 replay 事件层；type_theory 无图邻接、无 replay 命中
- `global_56` 的实际演化扩散方向是 `global_27`（modal/概率逻辑），不是 cs.LO type theory
- lo-n7/lo-n8 是比 lo-n5/lo-n6 更精准的近失负例：测试"缺少 type object"这一关键边界，而非主题整体错位
- 这条规则当前最适合在 baseline 叙事中充当“bridge-level contrast case”，用于解释为什么有些语义桥接应该保留，但不能被包装成演化事件
- 还没有在 replay 事件层浮现，且短期内不具备升级条件（global_980 孤立，active_periods=1）

### 3. `math_lo_set_theory_continuity`

当前桥接正例：

- `global_313 -> global_360`
  - `基数与超滤子公理 -> ZF基数选择公理`
- `global_51 -> global_75`
  - `基数与波莱尔公理 -> 基数迭代强制法`

当前负例 / near-miss：

- `global_339 -> global_51`（lo-a2，near-miss / ambiguous）
- `global_167 -> global_75`

判断：

- 这条规则在对象连续性上是通的，而且是当前 bridge-level ring 中**最像内环主干**的一支
- `global_313 -> global_360` 是它最值得保留的正例：共享 `cardinal/cardinals/axiom`，同时有 `adjacent_to`（0.4235）和 `evolves_from`（0.4435），说明集合论主干内部确有图结构支持
- `global_51 -> global_75` 的价值主要是**边界澄清**：带有 `forcing` 词的 case 不一定应被讲成 forcing 外支；在当前口径里，这对更应留在 set-theory backbone
- `global_339 -> global_51` / `global_167 -> global_75` 说明 cluster proximity 或弱对象重叠仍不足以稳定过线
- 但事件层没有稳定命中，且主正例基本都是 single-period topic，因此它仍应停留在 bridge-level，而不是升级为主事件解释器

### 4. `math_lo_forcing_continuity`

当前桥接正例：

- `global_51 -> global_951`
  - `基数与波莱尔公理 -> 基数与力迫法`

当前负例 / near-miss：

- `global_75 -> global_951`（lo-a1，near-miss / ambiguous）
- `global_339 -> global_951`

判断：

- 当前最有价值的是跨 `math.LO -> cs.LO` 的 forcing / large-cardinal 连续性，因此它更适合承担 **outer cross-path branch** 的角色
- `axiom` 作为必要词后，规则明显更稳；`lo-n1` / `lo-a1` 也因此变得更有意义，因为它们把 forcing 外支与 set-theory backbone 分开了
- `global_51 -> global_951` 这对正例本身没有 direct `adjacent_to` 或 `evolves_from` 边，所以它不能被包装成事件；它的价值在于保留一条“值得讲”的外环桥接
- `global_951` 在图里并非完全孤立：它与 `global_360`、`global_778`、`global_1155` 有邻接，说明 forcing 支路在整体 ring 中是可讲述的，但正例 pair 仍只是 bridge-level
- 仍未进入 replay 事件层

### 5. `math_lo_definability_continuity`

当前桥接正例：

- `global_75 -> global_778`
  - `基数迭代强制法 -> 武丁公理与可定义性`

当前负例：

- `global_167 -> global_778`
- `global_361 -> global_778`

判断：

- 这是目前最窄、也最干净的 `definability` 规则，因此最适合承担 **narrow capstone branch** 的角色
- `global_75 -> global_778` 既保留了 set-theoretic special object（`woodin/axiom`），又有 `adjacent_to` 边（0.225），说明它不是纯词面拼接
- `global_167 -> global_778` 与 `global_361 -> global_778` 的负例一起把边界钉住了：`definable` 不是自由通行证，仍要保留 `cardinal/cardinals + special object` 的组合要求
- 但它仍缺 replay 事件层命中，且 anchor/target 都只有 1 个活跃期，所以当前依然停留在 bridge-level

### 6. `math_lo_formal_system_continuity`

当前状态：

- 更像 `math.LO` 的总兜底规则
- 在细分规则增加后，应减少它直接承担解释的范围

判断：

- 后续应保留，但不应继续放宽
- 它更适合作为未覆盖子域的 fallback

## Failure Modes

- 把 `modal` 之外的 bridge-level positive 误讲成 `event-level`，会直接破坏 `math.LO` 的层级口径
- 把 `global_51 -> global_75` 这类集合论主干内部连续性误吸进 forcing 叙事，会让 bridge-level ring 失去清晰分工
- 把 `type`、`forcing`、`definable` 这类单词本身当成充分证据，会把支路说明退化成关键词拼接，而不是边界清楚的图谱解释

## Current Assessment

按成熟度排序：

1. `math_lo_modal_continuity`
2. `math_lo_type_theory_continuity`
3. `math_lo_set_theory_continuity`
4. `math_lo_forcing_continuity`
5. `math_lo_definability_continuity`
6. `math_lo_formal_system_continuity`

其中：

- `modal` 已进入事件层，可作为 `math.LO` 的 event-level baseline
- `type / set / forcing / definability` 当前更适合一起视为一个 bridge-level ring，而不是 4 条彼此孤立的正例
- 这个 ring 内部的角色分工应固定为：`type-theory = contrast`、`set theory = inner backbone`、`forcing = outer cross-path branch`、`definability = narrow capstone`
- `formal_system` 更像保底规则

## Recommended Next Step

下一步不建议继续横向增加更多 `math.LO` 规则数量。

更值的方向是二选一：

### Option A

改进 anchor 选择与事件抽取，让理论类 topic 更容易进入主案例。

目标：

- 让现有 `math.LO` 规则从 bridge-level 进入 event-level

### Option B

继续收紧已经建立的 `math.LO` benchmark / review 口径，而不是继续扩 case 数量。

目标：

- 固定 `modal = event-level baseline`
- 固定 `type-theory = bridge-level contrast`
- 固定 `set theory = inner backbone`
- 固定 `forcing = outer cross-path branch`
- 固定 `definability = narrow capstone`
- 用同一套三层边界描述 bridge-level：`词典级桥接`、`图结构支持`、`event-level readiness`

推荐优先做 `Option B`，因为 benchmark 已经建立，当前更缺的是叙事稳定性而不是 case 数量。
