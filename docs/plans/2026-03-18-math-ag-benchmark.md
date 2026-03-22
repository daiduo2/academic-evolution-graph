---
doc_type: "benchmark"
scope: "math > math.AG"
status: "active"
owner: "trend-monitor"
source_of_truth: true
upstream_docs:
  - "docs/plans/2026-03-11-evolution-doc-standards.md"
  - "docs/plans/2026-03-10-evolution-rule-coverage.md"
downstream_docs: []
last_reviewed: "2026-03-22"
---

# Math.AG Benchmark — v2

## Purpose

这份文档固定 `math.AG` 的第一批真实 benchmark cases（PKG-AG-01 产出）。

**重要区分**:
- `math_ag_object_continuity`: **RUNNER-READY BUT PARTIAL** - 当前 runner-positive baseline 仅固定 `ag-p1`
- `math_ag_method_continuity`: **TEST EVIDENCE ONLY** - 仅用于验证阈值

## Scope

- `math > math.AG`
- 代数簇与模空间相关主题
- 17 个真实 math.AG topic 节点（已核实来自 aligned_topics_hierarchy.json）

## Status

| 规则 | 状态 | Benchmark Runner |
|------|------|-----------------|
| `math_ag_object_continuity` | `partial` | ag-p1 是唯一 runner-positive；ag-p2/p3 明确为 bridge-level semantic positives，不进入 runner |
| `math_ag_method_continuity` | `test-evidence-only` | ❌ 否 |

---

## Graph Narrative Layers

| Layer | Cases | Meaning | Graph Role |
|------|-------|---------|------------|
| `confirmed core` | `ag-p1` | 唯一已确认的 runner-positive / event-level 主线 | 作为 AG 主干显示 |
| `bridge ring` | `ag-p2`, `ag-p3` | 语义上值得保留的 bridge-level positives，但不通过当前 exact-term gate | 作为主干外圈的 support ring 显示 |
| `excluded boundary` | `ag-n1`, `ag-n2`, `ag-n3` | 靠近 AG 主线、但应被明确挡在外面的失败模式 | 作为边界解释层显示，不画成正向连续演化 |

- `ag-amb1` 仍是 review-only 的 boundary dispute；它不是默认图层的一部分，避免把未定争议混入 bridge ring。

## Positive Cases

| Case ID | Anchor | Target | Level | Confidence | Shared Objects |
|---------|--------|--------|-------|------------|----------------|
| `ag-p1` | `global_69` 代数叠与层理论 | `global_287` 导出代数叠范畴 | event-level | 0.85 | stacks, stack |
| `ag-p2` | `global_30` 法诺簇模空间曲线 | `global_355` 超椭圆曲线阿贝尔簇 | bridge-level | 0.65 | curves (variety_family) |
| `ag-p3` | `global_355` 超椭圆曲线阿贝尔簇 | `global_117` 志村簇与Theta积分 | bridge-level | 0.60 | varieties (single exact but too generic) |

### Case Details

#### ag-p1: global_69 → global_287

- **Anchor** `global_69`: 代数叠与层理论 (math.AG)
  - keywords: stacks, algebraic, zariski, sheaves, stack, intersection
- **Target** `global_287`: 导出代数叠范畴 (math.AG)
  - keywords: stacks, derived, stack, algebraic, categories, equivariant
- **Shared exact AG objects**: stacks, stack
- **Why positive**: 导出代数叠范畴 is the categorical enrichment of 代数叠与层理论; the stack object persists exactly across the derivation, which is sufficient for the current `>=2` exact-term gate via `stacks` / `stack`.
- **Evidence**: Confirmed by the current AG benchmark runner under canonical case ID `ag-p1`. Historical runner IDs `ag-b1` / `ag-e2` were duplicate aliases for this same event-level pair and are no longer part of the active runner contract.

#### ag-p2: global_30 → global_355

- **Anchor** `global_30`: 法诺簇模空间曲线 (math.AG)
  - keywords: toric, conjecture, k3, hodge, moduli, adic, curves
- **Target** `global_355`: 超椭圆曲线阿贝尔簇 (math.AG)
  - keywords: abelian, varieties, hyperelliptic, curves, adic, genus
- **Shared**: "curves" (variety_family exact)
- **Why positive**: Both topics centrally involve algebraic curves; the Jacobian construction links Fano/moduli-of-curves research to hyperelliptic curves and their abelian variety Jacobians.
- **Note**: bridge-level semantic positive — only 1 exact AG object term. This is the inner bridge-ring case, not a runner-facing positive under the current partial baseline.

#### ag-p3: global_355 → global_117

- **Anchor** `global_355`: 超椭圆曲线阿贝尔簇 (math.AG)
  - keywords: abelian, varieties, hyperelliptic, curves, adic, genus
- **Target** `global_117`: 志村簇与Theta积分 (math.AG)
  - keywords: shimura, varieties, theta, integral, ramified, hodge
- **Shared**: "varieties" (1 exact term, but too generic)
- **Why positive**: Abelian varieties are the geometric objects parametrized by Shimura varieties; hyperelliptic-curve-via-Jacobian research naturally leads into the arithmetic of Shimura varieties of abelian type.
- **Note**: bridge-level semantic positive — only 1 generic exact AG object term. This is the outer bridge-ring case, not a runner-facing positive under the current partial baseline.

---

## Negative Cases

| Case ID | Anchor | Target | Failure Type | Expected |
|---------|--------|--------|-------------|----------|
| `ag-n1` | `global_69` 代数叠与层理论 | `global_136` 动机层与亨泽尔层 | object_domain_mismatch | none |
| `ag-n2` | `global_30` 法诺簇模空间曲线 | `global_287` 导出代数叠范畴 | class_overlap_false_positive | none |
| `ag-n3` | `global_134` 凸体与薄饼多面体 | `global_30` 法诺簇模空间曲线 | domain_boundary_error | none |

### Case Details

#### ag-n1: global_69 → global_136

- **Anchor** `global_69`: 代数叠与层理论 — stacks, algebraic, zariski, sheaves
- **Target** `global_136`: 动机层与亨泽尔层 — motivic, schemes, sheaves, henselian
- **Why negative**: Only "sheaves" is the exact shared term (1 term, below semantic threshold); global_69 is stack-theoretic while global_136 is motivic/henselian scheme-theoretic — different AG subdomains despite both using sheaves.
- **Pipeline risk**: Pre-MAG-02 gate accepted this pair via 1 exact term (`sheaves`) plus taxonomy support. Current replay still shows overlap score `1.75`, but relation now correctly stays `none`.

#### ag-n2: global_30 → global_287

- **Anchor** `global_30`: 法诺簇模空间曲线 — toric, k3, moduli, curves
- **Target** `global_287`: 导出代数叠范畴 — stacks, derived, categories
- **Why negative**: No exact shared AG object terms; pipeline triggers via class membership (moduli≈moduli_and_stack, bundles≈sheaf_and_bundle) — Fano/K3 varieties and derived algebraic stacks are unrelated research trajectories.
- **Evidence**: Documented pipeline failure in 2026-03-17 benchmark (ag-n1 there, passed=false)

#### ag-n3: global_134 → global_30

- **Anchor** `global_134`: 凸体与薄饼多面体 — polytopes, convex, bodies, pancake
- **Target** `global_30`: 法诺簇模空间曲线 — toric, k3, moduli, curves
- **Why negative**: global_134 belongs to convex/combinatorial geometry, not algebraic geometry; zero shared AG objects. Tests domain boundary of the rule.

---

## Ambiguous Cases

| Case ID | Anchor | Target | Shared Term | Verdict |
|---------|--------|--------|-------------|---------|
| `ag-amb1` | `global_4` 分级范畴聚类 | `global_287` 导出代数叠范畴 | categories | ambiguous |

### ag-amb1: global_4 → global_287

- **Anchor** `global_4`: 分级范畴聚类 (math.AG)
  - keywords: mathcal, lie, categories, homotopy, mathfrak
- **Target** `global_287`: 导出代数叠范畴 (math.AG)
  - keywords: stacks, derived, stack, algebraic, categories, equivariant
- **Shared exact**: categories (1 term)
- **For positive**: Derived algebraic stacks are built on ∞-categorical foundations; Lie/graded category theory feeds directly into the categorical machinery underlying derived stack theory (Lurie's connection).
- **For negative**: global_4's central objects are representation-theoretic categories (Lie algebra modules, graded structures); global_287's central objects are geometric stacks — "categories" is too generic to establish AG object continuity.
- **Verdict**: ambiguous — rule requires clarification on whether abstract categorical vocabulary counts as AG object vocabulary. Genuine mathematical boundary dispute (higher category theory vs. derived algebraic geometry).

---

## Review Notes

### Known False Positive Pattern

The pre-MAG-02 gate `len(shared_math_ag_objects) >= 2 or object_overlap["score"] >= 1.5` caused two distinct false-positive modes:

- `ag-n2`: class-overlap-only false positive (`score = 2.25`, `0` exact shared terms)
- `ag-n1`: single-exact-term false positive (`score = 1.75`, only `sheaves`)

**Current state**: `math_ag_object_continuity` now requires `>=2` exact shared AG object terms. Taxonomy overlap remains diagnostic output, not an independent promotion path.

### Runner Boundary

- `ag-p1` is the only stable runner-positive under the current partial baseline.
- `ag-p2` and `ag-p3` are semantic bridge-level positives only.
- `ag-p2` / `ag-p3` should not be described as pending runner promotions unless a new rule or benchmark decision explicitly changes that status.
- The active `pipeline/math_ag_benchmark.py` runner contract is `ag-p1` + `ag-n1/ag-n2/ag-n3`.
- Legacy positive IDs `ag-b1` / `ag-e2` were duplicate aliases for `global_69 -> global_287` and have been removed from the runner-facing contract.

### Why AG Should Look Thicker Without More Runner Positives

- The AG area should become thicker because the benchmark now fixes a stable second layer around the mainline, not because we promoted more relations into the runner.
- `ag-p2` / `ag-p3` give the graph a meaningful bridge ring: they show where object continuity is semantically nearby even though the exact-term guard intentionally keeps them out of `math_ag_object_continuity`.
- `ag-n1` / `ag-n2` / `ag-n3` give the graph an excluded boundary: they show which tempting neighbors must stay outside the AG continuity story.
- This produces a stable three-band reading for downstream consumers: `confirmed core` (`ag-p1`) + `bridge ring` (`ag-p2/ag-p3`) + `excluded boundary` (`ag-n1/ag-n2/ag-n3`).

### Object Vocabulary Blind Spots

1. **"varieties" too generic**: shimura varieties / abelian varieties / Fano varieties / toric varieties all share the word; class membership alone (variety_family) creates false positives across very different AG subdisciplines.

2. **"hodge/motivic/adic" ambiguity**: These terms can be AG objects (Hodge structure, motivic motive) or methods (Hodge theory, motivic techniques); misclassification affects both false positive and false negative rates.

### Current Assessment (2026-03-21 — PKG-AG-01)

- First real benchmark batch: 3P / 3N / 1A ✅
- ag-p1: sole stable runner-positive (event-level, confirmed) ✅
- ag-p2/ag-p3: semantic bridge-level positives only; explicitly outside the runner baseline ⚠️
- ag-n1/ag-n2/ag-n3: cover 3 distinct failure modes ✅
- ag-amb1: genuine boundary dispute ✅
- graph-ready reading: `confirmed core` + `bridge ring` + `excluded boundary` ✅
- Rule status: **partial** — stable runner-ready baseline now means one event-level positive (`ag-p1`) plus fixed negatives; bridge-level cases stay out of runner unless the benchmark contract changes

## Change Log

- `2026-03-17`: 初版建立 (2026-03-17-math-ag-benchmark.md)
- `2026-03-21`: PKG-AG-01 — 第一批真实 benchmark cases 固定；扩展为 3P/3N/1A；增加 rule review notes
- `2026-03-22`: MAG-02 — clarify exact-term guard cut: `ag-n1/ag-n2` should reject; `ag-p1` stays positive; `ag-p2/ag-p3` remain bridge-level
- `2026-03-22`: MAG-03 — stabilize partial baseline wording: `ag-p1` is sole runner-positive; `ag-p2/ag-p3` are bridge-level semantic positives only
- `2026-03-22`: MAG-04 — benchmark runner contract cleaned: `ag-p1` is the only runner-positive ID; legacy aliases `ag-b1/ag-e2` removed; runner negatives aligned to `ag-n1/ag-n2/ag-n3`
- `2026-03-22`: MAG-FILL-01 — graph narrative fixed as `confirmed core` (`ag-p1`) + `bridge ring` (`ag-p2/ag-p3`) + `excluded boundary` (`ag-n1/ag-n2/ag-n3`); benchmark runner contract unchanged
