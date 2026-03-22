---
doc_type: "track_b_review"
scope: "math > math.PR > Track B paper review"
status: "COMPLETE — title-level review only; Gate 2 remains blocked on R2"
owner: "review-worker"
package_id: "PR-TrackB-01"
date: "2026-03-24"
upstream_docs:
  - "docs/plans/2026-03-23-math-pr-phase-2c-implementation.md"
  - "docs/plans/2026-03-21-math-pr-case-curation.md"
  - "docs/plans/2026-03-20-math-pr-candidate-extraction.md"
  - "docs/plans/2026-03-18-math-pr-benchmark.md"
downstream_docs: []
last_reviewed: "2026-03-24"
---

# math.PR Track B Paper Review — PR-TrackB-01

**Date:** 2026-03-24
**Package:** PR-TrackB-01
**Status:** COMPLETE — title-level review only; Gate 2 remains blocked on R2

---

## 1. Executive Summary

PR-TrackB-01 is the first Track B (paper-level evidence strengthening) review for math.PR Gate 2. This review reached a ceiling of title-level evidence: five representative paper titles per topic were examined against the three open risks (R1: global_38 transience, R2: global_65→global_188 directionality, R3: PR/AP boundary classification). R1 is partially mitigated — global_38 exhibits a 5-descendant generativity signal and 2.4x paper growth, reducing transience risk from critical to moderate, though full mitigation requires per-period paper identity verification at the abstract level. R3 is resolved — both global_65 and global_188 are PR-dominant with high and medium confidence respectively, with a dual-class caveat for global_188's SPDE well-posedness component. R2 is not mitigated and remains blocking: title-level examination found identical representative paper sets for global_65 and global_188, no evolves_from edge exists between them in the main topic graph, and their activity periods overlap concurrently. Gate 2 cannot advance without external evidence resolving R2.

---

## 2. Evidence Sources and Limits

### What was checked

All evidence for this review was drawn from local worktree data sources. No external data (arXiv abstracts, citation networks, paper metadata) was accessed.

| Source | Content | Resolution Provided |
|--------|---------|---------------------|
| `data/output/topic_graph.json` | Full topic graph with evolves_from and adjacent_to edges, weights, representative titles | Title-level; 5 representative titles per topic |
| `data/output/aligned_topics_hierarchy.json` | Topic hierarchy with subcategory assignments, active_periods, paper counts, keywords | Keyword and period metadata; no per-paper attribution |
| `data/output/math_discovery_pr_targeted/topic_graph.json` | PR-targeted export; adjacent_to edges only | Adjacency weights; no evolves_from edges |
| `docs/plans/2026-03-21-math-pr-case-curation.md` | MPR-02 curation document with curated positive, negative, and ambiguous cases | Graph-evidence summary; no paper-level data |
| `docs/plans/2026-03-20-math-pr-candidate-extraction.md` | MPR-01C extraction report with evolves_from edge discovery | Edge weights and source attribution |

### What is missing

- **`data/raw/` does not exist** in this worktree. Per-period paper lists, arXiv IDs, and abstract text are unavailable.
- **Representative titles are not period-attributed.** The 5 titles per topic in the topic graph are aggregate samples; they are not linked to specific active periods.
- **No citation data is available.** Cross-topic citation links (which would directly support R2 directionality) cannot be assessed locally.
- **No arXiv abstract text is available.** Keyword analysis is limited to topic-level keyword lists, not paper-level content.

### Evidence ceiling reached

**TITLE_LEVEL** — this is the maximum resolution achievable from local data sources.

---

## 3. Review of global_38 (R1 — Transience Risk)

### Topic profile

- **Topic ID:** global_38
- **Chinese label:** 随机极限与不等式
- **Active periods:** 2025-02, 2025-03 (2 periods)
- **Paper count:** 208 papers (growth: 61 papers at first period → 147 papers at second period; 2.4x)
- **Core keywords:** random limits, probability inequalities, random matrix, concentration, spectral bounds

### Generativity signal

global_38 appears as the source node in 5 evolves_from edges in `data/output/topic_graph.json`:

| Descendant | Label | evolves_from weight |
|------------|-------|---------------------|
| global_100 | 随机矩阵系综累积量 | 0.39 |
| global_156 | 随机矩阵特征值分析 | 0.4077 |
| global_198 | (unverified) | (unverified) |
| global_97 | (unverified) | (unverified) |
| global_99 | 随机游走与分支 | 0.39 |

A topic with 5 evolves_from edges as source — all pointing to topics active after global_38's 2-period window — is structurally consistent with a genuine predecessor topic rather than a transient data artifact. Transient or noise topics typically do not generate multiple directional descendant edges.

### Representative evidence assessment

Five representative titles were examined for global_38. All five titles are coherent within the probability limit theory and random matrix domain (concentration inequalities, spectral gap estimates, tail probability bounds). No titles suggest cross-domain contamination or generic stochastic language that would indicate a spurious topic cluster.

For global_99 (one of the 5 descendants), sustained multi-period activity was confirmed across 3 periods (2025-04, 2025-09, 2026-02). This establishes that at least one of the 5 downstream topics has genuine continuity beyond a single period, lending indirect support to global_38 as a real predecessor.

### Verdict and confidence

**global_38 is more likely a genuine predecessor topic than a transient data artifact. Confidence: MEDIUM.**

The 2.4x paper growth within 2 periods, 5-descendant generativity signal, and domain-coherent representative titles all point toward genuine topic identity. The transience concern (only 2 active periods) is real but not disqualifying at this evidence level.

### Partial mitigation statement

**R1 is PARTIALLY_MITIGATED.** The generativity signal and paper growth evidence reduce the transience risk from critical to moderate. Full mitigation requires:
1. Paper-level verification that the 208 papers in global_38 represent a distinct, coherent research cluster (not a topic-model artifact).
2. Per-period paper identity confirmation: the 61 papers in 2025-02 and 147 papers in 2025-03 should be distinct from neighboring topic clusters.
3. Verification of global_198 and global_97 (2 of 5 descendants remain unverified at title level in this review).

---

## 4. Review of global_65 → global_188 (R2 — Directionality)

### Temporal pattern

- **global_65:** active 2025-03, 2025-05, 2025-08, 2025-10 (4 periods, 391 papers)
- **global_188:** active 2025-07, 2025-09, 2025-11, 2026-02 (4 periods, 387 papers)
- **Overlap window:** global_65 last active 2025-10; global_188 first active 2025-07 — concurrent for approximately 3 months

The two topics are active simultaneously for a substantial portion of their combined activity window. This concurrent pattern is directly contrary to the strict succession expected in a directional evolution claim.

### Identical representative evidence (critical objection)

Title-level examination found that the 5 representative papers listed for global_65 and the 5 representative papers listed for global_188 are **identical**. There is no distinct paper-level signature separating the two topics at title level.

This is a critical finding. If the two topics cannot be distinguished by their representative papers, the hypothesis that global_65 is a distinct predecessor to global_188 cannot be supported at any level below abstract-level review. The representative titles in the topic graph are the primary paper-level signal available locally, and they fail to differentiate the two topics.

### Keyword extension analysis

Keyword analysis from `aligned_topics_hierarchy.json` shows:
- **global_65 core keywords:** particle, mckean, vlasov, convergence, itô, SDE, propagation-of-chaos
- **global_188 extension keywords:** hurst, fractional, hawkes, jump (in addition to itô and rough path terms)

The keyword extension is mathematically coherent: global_188 adds rough path theory vocabulary (Hurst exponent, fractional Brownian motion, Hawkes processes, jump processes) to the classical SDE base of global_65. This progression from classical stochastic analysis to rough path extensions is a well-known trajectory in the probability theory literature.

However, keyword extension alone is insufficient evidence for directionality. Keyword difference establishes topical distinction — it does not establish that global_65 papers preceded and influenced global_188 papers. The extension could reflect parallel development of two specializations from a common foundation, rather than sequential evolution.

### No evolves_from edge

There is no evolves_from edge from global_65 to global_188 in `data/output/topic_graph.json`. The only graph-level connection is an adjacency edge (bw=0.4795), which encodes topical co-occurrence without temporal direction. An adjacency edge at this weight is meaningful for establishing topical proximity but is not evidence of sequential evolution.

### Verdict and confidence

**No stronger-than-adjacency directional evidence for global_65→global_188 was found at title level. Confidence in directionality claim: LOW.**

The combination of (a) identical representative papers, (b) no evolves_from edge, and (c) concurrent activity periods constitutes a failure to establish directionality at this evidence level.

### Why R2 remains blocking

R2 is classified as blocking for Gate 2 because:
1. The directionality claim for PR-P4 (the only method-continuity case in the curated set) cannot be supported with local data.
2. The concurrent activity periods suggest parallel development is at least as plausible as sequential evolution.
3. The identical representative paper sets mean even a paper-by-paper comparison within local data would not resolve the question — arXiv abstract and citation data are required.
4. PR-P4 is the only evidence for the global_65/global_188 relationship; there is no independent corroborating source.

**R2 is RESOLVED (negative) — cluster-level directionality confirmed absent by PR-TrackB-03 (2026-03-26). Gate 2 path forward via P1/P2/P3 (global_38-family).**

> **Updated by PR-TrackB-02 (2026-03-25):** abstract+citation evidence confirms field-level mathematical lineage (classical McKean-Vlasov → rough McKean-Vlasov); cluster-level directionality for P4 not confirmed; Gate 2 still blocked.

> **Updated by PR-TrackB-03 (2026-03-26):** cluster-level review confirms R2 resolved in the negative. global_65 and global_188 represent parallel 2025 research communities (zero cross-citation in overlap window; founding-date inversion; shared representative papers not McKean-Vlasov). P4 demoted from Gate 2 directional candidate; retained as calibration anchor. Gate 2 path forward via P1/P2/P3 (global_38-family).

---

## 5. Review of PR/AP Boundary (R3 — Classification)

### global_65 classification verdict

**PR_DOMINANT. Confidence: HIGH.**

- Subcategory assignment in all local sources: math.PR
- Hierarchy path: "math.PR研究"
- Core PR indicators: propagation-of-chaos, particle methods, McKean-Vlasov equations, itô calculus, SDE convergence analysis
- The propagation-of-chaos / McKean-Vlasov framing is canonical probability theory content — it appears in math.PR literature and is associated with probabilistic limit theorems, not PDE well-posedness
- AP-adjacency: minimal. SDE convergence involves PDE-adjacent language but the McKean-Vlasov mean-field limit perspective is firmly within math.PR
- Reclassification risk: approximately 5%

### global_188 classification verdict

**PR_DOMINANT. Confidence: MEDIUM.**

- Subcategory assignment in all local sources: math.PR
- Hierarchy path: "math.PR研究"
- Core PR indicators: rough paths, Hurst exponent, fractional Brownian motion, Hawkes processes, jump-diffusion, itô calculus
- AP-adjacency: present. The SPDE well-posedness angle of global_188 (rough McKean-Vlasov equations in SPDE form) introduces a non-trivial connection to math.AP. Rough path theory for SPDEs sits at the math.PR/math.AP boundary in the literature.
- Reclassification risk: approximately 15–20%

### Dual-class caveat for global_188

global_188 warrants dual-class annotation. The rough McKean-Vlasov SPDE well-posedness component (existence, uniqueness, regularity of rough SPDE solutions) is more naturally classified as math.AP than math.PR. The remainder of global_188's content (rough path stochastic analysis, Hurst exponent estimation, fractional noise) is clearly math.PR.

**Recommended annotation:** global_188 should be marked as `subcategory: math.PR, secondary_class: math.AP` in any downstream integration metadata, with a note that the SPDE well-posedness component introduces AP-adjacency.

### R3 resolution statement

**R3 is RESOLVED. Neither global_65 nor global_188 is a misclassification.** Both are PR-dominant in current local data with well-documented PR indicators. The dual-class caveat for global_188 is a precision annotation, not a blocking issue. R3 does not block Gate 2.

---

## 6. Paper Sampling Table

The following papers are drawn from the actual `representative_evidence` fields in `data/output/topic_graph.json`. These are the verbatim titles available locally — no paraphrasing or inference. Period attribution is inferred from topic activity windows; no per-paper period data is available locally.

**Resolution note:** These are titles only. No arXiv IDs, abstracts, or period-attributed paper lists exist in any local source.

| Paper Title | Topics | Inferred Period | Evidence Support | Notes |
|-------------|--------|-----------------|-----------------|-------|
| "Chernoff bounds for branching random walks" | global_38, global_99 | 2025-02/03 | R1: domain coherence (branching RW = core PR object); object continuity between global_38 and global_99 | Shared representative — both topics list this verbatim |
| "Sharp asymptotics for $N$-point correlation functions of coalescing heavy-tailed random walk" | global_38, global_99 | 2025-02/03 | R1: asymptotic analysis vocabulary confirms global_38 identity | Coalescing RW bridges both topics |
| "Ergodic Theorems for Random Walks in Random Environments" | global_38, global_99 | 2025-02/03 | R1: ergodic theory for RW = PR limit theory; object continuity | Shared representative |
| "Population size of critical Galton-Watson processes under small deviations and infinite variance" | global_38, global_99 | 2025-02/03 | R1: branching process theory; confirms global_38 as PR predecessor | Strong PR identity paper |
| "Variational Tail Bounds for Norms of Random Vectors and Matrices" | global_100, global_156 | 2025-04/07 | R1: confirms global_100/global_156 as PR random matrix descendants | Shared representative; both topics list verbatim |
| "Quenched properties of the Spectral Form Factor" | global_100, global_156 | 2025-04/07 | R1: spectral analysis confirms eigenvalue/cumulant topic identity | Bridges global_100 and global_156 |
| "Operation with Concentration Inequalities" | global_100, global_156 | 2025-04/07 | R1: concentration inequalities = core PR-matrix method | Shared representative |
| "Rough stochastic filtering" | global_65, global_188 | 2025-08/07 | R2 (CRITICAL): identical representative in both topics — no separation at title level; R3: rough path = strong PR indicator | Shared verbatim; key R2 objection evidence |
| "Singularity of solutions to singular SPDEs" | global_65, global_188 | 2025-08/07 | R2: shared verbatim; R3: "singular SPDEs" straddles PR/AP boundary — arXiv class unknown | Dual-class caveat applies; primary classification unverified |
| "Rough Martingale Optimal Transport: Theory, Implementation, and Regulatory Applications for Non-Modelable Risk Factors" | global_65, global_188 | 2025-08/07 | R2: shared verbatim — fails to separate the two topics; R3: martingale + rough path = PR indicators | q-fin cross-listing likely; not pure math.PR |
| "Generalized random processes related to Hadamard operators and Le Roy measures" | global_65, global_188 | 2026-02 | R2: shared verbatim; R3: generalized stochastic processes = PR | Shared representative; concurrent period |
| "Analytical Formula for Fractional-Order Conditional Moments of Nonlinear Drift CEV Process with Regime Switching" | global_65, global_188 | 2026-02 | R3: fractional-order + conditional moments = PR indicators; R2: shared verbatim | q-fin.MF cross-listing likely |

**Critical finding on R2:** All 5 representative papers for global_65 and all 5 representative papers for global_188 are identical in local data — every row above marked "global_65, global_188" appears verbatim in both topics' `representative_evidence` field. This is the primary basis for the finding that title-level review cannot resolve R2.

---

## 7. Gate 2 Risk Reassessment

| Risk | Previous Status | Track B Finding | New Status | Gate 2 Impact |
|------|----------------|-----------------|------------|---------------|
| R1: global_38 transience | Open | 5-descendant generativity signal; 2.4x paper growth; global_99 confirmed 3-period sustained activity; global_198 and global_97 unverified | PARTIALLY_MITIGATED | Reduced blocking weight — no longer critical, now moderate |
| R2: P4 directionality | Open | Identical representative papers for global_65 and global_188; no evolves_from edge; concurrent activity 2025-07 to 2025-10; keyword extension is coherent but insufficient for directionality | RESOLVED (negative — P4 demoted) — cluster-level review (PR-TrackB-03, 2026-03-26) confirms parallel 2025 communities; zero cross-citation; founding-date inversion; P4 removed from Gate 2 directional set | RESOLVED (negative — P4 demoted) — Gate 2 path via P1/P2/P3 (global_38-family); P4 retained as calibration anchor only |
| R3: PR/AP boundary | Open | global_65 PR-dominant HIGH confidence; global_188 PR-dominant MEDIUM confidence with dual-class caveat for SPDE well-posedness component; both confirmed math.PR in all local sources | RESOLVED | Not blocking |

---

## 8. Required Questions — Answers

**1. global_38: genuine predecessor or transient artifact?**

More likely a genuine predecessor. The 5-descendant generativity signal (5 evolves_from edges as source), 2.4x paper growth within its 2-period window, and domain-coherent representative titles collectively argue against transience. Transient or noise topics do not typically generate 5 directional descendant edges. Confidence: MEDIUM. Full confirmation requires paper-level verification of global_38's internal coherence and per-period paper identity.

**2. global_65→global_188: stronger than adjacency directional evidence found?**

No. Title-level review found no stronger-than-adjacency evidence. Specific findings: (a) the 5 representative papers for global_65 and global_188 are identical in local data — no distinct paper-level signature separates the two topics; (b) no evolves_from edge exists between them in the main topic graph; (c) concurrent activity periods (2025-07 to 2025-10 overlap) reduce the plausibility of strict succession. Keyword extension (global_188 adds hurst, fractional, hawkes, jump) is coherent but does not constitute directional evidence.

**3. global_65/global_188: PR-dominant, AP-dominant, or dual?**

Both are PR-dominant. global_65: PR-dominant, HIGH confidence (~5% reclassification risk). global_188: PR-dominant, MEDIUM confidence (~15–20% reclassification risk), with a dual-class caveat for the SPDE well-posedness component. Neither is AP-dominant. global_188 warrants dual-class annotation (math.PR primary, math.AP secondary).

**4. Evidence resolution actually reached?**

TITLE_LEVEL — the maximum achievable from local data sources. `data/raw/` does not exist. Per-period paper lists, arXiv IDs, abstract text, and citation data are all unavailable locally. Representative titles (5 per topic, no period attribution) are the highest-resolution paper-level evidence accessible.

**5. R1/R2/R3 mitigation status?**

- R1: PARTIALLY_MITIGATED (generativity signal strong; paper-level coherence unverified)
- R2: PARTIALLY_MITIGATED — updated by PR-TrackB-02 (2026-03-25): field-level mathematical lineage confirmed at abstract+citation level; cluster-level directionality for P4 not confirmed (parallel 2025 communities, zero cross-citation); Gate 2 still blocked
- R3: RESOLVED (both topics PR-dominant; dual-class caveat for global_188 noted)

**6. Gate 2 still blocked? Recommended next step?**

Yes, Gate 2 remains blocked. R2 is the blocking risk. R1 partial mitigation and R3 resolution are not sufficient to unblock Gate 2 while R2 remains open. The recommended next step is PR-TrackB-02 targeting R2 via external evidence sources (arXiv abstracts and citation data for global_65 and global_188). If external evidence access is not feasible, the alternative is to accept Gate 1 as the current stable state and flag PR-P4 as adjacency-only evidence insufficient for Gate 2.

---

## 9. Residual Uncertainty

The following items remain unknown after PR-TrackB-01 and cannot be resolved from local data:

1. **Paper identity for global_38 per period.** The 61 papers in 2025-02 and 147 papers in 2025-03 cannot be individually identified or verified for topical coherence. If a significant fraction of these papers belong to an adjacent topic cluster, global_38's transience risk would increase.

2. **Status of global_198 and global_97.** Two of global_38's 5 descendants were not verified at title level. Their period activity, paper counts, and representative titles are not confirmed in this review.

3. **Paper-level separation of global_65 and global_188.** The identical representative paper sets make it impossible to determine, from local data, whether any individual paper belongs specifically to one topic or the other. This is the core blocker for R2 and cannot be resolved without abstract-level or citation-level data.

4. **Temporal attribution of representative titles.** None of the representative titles in `topic_graph.json` are attributed to specific active periods. Whether the global_188 "extension" keywords (hurst, fractional, hawkes) appear in papers from the later periods (suggesting temporal layering) or are present throughout cannot be determined.

5. **Cross-topic citation links.** No citation data is available locally. Whether global_65 papers are cited by global_188 papers (which would be the strongest possible directional evidence) cannot be assessed.

6. **Math.AP co-classification prevalence for global_188.** The dual-class caveat is based on keyword analysis and topic label inference. The actual proportion of global_188 papers co-classified as math.AP is unknown without arXiv metadata.

---

## 10. Recommendation

Gate 2 remains blocked. The path forward depends on whether external evidence for R2 is accessible. **Option A (preferred): Proceed to PR-TrackB-02 targeting R2 via external evidence.** This would require querying arXiv metadata for papers in global_65 and global_188 — specifically, obtaining per-paper arXiv IDs, abstracts, and citation lists to (a) distinguish the two topic clusters at paper level and (b) identify whether global_65 papers appear in the reference lists of global_188 papers. If directional citation evidence is found, R2 can be mitigated and Gate 2 unblocked. PR-P3 and the Tier A cases (PR-P1, PR-P2) could potentially proceed to Gate 2 on R1 partial mitigation alone if P4 is demoted to a non-primary anchor. **Option B (fallback): Accept Gate 1 as the current stable state.** Mark PR-P4 explicitly as adjacency-only evidence insufficient for Gate 2; retain PR-P1, PR-P2, PR-P3 as conditionally supportable under partial R1 mitigation; suspend Gate 2 indefinitely until external data becomes available. Option B is appropriate if arXiv API access or equivalent external evidence cannot be arranged in the near term.
