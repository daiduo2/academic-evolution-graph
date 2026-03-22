# Codex Handoff

## Repo Path

`/Users/daiduo2/Documents/Playground/codex/academic-evolution-graph`

## Repo Role

这是从 `academic-trend-monitor` 独立出来的数学主题演化知识图谱主仓。

当前重点不是热点监控，也不是 daily fetch，而是：

- 数学子域演化规则
- 知识图谱导出
- GitHub Pages 上的静态图谱前端

## Current Deployment

- GitHub repo:
  - `https://github.com/daiduo2/academic-evolution-graph`
- GitHub Pages:
  - `https://daiduo2.github.io/academic-evolution-graph/`

## Current Baseline

### Default baseline domains

- `math.LO`
- `math.AG`

### Non-baseline but already graph-visible

- `math.CO`
- `math.DS`

### Started but not yet graph-visible enough

- `math.NA`

### Preview-only / excluded

- `math.PR`
  - preview only
- `math.QA`
  - gap / excluded
- `math.RA`
  - gap / excluded

## Recent Important Commits

- `b52347a`
  - narrow standalone repo validation policy
- `550a197`
  - separate narrative subgraph clusters in frontend
- `7caf0e4`
  - thicken graph with CO and DS overlays
- `a539712`
  - rewrite README around knowledge-graph method and progress
- `dadc1f4`
  - update GitHub Pages workflow actions
- `eacc9ea`
  - initial standalone repo extraction

## What Is Already Working

### Frontend

- Knowledge graph page is the main product surface
- `LO` and `AG` remain the default baseline topology
- `CO` and `DS` are already surfaced as non-baseline narrative overlays
- Narrative subgraph visibility has been strengthened with cluster positioning

### Export / Data

- KG bundles are generated and committed for:
  - `kg_v1`
  - `kg_v1_pr_conditional`
  - `kg_v1_visualization`
  - `kg_v1_pr_conditional_visualization`
- Exporter already carries:
  - `domain_knowledge_layers`
  - `graph_band`
  - `graph_layer`
  - `graph_role`
  - `graph_export_status`

### Docs / Workflow

- This standalone repo no longer defaults to parent-repo-wide validation
- `make test` is **not** the default completion gate here
- `/geb-docs` is **not** part of the workflow here

## Validation Policy

Use the narrowest relevant validation:

### Evolution rule / benchmark work

```bash
pytest tests/test_evolution_analysis.py -q
```

### KG export / visualization export work

```bash
pytest tests/test_math_kg_visualization_export.py -q
```

### Frontend work

```bash
npm --prefix frontend run test -- --run
npm --prefix frontend run build
```

Do **not** default to `make test` unless the task explicitly touches raw-data ingestion or whole-repo integrity behavior.

## Current Main Bottleneck

当前瓶颈已经不主要是研究规则，而是：

1. 让更多子域真正进入 graph-visible layer
2. 让前端把这些 graph-visible layers 更清楚地表现出来

当前最适合继续推进的是：

- `math.NA`
  - 尽量从 implementation-ready 推到 graph-visible
- 新子域 bootstrap
  - 如 `math.RT`
  - 如 `math.NT`
- 前端可视化强调
  - 让非 baseline overlays 更明显，但不污染 baseline truth

## Recommended Next Work

如果新线程是为了继续推进主线，优先顺序建议：

1. `math.NA`
   - push toward graph-visible but non-baseline
2. bootstrap one new domain
   - `math.RT` or `math.NT`
3. frontend emphasis
   - only if overlays are still too subtle on Pages

## Files Most Likely To Matter

### Frontend

- `frontend/src/views/KnowledgeGraph.jsx`
- `frontend/src/components/GraphVisualization.jsx`
- `frontend/src/components/GraphFilters.jsx`
- `frontend/src/hooks/useKnowledgeGraph.js`

### Export

- `pipeline/math_kg_export.py`
- `pipeline/math_kg_visualization_export.py`
- `tests/test_math_kg_visualization_export.py`

### Rule engine

- `pipeline/evolution_analysis.py`
- `tests/test_evolution_analysis.py`

### Domain docs

- `docs/plans/2026-03-10-evolution-rule-coverage.md`
- `docs/plans/2026-03-19-math-knowledge-graph.md`
- `docs/plans/2026-04-03-math-na-benchmark.md`
- `docs/plans/2026-04-03-math-na-rule-review.md`

## Constraints

- Do not expand baseline truth casually
- Keep `LO + AG` as the default baseline unless there is explicit evidence and a deliberate product decision
- Keep `PR` preview-only
- Keep `QA / RA` excluded unless new evidence changes their state
- Always end completed rule / export / frontend iterations with a local git commit

## Fast Start Prompt

When opening a fresh Codex thread, start with:

> Work in `/Users/daiduo2/Documents/Playground/codex/academic-evolution-graph`. First read `AGENTS.md`, `README.md`, and `docs/plans/2026-03-22-codex-handoff.md`. This is the standalone math evolution graph repo. Default baseline is `LO + AG`; `CO + DS` are graph-visible non-baseline overlays; `NA` is the next domain to push forward. Use targeted validations only, not `make test`, unless the task explicitly touches raw-data ingestion.
