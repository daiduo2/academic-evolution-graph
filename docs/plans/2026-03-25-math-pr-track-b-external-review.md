---
doc_type: "external_evidence_review"
scope: "math.PR R2 external evidence — PR-TrackB-02"
status: "COMPLETE — R2 PARTIALLY_MITIGATED (abstract+citation level)"
owner: "rule-worker"
package_id: "PR-TrackB-02"
date: "2026-03-25"
upstream_docs:
  - "docs/plans/2026-03-24-math-pr-track-b-paper-review.md"
  - "docs/plans/2026-03-23-math-pr-phase-2c-implementation.md"
downstream_docs: []
last_reviewed: "2026-03-25"
---

# math.PR R2 External Evidence Review — PR-TrackB-02

**Date:** 2026-03-25
**Package:** PR-TrackB-02
**Status:** COMPLETE — R2 PARTIALLY_MITIGATED (abstract+citation level)

---

## 1. Executive Summary

PR-TrackB-02 is the second Track B review for math.PR Gate 2, targeting R2 (global_65 → global_188 directionality) via external arXiv abstract and citation evidence. PR-TrackB-01 reached a ceiling of title-level evidence and left R2 as NOT_MITIGATED and blocking for Gate 2.

This review upgrades R2 from NOT_MITIGATED to PARTIALLY_MITIGATED. At the field level, the mathematical lineage from classical McKean-Vlasov / SDE convergence (global_65-type content) to rough stochastic McKean equations / rough path theory (global_188-type content) is well-supported by abstract and citation evidence. Canonical bridge papers exist (arXiv:1907.00578) and multiple 2025 papers explicitly extend the classical McKean-Vlasov framework into the rough path setting while citing Sznitman and Carmona-Delarue as foundations.

However, the upgrade cannot reach RESOLVED. The specific 2025 research clusters global_65 and global_188 represent parallel communities: their representative papers are not McKean-Vlasov papers; 2025 global_65-type papers show zero rough path citations; and the rough McKean field predates global_65's activity window by 7 years (first established 2018 by Bailleul et al.). The cluster-level directionality required for P4 (source=global_65, target=global_188, rule=math_pr_method_continuity) is not confirmed.

Gate 2 remains blocked. R2 PARTIALLY_MITIGATED is not sufficient for Gate 2 passage.

---

## 2. Evidence Sources Consulted

This review is based exclusively on external arXiv abstract and citation data. No pipeline, frontend, test, or graph output files were modified or used as evidence.

| Source | Resolution | Role |
|--------|-----------|------|
| arXiv abstracts (2025–2026 papers) | Abstract-level | Primary: directionality claim support and counter |
| arXiv reference lists (citation data) | Citation-level | Directionality and community separation |
| arXiv:1907.00578 (Bailleul, Catellier, Delarue) | Field-level bridge paper | Confirms mathematical lineage |
| arXiv:1802.05882 (Bailleul et al., 2018) | Field-level founding paper | Establishes rough McKean field predates global_65 |

No local pipeline data, no `data/output/` files, and no tests were used or modified.

---

## 3. Supporting Evidence for Directionality

### 3.1 Direct bridge papers (July 2025)

**arXiv:2507.13149** (Friz, Hocquet, Lê, July 2025): "McKean-Vlasov equations with rough common noise"
- Explicitly extends classical McKean-Vlasov to the rough path setting
- Abstract cites Sznitman and Carmona-Delarue as classical foundations
- Represents the precise methodological transition postulated by P4

**arXiv:2507.17469** (Bugini, Friz, Stannat, July 2025): "Nonlinear rough Fokker-Planck equations"
- Cites Coghi-Gess 2019 (a classical McKean-Vlasov paper) in the abstract
- Proceeds to extend that classical framework into the rough noise regime
- Provides citation-level confirmation of the classical→rough lineage

### 3.2 Canonical field-level bridge (pre-2025)

**arXiv:1907.00578** (Bailleul, Catellier, Delarue): "Propagation of chaos for McKean-Vlasov SDEs driven by rough paths"
- Canonical paper extending Sznitman propagation-of-chaos to rough paths
- Confirms the directional mathematical lineage at the field level
- Functions as the conceptual bridge between global_65-type and global_188-type research

### 3.3 Additional 2025 supporting papers

**arXiv:2507.02449** (Gess, Gvalani, Hu, July 2025): Random dynamical systems for McKean-Vlasov via rough path theory — further evidence of ongoing 2025 activity at the classical→rough intersection.

**arXiv:2506.11900** and **arXiv:2510.01017**: Both papers cite Sznitman/Carmona-Delarue as classical foundation, then extend to rough/fractional regime.

### 3.4 Primary category confirmation (R3 consistency)

All supporting papers above are primarily categorized as math.PR, consistent with R3 resolution in PR-TrackB-01. The mathematical lineage operates within a single discipline.

---

## 4. Counter-Evidence

### 4.1 Rough McKean field predates global_65 by 7 years

**arXiv:1802.05882** (Bailleul et al., February 2018): A founding paper for rough McKean-Vlasov theory, published 7 years before global_65's 2025 activity window.

This is the primary structural objection to P4 cluster-level directionality. The rough McKean field was not triggered by or derived from the specific 2025 global_65 cluster. Both communities descend from a shared earlier foundation; they are parallel 2025 developments, not sequentially related clusters.

### 4.2 Zero cross-citation in 2025 global_65-type papers

**arXiv:2510.16427** (Butkovsky et al., October 2025, global_65-type paper): ZERO rough path citations in reference list.

**arXiv:2502.20786** (February 2025, global_65-type paper): ZERO rough path citations.

The absence of rough path citations in papers clearly belonging to the global_65 community is direct evidence that the two 2025 clusters are not in citation contact. Papers in global_65's activity window do not cite the rough McKean literature.

### 4.3 Shared representative papers are not McKean-Vlasov papers

The 5 shared representative papers for global_65 and global_188 (arXiv:2509.11825, 2602.00097, 2409.10037, 2410.22880, 2411.13937) cover: rough stochastic filtering, mathematical finance, singular SPDEs, fractional calculus, and CEV finance models. None are McKean-Vlasov papers. The claimed directional pair does not have McKean-Vlasov content at the cluster level.

### 4.4 Complete community separation in 2025

The citation data shows two parallel 2025 research lineages with non-overlapping reference sets. The rough McKean community (global_188-type) cites Sznitman, Carmona-Delarue, and Bailleul 2018. The classical SDE convergence community (global_65-type) cites neither rough path nor McKean-Vlasov foundations in their 2025 papers. There is no cross-community citation visible in 2025 activity.

---

## 5. The Field-Level vs Cluster-Level Distinction

This is the central analytic finding of PR-TrackB-02.

### Field-level mathematical lineage

**Well-supported.** The abstract and citation evidence confirms that, as a matter of mathematical history and intellectual progression, classical McKean-Vlasov theory (propagation of chaos, SDE convergence, particle systems) preceded and influenced rough stochastic McKean equations (rough path theory, rough Fokker-Planck, rough McKean-Vlasov). This lineage is:
- Explicitly documented in bridge papers (arXiv:1907.00578, arXiv:2507.13149, arXiv:2507.17469)
- Confirmed by citation chains from rough 2025 papers back to classical foundations
- A recognized research trajectory within the math.PR community

### Cluster-level directionality for P4

**Not confirmed.** The specific 2025 research clusters global_65 and global_188 are parallel communities. The reasons are:
1. The rough McKean field (global_188-type) was founded in 2018 — it predates the global_65 2025 window by 7 years and was not triggered by global_65
2. The two 2025 clusters have zero cross-citation
3. Their shared representative papers are not McKean-Vlasov papers — the claimed directional pair does not show McKean-Vlasov content at the cluster level
4. 2025 global_65-type papers cite neither rough paths nor McKean-Vlasov literature

The conclusion is that the field-level lineage exists but does not translate into cluster-level directionality for P4. global_65 and global_188 represent two parallel 2025 communities that each descend from a shared mathematical foundation, not a sequential evolution from one cluster to the other.

---

## 6. R2 Verdict and Status Change

### Status change

| Review | Evidence Level | R2 Status |
|--------|---------------|-----------|
| Pre-TrackB | None | Open |
| PR-TrackB-01 | Title-level | NOT_MITIGATED |
| PR-TrackB-02 | Abstract+citation | PARTIALLY_MITIGATED |

### Why PARTIALLY_MITIGATED (not NOT_MITIGATED)

The abstract and citation evidence confirms that the mathematical tradition running from classical McKean-Vlasov to rough stochastic McKean equations is real, documented, and active in 2025. The keyword extension identified in PR-TrackB-01 (global_188 adding hurst, fractional, hawkes to global_65's mckean, vlasov, itô base) is confirmed by actual 2025 paper content. The field-level lineage is no longer speculative.

### Why not RESOLVED

The cluster-level directionality for P4 is the specific claim that needs to be confirmed for Gate 2. RESOLVED would require evidence that the 2025 global_65 cluster directly influenced or preceded the 2025 global_188 cluster. This is not established:
- The rough McKean field predates global_65 by 7 years
- The two 2025 clusters have zero cross-citation
- The representative papers for the pair are not McKean-Vlasov papers
- The evidence supports field-level continuity between mathematical traditions, not sequential evolution between the specific 2025 clusters

PARTIALLY_MITIGATED accurately captures the state: field-level support confirmed, cluster-level confirmation missing.

---

## 7. Gate 2 Implication

**Gate 2 remains blocked.** PARTIALLY_MITIGATED is not sufficient for Gate 2 passage.

Gate 2 requires that all blocking risks are resolved or mitigated at a level that supports baseline inclusion. R2 at PARTIALLY_MITIGATED carries a residual blocker: cluster-level directionality for P4 is not confirmed.

### What would be needed to resolve R2 fully

Option A (cluster citation evidence): Identify any 2025 paper from the global_65 cluster that cites a rough McKean paper, or any global_188 paper that explicitly builds on a global_65 paper. Even a single cross-cluster citation would upgrade the cluster-level evidence.

Option B (P4 demotion): Formally demote P4 from the conditional integration layer and proceed with Gate 2 on the basis of P1, P2, P3 only (all based on global_38 → global_100/156/99, Tier A and B, object continuity). If P4 is excluded, Gate 2 would need to be re-assessed with only the global_38-family cases, dependent on R1 resolution.

Option C (extended window): Run the same abstract+citation review over the full 2025-03 to 2026-02 window for all global_65 and global_188 papers (not just selected representatives), with specific attention to the 2025-07 to 2025-10 overlap period.

### Current Gate 2 risk table update

| Risk | Status After PR-TrackB-02 | Gate 2 Impact |
|------|--------------------------|---------------|
| R1: global_38 transience | PARTIALLY_MITIGATED (unchanged) | Moderate blocking weight |
| R2: P4 directionality | PARTIALLY_MITIGATED (upgraded from NOT_MITIGATED) | Still blocking — cluster-level confirmation missing |
| R3: PR/AP boundary | RESOLVED (unchanged) | Not blocking |

---

## 8. Required Question Answers

**1. What evidence resolution was actually reached in PR-TrackB-02?**

Abstract-level and citation-level. This is an upgrade from the title-level ceiling of PR-TrackB-01. arXiv abstracts and reference lists were consulted for multiple 2025 papers in both the global_65-type and global_188-type communities.

**2. Was stronger-than-adjacency directionality found for global_65→global_188?**

YES at field level: abstract and citation evidence confirms the mathematical tradition running from classical McKean-Vlasov to rough stochastic McKean equations, with explicit bridge papers.

NO at cluster level: the specific 2025 clusters global_65 and global_188 show zero cross-citation, and the rough McKean field predates global_65 by 7 years. The cluster-level relationship is parallel development from a shared mathematical foundation, not sequential evolution.

**3. What is R2 status after PR-TrackB-02?**

PARTIALLY_MITIGATED. Upgraded from NOT_MITIGATED (PR-TrackB-01). Field-level mathematical lineage confirmed. Cluster-level directionality for P4 not confirmed. Residual blocker remains.

**4. Is Gate 2 still blocked after PR-TrackB-02?**

YES. Gate 2 is still blocked. PARTIALLY_MITIGATED for R2 is not sufficient for Gate 2 passage. Cluster-level directionality for P4 is required and not confirmed.

**5. What is the PR-P4 inclusion decision after PR-TrackB-02?**

P4 remains in the conditional layer only. P4 cannot be promoted to baseline inclusion. The field-level support found in this review does not justify cluster-level baseline inclusion without cross-cluster citation evidence or formal P4 demotion.

**6. What is the recommended next step?**

Human verification of whether any 2025 global_65-type papers cite the rough McKean literature directly, or whether the two communities remain fully parallel throughout the 2025-03 to 2026-02 window. Specifically: sample ≥5 papers from global_65's 2025-08 and 2025-10 activity periods (the overlap window with global_188) and check their reference lists for rough path citations. If none found, proceed with Option B (P4 demotion) and re-assess Gate 2 on the global_38-family cases only.

---

## 9. Residual Risks and Next Steps

### Residual risks after PR-TrackB-02

**R2 cluster-level gap (primary blocker):** The field-level lineage is confirmed, but cluster-level directionality for P4 is not. The two 2025 communities (global_65 and global_188) have non-overlapping citation sets in the papers reviewed. This gap cannot be resolved by further field-level evidence — only cluster-level citation evidence (from the specific 2025 clusters) or a formal P4 demotion decision can close it.

**R1 global_38 transience (secondary blocker):** Unchanged from PR-TrackB-01. PARTIALLY_MITIGATED at title level; paper-level coherence verification pending. Not the primary blocker but still unresolved.

**Shared representative paper problem (structural):** The 5 shared representative papers for global_65 and global_188 are not McKean-Vlasov papers. This means the claimed directional pair (P4) does not have cluster-level content matching the field-level lineage that was confirmed in this review. The disconnect between field-level evidence and cluster-level content is a structural issue that complicates any further mitigation attempt.

### Next steps

1. **Primary (recommended):** Human spot-check of 2025-08 and 2025-10 global_65 papers (overlap window) for rough path citations. If any found: upgrade R2 to MITIGATED. If none found: proceed to Option B.

2. **Option B (fallback):** Formally demote P4 from the conditional layer. Re-assess Gate 2 on P1, P2, P3 only (global_38-family cases). This requires resolving R1 at paper level (global_38 coherence verification) and does not require R2 resolution.

3. **No further code or pipeline changes are needed.** This review is a research/evidence task only. The conditional layer implementation (PR-2C-impl) remains complete and correct regardless of R2 resolution outcome.
