"""
Generic math benchmark runner core.

Provides shared functionality for domain-specific benchmark runners.
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple, Callable

try:
    from evolution_analysis import DEFAULT_INPUT, build_adjacency, build_bridge_evidence, load_trend_source
except ModuleNotFoundError:
    from pipeline.evolution_analysis import DEFAULT_INPUT, build_adjacency, build_bridge_evidence, load_trend_source


def build_neighbor_map(adjacency_edges: Sequence[Dict[str, object]]) -> Dict[str, List[Tuple[str, float]]]:
    """Build neighbor map from adjacency edges."""
    neighbors: Dict[str, List[Tuple[str, float]]] = {}
    for edge in adjacency_edges:
        neighbors.setdefault(edge["source"], []).append((edge["target"], float(edge["weight"])))
        neighbors.setdefault(edge["target"], []).append((edge["source"], float(edge["weight"])))
    for topic_id, values in neighbors.items():
        values.sort(key=lambda item: (-item[1], item[0]))
    return neighbors


def evaluate_expected(actual_relation: str, expected_relation: str) -> Tuple[bool, str]:
    """
    Evaluate if actual relation matches expected relation.

    Returns:
        (passed, reason) tuple
    """
    if expected_relation == "review-needed":
        return True, "review_only"
    if expected_relation.startswith("not "):
        forbidden = expected_relation[4:]
        ok = actual_relation != forbidden
        return ok, "forbidden_relation" if not ok else "ok"
    ok = actual_relation == expected_relation
    return ok, "mismatch" if not ok else "ok"


def evaluate_case(
    case: Dict[str, object],
    topics: Dict,
    neighbor_map: Dict[str, List[Tuple[str, float]]]
) -> Dict[str, object]:
    """Evaluate a single benchmark case."""
    anchor = topics[case["anchor"]]
    target = topics[case["target"]]
    neighbors = neighbor_map.get(case["anchor"], [])
    bridge = build_bridge_evidence(anchor, target, neighbors, topics)
    relation = (bridge.get("pipeline_relation") or {}).get("relation", "none")
    passed, reason = evaluate_expected(relation, case["expected_relation"])
    return {
        "case_id": case["case_id"],
        "anchor_topic_id": case["anchor"],
        "anchor_topic_name": anchor.name,
        "target_topic_id": case["target"],
        "target_topic_name": target.name,
        "expected_relation": case["expected_relation"],
        "actual_relation": relation,
        "passed": passed,
        "reason": reason,
        "level": case.get("level", "bridge-level"),
        "confidence": case.get("confidence"),
        "pipeline_relation": bridge.get("pipeline_relation", {}),
        "evidence": case.get("evidence", {}),
    }


def evaluate_benchmark(
    topics: Dict,
    cases: Dict[str, List[Dict[str, object]]]
) -> Dict[str, object]:
    """
    Evaluate all benchmark cases.

    Args:
        topics: Loaded topic dictionary
        cases: Dictionary of case sections (positive, negative, ambiguous, etc.)

    Returns:
        Benchmark report dictionary
    """
    adjacency_edges = build_adjacency(topics)
    neighbor_map = build_neighbor_map(adjacency_edges)
    sections = {}
    total = 0
    passed = 0
    for section, case_list in cases.items():
        results = [evaluate_case(case, topics, neighbor_map) for case in case_list]
        sections[section] = results
        total += len(results)
        passed += sum(1 for item in results if item["passed"])
    return {
        "version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_cases": total,
        "passed_cases": passed,
        "failed_cases": total - passed,
        "sections": sections,
    }


def build_markdown_report(
    report: Dict[str, object],
    title: str,
    section_order: Optional[List[str]] = None
) -> str:
    """
    Build markdown report from benchmark results.

    Args:
        report: Benchmark report dictionary
        title: Report title
        section_order: Optional order of sections (defaults to dict iteration order)

    Returns:
        Markdown formatted report string
    """
    lines = [
        f"# {title}",
        "",
        f"- Generated at: {report['generated_at']}",
        f"- Total cases: {report['total_cases']}",
        f"- Passed: {report['passed_cases']}",
        f"- Failed: {report['failed_cases']}",
        "",
    ]
    sections = report["sections"]
    if section_order is None:
        section_order = list(sections.keys())

    for section in section_order:
        if section not in sections:
            continue
        lines.extend([f"## {section.title()} Cases", ""])
        for item in sections[section]:
            status = "PASS" if item["passed"] else "FAIL"
            confidence = f" (confidence={item['confidence']})" if item.get("confidence") else ""
            lines.append(
                f"- `{item['case_id']}` {status}: {item['anchor_topic_name']} -> {item['target_topic_name']} "
                f"(expected `{item['expected_relation']}`, actual `{item['actual_relation']}`){confidence}"
            )
        lines.append("")
    return "\n".join(lines)


def write_benchmark_outputs(
    report: Dict[str, object],
    output_dir: Path,
    json_filename: str,
    md_filename: str,
    markdown_title: str,
    section_order: Optional[List[str]] = None
) -> None:
    """
    Write benchmark outputs to files.

    Args:
        report: Benchmark report dictionary
        output_dir: Output directory path
        json_filename: Name of JSON output file
        md_filename: Name of markdown output file
        markdown_title: Title for markdown report
        section_order: Optional section ordering for markdown
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / json_filename).write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    report_md = build_markdown_report(report, markdown_title, section_order)
    (output_dir / md_filename).write_text(report_md, encoding="utf-8")


def run_benchmark(
    input_path: Path,
    output_dir: Path,
    cases: Dict[str, List[Dict[str, object]]],
    json_filename: str,
    md_filename: str,
    markdown_title: str,
    section_order: Optional[List[str]] = None
) -> Dict[str, object]:
    """
    Run complete benchmark workflow.

    Args:
        input_path: Path to aligned topics JSON
        output_dir: Output directory for reports
        cases: Benchmark cases dictionary
        json_filename: JSON output filename
        md_filename: Markdown output filename
        markdown_title: Title for markdown report
        section_order: Optional section ordering

    Returns:
        Benchmark report dictionary
    """
    _, topics = load_trend_source(input_path)
    report = evaluate_benchmark(topics, cases)
    write_benchmark_outputs(
        report, output_dir, json_filename, md_filename,
        markdown_title, section_order
    )
    return report


# Domain registry for unified CLI
# Maps domain names to their configuration
DOMAIN_REGISTRY = {
    "math_lo": {
        "cases_module": "math_lo_benchmark",
        "cases_attr": "BENCHMARK_CASES",
        "output_dir": "data/output/benchmarks/math_lo",
        "json_filename": "math_lo_benchmark.json",
        "md_filename": "math_lo_benchmark.md",
        "title": "Math.LO Benchmark Report",
        "section_order": ["positive", "negative", "ambiguous"],
    },
    "math_ag": {
        "cases_module": "math_ag_benchmark",
        "cases_attr": "BENCHMARK_CASES",
        "output_dir": "data/output/benchmarks/math_ag",
        "json_filename": "math_ag_benchmark.json",
        "md_filename": "math_ag_benchmark.md",
        "title": "Math.AG Benchmark Report",
        "section_order": ["positive", "negative"],
    },
}


def load_domain_cases(domain: str) -> Dict[str, List[Dict[str, object]]]:
    """Load benchmark cases for a specific domain."""
    if domain not in DOMAIN_REGISTRY:
        raise ValueError(f"Unknown domain: {domain}. Available: {list(DOMAIN_REGISTRY.keys())}")

    config = DOMAIN_REGISTRY[domain]
    module_name = config["cases_module"]

    # Try to import from pipeline package first, then as standalone
    try:
        module = __import__(f"pipeline.{module_name}", fromlist=[config["cases_attr"]])
    except ImportError:
        module = __import__(module_name, fromlist=[config["cases_attr"]])

    return getattr(module, config["cases_attr"])


def run_domain_benchmark(
    domain: str,
    input_path: Path,
    output_dir: Optional[Path] = None
) -> Dict[str, object]:
    """Run benchmark for a specific domain."""
    if domain not in DOMAIN_REGISTRY:
        raise ValueError(f"Unknown domain: {domain}. Available: {list(DOMAIN_REGISTRY.keys())}")

    config = DOMAIN_REGISTRY[domain]
    cases = load_domain_cases(domain)

    if output_dir is None:
        output_dir = Path(config["output_dir"])

    return run_benchmark(
        input_path=input_path,
        output_dir=output_dir,
        cases=cases,
        json_filename=config["json_filename"],
        md_filename=config["md_filename"],
        markdown_title=config["title"],
        section_order=config["section_order"],
    )


def parse_args() -> argparse.Namespace:
    """Parse command line arguments for unified CLI."""
    parser = argparse.ArgumentParser(
        description="Unified math benchmark runner supporting multiple domains."
    )
    parser.add_argument(
        "--domain",
        choices=list(DOMAIN_REGISTRY.keys()),
        required=True,
        help="Benchmark domain to run (e.g., math_lo, math_ag)",
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help="Path to aligned topics JSON.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Override output directory (defaults to domain-specific location).",
    )
    return parser.parse_args()


def main() -> None:
    """Main entry point for unified CLI."""
    args = parse_args()

    report = run_domain_benchmark(
        domain=args.domain,
        input_path=args.input,
        output_dir=args.output_dir,
    )

    output_dir = args.output_dir or Path(DOMAIN_REGISTRY[args.domain]["output_dir"])
    print(f"Wrote benchmark report to {output_dir}")
    print(f"Summary: {report['passed_cases']}/{report['total_cases']} passed")


# Unified CLI entry point
if __name__ == "__main__":
    main()
