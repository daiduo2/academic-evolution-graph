doc_type: "benchmark"
scope: "math > math.LO"
status: "active"
owner: "trend-monitor"
source_of_truth: true
upstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-11-evolution-doc-standards.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-10-evolution-rule-coverage.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-11-math-lo-rule-review.md"
downstream_docs: []
last_reviewed: "2026-03-22"

# Math.LO Benchmark

## Purpose

这份文档固定 `math.LO` 的代表性 benchmark case。

用途不是证明系统已经完成，而是给后续规则迭代、弱模型维护和回归检查提供一个统一基准。

## Scope

范围限定为：

- `math > math.LO`
- 以及与其直接相关的 `cs.LO` 跨路径连续性

## Case List

### Positive Cases

| Case ID | Anchor | Target | Expected Relation | Level |
|---------|--------|--------|-------------------|-------|
| `lo-b1` | `global_56` 直觉主义逻辑证明 | `global_27` 概率逻辑与自动机语义 | `math_lo_modal_continuity` | event-level |
| `lo-b2` | `global_56` 直觉主义逻辑证明 | `global_980` 程序线性化与类型 | `math_lo_type_theory_continuity` | bridge-level |
| `lo-b3` | `global_313` 基数与超滤子公理 | `global_360` ZF基数选择公理 | `math_lo_set_theory_continuity` | bridge-level |
| `lo-b4` | `global_51` 基数与波莱尔公理 | `global_951` 基数与力迫法 | `math_lo_forcing_continuity` | bridge-level |
| `lo-b5` | `global_75` 基数迭代强制法 | `global_778` 武丁公理与可定义性 | `math_lo_definability_continuity` | bridge-level |

### Positive Case Notes

- `lo-b1`（`global_56 -> global_27`）：这是当前 `math.LO` benchmark 中唯一明确的 `event-level` 正例。它不是只靠词面相似成立：两者有 `adjacent_to` 边（weight=0.4025），且都具备 multi-period 支撑（`active_periods=3`）；同时已在手动 replay 的事件层出现。因此它满足“词典级桥接 + 图结构支持 + event-level readiness”三层条件，是后续 demo/baseline 的首选标杆。
- `lo-b2`（`global_56 -> global_980`）：连接基于共享 `type/types/typed`（3 个 type object），anchor 有 `proof/calculus/intuitionistic`，target 有 `program/languages/subtyping/correctness`。词典级桥接合理。**但图结构无支持**：两者无 `adjacent_to` 边，无 `evolves_from` 边；`global_980` 拓扑孤立（`active_periods=1`，仅 1 条邻接边）。同时也**没有 event-level readiness**：未进入 replay 事件层，target 仅单期活跃。这是词典级桥接正例，不是图演化正例。确认为 bridge-level，不接近 event-level。
- `lo-b3`（`global_313 -> global_360`）：这是当前 bridge-level ring 里**图结构最完整**的一支。两者共享 `cardinal/cardinals/axiom`，同时有 `adjacent_to` 边（weight=0.4235）和 `evolves_from` 边（weight=0.4435）。但两者都只有 `active_periods=1`，也没有 replay 事件层命中，所以仍不能升到 event-level。它值得出现在图里，是因为它给 `math.LO` 提供了一个集合论主干内部的 **inner backbone**：说明 LO ring 不只是向外连 `cs.LO`，内部也存在可解释的桥接支路。
- `lo-b4`（`global_51 -> global_951`）：共享 `cardinal/cardinals/forcing/axiom`，把 `math.LO` 的集合论/力迫法主题连到 `cs.LO` 的大基数与力迫法邻域。**但这对正例本身没有 direct `adjacent_to` 或 `evolves_from` 边**，所以它的价值不是“已经形成事件”，而是“值得保留的一条 outward bridge”。`global_951` 在图里并非完全孤立：它与 `global_360`、`global_778`、`global_1155` 有邻接，说明 forcing 支路作为外环是可讲述的，但仍只能停留在 bridge-level。
- `lo-b5`（`global_75 -> global_778`）：共享 `definable`，并同时保持 `cardinal/cardinals + woodin/axiom` 这组 set-theoretic special object；两者有 `adjacent_to` 边（weight=0.225）。这比 type-theory/forcing 更接近图结构支持，但仍缺 replay 命中，且 anchor/target 都只有 `active_periods=1`。它值得保留，是因为它把 LO ring 从 forcing/cardinal 邻域收束到 `definability` 这一条**窄而干净的 capstone 支路**。

### Event-Level vs Bridge-Level Baseline

- `lo-b1` 应被视为 `math.LO` 的 event-level baseline：词典连续性已经被图邻接、multi-period 支撑和 replay 命中共同加固。
- `lo-b2` 应被视为 bridge-level contrast case：词典桥接成立，但图结构支持和 event-level readiness 都缺失，不能拿来叙述“真实演化事件”。
- 后续 baseline / demo 叙事应固定采用这组对照，而不是把 `math.LO` 所有 positive case 视为同一层级。

### Bridge-Level Ring Structure

- `type-theory`：对照支路。证明 `math.LO` 可以跨到 type/programming-logic 方向，但当前只具备词典级桥接。
- `set theory`：内环主干。`global_313 -> global_360` 给出集合论内部最稳的对象连续性，`global_51 -> global_75` 则说明带有 `forcing` 词的 case 也可能更适合留在集合论主干。
- `forcing`：外环跨路径支路。负责把 `math.LO` 集合论簇连到 `cs.LO` 的大基数/力迫法邻域，但 benchmark 正例本身还不是图事件。
- `definability`：窄支收束支路。把 forcing/cardinal 邻域收束到 `woodin + definable` 这一更窄的 set-theoretic semantics 方向。
- 后续知识图谱或说明层若要把 `math.LO` 讲成“1 条 baseline 主线 + 多条支路”，这 4 条支路应视为一个稳定的 bridge-level ring，而不是彼此无关的零散正例。

### Negative Cases

| Case ID | Anchor | Target | Expected Relation |
|---------|--------|--------|-------------------|
| `lo-n1` | `global_51` 基数与波莱尔公理 | `global_75` 基数迭代强制法 | `not math_lo_forcing_continuity` |
| `lo-n2` | `global_339` 基数、理想与力迫法 | `global_951` 基数与力迫法 | `none` |
| `lo-n3` | `global_167` 可定义基数塔基序 | `global_778` 武丁公理与可定义性 | `none` |
| `lo-n4` | `global_361` 亨泽尔域存在可定义性 | `global_778` 武丁公理与可定义性 | `none` |
| `lo-n5` | `global_56` 直觉主义逻辑证明 | `global_438` 大语言模型数学推理 | `none` |
| `lo-n6` | `global_980` 程序线性化与类型 | `global_438` 大语言模型数学推理 | `none` |
| `lo-n7` | `global_56` 直觉主义逻辑证明 | `global_977` 直觉主义逻辑片段证明 | `not math_lo_type_theory_continuity` |
| `lo-n8` | `global_56` 直觉主义逻辑证明 | `global_1155` 直觉主义模态逻辑语义 | `not math_lo_type_theory_continuity` |

### Negative Case Notes（type-theory 相关）

- `lo-n7`：`global_56 -> global_977`。两者**图邻接**（weight=0.225），语义高度相关（同为直觉主义逻辑）。`global_977` 关键词 `logic, intuitionistic, proof, fragment, connectives`——无 `type/types/typed`。type_theory_continuity 正确拒绝；应触发 `math_lo_modal_continuity`。这是比 lo-n5 更精准的近失：测试的是"缺少 type object"边界，而非主题完全错位。
- `lo-n8`：`global_56 -> global_1155`。两者**图邻接**（weight=0.2711），`global_1155`（直觉主义模态逻辑语义，cs.LO）关键词 `logic, intuitionistic, semantics, modal, calculi, calculus`——无 `type/types/typed`。type_theory_continuity 正确拒绝。特别价值：anchor 侧有 `intuitionistic + calculus`，target 在 cs.LO，高度接近，但 type object 缺失是决定性边界。

### Negative / Ambiguous Boundary Notes（set-theory / forcing / definability 相关）

- `lo-n1` + `lo-a1`：`global_51 -> global_75` 有 `adjacent_to` 边（0.3955），也确实共享 `forcing`；但当前更应被留在 `set-theory backbone`，而不是误讲成 forcing 外支。相对地 `global_75 -> global_951` 虽更靠近 cs.LO forcing target，却因缺 `axiom` 只能停留在 `review-needed` near-miss。这个对照说明 forcing 支路需要单独收紧，不能吞并集合论主干。
- `lo-n2` + `lo-a2`：`global_339` 与 `global_51` / `global_951` 都处在集合论-力迫法邻域，且 `global_339 -> global_51` 还有 `adjacent_to` 边（0.3455）。但“同簇 + shared cardinal/forcing”仍不足以稳定过线；这类 case 的价值在于告诉我们 ring 需要边界，而不是把整片 set-theory cluster 都画成正向支路。
- `lo-n3` + `lo-n4`：`global_167 -> global_778` 和 `global_361 -> global_778` 一起说明 `definable` 不是自由通行证。前者即便在 LO 集合论簇里图上很近，也缺 `woodin/axiom/reals/uniformization` 这类 special object；后者则是 domain mismatch。这样 definability 支路才能保持“窄而可解释”，不会退化成泛 `definable` 相似度。

### Ambiguous Cases

| Case ID | Anchor | Target | Current Status | Note |
|---------|--------|--------|----------------|------|
| `lo-a1` | `global_75` 基数迭代强制法 | `global_951` 基数与力迫法 | review-needed | 与 forcing 支路接近，但当前缺 `axiom` |
| `lo-a2` | `global_339` 基数、理想与力迫法 | `global_51` 基数与波莱尔公理 | review-needed | 对象连续性接近，但证据不足 |

## Expected Relations

- `lo-b1` 必须命中 `math_lo_modal_continuity`
- `lo-b2` 必须命中 `math_lo_type_theory_continuity`
- `lo-b3` 必须命中 `math_lo_set_theory_continuity`
- `lo-b4` 必须命中 `math_lo_forcing_continuity`
- `lo-b5` 必须命中 `math_lo_definability_continuity`

## Expected Non-Relations

- `lo-n1` 不能因为共享 `forcing` 就误判成 `math_lo_forcing_continuity`
- `lo-n2` 不能因为共享 `cardinal + forcing` 就误判
- `lo-n3` 不能因为 `definable + cardinals` 的弱联系就误判
- `lo-n4` 不能因为 `definable` 单词本身就误判
- `lo-n5` 不能把一般 AI 推理主题误判成类型理论连续性
- `lo-n6` 不能从类型系统方向误判 LLM 推理为类型理论连续性
- `lo-n7` 不能因为 anchor 侧有 `proof + intuitionistic` 就误判；target（`global_977`）无 `type/types/typed`，且两者图邻接——连接属于 modal 方向而非 type-theory 方向
- `lo-n8` 不能因为 anchor 侧有 `intuitionistic + calculus` 就误判；target（`global_1155`）无 `type` 对象词，相似性来自 modal/semantics 而非 type-theory 方向

## Review Notes

- 当前 benchmark 混合了 `event-level` 与 `bridge-level` 两种粒度，其中 `lo-b1` 是 event-level baseline，`lo-b2` 是 bridge-level contrast
- 当前更合适的叙事结构不是“5 条正例并排”，而是“1 条 baseline 主线 + 1 个 bridge-level ring”
- 后续优先目标不是增加 case 数量，而是让更多 `bridge-level` case 升到 `event-level`
- bridge-level 认定应统一拆成三层：`词典级桥接`、`图结构支持`、`event-level readiness`
- 每次新增 `math.LO` 规则时，必须至少补一个 positive case 和一个 negative case 到这份文档

### MLO-02 专项 Review（2026-03-21）

**`math_lo_type_theory_continuity` 层级确认：明确停留在 bridge-level，不接近 event-level。**

核心证据：

1. `lo-b2`（global_56 -> global_980）的连接**仅在关键词层成立**，图结构中两者无 `adjacent_to` 边，无 `evolves_from` 边
2. `global_980` 拓扑孤立：`active_periods=1`，全图仅 1 条邻接边（→ `global_1031`，weight=0.2）——孤立 topic 无法成为演化事件 target
3. `global_56` 的实际图演化方向是 `global_27`（modal/概率逻辑，adjacent weight=0.4025），而非 type theory 方向
4. 对比标杆：`math_lo_modal_continuity`（event-level）有图邻接 + replay 命中 + multi-period 支撑；type_theory 三项均无
5. 词面连接的理论基础有效（Curry-Howard 对应），但这是结构性先验知识，不是当前数据中的时序演化信号

**升级到 event-level 的前置条件（供未来参考）：**

1. `global_980` 需增加 active_periods（至少 2 个活跃期）
2. `global_56` 或同路径 anchor 需与 global_980 形成 `adjacent_to` 或 `evolves_from` 图边
3. 需在 automatic replay 中出现至少 1 次实际命中

### MLO-03 对照结论（2026-03-22）

- `math_lo_modal_continuity` 与 `math_lo_type_theory_continuity` 现在应明确承担不同叙事角色：前者是 event-level baseline，后者是 bridge-level contrast。
- `modal` 之所以是 event-level，不是因为它“更像逻辑学”，而是因为它同时满足三层条件：词典级桥接、图结构支持、event-level readiness。
- `type-theory` 之所以不是 event-level，不是因为词面桥接弱；恰恰相反，词面桥接是成立的。缺失的是图结构支持和事件层可复现性。
- `lo-n7` / `lo-n8` 的价值也因此更清楚：它们说明“图邻接 + 直觉主义词”本身并不足以把 case 推到 type-theory，决定性边界仍是 `type/types/typed` 对象词，以及是否出现独立的 event-level 证据。

### MLO-FILL-01 Bridge-Level Ring（2026-03-22）

- `modal` 的 event-level baseline 地位不变；本轮补厚的是其外侧的 bridge-level ring，而不是再抬高新的 event-level 分支。
- `set theory` 应被视为 ring 的内环主干：图结构最完整，但缺 replay / multi-period，因此仍停留在 bridge-level。
- `forcing` 应被视为 ring 的外环跨路径支路：语义值得保留，但 benchmark 正例本身无 direct graph edge，不能被写成事件。
- `definability` 应被视为 ring 的窄支收束：有轻量图支持，但价值更在于把 set-theoretic semantics 讲清，而不是声称事件成形。
- `type-theory` 保持 bridge-level contrast 角色，与上述 3 条支路一起构成“主线之外但值得进图”的稳定解释层。

## Change Log

- `2026-03-12`
  - 初版建立
  - 固定 5 个 positive、5 个 negative、2 个 ambiguous case
- `2026-03-12`
  - 补充 `lo-n6` 负例 (`global_980 -> global_438`)
  - 验证 `math_lo_type_theory_continuity` 规则不会从类型系统方向误判 LLM 推理
- `2026-03-21` (MLO-02)
  - 新增 `lo-n7`：global_56 -> global_977（图邻接 0.225，无 type object → 正确拒绝）
  - 新增 `lo-n8`：global_56 -> global_1155（图邻接 0.2711，无 type object → 正确拒绝）
  - 新增 Positive Case Notes：确认 lo-b2 为词典级桥接，无图结构支持
  - 新增 Negative Case Notes：说明 lo-n7/lo-n8 的近失诊断价值
  - 补充 MLO-02 专项 Review：基于图结构证据确认 type_theory_continuity 明确停留在 bridge-level
  - 明确 event-level 升级前置条件
- `2026-03-22` (MLO-03)
  - 补充 `lo-b1` Positive Case Note：明确它是 `math.LO` 当前唯一 event-level baseline
  - 收紧 `lo-b2` 说明：拆成“词典级桥接 / 图结构支持 / event-level readiness”三层边界
  - 新增 Event-Level vs Bridge-Level Baseline 小节，固定 `modal vs type-theory` 的 benchmark 对照口径
  - 补充 MLO-03 对照结论，统一后续 demo/baseline 叙事
- `2026-03-22` (MLO-FILL-01)
  - 补充 `lo-b3` / `lo-b4` / `lo-b5` Positive Case Notes，明确它们各自在 bridge-level ring 中的叙事角色
  - 新增 Bridge-Level Ring Structure 小节，固定 `type-theory / set theory / forcing / definability` 的 ring 分工
  - 新增 set-theory / forcing / definability 的负例与 near-miss 边界说明
  - 补充 MLO-FILL-01 bridge-level ring 结论，统一 benchmark 对图谱讲述层的支持口径
