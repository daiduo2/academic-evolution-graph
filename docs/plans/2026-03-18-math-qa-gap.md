doc_type: "gap_statement"
scope: "math > math.QA"
status: "gap"
assessment_date: "2026-03-21"
package_id: "MQAR-01"
reason: "zero topics in data"

# math.QA Gap Statement

## Current State

math.QA (Quantum Algebra) has **0 topics** in the current data.

The `math.QA` key is entirely absent from `hierarchies` in
`data/output/aligned_topics_hierarchy.json`. No topics were extracted,
assigned, or indexed for this domain.

| Metric | Value |
|--------|-------|
| Topics in hierarchy | 0 |
| Multi-period topics | 0 |
| evolves_from edges | 0 |
| adjacent_to edges | 0 |
| Evolution cases | 0 |

## Gap Layer

The gap begins at the **earliest possible layer**: topic modeling / data
ingestion. The absence is both topic-level (no topics extracted) and
hierarchy-level (no hierarchy key created). There is no data substrate
to work with at any downstream stage.

## Why Benchmark Is Not Possible

- Zero topics → zero topic pairs → zero temporal sequences
- No graph edges of any type involving math.QA topics
- Any benchmark run would operate on an empty set and produce vacuous results
- There is no minimal unit (even a single topic) to anchor an assessment

This is not a case of insufficient evidence — it is a case of no evidence.

## Why We Are Not Continuing

Continuing to plan for math.QA benchmark development would be premature
and misleading. Without at least a minimal data substrate, any rule
design, threshold tuning, or case curation is speculative.

The correct state is: **gap / no data / not ready**.

## Future Reopen Conditions

math.QA may be reconsidered only when ALL of the following are met:

1. **Total topics >= 10** in math.QA hierarchy
2. **Multi-period topics >= 3** (active_periods >= 2 each)
3. **>= 1 anchor-eligible topic**: papers >= 30, periods >= 2, neighbors >= 2
4. **>= 1 evolves_from edge** involving math.QA topics in topic graph
5. **>= 2 topics with non-generic, domain-specific vocabulary**
   (e.g., quantum groups, Hopf algebras, braided categories — not just
   "algebra", "theory", "structures")

If these thresholds are not met after 2 consecutive annual data refreshes,
math.QA should be merged into a broader algebra survey category rather
than maintained as a standalone gap.

## Upstream Note

The data gap may reflect one of:
- math.QA papers are present but miscategorized into other arXiv subcategories
- math.QA papers are excluded by current ingestion filters
- math.QA volume is genuinely too low in the current collection window

This distinction matters for remediation but does not change the current
gap status.

## Next Step

None. Do not proceed with benchmark planning.
If data conditions change, re-run MQA-01A (gap normalization check) before
any further work.
