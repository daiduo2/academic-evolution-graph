"""
Tests for Math Knowledge Graph v1 export (pipeline/math_kg_export.py).

These tests verify the KG export output structure, schema compliance,
and benchmark case annotations.
"""
import json
import pytest
import tempfile
from pathlib import Path
from typing import Dict, List, Any

try:
    from pipeline.math_kg_export import (
        load_hierarchy_data,
        parse_benchmark_docs,
        export_kg_v1,
    )
except ModuleNotFoundError:
    import sys
    sys.path.insert(0, "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor")
    from pipeline.math_kg_export import (
        load_hierarchy_data,
        parse_benchmark_docs,
        export_kg_v1,
    )

try:
    from pipeline.math_kg_export import parse_pr_docs
except ImportError:
    parse_pr_docs = None


# Fixtures

@pytest.fixture
def fresh_export_dir() -> Path:
    """Create temp dir, run exporter, return path."""
    worktree_root = Path("/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor")
    with tempfile.TemporaryDirectory() as tmpdir:
        export_kg_v1(
            input_file=str(worktree_root / "data/output/aligned_topics_hierarchy.json"),
            benchmark_lo=str(worktree_root / "docs/plans/2026-03-12-math-lo-benchmark.md"),
            benchmark_ag=str(worktree_root / "docs/plans/2026-03-17-math-ag-benchmark.md"),
            output_dir=tmpdir
        )
        yield Path(tmpdir)


@pytest.fixture
def output_dir(fresh_export_dir: Path) -> Path:
    """Return the output directory for KG v1 (fresh export)."""
    return fresh_export_dir


@pytest.fixture
def kg_nodes_dir(output_dir: Path) -> Path:
    """Return the nodes directory."""
    return output_dir / "nodes"


@pytest.fixture
def kg_edges_dir(output_dir: Path) -> Path:
    """Return the edges directory."""
    return output_dir / "edges"


@pytest.fixture
def topics_jsonl(kg_nodes_dir: Path) -> Path:
    """Return the topics.jsonl file path."""
    return kg_nodes_dir / "topics.jsonl"


@pytest.fixture
def subcategories_jsonl(kg_nodes_dir: Path) -> Path:
    """Return the subcategories.jsonl file path."""
    return kg_nodes_dir / "subcategories.jsonl"


@pytest.fixture
def periods_jsonl(kg_nodes_dir: Path) -> Path:
    """Return the periods.jsonl file path."""
    return kg_nodes_dir / "periods.jsonl"


@pytest.fixture
def evolves_to_jsonl(kg_edges_dir: Path) -> Path:
    """Return the evolves_to.jsonl file path."""
    return kg_edges_dir / "evolves_to.jsonl"


@pytest.fixture
def metadata_json(output_dir: Path) -> Path:
    """Return the metadata.json file path."""
    return output_dir / "metadata.json"


@pytest.fixture
def validation_report_json(output_dir: Path) -> Path:
    """Return the validation_report.json file path."""
    return output_dir / "validation_report.json"


@pytest.fixture
def load_jsonl_file():
    """Helper to load a JSONL file."""
    def _load(path: Path) -> List[Dict[str, Any]]:
        if not path.exists():
            return []
        records = []
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
        return records
    return _load


@pytest.fixture
def load_json_file():
    """Helper to load a JSON file."""
    def _load(path: Path) -> Dict[str, Any]:
        if not path.exists():
            return {}
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return _load


# Test 1: Output Directory Structure

class TestOutputDirectoryStructure:
    """Verify all expected files exist in the output directory."""

    def test_nodes_directory_exists(self, kg_nodes_dir: Path):
        """nodes/ directory should exist."""
        assert kg_nodes_dir.exists(), f"nodes directory not found: {kg_nodes_dir}"
        assert kg_nodes_dir.is_dir()

    def test_edges_directory_exists(self, kg_edges_dir: Path):
        """edges/ directory should exist."""
        assert kg_edges_dir.exists(), f"edges directory not found: {kg_edges_dir}"
        assert kg_edges_dir.is_dir()

    def test_topics_jsonl_exists(self, topics_jsonl: Path):
        """nodes/topics.jsonl should exist."""
        assert topics_jsonl.exists(), f"topics.jsonl not found: {topics_jsonl}"

    def test_subcategories_jsonl_exists(self, subcategories_jsonl: Path):
        """nodes/subcategories.jsonl should exist."""
        assert subcategories_jsonl.exists(), f"subcategories.jsonl not found: {subcategories_jsonl}"

    def test_periods_jsonl_exists(self, periods_jsonl: Path):
        """nodes/periods.jsonl should exist."""
        assert periods_jsonl.exists(), f"periods.jsonl not found: {periods_jsonl}"

    def test_contains_topic_jsonl_exists(self, kg_edges_dir: Path):
        """edges/contains_topic.jsonl should exist."""
        path = kg_edges_dir / "contains_topic.jsonl"
        assert path.exists(), f"contains_topic.jsonl not found: {path}"

    def test_active_in_jsonl_exists(self, kg_edges_dir: Path):
        """edges/active_in.jsonl should exist."""
        path = kg_edges_dir / "active_in.jsonl"
        assert path.exists(), f"active_in.jsonl not found: {path}"

    def test_neighbor_of_jsonl_exists(self, kg_edges_dir: Path):
        """edges/neighbor_of.jsonl should exist."""
        path = kg_edges_dir / "neighbor_of.jsonl"
        assert path.exists(), f"neighbor_of.jsonl not found: {path}"

    def test_parent_of_jsonl_exists(self, kg_edges_dir: Path):
        """edges/parent_of.jsonl should exist."""
        path = kg_edges_dir / "parent_of.jsonl"
        assert path.exists(), f"parent_of.jsonl not found: {path}"

    def test_evolves_to_jsonl_exists(self, evolves_to_jsonl: Path):
        """edges/evolves_to.jsonl should exist."""
        assert evolves_to_jsonl.exists(), f"evolves_to.jsonl not found: {evolves_to_jsonl}"

    def test_metadata_json_exists(self, metadata_json: Path):
        """metadata.json should exist."""
        assert metadata_json.exists(), f"metadata.json not found: {metadata_json}"

    def test_validation_report_json_exists(self, validation_report_json: Path):
        """validation_report.json should exist."""
        assert validation_report_json.exists(), f"validation_report.json not found: {validation_report_json}"


# Test 2: Topics JSONL Format

class TestTopicsJsonlFormat:
    """Verify each topic node has required fields."""

    REQUIRED_FIELDS = {
        "id", "type", "name", "keywords",
        "category", "subcategory",
        "topic_mode", "total_papers", "active_periods",
        "history", "hierarchy_path", "hierarchy_depth"
    }

    def test_topics_not_empty(self, topics_jsonl: Path, load_jsonl_file):
        """topics.jsonl should contain records."""
        records = load_jsonl_file(topics_jsonl)
        assert len(records) > 0, "topics.jsonl is empty"

    def test_each_topic_has_required_fields(self, topics_jsonl: Path, load_jsonl_file):
        """Each topic should have all required fields."""
        records = load_jsonl_file(topics_jsonl)
        for record in records:
            missing = self.REQUIRED_FIELDS - set(record.keys())
            assert not missing, f"Topic {record.get('id', 'unknown')} missing fields: {missing}"

    def test_topic_id_format(self, topics_jsonl: Path, load_jsonl_file):
        """Topic IDs should be in global_XXX format."""
        records = load_jsonl_file(topics_jsonl)
        for record in records:
            topic_id = record.get("id", "")
            assert topic_id.startswith("global_"), f"Invalid topic ID format: {topic_id}"

    def test_topic_type_is_topic(self, topics_jsonl: Path, load_jsonl_file):
        """Topic type should be 'topic'."""
        records = load_jsonl_file(topics_jsonl)
        for record in records:
            assert record.get("type") == "topic", f"Invalid type for topic {record.get('id')}"

    def test_topic_keywords_is_list(self, topics_jsonl: Path, load_jsonl_file):
        """Keywords should be a list."""
        records = load_jsonl_file(topics_jsonl)
        for record in records:
            assert isinstance(record.get("keywords"), list), f"Keywords not a list for {record.get('id')}"

    def test_topic_active_periods_is_int(self, topics_jsonl: Path, load_jsonl_file):
        """Active periods should be an integer count."""
        records = load_jsonl_file(topics_jsonl)
        for record in records:
            assert isinstance(record.get("active_periods"), int), f"active_periods not an int for {record.get('id')}"

    def test_topic_hierarchy_path_is_list(self, topics_jsonl: Path, load_jsonl_file):
        """Hierarchy path should be a list."""
        records = load_jsonl_file(topics_jsonl)
        for record in records:
            assert isinstance(record.get("hierarchy_path"), list), f"hierarchy_path not a list for {record.get('id')}"

    def test_topic_total_papers_is_int(self, topics_jsonl: Path, load_jsonl_file):
        """Total papers should be an integer."""
        records = load_jsonl_file(topics_jsonl)
        for record in records:
            assert isinstance(record.get("total_papers"), int), f"total_papers not an int for {record.get('id')}"


# Test 3: Subcategories JSONL Format

class TestSubcategoriesJsonlFormat:
    """Verify subcategory nodes have required fields."""

    REQUIRED_FIELDS = {
        "code", "name", "discipline",
        "topic_count", "multi_period_count", "single_period_count",
        "eligible_anchor_count", "status", "evidence_quality"
    }

    def test_subcategories_not_empty(self, subcategories_jsonl: Path, load_jsonl_file):
        """subcategories.jsonl should contain records."""
        records = load_jsonl_file(subcategories_jsonl)
        assert len(records) > 0, "subcategories.jsonl is empty"

    def test_each_subcategory_has_required_fields(self, subcategories_jsonl: Path, load_jsonl_file):
        """Each subcategory should have all required fields."""
        records = load_jsonl_file(subcategories_jsonl)
        for record in records:
            missing = self.REQUIRED_FIELDS - set(record.keys())
            assert not missing, f"Subcategory {record.get('code', 'unknown')} missing fields: {missing}"

    def test_subcategory_code_format(self, subcategories_jsonl: Path, load_jsonl_file):
        """Subcategory codes should be math.XX format."""
        records = load_jsonl_file(subcategories_jsonl)
        for record in records:
            code = record.get("code", "")
            assert code.startswith("math."), f"Invalid subcategory code: {code}"

    def test_subcategory_counts_are_integers(self, subcategories_jsonl: Path, load_jsonl_file):
        """Count fields should be integers."""
        records = load_jsonl_file(subcategories_jsonl)
        int_fields = ["topic_count", "multi_period_count", "single_period_count", "eligible_anchor_count"]
        for record in records:
            for field in int_fields:
                assert isinstance(record.get(field), int), f"{field} not an int for {record.get('code')}"


# Test 4: Periods JSONL Format

class TestPeriodsJsonlFormat:
    """Verify period nodes have required fields."""

    REQUIRED_FIELDS = {"id", "start_date", "end_date"}

    def test_periods_not_empty(self, periods_jsonl: Path, load_jsonl_file):
        """periods.jsonl should contain records."""
        records = load_jsonl_file(periods_jsonl)
        assert len(records) > 0, "periods.jsonl is empty"

    def test_each_period_has_required_fields(self, periods_jsonl: Path, load_jsonl_file):
        """Each period should have all required fields."""
        records = load_jsonl_file(periods_jsonl)
        for record in records:
            missing = self.REQUIRED_FIELDS - set(record.keys())
            assert not missing, f"Period {record.get('id', 'unknown')} missing fields: {missing}"

    def test_period_id_format(self, periods_jsonl: Path, load_jsonl_file):
        """Period IDs should be YYYY-MM format."""
        records = load_jsonl_file(periods_jsonl)
        for record in records:
            period_id = record.get("id", "")
            parts = period_id.split("-")
            assert len(parts) == 2, f"Invalid period ID format: {period_id}"
            assert parts[0].isdigit() and len(parts[0]) == 4, f"Invalid year in period ID: {period_id}"
            assert parts[1].isdigit() and len(parts[1]) == 2, f"Invalid month in period ID: {period_id}"


# Test 5: Edges JSONL Format

class TestEdgesJsonlFormat:
    """Verify all edges have required fields."""

    REQUIRED_FIELDS = {"source", "target", "type"}

    def test_contains_topic_edges_format(self, kg_edges_dir: Path, load_jsonl_file):
        """contains_topic edges should have required fields."""
        path = kg_edges_dir / "contains_topic.jsonl"
        records = load_jsonl_file(path)
        for record in records:
            missing = self.REQUIRED_FIELDS - set(record.keys())
            assert not missing, f"Edge missing fields: {missing}"
            assert record.get("type") == "CONTAINS_TOPIC"

    def test_active_in_edges_format(self, kg_edges_dir: Path, load_jsonl_file):
        """active_in edges should have required fields."""
        path = kg_edges_dir / "active_in.jsonl"
        records = load_jsonl_file(path)
        for record in records:
            missing = self.REQUIRED_FIELDS - set(record.keys())
            assert not missing, f"Edge missing fields: {missing}"
            assert record.get("type") == "ACTIVE_IN"

    def test_neighbor_of_edges_format(self, kg_edges_dir: Path, load_jsonl_file):
        """neighbor_of edges should have required fields."""
        path = kg_edges_dir / "neighbor_of.jsonl"
        records = load_jsonl_file(path)
        for record in records:
            missing = self.REQUIRED_FIELDS - set(record.keys())
            assert not missing, f"Edge missing fields: {missing}"
            assert record.get("type") == "NEIGHBOR_OF"

    def test_parent_of_edges_format(self, kg_edges_dir: Path, load_jsonl_file):
        """parent_of edges should have required fields."""
        path = kg_edges_dir / "parent_of.jsonl"
        records = load_jsonl_file(path)
        for record in records:
            missing = self.REQUIRED_FIELDS - set(record.keys())
            assert not missing, f"Edge missing fields: {missing}"
            assert record.get("type") == "PARENT_OF"


# Test 6: Evolve To Benchmark Annotations (CRITICAL)

class TestEvolveToBenchmarkAnnotations:
    """Verify evolves_to.jsonl edges have benchmark annotations."""

    REQUIRED_BENCHMARK_FIELDS = {
        "source", "target", "type",
        "evidence_type", "confidence", "benchmark_case_id",
        "benchmark_status", "expected_relation", "subcategory"
    }

    def test_evolves_to_edges_have_required_fields(self, evolves_to_jsonl: Path, load_jsonl_file):
        """Each evolves_to edge should have all benchmark annotation fields."""
        records = load_jsonl_file(evolves_to_jsonl)
        for record in records:
            missing = self.REQUIRED_BENCHMARK_FIELDS - set(record.keys())
            assert not missing, f"Edge {record.get('source')}->{record.get('target')} missing fields: {missing}"

    def test_evolves_to_type_is_correct(self, evolves_to_jsonl: Path, load_jsonl_file):
        """Edge type should be 'EVOLVES_TO'."""
        records = load_jsonl_file(evolves_to_jsonl)
        for record in records:
            assert record.get("type") == "EVOLVES_TO"

    def test_evidence_type_is_benchmark_confirmed(self, evolves_to_jsonl: Path, load_jsonl_file):
        """Evidence type should be 'benchmark-confirmed'."""
        records = load_jsonl_file(evolves_to_jsonl)
        for record in records:
            assert record.get("evidence_type") == "benchmark-confirmed", \
                f"Invalid evidence_type: {record.get('evidence_type')}"

    def test_confidence_values_are_valid(self, evolves_to_jsonl: Path, load_jsonl_file):
        """Confidence should be 'confirmed', 'negative', or 'ambiguous'."""
        valid_confidences = {"confirmed", "negative", "ambiguous"}
        records = load_jsonl_file(evolves_to_jsonl)
        for record in records:
            confidence = record.get("confidence")
            assert confidence in valid_confidences, f"Invalid confidence: {confidence}"

    def test_benchmark_status_values_are_valid(self, evolves_to_jsonl: Path, load_jsonl_file):
        """Benchmark status should be 'positive', 'negative', or 'ambiguous'."""
        valid_statuses = {"positive", "negative", "ambiguous"}
        records = load_jsonl_file(evolves_to_jsonl)
        for record in records:
            status = record.get("benchmark_status")
            assert status in valid_statuses, f"Invalid benchmark_status: {status}"

    def test_benchmark_case_id_format(self, evolves_to_jsonl: Path, load_jsonl_file):
        """Benchmark case IDs should follow lo-bX, lo-nX, lo-aX, ag-bX, ag-nX, ag-method-nX pattern."""
        records = load_jsonl_file(evolves_to_jsonl)
        for record in records:
            case_id = record.get("benchmark_case_id", "")
            assert case_id.startswith(("lo-", "ag-")), f"Invalid case_id prefix: {case_id}"
            # Allow patterns like: lo-b1, lo-n1, lo-a1, ag-b1, ag-n1, ag-method-n1
            valid_prefixes = ("lo-b", "lo-n", "lo-a", "ag-b", "ag-n", "ag-e", "ag-method-")
            assert any(case_id.startswith(p) for p in valid_prefixes), f"Invalid case_id format: {case_id}"

    def test_subcategory_is_math_lo_or_ag(self, evolves_to_jsonl: Path, load_jsonl_file):
        """Subcategory should be math.LO or math.AG."""
        valid_subcategories = {"math.LO", "math.AG"}
        records = load_jsonl_file(evolves_to_jsonl)
        for record in records:
            subcategory = record.get("subcategory")
            assert subcategory in valid_subcategories, f"Invalid subcategory: {subcategory}"

    def test_lo_edge_counts_match_benchmark(self, evolves_to_jsonl: Path, load_jsonl_file):
        """
        LO edges count verification (after KG-02-fix):
        - 2 positive + 1 negative + 1 ambiguous = 4 edges
        Note: Only 4 of 13 benchmark cases have both topics in LO hierarchy topic_assignments
        """
        records = load_jsonl_file(evolves_to_jsonl)
        lo_records = [r for r in records if r.get("subcategory") == "math.LO"]

        positive = len([r for r in lo_records if r.get("benchmark_status") == "positive"])
        negative = len([r for r in lo_records if r.get("benchmark_status") == "negative"])
        ambiguous = len([r for r in lo_records if r.get("benchmark_status") == "ambiguous"])

        assert positive == 2, f"Expected 2 LO positive edges, got {positive}"
        assert negative == 1, f"Expected 1 LO negative edges, got {negative}"
        assert ambiguous == 1, f"Expected 1 LO ambiguous edges, got {ambiguous}"
        assert len(lo_records) == 4, f"Expected 4 total LO edges, got {len(lo_records)}"

    def test_ag_edge_counts_match_benchmark(self, evolves_to_jsonl: Path, load_jsonl_file):
        """
        AG edges count verification:
        - 2 positive + 3 negative = 5 edges
        """
        records = load_jsonl_file(evolves_to_jsonl)
        ag_records = [r for r in records if r.get("subcategory") == "math.AG"]

        positive = len([r for r in ag_records if r.get("benchmark_status") == "positive"])
        negative = len([r for r in ag_records if r.get("benchmark_status") == "negative"])
        ambiguous = len([r for r in ag_records if r.get("benchmark_status") == "ambiguous"])

        assert positive == 2, f"Expected 2 AG positive edges, got {positive}"
        assert negative == 3, f"Expected 3 AG negative edges, got {negative}"
        assert ambiguous == 0, f"Expected 0 AG ambiguous edges, got {ambiguous}"
        assert len(ag_records) == 5, f"Expected 5 total AG edges, got {len(ag_records)}"

    def test_total_evolve_to_edge_count(self, evolves_to_jsonl: Path, load_jsonl_file):
        """
        Total evolves_to edges (after KG-02-fix):
        - LO: 4 + AG: 5 = 9 edges
        Note: Only 9 of 18 benchmark cases have both topics in hierarchy topic_assignments
        """
        records = load_jsonl_file(evolves_to_jsonl)
        assert len(records) == 9, f"Expected 9 total evolves_to edges, got {len(records)}"


# Test 7: PR Exclusion (CRITICAL)

class TestPRExclusion:
    """Verify math.PR topics are NOT in output."""

    def test_no_pr_topics_in_topics_jsonl(self, topics_jsonl: Path, load_jsonl_file):
        """No PR topics should be in topics.jsonl."""
        records = load_jsonl_file(topics_jsonl)
        pr_topics = [r for r in records if r.get("subcategory") == "math.PR"]
        assert len(pr_topics) == 0, f"Found {len(pr_topics)} PR topics in topics.jsonl"

    def test_no_pr_in_subcategories_jsonl(self, subcategories_jsonl: Path, load_jsonl_file):
        """math.PR should not be in subcategories.jsonl."""
        records = load_jsonl_file(subcategories_jsonl)
        pr_subcats = [r for r in records if r.get("code") == "math.PR"]
        assert len(pr_subcats) == 0, "Found math.PR in subcategories.jsonl"

    def test_no_edges_involving_pr_topics(self, kg_edges_dir: Path, load_jsonl_file):
        """No edges should involve PR topics."""
        edge_files = [
            "contains_topic.jsonl",
            "active_in.jsonl",
            "neighbor_of.jsonl",
            "parent_of.jsonl",
            "evolves_to.jsonl"
        ]

        # Load all topics to check which are PR
        topics_path = kg_edges_dir.parent / "nodes" / "topics.jsonl"
        if topics_path.exists():
            topics = load_jsonl_file(topics_path)
            pr_topic_ids = {r.get("id") for r in topics if r.get("subcategory") == "math.PR"}
        else:
            pr_topic_ids = set()

        for edge_file in edge_files:
            path = kg_edges_dir / edge_file
            if not path.exists():
                continue
            records = load_jsonl_file(path)
            for record in records:
                source = record.get("source", "")
                target = record.get("target", "")
                assert source not in pr_topic_ids, f"Edge involves PR topic {source}"
                assert target not in pr_topic_ids, f"Edge involves PR topic {target}"


# Test 8: Metadata Completeness

class TestMetadataCompleteness:
    """Verify metadata.json has all required fields."""

    REQUIRED_FIELDS = {
        "version", "generated_at", "scope",
        "topic_count", "edge_counts", "benchmark_case_counts"
    }

    def test_metadata_has_required_fields(self, metadata_json: Path, load_json_file):
        """metadata.json should have all required fields."""
        data = load_json_file(metadata_json)
        missing = self.REQUIRED_FIELDS - set(data.keys())
        assert not missing, f"metadata.json missing fields: {missing}"

    def test_version_is_string(self, metadata_json: Path, load_json_file):
        """Version should be a string."""
        data = load_json_file(metadata_json)
        assert isinstance(data.get("version"), str)

    def test_generated_at_is_string(self, metadata_json: Path, load_json_file):
        """Generated_at should be a string (ISO timestamp)."""
        data = load_json_file(metadata_json)
        assert isinstance(data.get("generated_at"), str)

    def test_scope_has_included_and_excluded(self, metadata_json: Path, load_json_file):
        """Scope should have included_subcategories and excluded_subcategories."""
        data = load_json_file(metadata_json)
        scope = data.get("scope", {})
        assert "included_subcategories" in scope
        assert "excluded_subcategories" in scope

    def test_scope_includes_lo_and_ag(self, metadata_json: Path, load_json_file):
        """Scope should include math.LO and math.AG."""
        data = load_json_file(metadata_json)
        scope = data.get("scope", {})
        included = scope.get("included_subcategories", [])
        assert "math.LO" in included
        assert "math.AG" in included

    def test_scope_excludes_pr(self, metadata_json: Path, load_json_file):
        """Scope should explicitly exclude math.PR."""
        data = load_json_file(metadata_json)
        scope = data.get("scope", {})
        excluded = scope.get("excluded_subcategories", [])
        assert "math.PR" in excluded

    def test_topic_count_is_int(self, metadata_json: Path, load_json_file):
        """Topic count should be an integer."""
        data = load_json_file(metadata_json)
        assert isinstance(data.get("topic_count"), int)
        assert data.get("topic_count") > 0

    def test_edge_counts_is_dict(self, metadata_json: Path, load_json_file):
        """Edge counts should be a dictionary."""
        data = load_json_file(metadata_json)
        edge_counts = data.get("edge_counts")
        assert isinstance(edge_counts, dict)

    def test_edge_counts_has_expected_types(self, metadata_json: Path, load_json_file):
        """Edge counts should have entries for all edge types."""
        data = load_json_file(metadata_json)
        edge_counts = data.get("edge_counts", {})
        expected_types = ["contains_topic", "active_in", "neighbor_of", "parent_of", "evolves_to"]
        for edge_type in expected_types:
            assert edge_type in edge_counts, f"Missing edge count for {edge_type}"

    def test_benchmark_case_counts_is_dict(self, metadata_json: Path, load_json_file):
        """Benchmark case counts should be a dictionary."""
        data = load_json_file(metadata_json)
        counts = data.get("benchmark_case_counts")
        assert isinstance(counts, dict)

    def test_benchmark_case_counts_has_lo_and_ag(self, metadata_json: Path, load_json_file):
        """Benchmark case counts should have math.LO and math.AG."""
        data = load_json_file(metadata_json)
        counts = data.get("benchmark_case_counts", {})
        assert "math.LO" in counts
        assert "math.AG" in counts


# Test 9: Validation Report

class TestValidationReport:
    """Verify validation_report.json has required structure."""

    REQUIRED_FIELDS = {
        "schema_errors", "missing_files",
        "node_count_check", "edge_count_check", "benchmark_alignment_check",
        "status"
    }

    def test_validation_report_has_required_fields(self, validation_report_json: Path, load_json_file):
        """validation_report.json should have all required fields."""
        data = load_json_file(validation_report_json)
        missing = self.REQUIRED_FIELDS - set(data.keys())
        assert not missing, f"validation_report.json missing fields: {missing}"

    def test_schema_errors_is_array(self, validation_report_json: Path, load_json_file):
        """Schema errors should be an array."""
        data = load_json_file(validation_report_json)
        assert isinstance(data.get("schema_errors"), list)

    def test_schema_errors_is_empty(self, validation_report_json: Path, load_json_file):
        """Schema errors should be empty (valid output)."""
        data = load_json_file(validation_report_json)
        assert len(data.get("schema_errors", [])) == 0, "Schema errors found in validation report"

    def test_missing_files_is_array(self, validation_report_json: Path, load_json_file):
        """Missing files should be an array."""
        data = load_json_file(validation_report_json)
        assert isinstance(data.get("missing_files"), list)

    def test_missing_files_is_empty(self, validation_report_json: Path, load_json_file):
        """Missing files should be empty."""
        data = load_json_file(validation_report_json)
        assert len(data.get("missing_files", [])) == 0, "Missing files found in validation report"

    def test_node_count_check_is_pass_or_fail(self, validation_report_json: Path, load_json_file):
        """Node count check should be 'pass' or 'fail'."""
        data = load_json_file(validation_report_json)
        check = data.get("node_count_check")
        assert check in {"pass", "fail"}, f"Invalid node_count_check: {check}"

    def test_edge_count_check_is_pass_or_fail(self, validation_report_json: Path, load_json_file):
        """Edge count check should be 'pass' or 'fail'."""
        data = load_json_file(validation_report_json)
        check = data.get("edge_count_check")
        assert check in {"pass", "fail"}, f"Invalid edge_count_check: {check}"

    def test_benchmark_alignment_check_is_pass_or_fail(self, validation_report_json: Path, load_json_file):
        """Benchmark alignment check should be 'pass' or 'fail'."""
        data = load_json_file(validation_report_json)
        check = data.get("benchmark_alignment_check")
        assert check in {"pass", "fail"}, f"Invalid benchmark_alignment_check: {check}"

    def test_status_is_valid_or_invalid(self, validation_report_json: Path, load_json_file):
        """Status should be 'valid' or 'invalid'."""
        data = load_json_file(validation_report_json)
        status = data.get("status")
        assert status in {"valid", "invalid"}, f"Invalid status: {status}"

    def test_overall_status_is_valid(self, validation_report_json: Path, load_json_file):
        """Overall status should be 'valid' for successful export."""
        data = load_json_file(validation_report_json)
        assert data.get("status") == "valid", "Validation report shows invalid status"


# Additional Integration Tests

class TestIntegration:
    """Integration tests for KG export consistency."""

    def test_topic_ids_consistent_across_files(self, output_dir: Path, load_jsonl_file):
        """Topic IDs should be consistent between topics.jsonl and edges."""
        topics_path = output_dir / "nodes" / "topics.jsonl"
        topics = load_jsonl_file(topics_path)
        topic_ids = {r.get("id") for r in topics}

        # Check evolves_to edges reference valid topics
        evolves_path = output_dir / "edges" / "evolves_to.jsonl"
        if evolves_path.exists():
            edges = load_jsonl_file(evolves_path)
            for edge in edges:
                assert edge.get("source") in topic_ids, f"Edge references unknown source: {edge.get('source')}"
                assert edge.get("target") in topic_ids, f"Edge references unknown target: {edge.get('target')}"

    def test_subcategory_counts_match_topics(self, output_dir: Path, load_jsonl_file):
        """Subcategory topic counts should match actual topics."""
        topics_path = output_dir / "nodes" / "topics.jsonl"
        subcats_path = output_dir / "nodes" / "subcategories.jsonl"

        topics = load_jsonl_file(topics_path)
        subcats = load_jsonl_file(subcats_path)

        # Count topics per subcategory
        actual_counts = {}
        for topic in topics:
            subcat = topic.get("subcategory")
            actual_counts[subcat] = actual_counts.get(subcat, 0) + 1

        # Verify against subcategory records
        # Map short codes to full codes (e.g., "LO" -> "math.LO")
        code_mapping = {code.replace("math.", ""): code for code in actual_counts.keys()}
        for subcat in subcats:
            code = subcat.get("code")  # e.g., "math.LO"
            short_code = code.replace("math.", "")  # e.g., "LO"
            expected_count = subcat.get("topic_count", 0)
            actual_count = actual_counts.get(short_code, 0)
            assert actual_count == expected_count, \
                f"Subcategory {code}: count mismatch (expected {expected_count}, found {actual_count})"

    def test_all_lo_ag_topics_included(self, output_dir: Path, load_jsonl_file):
        """All LO and AG topics from hierarchy should be in output."""
        # This test verifies that the exporter includes all relevant topics
        topics_path = output_dir / "nodes" / "topics.jsonl"
        topics = load_jsonl_file(topics_path)

        lo_topics = [r for r in topics if r.get("subcategory") in ("LO", "math.LO")]
        ag_topics = [r for r in topics if r.get("subcategory") in ("AG", "math.AG")]

        # Based on the hierarchy data, we expect 15 LO topics and 17 AG topics
        # Note: These numbers may need adjustment based on filtering criteria
        assert len(lo_topics) > 0, "No LO topics found in output"
        assert len(ag_topics) > 0, "No AG topics found in output"

    def test_period_ids_consistent(self, output_dir: Path, load_jsonl_file):
        """Period IDs in topics should match periods.jsonl."""
        periods_path = output_dir / "nodes" / "periods.jsonl"
        topics_path = output_dir / "nodes" / "topics.jsonl"

        periods = load_jsonl_file(periods_path)
        topics = load_jsonl_file(topics_path)

        valid_period_ids = {r.get("id") for r in periods}

        for topic in topics:
            # Check history field for period references
            history = topic.get("history", [])
            for h in history:
                period_id = h.get("period")
                if period_id:
                    assert period_id in valid_period_ids, \
                        f"Topic {topic.get('id')} references unknown period: {period_id}"


# Test 10: Key Assertions (CRITICAL)

class TestKeyAssertions:
    """Critical assertions for KG export validation."""

    def test_lo_topic_count_is_15(self, topics_jsonl: Path, load_jsonl_file):
        """LO topic count should be exactly 15."""
        records = load_jsonl_file(topics_jsonl)
        lo_topics = [r for r in records if r.get("subcategory") in ("LO", "math.LO")]
        assert len(lo_topics) == 15, f"Expected 15 LO topics, got {len(lo_topics)}"

    def test_ag_topic_count_is_17(self, topics_jsonl: Path, load_jsonl_file):
        """AG topic count should be exactly 17."""
        records = load_jsonl_file(topics_jsonl)
        ag_topics = [r for r in records if r.get("subcategory") in ("AG", "math.AG")]
        assert len(ag_topics) == 17, f"Expected 17 AG topics, got {len(ag_topics)}"

    def test_neighbor_of_count_less_than_241(self, kg_edges_dir: Path, load_jsonl_file):
        """neighbor_of count should be less than 241 (verifies not a clique)."""
        path = kg_edges_dir / "neighbor_of.jsonl"
        records = load_jsonl_file(path)
        assert len(records) < 241, f"neighbor_of count {len(records)} >= 241, graph may be a clique"

    def test_benchmark_edges_count_is_9(self, evolves_to_jsonl: Path, load_jsonl_file):
        """Benchmark edges (evolves_to) count should be exactly 9 (after KG-02-fix)."""
        records = load_jsonl_file(evolves_to_jsonl)
        assert len(records) == 9, f"Expected 9 benchmark edges, got {len(records)}"

    def test_pr_exclusion_verified(self, topics_jsonl: Path, subcategories_jsonl: Path, kg_edges_dir: Path, load_jsonl_file):
        """PR exclusion verified - no PR topics anywhere in output."""
        # Check topics
        topics = load_jsonl_file(topics_jsonl)
        pr_topics = [r for r in topics if r.get("subcategory") == "math.PR"]
        assert len(pr_topics) == 0, f"Found {len(pr_topics)} PR topics in topics.jsonl"

        # Check subcategories
        subcats = load_jsonl_file(subcategories_jsonl)
        pr_subcats = [r for r in subcats if r.get("code") == "math.PR"]
        assert len(pr_subcats) == 0, f"Found {len(pr_subcats)} PR subcategories in subcategories.jsonl"

        # Check edges
        edge_files = ["contains_topic.jsonl", "active_in.jsonl", "neighbor_of.jsonl", "parent_of.jsonl", "evolves_to.jsonl"]
        pr_topic_ids = {r.get("id") for r in topics if r.get("subcategory") == "math.PR"}
        for edge_file in edge_files:
            path = kg_edges_dir / edge_file
            if path.exists():
                edges = load_jsonl_file(path)
                for edge in edges:
                    assert edge.get("source") not in pr_topic_ids, f"Edge in {edge_file} involves PR topic {edge.get('source')}"
                    assert edge.get("target") not in pr_topic_ids, f"Edge in {edge_file} involves PR topic {edge.get('target')}"


# Test 11: Conditional PR Export

class TestConditionalPRExport:
    """Verify conditional PR export path: separate dir, PR included, baseline unaffected."""

    @pytest.fixture
    def fresh_pr_conditional_export(self) -> Path:
        """Create temp dir, run conditional exporter with --benchmark-pr, return path."""
        worktree_root = Path("/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor")
        pr_curation_doc = str(worktree_root / "docs/plans/2026-03-21-math-pr-case-curation.md")
        with tempfile.TemporaryDirectory() as tmpdir:
            export_kg_v1(
                input_file=str(worktree_root / "data/output/aligned_topics_hierarchy.json"),
                benchmark_lo=str(worktree_root / "docs/plans/2026-03-12-math-lo-benchmark.md"),
                benchmark_ag=str(worktree_root / "docs/plans/2026-03-17-math-ag-benchmark.md"),
                output_dir=tmpdir,
                benchmark_pr=pr_curation_doc,
            )
            yield Path(tmpdir)

    def _load_jsonl(self, path: Path):
        if not path.exists():
            return []
        records = []
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
        return records

    def _load_json(self, path: Path):
        if not path.exists():
            return {}
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def test_conditional_export_dir_structure(self, fresh_pr_conditional_export: Path):
        """Conditional export should produce same directory structure as baseline."""
        assert (fresh_pr_conditional_export / 'nodes' / 'topics.jsonl').exists()
        assert (fresh_pr_conditional_export / 'nodes' / 'subcategories.jsonl').exists()
        assert (fresh_pr_conditional_export / 'edges' / 'evolves_to.jsonl').exists()
        assert (fresh_pr_conditional_export / 'metadata.json').exists()
        assert (fresh_pr_conditional_export / 'validation_report.json').exists()

    def test_conditional_export_has_pr_subcategory(self, fresh_pr_conditional_export: Path):
        """Conditional export should include math.PR subcategory."""
        records = self._load_jsonl(fresh_pr_conditional_export / 'nodes' / 'subcategories.jsonl')
        codes = [r.get('code') for r in records]
        assert 'math.PR' in codes, f"math.PR not found in subcategories, got: {codes}"

    def test_conditional_export_has_lo_ag_subcategories(self, fresh_pr_conditional_export: Path):
        """Conditional export should still include LO and AG subcategories."""
        records = self._load_jsonl(fresh_pr_conditional_export / 'nodes' / 'subcategories.jsonl')
        codes = [r.get('code') for r in records]
        assert 'math.LO' in codes, "math.LO missing from conditional export"
        assert 'math.AG' in codes, "math.AG missing from conditional export"

    def test_conditional_export_has_pr_topics(self, fresh_pr_conditional_export: Path):
        """Conditional export should include PR topics."""
        records = self._load_jsonl(fresh_pr_conditional_export / 'nodes' / 'topics.jsonl')
        pr_topics = [r for r in records if r.get('subcategory') == 'PR']
        assert len(pr_topics) > 0, "No PR topics found in conditional export"

    def test_conditional_export_lo_ag_count_unchanged(self, fresh_pr_conditional_export: Path):
        """LO and AG topic counts should be unchanged in conditional export."""
        records = self._load_jsonl(fresh_pr_conditional_export / 'nodes' / 'topics.jsonl')
        lo_count = len([r for r in records if r.get('subcategory') in ('LO', 'math.LO')])
        ag_count = len([r for r in records if r.get('subcategory') in ('AG', 'math.AG')])
        assert lo_count == 15, f"Expected 15 LO topics in conditional export, got {lo_count}"
        assert ag_count == 17, f"Expected 17 AG topics in conditional export, got {ag_count}"

    def test_pr_evolves_to_edges_have_provisional_evidence(self, fresh_pr_conditional_export: Path):
        """PR conditional EVOLVES_TO edges should have evidence_type='provisional'."""
        records = self._load_jsonl(fresh_pr_conditional_export / 'edges' / 'evolves_to.jsonl')
        pr_edges = [r for r in records if r.get('subcategory') == 'math.PR']
        assert len(pr_edges) > 0, "No PR edges found in conditional export"
        for edge in pr_edges:
            assert edge.get('evidence_type') == 'provisional', \
                f"PR edge evidence_type should be 'provisional', got: {edge.get('evidence_type')}"

    def test_pr_evolves_to_edges_have_inferred_confidence(self, fresh_pr_conditional_export: Path):
        """PR conditional EVOLVES_TO edges should have confidence='inferred'."""
        records = self._load_jsonl(fresh_pr_conditional_export / 'edges' / 'evolves_to.jsonl')
        pr_edges = [r for r in records if r.get('subcategory') == 'math.PR']
        for edge in pr_edges:
            assert edge.get('confidence') == 'inferred', \
                f"PR edge confidence should be 'inferred', got: {edge.get('confidence')}"

    def test_pr_edges_have_conditional_metadata(self, fresh_pr_conditional_export: Path):
        """PR conditional edges should carry integration_scope=conditional."""
        records = self._load_jsonl(fresh_pr_conditional_export / 'edges' / 'evolves_to.jsonl')
        pr_edges = [r for r in records if r.get('subcategory') == 'math.PR']
        for edge in pr_edges:
            assert edge.get('integration_scope') == 'conditional', \
                f"PR edge integration_scope should be 'conditional', got: {edge.get('integration_scope')}"
            assert edge.get('human_review_required') is True, \
                f"PR edge human_review_required should be True"
            assert edge.get('curation_tier') in ('A', 'B'), \
                f"PR edge curation_tier should be A or B, got: {edge.get('curation_tier')}"

    def test_lo_ag_edges_unchanged_in_conditional(self, fresh_pr_conditional_export: Path):
        """LO and AG EVOLVES_TO edges should have same structure as baseline."""
        records = self._load_jsonl(fresh_pr_conditional_export / 'edges' / 'evolves_to.jsonl')
        lo_ag_edges = [r for r in records if r.get('subcategory') in ('math.LO', 'math.AG')]
        assert len(lo_ag_edges) == 9, f"Expected 9 LO+AG edges in conditional export, got {len(lo_ag_edges)}"
        for edge in lo_ag_edges:
            assert edge.get('evidence_type') == 'benchmark-confirmed', \
                f"LO/AG edge evidence_type should be 'benchmark-confirmed'"

    def test_conditional_metadata_version(self, fresh_pr_conditional_export: Path):
        """Conditional export metadata should have version=kg_v1_pr_conditional."""
        data = self._load_json(fresh_pr_conditional_export / 'metadata.json')
        assert data.get('version') == 'kg_v1_pr_conditional', \
            f"Expected version 'kg_v1_pr_conditional', got: {data.get('version')}"

    def test_conditional_metadata_scope_includes_pr(self, fresh_pr_conditional_export: Path):
        """Conditional export scope should include math.PR."""
        data = self._load_json(fresh_pr_conditional_export / 'metadata.json')
        scope = data.get('scope', {})
        included = scope.get('included_subcategories', [])
        excluded = scope.get('excluded_subcategories', [])
        assert 'math.PR' in included, f"math.PR should be in included_subcategories"
        assert 'math.PR' not in excluded, f"math.PR should not be in excluded_subcategories"

    def test_baseline_still_excludes_pr(self, fresh_export_dir: Path, load_jsonl_file):
        """Baseline export (no --benchmark-pr) should still exclude PR. Uses existing fixture."""
        records = load_jsonl_file(fresh_export_dir / 'nodes' / 'topics.jsonl')
        pr_topics = [r for r in records if r.get('subcategory') == 'PR']
        assert len(pr_topics) == 0, f"Baseline has {len(pr_topics)} PR topics - baseline was contaminated!"

    def test_validation_report_valid_for_conditional(self, fresh_pr_conditional_export: Path):
        """Conditional export validation report should show valid status."""
        data = self._load_json(fresh_pr_conditional_export / 'validation_report.json')
        assert data.get('status') == 'valid', \
            f"Conditional validation report shows: {data.get('status')}, errors: {data.get('schema_errors')}"
