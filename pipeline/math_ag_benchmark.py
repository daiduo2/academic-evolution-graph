import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

try:
    from evolution_analysis import DEFAULT_INPUT, build_adjacency, build_bridge_evidence, load_trend_source
except ModuleNotFoundError:
    from pipeline.evolution_analysis import DEFAULT_INPUT, build_adjacency, build_bridge_evidence, load_trend_source

# Import shared functionality from generic benchmark core
try:
    from pipeline.math_benchmark import (
        build_neighbor_map,
        evaluate_expected,
        evaluate_case,
        evaluate_benchmark,
        build_markdown_report,
        write_benchmark_outputs,
        run_benchmark,
    )
except ModuleNotFoundError:
    from math_benchmark import (
        build_neighbor_map,
        evaluate_expected,
        evaluate_case,
        evaluate_benchmark,
        build_markdown_report,
        write_benchmark_outputs,
        run_benchmark,
    )

AG_CASE_REGISTRY = {
    "ag-p1": {
        "case_id": "ag-p1",
        "anchor": "global_69",
        "target": "global_287",
        "expected_relation": "math_ag_object_continuity",
        "level": "event-level",
        "confidence": 0.85,
        "narrative_layer": "confirmed_core",
        "runner_role": "runner-positive",
        "narrative_note": "唯一稳定 runner-positive；作为 AG 主线 confirmed core 保留。",
        "evidence": {
            "shared_objects": ["stack", "stacks"],
            "taxonomy_overlap": ["moduli_and_stack"],
        },
    },
    "ag-p2": {
        "case_id": "ag-p2",
        "anchor": "global_30",
        "target": "global_355",
        "expected_relation": "none",
        "level": "bridge-level",
        "confidence": 0.65,
        "narrative_layer": "bridge_ring",
        "runner_role": "semantic-bridge-positive",
        "narrative_note": "共享 curves；值得作为 bridge ring 呈现，但不通过当前 exact-term gate。",
        "evidence": {
            "shared_objects": ["curves"],
            "taxonomy_overlap": ["variety_family"],
        },
    },
    "ag-p3": {
        "case_id": "ag-p3",
        "anchor": "global_355",
        "target": "global_117",
        "expected_relation": "none",
        "level": "bridge-level",
        "confidence": 0.60,
        "narrative_layer": "bridge_ring",
        "runner_role": "semantic-bridge-positive",
        "narrative_note": "共享 generic varieties；保留为 bridge ring 的远端支撑，不升级为 runner-positive。",
        "evidence": {
            "shared_objects": ["varieties"],
            "taxonomy_overlap": ["variety_family"],
        },
    },
    "ag-n1": {
        "case_id": "ag-n1",
        "anchor": "global_69",
        "target": "global_136",
        "expected_relation": "none",
        "narrative_layer": "excluded_boundary",
        "runner_role": "excluded-boundary",
        "reason": "仅共享 sheaves (1 个对象词)；不满足当前 >=2 exact-term gate",
    },
    "ag-n2": {
        "case_id": "ag-n2",
        "anchor": "global_30",
        "target": "global_287",
        "expected_relation": "none",
        "narrative_layer": "excluded_boundary",
        "runner_role": "excluded-boundary",
        "reason": "class-overlap-only false positive；无 exact shared AG object terms",
    },
    "ag-n3": {
        "case_id": "ag-n3",
        "anchor": "global_134",
        "target": "global_30",
        "expected_relation": "none",
        "narrative_layer": "excluded_boundary",
        "runner_role": "excluded-boundary",
        "reason": "domain boundary negative；凸几何主题不应进入 math.AG object continuity",
    },
}

# Curated graph/export narrative for Math.AG. This is intentionally wider than the
# runner-facing benchmark contract: ag-p2/ag-p3 remain visible as bridge-ring
# support, while ag-n1/ag-n2/ag-n3 explain the excluded boundary around the core.
AG_GRAPH_LAYERS = {
    "confirmed_core": {
        "summary": "Runner-confirmed event-level core for the current AG mainline.",
        "case_ids": ["ag-p1"],
    },
    "bridge_ring": {
        "summary": "Semantic bridge-level positives worth showing around the core, but not promoted by the current gate or runner.",
        "case_ids": ["ag-p2", "ag-p3"],
    },
    "excluded_boundary": {
        "summary": "Nearby negatives that keep the AG region bounded even when vocabulary or taxonomy overlap looks tempting.",
        "case_ids": ["ag-n1", "ag-n2", "ag-n3"],
    },
}

BENCHMARK_CASES = {
    "positive": [
        # Runner-facing contract: ag-p1 is the sole active positive baseline.
        # Historical runner aliases ag-b1/ag-e2 pointed to this same pair and are retired.
        AG_CASE_REGISTRY["ag-p1"],
        # NOTE: math_ag_method_continuity cases are NOT included here
        # They are test-evidence-only, not benchmark-ready
        # See docs/plans/2026-03-18-math-ag-benchmark.md for details
    ],
    "negative": [
        AG_CASE_REGISTRY["ag-n1"],
        AG_CASE_REGISTRY["ag-n2"],
        AG_CASE_REGISTRY["ag-n3"],
        # NOTE: ag-n5 removed - reverse evolution case with high object overlap
        # This is a boundary case where shared_objects >= 2 triggers continuity
        # even though direction is reversed. Not suitable for stable benchmark.
        # {
        #     "case_id": "ag-n5",
        #     "anchor": "global_287",
        #     "target": "global_69",
        #     "expected_relation": "none",
        #     "reason": "反向演化，但共享3个对象词触发规则 - 边界情况",
        # },
        # NOTE: ag-method-n1 is NOT included here
        # Method continuity is test-evidence-only, not in benchmark runner
    ],
}


# Note: build_neighbor_map, evaluate_expected, evaluate_case, evaluate_benchmark,
# build_markdown_report are now imported from pipeline.math_benchmark
# Keeping re-exports for backward compatibility if any external code imports them
__all__ = [
    "AG_CASE_REGISTRY",
    "AG_GRAPH_LAYERS",
    "BENCHMARK_CASES",
    "build_neighbor_map",
    "evaluate_expected",
    "evaluate_case",
    "evaluate_benchmark",
    "build_markdown_report",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Math.AG benchmark checks.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="Path to aligned topics JSON.")
    parser.add_argument("--output-dir", type=Path, default=Path("data/output/benchmarks/math_ag"), help="Output directory.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Use generic benchmark core with domain-specific config
    report = run_benchmark(
        input_path=args.input,
        output_dir=args.output_dir,
        cases=BENCHMARK_CASES,
        json_filename="math_ag_benchmark.json",
        md_filename="math_ag_benchmark.md",
        markdown_title="Math.AG Benchmark Report",
        section_order=["positive", "negative"],
    )

    print(f"Wrote benchmark report to {args.output_dir}")


if __name__ == "__main__":
    main()
