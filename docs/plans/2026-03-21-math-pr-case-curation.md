---
doc_type: "case_curation_report"
scope: "math > math.PR"
status: "COMPLETE — Conditional graph integration readiness confirmed"
owner: "case-worker"
package_id: "MPR-02"
date: "2026-03-21"
upstream_docs:
  - "docs/plans/2026-03-18-math-pr-benchmark.md"
  - "docs/plans/2026-03-20-math-pr-candidate-extraction.md"
  - "docs/plans/2026-03-12-math-worker-backlog.md"
  - "docs/plans/evolution-ops/03-task-packages.md"
downstream_docs: []
last_reviewed: "2026-03-21"
---

# math.PR Case Curation — MPR-02

**Date:** 2026-03-21
**Package:** MPR-02
**Status:** COMPLETE — Conditional graph integration readiness confirmed

---

## 1. Executive Summary

MPR-02 case curation is complete. The curation process produced 4 positive candidates (2 Tier A, 2 Tier B), 5 negative cases, and 2 ambiguous calibration cases across 11 total curated pairs.

All positive candidates are strong inferred curated cases derived from graph evidence (evolves_from edges and adjacency weights from `data/output/topic_graph.json`). None are benchmark-confirmed. Paper-level review is required before any positive pair is promoted to a benchmark-confirmed status.

The curated set satisfies the MPR-02 completion criteria and supports a conditional readiness decision for math.PR graph integration. Three residual risks have been identified and must be addressed before unconditional integration. The recommended next step is Option 2C (PR Phase 2C — conditional graph integration planning).

---

## 2. Input Evidence

Evidence for this curation was drawn from two graph sources within the worktree:

- **Main topic graph**: `data/output/topic_graph.json`
  - Contains both `evolves_from` and `adjacent_to` edge types
  - Source of all evolves_from weights used in this curation
- **PR-targeted export graph**: `data/output/math_discovery_pr_targeted/topic_graph.json`
  - Contains `adjacent_to` edges only (no evolves_from)
  - Source of adjacency weights for P1, P2, P4

The math.PR topic universe: 29 total topics, 12 multi-period, 11 eligible anchors (papers >= 60, periods >= 2). MPR-02 does not redefine the anchor rule; it curates a narrower case set from that 11-topic anchor pool. Candidate pairs were identified by MPR-01C (completed 2026-03-20).

**Important direction convention**: In pipeline semantics, `evolves_from` edges run source=OLDER topic, target=NEWER topic. global_38 (active 2025-02/03) is the older source; global_100/156/99 are newer targets.

---

## 3. Curated Positive Cases

### Tier A (Priority Integration Candidates)

Tier A positives have two independent graph sources (both evolves_from weight and adjacency weight), making them the strongest inferred candidates in the curated set.

---

#### PR-P1: global_38 → global_100

**pair_id:** PR-P1
**source → target:** global_38 (随机极限与不等式) → global_100 (随机矩阵系综累积量)
**continuity type:** Object continuity
**rule tag:** math_pr_object_continuity

**Evidence:**
- evolves_from weight: 0.39 (from main `data/output/topic_graph.json`)
- adjacency weight: 0.35 (from both main graph and PR-targeted export)
- Both graph sources agree on this pair

**Period activity:**
- global_38: first active 2025-02, last active 2025-03 (2 periods, 208 papers)
- global_100: first active 2025-04 or later (2 periods, 78 papers)
- Chronology type: strict succession (global_38 activity precedes global_100)

**Continuity rationale:** Both topics concern random matrix theory. global_38 covers random limit theorems and inequalities in the random matrix setting. global_100 covers ensemble-level cumulant analysis. The shared object (random matrix structures) and sequential period activity support object continuity classification.

**Known weaknesses:**
- global_38 is transient: only 2 active periods. This is a fragility risk (R1).
- evolves_from weight of 0.39 is above threshold but not high. A single paper-level misclassification could lower confidence.
- Paper-level review has not been performed.

**Curation status:** curated positive candidate (Tier A — two-source: evolves_from + adjacency)

---

#### PR-P2: global_38 → global_156

**pair_id:** PR-P2
**source → target:** global_38 (随机极限与不等式) → global_156 (随机矩阵特征值分析)
**continuity type:** Object continuity
**rule tag:** math_pr_object_continuity

**Evidence:**
- evolves_from weight: 0.4077 (from main `data/output/topic_graph.json`)
- adjacency weight: 0.4077 (from both main graph and PR-targeted export)
- Both graph sources agree; the equal weights suggest the adjacency and evolves_from edges share underlying scoring

**Period activity:**
- global_38: first active 2025-02, last active 2025-03 (2 periods, 208 papers)
- global_156: first active 2025-06, last active 2025-09 (2 periods, 78 papers)
- Chronology type: strict succession

**Continuity rationale:** global_38 and global_156 share the random matrix object domain. global_38 covers limit laws and probability inequalities; global_156 covers eigenvalue distribution analysis. The evolution from aggregate probabilistic bounds toward spectral analysis is a recognizable object-preserving transition within random matrix theory.

**Known weaknesses:**
- global_38 transience risk (R1, same as P1).
- Shared evolves_from and adjacency weights being identical (0.4077) warrants verification that these are not artefacts of the same underlying scoring computation.
- Paper-level review has not been performed.

**Curation status:** curated positive candidate (Tier A — two-source: evolves_from + adjacency)

---

### Tier B (Conditional — Require Paper-Level Confirmation)

Tier B positives have only a single graph source. They are included as curated positive candidates but require additional evidence (paper-level review or second graph source) before being treated as reliable benchmark anchors.

---

#### PR-P3: global_38 → global_99

**pair_id:** PR-P3
**source → target:** global_38 (随机极限与不等式) → global_99 (随机游走与分支)
**continuity type:** Object continuity
**rule tag:** math_pr_object_continuity

**Evidence:**
- evolves_from weight: 0.39 (from main `data/output/topic_graph.json`)
- adjacency weight: null — NO adjacency edge in either graph for this pair

**Period activity:**
- global_38: first active 2025-02, last active 2025-03 (2 periods, 208 papers)
- global_99: first active 2025-04, last active 2026-02 (3 periods, 179 papers)
- Chronology type: strict succession

**Continuity rationale:** Both topics operate within the probability space of discrete stochastic processes. global_38 covers limit theorems and inequalities applicable to random walk settings; global_99 covers random walk and branching process behavior. The evolves_from edge suggests a directional lineage, though the absence of an adjacency edge means the topical overlap is not corroborated by keyword co-occurrence at the adjacency threshold.

**Known weaknesses:**
- Single-source evidence (evolves_from only, no adjacency). Lower confidence than P1/P2.
- global_38 transience risk (R1).
- Absence of adjacency edge may indicate the topical overlap is weaker than it appears from the evolves_from edge alone.
- Paper-level review has not been performed.

**Curation status:** curated positive candidate (Tier B — single-source: evolves_from only)

---

#### PR-P4: global_65 → global_188

**pair_id:** PR-P4
**source → target:** global_65 (随机微分方程收敛) → global_188 (随机粗糙McKean方程)
**continuity type:** Method continuity
**rule tag:** math_pr_method_continuity

**Evidence:**
- evolves_from weight: null — NO evolves_from edge in main topic_graph.json for this pair
- adjacency weight: 0.4795 (strongest adjacent pair in the PR candidate pool; from PR-targeted export)

**Period activity:**
- global_65: first active 2025-03, last active 2025-10 (4 periods, 391 papers)
- global_188: first active 2025-07, last active 2026-02 (4 periods, 387 papers)
- Chronology type: concurrent (overlapping activity periods, not strict succession)

**Continuity rationale:** global_65 covers classical SDE convergence methods; global_188 covers rough path extensions (rough McKean-Vlasov equations). The methodological lineage from classical SDE analysis to rough path theory is a well-established trajectory in stochastic analysis. The adjacency weight (0.4795) is the highest in the PR candidate pool and indicates strong topical co-occurrence.

**Known weaknesses:**
- Adjacency-only evidence (no evolves_from). Method continuity is harder to verify without directional graph evidence (R2).
- Concurrent activity periods (global_65 and global_188 are active simultaneously). This reduces confidence that global_65 is a true predecessor and increases the possibility of parallel development rather than sequential evolution.
- PR/AP boundary risk: both global_65 and global_188 may have strong ties to applied mathematics (math.AP) given the McKean-Vlasov framing (R3).
- Paper-level review has not been performed.

**Curation status:** curated positive candidate (Tier B — adjacency-only: bw=0.4795)

**PR-TrackB-03 (2026-03-26): P4 DEMOTED from Gate 2 directional candidate.**
Cluster-level review found: zero cross-citation in 2025 overlap window; founding-date inversion (rough McKean founded 2018, predates global_65 by 7 years); shared representative papers not McKean-Vlasov; non-overlapping author communities. Adjacency edge (bw=0.4795) consistent with BERTopic vocabulary artifact. P4 retained as calibration anchor for adjacency-weight threshold analysis only.

---

## 4. Curated Negative Cases

Negative cases establish the boundary of what math.PR object/method continuity is NOT. They serve as calibration anchors to prevent false positives during benchmark evaluation.

---

#### PR-N1: global_211

**pair_id:** PR-N1
**topic:** global_211 (种群适应与生态进化)
**strength:** STRONG negative

**Reason:** Biological evolutionary domain. This topic covers population adaptation and ecological evolution — a completely different scientific domain from probability theory. There is zero graph connectivity to PR core topics. No shared probabilistic objects or methods.

**Evidence:** Zero evolves_from edges, zero adjacency edges to PR internal topics. Biological vocabulary (population, fitness, ecological) does not overlap with stochastic analysis vocabulary.

**Curation status:** curated negative

---

#### PR-N2: global_47

**pair_id:** PR-N2
**topic:** global_47 (伊辛相变与临界)
**strength:** MODERATE negative

**Reason:** math.MP boundary case. Ising model and phase transition topics sit at the intersection of mathematical physics (math.MP) and probability theory. While percolation and Ising models share some vocabulary, global_47 is classified under math.MP and does not represent a PR object in the probability theory sense. Adjacency bw=0.2375 is below the meaningful threshold used for P1/P2/P4.

**Evidence:** adjacency bw=0.2375 (below threshold), no evolves_from edge. Classified as math.MP crossover.

**Curation status:** curated negative

---

#### PR-N3: global_61

**pair_id:** PR-N3
**topic:** global_61 (重交通环形排队)
**strength:** STRONG negative

**Reason:** Applied queueing theory — theoretical probability boundary. This topic covers heavy-traffic ring queueing, which is an applied operations research topic. It uses stochastic language but does not constitute theoretical probability research. Zero graph connectivity to PR internal topics.

**Evidence:** Zero evolves_from edges, zero adjacency edges to PR internal topics.

**Curation status:** curated negative

---

#### PR-N4: global_214

**pair_id:** PR-N4
**topic:** global_214 (随机矩阵与正定性)
**strength:** STRONG negative

**Reason:** math.RA domain — despite the name suggesting random matrices, global_214 is classified under math.RA (Ring and Algebra theory) and focuses on positive definiteness in an algebraic rather than probabilistic sense. Adjacency bw=0.1955 is very low.

**Evidence:** adjacency bw=0.1955 (low), no evolves_from edge. Domain: math.RA not math.PR.

**Curation status:** curated negative

---

#### PR-N5: global_333

**pair_id:** PR-N5
**topic:** global_333 (math.OC topic)
**strength:** MODERATE negative

**Reason:** math.OC domain. Despite a spurious evolves_from edge from global_65 (weight 0.3211), this topic belongs to optimal control (math.OC). The evolves_from edge is flagged as spurious — it likely reflects shared vocabulary between SDE methods and control theory rather than a genuine probability-to-probability evolution.

**Evidence:** spurious evolves_from from global_65 (weight 0.3211), adjacency 0.3211. The equal weights again suggest a potential scoring artefact similar to the P2 concern. Domain: math.OC not math.PR.

**Curation status:** curated negative

---

## 5. Ambiguous / Calibration Cases

Ambiguous cases have non-trivial graph evidence but cannot be confidently classified as positive or negative. They serve as calibration data for threshold sensitivity analysis.

---

#### PR-A1: global_65 ↔ global_39

**pair_id:** PR-A1
**pair:** global_65 (随机微分方程收敛) ↔ global_39 (随机过程渗流方程)
**adjacency weight:** 0.3327 (one-direction only)
**chronology:** concurrent periods

**Ambiguity:** Both are core PR topics with substantial paper counts (391 and 1280 respectively). They share stochastic vocabulary. However, they represent different mathematical objects (SDE convergence vs percolation). The one-directional adjacency and concurrent activity periods mean there is no clear temporal directionality. It is unclear whether this represents a genuine evolution, a parallel development, or simply topical co-occurrence.

**Curation status:** calibration ambiguous case

---

#### PR-A2: global_271 ↔ global_99

**pair_id:** PR-A2
**pair:** global_271 (渗流与随机行走临界性) ↔ global_99 (随机游走与分支)
**adjacency weight:** 0.3275 (one-direction only)
**chronology:** concurrent or reversed periods

**Ambiguity:** global_271 (percolation and random walk criticality) and global_99 (random walk and branching) share object-level vocabulary. However, the period ordering is either concurrent or potentially reversed — meaning global_271 may not clearly precede global_99. Without strict succession, the evolves_from semantics are ambiguous. The pair may represent parallel research threads rather than a directional evolution.

**Curation status:** calibration ambiguous case

---

## 6. Evidence Schema

### Field Definitions

| Field | Type | Description | Allowed Values |
|-------|------|-------------|----------------|
| `pair_id` | string | Unique identifier for this curated pair | PR-P1 through PR-A2 |
| `case_type` | enum | Classification category | `positive_tier_a`, `positive_tier_b`, `negative`, `ambiguous` |
| `continuity` | enum | Type of continuity (positive cases only) | `object`, `method`, `none`, `contested` |
| `evolves_from_wt` | float or null | Weight of evolves_from edge from main topic_graph.json | float in [0,1], or null if no edge |
| `adj_wt` | float or null | Adjacency weight (best available across graph sources) | float in [0,1], or null if no edge |
| `ev_count` | int | Number of independent graph evidence sources | 0, 1, or 2 |
| `chron_type` | enum | Temporal relationship between source and target periods | `strict_succ`, `concurrent`, `reversed`, `n/a` |
| `curation_status` | enum | Final curation classification | `curated_positive`, `curated_negative`, `calibration_ambiguous` |

**Note on `evolves_from_wt` source**: All evolves_from weights in this document come from `data/output/topic_graph.json` (main graph). The PR-targeted export (`data/output/math_discovery_pr_targeted/topic_graph.json`) contains only `adjacent_to` edges and was NOT used as a source for evolves_from weights.

**Note on `spurious` flag**: PR-N5 has an evolves_from edge marked as spurious. Spurious edges are those where the domain context (math.OC vs math.PR) makes a genuine probability-to-probability evolution implausible despite the edge existing in the graph.

### Evidence Summary Table — All 11 Cases

| pair_id | case_type | continuity | evolves_from_wt | adj_wt | ev_count | chron_type | curation_status |
|---------|-----------|------------|-----------------|--------|----------|------------|-----------------|
| PR-P1 | positive_tier_a | object | 0.39 | 0.35 | 2 | strict_succ | curated_positive [DEMOTED FINAL post-TrackB-06 (2026-03-29): category mismatch confirmed, founding-date inversion confirmed (arXiv:2402.08206 predates global_38), citation absent, cluster incoherent; calibration case] |
| PR-P2 | positive_tier_a | object | 0.4077 | 0.4077 | 2 | strict_succ | curated_positive [DEMOTED FINAL post-TrackB-06 (2026-03-29): merged into P1 (global_100=global_156); equal-weight confirmed taxonomy artifact (Jaccard 0.071–0.154); calibration case] |
| PR-P3 | positive_tier_b | object | 0.39 | null | 1 | strict_succ | curated_positive [HISTORICAL] — demoted post-TrackB-04 (single-source; identical representative papers; no adjacency) |
| PR-P4 | positive_tier_b | method | null | 0.4795 | 1 | concurrent | curated_positive [HISTORICAL] — demoted post-TrackB-03 (calibration-only) |
| PR-N1 | negative | none | null | null | 0 | n/a | curated_negative |
| PR-N2 | negative | none | null | 0.2375 | 0 | n/a | curated_negative |
| PR-N3 | negative | none | null | null | 0 | n/a | curated_negative |
| PR-N4 | negative | none | null | 0.1955 | 0 | n/a | curated_negative |
| PR-N5 | negative | none | 0.3211* | 0.3211 | 0 | n/a | curated_negative |
| PR-A1 | ambiguous | contested | null | 0.3327 | 1 | concurrent | calibration_ambiguous |
| PR-A2 | ambiguous | contested | null | 0.3275 | 1 | concurrent | calibration_ambiguous |

*PR-N5 evolves_from weight marked as spurious (cross-domain edge, math.OC source).

---

## 7. Readiness for PR Graph Integration Discussion

### Does the curated set meet MPR-02 completion criteria?

**YES**, with the following specifics:

- **Positive cases**: 4 curated positive candidates (requirement: >= 3). Includes 2 Tier A (two-source) and 2 Tier B (single-source).
- **Negative cases**: 5 curated negatives (requirement: >= 2). Includes 3 STRONG negatives (N1, N3, N4) and 2 MODERATE negatives (N2, N5).
- **Ambiguous cases**: 2 calibration ambiguous cases (requirement: >= 1).
- **Vocabulary check**: All positive candidates use domain-specific vocabulary (eigenvalues, matrices, percolation, martingale, rough paths). None rely on generic terms (stochastic, random, probability) as the primary distinguishing feature.
- **Chronological check**: P1, P2, P3 have strict succession. P4 has concurrent periods (noted as a risk).

**Historical MPR-02 note (2026-03-21):** At the time of curation, the curated set was judged sufficient to proceed to the next phase. This historical readiness judgment was later superseded by the Track B review chain, which culminated in PR-TrackB-06 (2026-03-29) and collapsed Gate 2.

### Is math.PR ready for conditional graph integration discussion?

**Historical MPR-02 conclusion (2026-03-21):** YES — CONDITIONAL. At the time of this curation, the curated set satisfied MPR-02 completion criteria and supported a conditional readiness decision for math.PR graph integration. Three residual risks (R1, R2, R3) were identified for Track B resolution.

**Current status (post-TrackB-06, 2026-03-29):** Gate 2 COLLAPSED. All Track B review work is complete:
- All 4 Gate 2 candidates demoted (P4: TrackB-03, P3: TrackB-04, P1/P2: TrackB-05/06).
- R1 RESOLVED (negative): global_38 does not evolve into RMT/concentration cluster (PR-TrackB-06, 2026-03-29).
- R2 RESOLVED (negative): global_65→global_188 directionality absent (PR-TrackB-03, 2026-03-26).
- R3 RESOLVED: both topics PR-dominant (PR-TrackB-01, 2026-03-24).

math.PR is at long-term Gate 1. The conditional integration layer (`data/output/kg_v1_pr_conditional/`) is implemented and stable. Baseline inclusion (Gate 2) requires new directional evidence — no current path is open. The MPR-02 historical curation (positive cases, negative cases, calibration cases) retains value as calibration anchors for future reviews.

---

## 8. Residual Risk

### R1: global_38 Transience

**Track B status (PR-TrackB-01):** PARTIALLY_MITIGATED. global_38 exhibits 5-descendant generativity and 2.4x paper growth. global_99 confirmed multi-period. Risk reduced from critical to moderate. Full mitigation requires paper-level verification of global_38 paper identity.

**Track B status (PR-TrackB-04, 2026-03-27):** PARTIALLY_RESOLVED at title-level. P3 DEMOTED (identical representative papers; no adjacency; single-source). P1/P2 PROVISIONALLY RETAINED pending Level 3 abstract+citation review. Gate 2 path PARTIALLY VIABLE via P1+P2.

**Track B status (PR-TrackB-05, 2026-03-28):** global_100 and global_156 confirmed NOT RELIABLY DISTINCT (5/5 identical representative papers, bw=0.475). P1 CONDITIONALLY DEMOTED. P2 MERGED INTO P1, CONDITIONALLY DEMOTED. Gate 2 reduced to single-candidate heightened concern. PR-TrackB-06 (abstract+citation) required for final verdict.

global_38 (随机极限与不等式) is the source node for three of the four positive candidates (P1, P2, P3). It has only 2 active periods (2025-02 and 2025-03), which is the minimum for multi-period classification.

**Risk:** A topic with only 2 active periods is more susceptible to reclassification if the data window shifts or if the topic alignment changes. If global_38 is reclassified as single-period or merged with another topic in a future data update, P1, P2, and P3 would all lose their source node simultaneously — eliminating 75% of the curated positive candidates.

**Mitigation:** Paper-level review of global_38 to confirm it represents a genuine, distinct research topic with durable existence. If confirmed, document the specific papers that establish its identity.

### R2: P4 Adjacency-Only Fragility

**Track B status (PR-TrackB-03, 2026-03-26):** RESOLVED (negative, search-bounded). Six independent cluster-level findings confirm global_65 and global_188 are parallel 2025 research communities, not sequential evolution. Zero cross-citation found in 2025 overlap window (abstract+citation scope). Rough McKean field predates global_65 by 7 years (arXiv:1802.05882, 2018). Shared representative papers not McKean-Vlasov content. Non-overlapping author communities. Adjacency edge (bw=0.4795) consistent with BERTopic vocabulary artifact. P4 demoted from Gate 2 directional set; retained as calibration anchor. Gate 2 path via P1/P2/P3 (global_38-family).

**Prior Track B status (PR-TrackB-02, 2026-03-25):** PARTIALLY_MITIGATED. Field-level mathematical lineage confirmed at abstract+citation level. Cluster-level directionality not confirmed.

**Prior Track B status (PR-TrackB-01, 2026-03-24):** NOT_MITIGATED. Title-level review found identical representative papers across global_65 and global_188, and no evolves_from edge.

PR-P4 (global_65 → global_188) has no evolves_from edge in the main topic graph. It relies exclusively on the adjacency weight (0.4795) from the PR-targeted export.

**Risk:** Adjacency edges indicate topical co-occurrence but do not encode temporal directionality. Without an evolves_from edge, there is no graph-level signal that global_65 preceded global_188. The concurrent activity periods of both topics (global_65 active 2025-03 to 2025-10, global_188 active 2025-07 to 2026-02) further reduce confidence in a directional claim. P4 may represent parallel development rather than sequential evolution.

**Mitigation:** Paper-level review to establish whether specific papers in global_65 are cited by papers in global_188, or whether the methodological transition (classical SDE to rough paths) is explicitly articulated in the literature.

### R3: PR/AP Boundary for P4 Nodes

**Track B status (PR-TrackB-01):** RESOLVED. global_65 PR-dominant (HIGH confidence). global_188 PR-dominant with dual-class caveat for SPDE well-posedness component (MEDIUM confidence). Not a misclassification.

global_65 (随机微分方程收敛) and global_188 (随机粗糙McKean方程) both involve stochastic differential equations, which are a shared domain between mathematical probability (math.PR) and applied partial differential equations (math.AP).

**Risk:** If these topics are reclassified to math.AP in a future hierarchy update, or if their math.PR assignment is contested, P4's relevance to a math.PR-specific integration would be reduced. The McKean-Vlasov framing of global_188 in particular has strong connections to mean-field PDE literature typically classified under math.AP.

**Mitigation:** Verify the math.PR classification of both topics in the hierarchy metadata. If they have dual math.PR/math.AP assignments, document this explicitly and note the constraint in the integration plan.

---

## 9. Recommended Next Step

### Historical recommendation (MPR-02, 2026-03-21)

At the time of this curation, Option 2C (conditional graph integration planning) was recommended over Option 2D (full graph integration). Option 2C was subsequently implemented as PR-2C-impl (2026-03-23) and is complete.

### Current status (post-TrackB-06, 2026-03-29)

**Gate 2 COLLAPSED.** No current integration path is open. The recommended actions are:

1. **Monitor global_38→global_198** (branching RW with immigration; Jaccard ~0.4+; evolves_from weight 0.475). This is the genuine content heir identified by PR-TrackB-06. If global_198 develops sufficient directional signal in a future topic graph update, initiate TrackB-07.
2. **No code work required.** The conditional integration layer (PR-2C-impl) is stable. MPR-03 (PR benchmark runner) is not a current blocker — it becomes relevant only if a new Gate 2 candidate is identified.
3. **Do not initiate new TrackB reviews** without new directional evidence. The TrackB-01 through TrackB-06 chain is complete and closed.
