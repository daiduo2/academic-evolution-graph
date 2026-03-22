# Academic Evolution Graph

面向数学主题演化分析的独立仓库。这个项目从 `academic-trend-monitor` 中抽离出来，专注于两件事：

1. 用 benchmark / review / rule 的方式整理数学子域的历史主题演化证据。
2. 把这些证据导出成一个可静态部署的知识图谱前端。

项目没有运行时后端，前端直接读取静态 JSON bundle，并可部署到 GitHub Pages。

## 当前范围

当前知识图谱的默认基线是：

- `math.LO`
- `math.AG`

同时仓库已经具备面向下列子域的扩展能力：

- `math.CO`
- `math.DS`
- `math.NA`
- `math.PR`（preview only）

`math.QA / math.RA` 目前仍保持 gap / excluded 状态，不会被默认展示成结论层。

## 仓库结构

```text
academic-evolution-graph/
├── config/                 # 配置与 prompts
├── data/output/            # 对齐主题、KG、visualization bundle
├── docs/plans/             # evolution docs / benchmark / review / package docs
├── frontend/               # 静态知识图谱前端
├── pipeline/               # evolution / KG export / benchmark scripts
├── tests/                  # Python tests
├── Makefile
└── requirements.txt
```

## 常用命令

```bash
make install
make frontend-install
make evolution-analysis
make math-benchmark
make kg-export
make kg-visualization
make test
make deploy
```

## 本地预览

```bash
cd frontend
npm install
npm run build
npm run preview
```

默认访问：

- `http://127.0.0.1:4173/academic-evolution-graph/`
- `http://127.0.0.1:4173/academic-evolution-graph/knowledge-graph`

## GitHub Pages

本仓库默认按 GitHub Pages 静态站部署：

- `frontend/vite.config.js` 使用 `/academic-evolution-graph/` 作为 `base`
- `frontend/src/main.jsx` 根据 `BASE_URL` 推导 router basename
- deploy workflow 会把 `data/output/` 中的 KG bundle 拷贝到 `frontend/public/data/output/`

## 当前方法定位

这不是一个“普通热点图表项目”。它的核心目标是：

- 区分 confirmed / bridge / boundary / review
- 用 benchmark 约束主题演化叙述
- 逐步把数学子域积累成可信的历史演化知识图谱

当前最重要的实现层包括：

- `pipeline/evolution_analysis.py`
- `pipeline/math_kg_export.py`
- `pipeline/math_kg_visualization_export.py`
- `frontend/src/views/KnowledgeGraph.jsx`

## 备注

- 本仓库是演化分析独立线，后续可单独部署、提交和配置 CI/CD。
- 主项目 `academic-trend-monitor` 仍可按需要保留一版集成入口，但这里将作为后续演化分析的主战场。
  自动生成的历史演化分析报告。
- `data/recent.jsonl`
  最近论文的压缩格式索引。
- `data/weekly/*.json`
  滚动 7 天趋势报告。

## 环境准备

### 1. Python 依赖

```bash
make install
```

### 2. 前端依赖

```bash
make frontend-install
```

### 3. LLM 配置

项目默认读取环境变量中的 `LLM_API_KEY`：

```bash
export LLM_API_KEY=your_deepseek_key
```

LLM 与主题建模相关参数见 [`config/settings.yaml`](config/settings.yaml)。

### 4. 原始数据

把原始 arXiv 月度 JSONL 放到 `data/raw/`，文件名应为 `YYYY-MM.jsonl`。

示例：

```bash
cp /path/to/arxiv-trend-monitor/data/raw/*.jsonl data/raw/
```

## 快速开始

### 运行完整月度流水线

```bash
make pipeline
```

这个命令按顺序执行：

1. `pipeline/01_bertopic.py`
2. `pipeline/02_hierarchy.py`
3. `pipeline/03_alignment.py`

输出写入 `data/output/`。

### 启动本地前端

```bash
cd frontend
npm run dev
```

默认 Vite 路径基于 GitHub Pages 子路径配置，开发时访问形如：

```text
http://127.0.0.1:4173/academic-trend-monitor/
```

### 构建前端

```bash
cd frontend
npm run build
```

### 部署

```bash
make deploy
```

`make deploy` 会先把 `data/output/*.json` 复制到 `frontend/public/data/`，再执行前端构建。静态资源推送后可由 GitHub Pages 发布。

## 日更 / 周更工作流

### 日更：抓取并打标最近论文

```bash
python pipeline/daily_update.py
```

内部步骤：

1. 从 arXiv 抓取最近论文
2. 使用 topic index 打标签
3. 写入 `data/recent.jsonl`

### 周更：生成滚动 7 天趋势报告

```bash
python pipeline/weekly_trend.py
```

输出格式为：

```text
data/weekly/YYYY-MM-DD.json
```

### 主题索引构建

如果要支持日更打标，需要先有 topic index：

```bash
python pipeline/build_topic_index.py
```

### 历史主题演化分析

基于过去月份回放主题扩散、分化、收敛和跨领域迁移，不依赖最新月份。
当前版本会额外输出 `topic_mode` 和 `topic_profile`（`method` / `problem` / `hybrid` / `theory` 的主次标签与分数），并结合层级路径和邻域做轻量校正，用于解释层区分方法热点与问题热点。
演化分析文档现在按固定骨架维护：

- 顶层标准：[docs/plans/2026-03-11-evolution-doc-standards.md](docs/plans/2026-03-11-evolution-doc-standards.md)
- 规则总表：[docs/plans/2026-03-10-evolution-rule-coverage.md](docs/plans/2026-03-10-evolution-rule-coverage.md)
- `math.LO` 子域评审：[docs/plans/2026-03-11-math-lo-rule-review.md](docs/plans/2026-03-11-math-lo-rule-review.md)
- `math.LO` benchmark：[docs/plans/2026-03-12-math-lo-benchmark.md](docs/plans/2026-03-12-math-lo-benchmark.md)
- 弱模型执行手册：[docs/plans/2026-03-12-evolution-worker-playbook.md](docs/plans/2026-03-12-evolution-worker-playbook.md)
- 规则迭代任务模板：[docs/plans/2026-03-12-evolution-task-template.md](docs/plans/2026-03-12-evolution-task-template.md)
- 弱模型 / subagent 单页 prompt：[docs/plans/2026-03-12-evolution-worker-prompt.md](docs/plans/2026-03-12-evolution-worker-prompt.md)
- subagent 委派 SOP：[docs/plans/2026-03-12-subagent-delegation-sop.md](docs/plans/2026-03-12-subagent-delegation-sop.md)
- skills / plugin 设计稿：[docs/plans/2026-03-12-evolution-skills-design.md](docs/plans/2026-03-12-evolution-skills-design.md)
- 数学任务包 backlog：[docs/plans/2026-03-12-math-worker-backlog.md](docs/plans/2026-03-12-math-worker-backlog.md)
- Claude / subagent 操作文档索引：[docs/plans/evolution-ops/README.md](docs/plans/evolution-ops/README.md)
- 通用 benchmark runner 实现包：[docs/plans/evolution-ops/06-generic-runner-implementation-packages.md](docs/plans/evolution-ops/06-generic-runner-implementation-packages.md)
- benchmark 数据基线策略：[docs/plans/evolution-ops/07-benchmark-data-policy.md](docs/plans/evolution-ops/07-benchmark-data-policy.md)
新增规则时，需要先按该文档中的“规则登记模板”登记，再更新覆盖表。
事件详情中的 `diffused_to_neighbor` / `merged_into_parent` / `migrated_to_new_category` 会带方向性证据、分型字段，以及 `transfer_pattern` / `bridge_evidence`，用于说明这是迁移、融合还是外溢，并给出共享关键词、桥接主题、目标证据标题、`category_flow`、`pipeline_relation`、`evidence_title_overlap`、`bridge_strength` 和 `alias_risk`。高风险别名目标会在事件抽取阶段被跳过，避免把“中英文别名/重命名”误判成扩散。现在还会同时输出 target 与 anchor 两侧的后续持续性，以及 `relative_persistence`，并新增 `consistency_check` / `review_flags`，用来标记“同域高桥接但弱承接”这类需要人工复核的矛盾案例；对于“成像/测量 -> 分割/诊断/分析”“表示/渲染 -> 感知/重建”，以及数学/理论方向里“共享形式结构对象”的自然演进，会通过 `pipeline_relation` 降低误判。

`math.LO` benchmark 现在也有可执行检查入口：

```bash
make math-lo-benchmark
```

输出会写到：

- `data/output/benchmarks/math_lo/math_lo_benchmark.json`
- `data/output/benchmarks/math_lo/math_lo_benchmark.md`

```bash
make evolution-analysis
```

或者：

```bash
python3 pipeline/evolution_analysis.py --horizon 4 --max-cases 12
```

手动指定案例主题：

```bash
python3 pipeline/evolution_analysis.py --anchor-topics global_3,global_128
```

## 前端页面说明

### 领域热度分析

- 入口：`/`
- 作用：按学科 / 子类浏览主题树
- 特性：支持 Layer 3/4 drill-down、面包屑、详情弹窗

### 趋势追踪分析

- 入口：`/trends`
- 作用：查看单个全局 topic 或聚合主题的历史趋势
- 特性：支持从领域视图直接跳转并恢复上下文

### RSS 订阅

- 入口：`/rss`
- 作用：按 topic tag 过滤最近论文并生成本地可下载 feed
- 特性：支持从 URL 恢复订阅参数、展示滚动趋势摘要

## 常用命令

| 命令 | 说明 |
| --- | --- |
| `make install` | 安装 Python 依赖 |
| `make frontend-install` | 安装前端依赖 |
| `make test` | 运行 Python 测试 |
| `make pipeline` | 运行月度数据流水线 |
| `make evolution-analysis` | 运行历史主题演化分析 |
| `make deploy` | 构建前端并准备部署 |
| `make clean` | 清理生成物 |
| `cd frontend && npm test` | 运行前端测试 |
| `cd frontend && npm run build` | 构建前端 |

## 配置说明

核心配置文件：

- [`config/settings.yaml`](config/settings.yaml)
  包含 arXiv 分类、BERTopic、LLM、流水线参数。
- `config/prompts.yaml`
  包含层级构建与语义对齐相关 prompt。

其中比较关键的配置项：

- `topic_modeling.min_topic_size`
- `topic_modeling.embedding_model`
- `llm.provider`
- `llm.model`
- `pipeline.alignment.similarity_threshold`

## 测试与校验

### Python

```bash
make test
```

### Frontend

```bash
cd frontend
npm test
```

### 推荐的提交前检查

```bash
make test
cd frontend && npm test
cd frontend && npm run build
```

## 已知约束

- 项目当前依赖静态文件分发，不提供在线后端 API。
- 日更抓取依赖本地 Python 环境与外部网络可用性。
- `arxiv` / `requests` 在某些 macOS Python 环境下会出现 LibreSSL 兼容告警；当前代码会输出详细错误日志并在失败时返回空结果，避免污染 daily pipeline。
- 前端构建产物较大，Vite 可能提示 chunk size warning，但不影响功能。

## 文档与设计记录

如果你要理解这个项目为什么会长成现在这样，优先看这些文档：

- [`docs/plans/2026-03-04-design.md`](docs/plans/2026-03-04-design.md)
- [`docs/plans/2026-03-06-drill-down-dashboard-design.md`](docs/plans/2026-03-06-drill-down-dashboard-design.md)
- [`docs/plans/2026-03-07-multi-timeframe-trend-rss-design.md`](docs/plans/2026-03-07-multi-timeframe-trend-rss-design.md)
- [`docs/plans/2026-03-11-evolution-doc-standards.md`](docs/plans/2026-03-11-evolution-doc-standards.md)
- [`docs/plans/2026-03-10-evolution-rule-coverage.md`](docs/plans/2026-03-10-evolution-rule-coverage.md)
- [`docs/plans/2026-03-11-math-lo-rule-review.md`](docs/plans/2026-03-11-math-lo-rule-review.md)
- [`docs/plans/2026-03-12-math-lo-benchmark.md`](docs/plans/2026-03-12-math-lo-benchmark.md)
- [`docs/plans/2026-03-12-evolution-worker-playbook.md`](docs/plans/2026-03-12-evolution-worker-playbook.md)
- [`docs/plans/2026-03-12-evolution-task-template.md`](docs/plans/2026-03-12-evolution-task-template.md)
- [`docs/plans/2026-03-12-evolution-worker-prompt.md`](docs/plans/2026-03-12-evolution-worker-prompt.md)
- [`docs/plans/2026-03-12-subagent-delegation-sop.md`](docs/plans/2026-03-12-subagent-delegation-sop.md)
- [`docs/plans/2026-03-12-evolution-skills-design.md`](docs/plans/2026-03-12-evolution-skills-design.md)
- [`docs/plans/2026-03-12-math-worker-backlog.md`](docs/plans/2026-03-12-math-worker-backlog.md)
- [`docs/plans/evolution-ops/README.md`](docs/plans/evolution-ops/README.md)
- [`docs/plans/evolution-ops/06-generic-runner-implementation-packages.md`](docs/plans/evolution-ops/06-generic-runner-implementation-packages.md)

## License

MIT
