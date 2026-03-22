---
doc_type: "candidate_extraction"
scope: "math > math.PR"
status: "completed"
owner: "case-worker"
package_id: "MPR-01C"
source_of_truth: true
upstream_docs:
  - "docs/plans/2026-03-18-math-pr-benchmark.md"
  - "docs/plans/2026-03-12-math-worker-backlog.md"
  - "docs/plans/evolution-ops/03-task-packages.md"
downstream_docs: []
last_reviewed: "2026-03-20"
corrected_by: "MPR-01C-fix"
decision: "Option A — MPR-02 UNLOCKED"
---

# MPR-01C: PR-Targeted Candidate Extraction

**Package:** MPR-01C
**Scope:** math > math.PR
**Date:** 2026-03-20
**Status:** Completed
**Decision:** Option A — MPR-02 UNLOCKED

---

## Interpretation of evolves_from Direction

In this repository, `evolves_from` edges encode **forward evolution**: the `source` node is the **older** topic and the `target` node is the **newer** topic that grew from it.

This is confirmed by `pipeline/evolution_analysis.py` (`build_evolves_edges`): the outer loop iterates over the *new* topic (`target`), and finds a *candidate predecessor* (`source`) whose activity ended strictly before the new topic began. The edge is recorded as `{"source": candidate_id, "target": new_topic_id}`.

**Verified example:** `global_38 -> global_100`
- global_38 (随机极限与不等式, active 2025-02/03) is the older source
- global_100 (随机矩阵系综累积量, active 2025-04+) is the newer target

**Previous error in this document:** Pairs P1/P2/P3 were written as `global_100/156/99 -> global_38`, reversing source and target. These have been corrected below.

---

## Correction Notice (2026-03-20, MPR-01C-fix)

This document was corrected after MPR-01C-fix audit. The original version incorrectly attributed
`evolves_from` edges to the targeted export's `topic_graph.json`. The corrections below fix:
- Source attribution: `evolves_from` edges are in `data/output/topic_graph.json` (MAIN graph),
  not in `data/output/math_discovery_pr_targeted/topic_graph.json`
- The targeted export's `topic_graph.json` contains ONLY `adjacent_to` edges
- global_99→global_38: removed false bw=0.475 claim (that bw belongs to global_39↔global_99)
- global_99→global_38 is now "single-source inferred" (evolves_from main graph only, no adjacency)
- MPR-02 decision unchanged: Option A, still unlocked, based on corrected evidence

**MPR-01C-final-fix (2026-03-20):** Corrected evolves_from direction semantics. The source is the OLDER topic. Pairs P1/P2/P3 had source/target swapped in all prior versions of this document. Pairs have been corrected; narratives rewritten accordingly. MPR-02 lock state: UNLOCKED (Option A). Decision unchanged after direction correction.

---

## 1. PR Candidate Universe

### Full PR Topic Universe

The `aligned_topics_hierarchy.json` contains **29 total topics** mapped to the `math.PR` category.

| Metric | Count |
|--------|-------|
| Total PR topics in hierarchy | 29 |
| Multi-period topics (active_periods > 1) | 12 |
| Single-period topics | 17 |
| Eligible anchors (papers >= 60 AND periods >= 2) | 11 |

Single-period topics (17 topics) are not eligible for evolution pair extraction because at least two active periods are required to observe continuity or divergence between time windows.

### Eligible Anchors (11 topics)

| Topic ID | Chinese Name | Papers | Periods | Active History | Keywords |
|----------|-------------|--------|---------|----------------|----------|
| global_39 | 随机过程渗流方程 | 1280 | 4 | 2025-02, 2025-06, 2025-12, 2026-01 | convergence, stochastic, percolation, equations, time |
| global_65 | 随机微分方程收敛 | 391 | 4 | 2025-03, 2025-05, 2025-08, 2025-10 | convergence, stochastic, equations, existence, noise |
| global_188 | 随机粗糙McKean方程 | 387 | 4 | 2025-07, 2025-09, 2025-11, 2026-02 | jump, spdes, stochastic, hawkes, equations |
| global_99 | 随机游走与分支 | 179 | 3 | 2025-04, 2025-09, 2026-02 | ruin, hawkes, percolation, gsaws, martingale |
| global_38 | 随机极限与不等式 | 208 | 2 | 2025-02, 2025-03 | convergence, g_n, matrices, walk, infty |
| global_271 | 渗流与随机行走临界性 | 118 | 2 | 2025-10, 2026-02 | coalescing, percolation, kpz, brownian, lattice |
| global_47 | 伊辛相变与临界 | 96 | 2 | 2025-03, 2025-07 | scaling, potts, xy, spin, temperature |
| global_211 | 种群适应与生态进化 | 94 | 2 | 2025-08, 2025-12 | growth, ecological, population, populations, competition |
| global_100 | 随机矩阵系综累积量 | 78 | 2 | 2025-04, 2025-07 | matrix, eigenvalues, matrices, tensor, eigenvalue |
| global_156 | 随机矩阵特征值分析 | 78 | 2 | 2025-06, 2025-09 | fourier, matrix, operatorname, eigenvalues, matrices |
| global_116 | 强化随机游走渗流 | 65 | 2 | 2025-05, 2025-07 | reinforced, markov, step, elephant, percolation |

The largest anchor (global_39, 1280 papers, 4 periods) represents the backbone of PR activity and serves as the primary integration point for graph adjacency analysis.

---

## 2. Export vs Hierarchy Evidence

### The Export Limitation Problem

The math-wide pipeline export (`evolution_analysis.py --category-filter math --max-cases 20`) produced **20 total cases**, of which only **1 case was PR-anchored** (global_39). This represents a **5% PR visibility rate** in the export.

This is a structural artifact of the math-wide export, not a true reflection of PR activity:

- The `--category-filter math` flag rotates through all math sub-categories, and with ~10+ math sub-categories competing for 20 export slots, PR receives proportionally compressed representation.
- Export-based extraction alone would yield only global_39's evolution context, missing all other eligible anchors and all non-global_39 evolves_from edges.

### Two Data Sources: Evidence Scope

This extraction draws from two distinct graph files with different edge content:

**`data/output/topic_graph.json` (MAIN graph):**
- Contains `belongs_to`, `active_in`, `adjacent_to`, and `evolves_from` edges
- All three evolves_from pairs in this document (global_38→100, global_38→156, global_38→99) are sourced exclusively from this file
- This is the authoritative source for evolution direction evidence

**`data/output/math_discovery_pr_targeted/topic_graph.json` (targeted export):**
- Contains ONLY `adjacent_to` edges — no `evolves_from` edges at all
- Provides corroborating adjacency (bridge_weight) evidence for pairs that also appear in the main graph
- Cannot independently establish evolution direction

All `evolves_from` claims in this document refer to the MAIN graph only.

### What Hierarchy-Scoped Extraction Added

By working directly from `aligned_topics_hierarchy.json` and `topic_graph.json`, this extraction recovered:

| Evidence Type | Export-Based | Hierarchy-Scoped |
|--------------|-------------|-----------------|
| PR eligible anchors identified | 1 (global_39) | 11 |
| Explicit evolves_from edges among anchors (MAIN graph) | 0 | 3 |
| Additional evolves_from edges involving any PR topics (MAIN graph) | 0 | 7 |
| Strong adjacent edges (bridge_weight >= 0.4) | 0 | 7 |
| Candidate pairs recoverable | 0 | 4 (strong inferred) |

The hierarchy-scoped approach is therefore essential for PR-targeted work. Export-only approaches are insufficient for building benchmarks in sub-categories with low rotation probability.

### global_39's Export Case Details

The one PR-anchored export case (global_39) included:
- **neighbor_topics:** global_99, global_116, global_278, global_188, global_222
- **key_supporting_topics:** global_65 (weight=0.3327), global_38 (weight=0.3778), global_60 (weight=0.3292), global_97 (weight=0.3955)
- **event_types:** diffused_to_neighbor, emerged, expanded
- **review_flags:** same_category_high_bridge_weak_carryover

The export case for global_39 validates the adjacency structure but does not directly yield candidate pairs — it requires the evolves_from graph and topic attribute analysis done in this extraction.

---

## 3. Candidate Pair Buckets

### Bucket 1: Strong Inferred Positive Candidates (NOT Benchmark-Confirmed)

All four pairs below are **strong inferred** candidates derived from explicit graph evidence. They are NOT benchmark-confirmed. MPR-02 is required to fix them as final benchmark cases.

**Pair P1: `global_38 → global_100`** — TWO-SOURCE STRONG INFERRED
Object: random limits and inequalities → random matrix ensemble cumulants

- Evidence type: `evolves_from` edge in MAIN graph (`data/output/topic_graph.json`) + adjacency bw=0.35 in both MAIN graph and targeted export
- Mechanism: Object continuity — global_38's random limits/inequalities framework (convergence/matrices/walk) specializing into random matrix ensemble cumulant theory (eigenvalues/matrices/tensor)
- Keywords (source/older, global_38): convergence, g_n, matrices, walk, infty
- Keywords (target/newer, global_100): matrix, eigenvalues, matrices, tensor, eigenvalue
- Note: Shared keyword "matrices" confirms object continuity. NOT generic "stochastic" — both topics operate on specific algebraic random objects.

**Pair P2: `global_38 → global_156`** — TWO-SOURCE STRONG INFERRED
Object: random limits and inequalities → random matrix eigenvalue analysis

- Evidence type: `evolves_from` edge in MAIN graph (`data/output/topic_graph.json`) + adjacency bw=0.4077 in both MAIN graph and targeted export
- Mechanism: Object continuity — global_38's limit-theoretic framework (convergence/matrices) giving rise to focused random matrix eigenvalue analysis (fourier/matrix/eigenvalues)
- Keywords (source/older, global_38): convergence, g_n, matrices, walk, infty
- Keywords (target/newer, global_156): fourier, matrix, operatorname, eigenvalues, matrices
- Note: global_100 and global_156 both independently evolve from global_38 per the MAIN graph, suggesting global_38 is a genuine predecessor whose limit/inequality framework spawned two parallel random matrix research streams.

**Pair P3: `global_38 → global_99`** — SINGLE-SOURCE INFERRED
Object: random limits and inequalities → random walks and branching

- Evidence type: `evolves_from` edge in MAIN graph (`data/output/topic_graph.json`) ONLY. NO adjacency edge exists between global_38 and global_99 in any graph. The bw=0.475 figure previously cited here has been removed — that bridge_weight belongs to the global_39↔global_99 pair, not to global_99↔global_38.
- Mechanism: Object continuity — global_38's asymptotic inequality framework (convergence/walk) developing into dedicated random walk/branching research (percolation/hawkes/martingale)
- Keywords (source/older, global_38): convergence, g_n, matrices, walk, infty
- Keywords (target/newer, global_99): ruin, hawkes, percolation, gsaws, martingale
- Note: The keyword "walk" appears in both anchor keyword sets, and "martingale" in global_99 is conceptually downstream of convergence limit theorems in global_38. However, the evolution claim rests on the MAIN graph evolves_from edge alone; no corroborating adjacency evidence exists for this pair.

**Pair P4: `global_65 → global_188`** — ADJACENCY-DERIVED METHOD INFERRED
Method: SDE convergence → rough McKean stochastic equations

- Evidence type: Adjacent edge with strongest bridge_weight among all anchor pairs (bw=0.4795 in both MAIN graph and targeted export). No evolves_from edge in any graph.
- Mechanism: Method continuity — classical SDE analysis (convergence/stochastic/equations/existence/noise) evolving toward rough path McKean-Vlasov theory (jump/spdes/stochastic/hawkes/equations)
- Keywords (source): convergence, stochastic, equations, existence, noise
- Keywords (target): jump, spdes, stochastic, hawkes, equations
- Note: Both topics are 4-period anchors (the two longest-running PR topics in the hierarchy), consistent with a sustained methodological relationship. The adjacency here is the strongest observed among all PR anchor pairs.

### Bucket 2: Boundary Negatives

**Pair N1: `global_211 ↔ any PR anchor`**
Cross-domain exclusion: population ecology does not belong in probability theory

- Keywords: growth, ecological, population, populations, competition
- Assessment: These keywords signal mathematical biology / population dynamics (closer to math.AP or quantitative biology). No shared probabilistic object with any PR anchor.
- Risk: A math-wide export might surface global_211 as "stochastic" due to growth models, but its object domain is ecological populations, not probability spaces or stochastic processes in the theoretical sense.

**Pair N2: `global_47 ↔ global_39`**
Object mismatch: Ising phase transitions vs. geometric percolation

- Keywords (global_47): scaling, potts, xy, spin, temperature
- Keywords (global_39): convergence, stochastic, percolation, equations, time
- Assessment: While both use "phase transition" language, global_47's object is spin systems with Hamiltonian structure (statistical physics / math.MP), distinct from global_39's geometric percolation and SDE framework. The adjacent edge between global_271 and global_47 (bw=0.2375) is relatively weak and likely reflects graph proximity from shared arxiv tagging rather than true object continuity.

**Pair N3: `global_61 ↔ any pure PR anchor`**
Applied probability exclusion: queueing theory ≠ theoretical probability

- Assessment: 重交通环形排队 represents heavy-traffic queueing theory, which is applied probability and operations research. Despite potential surface-level overlap with stochastic processes, its research object (queue lengths, waiting times, traffic intensity) is distinct from the theoretical probability objects in the 11 eligible anchors.
- Note: global_61 is not among the 11 eligible anchors but is flagged here because it may appear in downstream proximity analysis as a candidate; it should be explicitly excluded from MPR-02 scope.

### Bucket 3: Ambiguous / Needs Review

**Pair A1: `global_65 (SDE) ↔ global_39 (percolation/equations)`**
Weak adjacent evidence, object ambiguity

- Adjacent bridge_weight: 0.3327 (weakest among the adjacent pairs in Bucket 1 reasoning)
- Ambiguity: global_65 operates on noise-driven differential equations (SDE, existence, noise); global_39 covers geometric percolation AND stochastic equations. The stochastic equation component of global_39 could overlap with global_65's SDE framework, but the percolation component does not. The pair is plausible as a partial method overlap but the object continuity claim is weaker than Pairs P1-P4.
- Recommendation for MPR-02: Flag for deeper keyword overlap analysis. Retain as a "possible" rather than "probable" pair.

**Pair A2: `global_47 (Ising)` classification boundary**
math.PR vs. math.MP ambiguity

- The keywords scaling, potts, xy, spin, temperature are characteristic of statistical mechanics models that live at the intersection of math.PR and math.MP.
- Spin systems do admit probabilistic measures (Gibbs measures, FK-percolation), so global_47 is not categorically excluded from PR, but its terminology is more strongly associated with math.MP research programs.
- Recommendation for MPR-02: Do not include global_47 as a positive candidate. If included, classify as "borderline PR/MP" and require explicit subject-area justification in the benchmark case.

### Bucket 4: Export-Limited / Visibility-Limited

The following anchor pairs have strong graph evidence but were not represented in the 20-case math-wide export:

| Pair | Evidence | Export Visibility |
|------|----------|------------------|
| global_38 -> global_100 | evolves_from (MAIN graph) + adjacent bw=0.35 (both graphs) | not in export |
| global_38 -> global_156 | evolves_from (MAIN graph) + adjacent bw=0.4077 (both graphs) | not in export |
| global_38 -> global_99 | evolves_from (MAIN graph) ONLY; no adjacency in any graph | not in export |
| global_65 ↔ global_188 | adjacent bw=0.4795 (both graphs, strongest PR pair); no evolves_from | not in export |

These are "hierarchy-visible but export-invisible" candidates. Their absence from the export is a consequence of math-wide category rotation compressing PR's 5% slot allocation to a single case (global_39). They are not weaker candidates — they are structurally invisible to export-based analysis.

This reinforces the finding in Section 2: export-only extraction is insufficient for PR benchmark construction. Hierarchy-scoped extraction is the correct method for this sub-category.

### Evidence Verification Table (Corrected)

The following table records the verified ground truth for all five pairs discussed in this document,
including global_39↔global_99 to clarify the source of the bw=0.475 figure:

| Pair | Main adj.bw | Main evolves_from | Targeted adj.bw | Corrected Status |
|------|-------------|-------------------|-----------------|-----------------|
| global_38 -> global_99 | NONE | YES (global_38 is source) | NONE | single-source inferred (evolves_from MAIN graph only) |
| global_38 -> global_100 | 0.35 | YES (global_38 is source) | 0.35 | two-source strong inferred |
| global_38 -> global_156 | 0.4077 | YES (global_38 is source) | 0.4077 | two-source strong inferred |
| global_65 ↔ global_188 | 0.4795 | no | 0.4795 | adjacency-derived method inferred |
| global_39 ↔ global_99 | 0.475 | no | 0.475 | adjacency pair (note: bw=0.475 belongs here, not to global_99↔global_38) |

The targeted export (`data/output/math_discovery_pr_targeted/topic_graph.json`) contains only
`adjacent_to` edges. Any evolves_from evidence in this document comes exclusively from the MAIN
graph (`data/output/topic_graph.json`).

---

## 4. Boundary Analysis

### math.PR vs. Adjacent Math Sub-categories

The following confusion risks apply when identifying PR candidates from the broader topic graph:

**math.PR vs. math.ST (Statistics)**

- Risk: Topics with keywords involving convergence, distributions, and estimation may be claimed by both PR and ST.
- Distinguishing signal: PR focuses on stochastic objects themselves (random walks, SDEs, Markov chains, percolation). ST focuses on statistical inference procedures (estimators, hypothesis tests, confidence intervals) applied to data.
- Affected candidate: None in the current 11 anchors show significant ST confusion risk.

**math.PR vs. math.AP (Applied Mathematics / Partial Differential Equations)**

- Risk: Topics involving SPDEs, McKean-Vlasov equations, and diffusion equations (global_188, global_65) could be claimed by math.AP if the focus shifts from the probabilistic measure to the PDE structure.
- Distinguishing signal: If the research object is a probability measure or stochastic process, classify as PR. If the object is a deterministic PDE solution approximated by probabilistic methods, consider math.AP.
- Affected candidates: global_188 (spdes, McKean) and global_65 (SDE, equations) are at the PR/AP boundary. Their PR classification is defensible because their active period keyword sets consistently include stochastic and convergence (probabilistic behavior), not just PDE solution existence.

**math.PR vs. math.MP (Mathematical Physics)**

- Risk: Spin systems, phase transitions, and Ising models (global_47) have both PR and MP interpretations. KPZ universality (global_271 keyword) is also a PR/MP boundary topic.
- Distinguishing signal: PR framing emphasizes probability measure, random variable distributions, and stochastic process trajectories. MP framing emphasizes Hamiltonian structure, partition functions, and scaling limits as physical observables.
- Affected candidates: global_47 is the primary PR/MP confusion risk (see Bucket 3, Pair A2). global_271 contains "kpz" which spans PR and MP but its other keywords (coalescing, percolation, brownian, lattice) are predominantly PR.

**math.PR vs. math.NA (Numerical Analysis)**

- Risk: Topics involving approximation schemes, numerical convergence, or discretization of SDEs.
- Distinguishing signal: PR candidates should be studying the stochastic process's analytical properties, not the numerical algorithm's convergence rate.
- Affected candidates: global_65 (convergence, existence, equations) is the closest to a PR/NA boundary case if "convergence" is interpreted as numerical. However, global_65's keyword "noise" and "stochastic" anchor it in PR, not NA.

---

## 5. Decision Fork

### Decision: Option A — UNLOCK MPR-02

All four required conditions for unlocking MPR-02 are met:

| Condition | Required | Met? | Details |
|-----------|----------|------|---------|
| >= 2 strong positive pairs | Yes | Yes | 4 pairs: P1, P2, P3, P4 |
| >= 2 boundary negatives | Yes | Yes | 3 negatives: N1 (global_211), N2 (global_47), N3 (global_61) |
| >= 1 ambiguous pair | Yes | Yes | A1: global_65 vs global_39 |
| Keywords are specific (not purely generic) | Yes | Yes | eigenvalues, matrices, percolation, martingale, rough paths, McKean — all domain-specific |

### Option A holds after evidence correction

Option A holds even after evidence correction: P1 and P2 are two-source strong inferred
(evolves_from in MAIN graph plus corroborating adjacency in both graphs); P3 is single-source
inferred (evolves_from MAIN graph only, no adjacency); P4 is adjacency-only method continuity
(strongest raw bridge_weight among all PR anchor pairs). All four conditions for unlocking
MPR-02 remain satisfied.

All evolves_from evidence in this document comes from the MAIN graph (`data/output/topic_graph.json`),
not from the targeted extraction run. The targeted export's `topic_graph.json` provides adjacency
corroboration for P1, P2, and P4 only.

### Why Not Option B (Defer MPR-02)

Option B (defer due to insufficient evidence) would require either:
- Fewer than 2 strong pairs supported by explicit graph evidence, or
- All pairs relying only on generic stochastic keywords with no specific object continuity, or
- No clear negatives available for benchmark calibration.

None of these conditions hold. The three explicit evolves_from edges (P1: global_38→100, P2: global_38→156, P3: global_38→99) in the MAIN
graph provide directed evolution evidence that cannot be dismissed as coincidental co-tagging.
P1 and P2 each carry two-source corroboration. Pair P4 has the strongest adjacent bridge weight
observed among all PR anchor pairs. The negatives (N1, N2, N3) are clearly distinguishable from
PR objects by keyword analysis. P3's downgrade to single-source does not remove it as a
contributing positive — it retains a directed evolves_from edge from the MAIN graph.

The caveat is that this evidence base is **strong inferred, not benchmark-confirmed**. MPR-02 is
the step that confirms or revises these pairs through actual case curation. Option A is the
appropriate decision precisely because the evidence is strong enough to warrant that curation
investment.

---

## 6. Questions Answered

**Q1: math.PR 真实 hierarchy-scoped candidate pool 大概有多大？**

The hierarchy-scoped candidate pool for math.PR is **11 eligible anchors** (topics meeting papers >= 60 and periods >= 2), drawn from 29 total PR topics. Among these 11, the graph analysis surfaces **4 strong inferred candidate pairs** for evolution benchmark purposes. The realistic pool for MPR-02 curation is these 4 pairs plus 1-2 ambiguous pairs, for a working set of 5-6 candidate pairs before filtering.

**Q2: 当前 export 中显式可见的 PR evidence 有多少？**

The math-wide export (20 cases, `--category-filter math`) contains exactly **1 PR-anchored case**: global_39. This is 5% of the export (1/20). The export case provides neighborhood structure for global_39 but does not directly yield candidate pairs. Zero evolves_from edges and zero explicit evolution events are visible in the export output for PR-internal pairs.

**Q3: 哪些 positive candidate pairs 最强？**

Ranked by evidence strength (corrected after MPR-01C-fix audit):

1. **P1: global_38 -> global_100** — two-source: evolves_from in MAIN graph + adjacency bw=0.35 in both graphs. Part of the coherent dual-source divergence from global_38.
2. **P2: global_38 -> global_156** — two-source: evolves_from in MAIN graph + adjacency bw=0.4077 in both graphs. Part of the dual-source divergence from global_38.
3. **P4: global_65 → global_188** — strongest raw adjacent bridge_weight (bw=0.4795) among all PR anchor pairs in both graphs, but no explicit evolves_from edge. Adjacency-only evidence.
4. **P3: global_38 -> global_99** — single-source: evolves_from in MAIN graph only; NO adjacency in any graph. The bw=0.475 figure previously cited for this pair has been corrected — that bridge_weight belongs to global_39↔global_99, not to global_38↔global_99. P3 is the weakest positive: directional but uncorroborated.

P1 and P2 together form a structurally coherent picture: a generalized limit/inequality framework (global_38) gave rise to two parallel random matrix topics (global_100 and global_156) per the MAIN graph, which is a plausible theoretical development — the broader asymptotic framework preceding the specialized matrix-theoretic research streams.

**Q4: 哪些 negative pairs 最稳？**

Most stable negative: **N1 (global_211 — population ecology)**. Its keyword domain (ecological, population, competition, growth) is categorically outside theoretical probability. There is no keyword overlap with any of the 11 eligible PR anchors. This negative is unambiguous and robust to reanalysis.

Second most stable: **N3 (global_61 — queueing theory)**. Applied probability queueing is structurally distinct from the theoretical probability objects in the anchor set, and its object domain (queues, traffic, service times) shares no keywords with PR anchors.

N2 (global_47 — Ising) is the least stable negative because Ising models do have PR interpretations. It is negative for the purpose of pairing with global_39 specifically, but it is not categorically excluded from PR as a subject area.

**Q5: 哪个 ambiguous pair 最值得保留？**

**A1: global_65 (SDE) ↔ global_39 (percolation/equations)** is the most valuable ambiguous pair to retain for MPR-02. It tests the boundary between two legitimate PR sub-areas: SDE-driven analysis and geometric/combinatorial stochastic processes. A well-constructed benchmark case for this pair would help calibrate the system's ability to distinguish method-level overlap (both use stochastic) from genuine object continuity (SDE vs. percolation are different objects). The weak adjacent evidence (bw=0.3327) makes it a genuine ambiguity, not a suppressed positive.

**Q6: 这轮是否足以解锁 MPR-02？**

**Yes.** The extraction meets all four unlocking conditions (see Section 5). The decision is **Option A — MPR-02 UNLOCKED**.

**Q7: 如果解锁，最小 candidate set 是什么？**

See Section 7 for the formal minimum candidate set statement.

**Q8: 如果不解锁，差的到底是哪一层证据？（N/A — MPR-02 is unlocked）**

N/A — MPR-02 is unlocked by this extraction. For completeness, the gap that MPR-01B (the prior benchmark state) had was: zero explicit evolves_from edges identified for PR-internal anchor pairs and zero hierarchy-scoped anchor enumeration. MPR-01B operated from export-only data, which yielded only global_39's neighborhood without evolves_from attribution. The gap was at the "graph-derived object continuity evidence" layer — not at the keyword or adjacency layer, but at the directed evolution relationship layer.

The evolves_from edges that closed this gap (for P1, P2, P3) are present in the MAIN graph
(`data/output/topic_graph.json`), not in the targeted export's graph file. The targeted export
contributed adjacency corroboration for P1 and P2, but not directed evolution evidence.

---

## 7. Minimum Candidate Set

If MPR-02 proceeds with the minimum viable input set, it must include at minimum:

### Positive Pairs (object/method continuity, strong inferred)

| Pair ID | Source → Target | Continuity Type | Evidence |
|---------|----------------|-----------------|---------|
| P1 | global_38 -> global_100 | Object (limits → random matrix ensemble) | evolves_from (MAIN graph) + adjacent bw=0.35 (both graphs) |
| P2 | global_38 -> global_156 | Object (limits → eigenvalue analysis) | evolves_from (MAIN graph) + adjacent bw=0.4077 (both graphs) |
| P3 | global_38 -> global_99 | Object (limits → random walk/branching) | evolves_from (MAIN graph) ONLY; no adjacency in any graph |
| P4 | global_65 → global_188 | Method (SDE → rough McKean) | adjacent bw=0.4795 (both graphs, strongest PR pair); no evolves_from |

### Negative Pairs (boundary exclusions)

| Pair ID | Topic | Exclusion Reason |
|---------|-------|-----------------|
| N1 | global_211 | Cross-domain: mathematical biology, not probability |
| N2 | global_47 | Object mismatch: statistical physics / math.MP crossover |
| N3 | global_61 | Applied probability (queueing), not theoretical PR |

### Ambiguous Pair (boundary calibration)

| Pair ID | Source ↔ Target | Ambiguity Type |
|---------|----------------|----------------|
| A1 | global_65 ↔ global_39 | Stochastic method vs. stochastic object boundary |

**Total minimum set: 4 positives + 3 negatives + 1 ambiguous = 8 candidate pairs**

This set is sufficient to begin MPR-02 curation. Additional pairs may be added from the broader PR topic graph if the curation team identifies further evolves_from edges or high-bridge-weight adjacencies during the MPR-02 review cycle.

---

## 8. Evidence Scope Disclaimer

**CRITICAL: All positive candidate pairs in this document are "strong inferred" (graph-derived). They are NOT benchmark-confirmed.**

Specifically:

- Pairs P1 (global_38→100), P2 (global_38→156), P3 (global_38→99) are derived from `evolves_from` edges in `data/output/topic_graph.json` (the MAIN graph). These edges were generated by the pipeline's topic evolution analysis module. They represent algorithmic inferences about topic lineage, not human-curated ground truth. The targeted export's `topic_graph.json` (`data/output/math_discovery_pr_targeted/topic_graph.json`) contains no evolves_from edges and was not the source of these claims.
- Pair P4 is derived from the strongest adjacent `bridge_weight` in the PR anchor set. Bridge weight measures cross-topic paper overlap, which correlates with evolution but is not equivalent to it.
- No human expert has reviewed and confirmed that any of these pairs represents a genuine scientific evolution event in the math.PR literature.
- The keyword analysis supporting object/method continuity is the current author's interpretation of topic keywords. Different interpretations of "convergence" (probabilistic vs. numerical) or "equations" (SDE vs. PDE) could alter the assessment.

**What MPR-02 will do that this document cannot:**

MPR-02 is the case curation step that will:
1. Inspect actual paper titles and abstracts for each proposed pair
2. Verify that the source topic's papers contain language anticipating or motivating the target topic
3. Assign formal benchmark labels (positive / negative / ambiguous) with human justification
4. Fix the final candidate set for training/evaluation use

Until MPR-02 is complete, these pairs should be treated as **inputs to curation**, not as benchmark ground truth.

---

## 9. Residual Risks

### Risk R1: global_38's short activity history

global_38 (随机极限与不等式) has only 2 active periods (2025-02, 2025-03) and is the source of three evolves_from edges (P1, P2, P3). Its short history raises the possibility that it is a transient topic cluster rather than a stable research stream. If global_38 does not persist in later periods, the evolution narratives P1/P2/P3 may reflect a temporary clustering artifact rather than genuine scientific evolution.

Mitigation: MPR-02 should check whether global_38's 2025-02/2025-03 papers are substantively about limit theory and inequalities (confirming it as a real topic) or are a heterogeneous catch-all cluster.

### Risk R2: evolves_from edge directionality

The three evolves_from edges (P1: global_38→100, P2: global_38→156, P3: global_38→99) all originate from global_38. This is consistent with the pipeline semantics (source=older, target=newer): global_38 (active 2025-02/03) precedes global_100 (active 2025-04+), global_156 (active 2025-06+), and global_99 (active 2025-04+). However, global_38 has 208 papers while global_100 and global_156 have only 78 each — an older, larger topic giving rise to smaller, newer specialized topics is the expected evolution pattern.

Mitigation: MPR-02 should verify that the chronology is consistent — global_38's active periods (2025-02/03) should strictly precede global_100, global_156, and global_99's first active periods.

### Risk R3: PR sub-category coverage bias

The 11 eligible anchors may not represent the full breadth of math.PR research. Topics with fewer than 60 papers (the eligibility threshold) may contain important evolution signals. The threshold was set to ensure statistical reliability, but it may exclude niche areas (e.g., rough paths, Malliavin calculus, free probability) that generate fewer but highly significant papers.

Mitigation: This is an acceptable risk for MPR-01C/MPR-02 scope. A future MPR-03 or papers-threshold sensitivity pass could lower the threshold to 30 and re-examine.

### Risk R4: Pair P4 lacks evolves_from evidence

Pair P4 (global_65 → global_188) is the only positive pair without an explicit evolves_from edge. It relies solely on adjacency (bridge_weight=0.4795). If the adjacency is driven by co-tagging of papers that use both SDE and rough path methods (rather than a research community's methodological evolution), P4 may not survive MPR-02 curation.

Mitigation: Retain P4 as a candidate but flag it for closer scrutiny in MPR-02. The 4-period overlap of both topics (both among the longest-running PR anchors) provides corroborating circumstantial evidence.

### Risk R5: Export slot allocation for PR may improve

The current math-wide export gives PR approximately 1 slot per 20 cases. If future pipeline runs increase `--max-cases` or introduce a `--category-filter math.PR` option, export-based extraction could become viable for PR. This document's hierarchy-scoped approach would then be a bootstrapping step rather than a permanent method.

Mitigation: Document the hierarchy-scoped method as the canonical approach for low-visibility sub-categories. When export slot allocation improves, validate that export-derived pairs match the hierarchy-scoped pairs found here.

---

## 10. Next Steps

### MPR-02 Scope

MPR-02 (PR Candidate Case Curation) should proceed with the following scope, directly derived from this extraction:

**Input to MPR-02:**
- Minimum candidate set: 4 positives + 3 negatives + 1 ambiguous (see Section 7)
- Source data: `data/output/aligned_topics_hierarchy.json`, `data/output/topic_graph.json`
- Reference export: `data/output/math_discovery_pr_targeted/` (for global_39 neighborhood context)

**MPR-02 Tasks:**
1. For each positive pair (P1-P4): retrieve source (older) and target (newer) topic paper lists; verify chronological ordering of active periods (source must predate target); sample 5-10 paper titles per topic to confirm object/method label accuracy
2. For each negative pair (N1-N3): confirm exclusion rationale with a brief paper sample review
3. For ambiguous pair A1: document the specific ambiguity with paper-level evidence; assign a provisional label (positive/negative/ambiguous) with justification
4. Produce benchmark case records in the standard format established by math.LO (see `docs/plans/2026-03-12-math-lo-benchmark.md`) and math.AG benchmarks
5. Assign final candidate status: confirmed_positive, confirmed_negative, or requires_further_review

**MPR-02 Acceptance Criteria:**
- At least 3 confirmed positive pairs with paper-level justification
- At least 2 confirmed negative pairs with exclusion rationale
- Ambiguous pairs explicitly labeled and documented
- No pair labeled "confirmed" without paper-level review

**Downstream Impact:**
Upon MPR-02 completion, populate `downstream_docs` in this document's frontmatter with the MPR-02 output document path, and update this document's `status` from "completed" to "superseded_by_MPR-02".
