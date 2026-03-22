---
doc_type: "frontend_demo_note"
scope: "math knowledge graph demo v1 framing"
status: "active"
owner: "codex-worker"
package_id: "MATH-DEMO-04"
last_reviewed: "2026-03-22"
---

# Math Demo v1

## Default Demo

- 默认 `/knowledge-graph` 只读取 `data/output/kg_v1_visualization/`。
- 默认 demo baseline 仍然是 `math.LO + math.AG`。
- 默认页面的 framing 必须明确：这是当前稳定层，不代表数学全域都已确认完成。

## Preview Layer

- 只有在 `/knowledge-graph?pr_preview=1` 时才读取 `data/output/kg_v1_pr_conditional_visualization/`。
- `math.PR` 在页面中被表达为 `Research Preview / conditional layer`，不是 baseline truth。
- preview 的视觉语言与文案都需要区分：
  - 顶部 badge 和 framing 使用 preview 口径
  - preset 中单列 `Research Preview`
  - 帮助文案明确说明紫色关系表示条件层
  - TopicDetail 中把相关关系标为 `Inferred` / `Conditional`

## Productization Work

- 页面级 framing：
  - 新增 baseline 说明卡，明确当前稳定层是 LO + AG
  - 新增 preview 增量说明卡，解释 PR 只是在研究层出现
- demo 入口：
  - 新增 `Demo 导览`
  - 新增 `稳定基线`
  - 在 preview 模式下新增 `Research Preview`
- filters / legend / helper copy：
  - 让默认读者不需要先理解内部包名也能读懂 baseline、preview、结构背景、待复核
  - 修正子类别 preset 过滤逻辑，确保 preset 真正生效
- TopicDetail：
  - 增加“这个主题是什么”“为什么它值得讲”
  - 增加 `Confirmed / Inferred / Conditional / Review Required` 状态徽标
  - 让 edge 列表显示主题名、关系含义和 baseline / preview 身份

## MATH-DEMO-02 Refinements

- 默认 demo 入口继续保持 baseline-safe，但增强“先看什么 / 怎么看”的 first-glance guidance：
  - 顶部 summary 区直接写清观看顺序
  - Demo 入口区域明确推荐从 `Demo 导览` 开始
  - preset 增加 `推荐起点 / 默认入口 / Preview only` 标签
- `?pr_preview=1` 继续保持 preview-only data source，但默认讲述入口回到 `Demo 导览`：
  - 页面级 badge 明确当前是 `Preview Bundle Active`
  - 文案明确 `默认 baseline 未变更`
  - `Research Preview` 继续保留为独立 preset，用于只看 PR conditional layer
- TopicDetail 进一步产品化为“讲述卡”而不是字段卡：
  - 新增 `30 秒讲法`
  - 单独拆出 `状态说明`
  - 单独拆出 `关系怎么讲`
  - 强化“为什么这个 topic 值得看”的 demo 口径
- 图内提示和图例同步更新：
  - 图内增加轻量观看提示
  - 图例把紫色明确标为 `preview 候选`

## MATH-DEMO-03 Stabilization

- 继续保持 demo baseline-safe / preview-safe，但开始控制页面初始负担：
  - 时间轴改为页面稳定后再请求与渲染
  - 右侧完整 `TopicDetail` 改为按需 lazy load
  - 页面级 route 改为 lazy split，避免把知识图谱和其他重视图一起打进入口包
  - 首屏默认只保留最必要的 framing、preset 入口和 graph/detail 主区
- 收轻第一次打开的认知负担：
  - 把重复的 first-glance guidance 压缩成更短的推荐顺序 + 两条轻提示
  - 去掉选中后额外的页面级 context strip，避免和图内 / 右侧卡片重复
  - 底部帮助区继续保留，但减少重复文案
- 提升 graph/detail 协同感：
  - 选中节点后，图内持续提亮直连关系并压暗无关节点
  - 选中节点时尽量保持布局稳定，避免因为 selection 导致图明显跳动
  - TopicDetail 顶部增加更直接的主状态标签和 `图中已聚焦` 呼应
- Intentionally still not done:
  - 不引入新的全站级性能重构
  - 不把 PR preview 变成默认 baseline
  - 不恢复 preview-only 视角下被隐藏的 timeline

## MATH-DEMO-04 Pages Readiness

- 当前 math knowledge graph demo 可以直接挂在 GitHub Pages repo path 下：
  - Vite `base` 固定为 `/academic-trend-monitor/`
  - router basename 与 `import.meta.env.BASE_URL` 对齐
  - knowledge graph、topics、weekly、recent 等静态 fetch 都走 `BASE_URL`
- 当前部署模式是纯静态站：
  - 页面依赖 `data/output/kg_v1_visualization/` 与 `data/output/kg_v1_pr_conditional_visualization/` 等静态 JSON bundle
  - 不需要运行时后端，也不依赖动态 API
- `make deploy` 现已同步 baseline / preview 两套知识图谱 bundle，保证本地 Pages-ready 构建可复现。
- 当前已知限制：
  - GitHub Actions deploy workflow 也需要保持相同的 bundle 同步清单，否则 `?pr_preview=1` 可能在 Pages 上缺少 preview 数据
  - 站点仍然依赖构建前本地已有最新静态 JSON 数据

## Intentionally Not Done

- 没有修改 `pipeline/`
- 没有把 `math.PR` 并入默认 baseline
- 没有改动 graph layout 算法
- 没有重写全站信息架构或设计系统
- 没有把这轮扩大到其他领域 demo
