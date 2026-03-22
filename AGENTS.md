# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Project Overview

Academic Trend Monitor - 学术热点趋势分析仪表盘

基于 BERTopic + LLM 的学术研究热点分析工具，支持从时间切片和领域切片两个维度展示研究热点。

## Architecture

- **Data Pipeline**: Python scripts that run monthly to process arXiv data
- **Frontend**: React + D3.js static site deployed to GitHub Pages
- **Storage**: Static JSON files (no backend)

## Common Commands

```bash
# Install dependencies
make install

# Run data pipeline (monthly update)
make pipeline

# Deploy to GitHub Pages
make deploy

# Clean generated data
make clean
```

## Project Structure

```
├── data/
│   ├── raw/              # Raw arXiv data (JSONL files)
│   └── output/           # Generated topic data (JSON)
├── pipeline/             # Python data processing scripts
├── frontend/             # React + Vite frontend
├── config/               # Configuration files
└── docs/plans/           # Design documents
```

## Development Workflow

**CRITICAL**: Evolution-analysis documentation must follow the standard skeleton before further rule expansion.

1. **Documentation standard first**: Follow `docs/plans/2026-03-11-evolution-doc-standards.md`
2. **Worker constraints**: For repetitive or lower-confidence rule work, follow `docs/plans/2026-03-12-evolution-worker-playbook.md`
3. **Task template**: Use `docs/plans/2026-03-12-evolution-task-template.md` as the default iteration template for dirty work
4. **Worker prompt**: If delegating to a weaker model or Claude subagent, use `docs/plans/2026-03-12-evolution-worker-prompt.md`
5. **Subagent SOP**: If you are delegating work, use `docs/plans/2026-03-12-subagent-delegation-sop.md`
6. **Skills design**: If you are preparing slash-command based delegation, follow `docs/plans/2026-03-12-evolution-skills-design.md`
7. **Math task backlog**: For math dirty work, prefer dispatching packages from `docs/plans/2026-03-12-math-worker-backlog.md`
8. **Ops docs first**: If you are Claude or a weaker subagent working on evolution-analysis, read `docs/plans/evolution-ops/README.md` and follow that directory before trying to resolve ambiguity yourself
9. **When adding/changing evolution rules**: Update `docs/plans/2026-03-10-evolution-rule-coverage.md`
10. **Rule registration**: New rules must be registered using the template in the registry document
11. **Domain review sync**: If the rule belongs to an existing reviewed path, update its domain review document too
12. **Benchmark sync**: If the path has a benchmark document, update it in the same turn
13. **Rule evaluation**: After adding a new evolution relation, use a Claude subagent to review representative cases and summarize the evaluation; only use local `claude -p` when the environment supports direct CLI invocation
14. **Rule commit**: Every completed evolution-rule write-in must create a local git commit; do not skip commit creation even if you do not push
15. **Before committing**: Run `make test` to verify data integrity
16. **Monthly update**: Run `make pipeline` then `make deploy`

## Data Flow

1. BERTopic extracts flat topics from monthly arXiv data
2. LLM (DeepSeek) builds hierarchical structure and aligns topics across months
3. Export static JSON files
4. Frontend loads JSON and visualizes trends

## Configuration

- `config/settings.yaml` - Topic modeling and LLM settings
- `config/prompts.yaml` - LLM prompts for hierarchy building

## Important Notes

- Layer 1-2 (Discipline/Category) are fixed arXiv classifications
- Layer 3+ are dynamically built by LLM with dynamic depth
- Each topic has one primary parent (semantic specificity priority)
- Cross-disciplinary topics have related_paths for reference
- **Documentation**: Evolution docs now have a fixed hierarchy: governance -> registry -> domain review -> benchmark
- **Documentation**: When evolution rules change, update the rule registry document and keep its tree-path coverage table in sync
- **Documentation**: Prefer tree-path-scoped domain reviews over free-form notes; avoid introducing new rule notes outside the standard skeleton
- **Documentation**: For weaker models or repetitive work, prefer the worker playbook and benchmark before attempting new rules
- **Documentation**: If you are delegating to subagents via slash commands, route work through the skills design and math worker backlog rather than issuing open-ended "continue" prompts
- **Documentation**: If ambiguity remains, do not improvise first; check the documents in `docs/plans/evolution-ops/` in order and only escalate after following that troubleshooting flow
- **Evaluation**: Every newly added evolution relation should be checked with Claude on representative positive / ambiguous cases; in Claude environments prefer a subagent over self-invocation
- **Git**: Every completed evolution-rule iteration should end with a local git commit, even if no push is requested
