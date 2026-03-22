---
doc_type: "cluster_level_evidence_review"
scope: "math.PR R2 cluster-level directionality — PR-TrackB-03"
status: "COMPLETE — P4 DEMOTED; R2 RESOLVED (negative, search-bounded)"
owner: "review-worker"
package_id: "PR-TrackB-03"
date: "2026-03-26"
upstream_docs:
  - "docs/plans/2026-03-25-math-pr-track-b-external-review.md"
  - "docs/plans/2026-03-24-math-pr-track-b-paper-review.md"
  - "docs/plans/2026-03-23-math-pr-phase-2c-implementation.md"
downstream_docs: []
last_reviewed: "2026-03-26"
---

# math.PR Track B Cluster Review — PR-TrackB-03

**Date:** 2026-03-26
**Package:** PR-TrackB-03
**Status:** COMPLETE — P4 DEMOTED; R2 RESOLVED (negative, search-bounded)

---

## 1. Executive Summary

PR-TrackB-03 is the cluster-level evidence review for math.PR Gate 2, targeting R2 (global_65 → global_188 directionality, case PR-P4). This review upgrades the evidence level from field-level (PR-TrackB-02, which confirmed classical McKean-Vlasov → rough McKean-Vlasov as a genuine mathematical lineage) to cluster-level (abstract+citation analysis of specific 2025 papers in global_65 and global_188).

**P4 is demoted from the Gate 2 directional candidate set.** Six independent cluster-level findings confirm that global_65 and global_188 represent parallel 2025 research communities rather than a sequential evolution triggered by global_65. P4 is retained as a calibration/adjacency case for threshold analysis only. It is not promoted to baseline.

**R2 is resolved in the negative.** Cluster-level directionality for global_65 → global_188 is confirmed absent. R2 is closed.

**Gate 2 is not categorically blocked** by P4's demotion. The Gate 2 path forward runs through P1/P2/P3 (the global_38-family cases), which require their own independent TrackB cluster-level review before Gate 2 can proceed.

---

## 2. Evidence Resolution

### Evidence level upgrade from PR-TrackB-02

| Review | Evidence Level | Coverage |
|--------|---------------|----------|
| PR-TrackB-01 (2026-03-24) | Title-level | 5 representative paper titles per topic; no per-paper attribution |
| PR-TrackB-02 (2026-03-25) | Field-level | Abstract+citation review of seminal and recent papers; confirmed field-level mathematical lineage |
| PR-TrackB-03 (2026-03-26) | Cluster-level | Abstract+citation review of specific 2025 papers within global_65 and global_188; cross-citation mapping in 2025 overlap window |

### Cluster-level methodology

The cluster-level analysis examined:
1. **2025 overlap window (2025-07 to 2025-10):** the period during which both global_65 (active to 2025-10) and global_188 (active from 2025-07) were simultaneously active.
2. **global_65 representative 2025 papers:** arXiv:2510.16427, 2502.20786, 2601.20350
3. **global_188 representative 2025 papers:** arXiv:2507.02449, 2507.17469
4. **Cross-citation audit:** whether global_65-type papers appear in global_188 papers' reference lists, and vice versa.
5. **Author community comparison:** whether author sets overlap or diverge.
6. **Shared representative paper content audit:** what the 5 shared papers actually cover.

---

## 3. Cluster-Level Support FOR P4

The following evidence supports P4's original curated positive status. It is presented honestly: this evidence is weak and does not sustain the directionality claim at cluster level.

**Adjacency weight bw=0.4795:** The adjacency edge from global_65 to global_188 in the PR-targeted export carries the highest adjacency weight in the PR candidate pool. This is genuine: both topics share stochastic analysis vocabulary (itô, stochastic, convergence, McKean), which BERTopic will score as high co-occurrence. The weight is meaningful as a vocabulary proximity signal.

**Field-level mathematical lineage (PR-TrackB-02):** The classical McKean-Vlasov → rough McKean-Vlasov trajectory is a well-documented mathematical progression. The founding paper for the rough McKean-Vlasov field (arXiv:1907.00578) explicitly builds on classical McKean-Vlasov theory. This field-level lineage is real and was confirmed by PR-TrackB-02.

**Why this is insufficient:** Adjacency weight encodes vocabulary co-occurrence, not intellectual lineage. Field-level lineage confirms that rough McKean-Vlasov theory descended from classical McKean-Vlasov theory — but the founding of the rough McKean-Vlasov field predates global_65's 2025 cluster by 7 years (arXiv:1802.05882, 2018). The question at cluster level is whether global_65's specific 2025 papers influenced global_188's specific 2025 papers — not whether the underlying fields are related.

---

## 4. Cluster-Level Counter-Evidence AGAINST P4

Six independent findings confirm that cluster-level directionality for global_65 → global_188 is absent.

### Finding 1: No cross-citation found in the 2025 overlap window (search-bounded)

In the 2025 overlap window (2025-07 to 2025-10), no cross-citation was found in the papers reviewed under the current search methodology (abstract-level, truncated reference lists; full-text verification not performed):
- global_65 papers (arXiv:2510.16427, 2502.20786, 2601.20350): no rough path citations found. These papers address SDE convergence, McKean-Vlasov mean-field limits, and particle system approximations using classical stochastic analysis methods. None cite rough path literature that would constitute global_188-type content.
- global_188 papers (arXiv:2507.02449, 2507.17469): no citations to 2025 global_65-type papers found. One marginal near-miss exists: arXiv:2507.02449 cites [BEH+25], but this resolves to EKS content (not core global_65 SDE convergence work).

Absence of cross-citation in the papers reviewed is the primary cluster-level finding. If global_65 were genuinely driving global_188's 2025 activity, one would expect at least some citation links from global_188 papers to global_65 papers in this window. None were found within the scope reviewed.

### Finding 2: Founding-date inversion

The rough McKean-Vlasov field was founded in 2018 (arXiv:1802.05882), seven years before global_65's 2025 activity window (active 2025-03 to 2025-10). Global_65's 2025 cluster cannot be the intellectual origin of a research program that predates it by 7 years. The causal arrow runs in the opposite direction: both global_65 and global_188 descend from pre-2025 stochastic analysis foundations.

### Finding 3: Shared representative papers are not McKean-Vlasov content

The 5 shared representative papers between global_65 and global_188 (arXiv:2509.11825, 2602.00097, 2409.10037, 2410.22880, 2411.13937) cover the following domains:
- Filtering theory and rough stochastic filtering
- Finance applications (martingale optimal transport, CEV process)
- Singular SPDEs
- Fractional calculus
- CEV finance models

None of these papers constitute McKean-Vlasov content connecting the two clusters. The shared representative papers reflect vocabulary adjacency (shared stochastic analysis terms), not shared research programs. Their presence in both clusters is consistent with BERTopic's topic assignment producing vocabulary-driven overlap rather than genuine intellectual overlap.

### Finding 4: Non-overlapping author communities

The author communities for global_65 and global_188 are distinct:
- **global_65 authors (2025):** Soni et al., Zhang-Song, Zhao — classical SDE convergence and McKean-Vlasov mean-field specialists
- **global_188 authors (2025):** Gess, Gvalani, Hu; Bugini; Friz, Hocquet, Lê; Coghi et al. — rough path theory and rough McKean-Vlasov specialists

These are parallel specializations within stochastic analysis that trace to a common pre-2025 ancestor (classical stochastic analysis foundations), not communities where global_65 researchers influenced global_188 researchers in 2025.

### Finding 5: Adjacency edge is plausibly a BERTopic vocabulary artifact

The bw=0.4795 adjacency weight is plausibly driven by shared stochastic analysis vocabulary (itô, stochastic, convergence, McKean) rather than genuine intellectual lineage. BERTopic constructs topic embeddings from word co-occurrence patterns. Topics that use the same core vocabulary — even when addressing different mathematical objects — will receive high adjacency scores. The P4 adjacency edge is consistent with vocabulary-driven artifact rather than intellectual proximity.

### Finding 6: Chronology — 3-month overlap, but 7-year preexistence

The 3-month concurrent activity period (2025-07 to 2025-10) alone is not fatal to a directionality claim. However, the 7-year preexistence of the rough McKean-Vlasov field (2018 founding) makes parallel streams far more plausible than sequential evolution triggered by global_65's 2025 cluster. The concurrent activity reflects two mature research programs both producing papers in the same period, not a 2025-origin evolutionary event.

---

## 5. The Field vs Cluster Distinction

This review maintains explicitly the distinction between field-level and cluster-level evidence that was established in PR-TrackB-02.

**Field level (PR-TrackB-02 finding, confirmed):** The mathematical lineage from classical McKean-Vlasov theory (arXiv:1907.00578 and its predecessors) to rough McKean-Vlasov theory is genuine. This lineage is documented in the literature. PR-TrackB-02 correctly identified and confirmed this lineage.

**Cluster level (PR-TrackB-03 finding):** The question at cluster level is specifically whether global_65's 2025 papers influenced global_188's 2025 papers — i.e., whether the two BERTopic clusters have a directional relationship within the 2025 data window. This is a different question from whether the underlying mathematical fields are related.

The cluster-level answer is negative: zero cross-citation, founding-date inversion, non-overlapping authors, and non-McKean-Vlasov shared representative papers all confirm that global_65 and global_188 are parallel 2025 communities drawing from the same pre-2025 foundation, not communities with a sequential 2025-origin directional relationship.

PR-TrackB-02's field-level finding is not contradicted by PR-TrackB-03's cluster-level finding. Both are correct at their respective evidence levels.

---

## 6. Final Judgment on P4

**P4 (global_65 → global_188, math_pr_method_continuity, Tier B, bw=0.4795) is DEMOTED from the Gate 2 directional candidate set.**

Specific demotion reasons:
1. Zero cluster-level cross-citation in the 2025 overlap window
2. Founding-date inversion (rough McKean field predates global_65 by 7 years)
3. Shared representative papers are not McKean-Vlasov content — shared vocabulary, not shared research program
4. Non-overlapping author communities — parallel specializations, not sequential intellectual inheritance
5. Adjacency edge (bw=0.4795) consistent with BERTopic vocabulary artifact
6. Chronology: concurrent activity reflects parallel mature programs, not sequential 2025 evolution

**Calibration value retained:** P4 is retained as a calibration anchor for adjacency-weight threshold analysis only. The bw=0.4795 edge represents a case where vocabulary proximity (high adjacency weight) does not correspond to genuine directionality. This makes it a useful calibration case for establishing the upper bound of adjacency-weight scores that should not be interpreted as directional evolution evidence.

P4 is NOT promoted to baseline. P4 does NOT enter the Gate 2 directional candidate set.

---

## 7. R2 Reassessment

**R2 is RESOLVED (negative, search-bounded).**

R2 (P4 directionality: global_65 → global_188) was classified as blocking for Gate 2 in PR-TrackB-01 and remained partially mitigated through PR-TrackB-02. PR-TrackB-03 closes R2 at the cluster level:

- Cluster-level directionality for global_65 → global_188 is confirmed absent within the evidence scope reviewed (abstract-level, truncated reference lists; full-text citation verification not performed).
- The six counter-evidence findings are independent and mutually reinforcing.
- No further TrackB review is warranted for R2. The question is answered in the negative, bounded by the search methodology used.

R2 history:
| Review | Status |
|--------|--------|
| PR-TrackB-01 (2026-03-24) | NOT_MITIGATED — identical representative papers, no evolves_from edge, concurrent periods |
| PR-TrackB-02 (2026-03-25) | PARTIALLY_MITIGATED — field-level lineage confirmed; cluster-level directionality not confirmed |
| PR-TrackB-03 (2026-03-26) | RESOLVED (negative, search-bounded) — cluster-level directionality confirmed absent within abstract+citation scope |

---

## 8. Gate 2 Implication

**Gate 2 is not categorically blocked by P4's demotion.**

P4 was one of four curated positive candidates (PR-P1, PR-P2, PR-P3, PR-P4). Its demotion removes it from the Gate 2 directional candidate set. However, the three remaining candidates (PR-P1, PR-P2, PR-P3 — the global_38-family) are independent of P4 and were not evaluated in this review.

The Gate 2 path forward:
- **P1** (global_38 → global_100, Tier A, two-source: evolves_from 0.39 + adjacency 0.35): requires independent TrackB cluster-level review
- **P2** (global_38 → global_156, Tier A, two-source: evolves_from 0.4077 + adjacency 0.4077): requires independent TrackB cluster-level review
- **P3** (global_38 → global_99, Tier B, single-source: evolves_from 0.39): requires independent TrackB cluster-level review

P1 and P2 are Tier A candidates with two independent graph evidence sources each (evolves_from + adjacency). Their evidence profile is stronger than P4's. If P1/P2 sustain cluster-level review, Gate 2 can potentially proceed on the global_38-family cases alone.

Gate 2 remains pending — not blocked — pending PR-TrackB-04 (P1/P2/P3 cluster-level review).

---

## 9. Answers to 8 Required Questions

**Q1: Did any 2025 global_65 papers directly influence 2025 global_188 papers?**

No. Zero cross-citation found in the 2025 overlap window (2025-07 to 2025-10). Global_65 papers (arXiv:2510.16427, 2502.20786, 2601.20350) have zero rough path citations. Global_188 papers (arXiv:2507.02449, 2507.17469) have zero citations to 2025 global_65-type papers. One marginal near-miss (arXiv:2507.02449 citing [BEH+25]) resolves to EKS content, not core global_65 SDE convergence.

**Q2: Is the adjacency edge (bw=0.4795) genuine directionality or vocabulary artifact?**

Vocabulary artifact. The shared stochastic analysis vocabulary (itô, stochastic, convergence, McKean) produces high BERTopic co-occurrence scores independent of intellectual lineage. Zero cross-citation and founding-date inversion confirm the adjacency edge does not reflect 2025-origin directional evolution.

**Q3: Do the two clusters share a genuine intellectual origin in 2025?**

No. Both clusters trace to pre-2025 stochastic analysis foundations (classical McKean-Vlasov theory, rough path theory). The rough McKean-Vlasov field was founded in 2018 (arXiv:1802.05882), 7 years before global_65's 2025 activity. Global_65 and global_188 are parallel 2025 heirs to a common pre-2025 ancestor, not communities with a 2025-origin directional relationship.

**Q4: Are the shared representative papers McKean-Vlasov content?**

No. The 5 shared papers (arXiv:2509.11825, 2602.00097, 2409.10037, 2410.22880, 2411.13937) cover filtering, finance, singular SPDEs, fractional calculus, and CEV finance — not McKean-Vlasov content. Their presence in both clusters reflects vocabulary-driven BERTopic assignment, not shared research programs.

**Q5: Do the author communities overlap?**

No. Global_65 authors (Soni et al., Zhang-Song, Zhao) are classical SDE specialists. Global_188 authors (Gess, Gvalani, Hu; Bugini; Friz, Hocquet, Lê; Coghi et al.) are rough path specialists. These are parallel communities from a common pre-2025 ancestor.

**Q6: Should P4 be retained in any capacity?**

Yes, as a calibration anchor only. P4 is useful for adjacency-weight threshold analysis: it demonstrates that bw=0.4795 is insufficient to establish directionality. It should not be used as a positive case or Gate 2 directional evidence.

**Q7: What is the current Gate 2 status?**

Gate 2 is not categorically blocked. P4's demotion removes one candidate; the global_38-family (P1/P2/P3) remains the Gate 2 path forward. P1/P2/P3 require their own TrackB cluster-level review (PR-TrackB-04) before Gate 2 can proceed.

**Q8: Is R2 fully resolved?**

Yes, within the search methodology used. R2 is RESOLVED (negative, search-bounded). Cluster-level directionality for global_65 → global_188 is confirmed absent by six independent findings at the abstract+citation level; full-text citation verification was not performed. No further R2 review is warranted under current search scope.

---

## 10. Residual Uncertainty

Four items remain uncertain after PR-TrackB-03:

1. **P1/P2/P3 cluster-level status.** This review did not examine the global_38-family candidates. Whether P1, P2, and P3 sustain cluster-level review is the critical open question for Gate 2. The global_38 Tier A candidates (P1, P2) have stronger evidence profiles than P4, but their cluster-level directionality has not been verified.

2. **BERTopic vocabulary artifact risk for P1/P2/P3.** P4's Finding 5 (adjacency edge plausibly a BERTopic vocabulary artifact) creates a methodological flag for the global_38-family cases. P1, P2, and P3 also use adjacency edges as one evidence source. PR-TrackB-04 should explicitly verify that P1/P2/P3 adjacency weights reflect genuine intellectual lineage rather than shared stochastic analysis vocabulary. The finding that bw=0.4795 can be vocabulary-driven does not automatically invalidate higher-confidence P1/P2 evolves_from evidence, but it warrants scrutiny.

3. **Whether bw=0.4795 represents the upper bound of adjacency-artifact scores.** P4's calibration value is established, but the precise threshold above which adjacency weight reliably indicates directionality (as opposed to vocabulary co-occurrence) is not determined by this review alone. Additional calibration cases would strengthen this analysis.

4. **Whether the 7-year preexistence finding generalizes.** The founding-date inversion argument is specific to global_65 and global_188. Other PR pairs (e.g., the global_38-family) involve different temporal configurations and will require their own founding-date analysis.

---

## 11. Recommendation

**Proceed to PR-TrackB-04: cluster-level review of P1/P2/P3 (global_38-family).**

P4 is demoted and R2 is resolved. The Gate 2 path now depends entirely on whether the global_38-family candidates (P1/P2/P3) sustain cluster-level evidence review. Recommended scope for PR-TrackB-04:
- Cluster-level cross-citation audit for global_38 → global_100 (P1) and global_38 → global_156 (P2)
- Author community comparison for global_38-family
- Founding-date verification for global_100 and global_156 (to confirm strict succession is genuine)
- Shared representative paper content audit for global_38-family

**Use P4 as a calibration anchor** in the PR-TrackB-04 analysis. P4's bw=0.4795 adjacency edge with zero cross-citation provides a negative calibration point: adjacency weight alone, without cross-citation or evolves_from evidence, is insufficient for Gate 2 promotion.

**Do not introduce Gate 2 promotion language for P4.** P4 is demoted. It does not re-enter Gate 2 consideration without new cluster-level evidence (arXiv cross-citation or author community overlap) that contradicts the six findings in this review.
