doc_type: "design"
scope: "math knowledge graph v1 coverage scope"
status: "draft"
owner: "coverage-agent"
source_of_truth: true
upstream_docs:
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/2026-03-12-math-worker-backlog.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/03-task-packages.md"
  - "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor/docs/plans/evolution-ops/12-math-knowledge-graph-package.md"
downstream_docs: []
last_reviewed: "2026-03-19"

# Math Knowledge Graph v1 Coverage Scope Decision

## Executive Summary

**PKG-MATH-KG-01** v1 scope is explicitly limited to:

| Status | Subdomain | Evidence Level | Cases |
|--------|-----------|----------------|-------|
| ✅ IN SCOPE | math.LO | Production-ready | 11 benchmark cases (5+6+2) |
| ✅ IN SCOPE | math.AG | Production-ready | 6 benchmark cases (object_continuity only) |
| ⚠️ IN SCOPE (Provisional) | math.PR | Pre-curation | 12 multi-period topics, 6 eligible anchors, candidate chains identified |
| ❌ OUT OF SCOPE | math.QA | Insufficient data | 3 single-period topics, 0 evolution cases |
| ❌ OUT OF SCOPE | math.RA | Insufficient data | 3 single-period topics, 0 evolution cases |
| ❌ OUT OF SCOPE | math.RT | Not assessed | Unknown data status |
| ❌ OUT OF SCOPE | Other math subdomains | Not assessed | Unknown data status |

**Rationale**: v1 prioritizes subdomains with verified temporal evolution evidence. Only subdomains with multi-period topics and demonstrable anchor-target relationships enter the graph. Provisional inclusion (math.PR) requires explicit labeling of evidence confidence levels.

---

## IN SCOPE Subdomains

### 1. math.LO (Logic)

**Inclusion Justification**: Strongest evidence base among all math subdomains.

**Evidence Types Available**:
- **11 fixed benchmark cases** with explicit positive/negative/ambiguous classification:
  - 5 positive cases (verified object/method continuity)
  - 6 negative cases (verified boundary distinctions)
  - 2 ambiguous cases (intentional edge cases for model calibration)
- **Event-level evolution chains**: Forcing continuity, definability continuity, type theory continuity
- **Bridge-level evidence**: Set theory cardinal/forcing relationships

**Data Characteristics**:
- Multiple multi-period topics with clear temporal signatures
- Distinct object vocabulary (forcing, cardinal, definability, type theory)
- Clear methodological boundaries

**Limitations**:
- Type theory continuity remains at bridge-level (not event-level)
- Some cases require domain expertise to validate

**Graph Representation**:
- Nodes: Topics with full metadata (paper counts, periods, keywords)
- Edges: `evolves_to` with evidence type annotations (confirmed/inferred/ambiguous)
- Evidence provenance: Direct mapping from benchmark cases

---

### 2. math.AG (Algebraic Geometry)

**Inclusion Justification**: Verified object continuity with clean scope boundaries.

**Evidence Types Available**:
- **6 fixed benchmark cases** for object_continuity:
  - 2 positive cases (verified object evolution)
  - 4 negative cases (verified boundary distinctions)
- **Method vocabulary**: Cohomology, derived, motivic, tropical, étale (documented but not benchmarked)

**Data Characteristics**:
- Clear object vocabulary (varieties, schemes, stacks, cohomology theories)
- Temporal evolution visible in topic relationships
- Strong negative case coverage prevents false positives

**Scope Limitations** (Explicitly Documented):
- `math_ag_method_continuity`: **TEST-EVIDENCE-ONLY**
  - No event-level cases identified (only bridge-level)
  - Synthetic cases removed from benchmark
  - Method vocabulary available for graph annotation but not for evolution edges

**Graph Representation**:
- Nodes: Topics with object vocabulary tags
- Edges: `evolves_to` limited to object_continuity verified cases
- Method vocabulary: Stored as topic attributes, not evolution evidence

---

### 3. math.PR (Probability)

**Inclusion Justification (Provisional)**: Strong structural evidence, pending explicit case curation.

**Evidence Types Available**:
- **12 multi-period topics** (confirmed via `active_periods` field)
- **6 eligible anchors** meeting all filters (papers>=60, periods>=2, neighbors>=2)
- **3 inferred evolution chains** from neighbor analysis:
  - Percolation chain: global_39 → global_99 → global_188
  - Random matrix chain: global_156 → global_38
  - Stochastic process chain: global_39 → global_65 → global_188

**Why PROVISIONAL Status**:
- Explicit exported cases: Only 1 in math-wide 20-case export (5% visibility)
- Inferred candidates from neighbor relationships require validation
- No fixed positive/negative cases yet (pre-curation state)
- MPR-02 (case curation) remains **LOCKED** pending PR-targeted extraction

**Data Characteristics**:
- Strong temporal structure (29 topics, 12 multi-period)
- Clear object vocabulary (percolation, random matrix, SDE, rough paths)
- Applied vs theoretical boundaries identifiable

**Graph Representation (Provisional)**:
- Nodes: All 12 multi-period topics with confidence="high"
- Nodes: All 17 single-period topics with confidence="baseline"
- Edges: **Distinguish evidence levels**:
  - `evolves_to` + evidence="confirmed": Explicitly verified cases (none yet)
  - `evolves_to` + evidence="inferred": Neighbor-derived candidates (3 chains)
  - `evolves_to` + evidence="ambiguous": Boundary cases requiring review

**Conditions for Promotion to Full Status**:
1. PR-targeted extraction (MPR-01C) produces >=2 explicit exported cases
2. Case curation (MPR-02) fixes >=3 positive and >=2 negative cases
3. Runner implementation (MPR-03) validates benchmark coverage

---

## OUT OF SCOPE Subdomains

### 1. math.QA (Quantum Algebra)

**Exclusion Reason**: Insufficient temporal evolution data.

**Data Gap**:
- Only 3 topics in current data window
- All 3 topics are **single-period** (no temporal evolution)
- 0 evolution cases in any export

**What Would Be Needed**:
- Minimum 4-5 topics with >=2 periods each
- At least 2 candidate anchor-target pairs with temporal separation
- Clear object vocabulary beyond generic terms (quantum, representation)

**Longer-Window Exploration Potential**:
- PKG-QA-01B planned for extended window exploration
- If longer window reveals >=2 multi-period topics, reassess for v2
- Current assessment: **Not viable for v1**

**Graph Representation**:
- v1: Exclude entirely
- v2 candidate: Reassess after PKG-QA-01B completion

---

### 2. math.RA (Rings and Algebras)

**Exclusion Reason**: Absence of temporal evolution structure.

**Data Gap**:
- Only 3 topics in current data window
- All 3 topics are **single-period** (1 active month each)
- 0 evolution cases, 0 temporal pairs
- Topics: Poisson-Baxter Lie algebras, polynomial mappings, random matrices

**What Would Be Needed**:
- Minimum 4-5 topics with >=2 periods each
- Topics must span >=6 months to show temporal patterns
- Distinct object vocabulary (ring, module, ideal, algebra) with specific contexts

**Longer-Window Exploration Potential**:
- PKG-RA-01B planned for extended window exploration
- Requires >=24 month data window to overcome single-period limitation
- If exploration finds >=2 event-level positives, reassess for v2

**Graph Representation**:
- v1: Exclude entirely
- v2 candidate: Conditional on PKG-RA-01B findings

---

### 3. math.RT (Representation Theory)

**Exclusion Reason**: Not yet assessed.

**Data Status**: Unknown
- No audit performed
- Topic count, period distribution, evolution cases: all unverified

**Assessment Required**:
- Run math-focused export with RT subcategory filter
- Count multi-period topics
- Identify candidate anchors
- Apply decision fork: skeleton-ready vs gap vs provisional

**Graph Representation**:
- v1: Exclude pending assessment
- v1.5 candidate: If assessment reveals strong evidence, consider mid-cycle addition

---

### 4. Other Math Subdomains

**Exclusion Reason**: Not assessed.

**List of Unassessed Subdomains**:
- math.AP (Analysis of PDEs)
- math.OC (Optimization and Control)
- math.NA (Numerical Analysis)
- math.CO (Combinatorics)
- math.GR (Group Theory)
- math.NT (Number Theory)
- math.AT (Algebraic Topology)
- math.DG (Differential Geometry)
- math.GT (Geometric Topology)
- math.CA (Classical Analysis)
- math.CV (Complex Variables)
- math.DS (Dynamical Systems)
- math.FA (Functional Analysis)
- math.GM (General Mathematics)
- math.GN (General Topology)
- math.HO (History and Overview)
- math.IT (Information Theory)
- math.KT (K-Theory and Homology)
- math.MG (Metric Geometry)
- math.MP (Mathematical Physics)
- math.OA (Operator Algebras)
- math.SP (Spectral Theory)
- math.ST (Statistics Theory)

**Assessment Priority for v2**:
1. math.NT (Number Theory) - historically rich evolution patterns
2. math.DG (Differential Geometry) - strong object continuity potential
3. math.CO (Combinatorics) - method continuity patterns

---

## Evidence Model for Graph Edges

### Edge Type: `evolves_to`

| Evidence Level | Source | Confidence | Use in v1 |
|----------------|--------|------------|-----------|
| confirmed | Benchmark case (positive) | High | Primary edge type |
| inferred | Neighbor analysis, graph structure | Medium | Label explicitly, flag for review |
| ambiguous | Boundary cases, model calibration | Variable | Include with notes, exclude from metrics |
| unavailable | No evidence | N/A | No edge created |

### Node Confidence Levels

| Level | Criteria | Example Subdomains |
|-------|----------|-------------------|
| high | Multi-period + eligible anchor + explicit cases | math.LO, math.AG |
| medium | Multi-period + eligible anchor, pre-curation | math.PR |
| baseline | Single-period or unassessed | All out-of-scope subdomains |

---

## Conditions for Future Inclusion

### v1.5 (Mid-Cycle Addition)

Subdomains may be added to v1 if:
1. PR-targeted extraction (MPR-01C) unlocks MPR-02
2. math.PR case curation produces >=5 confirmed cases
3. Assessment of math.RT or math.NT reveals >=4 multi-period topics with clear evolution

### v2 (Full Reassessment)

All out-of-scope subdomains reassessed if:
1. Longer-window exploration (PKG-QA-01B, PKG-RA-01B) reveals temporal evolution
2. Data pipeline extended to >=24 months
3. New export strategies surface previously hidden cases

---

## Schema Implications

### Required Node Properties

```yaml
node:
  id: string              # global topic id
  subdomain: string       # math.LO, math.AG, etc.
  name: string            # human-readable topic name
  papers: int             # total paper count
  periods: int            # number of active periods
  confidence: enum        # high | medium | baseline
  in_v1_scope: boolean    # true for LO, AG, PR
  keywords: [string]      # extracted vocabulary
  status: enum            # confirmed | provisional | excluded
```

### Required Edge Properties

```yaml
edge:
  source: string          # anchor topic id
  target: string          # evolved topic id
  type: enum              # evolves_to | related_to
  evidence: enum          # confirmed | inferred | ambiguous
  subdomain: string       # math.LO, math.AG, etc.
  basis: string           # benchmark_case | neighbor_graph | manual
  confidence_score: float # 0.0-1.0
```

---

## Summary

**v1 Coverage Philosophy**: Quality over quantity. Only include subdomains with:
1. Verified multi-period temporal structure
2. Explicit positive/negative case coverage
3. Clear object/method vocabulary boundaries

**math.PR Exception**: Included provisionally due to strong structural evidence, but edges must distinguish confirmed vs inferred evidence levels.

**Out-of-Scope Path**: All excluded subdomains have documented re-entry conditions based on data exploration or longer time windows.
