"""
Tests for Math Knowledge Graph v1 Visualization Export.

These tests verify that visualization bundles can be generated from KG v1 data,
with proper subgraph structure for LO and AG, PR exclusion, and frontend-readable
evidence labels.
"""
import json
import pytest
import tempfile
import sys
from pathlib import Path
from typing import Dict, List, Any, Set

# Add project root to path
sys.path.insert(0, "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor")

from pipeline.math_kg_export import (
    load_hierarchy_data,
    parse_benchmark_docs,
    export_kg_v1,
)
from pipeline.math_kg_visualization_export import (
    build_graph_bundle,
    build_subgraph,
    build_timeline_summary,
    build_legend,
)


# Fixtures

@pytest.fixture
def worktree_root() -> Path:
    """Return the worktree root path."""
    return Path("/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor")


@pytest.fixture
def fresh_kg_export(worktree_root: Path) -> Path:
    """Create a fresh KG v1 export in a temp directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        export_kg_v1(
            input_file=str(worktree_root / "data/output/aligned_topics_hierarchy.json"),
            benchmark_lo=str(worktree_root / "docs/plans/2026-03-12-math-lo-benchmark.md"),
            benchmark_ag=str(worktree_root / "docs/plans/2026-03-18-math-ag-benchmark.md"),
            output_dir=tmpdir
        )
        yield Path(tmpdir)


@pytest.fixture
def kg_nodes(fresh_kg_export: Path) -> Path:
    """Return the nodes directory path."""
    return fresh_kg_export / "nodes"


@pytest.fixture
def kg_edges(fresh_kg_export: Path) -> Path:
    """Return the edges directory path."""
    return fresh_kg_export / "edges"


@pytest.fixture
def load_jsonl():
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
def load_json():
    """Helper to load a JSON file."""
    def _load(path: Path) -> Dict[str, Any]:
        if not path.exists():
            return {}
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return _load


@pytest.fixture
def fresh_visualization_export(fresh_kg_export: Path) -> Path:
    """Generate visualization bundle from KG v1 export using actual exporter."""
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as tmpdir:
        # Call the actual exporter functions
        bundle = build_graph_bundle(str(fresh_kg_export))
        subgraph_lo = build_subgraph(bundle, 'LO')
        subgraph_ag = build_subgraph(bundle, 'AG')
        timeline = build_timeline_summary(bundle)
        legend = build_legend()

        # Write output files
        output_path = Path(tmpdir)
        with open(output_path / 'graph_bundle.json', 'w', encoding='utf-8') as f:
            json.dump(bundle, f, indent=2, ensure_ascii=False)
        with open(output_path / 'subgraph_lo.json', 'w', encoding='utf-8') as f:
            json.dump(subgraph_lo, f, indent=2, ensure_ascii=False)
        with open(output_path / 'subgraph_ag.json', 'w', encoding='utf-8') as f:
            json.dump(subgraph_ag, f, indent=2, ensure_ascii=False)
        with open(output_path / 'timeline_summary.json', 'w', encoding='utf-8') as f:
            json.dump(timeline, f, indent=2, ensure_ascii=False)
        with open(output_path / 'legend.json', 'w', encoding='utf-8') as f:
            json.dump(legend, f, indent=2, ensure_ascii=False)
        for domain_code, narrative_subgraph in bundle.get('narrative_subgraphs', {}).items():
            short_code = domain_code.split('.')[-1].lower()
            with open(output_path / f'subgraph_{short_code}.json', 'w', encoding='utf-8') as f:
                json.dump(narrative_subgraph, f, indent=2, ensure_ascii=False)

        yield output_path


@pytest.fixture
def visualization_bundle(fresh_kg_export: Path, load_jsonl) -> Dict[str, Any]:
    """
    Generate a visualization bundle from KG v1 export.

    Bundle structure:
    - nodes: all topics with their properties
    - edges: all edge types organized by type
    - subgraphs: LO and AG subgraphs with filtered nodes/edges
    - metadata: bundle metadata
    """
    nodes_dir = fresh_kg_export / "nodes"
    edges_dir = fresh_kg_export / "edges"

    # Load all nodes
    topics = load_jsonl(nodes_dir / "topics.jsonl")
    subcategories = load_jsonl(nodes_dir / "subcategories.jsonl")
    periods = load_jsonl(nodes_dir / "periods.jsonl")

    # Load all edges
    contains_topic = load_jsonl(edges_dir / "contains_topic.jsonl")
    active_in = load_jsonl(edges_dir / "active_in.jsonl")
    parent_of = load_jsonl(edges_dir / "parent_of.jsonl")
    neighbor_of = load_jsonl(edges_dir / "neighbor_of.jsonl")
    evolves_to = load_jsonl(edges_dir / "evolves_to.jsonl")

    # Build topic lookup
    topic_by_id = {t["id"]: t for t in topics}

    # Build subgraphs for LO and AG
    lo_topic_ids = {t["id"] for t in topics if t.get("subcategory") == "LO"}
    ag_topic_ids = {t["id"] for t in topics if t.get("subcategory") == "AG"}

    lo_subgraph = {
        "nodes": [t for t in topics if t["id"] in lo_topic_ids],
        "edges": {
            "evolves_to": [e for e in evolves_to
                          if e.get("source") in lo_topic_ids or e.get("target") in lo_topic_ids],
            "neighbor_of": [e for e in neighbor_of
                           if e.get("source") in lo_topic_ids and e.get("target") in lo_topic_ids],
            "parent_of": [e for e in parent_of
                         if e.get("source") in lo_topic_ids or e.get("target") in lo_topic_ids],
            "active_in": [e for e in active_in
                         if e.get("source") in lo_topic_ids],
        }
    }

    ag_subgraph = {
        "nodes": [t for t in topics if t["id"] in ag_topic_ids],
        "edges": {
            "evolves_to": [e for e in evolves_to
                          if e.get("source") in ag_topic_ids or e.get("target") in ag_topic_ids],
            "neighbor_of": [e for e in neighbor_of
                           if e.get("source") in ag_topic_ids and e.get("target") in ag_topic_ids],
            "parent_of": [e for e in parent_of
                         if e.get("source") in ag_topic_ids or e.get("target") in ag_topic_ids],
            "active_in": [e for e in active_in
                         if e.get("source") in ag_topic_ids],
        }
    }

    return {
        "nodes": {
            "topics": topics,
            "subcategories": subcategories,
            "periods": periods,
        },
        "edges": {
            "contains_topic": contains_topic,
            "active_in": active_in,
            "parent_of": parent_of,
            "neighbor_of": neighbor_of,
            "evolves_to": evolves_to,
        },
        "subgraphs": {
            "math.LO": lo_subgraph,
            "math.AG": ag_subgraph,
        },
        "metadata": {
            "total_topics": len(topics),
            "total_edges": sum(len(v) for v in [contains_topic, active_in, parent_of, neighbor_of, evolves_to]),
            "lo_topic_count": len(lo_topic_ids),
            "ag_topic_count": len(ag_topic_ids),
            "evolves_to_count": len(evolves_to),
        }
    }


# Test Classes

class TestBundleGeneration:
    """Test basic bundle creation from kg_v1."""

    def test_bundle_has_required_structure(self, visualization_bundle: Dict[str, Any]):
        """Bundle should have nodes, edges, subgraphs, and metadata."""
        assert "nodes" in visualization_bundle, "Bundle missing nodes"
        assert "edges" in visualization_bundle, "Bundle missing edges"
        assert "subgraphs" in visualization_bundle, "Bundle missing subgraphs"
        assert "metadata" in visualization_bundle, "Bundle missing metadata"

    def test_bundle_nodes_has_topics(self, visualization_bundle: Dict[str, Any]):
        """Bundle nodes should contain topics."""
        assert "topics" in visualization_bundle["nodes"], "Bundle nodes missing topics"
        assert len(visualization_bundle["nodes"]["topics"]) > 0, "Bundle has no topics"

    def test_bundle_nodes_has_subcategories(self, visualization_bundle: Dict[str, Any]):
        """Bundle nodes should contain subcategories."""
        assert "subcategories" in visualization_bundle["nodes"], "Bundle nodes missing subcategories"
        assert len(visualization_bundle["nodes"]["subcategories"]) > 0, "Bundle has no subcategories"

    def test_bundle_nodes_has_periods(self, visualization_bundle: Dict[str, Any]):
        """Bundle nodes should contain periods."""
        assert "periods" in visualization_bundle["nodes"], "Bundle nodes missing periods"
        assert len(visualization_bundle["nodes"]["periods"]) > 0, "Bundle has no periods"

    def test_bundle_edges_has_all_types(self, visualization_bundle: Dict[str, Any]):
        """Bundle edges should contain all edge types."""
        edge_types = ["contains_topic", "active_in", "parent_of", "neighbor_of", "evolves_to"]
        for edge_type in edge_types:
            assert edge_type in visualization_bundle["edges"], f"Bundle edges missing {edge_type}"

    def test_bundle_metadata_has_counts(self, visualization_bundle: Dict[str, Any]):
        """Bundle metadata should have count fields."""
        metadata = visualization_bundle["metadata"]
        assert "total_topics" in metadata, "Metadata missing total_topics"
        assert "total_edges" in metadata, "Metadata missing total_edges"
        assert "lo_topic_count" in metadata, "Metadata missing lo_topic_count"
        assert "ag_topic_count" in metadata, "Metadata missing ag_topic_count"
        assert "evolves_to_count" in metadata, "Metadata missing evolves_to_count"


class TestSubgraphLO:
    """Test LO subgraph structure."""

    def test_lo_subgraph_exists(self, visualization_bundle: Dict[str, Any]):
        """LO subgraph should exist."""
        assert "math.LO" in visualization_bundle["subgraphs"], "LO subgraph missing"

    def test_lo_subgraph_has_nodes(self, visualization_bundle: Dict[str, Any]):
        """LO subgraph should have nodes."""
        lo_subgraph = visualization_bundle["subgraphs"]["math.LO"]
        assert "nodes" in lo_subgraph, "LO subgraph missing nodes"
        assert len(lo_subgraph["nodes"]) > 0, "LO subgraph has no nodes"

    def test_lo_subgraph_has_edges(self, visualization_bundle: Dict[str, Any]):
        """LO subgraph should have edges."""
        lo_subgraph = visualization_bundle["subgraphs"]["math.LO"]
        assert "edges" in lo_subgraph, "LO subgraph missing edges"

    def test_lo_subgraph_nodes_are_all_lo(self, visualization_bundle: Dict[str, Any]):
        """All nodes in LO subgraph should be LO subcategory."""
        lo_subgraph = visualization_bundle["subgraphs"]["math.LO"]
        for node in lo_subgraph["nodes"]:
            assert node.get("subcategory") == "LO", f"Non-LO topic in LO subgraph: {node.get('id')}"

    def test_lo_subgraph_has_15_topics(self, visualization_bundle: Dict[str, Any]):
        """LO subgraph should have exactly 15 topics (KG-02 baseline)."""
        lo_subgraph = visualization_bundle["subgraphs"]["math.LO"]
        assert len(lo_subgraph["nodes"]) == 15, f"Expected 15 LO topics, got {len(lo_subgraph['nodes'])}"

    def test_lo_subgraph_evolves_to_edges(self, visualization_bundle: Dict[str, Any]):
        """LO subgraph should have evolves_to edges."""
        lo_subgraph = visualization_bundle["subgraphs"]["math.LO"]
        evolves_to = lo_subgraph["edges"].get("evolves_to", [])
        # After KG-02-fix: 4 LO edges (2 positive + 1 negative + 1 ambiguous)
        assert len(evolves_to) == 4, f"Expected 4 LO evolves_to edges, got {len(evolves_to)}"


class TestSubgraphAG:
    """Test AG subgraph structure."""

    def test_ag_subgraph_exists(self, visualization_bundle: Dict[str, Any]):
        """AG subgraph should exist."""
        assert "math.AG" in visualization_bundle["subgraphs"], "AG subgraph missing"

    def test_ag_subgraph_has_nodes(self, visualization_bundle: Dict[str, Any]):
        """AG subgraph should have nodes."""
        ag_subgraph = visualization_bundle["subgraphs"]["math.AG"]
        assert "nodes" in ag_subgraph, "AG subgraph missing nodes"
        assert len(ag_subgraph["nodes"]) > 0, "AG subgraph has no nodes"

    def test_ag_subgraph_has_edges(self, visualization_bundle: Dict[str, Any]):
        """AG subgraph should have edges."""
        ag_subgraph = visualization_bundle["subgraphs"]["math.AG"]
        assert "edges" in ag_subgraph, "AG subgraph missing edges"

    def test_ag_subgraph_nodes_are_all_ag(self, visualization_bundle: Dict[str, Any]):
        """All nodes in AG subgraph should be AG subcategory."""
        ag_subgraph = visualization_bundle["subgraphs"]["math.AG"]
        for node in ag_subgraph["nodes"]:
            assert node.get("subcategory") == "AG", f"Non-AG topic in AG subgraph: {node.get('id')}"

    def test_ag_subgraph_has_17_topics(self, visualization_bundle: Dict[str, Any]):
        """AG subgraph should have exactly 17 topics (KG-02 baseline)."""
        ag_subgraph = visualization_bundle["subgraphs"]["math.AG"]
        assert len(ag_subgraph["nodes"]) == 17, f"Expected 17 AG topics, got {len(ag_subgraph['nodes'])}"

    def test_ag_subgraph_evolves_to_edges(self, visualization_bundle: Dict[str, Any]):
        """AG subgraph should have evolves_to edges."""
        ag_subgraph = visualization_bundle["subgraphs"]["math.AG"]
        evolves_to = ag_subgraph["edges"].get("evolves_to", [])
        # After KG-02-fix: 5 AG edges (2 positive + 3 negative)
        assert len(evolves_to) == 5, f"Expected 5 AG evolves_to edges, got {len(evolves_to)}"


class TestPRExclusion:
    """Test that PR is NOT in any bundle output."""

    def test_no_pr_topics_in_bundle(self, visualization_bundle: Dict[str, Any]):
        """No PR topics should be in the bundle."""
        topics = visualization_bundle["nodes"]["topics"]
        pr_topics = [t for t in topics if t.get("subcategory") == "PR"]
        assert len(pr_topics) == 0, f"Found {len(pr_topics)} PR topics in bundle"

    def test_no_pr_in_subcategories(self, visualization_bundle: Dict[str, Any]):
        """math.PR should not be in subcategories."""
        subcategories = visualization_bundle["nodes"]["subcategories"]
        pr_subcats = [s for s in subcategories if s.get("code") == "math.PR"]
        assert len(pr_subcats) == 0, f"Found {len(pr_subcats)} PR subcategories"

    def test_no_pr_edges_in_bundle(self, visualization_bundle: Dict[str, Any]):
        """No edges should involve PR topics."""
        topics = visualization_bundle["nodes"]["topics"]
        pr_topic_ids = {t["id"] for t in topics if t.get("subcategory") == "PR"}

        for edge_type, edges in visualization_bundle["edges"].items():
            for edge in edges:
                assert edge.get("source") not in pr_topic_ids, \
                    f"Edge in {edge_type} involves PR topic: {edge.get('source')}"
                assert edge.get("target") not in pr_topic_ids, \
                    f"Edge in {edge_type} involves PR topic: {edge.get('target')}"

    def test_no_pr_in_subgraphs(self, visualization_bundle: Dict[str, Any]):
        """No PR topics should be in any subgraph."""
        for subcat, subgraph in visualization_bundle["subgraphs"].items():
            for node in subgraph["nodes"]:
                assert node.get("subcategory") != "PR", \
                    f"PR topic found in {subcat} subgraph: {node.get('id')}"

    def test_pr_not_in_subgraphs_key(self, visualization_bundle: Dict[str, Any]):
        """math.PR should not be a subgraph key."""
        assert "math.PR" not in visualization_bundle["subgraphs"], \
            "math.PR should not have its own subgraph"


class TestEvidenceLabels:
    """Test that edge evidence labels are frontend-readable."""

    def test_evolves_to_edges_have_evidence_type(self, visualization_bundle: Dict[str, Any]):
        """All evolves_to edges should have evidence_type field."""
        evolves_to = visualization_bundle["edges"]["evolves_to"]
        for edge in evolves_to:
            assert "evidence_type" in edge, f"Edge missing evidence_type: {edge.get('source')} -> {edge.get('target')}"

    def test_evolves_to_edges_have_confidence(self, visualization_bundle: Dict[str, Any]):
        """All evolves_to edges should have confidence field."""
        evolves_to = visualization_bundle["edges"]["evolves_to"]
        for edge in evolves_to:
            assert "confidence" in edge, f"Edge missing confidence: {edge.get('source')} -> {edge.get('target')}"

    def test_evolves_to_edges_have_benchmark_case_id(self, visualization_bundle: Dict[str, Any]):
        """All evolves_to edges should have benchmark_case_id field."""
        evolves_to = visualization_bundle["edges"]["evolves_to"]
        for edge in evolves_to:
            assert "benchmark_case_id" in edge, f"Edge missing benchmark_case_id: {edge.get('source')} -> {edge.get('target')}"

    def test_evolves_to_edges_have_benchmark_status(self, visualization_bundle: Dict[str, Any]):
        """All evolves_to edges should have benchmark_status field."""
        evolves_to = visualization_bundle["edges"]["evolves_to"]
        for edge in evolves_to:
            assert "benchmark_status" in edge, f"Edge missing benchmark_status: {edge.get('source')} -> {edge.get('target')}"

    def test_evolves_to_edges_have_expected_relation(self, visualization_bundle: Dict[str, Any]):
        """All evolves_to edges should have expected_relation field."""
        evolves_to = visualization_bundle["edges"]["evolves_to"]
        for edge in evolves_to:
            assert "expected_relation" in edge, f"Edge missing expected_relation: {edge.get('source')} -> {edge.get('target')}"

    def test_evidence_labels_are_strings(self, visualization_bundle: Dict[str, Any]):
        """Evidence label values should be strings (frontend-readable)."""
        evolves_to = visualization_bundle["edges"]["evolves_to"]
        string_fields = ["evidence_type", "confidence", "benchmark_case_id", "benchmark_status", "expected_relation"]

        for edge in evolves_to:
            for field in string_fields:
                if field in edge:
                    assert isinstance(edge[field], str), \
                        f"Field {field} should be string, got {type(edge[field])}"

    def test_confidence_values_are_valid(self, visualization_bundle: Dict[str, Any]):
        """Confidence values should be valid."""
        valid_confidences = {"confirmed", "negative", "ambiguous"}
        evolves_to = visualization_bundle["edges"]["evolves_to"]
        for edge in evolves_to:
            confidence = edge.get("confidence")
            assert confidence in valid_confidences, f"Invalid confidence: {confidence}"

    def test_benchmark_status_values_are_valid(self, visualization_bundle: Dict[str, Any]):
        """Benchmark status values should be valid."""
        valid_statuses = {"positive", "negative", "ambiguous"}
        evolves_to = visualization_bundle["edges"]["evolves_to"]
        for edge in evolves_to:
            status = edge.get("benchmark_status")
            assert status in valid_statuses, f"Invalid benchmark_status: {status}"

    def test_evidence_type_is_benchmark_confirmed(self, visualization_bundle: Dict[str, Any]):
        """Evidence type should be 'benchmark-confirmed'."""
        evolves_to = visualization_bundle["edges"]["evolves_to"]
        for edge in evolves_to:
            assert edge.get("evidence_type") == "benchmark-confirmed", \
                f"Invalid evidence_type: {edge.get('evidence_type')}"


class TestCountsAlignment:
    """Test that bundle counts align with KG-02 baseline."""

    def test_total_topic_count_is_32(self, visualization_bundle: Dict[str, Any]):
        """Total topic count should be 32 (15 LO + 17 AG)."""
        topics = visualization_bundle["nodes"]["topics"]
        assert len(topics) == 32, f"Expected 32 topics, got {len(topics)}"

    def test_lo_topic_count_is_15(self, visualization_bundle: Dict[str, Any]):
        """LO topic count should be 15."""
        topics = visualization_bundle["nodes"]["topics"]
        lo_count = len([t for t in topics if t.get("subcategory") == "LO"])
        assert lo_count == 15, f"Expected 15 LO topics, got {lo_count}"

    def test_ag_topic_count_is_17(self, visualization_bundle: Dict[str, Any]):
        """AG topic count should be 17."""
        topics = visualization_bundle["nodes"]["topics"]
        ag_count = len([t for t in topics if t.get("subcategory") == "AG"])
        assert ag_count == 17, f"Expected 17 AG topics, got {ag_count}"

    def test_evolves_to_count_is_9(self, visualization_bundle: Dict[str, Any]):
        """evolves_to edge count should be 9 (4 LO + 5 AG)."""
        evolves_to = visualization_bundle["edges"]["evolves_to"]
        assert len(evolves_to) == 9, f"Expected 9 evolves_to edges, got {len(evolves_to)}"

    def test_lo_evolves_to_count_is_4(self, visualization_bundle: Dict[str, Any]):
        """LO evolves_to edge count should be 4."""
        evolves_to = visualization_bundle["edges"]["evolves_to"]
        lo_count = len([e for e in evolves_to if e.get("subcategory") == "math.LO"])
        assert lo_count == 4, f"Expected 4 LO evolves_to edges, got {lo_count}"

    def test_ag_evolves_to_count_is_5(self, visualization_bundle: Dict[str, Any]):
        """AG evolves_to edge count should be 5."""
        evolves_to = visualization_bundle["edges"]["evolves_to"]
        ag_count = len([e for e in evolves_to if e.get("subcategory") == "math.AG"])
        assert ag_count == 5, f"Expected 5 AG evolves_to edges, got {ag_count}"

    def test_metadata_counts_match_actual(self, visualization_bundle: Dict[str, Any]):
        """Metadata counts should match actual data counts."""
        metadata = visualization_bundle["metadata"]
        topics = visualization_bundle["nodes"]["topics"]
        evolves_to = visualization_bundle["edges"]["evolves_to"]

        lo_count = len([t for t in topics if t.get("subcategory") == "LO"])
        ag_count = len([t for t in topics if t.get("subcategory") == "AG"])

        assert metadata["lo_topic_count"] == lo_count, \
            f"Metadata lo_topic_count mismatch: {metadata['lo_topic_count']} vs {lo_count}"
        assert metadata["ag_topic_count"] == ag_count, \
            f"Metadata ag_topic_count mismatch: {metadata['ag_topic_count']} vs {ag_count}"
        assert metadata["evolves_to_count"] == len(evolves_to), \
            f"Metadata evolves_to_count mismatch: {metadata['evolves_to_count']} vs {len(evolves_to)}"


class TestSubgraphEdgeConsistency:
    """Test that subgraph edges are consistent with full graph."""

    def test_lo_subgraph_edges_subset_of_full(self, visualization_bundle: Dict[str, Any]):
        """LO subgraph edges should be subset of full edges."""
        full_evolves_to = {(e["source"], e["target"]) for e in visualization_bundle["edges"]["evolves_to"]}
        lo_subgraph = visualization_bundle["subgraphs"]["math.LO"]
        lo_edges = lo_subgraph["edges"]["evolves_to"]

        for edge in lo_edges:
            edge_key = (edge["source"], edge["target"])
            assert edge_key in full_evolves_to, f"LO subgraph edge not in full graph: {edge_key}"

    def test_ag_subgraph_edges_subset_of_full(self, visualization_bundle: Dict[str, Any]):
        """AG subgraph edges should be subset of full edges."""
        full_evolves_to = {(e["source"], e["target"]) for e in visualization_bundle["edges"]["evolves_to"]}
        ag_subgraph = visualization_bundle["subgraphs"]["math.AG"]
        ag_edges = ag_subgraph["edges"]["evolves_to"]

        for edge in ag_edges:
            edge_key = (edge["source"], edge["target"])
            assert edge_key in full_evolves_to, f"AG subgraph edge not in full graph: {edge_key}"

    def test_all_evolves_to_edges_in_subgraphs(self, visualization_bundle: Dict[str, Any]):
        """All evolves_to edges should be in either LO or AG subgraph."""
        full_evolves_to = {(e["source"], e["target"]): e for e in visualization_bundle["edges"]["evolves_to"]}

        lo_subgraph = visualization_bundle["subgraphs"]["math.LO"]
        ag_subgraph = visualization_bundle["subgraphs"]["math.AG"]

        lo_edges = {(e["source"], e["target"]) for e in lo_subgraph["edges"]["evolves_to"]}
        ag_edges = {(e["source"], e["target"]) for e in ag_subgraph["edges"]["evolves_to"]}

        all_subgraph_edges = lo_edges | ag_edges

        assert len(all_subgraph_edges) == len(full_evolves_to), \
            f"Subgraph edges ({len(all_subgraph_edges)}) don't match full graph ({len(full_evolves_to)})"

        for edge_key in full_evolves_to:
            assert edge_key in all_subgraph_edges, f"Edge not in any subgraph: {edge_key}"


class TestVisualizationExporterOutput:
    """Test actual visualization exporter output (KG-03-fix: tests now cover real exporter)."""

    def test_graph_bundle_file_exists(self, fresh_visualization_export: Path):
        """graph_bundle.json should exist."""
        assert (fresh_visualization_export / 'graph_bundle.json').exists()

    def test_subgraph_lo_file_exists(self, fresh_visualization_export: Path):
        """subgraph_lo.json should exist."""
        assert (fresh_visualization_export / 'subgraph_lo.json').exists()

    def test_subgraph_ag_file_exists(self, fresh_visualization_export: Path):
        """subgraph_ag.json should exist."""
        assert (fresh_visualization_export / 'subgraph_ag.json').exists()

    def test_timeline_summary_file_exists(self, fresh_visualization_export: Path):
        """timeline_summary.json should exist."""
        assert (fresh_visualization_export / 'timeline_summary.json').exists()

    def test_legend_file_exists(self, fresh_visualization_export: Path):
        """legend.json should exist."""
        assert (fresh_visualization_export / 'legend.json').exists()

    def test_graph_bundle_has_correct_counts(self, fresh_visualization_export: Path):
        """graph_bundle.json should have correct counts."""
        with open(fresh_visualization_export / 'graph_bundle.json', 'r', encoding='utf-8') as f:
            bundle = json.load(f)

        assert bundle['stats']['topic_count'] == 32
        assert bundle['stats']['subcategory_count'] == 2
        assert bundle['stats']['evolves_to_count'] == 9
        assert bundle['nodes']['total'] == 47  # 32 topics + 2 subcategories + 13 periods

    def test_graph_bundle_has_subcategory_codes(self, fresh_visualization_export: Path):
        """graph_bundle.json subcategories should have canonical code field."""
        with open(fresh_visualization_export / 'graph_bundle.json', 'r', encoding='utf-8') as f:
            bundle = json.load(f)

        subcats = bundle['nodes']['subcategories']
        assert len(subcats) == 2

        codes = [s.get('code') for s in subcats]
        assert 'math.LO' in codes, f"Expected 'math.LO' in codes, got {codes}"
        assert 'math.AG' in codes, f"Expected 'math.AG' in codes, got {codes}"

    def test_graph_bundle_subcategory_id_code_consistency(self, fresh_visualization_export: Path):
        """Subcategory id and code should be consistent."""
        with open(fresh_visualization_export / 'graph_bundle.json', 'r', encoding='utf-8') as f:
            bundle = json.load(f)

        for subcat in bundle['nodes']['subcategories']:
            # id and code should be the same (canonical form)
            assert subcat['id'] == subcat['code'], \
                f"Subcategory id ({subcat['id']}) != code ({subcat['code']})"
            # subcategory should be short form
            assert subcat['subcategory'] == subcat['code'].replace('math.', ''), \
                f"Subcategory field should be short form of code"

    def test_subgraph_lo_has_correct_counts(self, fresh_visualization_export: Path):
        """subgraph_lo.json should have correct counts."""
        with open(fresh_visualization_export / 'subgraph_lo.json', 'r', encoding='utf-8') as f:
            subgraph = json.load(f)

        assert subgraph['stats']['topic_count'] == 15
        assert subgraph['stats']['evolves_to_count'] == 4

    def test_subgraph_ag_has_correct_counts(self, fresh_visualization_export: Path):
        """subgraph_ag.json should have correct counts."""
        with open(fresh_visualization_export / 'subgraph_ag.json', 'r', encoding='utf-8') as f:
            subgraph = json.load(f)

        assert subgraph['stats']['topic_count'] == 17
        assert subgraph['stats']['evolves_to_count'] == 5

    def test_no_pr_data_in_bundle(self, fresh_visualization_export: Path):
        """PR data should not be in any bundle files."""
        with open(fresh_visualization_export / 'graph_bundle.json', 'r', encoding='utf-8') as f:
            bundle = json.load(f)

        # No PR subcategories
        subcat_codes = [s.get('code') for s in bundle['nodes']['subcategories']]
        assert 'math.PR' not in subcat_codes, "Found math.PR in subcategories"

        # No PR topics
        for topic in bundle['nodes']['topics']:
            assert topic.get('subcategory') != 'PR', f"Found PR topic: {topic.get('id')}"

        # No PR evolves_to edges
        for edge in bundle['edges']['by_kind']['EVOLVES_TO']:
            assert edge.get('subcategory') != 'math.PR', f"Found PR edge"

    def test_evolves_to_edges_have_required_fields(self, fresh_visualization_export: Path):
        """EVOLVES_TO edges should have all required evidence fields."""
        with open(fresh_visualization_export / 'graph_bundle.json', 'r', encoding='utf-8') as f:
            bundle = json.load(f)

        evolves_to = bundle['edges']['by_kind']['EVOLVES_TO']
        assert len(evolves_to) == 9

        required_fields = ['evidence_type', 'confidence', 'benchmark_case_id',
                          'benchmark_status', 'expected_relation']
        for edge in evolves_to:
            for field in required_fields:
                assert field in edge, f"Edge {edge.get('source')}->{edge.get('target')} missing {field}"

    def test_graph_bundle_exposes_domain_knowledge_layers(self, fresh_visualization_export: Path):
        """graph_bundle.json should expose export-facing domain narrative metadata."""
        with open(fresh_visualization_export / 'graph_bundle.json', 'r', encoding='utf-8') as f:
            bundle = json.load(f)

        domain_layers = bundle.get('metadata', {}).get('domain_knowledge_layers', {})
        assert 'math.LO' in domain_layers
        assert 'math.AG' in domain_layers
        assert 'math.CO' in domain_layers
        assert 'math.DS' in domain_layers
        assert 'math.NA' in domain_layers

    def test_domain_layers_keep_lo_ag_co_ds_na_statuses_separate(self, fresh_visualization_export: Path):
        """LO/AG baseline subgraphs, CO contract metadata, and DS/NA narrative-only metadata should stay distinct."""
        with open(fresh_visualization_export / 'graph_bundle.json', 'r', encoding='utf-8') as f:
            bundle = json.load(f)

        domain_layers = bundle['metadata']['domain_knowledge_layers']
        lo_meta = domain_layers['math.LO']
        ag_meta = domain_layers['math.AG']
        co_meta = domain_layers['math.CO']
        ds_meta = domain_layers['math.DS']
        na_meta = domain_layers['math.NA']

        assert lo_meta['graph_shape'] == 'baseline_plus_bridge_ring'
        assert lo_meta['baseline_truth_layer_keys'] == ['modal_baseline']
        assert lo_meta['narrative_only_layer_keys'] == ['bridge_ring', 'boundary_negative', 'review_boundary']
        assert lo_meta['layers']['modal_baseline']['case_ids'] == ['lo-b1']
        assert lo_meta['layers']['bridge_ring']['case_ids'] == ['lo-b2', 'lo-b3', 'lo-b4', 'lo-b5']

        assert ag_meta['graph_shape'] == 'confirmed_core_plus_bridge_ring_plus_boundary'
        assert ag_meta['baseline_truth_layer_keys'] == ['confirmed_core']
        assert ag_meta['layers']['confirmed_core']['case_ids'] == ['ag-p1']
        assert ag_meta['layers']['bridge_ring']['metadata_only_case_ids'] == ['ag-p2', 'ag-p3']

        assert co_meta['export_presence'] == 'docs_only_contract'
        assert co_meta['selected_rule'] == 'math_co_matroid_structure_continuity'
        assert co_meta['graph_visible_layer_keys'] == ['matroid_mvp', 'bridge_support', 'excluded_boundary', 'review_boundary']
        assert co_meta['metadata_only_layer_keys'] == ['deferred_branch']
        assert co_meta['layers']['matroid_mvp']['case_ids'] == ['co-m1', 'co-m2']
        assert co_meta['layers']['matroid_mvp']['graph_visible_case_ids'] == ['co-m1', 'co-m2']
        assert co_meta['layers']['bridge_support']['graph_visible_case_ids'] == ['co-b2']
        assert co_meta['graph_visible_case_ids'] == ['co-b2', 'co-m1', 'co-m2', 'co-mn1', 'co-mn2', 'co-ma1']
        assert co_meta['case_counts_by_export_status'] == {
            'narrative_subgraph_only': 6,
            'docs_only_outside_export_scope': 1,
        }
        assert co_meta['graph_visible_subgraph']['stats']['topic_count'] == 8
        assert co_meta['graph_visible_subgraph']['stats']['edge_count'] == 6
        assert co_meta['graph_visible_subgraph']['stats']['edges_by_graph_band'] == {
            'bridge': 1,
            'boundary': 2,
            'review': 1,
            'contract': 2,
        }

        assert ds_meta['export_presence'] == 'docs_only_narrative'
        assert ds_meta['topology_status'] == 'not_in_baseline_topology'
        assert ds_meta['candidate_rule'] == 'math_ds_ergodic_entropy_continuity'
        assert ds_meta['narrative_status'] == 'benchmark_skeleton_ready'
        assert ds_meta['encoded_case_ids'] == []
        assert ds_meta['graph_visible_layer_keys'] == ['ergodic_entropy_skeleton', 'excluded_boundary', 'review_boundary']
        assert ds_meta['metadata_only_layer_keys'] == []
        assert ds_meta['graph_visible_case_ids'] == ['ds-b1', 'ds-b2', 'ds-n1', 'ds-n2', 'ds-a1']
        assert ds_meta['layers']['ergodic_entropy_skeleton']['graph_visible_case_ids'] == ['ds-b1', 'ds-b2']
        assert ds_meta['layers']['excluded_boundary']['graph_visible_case_ids'] == ['ds-n1', 'ds-n2']
        assert ds_meta['layers']['review_boundary']['graph_visible_case_ids'] == ['ds-a1']
        assert ds_meta['case_counts_by_graph_band'] == {
            'bridge': 2,
            'boundary': 2,
            'review': 1,
        }
        assert ds_meta['case_counts_by_export_status'] == {
            'narrative_subgraph_only': 5,
        }
        assert ds_meta['visible_graph_bands'] == ['bridge', 'boundary', 'review']
        assert ds_meta['graph_visible_subgraph']['stats']['topic_count'] == 6
        assert ds_meta['graph_visible_subgraph']['stats']['edge_count'] == 5
        assert ds_meta['graph_visible_subgraph']['stats']['edges_by_graph_band'] == {
            'bridge': 2,
            'boundary': 2,
            'review': 1,
        }

        assert na_meta['export_presence'] == 'docs_only_narrative'
        assert na_meta['topology_status'] == 'not_in_baseline_topology'
        assert na_meta['candidate_rule'] == 'math_na_krylov_iterative_continuity'
        assert na_meta['narrative_status'] == 'benchmark_skeleton_ready'
        assert na_meta['baseline_truth_layer_keys'] == []
        assert na_meta['narrative_only_layer_keys'] == ['krylov_iterative_skeleton', 'excluded_boundary', 'review_boundary']
        assert na_meta['encoded_case_ids'] == []
        assert na_meta['layers']['krylov_iterative_skeleton']['metadata_only_case_ids'] == ['na-b1', 'na-b2']
        assert na_meta['case_counts_by_graph_band'] == {
            'bridge': 2,
            'boundary': 2,
            'review': 1,
        }
        assert na_meta['case_counts_by_export_status'] == {
            'docs_only_outside_export_scope': 5,
        }
        assert na_meta['visible_graph_bands'] == ['bridge', 'boundary', 'review']

    def test_graph_bundle_tracks_evolves_to_bands(self, fresh_visualization_export: Path):
        """graph_bundle.json should expose graph-band counts without changing edge totals."""
        with open(fresh_visualization_export / 'graph_bundle.json', 'r', encoding='utf-8') as f:
            bundle = json.load(f)

        assert bundle['stats']['evolves_to_by_graph_band'] == {
            'baseline': 2,
            'bridge': 1,
            'boundary': 4,
            'review': 2,
        }

    def test_graph_bundle_tracks_narrative_case_stats(self, fresh_visualization_export: Path):
        """graph_bundle.json should expose narrative-only band stats separately from encoded edges."""
        with open(fresh_visualization_export / 'graph_bundle.json', 'r', encoding='utf-8') as f:
            bundle = json.load(f)

        assert bundle['stats']['domain_count'] == 5
        assert bundle['stats']['domain_export_presence_counts'] == {
            'baseline_subgraph': 2,
            'docs_only_contract': 1,
            'docs_only_narrative': 2,
        }
        assert bundle['stats']['domain_topology_status_counts'] == {
            'baseline_topology_included': 2,
            'not_in_baseline_topology': 3,
        }
        assert bundle['stats']['narrative_case_counts_by_graph_band'] == {
            'baseline': 2,
            'bridge': 11,
            'boundary': 15,
            'review': 6,
            'contract': 2,
            'deferred': 1,
        }
        assert bundle['stats']['narrative_layer_counts_by_graph_band'] == {
            'baseline': 2,
            'bridge': 5,
            'boundary': 5,
            'review': 5,
            'contract': 1,
            'deferred': 1,
        }
        assert bundle['stats']['narrative_subgraph_domain_count'] == 2
        assert bundle['stats']['narrative_subgraph_edge_count'] == 11
        assert bundle['stats']['narrative_subgraph_node_count'] == 14
        assert bundle['stats']['narrative_subgraph_counts_by_graph_band'] == {
            'bridge': 3,
            'boundary': 4,
            'review': 2,
            'contract': 2,
        }

    def test_graph_bundle_filters_expose_narrative_graph_bands(self, fresh_visualization_export: Path):
        """filters should expose graph bands present in metadata-only narrative layers too."""
        with open(fresh_visualization_export / 'graph_bundle.json', 'r', encoding='utf-8') as f:
            bundle = json.load(f)

        assert bundle['filters']['graph_bands'] == ['baseline', 'bridge', 'boundary', 'review', 'contract', 'deferred']
        assert bundle['filters']['encoded_graph_bands'] == ['baseline', 'bridge', 'boundary', 'review']
        assert bundle['filters']['domain_export_presences'] == ['baseline_subgraph', 'docs_only_contract', 'docs_only_narrative']
        assert bundle['filters']['topology_statuses'] == ['baseline_topology_included', 'not_in_baseline_topology']
        assert bundle['filters']['narrative_statuses'] == ['benchmark_skeleton_ready']
        assert bundle['filters']['narrative_subgraph_domains'] == ['math.CO', 'math.DS']

    def test_evolves_to_edges_have_graph_annotations(self, fresh_visualization_export: Path):
        """EVOLVES_TO edges should expose narrative band/layer metadata."""
        with open(fresh_visualization_export / 'graph_bundle.json', 'r', encoding='utf-8') as f:
            bundle = json.load(f)

        evolves_to = bundle['edges']['by_kind']['EVOLVES_TO']
        required_fields = ['graph_band', 'graph_layer', 'graph_role', 'graph_export_status']
        for edge in evolves_to:
            for field in required_fields:
                assert edge.get(field), f"Edge {edge.get('benchmark_case_id')} missing {field}"

        by_case = {edge['benchmark_case_id']: edge for edge in evolves_to}
        assert by_case['lo-b1']['graph_band'] == 'baseline'
        assert by_case['lo-b3']['graph_band'] == 'bridge'
        assert by_case['ag-p1']['graph_layer'] == 'confirmed_core'
        assert by_case['ag-amb1']['graph_band'] == 'review'

    def test_subgraphs_expose_narrative_metadata(self, fresh_visualization_export: Path):
        """subgraph files should carry narrative metadata for graph-facing explanation."""
        with open(fresh_visualization_export / 'subgraph_lo.json', 'r', encoding='utf-8') as f:
            subgraph_lo = json.load(f)
        with open(fresh_visualization_export / 'subgraph_ag.json', 'r', encoding='utf-8') as f:
            subgraph_ag = json.load(f)

        assert subgraph_lo['metadata']['graph_shape'] == 'baseline_plus_bridge_ring'
        assert subgraph_lo['metadata']['baseline_truth_layer_keys'] == ['modal_baseline']
        assert subgraph_lo['metadata']['narrative_only_layer_keys'] == ['bridge_ring', 'boundary_negative', 'review_boundary']
        assert subgraph_lo['metadata']['visible_graph_bands'] == ['baseline', 'bridge', 'boundary', 'review']
        assert 'bridge_ring' in subgraph_lo['metadata']['narrative_layers']
        assert len(subgraph_lo['metadata']['narrative_case_registry']) == 13
        assert subgraph_lo['stats']['narrative_case_counts_by_graph_band'] == {
            'baseline': 1,
            'bridge': 4,
            'boundary': 6,
            'review': 2,
        }
        assert subgraph_lo['stats']['narrative_layer_counts_by_graph_band'] == {
            'baseline': 1,
            'bridge': 1,
            'boundary': 1,
            'review': 1,
        }
        assert subgraph_lo['stats']['evolves_to_by_graph_band'] == {
            'baseline': 1,
            'bridge': 1,
            'boundary': 1,
            'review': 1,
        }

        assert subgraph_ag['metadata']['graph_shape'] == 'confirmed_core_plus_bridge_ring_plus_boundary'
        assert subgraph_ag['metadata']['baseline_truth_layer_keys'] == ['confirmed_core']
        assert subgraph_ag['metadata']['narrative_only_layer_keys'] == ['bridge_ring', 'excluded_boundary', 'review_boundary']
        assert subgraph_ag['metadata']['visible_graph_bands'] == ['baseline', 'bridge', 'boundary', 'review']
        assert subgraph_ag['metadata']['narrative_layers']['bridge_ring']['metadata_only_case_ids'] == ['ag-p2', 'ag-p3']
        assert len(subgraph_ag['metadata']['narrative_case_registry']) == 7
        assert subgraph_ag['stats']['narrative_case_counts_by_graph_band'] == {
            'baseline': 1,
            'bridge': 2,
            'boundary': 3,
            'review': 1,
        }
        assert subgraph_ag['stats']['narrative_layer_counts_by_graph_band'] == {
            'baseline': 1,
            'bridge': 1,
            'boundary': 1,
            'review': 1,
        }
        assert subgraph_ag['stats']['evolves_to_by_graph_band'] == {
            'baseline': 1,
            'boundary': 3,
            'review': 1,
        }

    def test_graph_bundle_exposes_co_narrative_subgraph(self, fresh_visualization_export: Path):
        """graph_bundle.json should expose a graph-visible but non-baseline CO narrative subgraph."""
        with open(fresh_visualization_export / 'graph_bundle.json', 'r', encoding='utf-8') as f:
            bundle = json.load(f)

        narrative_subgraphs = bundle.get('narrative_subgraphs', {})
        assert list(narrative_subgraphs.keys()) == ['math.CO', 'math.DS']

        subgraph_co = narrative_subgraphs['math.CO']
        assert subgraph_co['metadata']['truth_scope'] == 'narrative_only'
        assert subgraph_co['metadata']['selected_rule'] == 'math_co_matroid_structure_continuity'
        assert subgraph_co['metadata']['graph_visible_layer_keys'] == ['matroid_mvp', 'bridge_support', 'excluded_boundary', 'review_boundary']
        assert subgraph_co['metadata']['metadata_only_layer_keys'] == ['deferred_branch']
        assert subgraph_co['metadata']['visible_graph_bands'] == ['bridge', 'boundary', 'review', 'contract']
        assert subgraph_co['stats']['topic_count'] == 8
        assert subgraph_co['stats']['edge_count'] == 6
        assert subgraph_co['stats']['edges_by_export_status'] == {
            'narrative_subgraph_only': 6,
        }
        assert subgraph_co['stats']['edges_by_benchmark_status'] == {
            'positive': 3,
            'negative': 2,
            'ambiguous': 1,
        }

        edge_by_case = {edge['benchmark_case_id']: edge for edge in subgraph_co['edges']}
        assert edge_by_case['co-m1']['graph_band'] == 'contract'
        assert edge_by_case['co-m1']['truth_scope'] == 'narrative_only'
        assert edge_by_case['co-m1']['baseline_truth'] is False
        assert edge_by_case['co-b2']['graph_band'] == 'bridge'
        assert edge_by_case['co-mn1']['benchmark_status'] == 'negative'
        assert edge_by_case['co-ma1']['benchmark_status'] == 'ambiguous'

    def test_subgraph_co_file_exists(self, fresh_visualization_export: Path):
        """subgraph_co.json should exist for the graph-visible CO narrative layer."""
        assert (fresh_visualization_export / 'subgraph_co.json').exists()

    def test_subgraph_ds_file_exists(self, fresh_visualization_export: Path):
        """subgraph_ds.json should exist for the graph-visible DS narrative layer."""
        assert (fresh_visualization_export / 'subgraph_ds.json').exists()

    def test_subgraph_co_has_non_baseline_graph_visible_edges(self, fresh_visualization_export: Path):
        """subgraph_co.json should expose CO narrative edges without changing baseline truth scope."""
        with open(fresh_visualization_export / 'subgraph_co.json', 'r', encoding='utf-8') as f:
            subgraph_co = json.load(f)

        assert subgraph_co['metadata']['topology_status'] == 'not_in_baseline_topology'
        assert subgraph_co['metadata']['truth_scope'] == 'narrative_only'
        assert subgraph_co['metadata']['case_ids'] == ['co-m1', 'co-m2', 'co-b2', 'co-mn1', 'co-mn2', 'co-ma1']
        assert subgraph_co['metadata']['layer_keys'] == ['matroid_mvp', 'bridge_support', 'excluded_boundary', 'review_boundary']
        assert subgraph_co['stats']['edges_by_graph_band'] == {
            'bridge': 1,
            'boundary': 2,
            'review': 1,
            'contract': 2,
        }
        assert len(subgraph_co['nodes']['topics']) == 8
        assert len(subgraph_co['edges']) == 6
        assert {edge['benchmark_case_id'] for edge in subgraph_co['edges']} == {'co-b2', 'co-m1', 'co-m2', 'co-mn1', 'co-mn2', 'co-ma1'}

    def test_graph_bundle_exposes_ds_narrative_subgraph(self, fresh_visualization_export: Path):
        """graph_bundle.json should expose DS as a graph-visible but non-baseline narrative subgraph."""
        with open(fresh_visualization_export / 'graph_bundle.json', 'r', encoding='utf-8') as f:
            bundle = json.load(f)

        subgraph_ds = bundle['narrative_subgraphs']['math.DS']
        assert subgraph_ds['metadata']['truth_scope'] == 'narrative_only'
        assert subgraph_ds['metadata']['candidate_rule'] == 'math_ds_ergodic_entropy_continuity'
        assert subgraph_ds['metadata']['graph_visible_layer_keys'] == ['ergodic_entropy_skeleton', 'excluded_boundary', 'review_boundary']
        assert subgraph_ds['metadata']['metadata_only_layer_keys'] == []
        assert subgraph_ds['metadata']['visible_graph_bands'] == ['bridge', 'boundary', 'review']
        assert subgraph_ds['stats']['topic_count'] == 6
        assert subgraph_ds['stats']['edge_count'] == 5
        assert subgraph_ds['stats']['edges_by_export_status'] == {
            'narrative_subgraph_only': 5,
        }
        assert subgraph_ds['stats']['edges_by_benchmark_status'] == {
            'positive': 2,
            'negative': 2,
            'ambiguous': 1,
        }

        edge_by_case = {edge['benchmark_case_id']: edge for edge in subgraph_ds['edges']}
        assert edge_by_case['ds-b1']['confidence'] == 'inferred'
        assert edge_by_case['ds-b1']['benchmark_status'] == 'positive'
        assert edge_by_case['ds-b1']['evidence_type'] == 'provisional'
        assert edge_by_case['ds-b1']['baseline_truth'] is False
        assert edge_by_case['ds-n1']['confidence'] == 'negative'
        assert edge_by_case['ds-a1']['confidence'] == 'ambiguous'

    def test_timeline_summary_has_periods(self, fresh_visualization_export: Path):
        """timeline_summary.json should have 13 periods."""
        with open(fresh_visualization_export / 'timeline_summary.json', 'r', encoding='utf-8') as f:
            timeline = json.load(f)

        assert len(timeline['timeline']) == 13

    def test_legend_has_schema_definitions(self, fresh_visualization_export: Path):
        """legend.json should have schema definitions."""
        with open(fresh_visualization_export / 'legend.json', 'r', encoding='utf-8') as f:
            legend = json.load(f)

        assert 'node_kinds' in legend
        assert 'edge_kinds' in legend
        assert 'confidence_levels' in legend
        assert 'graph_bands' in legend
        assert 'graph_export_statuses' in legend
        assert 'domain_export_presence' in legend
        assert 'domain_layer_fields' in legend
        assert 'topology_statuses' in legend
        assert 'truth_scopes' in legend

    def test_legend_has_docs_only_narrative_presence(self, fresh_visualization_export: Path):
        """legend.json should explain docs_only_narrative domain exposure."""
        with open(fresh_visualization_export / 'legend.json', 'r', encoding='utf-8') as f:
            legend = json.load(f)

        domain_export_presence = legend.get('domain_export_presence', {})
        assert 'docs_only_narrative' in domain_export_presence
        graph_export_statuses = legend.get('graph_export_statuses', {})
        assert 'narrative_subgraph_only' in graph_export_statuses
        evidence_types = legend.get('evidence_types', {})
        assert 'docs-narrative' in evidence_types
        truth_scopes = legend.get('truth_scopes', {})
        assert 'narrative_only' in truth_scopes
        topology_statuses = legend.get('topology_statuses', {})
        assert 'not_in_baseline_topology' in topology_statuses


class TestConditionalPRVisualizationBundle:
    """Test conditional PR visualization bundle generation."""

    @pytest.fixture
    def fresh_pr_conditional_kg(self, worktree_root: Path) -> Path:
        """Create a conditional KG export with PR data."""
        pr_curation_doc = str(worktree_root / "docs/plans/2026-03-21-math-pr-case-curation.md")
        with tempfile.TemporaryDirectory() as tmpdir:
            export_kg_v1(
                input_file=str(worktree_root / "data/output/aligned_topics_hierarchy.json"),
                benchmark_lo=str(worktree_root / "docs/plans/2026-03-12-math-lo-benchmark.md"),
                benchmark_ag=str(worktree_root / "docs/plans/2026-03-18-math-ag-benchmark.md"),
                output_dir=tmpdir,
                benchmark_pr=pr_curation_doc,
            )
            yield Path(tmpdir)

    @pytest.fixture
    def fresh_pr_conditional_viz(self, fresh_pr_conditional_kg: Path) -> Path:
        """Generate PR conditional visualization bundle."""
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle = build_graph_bundle(str(fresh_pr_conditional_kg))
            subgraph_lo = build_subgraph(bundle, 'LO')
            subgraph_ag = build_subgraph(bundle, 'AG')

            # Build subgraph_pr if PR topics exist
            has_pr = any(t.get('subcategory') == 'PR' for t in bundle['nodes']['topics'])

            timeline = build_timeline_summary(bundle)
            legend = build_legend()

            output_path = Path(tmpdir)
            with open(output_path / 'graph_bundle.json', 'w', encoding='utf-8') as f:
                json.dump(bundle, f, indent=2, ensure_ascii=False)
            with open(output_path / 'subgraph_lo.json', 'w', encoding='utf-8') as f:
                json.dump(subgraph_lo, f, indent=2, ensure_ascii=False)
            with open(output_path / 'subgraph_ag.json', 'w', encoding='utf-8') as f:
                json.dump(subgraph_ag, f, indent=2, ensure_ascii=False)
            with open(output_path / 'timeline_summary.json', 'w', encoding='utf-8') as f:
                json.dump(timeline, f, indent=2, ensure_ascii=False)
            with open(output_path / 'legend.json', 'w', encoding='utf-8') as f:
                json.dump(legend, f, indent=2, ensure_ascii=False)

            if has_pr:
                subgraph_pr = build_subgraph(bundle, 'PR')
                with open(output_path / 'subgraph_pr.json', 'w', encoding='utf-8') as f:
                    json.dump(subgraph_pr, f, indent=2, ensure_ascii=False)

            yield output_path

    def test_pr_bundle_has_graph_bundle(self, fresh_pr_conditional_viz: Path):
        """PR conditional viz should have graph_bundle.json."""
        assert (fresh_pr_conditional_viz / 'graph_bundle.json').exists()

    def test_pr_bundle_has_subgraph_pr(self, fresh_pr_conditional_viz: Path):
        """PR conditional viz should generate subgraph_pr.json."""
        # If there are PR topics, subgraph_pr.json should exist
        with open(fresh_pr_conditional_viz / 'graph_bundle.json', 'r', encoding='utf-8') as f:
            bundle = json.load(f)
        pr_topic_count = len([t for t in bundle['nodes']['topics'] if t.get('subcategory') == 'PR'])
        if pr_topic_count > 0:
            assert (fresh_pr_conditional_viz / 'subgraph_pr.json').exists(), \
                "subgraph_pr.json should exist when PR topics are present"

    def test_baseline_bundle_unchanged(self, fresh_visualization_export: Path):
        """Baseline bundle should not be affected by PR conditional changes. Uses existing fixture."""
        with open(fresh_visualization_export / 'graph_bundle.json', 'r', encoding='utf-8') as f:
            bundle = json.load(f)
        assert bundle['stats']['topic_count'] == 32
        assert bundle['stats']['evolves_to_count'] == 9
        # No PR in baseline bundle
        for topic in bundle['nodes']['topics']:
            assert topic.get('subcategory') != 'PR', f"PR topic found in baseline bundle"

    def test_legend_has_provisional_evidence_type(self, fresh_visualization_export: Path):
        """legend.json should have 'provisional' evidence_type entry."""
        with open(fresh_visualization_export / 'legend.json', 'r', encoding='utf-8') as f:
            legend = json.load(f)
        evidence_types = legend.get('evidence_types', {})
        assert 'provisional' in evidence_types, \
            f"'provisional' not found in evidence_types. Got: {list(evidence_types.keys())}"

    def test_legend_provisional_has_required_fields(self, fresh_visualization_export: Path):
        """legend.json provisional entry should have required fields."""
        with open(fresh_visualization_export / 'legend.json', 'r', encoding='utf-8') as f:
            legend = json.load(f)
        provisional = legend.get('evidence_types', {}).get('provisional', {})
        assert 'description' in provisional
        assert 'color' in provisional

    def test_pr_bundle_has_lo_ag_subcategories(self, fresh_pr_conditional_viz: Path):
        """PR conditional bundle should still include LO and AG subcategories."""
        with open(fresh_pr_conditional_viz / 'graph_bundle.json', 'r', encoding='utf-8') as f:
            bundle = json.load(f)
        codes = [s.get('code') for s in bundle['nodes']['subcategories']]
        assert 'math.LO' in codes, "LO missing from PR conditional bundle"
        assert 'math.AG' in codes, "AG missing from PR conditional bundle"


class TestConditionalVisualizationEntrypoint:
    """Test that the visualization exporter main() entrypoint writes conditional bundle correctly.

    KG-03-fix: These tests verify the actual entrypoint path, not just helper functions.
    They confirm that calling main() with PR conditional input produces the expected
    disk-written files with correct conditional metadata.
    """

    @pytest.fixture
    def fresh_pr_conditional_kg_for_entrypoint(self, worktree_root: Path) -> Path:
        """Create a PR conditional KG export for entrypoint testing."""
        pr_curation_doc = str(worktree_root / "docs/plans/2026-03-21-math-pr-case-curation.md")
        with tempfile.TemporaryDirectory() as tmpdir:
            from pipeline.math_kg_export import export_kg_v1
            export_kg_v1(
                input_file=str(worktree_root / "data/output/aligned_topics_hierarchy.json"),
                benchmark_lo=str(worktree_root / "docs/plans/2026-03-12-math-lo-benchmark.md"),
                benchmark_ag=str(worktree_root / "docs/plans/2026-03-18-math-ag-benchmark.md"),
                output_dir=tmpdir,
                benchmark_pr=pr_curation_doc,
            )
            yield Path(tmpdir)

    def test_entrypoint_writes_graph_bundle(self, fresh_pr_conditional_kg_for_entrypoint: Path, tmp_path: Path):
        """main() should write graph_bundle.json to output dir."""
        from unittest.mock import patch
        from pipeline.math_kg_visualization_export import main
        output_dir = tmp_path / 'conditional_viz'
        output_dir.mkdir()
        with patch('sys.argv', ['math_kg_visualization_export.py',
                                '--input-dir', str(fresh_pr_conditional_kg_for_entrypoint),
                                '--output-dir', str(output_dir)]):
            result = main()
        assert result == 0
        assert (output_dir / 'graph_bundle.json').exists(), "main() should write graph_bundle.json"

    def test_entrypoint_writes_subgraph_pr(self, fresh_pr_conditional_kg_for_entrypoint: Path, tmp_path: Path):
        """main() should write subgraph_pr.json when PR topics present."""
        from unittest.mock import patch
        from pipeline.math_kg_visualization_export import main
        output_dir = tmp_path / 'conditional_viz2'
        output_dir.mkdir()
        with patch('sys.argv', ['math_kg_visualization_export.py',
                                '--input-dir', str(fresh_pr_conditional_kg_for_entrypoint),
                                '--output-dir', str(output_dir)]):
            result = main()
        assert result == 0
        # Verify graph_bundle has PR topics first
        with open(output_dir / 'graph_bundle.json', 'r') as f:
            bundle = json.load(f)
        pr_topics = [t for t in bundle['nodes']['topics'] if t.get('subcategory') == 'PR']
        if len(pr_topics) > 0:
            assert (output_dir / 'subgraph_pr.json').exists(), \
                "main() should write subgraph_pr.json when PR topics are present"

    def test_entrypoint_writes_timeline_summary(self, fresh_pr_conditional_kg_for_entrypoint: Path, tmp_path: Path):
        """main() should write timeline_summary.json."""
        from unittest.mock import patch
        from pipeline.math_kg_visualization_export import main
        output_dir = tmp_path / 'conditional_viz3'
        output_dir.mkdir()
        with patch('sys.argv', ['math_kg_visualization_export.py',
                                '--input-dir', str(fresh_pr_conditional_kg_for_entrypoint),
                                '--output-dir', str(output_dir)]):
            result = main()
        assert result == 0
        assert (output_dir / 'timeline_summary.json').exists(), "main() should write timeline_summary.json"
        with open(output_dir / 'timeline_summary.json', 'r') as f:
            timeline = json.load(f)
        assert 'timeline' in timeline
        assert len(timeline['timeline']) == 13

    def test_entrypoint_sets_conditional_metadata(self, fresh_pr_conditional_kg_for_entrypoint: Path, tmp_path: Path):
        """main() should set is_conditional=True for pr_conditional input."""
        from unittest.mock import patch
        from pipeline.math_kg_visualization_export import main
        output_dir = tmp_path / 'conditional_viz4'
        output_dir.mkdir()
        # Use a path that contains 'pr_conditional' so is_conditional is set
        import shutil
        pr_input = tmp_path / 'kg_v1_pr_conditional'
        shutil.copytree(str(fresh_pr_conditional_kg_for_entrypoint), str(pr_input))
        with patch('sys.argv', ['math_kg_visualization_export.py',
                                '--input-dir', str(pr_input),
                                '--output-dir', str(output_dir)]):
            result = main()
        assert result == 0
        with open(output_dir / 'graph_bundle.json', 'r') as f:
            bundle = json.load(f)
        assert bundle.get('is_conditional') is True, "Conditional bundle should have is_conditional=True"
        assert bundle.get('conditional_scope') == 'math.PR'

    def test_entrypoint_writes_legend(self, fresh_pr_conditional_kg_for_entrypoint: Path, tmp_path: Path):
        """main() should write legend.json."""
        from unittest.mock import patch
        from pipeline.math_kg_visualization_export import main
        output_dir = tmp_path / 'conditional_viz5'
        output_dir.mkdir()
        with patch('sys.argv', ['math_kg_visualization_export.py',
                                '--input-dir', str(fresh_pr_conditional_kg_for_entrypoint),
                                '--output-dir', str(output_dir)]):
            result = main()
        assert result == 0
        assert (output_dir / 'legend.json').exists(), "main() should write legend.json"
        with open(output_dir / 'legend.json', 'r') as f:
            legend = json.load(f)
        assert 'provisional' in legend.get('evidence_types', {}), "legend should have provisional entry"
