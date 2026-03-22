<!-- docs/geb/api/data-format.md -->
@geb-leaf #api-data-format
@mirror ./data/output/final_topics.json
@loop #architecture
@loop #topic-hierarchy
@invariant "Schema matches actual output"
@invariant "All fields documented"
@emerge "update all refs on format change"
@reflect "on_data_change"

# 数据格式规范

## 输出文件

| 文件 | 路径 | 说明 |
|------|------|------|
| final_topics.json | `data/output/final_topics.json` | 主题数据 |
| timeline.json | `data/output/timeline.json` | 时间线数据 |
| topic_graph.json | `data/output/topic_graph.json` | 主题时间图 |
| evolution_cases.json | `data/output/evolution_cases.json` | 历史演化案例摘要 |

`topic_graph.json` 中的 topic 节点会额外包含 `topic_mode` 与 `topic_profile`，用于区分 `method` / `problem` / `hybrid` / `theory` 四类解释视角，并暴露主次标签分数；该 profile 会结合层级路径、邻域多数和 `representative_evidence` 做轻量校正。`evolution_cases.json` 中的案例也会同步暴露 anchor 的 `topic_mode` / `topic_profile`。事件详情中的 `diffused_to_neighbor` / `merged_into_parent` / `migrated_to_new_category` 会附带方向性 `evidence` 字段，以及分型值（如 `method_diffusion` / `problem_diffusion` / `method_transfer` / `problem_transfer`）、`transfer_pattern`（如 `migration` / `fusion` / `spillover`）、`bridge_evidence`，以及 target/anchor 两侧的 `post_transfer_persistence` / `anchor_post_event_persistence` 和 `relative_persistence`。其中 `bridge_evidence` 现在还会显式给出 `category_flow`、`pipeline_relation`、`evidence_title_overlap`、`bridge_strength` 和 `alias_risk`，用于在没有作者信息时提供降级版的桥接证据，并标记高风险别名连接。相关事件还会输出 `consistency_check`，案例摘要层则汇总为 `review_flags`，专门标记“同域高桥接但弱承接”这类需要人工复核的矛盾信号；若命中 `imaging_to_analysis_same_pipeline`、`representation_to_perception_same_pipeline` 或 `formal_structure_same_lineage`，则会将该事件标为 `pipeline_consistent`，避免把自然演进误判为跨域噪声、同域伪扩散，或数学/理论中的结构连续性演化。

## 主题数据结构

```typescript
interface TopicData {
  // 基础信息
  id: string;           // 唯一标识: "{category}-{year}-{month}-{seq}"
  name: string;         // 主题名称
  layer: number;        // 层级 (1-4+)

  // 层次关系
  parent_id: string | null;     // 父节点ID
  children_ids: string[];       // 子节点ID列表
  related_paths: string[];      // 跨学科关联

  // 统计信息
  paper_count: number;          // 论文数量
  keywords: string[];           // 关键词

  // 时间序列
  timeline: TimelinePoint[];    // 跨月数据

  // 元数据
  description?: string;         // LLM生成的描述
  sample_papers: Paper[];       // 示例论文
}

interface TimelinePoint {
  month: string;        // "YYYY-MM"
  paper_count: number;  // 该月论文数
  trend: 'up' | 'down' | 'stable';  // 趋势
}

interface Paper {
  id: string;           // arXiv ID
  title: string;        // 论文标题
  authors: string[];    // 作者列表
  abstract: string;     // 摘要
  url: string;          // arXiv URL
}
```

## 完整示例

```json
{
  "id": "cs.AI-2024-01-001",
  "name": "大语言模型对齐技术",
  "layer": 3,
  "parent_id": "cs.AI",
  "children_ids": ["cs.AI-2024-01-001-001", "cs.AI-2024-01-001-002"],
  "related_paths": ["cs.CL-2024-01-005", "cs.LG-2024-01-012"],
  "paper_count": 45,
  "keywords": ["RLHF", "指令微调", "安全对齐", "人类反馈"],
  "timeline": [
    {"month": "2024-01", "paper_count": 45, "trend": "up"},
    {"month": "2024-02", "paper_count": 52, "trend": "up"},
    {"month": "2024-03", "paper_count": 78, "trend": "up"}
  ],
  "description": "研究如何通过人类反馈强化学习(RLHF)等技术使大语言模型与人类意图对齐",
  "sample_papers": [
    {
      "id": "2401.12345",
      "title": "Advanced RLHF Techniques for LLM Alignment",
      "authors": ["Alice Smith", "Bob Jones"],
      "abstract": "We propose a novel approach to...",
      "url": "https://arxiv.org/abs/2401.12345"
    }
  ]
}
```

## 数据约束

1. **ID 格式**: `{category}-{year}-{month}-{sequence}`
2. **层级范围**: 1 <= layer <= 6 (实际通常 1-4)
3. **时间格式**: 严格 `YYYY-MM`
4. **关键词数量**: 3-10 个

## 前端消费

```typescript
// React Hook 示例
function useTopicData() {
  const [data, setData] = useState<TopicData[]>([]);

  useEffect(() => {
    fetch('/data/final_topics.json')
      .then(r => r.json())
      .then(setData);
  }, []);

  return data;
}
```

## 相关节点

- @geb-node #architecture - 架构总览
- @geb-leaf #topic-hierarchy - 层次结构模型
- @geb-node #frontend - 前端消费方式
