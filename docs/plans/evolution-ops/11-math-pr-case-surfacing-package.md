doc_type: "task_package_detail"
scope: "math > math.PR case surfacing"
status: "active"
owner: "trend-monitor"
source_of_truth: true
upstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/03-task-packages.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-18-math-pr-benchmark.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-18-math-export-review.md"
downstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-12-math-worker-backlog.md"
last_reviewed: "2026-03-18"
package_id: "MPR-01B / PKG-PR-01B"
---

# Math.PR Case Surfacing Package

## Purpose

这个包用于把 `math.PR` 从当前的 `provisional skeleton candidate` 推进到更稳的、可进入 curation 的状态。

当前我们已经确认：

- `math.PR` 不是 gap
- 存在 12 个 multi-period topics
- 存在 6 个 candidate anchors

但我们还没有把这些底层结构证据固定成**显式的 PR-specific cases**。  
也就是说，目前的候选链条仍然主要来自：

- topic metadata
- neighbor relationships
- filtered export 中的有限可见案例

而不是一套已经固定好的：

- positive pairs
- negative pairs
- ambiguous pairs

## Goal

在不修改 pipeline / tests / Makefile 的前提下，完成一次 `math.PR` 的显式 case surfacing：

1. 从 math-focused export 与 PR topic graph 中整理 `math.PR` 候选 pairs
2. 区分：
   - explicit exported cases
   - graph-inferred candidate cases
3. 固定第一批：
   - 2-3 positive candidates
   - 2 negative candidates
   - 1 ambiguous candidate
4. 明确这些 pair 中哪些足够进入 `MPR-02 case curation`

## Why This Package Exists

`PKG-PR-01` 最初把 `math.PR` 写得过强，后续通过 `PKG-PR-01-provisional-fix` 已经收回到正确强度：

- 真实证据：有 multi-period topics / candidate anchors
- 证据缺口：显式 exported PR cases 仍偏少

所以这一步不是重复 bootstrap，而是补齐“从底层结构证据到可 curated cases”的中间层。

## Package Definition

```yaml
package_id: "PKG-PR-01B"
owner: "case-worker"
tree_path: "math > math.PR"
task_type: "pr_specific_case_surfacing"
target_rule:
  - "math_pr_object_continuity"
  - "math_pr_method_continuity"
goal: "把 math.PR 的底层 multi-period / anchor 证据显式整理为 candidate cases，并判断是否足以进入 MPR-02"
allowed_files:
  - "docs/plans/2026-03-18-math-pr-benchmark.md"
  - "docs/plans/2026-03-12-math-worker-backlog.md"
  - "docs/plans/evolution-ops/03-task-packages.md"
  - "docs/plans/evolution-ops/11-math-pr-case-surfacing-package.md"
required_commands:
  - "python3 pipeline/evolution_analysis.py --input data/output/aligned_topics_hierarchy.json --output-dir data/output/math_discovery_pr_surfacing --max-cases 20 --category-filter math"
done_when:
  - "explicit exported PR cases 与 graph-inferred cases 被清晰区分"
  - "至少固定 2-3 个 positive candidate pairs"
  - "至少固定 2 个 negative candidate pairs"
  - "至少固定 1 个 ambiguous candidate pair"
  - "明确判断 MPR-02 是否解锁"
stop_if:
  - "所有候选都只能靠 random / stochastic / probability 这类泛词区分"
  - "必须修改 pipeline、tests 或 Makefile 才能完成"
  - "必须引入 synthetic case 才能凑够 pair"
```

## Strong Constraints

### Allowed

- 运行 math-focused export 到单独目录
- 用 export + filtered graph + benchmark doc 复核候选
- 更新 benchmark doc / backlog / task-packages

### Not Allowed

- 不修改 `pipeline/`
- 不修改 `tests/`
- 不修改 `Makefile`
- 不修改 registry
- 不直接进入 runner
- 不把 `math.PR` 直接写成 ready
- 不扩展到 `math.NT`
- 不用 synthetic case

## Recommended Agent Team Split

这个包适合并发执行，建议至少 4 个 agent。

### Agent 1: export-agent

职责：

- 运行 `math.PR` surfacing export
- 从 `evolution_cases.json` 中找出显式的 PR cases
- 记录：
  - 哪些 anchor 真的在 export 里出现
  - 哪些 target 在 export 里被显式支持

禁止：

- 改文档
- 改代码

### Agent 2: graph-agent

职责：

- 从 `topic_graph.json` 和 trend metadata 中整理 graph-inferred candidate pairs
- 区分：
  - neighbor-only
  - stronger candidate links
- 标记“只是相邻”与“有较强 continuity 指向”的差别

禁止：

- 改代码
- 改 registry

### Agent 3: boundary-agent

职责：

- 审查边界
- 重点区分：
  - `math.PR` vs `math.ST`
  - `math.PR` vs `math.AP`
  - `math.PR` vs `math.OC`
  - `math.PR` vs `math.NA`
- 形成 negative / ambiguous 候选清单

禁止：

- 改代码
- 改文档主结论

### Agent 4: doc-agent

职责：

- 汇总前 3 个 agent 的证据
- 更新 benchmark doc / backlog / ops task packages
- 产出“是否解锁 `MPR-02`”的最终结论

禁止：

- 改 pipeline
- 改 tests

## Working Definition

### Explicit Exported PR Case

满足以下任一更强条件：

- 在 filtered `evolution_cases.json` 中直接出现
- 或在 export report 中被明确记为案例而非仅 topic presence

### Graph-Inferred Candidate Case

满足以下较弱条件：

- anchor topic 满足 papers / periods / neighbors 条件
- 与另一 PR topic 存在图关系
- 但尚未在 export 中显式出现为案例

### Candidate Pair Acceptance Rule

要进入 `MPR-02`，至少需要：

- 2 个 positive candidate pairs
- 2 个 negative candidate pairs
- 1 个 ambiguous candidate pair

并且这些 pair 不能只靠泛词成立。

## Suggested Output Shape

最终应把候选分为 4 桶：

### 1. Confirmed / Export-Supported

有 export 层直接支持的 candidate pairs。

### 2. Strong Inferred

虽未显式 export，但有较强 graph + topic object continuity 支撑。

### 3. Boundary Negatives

应明确排除的 pairs。

### 4. Ambiguous / Review-Needed

边界未收紧前不应当作正例的 pairs。

## Recommended Decision Fork

### Option A: Unlock MPR-02 (NOT achieved by PKG-PR-01B)

条件（**PKG-PR-01B 未满足**）：

- ❌ explicit exported PR-specific positives >= 2
- ❌ negative >= 2
- ❌ ambiguous >= 1

**PKG-PR-01B 的问题**:
- 使用的是 math-wide export，不是 PR-specific extraction
- Export 中 PR-related content 仅 ~10%
- 需要 **MPR-01C: PR-targeted candidate extraction** 才能满足条件

### Option B: Stay Provisional (Current Status)

PKG-PR-01B 确认：

- ✅ 有底层结构证据 (12 multi-period, 6 eligible anchors)
- ✅ Schema 健康 (neighbor_topics, key_supporting_topics 完整)
- ❌ **Export scope 太宽** — math-wide 而非 PR-specific
- ❌ **Explicit PR cases 不足** — 需要真正的 PR-targeted extraction

动作：

- 维持 `provisional skeleton candidate`
- **不解锁 `MPR-02`**
- 下一步：**MPR-01C: PR-targeted candidate extraction** (使用 hierarchy filter)

## Non-Goals

本包不做：

- runner implementation
- registry 升级
- benchmark-ready 最终宣告
- math.NT 扩展

## Expected Outcome (Revised)

这个包做完后，`math.PR` 应该明确：

**PKG-PR-01B 实际产出**:
- ✅ 确认了 math-wide export 的 scope limitation
- ✅ 纠正了 "0 neighbors / data-baseline issue" 错误认知
- ✅ 验证了 schema 完整性 (neighbor_topics: 98 refs, key_supporting_topics: 62 refs)
- ❌ **不能**解锁 MPR-02 — 需要真正的 PR-specific extraction

**下一步**: 执行 **MPR-01C: PR-targeted candidate extraction**
- 使用 `--hierarchy-filter math.PR` 或 subcategory filter
- 获取真正 PR-specific 的 explicit cases
- 然后评估 MPR-02 解锁条件

**状态**: math.PR 保持 provisional，直到 PR-specific extraction 完成。

