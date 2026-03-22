---
doc_type: "title_level_graph_structural_identity_audit"
scope: "math.PR P1/P2 Level 3 pre-review — PR-TrackB-05 (title-level + graph-structural identity audit; NOT completed abstract/citation review)"
status: "COMPLETE — P1/P2 CONDITIONALLY DEMOTED; global_100/global_156 NOT RELIABLY DISTINCT; Gate 2 SINGLE-CANDIDATE HEIGHTENED CONCERN"
owner: "review-worker"
package_id: "PR-TrackB-05"
date: "2026-03-28"
upstream_docs:
  - "docs/plans/2026-03-27-math-pr-track-b-global38-review.md"
  - "docs/plans/2026-03-26-math-pr-track-b-cluster-review.md"
  - "docs/plans/2026-03-23-math-pr-phase-2c-implementation.md"
  - "docs/plans/2026-03-21-math-pr-case-curation.md"
downstream_docs:
  - "docs/plans/2026-03-29-math-pr-track-b-merged-candidate-review.md"
last_reviewed: "2026-03-28"
---

# math.PR Track B P1/P2 Level 3 Pre-Review — PR-TrackB-05 (Title-Level + Graph-Structural Identity Audit)

**Date:** 2026-03-28
**Package:** PR-TrackB-05
**Status:** COMPLETE — P1/P2 CONDITIONALLY DEMOTED; global_100/global_156 NOT RELIABLY DISTINCT; Gate 2 SINGLE-CANDIDATE HEIGHTENED CONCERN

---

## 1. Executive Summary

PR-TrackB-04 (2026-03-27) provisionally retained P1 (global_38 → global_100) and P2 (global_38 → global_156) at title-level + graph-structural resolution and demoted P3. PR-TrackB-05 is the Level 3 review tasked with strengthening the evidence for P1 and P2 through deeper structural analysis and identity verification.

**Evidence level ceiling for this review:** Title-level + graph-structural. This review did NOT access paper abstracts, citation lists, arXiv IDs, or author community data. What IS new relative to PR-TrackB-04: identity confirmation of global_100 vs global_156 has been completed at title-level — 5/5 representative papers confirmed identical across the two clusters.

**Summary of outcomes:**

- **global_100 / global_156 identity:** CONFIRMED NOT RELIABLY DISTINCT (FINAL at title-level). 5/5 identical representative papers; inter-cluster adjacency bw=0.475; equal paper counts. Global_100 and global_156 are not reliably distinct clusters. They represent a BERTopic bisection of a single merged RMT/concentration cluster.
- **P1 (global_38 → global_100):** CONDITIONALLY DEMOTED — not removed. Demotion converts to final if PR-TrackB-06 confirms founding-date inversion and citation signal absence at abstract level. Key concerns: identity collapse (P1 and P2 now point to the same merged cluster), founding-date pressure (RMT fields 30-70 years old relative to global_38's 2025 cluster), category mismatch concern (global_38 is classical random walks; "matrices" keyword may be Markov chain / transition matrix notation, not RMT), citation signal ABSENT at title-level reasoning.
- **P2 (global_38 → global_156):** MERGED INTO P1, CONDITIONALLY DEMOTED. P2 has no independent existence because global_100 = global_156 (not reliably distinct). The equal-weight concern (evolves_from wt=0.4077 = adjacency bw=0.4077) further weakens the source independence claim; treat as 1.5 effective sources.
- **Gate 2 path:** SINGLE-CANDIDATE HEIGHTENED CONCERN. Prior two-candidate structure (P1+P2) is eliminated by the identity finding. The single remaining candidate path is global_38 → merged_RMT_concentration_cluster, conditionally viable pending PR-TrackB-06.

**What is new vs PR-TrackB-04:**
- Identity of global_100 and global_156 is NOW CONFIRMED (not suspected) at title-level: 5/5 representative papers are identical.
- P2 has no independent target cluster — it is not a separate Gate 2 candidate.
- Category mismatch concern has been strengthened by analysis of global_38's representative paper titles (all 5 concern classical random walks and branching processes, not random matrix theory).
- False cognate analysis has been completed: "Chernoff bounds," "quenched," and "correlation functions" in the cluster vocabularies are confirmed as false cognates relative to citation linkage.

---

## 2. Evidence Level and Methodology

### Evidence available to this review

This review had access to:
- 5 representative paper titles per topic (BERTopic cluster representatives, title-level only)
- Graph edges from `data/output/topic_graph.json`: evolves_from weights, adjacency weights
- Keyword sets per topic (BERTopic-derived)
- Period activity data (first/last active period, paper counts)
- Inter-cluster adjacency for global_100 ↔ global_156

### What was NOT available

- Paper abstracts (not accessed — no arXiv IDs used, no abstract text reviewed)
- Citation lists (not accessed — no reference list review, no cross-citation mapping performed)
- Author community data (not accessed)
- Founding-date data from primary sources (only background knowledge used; NOT confirmed at abstract level)

### Evidence level comparison across PR TrackB reviews

| Review | Evidence Level | Key Coverage | New vs Prior |
|--------|---------------|--------------|--------------|
| PR-TrackB-01 (2026-03-24) | Title-level | 5 representative paper titles per topic; no per-paper attribution; no abstracts | Baseline title-level review |
| PR-TrackB-02 (2026-03-25) | Field-level (abstract+citation) | Abstract+citation review of seminal papers; confirmed field-level mathematical lineage for P4 | External arXiv evidence for R2 |
| PR-TrackB-03 (2026-03-26) | Cluster-level (abstract+citation) | Specific 2025 papers within global_65 and global_188; cross-citation mapping; author community analysis | Full cluster-level for P4; led to demotion |
| PR-TrackB-04 (2026-03-27) | Title-level + graph-structural | 5 representative paper titles; evolves_from and adjacency edges; keyword analysis; graph topology | P3 demoted; P1/P2 provisionally retained |
| PR-TrackB-05 (2026-03-28) | Title-level + graph-structural | Global_100/global_156 identity audit (5/5 representative papers confirmed identical); false cognate analysis; founding-date background assessment | Identity CONFIRMED; P1/P2 CONDITIONALLY DEMOTED; Gate 2 SINGLE-CANDIDATE HEIGHTENED CONCERN |

PR-TrackB-05 operates at the same evidence ceiling as PR-TrackB-04 and PR-TrackB-01. The identity confirmation (5/5 identical papers for global_100 and global_156) IS a valid title-level finding. The founding-date pressure and category mismatch concern are assessed at background-knowledge level only — they are NOT confirmed findings and require abstract+citation verification in PR-TrackB-06.

---

## 3. global_38 Representative Paper Analysis

### The 5 representative papers for global_38

1. "Chernoff bounds for branching random walks"
2. "Sharp asymptotics for N-point correlation functions of coalescing heavy-tailed random walk"
3. "Ergodic Theorems for Random Walks in Random Environments"
4. "Some old and basic facts about random walks on groups"
5. "Population size of critical Galton-Watson processes under small deviations and infinite variance"

### Assessment: global_38 is a classical random walk cluster

All 5 representative papers concern classical discrete probability theory:

- Papers 1, 2, 3, 5 directly address random walks and branching processes (Galton-Watson processes are the canonical branching process model).
- Paper 4 ("old and basic facts about random walks on groups") is an explicit reference to classical random walk theory on groups — the word "old" signals this is foundational/historical material, not frontier spectral probability.
- Paper 2's "N-point correlation functions" refers to particle correlation in coalescing random walk systems, not spectral statistics or random matrix correlation functions.
- Paper 1's "Chernoff bounds for branching random walks" concerns probability tail inequalities in a branching walk setting, not random matrix concentration inequalities.

**Conclusion:** global_38 is unambiguously a classical random walk / branching process cluster. There is no RMT content in these 5 titles.

### The "matrices" keyword concern

global_38 keywords include: convergence, g_n, **matrices**, walk, infty, leq, random, x_n, frac, limit, prove, branching, mathbb, asymptotic, probability.

The "matrices" keyword in global_38 is anomalous given the representative paper content. Two interpretations are possible:

1. **Transition matrix notation:** Random walks on groups are often analyzed via transition matrices (matrices of transition probabilities). The word "matrices" in this context refers to Markov chain transition matrices, not random matrix ensembles. This is the more plausible interpretation given the representative paper content.

2. **Vocabulary spillover artifact:** BERTopic may have captured vocabulary from papers tangentially adjacent to the random walk cluster that use matrix notation in a non-RMT context.

**Assessment:** The "matrices" keyword does NOT confirm that global_38 is an RMT cluster. The representative paper analysis contradicts an RMT interpretation. The term is more consistent with Markov chain transition matrix notation in a classical random walk setting. This is a key category mismatch concern for P1/P2: if global_38's "matrices" vocabulary refers to transition matrices rather than random matrix ensembles, the vocabulary bridge between global_38 and global_100/global_156 is weaker than PR-TrackB-04 assumed.

---

## 4. P1 Review (global_38 → global_100)

### Evidence summary

| Field | Value |
|-------|-------|
| Pair ID | PR-P1 |
| Edge type | evolves_from wt=0.39 (primary) + adjacency bw=0.35 (corroborating) |
| Evidence count | 2 (two-source) |
| Chronology | Strict succession: global_38 active 2025-02/03; global_100 active 2025-04+ |
| Temporal gap | 1 month (2025-03 → 2025-04) |

### global_100 representative papers

1. "Variational Tail Bounds for Norms of Random Vectors and Matrices"
2. "The Magmoid of Normalized Stochastic Kernels"
3. "A categorical account of the Metropolis-Hastings algorithm"
4. "Quenched properties of the Spectral Form Factor"
5. "Operation with Concentration Inequalities"

### global_100 representative paper analysis

The 5 representative papers for global_100 cover concentration inequalities, spectral statistics, and categorical probability:

- Paper 1 ("Variational Tail Bounds"): concentration inequalities for random vectors/matrices — this is an RMT-adjacent concentration inequality result, but the "variational" framing is specific and distinct from classical random walk inequalities.
- Paper 2 ("Magmoid of Normalized Stochastic Kernels"): algebraic/categorical structure of Markov kernels — this is abstract probability theory, not a random walk or RMT paper in the classical sense.
- Paper 3 ("Categorical account of Metropolis-Hastings"): categorical probability / MCMC theory — a category-theory perspective on Markov chain Monte Carlo, not classical random walks or RMT.
- Paper 4 ("Quenched properties of Spectral Form Factor"): spectral statistics — "quenched" refers to a disorder-averaging technique in random matrix / quantum chaos settings, NOT the same as "quenched" in random walk in random environment (RWRE). This is a FALSE COGNATE relative to global_38's random walk content.
- Paper 5 ("Operation with Concentration Inequalities"): concentration inequalities — related to Paper 1's theme.

### False cognate identification for P1

**"Quenched" (Paper 4 in global_100 vs global_38's RWRE content):** In global_38, the paper "Ergodic Theorems for Random Walks in Random Environments" concerns quenched (almost-sure, per environment realization) vs annealed (averaged) behavior in RWRE theory. In global_100's Paper 4, "Quenched properties of the Spectral Form Factor" uses "quenched" in the random matrix / quantum chaos sense (disorder average over random Hamiltonians). These are the same word used in two different mathematical disciplines. The shared vocabulary does not confirm intellectual citation linkage between global_38 and global_100.

**"Chernoff bounds" (global_38 Paper 1 vs global_100 concentration themes):** Chernoff bounds in the context of branching random walks (global_38) concern tail probabilities for sums of random variables in a branching structure. Concentration inequalities in global_100 (Papers 1 and 5) concern operator norms and spectral concentration. The vocabulary overlap ("bounds," "concentration," "tail") is domain-general probability terminology, not a citation-specific linkage.

### Category mismatch concern for P1

PR-TrackB-04 found that global_38 (random walks) and global_100 (random matrix ensembles / concentration) are different mathematical objects and recommended reclassifying the edge from "object_continuity" to "domain_bridge / cross-subfield evolution." PR-TrackB-05 strengthens this concern:

- global_38's 5 representative papers contain no RMT content.
- global_38's "matrices" keyword is more consistent with transition matrix notation than with random matrix ensemble vocabulary.
- global_100's representative papers include categorical probability (Papers 2, 3) and spectral statistics (Paper 4) content that is conceptually distant from global_38's classical random walk material.
- The domain bridge interpretation (classical probability → spectral/categorical probability) is plausible at a high level, but the specific paper content suggests the connection may be a vocabulary artifact rather than a genuine citation-level intellectual succession.

### Founding-date pressure for P1

Background knowledge strongly suggests that the mathematical fields represented in global_100 predate global_38's 2025 cluster:

- Random matrix theory (RMT) has foundational papers from the 1950s-1960s (Wigner 1955, Dyson 1962). The modern spectral concentration inequality literature builds on this foundation. This means the "target" field represented by global_100's spectral statistics papers is 60-70 years older than the "source" cluster global_38 (2025).
- Concentration inequalities as a field (Talagrand, Ledoux) date to the 1990s — approximately 30 years before global_38's 2025 activity window.
- If global_100 represents 2025 papers that continue a mathematical tradition 30-70 years old, the founding-date argument against "global_38 generated global_100" is strong — the target field was well-established long before the source cluster appeared.

**Qualification:** This founding-date pressure is assessed at background-knowledge level. The specific arXiv founding dates for global_100's representative papers have NOT been verified. This is NOT a confirmed finding — it is a concern that PR-TrackB-06 must test at abstract+citation level.

### Verdict for P1

**CONDITIONALLY DEMOTED** — not removed from consideration.

The conditional demotion is based on three converging concerns:
1. Identity collapse: global_100 and global_156 are NOT RELIABLY DISTINCT — P1 and P2 now point to the same merged cluster, reducing the independent evidence from two cases to one.
2. Category mismatch: global_38 is a classical random walk cluster; global_100 is a spectral/categorical probability cluster; the "matrices" bridge vocabulary may be transition matrix notation, not RMT.
3. Citation signal absent at title-level reasoning, strengthened by false cognate analysis.

The demotion converts to final if PR-TrackB-06 confirms: (A) category mismatch (global_38 papers do not cite global_100 papers); (B) founding-date inversion (global_100 representative papers have pre-2025 founding dates); (C) citation linkage is absent at abstract level.

The demotion does NOT become final automatically. If PR-TrackB-06 finds positive citation linkage and rejects the founding-date inversion, P1 reverts to provisionally retained.

---

## 5. P2 Review (global_38 → global_156)

### Evidence summary

| Field | Value |
|-------|-------|
| Pair ID | PR-P2 |
| Edge type | evolves_from wt=0.4077 (primary) + adjacency bw=0.4077 (corroborating) |
| Evidence count | Nominally 2 (two-source), assessed as 1.5 effective sources |
| Chronology | Strict succession: global_38 active 2025-02/03; global_156 active 2025-06+ |
| Temporal gap | 3 months (2025-03 → 2025-06) |

### Primary verdict: MERGED INTO P1

P2 has no independent existence as a Gate 2 candidate. The identity audit (Section 6) confirms that global_100 and global_156 are NOT RELIABLY DISTINCT — they share 5/5 representative papers, have an inter-cluster adjacency of bw=0.475, and have equal paper counts. Whatever target cluster global_156 nominally represents is the same entity as global_100.

Therefore, P2 (global_38 → global_156) and P1 (global_38 → global_100) both point to the same merged RMT/concentration cluster. P2 is not an independent second Gate 2 candidate — it is P1 restated with a different target cluster label.

### Secondary verdict: CONDITIONALLY DEMOTED by merger

Because P2 merges into P1, P2 inherits P1's conditional demotion. All concerns identified in Section 4 (category mismatch, founding-date pressure, false cognates, citation signal absence) apply to the merged cluster and therefore to P2's demotion as well.

### global_156 representative papers (identical to global_100)

1. "Variational Tail Bounds for Norms of Random Vectors and Matrices"
2. "The Magmoid of Normalized Stochastic Kernels"
3. "A categorical account of the Metropolis-Hastings algorithm"
4. "Quenched properties of the Spectral Form Factor"
5. "Operation with Concentration Inequalities"

The keywords for global_156 differ from global_100 (fourier, matrix, operatorname, eigenvalues, matrices, log, entries, mccm, random, ensembles, ginibre, frac, inequality, inequalities, mathbb). The keyword difference is explained by BERTopic's noisy bisection of what is effectively one cluster into two topic IDs, each capturing a different vocabulary subset while drawing representative papers from the same underlying paper pool.

---

## 6. global_100 / global_156 Identity Audit

### Supporting evidence for "NOT RELIABLY DISTINCT"

**Finding 1 (DECISIVE): 5/5 identical representative papers.** The 5 representative papers assigned by BERTopic to global_100 and global_156 are identical. In the BERTopic framework, representative papers are selected as the papers most central to each cluster's semantic space. If two clusters share all 5 representative papers, they are drawing from the same underlying semantic neighborhood — this is strong evidence that the two topic IDs represent the same research community.

**Finding 2: High inter-cluster adjacency bw=0.475.** The adjacency weight between global_100 and global_156 (bw=0.475) is higher than the P1 adjacency (bw=0.35) and equal to or higher than the P2 adjacency (bw=0.4077). This means global_100 and global_156 are more topically similar to each other than global_38 is to either of them. Topics this similar are more likely to be the same community under different labels than genuinely distinct research communities.

**Finding 3: Equal paper counts.** Both global_100 and global_156 have 78 papers each. Exact equal paper counts in two topics that share 5/5 representative papers is consistent with a BERTopic bisection that divided a single cluster's paper pool evenly across two topic IDs.

**Finding 4: Keyword overlap.** Shared keywords between global_100 and global_156 include: matrix, eigenvalues, matrices, random, ensembles, entries. The keyword differences (global_100: cumulants, rectangular, tensor, free; global_156: fourier, ginibre, log, mccm, inequality) are consistent with vocabulary subsets of a single RMT/concentration field rather than genuinely distinct sub-disciplines.

### Counter-evidence for "distinct" interpretation

**Counter 1: Different keyword sets.** global_100 and global_156 have distinct keywords. global_100 emphasizes ensemble/cumulant vocabulary (cumulants, ensembles, tensor, free); global_156 emphasizes spectral/inequality vocabulary (ginibre, fourier, inequality, inequalities). These could represent genuinely distinct sub-communities within the RMT/concentration space.

**Counter 2: Different graph outgoing edges.** global_100 has an outgoing evolves_from edge to global_276 (wt=0.3227); global_156 has an outgoing evolves_from edge to global_392 (wt=0.375). Different downstream descendants could indicate distinct cluster identities.

**Assessment of counter-evidence:** The counter-evidence is insufficient to override the decisive Finding 1 (5/5 identical representative papers). Different keyword subsets within the same cluster are expected under BERTopic bisection — a cluster split into two topic IDs will by construction assign different vocabulary weights to each ID. Different downstream evolves_from edges could reflect the different paper-subset composition of each half of the bisected cluster rather than genuinely different intellectual trajectories.

### Verdict: NOT RELIABLY DISTINCT (FINAL at title-level)

The identity verdict is FINAL at title-level. This is a confirmed finding, not a provisional concern. However, computational verification (full paper set comparison) has not been performed — a PR-TrackB-06 computational audit could in principle find non-overlapping paper sets that override the 5/5 representative paper identity. The FINAL qualifier applies to the current evidence level.

---

## 7. Equal-Weight Independence Audit (P2)

### The concern

P2 has evolves_from weight = 0.4077 and adjacency weight = 0.4077, exactly equal. This exact numerical equality raises the question of whether the two "independent" sources are actually the same underlying computation presented twice.

### SUSPICIOUS assessment

**Prior art:** PR-N5 (global_333 in the math.OC domain) also shows an equal-weight pattern (evolves_from = 0.3211, adjacency = 0.3211), and PR-N5 is the only other equal-weight case in the curated set. PR-N5 is a curated negative — the equal-weight pattern there is associated with a spurious cross-domain edge. The only other equal-weight case in the dataset is a confirmed negative, which provides circumstantial evidence that equal-weight cases may reflect a computational artifact rather than genuine two-source evidence.

**Treat as 1.5 effective sources:** P2's evolves_from weight (0.4077) and adjacency weight (0.4077) cannot be confirmed as independent without a computational audit of the scoring algorithms. Until confirmed, P2 should be treated as having 1.5 effective sources rather than 2 fully independent sources. This weakens P2's two-source classification but does not by itself trigger demotion.

**Computational audit required:** A full resolution of this concern requires tracing the computation provenance of both 0.4077 values back to the scoring code. This is a PR-TrackB-06 task (Q-D).

---

## 8. Citation Signal Analysis

### Method

At title-level reasoning, citation signal is assessed by examining whether the representative paper titles of the source cluster (global_38) and the target cluster (global_100/global_156) contain vocabulary that would indicate citation linkage — that is, whether the downstream cluster's papers appear to build on, respond to, or explicitly extend the upstream cluster's research tradition.

This is NOT a confirmed citation finding. It is a title-level reasoning exercise. The actual citation lists have not been accessed.

### Paper-by-paper analysis

**global_38 papers vs global_100/global_156 papers:**

| global_38 Paper | Expected Citation Target? | Assessment |
|----------------|--------------------------|------------|
| "Chernoff bounds for branching random walks" | Would cite concentration inequality papers? | FALSE COGNATE — Chernoff bounds in branching walk settings ≠ operator norm concentration. Not a strong citation link indicator. |
| "Sharp asymptotics for N-point correlation functions of coalescing heavy-tailed random walk" | Would cite spectral form factor or matrix papers? | FALSE COGNATE — "N-point correlation functions" here refers to particle correlation in random walk systems, not spectral statistics correlation functions. |
| "Ergodic Theorems for Random Walks in Random Environments" | Would cite quenched spectral papers? | FALSE COGNATE — "quenched" in RWRE ≠ "quenched" in spectral form factor. Different disciplines sharing a word. |
| "Some old and basic facts about random walks on groups" | Would cite categorical probability or Metropolis-Hastings? | IMPLAUSIBLE — a paper about "old and basic facts" in classical random walk theory would not typically cite frontier categorical probability work. |
| "Population size of critical Galton-Watson processes" | Would cite variational tail bounds or concentration inequalities? | POSSIBLE but WEAK — probabilistic tail bound techniques span disciplines, but Galton-Watson process papers typically cite branching process literature, not RMT concentration literature. |

### Verdict: Citation signal ABSENT at title-level reasoning

The title-level reasoning does not support citation linkage between global_38's representative papers and global_100/global_156's representative papers. Three of five pairs involve false cognates (shared vocabulary with different disciplinary meanings). One pair is implausible on intellectual grounds. One pair is possible but weak.

**Important qualification:** This is NOT "cross-citation confirmed absent." The actual citation lists have not been accessed. This verdict is: citation signal absent at title-level reasoning. It is possible that global_38 papers do cite global_100/global_156 papers — abstract+citation review is required to confirm or rebut this assessment.

---

## 9. Founding-Date and Category Assessment

### Founding-date concern

The founding-date pressure for P1/P2 concerns the possibility that the mathematical traditions represented by global_100/global_156 predate global_38's 2025 activity window. If the "target" field (RMT / concentration inequalities) is 30-70 years older than the "source" cluster (global_38, active 2025-02/03), then the directional claim "global_38 → merged RMT cluster" faces the same founding-date inversion problem that led to P4's demotion.

**Background knowledge assessment:**
- Random matrix theory (Wigner semi-circle, Dyson ensembles): 1950s-1960s — approximately 60-70 years before global_38's 2025 cluster.
- Concentration inequalities (Talagrand, Ledoux, Milman): 1990s — approximately 30 years before global_38.
- The specific papers in global_100/global_156 are 2025 papers, but they continue traditions 30-70 years old.

The founding-date pressure here is STRONGER than P4's case. P4's rough McKean-Vlasov field predated global_65 by 7 years (founding: 2018). The RMT/concentration fields represented by global_100/global_156 predate global_38 by at minimum 30 years. This is a substantially more severe temporal asymmetry.

**Critical qualification:** This is assessed at background-knowledge level only. It has NOT been confirmed at abstract level. The specific arXiv IDs for global_100/global_156 papers have not been examined. The founding dates of those specific 2025 papers' lineages have not been verified. This background-knowledge assessment must be tested in PR-TrackB-06.

**How this differs from P4:** P4's founding-date inversion was confirmed at abstract+citation level (arXiv:1802.05882 confirmed 2018 rough McKean founding, predating global_65 by 7 years). P1/P2's founding-date pressure is background knowledge, not confirmed arXiv evidence. The concern is stronger in magnitude (30-70 years vs 7 years) but the evidence level is lower (background knowledge vs confirmed arXiv abstract). This asymmetry means the founding-date pressure is a serious concern but not yet a confirmed demotion factor.

### Category mismatch concern

Global_38's 5 representative papers are classical random walks and branching processes. Global_100/global_156's representative papers include spectral statistics, categorical probability, and concentration inequalities. These are different mathematical subfields within probability theory.

The category mismatch concern is stronger than the founding-date concern because it is based on direct title analysis rather than background knowledge:
- global_38 representative papers: ALL concern random walks, branching processes, or Galton-Watson processes.
- global_100/global_156 representative papers: NONE concern random walks or branching processes directly.
- The vocabulary bridge ("matrices" in global_38) is more consistent with Markov chain transition matrix notation than with random matrix ensemble notation.

The category mismatch concern does not definitively demote P1/P2 — a vocabulary-level domain bridge from classical probability to spectral probability is possible. But it substantially reduces confidence in the directional claim.

---

## 10. Gate 2 Reassessment

### Prior structure (PR-TrackB-04): TWO-CANDIDATE PATH

As of PR-TrackB-04, Gate 2 had a two-candidate directional path:
- P1 (global_38 → global_100): provisionally retained, secondary candidate
- P2 (global_38 → global_156): provisionally retained, primary candidate

This structure was contingent on global_100 and global_156 being genuinely distinct.

### Current structure (PR-TrackB-05): SINGLE-CANDIDATE HEIGHTENED CONCERN

The identity finding (global_100 = global_156, NOT RELIABLY DISTINCT) eliminates the two-candidate structure. P1 and P2 are now the same directional claim: global_38 → merged_RMT_concentration_cluster.

**Gate 2 path status: SINGLE-CANDIDATE HEIGHTENED CONCERN**

A single-candidate Gate 2 path is inherently weaker than a two-candidate path. If this single candidate is demoted in PR-TrackB-06, Gate 2 is blocked entirely for the global_38-family. Alternative Gate 2 candidates (from other parts of the math.PR topic graph) would need to be identified.

### Conditions required for Gate 2 to advance (C1-C4)

**C1 (Category mismatch confirmation/rebuttal):** PR-TrackB-06 must determine whether global_38 papers (at abstract level) build on or cite RMT/concentration literature. If the category mismatch is confirmed (global_38 is purely classical random walk, no RMT content at abstract level), the directional claim is weakened. If the category mismatch is rebutted (global_38 abstracts contain genuine RMT vocabulary), the claim is strengthened.

**C2 (Founding-date confirmation/rebuttal):** PR-TrackB-06 must examine the specific arXiv papers in global_100/global_156 for founding dates. If the founding dates confirm 30-70 year temporal inversion, the conditional demotion converts to final. If the founding dates show that the specific 2025 papers represent NEW mathematical developments not established before 2025, the founding-date pressure is mitigated.

**C3 (Citation linkage check):** PR-TrackB-06 must check whether global_100/global_156 papers (2025-04+ and 2025-06+ respectively) cite global_38 papers (2025-02/03). Presence of citation linkage would support P1/P2 retention. Absence of citation linkage (as in P4's case) would trigger final demotion.

**C4 (Equal-weight computational audit for P2):** PR-TrackB-06 should trace the computation provenance of the P2 equal-weight (0.4077 = 0.4077). If the two weights are confirmed as independent computations, P2 (merged into P1) retains its two-source classification. If they are the same computation, P2 has one effective source, further weakening the merged candidate.

### Alternative Gate 2 candidates

If PR-TrackB-06 demotes P1/P2 as a merged candidate, Gate 2 for math.PR would require alternative directional candidates. The current candidate set does not include any remaining provisionally retained candidates — P3 was demoted in PR-TrackB-04 and P4 in PR-TrackB-03. Identifying alternative candidates would require a new curation pass over the math.PR topic graph.

PR-TrackB-06 must also address Question Q-E: whether any alternative Gate 2 candidates exist in the math.PR topic graph that could substitute for the global_38-family path if P1/P2 are finally demoted.

---

## 11. Residual Uncertainty

The following questions remain open after PR-TrackB-05 and must be answered by PR-TrackB-06:

**Q-A (Category mismatch confirmation/rebuttal):** At abstract level, do global_38 papers contain genuine RMT vocabulary? Do they cite RMT/concentration literature? The title-level analysis suggests global_38 is purely classical random walk, but titles alone are insufficient to determine abstract-level content.

**Q-B (Founding-date confirmation/rebuttal):** Do the specific 2025 papers in global_100/global_156 belong to mathematical traditions established before 2025? Can specific arXiv founding dates be identified for the representative papers? The background knowledge assessment suggests 30-70 year founding-date pressure, but this requires abstract-level confirmation.

**Q-C (Citation linkage check):** Do global_100/global_156 papers (2025-04+, 2025-06+) cite global_38 papers (2025-02/03) in their reference lists? This is the most direct test of genuine intellectual succession.

**Q-D (Equal-weight computational audit):** Are the P2 evolves_from weight (0.4077) and adjacency weight (0.4077) computed by genuinely independent algorithms? This requires tracing the scoring code provenance.

**Q-E (Alternative Gate 2 candidates):** If P1/P2 (merged) are finally demoted, are there other directional candidates in the math.PR topic graph that could support a Gate 2 path? This requires a scan of the topic graph beyond the global_38-family and global_65-family.

**Q-F (Full paper set comparison for global_100/global_156):** The 5/5 representative paper identity is a title-level finding. A full paper set comparison (all 78 papers per cluster, not just 5 representatives) would either confirm or override the identity verdict. This is a PR-TrackB-06 computational task.

---

## 12. Answers to 8 Required Questions (Q1-Q8)

**Q1: Is global_38 a genuine predecessor or a transient/artifact?**

GENUINE PREDECESSOR (HIGH confidence, unchanged from PR-TrackB-04). The 5 representative papers form a coherent classical random walk and branching process cluster. Multi-period descendant generativity is confirmed (3 descendants including the merged global_100/global_156 cluster). R1 is substantially mitigated at title-level.

**Q2: P1 — retained, conditionally demoted, or removed?**

CONDITIONALLY DEMOTED. P1 is not removed — the structural evidence (evolves_from wt=0.39, adjacency bw=0.35, strict succession 1-month gap) remains present. However, three converging concerns (identity collapse with P2, category mismatch strengthened by title analysis, citation signal absent at title-level reasoning) justify conditional demotion. Demotion converts to final if PR-TrackB-06 confirms founding-date inversion and citation absence at abstract level.

**Q3: P2 — retained, conditionally demoted, or removed?**

MERGED INTO P1, CONDITIONALLY DEMOTED. P2 has no independent existence as a Gate 2 candidate because global_100 = global_156 (NOT RELIABLY DISTINCT). P2 inherits P1's conditional demotion. Additionally, the equal-weight concern (0.4077 = 0.4077) reduces P2 to 1.5 effective sources.

**Q4: What is the Gate 2 path status?**

SINGLE-CANDIDATE HEIGHTENED CONCERN. Prior two-candidate structure (P1+P2) is eliminated by the identity finding. The single remaining candidate is global_38 → merged_RMT_concentration_cluster (nominally P1 or P2, now the same claim). This path is CONDITIONALLY VIABLE pending PR-TrackB-06 satisfying conditions C1-C4. If PR-TrackB-06 confirms the category mismatch, founding-date inversion, and citation absence, Gate 2 is blocked for the global_38-family.

**Q5: Is the identity verdict final?**

CONFIRMED NOT RELIABLY DISTINCT (FINAL at title-level). This is a title-level confirmed finding based on 5/5 identical representative papers and bw=0.475 inter-cluster adjacency. Full paper set comparison (all 78 papers) has not been performed — a PR-TrackB-06 computational audit could in principle override the title-level finding if the full paper sets are non-overlapping. The FINAL qualifier applies at the current evidence level.

**Q6: What is the evidence ceiling for PR-TrackB-05?**

Title-level + graph-structural. This review did NOT access abstracts, citation lists, arXiv IDs, or author community data. The identity confirmation (5/5 papers identical) IS a valid title-level finding. The founding-date and category mismatch concerns are background-knowledge assessments, not confirmed findings. PR-TrackB-06 is required for abstract+citation level evidence.

**Q7: How does this compare to PR-TrackB-03's P4 demotion?**

P4's demotion (PR-TrackB-03) was FINAL, based on confirmed abstract+citation evidence: confirmed zero cross-citation, confirmed founding-date inversion (arXiv:1802.05882, 2018), confirmed non-overlapping author communities. P1/P2's conditional demotion (PR-TrackB-05) is provisional, based on title-level analysis, false cognate identification, and background knowledge. The concerns are structurally similar to P4's demotion factors, but the evidence level is lower. P4's demotion was confirmed; P1/P2's demotion is conditional.

**Q8: What must PR-TrackB-06 answer for Gate 2 to advance?**

Five questions must be answered: (Q-A) category mismatch confirmation/rebuttal at abstract level; (Q-B) founding-date confirmation/rebuttal for global_100/global_156 representative papers; (Q-C) citation linkage check (do global_100/global_156 papers cite global_38 papers?); (Q-D) equal-weight computational audit for P2; (Q-E) alternative Gate 2 candidates if P1/P2 merged candidate is finally demoted. If Q-A, Q-B, and Q-C all produce negative findings (mismatch confirmed, inversion confirmed, citation absent), the merged P1/P2 candidate is finally demoted and Gate 2 is blocked for the global_38-family.

---

## 13. Recommendation

### Next step: PR-TrackB-06 — abstract+citation review

PR-TrackB-05 has reached the ceiling of title-level evidence. PR-TrackB-06 is required to resolve the conditional demotion with abstract+citation evidence.

**PR-TrackB-06 recommended scope:**

1. **(Q-A) Category mismatch test:** Read abstracts of global_38 representative papers. Do the abstracts contain genuine RMT vocabulary (eigenvalues, Wigner, Dyson, spectral gap, GUE/GOE/GSE)? Or are they exclusively classical random walk / branching process content? If exclusively classical, the category mismatch is confirmed.

2. **(Q-B) Founding-date test:** Identify the arXiv IDs for global_100 and global_156 representative papers. Check the founding dates of the mathematical traditions they represent. Are these 2025 papers contributing NEW results to established 30-70 year old fields, or do they represent genuinely novel mathematical developments? If the fields are established pre-2025, founding-date pressure is confirmed.

3. **(Q-C) Citation linkage check:** For global_100 representative papers (2025-04+) and global_156 representative papers (2025-06+), check whether their reference lists include citations to global_38 papers (published 2025-02/03). Absence of cross-citation would mirror P4's zero cross-citation finding and would confirm final demotion.

4. **(Q-D) Equal-weight computational audit:** Examine the scoring code that produces evolves_from weights and adjacency weights. Are the two 0.4077 values computed by different algorithms, or do they share a common underlying computation? If the same computation, P2 has one effective source.

5. **(Q-E) Alternative Gate 2 candidate scan:** If P1/P2 are finally demoted, identify whether any other directional candidates exist in the math.PR topic graph (outside the global_38-family and global_65-family) that could support a Gate 2 path.

### Conditions for Gate 1 stability acceptance

If PR-TrackB-06 confirms final demotion (Q-A, Q-B, Q-C all negative), the recommendation is:
- Gate 1 stability: ACCEPT the current conditional layer as a stable research state without requiring Gate 2 advance.
- The conditional layer (`data/output/kg_v1_pr_conditional/`) remains valid as a research tool.
- math.PR does NOT enter `data/output/kg_v1/` (baseline) until new Gate 2 candidates are identified and reviewed.
- Document the outcome as Gate 2 BLOCKED — global_38-family path not viable.

If PR-TrackB-06 rebuts the demotion concerns (Q-A or Q-B or Q-C finds positive results), P1/P2 merged candidate reverts to provisionally retained and Gate 2 path remains open.

**Do not write "Gate 2 approved" or "Gate 2 confirmed."** The current status is SINGLE-CANDIDATE HEIGHTENED CONCERN. Gate 2 can only advance after PR-TrackB-06 completes with positive findings.

---

**Updated by PR-TrackB-06 (2026-03-29):** Conditional demotion converted to FINAL DEMOTION. All PR-TrackB-05 concerns confirmed at abstract+citation level: category mismatch CONFIRMED, founding-date inversion CONFIRMED (arXiv:2402.08206 submitted 12 months before global_38 existed), citation signal ABSENT, cluster INCOHERENT (3 non-citing subcommunities), BERTopic edge INVALID (taxonomy artifact, Jaccard 0.071–0.154). Gate 2 COLLAPSED — all 4 candidates demoted. math.PR Track B at long-term Gate 1.
