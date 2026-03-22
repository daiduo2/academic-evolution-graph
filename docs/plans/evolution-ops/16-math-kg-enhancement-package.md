---
doc_type: "enhancement_package"
package_id: "KG-05"
status: "completed"
date: "2026-03-20"
owner: "frontend-worker"
baseline: "KG-04-fix"
---

# KG-05: Math Knowledge Graph Enhancement Package

## Overview

KG-05 is a frontend-only enhancement pass applied to the Math Knowledge Graph `/knowledge-graph` page. It builds directly on the KG-04-fix stable baseline and focuses on three goals: (1) making the graph more explorable through richer interactions, (2) making the evidence model more legible in the detail panel, and (3) improving the overall visual language so the page is suitable for a first external demonstration without requiring any data or backend changes.

All enhancements are scoped to five React components. No pipeline files, no backend, no Neo4j, no new exporters, and no data schema changes are involved.

## Baseline

- Built on: **KG-04-fix** (filter normalization + useSubcategory fix + TimelineSummary mount)
- Data source: **KG-03 visualization bundle** (`graph_bundle.json` + `timeline_summary.json`) — unchanged
- Topic scope: **LO + AG confirmed baseline only** — math.PR is not introduced
- Exporter scope: KG-02 and KG-03 exporters are not touched

## Enhancements

### GraphVisualization.jsx

- **Hover highlight with neighbor dimming**: When hovering over a node, the hovered node and its direct neighbors are highlighted at full opacity; all other nodes and edges are dimmed. This makes it immediately clear what a node is connected to without clicking.
- **Arrow markers on EVOLVES_TO edges**: Directed arrow markers are rendered at the target end of `EVOLVES_TO` edges, making the direction of evolution relationships visually unambiguous.
- **Selection ring for selected node**: A distinct outer ring is drawn around the currently selected node, distinguishing it from hover state and idle state at a glance.
- **Reset-view button**: A button is added to restore the graph to its initial zoom level and pan position, allowing users to recover from deep zoom or drift without reloading the page.
- **Better legend**: The legend now accurately reflects the visual language used in the graph (node colors by subcategory, edge styles by type, arrow marker for EVOLVES_TO, ring for selection).

### TopicDetail.jsx

- **Edge type badges with colors**: Each edge in the detail panel now shows a colored badge indicating its type (`EVOLVES_TO`, `NEIGHBOR_OF`, etc.), making the edge type scannable without reading label text.
- **Confidence indicators**: Confidence levels are displayed with a visual indicator (e.g., color or icon) alongside the text label, giving a quick signal of evidence strength.
- **Priority sorting — EVOLVES_TO confirmed first**: Edges are sorted so that confirmed `EVOLVES_TO` edges appear at the top, followed by other confirmed edges, then unconfirmed. This surfaces the most analytically important relationships immediately.
- **Evidence summary stats**: A compact summary row at the top of the edge list shows total edge count broken down by type (e.g., "3 EVOLVES_TO · 5 NEIGHBOR_OF"), giving orientation before reading individual edges.
- **Benchmark evidence indicator**: Edges that are backed by benchmark evidence carry a distinct visual marker, allowing users to distinguish data-derived relationships from benchmark-confirmed ones.
- **Better empty state**: When a topic has no edges matching the current filters, a descriptive empty state is shown rather than a blank panel.
- **Expanded edge display limit**: The edge limit in the detail panel is raised from 5 to 8, reducing the need to scroll or paginate on typical topics.

### GraphFilters.jsx

- **Active filter summary badge**: When filters are active, a badge shows a compact summary of what is currently applied (e.g., "2 filters active"), so users always know the graph is filtered.
- **One-click preset buttons**: Three preset buttons are added for common filter configurations:
  - "只看演化边" — show only EVOLVES_TO edges
  - "仅已确认关系" — show only confirmed relationships
  - "全部显示" — reset all filters to show everything
- **Edge kind count indicator**: Each edge-kind filter option shows a count of how many edges of that kind exist in the current graph, helping users understand the composition before filtering.
- **Smarter reset button**: The reset button is only active when filters differ from the default state, and it resets to "全部显示" rather than to an arbitrary default.

### TimelineSummary.jsx

- **Trend analysis insight text**: A text summary is rendered above or below the chart describing the dominant trend observed in the period data (e.g., which period had the most activity, or whether activity is growing/declining).
- **Better labels in Chinese**: All axis labels, tooltips, and legend items are localized to Chinese to align with the target audience.
- **Tooltip formatters**: Custom tooltip formatters ensure the chart tooltips show period names and topic counts in a readable format rather than raw values.
- **Period range in stats**: The stats section now includes the date range covered by the visible periods, giving context for how wide the timeline window is.

### KnowledgeGraph.jsx (page)

- **Baseline badge (LO + AG · v1)**: A persistent badge in the page header displays "LO + AG · v1", communicating to viewers exactly what data scope the graph represents.
- **Selection context strip**: When a topic node is selected, a slim strip below the graph header shows the selected topic's name and subcategory, providing persistent context even when the user has scrolled down to the detail panel.
- **Section dividers**: Visual dividers separate the graph section, the detail panel section, and the timeline section, improving the overall layout hierarchy.
- **Improved help text with visual language guide**: The help/guide text is updated to describe the specific visual language used in this version: node colors, edge arrow markers, selection ring, and filter presets.

## Non-Goals (Strict Scope Constraints)

The following were explicitly not done in KG-05:

- No introduction of math.PR data into the graph bundle or visualization
- No changes to the KG-03 bundle schema (`graph_bundle.json`, `timeline_summary.json`)
- No changes to `pipeline/math_kg_export.py` or `pipeline/math_kg_visualization_export.py`
- No changes to KG-02 or KG-03 test files
- No new backend API endpoints
- No Neo4j integration
- No full frontend architecture rewrite (all changes are scoped to the five listed components)
- No addition of math.QA, math.RA, or math.RT data
- No synthetic data

## Usage Scenario

After KG-05, the `/knowledge-graph` page is suitable for a **first external demonstration** to an audience who wants to understand how mathematical topics evolve over time. A typical session looks like:

1. The viewer lands on the page and immediately sees the "LO + AG · v1" badge, anchoring expectations about scope.
2. They use the "只看演化边" preset to isolate the directed evolution relationships.
3. They hover over a node to see its neighbors highlighted, then click to select it.
4. The selection ring and context strip keep the selected topic visible as they scroll down to the detail panel.
5. In the detail panel, they see benchmark-confirmed EVOLVES_TO edges listed first with evidence indicators.
6. They scroll to the timeline to read the trend insight text and understand which periods had the most activity.
7. They use the reset-view button to return to the full graph before exploring a different topic.

The page does not require any backend or database connection — all data is served from the static KG-03 bundle.

## Answers to Required Questions

**1. KG-05 相比 KG-04，最大的 3 个体验提升是什么？**

- **图探索可读性**: Hover 高亮 + 邻居 dimming 让用户在密集图中能立刻看清一个节点的直接连接，无需点击。
- **证据可见性**: 详情面板中的 benchmark evidence 指示器、边类型徽章和优先排序（EVOLVES_TO confirmed 置顶）让分析价值的核心信息直接可读，而不是埋在平铺列表里。
- **页面范围自说明**: Baseline badge "LO + AG · v1" 和更新后的帮助文字让页面本身解释自己的数据范围，不需要外部说明文档。

**2. graph exploration 现在新增了哪些交互？**

- Hover 高亮（节点 + 邻居亮起，其余 dim）
- EVOLVES_TO 边的方向箭头标记
- 已选节点的 selection ring
- Reset-view 按钮（恢复初始缩放/平移）
- 过滤器预设按钮（三个一键预设）
- Active filter summary badge（实时显示当前过滤状态）

**3. detail panel 现在比之前多了什么分析价值？**

- 边类型彩色徽章（边类型可扫描）
- 置信度视觉指示器（证据强度一目了然）
- EVOLVES_TO confirmed 优先排序（最重要关系置顶）
- 边类型分布摘要行（选中节点的关系概况）
- Benchmark evidence 标记（区分数据推断 vs benchmark 确认）
- 展示上限从 5 提升到 8（减少截断）

**4. timeline 和 graph 的关系现在是如何表达的？**

Timeline 通过趋势分析文字与图谱形成叙事连接：图谱显示"谁演化了谁"，timeline 显示"演化活动在哪些时期最密集"。Period range 显示覆盖的日期范围，让用户在读图谱时能将节点的时间属性对应到 timeline 的坐标系里。两者共享同一份 KG-03 bundle 数据，因此 timeline 的 period 与图谱节点的 active_periods 是一致的。

**5. 页面是否仍严格限定在 LO + AG baseline？**

是。KG-05 没有引入 math.PR、math.QA、math.RA 或任何其他子域的数据。Bundle schema 未改变，LO + AG · v1 badge 明确传达了这个限定。

**6. 前端测试和构建是否通过？**

已验证。KG-05-fix 修复后实际运行结果：

- 测试命令：`npm --prefix frontend run test`
  结果：4/4 pass（2 test files, 4 tests, vitest v3.2.4）
- 构建命令：`npm --prefix frontend run build`
  结果：vite build success（1103 modules transformed，built in 1.44s）

**7. 现在这个页面是否已经足够支持"第一版对外演示"？**

是。具备：范围自说明（baseline badge）、视觉语言清晰（方向箭头、ring、dimming）、证据层次可读（徽章 + 排序 + 指示器）、交互足够友好（preset 按钮、reset view、context strip）。数据来自静态 bundle，无网络依赖。

**8. 下一步更适合：MPR-01C 还是 KG-06？**

推荐 **MPR-01C**。理由见下方 Recommendation 章节。

## Recommendation

**推荐下一步：MPR-01C（Math.PR PR-targeted candidate extraction）**

KG-05 完成后，/knowledge-graph 页面已具备第一版对外演示能力，LO + AG baseline 的前端体验完整。继续在前端上叠加功能（KG-06）的边际收益此时低于扩展数据范围的价值。

MPR-01C 是解锁 math.PR 数据进入 KG baseline 的必要前置步骤：它执行 PR-specific candidate extraction，为后续的 MPR-02 curation 提供足够的 explicit cases。一旦 math.PR 通过 curation 进入 baseline，KG-04/KG-05 的前端已经能够直接承载新数据——因为 graph_bundle.json 只需重新导出，前端无需改动。

如果 math.PR 探索阶段仍不满足解锁条件（参见 PKG-PR-01B 的 decision），则可转向 KG-06 来进一步完善前端体验（例如：路径查找、全局 timeline 过滤联动、节点搜索）。
