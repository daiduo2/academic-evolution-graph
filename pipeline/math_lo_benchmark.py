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


BENCHMARK_CASES = {
    "positive": [
        {
            "case_id": "lo-b1",
            "anchor": "global_56",
            "target": "global_27",
            "expected_relation": "math_lo_modal_continuity",
            "level": "event-level",
        },
        {
            "case_id": "lo-b2",
            "anchor": "global_56",
            "target": "global_980",
            "expected_relation": "math_lo_type_theory_continuity",
            "level": "bridge-level",
        },
        {
            "case_id": "lo-b3",
            "anchor": "global_313",
            "target": "global_360",
            "expected_relation": "math_lo_set_theory_continuity",
            "level": "bridge-level",
        },
        {
            "case_id": "lo-b4",
            "anchor": "global_51",
            "target": "global_951",
            "expected_relation": "math_lo_forcing_continuity",
            "level": "bridge-level",
        },
        {
            "case_id": "lo-b5",
            "anchor": "global_75",
            "target": "global_778",
            "expected_relation": "math_lo_definability_continuity",
            "level": "bridge-level",
        },
    ],
    "negative": [
        {
            "case_id": "lo-n1",
            "anchor": "global_51",
            "target": "global_75",
            "expected_relation": "not math_lo_forcing_continuity",
        },
        {
            "case_id": "lo-n2",
            "anchor": "global_339",
            "target": "global_951",
            "expected_relation": "none",
        },
        {
            "case_id": "lo-n3",
            "anchor": "global_167",
            "target": "global_778",
            "expected_relation": "none",
        },
        {
            "case_id": "lo-n4",
            "anchor": "global_361",
            "target": "global_778",
            "expected_relation": "none",
        },
        {
            "case_id": "lo-n5",
            "anchor": "global_56",
            "target": "global_438",
            "expected_relation": "none",
        },
        {
            "case_id": "lo-n6",
            "anchor": "global_980",
            "target": "global_438",
            "expected_relation": "none",
        },
    ],
    "ambiguous": [
        {
            "case_id": "lo-a1",
            "anchor": "global_75",
            "target": "global_951",
            "expected_relation": "review-needed",
        },
        {
            "case_id": "lo-a2",
            "anchor": "global_339",
            "target": "global_51",
            "expected_relation": "review-needed",
        },
    ],
}


# Note: build_neighbor_map, evaluate_expected, evaluate_case, evaluate_benchmark,
# build_markdown_report are now imported from pipeline.math_benchmark
# Keeping re-exports for backward compatibility if any external code imports them
__all__ = [
    "BENCHMARK_CASES",
    "build_neighbor_map",
    "evaluate_expected",
    "evaluate_case",
    "evaluate_benchmark",
    "build_markdown_report",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Math.LO benchmark checks.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="Path to aligned topics JSON.")
    parser.add_argument("--output-dir", type=Path, default=Path("data/output/benchmarks/math_lo"), help="Output directory.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Use generic benchmark core with domain-specific config
    report = run_benchmark(
        input_path=args.input,
        output_dir=args.output_dir,
        cases=BENCHMARK_CASES,
        json_filename="math_lo_benchmark.json",
        md_filename="math_lo_benchmark.md",
        markdown_title="Math.LO Benchmark Report",
        section_order=["positive", "negative", "ambiguous"],
    )

    print(f"Wrote benchmark report to {args.output_dir}")


if __name__ == "__main__":
    main()
