# Math.AG Benchmark Report

- Generated at: 2026-03-17T15:03:00.711227+00:00
- Total cases: 6
- Passed: 2
- Failed: 4

## Positive Cases

- `ag-b1` PASS: 代数叠与层理论 -> 导出代数叠范畴 (expected `math_ag_object_continuity`, actual `math_ag_object_continuity`)
- `ag-e2` PASS: 代数叠与层理论 -> 导出代数叠范畴 (expected `math_ag_object_continuity`, actual `math_ag_object_continuity`) (confidence=0.85)

## Negative Cases

- `ag-n1` FAIL: 法诺簇模空间曲线 -> 导出代数叠范畴 (expected `none`, actual `math_ag_object_continuity`)
- `ag-n2` FAIL: 法诺簇模空间曲线 -> 代数叠与层理论 (expected `none`, actual `math_ag_object_continuity`)
- `ag-n3` FAIL: 导出代数叠范畴 -> 法诺簇模空间曲线 (expected `none`, actual `math_ag_object_continuity`)
- `ag-n4` FAIL: 代数叠与层理论 -> 法诺簇模空间曲线 (expected `none`, actual `math_ag_object_continuity`)
