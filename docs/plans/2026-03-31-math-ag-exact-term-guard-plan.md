---
doc_type: "implementation_plan"
scope: "math > math.AG exact-term guard for object continuity"
status: "active"
owner: "trend-monitor"
package_id: "MAG-02"
upstream_docs:
  - "docs/plans/2026-03-18-math-ag-benchmark.md"
  - "docs/plans/2026-03-18-math-ag-rule-review.md"
  - "docs/plans/2026-03-10-evolution-rule-coverage.md"
downstream_docs: []
last_reviewed: "2026-03-22"
---

# Math.AG Exact-Term Guard Plan

## Goal

为 `math_ag_object_continuity` 增加一个实现边界清晰、验证面最小的 guard，优先修复当前最明确的 false positives，而不是在这轮继续扩展 Math.AG pipeline 的覆盖面。

## Current Gate

当前代码位于 `pipeline/evolution_analysis.py`：

```python
elif math_ag_domain and (len(shared_math_ag_objects) >= 2 or object_overlap["score"] >= 1.5):
    relation = "math_ag_object_continuity"
```

这会把 taxonomy overlap 当成独立准入条件，导致两类误判：

1. **class-overlap-only false positive**
   - `ag-n2` (`global_30 -> global_287`)
   - 0 exact shared AG object terms
   - taxonomy score `2.25`

2. **single-exact-term false positive**
   - `ag-n1` (`global_69 -> global_136`)
   - only 1 exact shared AG object term: `sheaves`
   - taxonomy score `1.75`

`ag-n1` 说明“require >=1 exact term”仍然不够。

## Proposed Code Change

将 `math_ag_object_continuity` 的准入条件收紧为：

```python
elif math_ag_domain and len(shared_math_ag_objects) >= 2:
    relation = "math_ag_object_continuity"
```

同时保留 `math_ag_object_matches.overlap` 的输出，不删除 taxonomy score、shared_classes、related_classes。这些字段继续作为诊断信息存在，但不再单独提升 relation。

## Expected Case Delta

| Case ID | Current | After Guard | Reason |
|---------|---------|-------------|--------|
| `ag-p1` | `math_ag_object_continuity` | `math_ag_object_continuity` | shared exact objects = `sheaf`, `stack`, `stacks` |
| `ag-n1` | `math_ag_object_continuity` | `none` | only 1 exact term (`sheaves`) |
| `ag-n2` | `math_ag_object_continuity` | `none` | 0 exact terms; taxonomy-only trigger removed |
| `ag-p2` | `none` | `none` | only 1 exact term (`curves`); remains bridge-level |
| `ag-p3` | `none` | `none` | only 1 exact generic term (`varieties`); remains bridge-level |

## Non-Goals

- 不在这轮把 `ag-p2` / `ag-p3` 升级进 runner。
- 不在这轮重做 Math.AG taxonomy。
- 不在这轮引入新的 bridge-level 规则或 generic fallback。

## Graph Narrative After The Guard

在 `>=2` exact-term guard 固定后，Math.AG 的图谱叙事应稳定成三层，而不是继续用更松的对象门槛去换更多 positives：

- `confirmed core`: `ag-p1`，唯一 runner-positive / event-level 主线
- `bridge ring`: `ag-p2` / `ag-p3`，语义上值得保留的 bridge-level positives，但不进入 runner
- `excluded boundary`: `ag-n1` / `ag-n2` / `ag-n3`，说明单个 exact term 或 taxonomy overlap 为什么必须停在边界外

这意味着后续前端或导出层若要把 AG 区域画得更厚，应优先消费这组分层元数据，而不是重新放宽 object gate。

## Minimal Validation

最小验证分两层：

1. **unit-level gate checks**
   - multi-exact-object positive 仍命中
   - class-overlap-only case 被拒绝
   - single-exact-term + taxonomy-support case 被拒绝

2. **real-case replay**
   - `ag-p1` must remain positive
   - `ag-n1` must flip to `none`
   - `ag-n2` must flip to `none`
   - `ag-p2` / `ag-p3` must remain `none`

## Residual Risk

这个 guard 会主动收紧 Math.AG object continuity 的触发面，因此任何“只有 1 个 exact object term 但语义上像 bridge-level 正例”的 pair 都不会被升级。当前这是有意行为，因为 benchmark 已明确要求先止住 false positives，再讨论 bridge-level 的单独建模。

## Post-MAG-04 Baseline Note

- `ag-p1` is now the sole runner-positive event-level case for the current partial baseline.
- `ag-p2` and `ag-p3` are fixed as semantic bridge-level positives only.
- `ag-p2/ag-p3` should not be treated as near-runner or pending runner promotions under the current contract.
- The active AG benchmark runner contract is `ag-p1` + `ag-n1/ag-n2/ag-n3`.
- Historical runner IDs `ag-b1` / `ag-e2` were duplicate aliases for the `global_69 -> global_287` pair and have been removed from the active contract.
- `pipeline/math_ag_benchmark.py` now mirrors the same split for downstream graph/export use as `confirmed_core`, `bridge_ring`, and `excluded_boundary`.
