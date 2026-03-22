doc_type: "design"
scope: "math benchmark runner architecture"
status: "draft"
owner: "trend-monitor"
source_of_truth: true
upstream_docs:
  - "docs/plans/evolution-ops/03-task-packages.md"
downstream_docs: []
last_reviewed: "2026-03-17"

# Math Benchmark Runner Design

## Purpose

设计通用 benchmark runner，统一 `math_lo` 和 `math_ag` 的实现。

## Background

当前状态：
- `math_lo_benchmark.py`: 13 cases (5 positive + 6 negative + 2 ambiguous)
- `math_ag_benchmark.py`: 6 cases (2 positive + 4 negative)
- 两者代码结构 90% 相同，仅 case 数据和输出目录不同

目标：
- 提取公共逻辑到 `math_benchmark.py`
- 保留 domain-specific case definitions
- 支持统一调用接口

## Analysis: Current Implementation

### Common Elements (LO & AG)

```python
# Shared imports
import argparse, json, datetime, pathlib
from typing import Dict, List, Sequence, Tuple
from evolution_analysis import (
    DEFAULT_INPUT, build_adjacency,
    build_bridge_evidence, load_trend_source
)

# Shared functions (identical implementation)
def build_neighbor_map(adjacency_edges) -> Dict[str, List[Tuple[str, float]]]
def evaluate_expected(actual: str, expected: str) -> Tuple[bool, str]
def evaluate_case(case, topics, neighbor_map) -> Dict[str, object]
def evaluate_benchmark(topics) -> Dict[str, object]
def build_markdown_report(report: Dict) -> str

# Shared main() structure
load_trend_source() -> topics
build_adjacency() -> edges
build_neighbor_map() -> neighbor_map
evaluate_benchmark() -> report
write json + md outputs
```

### Differences (LO vs AG)

| Aspect | math_lo | math_ag |
|--------|---------|---------|
| BENCHMARK_CASES | 5+6+2 | 2+4+0 |
| Has ambiguous section | Yes | No |
| Output dir | `math_lo/` | `math_ag/` |
| Case levels | event/bridge | event-only |

## Design Proposal

### Option A: Config-Driven Base Class (Recommended)

```python
# pipeline/math_benchmark.py
from abc import ABC, abstractmethod
from typing import Protocol

class BenchmarkCaseLoader(Protocol):
    """Domain-specific case loader"""
    def load_cases(self) -> Dict[str, List[Dict]]: ...
    def get_domain_name(self) -> str: ...

class BaseBenchmarkRunner:
    """Shared benchmark execution logic"""

    def __init__(self, case_loader: BenchmarkCaseLoader):
        self.case_loader = case_loader
        self.domain = case_loader.get_domain_name()

    def run(self, input_path: Path, output_dir: Path) -> Dict:
        topics = self._load_topics(input_path)
        edges = build_adjacency(topics)
        neighbor_map = self._build_neighbor_map(edges)

        report = self._evaluate_benchmark(topics, neighbor_map)
        self._write_outputs(report, output_dir)
        return report

    def _evaluate_benchmark(self, topics, neighbor_map) -> Dict:
        cases = self.case_loader.load_cases()
        # ... shared evaluation logic

    # ... other shared methods

class ScoreCalculator:
    """Unified scoring across domains"""

    def calculate(self, sections: Dict[str, List[Dict]]) -> Dict[str, float]:
        return {
            "total_cases": total,
            "passed_cases": passed,
            "failed_cases": failed,
            "pass_rate": passed / total if total else 0,
            "by_section": {
                section: self._section_score(cases)
                for section, cases in sections.items()
            }
        }
```

### Option B: Functional Composition

```python
# pipeline/math_benchmark.py

def create_benchmark_runner(
    cases: Dict[str, List[Dict]],
    domain_name: str,
    output_dir: Path
) -> Callable:
    """Factory function creating domain-specific runner"""

    def runner(input_path: Path) -> Dict:
        # Shared logic using injected cases/domain/output_dir
        ...

    return runner

# Usage in math_lo_benchmark.py
from pipeline.math_benchmark import create_benchmark_runner
from .cases.math_lo import BENCHMARK_CASES

run_math_lo_benchmark = create_benchmark_runner(
    cases=BENCHMARK_CASES,
    domain_name="math_lo",
    output_dir=Path("data/output/benchmarks/math_lo")
)

if __name__ == "__main__":
    run_math_lo_benchmark(parse_args().input)
```

## Recommended: Option A (Class-Based)

理由：
1. 更清晰的分层（base / domain / test）
2. 更容易扩展新 domain
3. 支持依赖注入，便于测试
4. 符合现有代码风格

## Detailed Design

### 1. Input Spec

```python
class BenchmarkInput:
    """Standardized benchmark input"""
    aligned_topics_path: Path
    domain_config: DomainConfig  # cases, scoring rules, etc.

class DomainConfig:
    """Domain-specific configuration"""
    name: str                    # "math_lo", "math_ag", etc.
    cases: BenchmarkCases        # positive/negative/ambiguous
    output_subdir: str
    scoring_weights: Dict[str, float]  # optional per-domain weights
```

### 2. Output Report Structure

```python
class BenchmarkReport:
    version: str = "1.0"
    generated_at: datetime
    domain: str

    summary: SummaryStats
    sections: Dict[str, SectionResult]

class SummaryStats:
    total_cases: int
    passed_cases: int
    failed_cases: int
    pass_rate: float

class SectionResult:
    cases: List[CaseResult]
    passed_count: int
    failed_count: int

class CaseResult:
    case_id: str
    anchor_topic_id: str
    anchor_topic_name: str
    target_topic_id: str
    target_topic_name: str
    expected_relation: str
    actual_relation: str
    passed: bool
    reason: str
    level: Optional[str]  # event-level, bridge-level
    confidence: Optional[float]
    pipeline_relation: Dict
    evidence: Dict
```

### 3. Score Calculation Strategy

```python
class ScoreStrategy(ABC):
    @abstractmethod
    def calculate(self, sections: Dict[str, List[CaseResult]]) -> ScoreBreakdown:
        ...

class DefaultScoreStrategy(ScoreStrategy):
    """Default: all cases weighted equally"""
    def calculate(self, sections) -> ScoreBreakdown:
        total = sum(len(cases) for cases in sections.values())
        passed = sum(
            sum(1 for c in cases if c.passed)
            for cases in sections.values()
        )
        return ScoreBreakdown(
            total=total,
            passed=passed,
            failed=total - passed,
            by_section={
                name: SectionScore(...)
                for name, cases in sections.items()
            }
        )

class WeightedScoreStrategy(ScoreStrategy):
    """Weighted: event-level cases worth more than bridge-level"""
    weights = {"positive": 1.5, "negative": 1.0, "ambiguous": 0.5}
    # ...
```

### 4. Wrapper Implementation

```python
# pipeline/math_lo_benchmark.py (refactored)
from pipeline.math_benchmark import BaseBenchmarkRunner, BenchmarkCaseLoader

class MathLOCaseLoader(BenchmarkCaseLoader):
    def load_cases(self) -> Dict[str, List[Dict]]:
        return {
            "positive": [...],
            "negative": [...],
            "ambiguous": [...],  # LO has ambiguous
        }

    def get_domain_name(self) -> str:
        return "math_lo"

def main():
    runner = BaseBenchmarkRunner(MathLOCaseLoader())
    args = parse_args()
    report = runner.run(
        input_path=args.input,
        output_dir=args.output_dir or Path("data/output/benchmarks/math_lo")
    )
    print(f"Benchmark complete: {report['summary']['pass_rate']:.1%} pass rate")

# pipeline/math_ag_benchmark.py (refactored)
class MathAGCaseLoader(BenchmarkCaseLoader):
    def load_cases(self) -> Dict[str, List[Dict]]:
        return {
            "positive": [...],
            "negative": [...],
            # No ambiguous section for AG
        }

    def get_domain_name(self) -> str:
        return "math_ag"

def main():
    runner = BaseBenchmarkRunner(MathAGCaseLoader())
    # ...
```

### 5. Unified CLI Interface

```python
# pipeline/math_benchmark.py

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", choices=["math_lo", "math_ag", "all"])
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()

    if args.domain == "all":
        for loader in [MathLOCaseLoader(), MathAGCaseLoader()]:
            runner = BaseBenchmarkRunner(loader)
            runner.run(args.input, args.output_dir)
    else:
        loader = get_loader_for_domain(args.domain)
        runner = BaseBenchmarkRunner(loader)
        runner.run(args.input, args.output_dir)
```

### 6. Makefile Integration

```makefile
math-benchmark:
	python3 pipeline/math_benchmark.py --domain all

math-lo-benchmark:
	python3 pipeline/math_benchmark.py --domain math_lo
	# Or keep backward compatibility:
	# python3 pipeline/math_lo_benchmark.py

math-ag-benchmark:
	python3 pipeline/math_benchmark.py --domain math_ag
	# Or: python3 pipeline/math_ag_benchmark.py
```

## Migration Plan

### Phase 1: Create Base Infrastructure
1. Create `pipeline/math_benchmark.py` with base classes
2. Create `pipeline/benchmark/cases/` directory
3. Move cases to `pipeline/benchmark/cases/math_lo.py` and `math_ag.py`

### Phase 2: Refactor Existing Runners
1. Update `math_lo_benchmark.py` to use base class
2. Update `math_ag_benchmark.py` to use base class
3. Ensure backward compatibility (old CLI still works)

### Phase 3: Unified Interface
1. Add `--domain` parameter to `math_benchmark.py`
2. Add `math-benchmark` make target
3. Update documentation

### Phase 4: Cleanup
1. Deprecate old standalone runners (optional)
2. Consolidate tests to `test_math_benchmark.py`

## Open Questions

1. **Ambiguous section handling**: Should base class support optional sections?
2. **Scoring weights**: Do different domains need different scoring strategies?
3. **Test strategy**: Keep separate test files or unify to `test_math_benchmark.py`?
4. **Case definitions**: Move to YAML/JSON files instead of Python dicts?

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-03-17 | Use Option A (Class-based) | Clearer separation, easier to extend |
| 2026-03-17 | Keep backward compatibility | Don't break existing make targets |

## Next Steps

1. Review this design with stakeholders
2. Create `pipeline/math_benchmark.py` skeleton
3. Implement base classes
4. Refactor LO runner as proof of concept
5. Refactor AG runner
6. Add unified CLI
7. Update tests

---

**Status**: Design draft ready for review
**Blocking**: None (LO and AG already aligned)
**Estimated effort**: 1-2 sessions
