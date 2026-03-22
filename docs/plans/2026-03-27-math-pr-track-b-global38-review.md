---
doc_type: "cluster_level_evidence_review"
scope: "math.PR global_38-family cluster-level review — PR-TrackB-04"
status: "COMPLETE — P3 DEMOTED; P1/P2 PROVISIONALLY RETAINED (title-level); Gate 2 PARTIALLY VIABLE"
owner: "review-worker"
package_id: "PR-TrackB-04"
date: "2026-03-27"
upstream_docs:
  - "docs/plans/2026-03-26-math-pr-track-b-cluster-review.md"
  - "docs/plans/2026-03-24-math-pr-track-b-paper-review.md"
  - "docs/plans/2026-03-23-math-pr-phase-2c-implementation.md"
  - "docs/plans/2026-03-21-math-pr-case-curation.md"
downstream_docs:
  - "docs/plans/2026-03-28-math-pr-track-b-p1p2-level3-review.md"
last_reviewed: "2026-03-27"
---

# math.PR Track B global_38-Family Review — PR-TrackB-04

**Date:** 2026-03-27
**Package:** PR-TrackB-04
**Status:** COMPLETE — P3 DEMOTED; P1/P2 PROVISIONALLY RETAINED (title-level); Gate 2 PARTIALLY VIABLE

---

## 1. Executive Summary

PR-TrackB-03 (2026-03-26) demoted P4 (global_65 → global_188) from the Gate 2 directional candidate set and resolved R2 in the negative. PR-TrackB-04 completes the global_38-family review: P1 (global_38 → global_100), P2 (global_38 → global_156), and P3 (global_38 → global_99).

**CRITICAL EVIDENCE LEVEL QUALIFICATION:** This entire review is at title-level resolution — 5 representative paper titles per topic, graph edges (evolves_from weights and adjacency weights), and keyword sets. This is the same evidence level as PR-TrackB-01, not the abstract+citation level of PR-TrackB-03. All verdicts must be understood as provisional, pending Level 3 abstract+citation review.

**Summary of outcomes:**

- **global_38 as predecessor:** VERDICT: genuine_predecessor (HIGH confidence). Confirmed as a legitimate, distinct research topic with multi-period generativity and coherent representative paper set.
- **P1 (global_38 → global_100):** PROVISIONALLY RETAINED — two-source evidence (evolves_from + adjacency), strict succession, distinct representative papers. Label reclassification recommended: from "object_continuity" to "domain_bridge / cross-subfield evolution." Pending Level 3 abstract+citation review.
- **P2 (global_38 → global_156):** PROVISIONALLY RETAINED — strongest Gate 2 candidate. Two-source evidence, strict succession, coherent downstream topology. Equal-weight caveat and global_100/global_156 identity question remain open.
- **P3 (global_38 → global_99):** DEMOTED — three structural deficiencies: identical representative papers with global_38 (non-distinct cluster), no adjacency edge, single-source evidence only.
- **Gate 2 path:** PARTIALLY VIABLE via P1+P2, conditional on (1) global_100/global_156 identity resolution, (2) P2 equal-weight source independence audit, (3) Level 3 abstract+citation review of P1/P2.

---

## 2. Evidence Level and Methodology

### Evidence available to this review

This review had access to:
- 5 representative paper titles per topic (BERTopic cluster representatives, title-level only)
- Graph edges from `data/output/topic_graph.json`: evolves_from weights and adjacency weights
- Keyword sets per topic (BERTopic-derived)
- Period activity data (first/last active period, paper counts)

### What was NOT available

- Paper abstracts (not accessed)
- Citation lists (not accessed)
- arXiv IDs for systematic cross-citation auditing
- Author community data
- Founding-date analysis (field-level historical lineage not examined)

### Evidence level comparison across PR TrackB reviews

| Review | Evidence Level | Coverage |
|--------|---------------|----------|
| PR-TrackB-01 (2026-03-24) | Title-level | 5 representative paper titles per topic; no per-paper attribution; no abstracts |
| PR-TrackB-02 (2026-03-25) | Field-level | Abstract+citation review of seminal papers; confirmed field-level mathematical lineage for P4 |
| PR-TrackB-03 (2026-03-26) | Cluster-level (abstract+citation) | Specific 2025 papers within global_65 and global_188; cross-citation mapping; author community analysis |
| PR-TrackB-04 (2026-03-27) | Title-level + graph-structural | 5 representative paper titles per topic; evolves_from and adjacency edges; keyword analysis; graph topology |

PR-TrackB-04 operates at the same evidence ceiling as PR-TrackB-01. It adds graph-structural analysis (multi-descendant topology, adjacency edge presence/absence, evolves_from weight independence) but cannot perform the abstract+citation analysis that made PR-TrackB-03's P4 demotion conclusive. The P1/P2 provisional retention decisions here are therefore weaker than PR-TrackB-03's P4 demotion: the structural evidence supports retention, but abstract+citation evidence is required to confirm or demote at the next level.

---

## 3. global_38 as Predecessor

### Identity assessment

**global_38** (随机极限与不等式, "random limits and inequalities") is a 2-period topic active 2025-02 and 2025-03, with 208 papers.

**VERDICT: genuine_predecessor (HIGH confidence)**

**Supporting evidence:**

**Representative paper coherence:** The 5 representative paper titles for global_38 form a coherent random walk and branching process cluster. The titles address convergence of stochastic processes, limit theorems for random sequences, and probabilistic inequalities in discrete process settings. This is internally consistent: global_38 represents a genuine, identifiable research community in classical probability theory.

**Multi-period descendant generativity:** global_38 has 3 confirmed multi-period descendants in the evolves_from graph:
- global_100 (random matrix ensemble cumulants, active 2025-04+) — P1
- global_156 (random matrix eigenvalue analysis, active 2025-06+) — P2
- global_99 (random walk and branching, active 2025-04+) — P3

The 3-descendant generativity is strong evidence that global_38 is a genuine predecessor with productive research influence. Transient or artifact topics typically have zero or one descendant; three descendants with distinct identity profiles is more consistent with a genuine research hub.

**Bridge vocabulary coherence:** The dominant vocabulary in global_38 ("walk" + "matrices") bridges the downstream random walk and random matrix clusters. This is internally coherent: a topic covering random limits and inequalities would naturally produce descendants in both the random walk direction (global_99: more classical probability) and the random matrix direction (global_100, global_156: more modern spectral probability).

**global_97 concern:** One additional evolves_from edge from global_38 leads to global_97, which appears to be a combinatorics/graph theory (CO) or geometric representation (GR) artifact. This cross-domain edge does not undermine the global_38 predecessor identity: a genuine predecessor can produce cross-domain edges when BERTopic topic embedding captures vocabulary spillover into adjacent subfields.

**Conclusion:** global_38 is a genuine predecessor. The 2-period activity window is the minimum for multi-period classification, but the 3-descendant generativity and coherent representative paper set support genuine, not transient, predecessor status. R1 (global_38 transience risk) is substantially mitigated at title-level, though full mitigation requires abstract+citation verification.

---

## 4. P1 Review (global_38 → global_100, Tier A)

### Evidence summary

| Field | Value |
|-------|-------|
| Pair ID | PR-P1 |
| Edge type | evolves_from wt=0.39 (primary) + adjacency bw=0.35 (corroborating) |
| Evidence count | 2 (two-source) |
| Chronology | Strict succession: global_38 active 2025-02/03; global_100 active 2025-04+ |
| Temporal gap | 1 month (2025-03 → 2025-04) |

### Representative paper analysis

**global_38 representative papers:** Coherent random walk and branching process cluster. Convergence theorems, limit laws, probabilistic inequalities in classical discrete stochastic process settings.

**global_100 representative papers:** Distinct from global_38. global_100 covers random matrix ensemble cumulant analysis — spectral statistics, eigenvalue cumulants, Wigner-Dyson universality class behavior. This is a different mathematical object from global_38's random walk/limit law focus.

**p1-agent finding — "different mathematical objects" argument:** The agent noted that global_38 (random walk / branching processes) and global_100 (random matrix ensembles) concern different mathematical objects. Random walks are discrete stochastic processes operating on graphs or lattices; random matrix ensembles are continuous spectral objects. The two are related through shared probabilistic foundations (limit theorems apply to both) but are not the same mathematical object.

**gate-agent resolution:** The gate-agent determined that the "different mathematical objects" observation is a label reclassification finding, not a demotion-level finding. Specifically:
- The evolves_from edge (wt=0.39) is independently generated by the temporal algorithm and is not derived from adjacency
- The chronological strict succession is genuine (1-month gap, no overlap)
- The vocabulary bridge ("walk" + "matrices" in global_38) is coherent with the observed evolution: a topic covering random limits and inequalities naturally bridges toward both random walk descendants and random matrix descendants
- The edge type "object_continuity" is misclassified: the relationship is better described as "domain_bridge / cross-subfield evolution" (classical probability → spectral probability)
- A domain bridge label reclassification is not a demotion. It changes the interpretation of what the edge represents, not whether the edge represents a genuine directional relationship.

### Adjacency credibility assessment

The P1 adjacency edge (bw=0.35) is assessed as MORE TRUSTWORTHY than P4's demoted adjacency edge (bw=0.4795). Reasons:
- The vocabulary driver in P1 is domain-specific: "matrices" and "eigenvalues" are specific to random matrix theory, not generic stochastic analysis vocabulary. BERTopic is less likely to generate a vocabulary artifact from domain-specific terms than from generic terms (itô, stochastic, convergence) as in P4.
- The lower adjacency weight (0.35 vs 0.4795) reduces the risk that the edge reflects maximum vocabulary saturation artifact
- The independent evolves_from edge (wt=0.39) corroborates the adjacency, providing a two-source verification structure that P4 lacked

### Final verdict

**PROVISIONALLY RETAINED** — pending Level 3 abstract+citation review

Label reclassification recommended: change edge type from "math_pr_object_continuity" to "domain_bridge / cross-subfield evolution." This changes the interpretive category but does not remove P1 from the Gate 2 directional candidate set.

---

## 5. P2 Review (global_38 → global_156, Tier A)

### Evidence summary

| Field | Value |
|-------|-------|
| Pair ID | PR-P2 |
| Edge type | evolves_from wt=0.4077 (primary) + adjacency bw=0.4077 (corroborating) |
| Evidence count | 2 (two-source) |
| Chronology | Strict succession: global_38 active 2025-02/03; global_156 active 2025-06+ |
| Temporal gap | 3 months (2025-03 → 2025-06) |

### Representative paper analysis

**global_156 representative papers:** Distinct from global_38. global_156 covers random matrix eigenvalue distribution analysis — spectral gap theory, eigenvalue spacing distributions, universality of spectral statistics. Like global_100, this is a different mathematical specialization from global_38's classical random walk/limit law focus.

**Downstream topology:** global_156 has a coherent downstream identity:
- global_156 → global_392 (downstream evolves_from)
- global_156 → global_276 (downstream evolves_from)

This downstream generativity confirms that global_156 is not a transient or terminal cluster; it is an active research hub with its own productive lineage.

### Equal-weight concern

The most significant concern for P2 is the exact equality of evolves_from weight (0.4077) and adjacency weight (0.4077). This exact equality raises the question of whether the two "independent" sources are actually the same underlying computation presented twice. If the adjacency weight is derived from or directly mirrors the evolves_from weight, then P2 has only one independent evidence source rather than two.

**Assessment:** The equal weight is anomalous but not dispositive at title-level. The temporal algorithm that generates evolves_from weights and the adjacency-scoring algorithm that generates adjacency weights are designed to be different computations. However, the exact numerical equality 0.4077 = 0.4077 cannot be dismissed as coincidence — it requires an explicit source independence audit at Level 3.

**Prior art:** The same equal-weight concern was identified in MPR-02 (case curation, 2026-03-21): "Shared evolves_from and adjacency weights being identical (0.4077) warrants verification that these are not artefacts of the same underlying scoring computation." This concern was flagged at curation and remains unresolved.

### global_100/global_156 identity concern

Both global_100 and global_156 are described as random matrix topics descending from global_38. A secondary concern identified during this review is that global_100 and global_156 share identical representative papers in the 5-paper title set. If the two topics have the same representative papers, they may represent the same underlying cluster under different IDs (a BERTopic identity split artifact) rather than two genuinely distinct downstream communities.

If global_100 and global_156 are the same cluster with split IDs, then P1 and P2 are duplicates pointing to the same target rather than two independent evolution paths from global_38. This would reduce the Gate 2 directional candidate count from 2 to 1 (or fewer).

**Resolution required:** Level 3 review must determine whether global_100 and global_156 have genuinely distinct paper sets and research identities or whether they are a BERTopic identity split of a single random matrix cluster.

### Final verdict

**PROVISIONALLY RETAINED as primary Gate 2 candidate** — pending Level 3 abstract+citation review

P2 has the strongest individual evidence profile of the three reviewed cases: highest evolves_from weight (0.4077), longest temporal gap (3 months), coherent downstream topology (→ global_392, → global_276), and distinct representative papers from global_38. Its two open concerns (equal-weight non-independence, global_100/global_156 identity) are resolvable at Level 3 and do not currently warrant demotion.

---

## 6. P3 Review (global_38 → global_99, Tier B)

### Evidence summary

| Field | Value |
|-------|-------|
| Pair ID | PR-P3 |
| Edge type | evolves_from wt=0.39 (only source) |
| Evidence count | 1 (single-source) |
| Chronology | Strict succession: global_38 active 2025-02/03; global_99 active 2025-04+ |
| Temporal gap | 1 month (2025-03 → 2025-04) |
| Adjacency | null — NO adjacency edge in either graph |

### Three structural deficiencies

**Deficiency 1: Identical representative papers — cluster non-distinctness**

All 5 representative paper titles for global_99 are identical to 5 of global_38's representative paper titles. This is the most damaging finding for P3. If global_99 and global_38 share the same representative papers, the two BERTopic topics may be:
- The same research community assigned to two different topic IDs in different periods (a temporal split artifact)
- A BERTopic over-segmentation of what is actually a single evolving topic

In either case, the evolves_from edge global_38 → global_99 may represent a within-topic temporal progression (BERTopic re-clustering the same papers across periods) rather than a genuine between-topic evolution. The evolves_from edge would then reflect BERTopic's internal temporal mechanism rather than genuine intellectual succession.

This is the decisive structural finding against P3.

**Deficiency 2: No adjacency edge — anomalous given P1/P2 structure**

P1 has an adjacency edge (bw=0.35). P2 has an adjacency edge (bw=0.4077). P3 has no adjacency edge. This absence is anomalous: if global_38 and global_99 represent a genuine evolution with topical overlap, one would expect keyword co-occurrence to produce some adjacency weight. The absence of any adjacency signal suggests that the topical overlap between global_38 and global_99 is weaker than the evolves_from edge alone implies.

When combined with Deficiency 1, the adjacency absence strengthens the interpretation that the evolves_from edge reflects within-cluster temporal mechanics rather than genuine between-cluster intellectual succession.

**Deficiency 3: Single-source evidence only**

P3 has only one evidence source (evolves_from wt=0.39). P1 and P2 both have two independent evidence sources. Single-source evidence is insufficient to overcome the first two structural deficiencies. Even if the evolves_from weight were higher than 0.39, single-source evidence combined with identical representative papers and absent adjacency would not sustain a Gate 2 directional claim.

### Keyword differentiation — genuine but insufficient

The keyword sets of global_38 and global_99 are genuinely distinct. global_99 keywords include SLE (Schramm-Löwner evolution), VRJP (vertex-reinforced jump processes), and GSAWS (generalized self-avoiding walks) — all of which are distinct from global_38's general convergence/inequality keywords. This keyword differentiation is real and would normally support a distinct identity claim.

However, keyword differentiation is insufficient to override the three structural deficiencies. BERTopic can assign a topic distinct keywords while still sharing representative papers with another topic (particularly when two topics represent the same papers re-clustered across periods). The keyword differentiation shows that global_99's semantic space is recognizable as distinct, but it does not resolve the representative paper identity problem.

### Comparison to P4's demotion reasons

P4 was demoted in PR-TrackB-03 for six reasons. The applicable demotion reasons for P3 are:

| P4 Demotion Reason | Applies to P3? |
|-------------------|----------------|
| Zero cross-citation in 2025 overlap window | Unknown (not verified at title-level) |
| Founding-date inversion | Not applicable (global_99 does not predate global_38) |
| Shared representative papers not relevant to claimed edge | YES — shared representative papers indicate non-distinct clusters |
| Non-overlapping author communities | Unknown (not verified at title-level) |
| Adjacency edge consistent with vocabulary artifact | PARTIAL — absence of adjacency edge is a different deficiency but has the same direction (reduced confidence) |
| Concurrent activity: parallel programs, not sequential evolution | NOT APPLICABLE — P3 has strict succession (opposite of P4's concurrency) |

P3's demotion grounds are different from P4's. P4 was demoted because its evidence supported parallel communities. P3 is demoted because its evidence suggests it is not a distinct community from global_38 at all (identical representative papers). P4's chronology was concurrent (fatal for directionality). P3's chronology is strict succession (supporting retention in principle) — but the representative paper identity problem overrides the chronological advantage.

### Final verdict

**DEMOTED — structural grounds**

P3 is demoted from the Gate 2 directional candidate set. Three structural deficiencies (identical representative papers, no adjacency edge, single-source evidence) collectively indicate that the evolves_from edge global_38 → global_99 likely reflects a within-topic temporal mechanism rather than a genuine between-topic intellectual succession. P3 should not be reconsidered as a Gate 2 candidate without new structural evidence that resolves the representative paper identity problem.

---

## 7. Adjacency Artifact Assessment

### Summary from artifact-level analysis

The artifact-agent assessment compared P1 and P2 adjacency edges against P4's confirmed artifact (bw=0.4795, zero cross-citation, vocabulary-driven).

**P1 adjacency (bw=0.35): assessed as MORE TRUSTWORTHY than P4**

Reasons:
1. Domain-specific vocabulary driver: "matrices" and "eigenvalues" are specific to random matrix theory. BERTopic vocabulary artifacts are most common with generic vocabulary (itô, stochastic, convergence). Domain-specific vocabulary generates more meaningful co-occurrence.
2. Lower weight: 0.35 < 0.4795. Lower adjacency weight is less consistent with maximum vocabulary saturation artifact than P4's near-peak 0.4795 score.
3. Independent evolves_from corroboration (wt=0.39): the existence of an evolves_from edge from a different algorithm provides corroboration that P4 lacked entirely.
4. Distinct representative papers from global_38: the distinct paper sets confirm that global_100 is a recognizably different cluster from global_38, which supports genuine topical adjacency rather than within-cluster vocabulary echo.

**P2 adjacency (bw=0.4077): assessed as MORE TRUSTWORTHY than P4, with caveats**

The same reasoning applies: domain-specific vocabulary, independent evolves_from, distinct representative papers. The caveat is the equal-weight concern (bw=0.4077 = evolves_from wt=0.4077 exactly), which introduces uncertainty about source independence. Until resolved, P2's adjacency edge should be treated as providing corroboration rather than full independence.

**P3 adjacency: ABSENT**

The absence of adjacency is the expected condition for a non-distinct cluster (identical representative papers). BERTopic would not generate a high adjacency score between two topics that represent the same underlying papers, because there is no vocabulary gap to bridge. The absence confirms rather than contradicts the Deficiency 1 finding.

---

## 8. Chronological Analysis

### Summary

All three reviewed pairs have strict succession chronology. This is the structural opposite of P4's concurrent activity, which was one of P4's demotion factors.

| Case | Source Last Active | Target First Active | Gap | Chronology Type |
|------|-------------------|---------------------|-----|-----------------|
| P1 | 2025-03 | 2025-04 | 1 month | Strict succession |
| P2 | 2025-03 | 2025-06 | 3 months | Strict succession |
| P3 | 2025-03 | 2025-04 | 1 month | Strict succession |

No founding-date inversion was detected for any of P1, P2, or P3. Unlike P4 (where the rough McKean-Vlasov field predated global_65 by 7 years), the target topics for P1/P2/P3 (global_100, global_156, global_99) all have first active periods after global_38's final active period. There is no temporal paradox.

**Implication for retention:** Chronology SUPPORTS RETENTION for P1 and P2. The strict succession with meaningful gaps (1 month and 3 months respectively) is consistent with genuine sequential evolution.

**Implication for P3:** Chronology is NEUTRAL for the P3 demotion. The strict succession (1 month gap) would normally support retention. However, chronology cannot override the representative paper identity problem. A topic that shares the same representative papers as its predecessor likely represents the same cluster re-encountered in a subsequent period, regardless of whether the period gap is 1 month or 12 months.

---

## 9. Gate 2 Reassessment

### Gate 2 path status: PARTIALLY VIABLE

| Candidate | Status | Gate 2 Eligibility |
|-----------|--------|-------------------|
| P1 (global_38 → global_100) | PROVISIONALLY RETAINED | Secondary Gate 2 candidate (label reclassification pending) |
| P2 (global_38 → global_156) | PROVISIONALLY RETAINED | Primary Gate 2 candidate |
| P3 (global_38 → global_99) | DEMOTED | NOT a Gate 2 candidate |
| P4 (global_65 → global_188) | DEMOTED (PR-TrackB-03) | NOT a Gate 2 candidate |

Gate 2 can potentially proceed via P1+P2 if Level 3 review confirms their directional claims. Gate 2 cannot proceed on P3 or P4.

### Conditions required before Gate 2 can advance

Gate 2 advancement from PARTIALLY VIABLE to VIABLE requires all of the following:

1. **global_100/global_156 identity resolution:** Determine whether global_100 and global_156 are genuinely distinct clusters or a BERTopic identity split. If they are the same cluster, P1 and P2 become duplicates, and Gate 2 reduces to a single-case path.

2. **P2 equal-weight source independence audit:** Verify that the evolves_from weight (0.4077) and adjacency weight (0.4077) for P2 are computed by genuinely independent algorithms. If they are the same underlying computation, P2 has only one evidence source, which weakens its two-source classification.

3. **Level 3 abstract+citation review of P1 and P2:** The provisional retention decisions in this review are title-level. They cannot be elevated to confirmed Gate 2 directional evidence without abstract+citation analysis at the level of PR-TrackB-03. Specifically:
   - Cross-citation audit: do global_100 papers (2025-04+) cite global_38 papers (2025-02/03)?
   - Do global_156 papers (2025-06+) cite global_38 papers?
   - Author community analysis: is there continuity or does the author community shift?
   - Vocabulary analysis beyond titles: do the paper abstracts confirm the domain bridge interpretation?

4. **MPR-03 benchmark runner implementation:** Code prerequisite, independent of TrackB review.

**P3 is NOT a Gate 2 candidate** and should not be reconsidered without new structural evidence resolving the representative paper identity problem.

---

## 10. Evidence Gap — Required Level 3 Review

This review reached the ceiling of title-level evidence. The following abstract+citation evidence is required to match PR-TrackB-03 rigor and confirm or demote P1/P2:

### 1. Cross-citation audit for P1 and P2

Examine the reference lists of global_100 papers (first active 2025-04) and global_156 papers (first active 2025-06) for citations to global_38 papers (active 2025-02/03). If global_38 papers are cited by global_100 or global_156 papers, this confirms genuine intellectual succession. If no cross-citation is found (as in P4's zero-citation finding), the provisional retention should be demoted.

### 2. Author overlap analysis

Compare the author communities of global_38, global_100, and global_156. If the same authors appear in global_38 papers and subsequently in global_100 or global_156 papers, this confirms sequential intellectual development. If the author communities are entirely disjoint (as in P4), this suggests parallel communities from a common pre-38 ancestor rather than direct succession.

### 3. global_100/global_156 identity resolution

Access the full paper sets for global_100 and global_156 and compare them directly. If the underlying paper sets are distinct (non-overlapping), the two clusters represent genuinely different research communities and P1/P2 are independent Gate 2 candidates. If they substantially overlap, the two clusters are likely a BERTopic identity split and P1/P2 would merge into a single Gate 2 case.

### 4. P2 equal-weight source independence audit

Examine the computation provenance of the evolves_from weight (0.4077) and adjacency weight (0.4077) for global_38 → global_156. Trace whether the two 0.4077 values come from different algorithmic paths or from a shared underlying computation. If the weights are computed independently (different algorithms, different edge types), the two-source classification stands. If one is derived from or mirrors the other, P2 is a single-source case.

---

## 11. Required Questions — Answers

**Q1: Is global_38 a genuine predecessor or a transient/artifact?**

GENUINE PREDECESSOR (HIGH confidence). global_38 has 3 multi-period descendants with distinct identities, a coherent representative paper set (random walk and branching process literature), and internally consistent bridge vocabulary ("walk" + "matrices"). The 2-period activity window is the minimum for multi-period classification, but the 3-descendant generativity and representative paper coherence support genuine, not transient, predecessor status. R1 is substantially mitigated at title-level.

**Q2: P1 — retained, demoted, or removed?**

PROVISIONALLY RETAINED. Two-source evidence (evolves_from wt=0.39 + adjacency bw=0.35), strict succession (1-month gap), distinct representative papers. Label reclassification recommended from "object_continuity" to "domain_bridge / cross-subfield evolution." Pending Level 3 abstract+citation review before promotion to confirmed Gate 2 candidate.

**Q3: P2 — retained, demoted, or removed?**

PROVISIONALLY RETAINED as primary Gate 2 candidate. Two-source evidence (evolves_from wt=0.4077 + adjacency bw=0.4077), strict succession (3-month gap), coherent downstream topology (→ global_392, → global_276), distinct representative papers. Equal-weight source independence concern and global_100/global_156 identity question are open but not dispositive at title-level. Pending Level 3 abstract+citation review.

**Q4: P3 — retained, demoted, or removed?**

DEMOTED. Three structural deficiencies: (1) all 5 representative papers identical to global_38 — cluster non-distinctness; (2) no adjacency edge — anomalous given P1/P2 structure; (3) single-source evidence only. Keyword differentiation (SLE, VRJP, GSAWS) is genuine but insufficient to override the representative paper identity problem. Not a Gate 2 candidate.

**Q5: Is P1/P2 adjacency more credible than P4's? Why?**

YES, for three reasons:
1. **Domain-specific vocabulary**: P1 and P2 adjacency edges are driven by specific random matrix vocabulary ("matrices," "eigenvalues"), whereas P4's adjacency was driven by generic stochastic analysis vocabulary ("itô," "stochastic," "convergence," "McKean"). Domain-specific vocabulary is a more reliable BERTopic co-occurrence signal.
2. **Lower weights**: P1 (bw=0.35) and P2 (bw=0.4077) are both lower than P4 (bw=0.4795). Lower weights are less consistent with maximum vocabulary saturation artifact.
3. **Independent evolves_from corroboration**: Both P1 and P2 have independent evolves_from edges (different algorithm) corroborating the adjacency. P4 had no evolves_from edge at all — its entire evidence was the adjacency edge alone.

**Q6: Did this review get genuine cluster-level evidence, or just repeat graph evidence?**

Primarily graph-structural evidence — not full cluster-level evidence in the sense of PR-TrackB-03. This review analyzed: evolves_from edges, adjacency edges, representative paper title coherence, keyword sets, period activity data, and multi-descendant graph topology. It did not access abstracts, citations, arXiv IDs, author communities, or founding-date data (which were the core of PR-TrackB-03's cluster-level analysis). The "cluster-level" scope of PR-TrackB-04 as specified in PR-TrackB-03's recommendation was not fully achieved at abstract+citation depth. The evidence ceiling is title-level + graph-structural.

**Q7: Gate 2 path via P1/P2/P3 — viable, partially viable, or collapsed?**

PARTIALLY VIABLE. P2 is the primary Gate 2 candidate (provisionally retained). P1 is a secondary Gate 2 candidate (provisionally retained, label reclassification pending). P3 is demoted — not a Gate 2 candidate. Gate 2 is not collapsed, but it cannot advance to the next step without Level 3 abstract+citation review of P1/P2.

**Q8: If only P1/P2 survive, can Gate 2 continue?**

YES, conditionally. Gate 2 does not require all three global_38-family cases to sustain. If P1 and P2 are confirmed at Level 3, the global_38-family provides two Tier A directional cases with two-source evidence each — a stronger base than the single case used for LO and AG benchmark seeding. Gate 2 can proceed with P1+P2 alone, subject to the three conditions listed in Section 9 (identity resolution, equal-weight audit, Level 3 review).

---

## 12. Residual Uncertainty

The following questions remain open after PR-TrackB-04:

1. **global_100/global_156 identity:** Whether the two random matrix clusters are genuinely distinct or a BERTopic identity split. This is the highest-priority resolution question for Gate 2.

2. **P2 equal-weight source independence:** Whether the evolves_from and adjacency weights of 0.4077 reflect independent computations or a shared underlying scoring.

3. **P1/P2 cross-citation depth:** Whether global_38 papers (2025-02/03) appear in the reference lists of global_100 (2025-04+) or global_156 (2025-06+) papers. Absence of cross-citation (as in P4) would trigger demotion at Level 3.

4. **P1/P2 author community analysis:** Whether the author communities of global_38 and its downstream random matrix clusters show continuity or represent parallel specializations from a common ancestor.

5. **P3 re-evaluation conditions:** Whether P3 could be reconsidered if future evidence (e.g., a paper-level analysis showing distinct paper sets between global_38 and global_99 despite the same representative titles) resolves the non-distinctness finding.

6. **global_97 CO/GR artifact:** The evolves_from edge from global_38 to global_97 (cross-domain, CO/GR classification) has not been examined. This edge does not affect the P1/P2/P3 verdicts but may be relevant for understanding global_38's full descendant topology.

---

## 13. Recommendation

### Next step: PR-TrackB-05 — Level 3 abstract+citation review of P1/P2

The provisional retention of P1 and P2 at title-level is a necessary intermediate step, not the final verdict. Before Gate 2 can advance, P1 and P2 require the same quality of abstract+citation evidence that PR-TrackB-03 applied to P4.

**PR-TrackB-05 recommended scope:**
1. Cross-citation audit: do global_100 and global_156 papers (2025-04+) cite global_38 papers (2025-02/03)?
2. Author community analysis: continuity or divergence between global_38, global_100, and global_156 research communities?
3. global_100/global_156 identity resolution: full paper set comparison to determine whether the two clusters are genuinely distinct
4. P2 equal-weight source independence audit: computational provenance of 0.4077 = 0.4077
5. Founding-date verification: confirm no temporal paradox for global_100 and global_156

**P3:** Demoted. P3 should not be included in PR-TrackB-05 unless new evidence resolves the representative paper identity problem. The three structural deficiencies identified in this review are sufficient to exclude P3 from Gate 2 consideration at current evidence levels.

**Gate 2 pathway (conditional):** If PR-TrackB-05 confirms P1 and P2 at abstract+citation level (positive cross-citation, distinct cluster identities, no founding-date inversion), Gate 2 can advance to the engineering phase:
- MPR-03: PR benchmark runner implementation
- Baseline inclusion: math.PR integration into `data/output/kg_v1/`

If PR-TrackB-05 demotes P1 and/or P2 (zero cross-citation, identical cluster identities, or founding-date inversion analogous to P4), Gate 2 would be blocked pending further candidate identification.

**Do not write "Gate 2 approved" or "Gate 2 confirmed."** The current status is PARTIALLY VIABLE. Gate 2 can only advance to confirmed-viable after PR-TrackB-05 completes with positive findings for P1/P2.

---

**Updated by PR-TrackB-05 (2026-03-28):** global_100 and global_156 confirmed NOT RELIABLY DISTINCT (5/5 identical representative papers; bw=0.475 inter-cluster adjacency). P1 and P2 collapse to single candidate: global_38 → merged_RMT_concentration_cluster. P1: CONDITIONALLY DEMOTED. P2: MERGED INTO P1, CONDITIONALLY DEMOTED. Gate 2 structure: SINGLE-CANDIDATE HEIGHTENED CONCERN. Next step: PR-TrackB-06 abstract+citation review.
