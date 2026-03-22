"""
Tests for generic math benchmark core (pipeline/math_benchmark.py).

These tests verify the shared functionality used by domain-specific runners.
"""
import pytest
from datetime import datetime, timezone
from typing import Dict, List, Tuple

try:
    from pipeline.math_benchmark import (
        build_neighbor_map,
        evaluate_expected,
        build_markdown_report,
    )
except ModuleNotFoundError:
    import sys
    sys.path.insert(0, "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor")
    from pipeline.math_benchmark import (
        build_neighbor_map,
        evaluate_expected,
        build_markdown_report,
    )


class TestEvaluateExpected:
    """Test evaluate_expected function."""

    def test_exact_match_passes(self):
        """Exact relation match should pass."""
        passed, reason = evaluate_expected("math_lo_modal_continuity", "math_lo_modal_continuity")
        assert passed is True
        assert reason == "ok"

    def test_mismatch_fails(self):
        """Relation mismatch should fail."""
        passed, reason = evaluate_expected("none", "math_lo_modal_continuity")
        assert passed is False
        assert reason == "mismatch"

    def test_forbidden_relation_when_different_passes(self):
        """Not-X constraint passes when actual is different."""
        passed, reason = evaluate_expected("math_lo_set_theory_continuity", "not math_lo_forcing_continuity")
        assert passed is True
        assert reason == "ok"

    def test_forbidden_relation_when_same_fails(self):
        """Not-X constraint fails when actual equals forbidden."""
        passed, reason = evaluate_expected("math_lo_forcing_continuity", "not math_lo_forcing_continuity")
        assert passed is False
        assert reason == "forbidden_relation"

    def test_review_needed_always_passes(self):
        """review-needed expectation always passes."""
        passed, reason = evaluate_expected("none", "review-needed")
        assert passed is True
        assert reason == "review_only"

    def test_none_equals_none_passes(self):
        """Expected none with actual none should pass."""
        passed, reason = evaluate_expected("none", "none")
        assert passed is True
        assert reason == "ok"


class TestBuildNeighborMap:
    """Test build_neighbor_map function."""

    def test_empty_edges_returns_empty(self):
        """Empty edge list should return empty dict."""
        result = build_neighbor_map([])
        assert result == {}

    def test_single_edge_creates_bidirectional(self):
        """Single edge should create bidirectional neighbors."""
        edges = [{"source": "A", "target": "B", "weight": 0.5}]
        result = build_neighbor_map(edges)
        assert result == {
            "A": [("B", 0.5)],
            "B": [("A", 0.5)],
        }

    def test_multiple_edges_aggregate(self):
        """Multiple edges to same node should aggregate."""
        edges = [
            {"source": "A", "target": "B", "weight": 0.8},
            {"source": "A", "target": "C", "weight": 0.6},
        ]
        result = build_neighbor_map(edges)
        assert "A" in result
        assert len(result["A"]) == 2
        # Should be sorted by weight descending
        assert result["A"][0] == ("B", 0.8)
        assert result["A"][1] == ("C", 0.6)

    def test_weight_sorting_descending(self):
        """Neighbors should be sorted by weight descending."""
        edges = [
            {"source": "A", "target": "C", "weight": 0.3},
            {"source": "A", "target": "B", "weight": 0.9},
            {"source": "A", "target": "D", "weight": 0.6},
        ]
        result = build_neighbor_map(edges)
        weights = [w for _, w in result["A"]]
        assert weights == [0.9, 0.6, 0.3]

    def test_tie_breaker_by_id(self):
        """Same weight neighbors sorted by ID."""
        edges = [
            {"source": "A", "target": "C", "weight": 0.5},
            {"source": "A", "target": "B", "weight": 0.5},
        ]
        result = build_neighbor_map(edges)
        # Should be sorted by ID ascending when weights are equal
        ids = [n for n, _ in result["A"]]
        assert ids == ["B", "C"]


class TestBuildMarkdownReport:
    """Test build_markdown_report function."""

    @pytest.fixture
    def sample_report(self) -> Dict:
        """Create a sample benchmark report."""
        return {
            "version": "1.0",
            "generated_at": "2026-03-17T10:00:00+00:00",
            "total_cases": 3,
            "passed_cases": 2,
            "failed_cases": 1,
            "sections": {
                "positive": [
                    {
                        "case_id": "test-1",
                        "anchor_topic_name": "Topic A",
                        "target_topic_name": "Topic B",
                        "expected_relation": "continuity",
                        "actual_relation": "continuity",
                        "passed": True,
                        "confidence": 0.85,
                    },
                ],
                "negative": [
                    {
                        "case_id": "test-2",
                        "anchor_topic_name": "Topic C",
                        "target_topic_name": "Topic D",
                        "expected_relation": "none",
                        "actual_relation": "none",
                        "passed": True,
                    },
                    {
                        "case_id": "test-3",
                        "anchor_topic_name": "Topic E",
                        "target_topic_name": "Topic F",
                        "expected_relation": "none",
                        "actual_relation": "continuity",
                        "passed": False,
                    },
                ],
            },
        }

    def test_report_contains_title(self, sample_report):
        """Report should contain the title."""
        md = build_markdown_report(sample_report, "Test Benchmark")
        assert "# Test Benchmark" in md

    def test_report_contains_summary_stats(self, sample_report):
        """Report should contain summary statistics."""
        md = build_markdown_report(sample_report, "Test Benchmark")
        assert "Total cases: 3" in md
        assert "Passed: 2" in md
        assert "Failed: 1" in md

    def test_report_contains_section_headers(self, sample_report):
        """Report should contain section headers."""
        md = build_markdown_report(sample_report, "Test Benchmark")
        assert "## Positive Cases" in md
        assert "## Negative Cases" in md

    def test_report_shows_pass_status(self, sample_report):
        """Report should show PASS for passing cases."""
        md = build_markdown_report(sample_report, "Test Benchmark")
        assert "`test-1` PASS:" in md
        assert "`test-2` PASS:" in md

    def test_report_shows_fail_status(self, sample_report):
        """Report should show FAIL for failing cases."""
        md = build_markdown_report(sample_report, "Test Benchmark")
        assert "`test-3` FAIL:" in md

    def test_report_includes_confidence(self, sample_report):
        """Report should include confidence when present."""
        md = build_markdown_report(sample_report, "Test Benchmark")
        assert "(confidence=0.85)" in md

    def test_report_shows_expected_actual_relations(self, sample_report):
        """Report should show expected and actual relations."""
        md = build_markdown_report(sample_report, "Test Benchmark")
        assert "(expected `continuity`, actual `continuity`)" in md
        assert "(expected `none`, actual `continuity`)" in md

    def test_custom_section_order(self, sample_report):
        """Custom section order should be respected."""
        md = build_markdown_report(
            sample_report,
            "Test Benchmark",
            section_order=["negative", "positive"]
        )
        # Negative should appear before positive in the output
        negative_pos = md.find("## Negative Cases")
        positive_pos = md.find("## Positive Cases")
        assert negative_pos < positive_pos

    def test_missing_section_skipped(self, sample_report):
        """Sections not in report should be skipped."""
        md = build_markdown_report(
            sample_report,
            "Test Benchmark",
            section_order=["ambiguous", "positive", "negative"]
        )
        # ambiguous not in report, so shouldn't appear
        assert "## Ambiguous Cases" not in md
        # But positive and negative should
        assert "## Positive Cases" in md
        assert "## Negative Cases" in md


class TestIntegration:
    """Integration tests for core functionality."""

    def test_evaluate_expected_with_various_relations(self):
        """Test various relation combinations."""
        test_cases = [
            # (actual, expected, should_pass)
            ("relation_a", "relation_a", True),
            ("relation_a", "relation_b", False),
            ("none", "none", True),
            ("continuity", "none", False),
            ("none", "not continuity", True),
            ("continuity", "not continuity", False),
            ("math_ag_object_continuity", "math_ag_object_continuity", True),
            ("math_lo_modal_continuity", "math_lo_modal_continuity", True),
        ]

        for actual, expected, should_pass in test_cases:
            passed, _ = evaluate_expected(actual, expected)
            assert passed == should_pass, \
                f"evaluate_expected({actual!r}, {expected!r}) should return {should_pass}, got {passed}"
