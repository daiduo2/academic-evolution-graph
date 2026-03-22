doc_type: "project_positioning"
scope: "historical topic evolution graph methodology"
status: "draft"
owner: "trend-monitor"
source_of_truth: false
upstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/README.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-19-math-knowledge-graph.md"
downstream_docs: []
last_reviewed: "2026-03-19"
---

# Historical Topic Evolution Graph: 方法定位说明

## Why This Document Exists

随着项目推进，我们逐渐发现，这套工作已经不只是“Academic Trend Monitor 的一个附属分析模块”，而是在形成一套相对独立的方法论：

- 如何从跨时间 topic 对齐中恢复研究主题的历史演化结构
- 如何区分确认关系、推断关系与待审查关系
- 如何把 benchmark、case replay 和 graph structure 组合成一个可审计的知识表达层

这意味着，它未来有机会从当前项目中抽离出来，成为一个独立的子项目或方法框架。

本文件的目的，是把这套方法的定位讲清楚，避免后续我们把它误解成：

- 只是多做了一套 benchmark 文档
- 或只是一个普通的 topic graph 可视化

## One-Sentence Positioning

这套方法可以被概括为：

**一个面向历史主题演化的、带证据分级的知识图谱构建框架。**

它的核心不是“发现尽可能多的关系”，而是：

**用结构化证据去约束哪些关系可以被写进图谱，以及这些关系的强度应该如何被表达。**

## The Core Problem It Solves

普通的 topic analysis 通常能回答的问题是：

- 哪些关键词一起出现
- 哪些 topic 在某个时间段更热
- 哪些主题之间有相似性或邻接关系

但它难以稳定回答下面这些问题：

- 一个 topic 是否真的沿着时间演化成了另一个 topic
- 某条研究线是对象连续性，还是方法迁移
- 一个新方向是内部延续、外溢、融合，还是跨子域桥接
- 哪些关系已经足够可信，哪些仍只是候选推断

在数学这样的高抽象学科中，这个问题尤其突出，因为：

- 词相似不等于知识对象相同
- 结构相邻不等于研究脉络连续
- 方法共享不等于对象迁移
- 一个边画错了，解释代价往往很高

所以，这套方法要解决的不是“如何把更多边连出来”，而是：

**如何把‘主题如何演化’表达成带证据等级的结构化知识。**

## Method Principle

这套方法目前依赖四个连续层次。

### 1. Topic Alignment

先把不同月份的局部 topic 对齐成全局 topic。

这里解决的是：

- 同一知识线索能否跨时间被识别
- topic 是否具有 multi-period history
- topic 在层级结构中的主路径是什么

没有这一步，就没有“历史演化”，只有“分月热点快照”。

### 2. Evolution Replay

然后不是只看 topic 是否存在，而是回放它的历史变化。

这一步关心的是：

- 它与哪些 topic 邻接
- 它朝哪些方向扩散
- 是否发生桥接、分化、融合、迁移
- 它的对象和方法层到底发生了什么变化

这部分目前依赖：

- `topic_graph.json`
- `evolution_cases.json`
- `evolution_case_detail/*`

### 3. Evidence Layering

这是整个方法最关键的部分。

不是所有 graph edge 都能直接进入知识图谱。

我们需要明确区分：

- `confirmed`
  - 已经被 benchmark 或 curated cases 验证
- `inferred`
  - 来自 graph / export / metadata 的推断
- `ambiguous`
  - 有候选关系，但边界不稳
- `unavailable`
  - 数据不足或当前子域未纳入

这一步的作用，是把“图结构”提升为“知识结构”。

### 4. Benchmark Constraint

benchmark 在这里不是单纯的评测工具，而是认识论约束。

它强迫我们持续区分：

- event-level vs bridge-level
- object continuity vs method continuity
- exported case vs inferred candidate
- ready vs provisional vs gap

如果没有 benchmark 约束，图谱很容易退化为一张“看起来合理”的连线图。

## Philosophical Position

这套方法更接近一种**高解释性、强约束**的知识构建路线。

如果借一个粗略的哲学比喻，它更像偏“唯理论”的图谱构建：

- 先定义对象
- 再定义关系
- 再定义证据等级
- 再决定哪些边可以进入图谱

这与很多更“经验主义 / 统计主义”的知识图谱路线不同。后者通常更强调：

- 大规模共现或相关性
- embedding / similarity
- 弱监督关系发现
- 让统计结构自己浮现

## Why This Is Not Anti-Statistics

重要的是，这套方法**并不是反统计学**，也不是反“大模型 / scaling law”。

更准确的定位应该是：

**它是在统计发现之上，加了一层 evidence-aware 的知识约束。**

也就是说：

- 候选关系的提出，可以是偏经验主义的
- 关系是否进入图谱核心层，则需要更强的证据分级

这样，我们既不放弃统计发现的扩展能力，也不放弃高解释性和可审计性。

换句话说：

> 候选关系可以来自经验主义；确认关系则需要更严格的约束。

## What Makes It Potentially Independent

如果把它当作一个独立子项目，它真正独立的，不是“给数学做图谱”本身，而是：

### 1. 它有自己的问题定义

问题不是“怎么做 topic graph”，而是：

**怎么构建一个带证据层级的历史主题演化图谱。**

### 2. 它有自己的输入-输出结构

输入：

- aligned topics
- temporal graph
- replay cases
- benchmark evidence

输出：

- evidence-aware evolution graph

### 3. 它有自己的评估思路

不是只看 coverage，而是看：

- confirmed / inferred / ambiguous 是否区分清楚
- 关系是否可追溯
- benchmark 是否能约束图谱叙述

### 4. 它有潜在的跨领域迁移性

今天它先服务数学，但方法本身理论上可以迁移到：

- 物理
- CS 子方向
- 更广义的学术语料演化分析

## What It Is Not

为了防止后续定位漂移，也需要明确它不是什么。

它不是：

- 通用的图数据库产品
- 纯统计意义上的大规模关系发现系统
- “自动把一切 topic 都连起来”的知识抽取器
- 不需要人工审计的全自动学术图谱引擎

它更像是：

- 一个中间层
- 一个知识表达框架
- 一个对统计发现结果做证据分级和约束的系统

## Why It Matters For This Repository

即使它未来不拆出去，明确这层定位也很重要，因为它会反过来影响当前仓库里的优先级：

- benchmark 不再是最终目标，而是图谱的验证层
- 子域扩张不再只是“多做几个 benchmark”，而是为了扩充可信图谱核心
- `LO + AG + PR(provisional)` 之所以重要，不是因为它们只是先做完，而是因为它们能构成图谱 v1 的核心子图

这能帮助我们避免一个常见陷阱：

**为了 benchmark 而 benchmark，而忘了最终目标是知识图谱。**

## Proposed Future Framing

如果未来要把它作为独立子项目来描述，我建议用下面这个方向：

### English

`An evidence-aware framework for constructing historical topic evolution graphs`

### Chinese

`一个面向历史主题演化的带证据分级的知识图谱构建框架`

这个表述比“另一个知识图谱系统”更准确，也更能体现它和纯统计路线的区别。

## Current Working Thesis

到目前为止，我认为这套方法最准确的工作性表述是：

> 我们不是在和统计式知识图谱竞争谁更“真”；我们是在为主题演化分析构造一个可审计、可分级、可积累的知识表达层。

如果这个判断成立，那么它就不只是当前项目里的一个技术细节，而是一个值得独立维护的方法子系统。

