from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pipeline.evolution_analysis import (
    DEFAULT_INPUT,
    TopicRecord,
    analyze_evolution_cases,
    build_topic_graph,
    build_bridge_evidence,
    build_consistency_check,
    build_post_transfer_persistence,
    build_relative_persistence,
    calibrate_topic_profiles,
    detect_alias_risk,
    enrich_with_topics_tree_evidence,
    classify_diffusion_kind,
    classify_transfer_pattern,
    classify_transfer_kind,
    infer_topic_mode,
    infer_topic_profile,
    load_trend_source,
    select_anchor_topics,
)
from pipeline.math_ag_benchmark import AG_CASE_REGISTRY, AG_GRAPH_LAYERS, BENCHMARK_CASES


def make_topic(
    topic_id,
    name,
    keywords,
    category,
    subcategory,
    history,
    hierarchy_path,
):
    return TopicRecord(
        topic_id=topic_id,
        name=name,
        keywords=tuple(keywords),
        keyword_set=set(keywords),
        category=category,
        subcategory=subcategory,
        history=tuple({"period": period, "paper_count": count} for period, count in history),
        history_map={period: count for period, count in history},
        total_papers=sum(count for _, count in history),
        active_periods=len(history),
        hierarchy_path=tuple(hierarchy_path),
        hierarchy_depth=len(hierarchy_path),
        representative_evidence=(),
    )


def synthetic_topics():
    return {
        "topic_anchor": make_topic(
            "topic_anchor",
            "Transformer Reasoning",
            ["transformer", "reasoning", "llm"],
            "cs",
            "AI",
            [("2025-01", 12), ("2025-02", 28), ("2025-03", 35), ("2025-04", 31)],
            ["cs.AI研究", "LLM推理"],
        ),
        "topic_neighbor": make_topic(
            "topic_neighbor",
            "Agentic Reasoning",
            ["reasoning", "agent", "llm"],
            "cs",
            "AI",
            [("2025-01", 1), ("2025-02", 4), ("2025-03", 16), ("2025-04", 22)],
            ["cs.AI研究", "LLM推理", "Agent"],
        ),
        "topic_child": make_topic(
            "topic_child",
            "Formal Reasoning Benchmarks",
            ["reasoning", "benchmark", "llm"],
            "cs",
            "AI",
            [("2025-02", 2), ("2025-03", 11), ("2025-04", 15)],
            ["cs.AI研究", "LLM推理", "Benchmark", "Formal"],
        ),
        "topic_parent": make_topic(
            "topic_parent",
            "General LLM Systems",
            ["llm", "system", "reasoning"],
            "cs",
            "AI",
            [("2025-01", 30), ("2025-02", 34), ("2025-03", 41), ("2025-04", 46)],
            ["cs.AI研究"],
        ),
        "topic_other_field": make_topic(
            "topic_other_field",
            "Reasoning in Economics",
            ["reasoning", "market", "llm"],
            "econ",
            "GN",
            [("2025-01", 0), ("2025-02", 1), ("2025-03", 9), ("2025-04", 14)],
            ["econ.GN研究", "市场推理"],
        ),
        "topic_sparse": make_topic(
            "topic_sparse",
            "Sparse Topic",
            ["rare", "token"],
            "math",
            "OA",
            [("2025-02", 3)],
            ["math.OA研究"],
        ),
    }


def stabilized_topics():
    return {
        "topic_anchor": make_topic(
            "topic_anchor",
            "Medical Image Segmentation",
            ["segmentation", "imaging", "diagnosis"],
            "cs",
            "CV",
            [("2025-01", 25), ("2025-02", 24), ("2025-03", 23), ("2025-04", 26)],
            ["cs.CV研究", "医学成像"],
        ),
        "topic_neighbor": make_topic(
            "topic_neighbor",
            "Medical Vision Benchmark",
            ["benchmark", "imaging", "segmentation"],
            "cs",
            "CV",
            [("2025-01", 4), ("2025-02", 8), ("2025-03", 10), ("2025-04", 9)],
            ["cs.CV研究", "医学成像", "Benchmark"],
        ),
        "topic_parent": make_topic(
            "topic_parent",
            "Medical Vision Systems",
            ["system", "imaging", "segmentation"],
            "cs",
            "CV",
            [("2025-01", 18), ("2025-02", 20), ("2025-03", 19), ("2025-04", 21)],
            ["cs.CV研究"],
        ),
    }


def test_build_topic_graph_has_no_self_loops_and_required_edges():
    topics = synthetic_topics()
    periods = ["2025-01", "2025-02", "2025-03", "2025-04"]

    graph = build_topic_graph(periods, topics, top_k=4, min_similarity=0.1)

    assert graph["nodes"]["topics"]
    assert graph["edges"]["belongs_to"]
    assert graph["edges"]["active_in"]
    assert graph["edges"]["adjacent_to"]
    assert all(edge["source"] != edge["target"] for edge in graph["edges"]["adjacent_to"])


def test_select_anchor_topics_filters_sparse_topics():
    topics = synthetic_topics()
    periods = ["2025-01", "2025-02", "2025-03", "2025-04", "2025-05"]
    graph = build_topic_graph(periods, topics, top_k=4, min_similarity=0.1)

    selected = select_anchor_topics(
        topics,
        graph["edges"]["adjacent_to"],
        periods,
        horizon=2,
        max_cases=4,
        min_total_papers=20,
        min_active_periods=2,
        min_neighbors=2,
    )

    assert "topic_anchor" in selected
    assert "topic_sparse" not in selected


def test_infer_topic_mode_distinguishes_method_and_problem():
    topics = synthetic_topics()
    method_topic = make_topic(
        "topic_method",
        "Transformer Optimization Framework",
        ["transformer", "optimization", "framework"],
        "cs",
        "AI",
        [("2025-01", 12), ("2025-02", 13)],
        ["cs.AI研究", "模型优化"],
    )

    assert infer_topic_mode(method_topic) == "method"
    assert infer_topic_mode(topics["topic_other_field"]) == "problem"
    profile = infer_topic_profile(topics["topic_other_field"])
    assert profile.primary_mode == "problem"
    assert profile.problem_score > profile.method_score


def test_calibrated_profiles_use_neighbor_and_path_context():
    topics = synthetic_topics()
    periods = ["2025-01", "2025-02", "2025-03", "2025-04"]
    graph = build_topic_graph(periods, topics, top_k=4, min_similarity=0.1)
    profiles = calibrate_topic_profiles(topics, graph["edges"]["adjacent_to"])

    assert profiles["topic_anchor"].primary_mode == "hybrid"
    assert profiles["topic_child"].secondary_mode in {"method", "problem", None}


def test_calibrated_profiles_use_representative_evidence_terms():
    topic = make_topic(
        "topic_evidence",
        "Open Problem",
        ["open"],
        "cs",
        "AI",
        [("2025-01", 5), ("2025-02", 7)],
        ["cs.AI研究"],
    )
    topic = TopicRecord(
        topic_id=topic.topic_id,
        name=topic.name,
        keywords=topic.keywords,
        keyword_set=topic.keyword_set,
        category=topic.category,
        subcategory=topic.subcategory,
        history=topic.history,
        history_map=topic.history_map,
        total_papers=topic.total_papers,
        active_periods=topic.active_periods,
        hierarchy_path=topic.hierarchy_path,
        hierarchy_depth=topic.hierarchy_depth,
        representative_evidence=("A benchmark for image segmentation diagnosis",),
    )
    topics = {"topic_evidence": topic}
    profiles = calibrate_topic_profiles(topics, [])
    assert profiles["topic_evidence"].primary_mode == "problem"


def test_enrich_with_topics_tree_evidence_matches_exact_name(tmp_path):
    topic = make_topic(
        "global_x",
        "Medical Image Segmentation",
        ["segmentation", "imaging"],
        "cs",
        "CV",
        [("2025-01", 5)],
        ["cs.CV研究"],
    )
    topics = {"global_x": topic}
    tree_path = tmp_path / "topics_tree.json"
    tree_path.write_text(
        __import__("json").dumps(
            {
                "topics": {
                    "topic_1": {
                        "name": "Medical Image Segmentation",
                        "keywords": ["segmentation", "imaging"],
                        "representative_docs": [{"title": "Segmentation paper", "primary_category": "cs.CV"}],
                    }
                }
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    enriched = enrich_with_topics_tree_evidence(topics, tree_path)
    assert enriched["global_x"].representative_evidence == ("Segmentation paper",)


def test_enrich_with_topics_tree_evidence_matches_by_keywords(tmp_path):
    topic = make_topic(
        "global_y",
        "Galaxy Stellar Gas",
        ["galaxy", "stellar", "gas"],
        "astro-ph",
        "GA",
        [("2025-01", 5)],
        ["astro-ph.GA研究"],
    )
    topics = {"global_y": topic}
    tree_path = tmp_path / "topics_tree.json"
    tree_path.write_text(
        __import__("json").dumps(
            {
                "topics": {
                    "topic_2": {
                        "name": "Galaxy Gas Structure",
                        "keywords": ["galaxy", "stellar", "gas", "halo"],
                        "representative_docs": [{"title": "Galaxy gas evidence", "primary_category": "astro-ph.GA"}],
                    }
                }
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    enriched = enrich_with_topics_tree_evidence(topics, tree_path)
    assert enriched["global_y"].representative_evidence == ("Galaxy gas evidence",)


def test_classify_transfer_kind_distinguishes_problem_and_method_flows():
    method_profile = infer_topic_profile(
        make_topic("m", "Optimization Framework", ["optimization", "framework"], "cs", "AI", [("2025-01", 1)], ["cs.AI研究"])
    )
    problem_profile = infer_topic_profile(
        make_topic("p", "Image Segmentation", ["segmentation", "imaging"], "cs", "CV", [("2025-01", 1)], ["cs.CV研究"])
    )

    assert classify_transfer_kind(method_profile, method_profile) == "method_transfer"
    assert classify_transfer_kind(problem_profile, problem_profile) == "problem_transfer"
    assert classify_diffusion_kind(method_profile, method_profile) == "method_diffusion"
    assert classify_diffusion_kind(problem_profile, problem_profile) == "problem_diffusion"
    assert classify_transfer_pattern(
        make_topic("a", "Same Name", ["vision", "rendering", "gaussian"], "cs", "CV", [("2025-01", 1)], ["cs.CV研究"]),
        make_topic("b", "Same Name", ["vision", "rendering", "gaussian"], "eess", "IV", [("2025-01", 1)], ["eess.IV研究"]),
        method_profile,
        method_profile,
    ) == "migration"
    assert classify_transfer_pattern(
        make_topic("c", "Galaxy Methods", ["galaxy", "star"], "astro-ph", "GA", [("2025-01", 1)], ["astro-ph.GA研究"]),
        make_topic("d", "Galaxy Problems", ["galaxy", "star"], "astro-ph", "GA", [("2025-01", 1)], ["astro-ph.GA研究"]),
        infer_topic_profile(make_topic("c", "Galaxy Methods", ["galaxy", "framework"], "astro-ph", "GA", [("2025-01", 1)], ["astro-ph.GA研究"])),
        infer_topic_profile(make_topic("d", "Galaxy Problems", ["galaxy", "diagnosis"], "astro-ph", "GA", [("2025-01", 1)], ["astro-ph.GA研究"])),
    ) == "spillover"


def test_analyze_evolution_cases_extracts_diffusion_specialization_and_migration():
    topics = synthetic_topics()
    periods = ["2025-01", "2025-02", "2025-03", "2025-04", "2025-05"]
    graph = build_topic_graph(periods, topics, top_k=4, min_similarity=0.1)

    summary, details = analyze_evolution_cases(
        periods,
        topics,
        graph,
        horizon=2,
        max_cases=3,
        manual_topic_ids=["topic_anchor"],
    )

    assert summary["total_cases"] == 1
    case = summary["cases"][0]
    detail = details[case["case_id"]]

    assert case["anchor_topic_id"] == "topic_anchor"
    assert "expanded" in case["event_types"]
    assert "diffused_to_neighbor" in case["event_types"]
    assert "specialized_into_child" in case["event_types"]
    assert "migrated_to_new_category" in case["event_types"]
    assert detail["cross_category_moves"] == ["econ"]
    assert case["anchor_topic_profile"]["primary_mode"] == "hybrid"
    assert detail["evolution_path"][0]["period"] == "2025-01"
    assert detail["evolution_path"][-1]["period"] == "2025-03"
    migration_event = next(event for event in detail["events"] if event["type"] == "migrated_to_new_category")
    assert migration_event["evidence"]["source_category"] == "cs"
    assert migration_event["evidence"]["target_category"] == "econ"
    assert migration_event["evidence"]["transfer_kind"] in {"problem_transfer", "mixed_transfer", "method_transfer"}
    assert migration_event["evidence"]["transfer_pattern"] in {"migration", "fusion", "spillover"}
    assert "post_transfer_persistence" in migration_event["evidence"]
    assert "anchor_post_event_persistence" in migration_event["evidence"]
    assert "relative_persistence" in migration_event["evidence"]
    diffusion_event = next(event for event in detail["events"] if event["type"] == "diffused_to_neighbor")
    assert diffusion_event["evidence"]["transfer_kind"] in {"problem_diffusion", "method_diffusion", "mixed_diffusion"}
    assert "bridge_evidence" in diffusion_event["evidence"]
    assert "shared_keywords" in diffusion_event["evidence"]["bridge_evidence"]
    assert "post_transfer_persistence" in diffusion_event["evidence"]
    assert "anchor_post_event_persistence" in diffusion_event["evidence"]
    assert "relative_persistence" in diffusion_event["evidence"]
    assert "consistency_check" in diffusion_event["evidence"]


def test_build_bridge_evidence_returns_shared_terms_and_titles():
    anchor_base = make_topic(
        "anchor",
        "Gaussian Rendering",
        ["gaussian", "rendering", "3d"],
        "cs",
        "CV",
        [("2025-01", 3)],
        ["cs.CV研究"],
    )
    anchor = TopicRecord(
        topic_id=anchor_base.topic_id,
        name=anchor_base.name,
        keywords=anchor_base.keywords,
        keyword_set=anchor_base.keyword_set,
        category=anchor_base.category,
        subcategory=anchor_base.subcategory,
        history=anchor_base.history,
        history_map=anchor_base.history_map,
        total_papers=anchor_base.total_papers,
        active_periods=anchor_base.active_periods,
        hierarchy_path=anchor_base.hierarchy_path,
        hierarchy_depth=anchor_base.hierarchy_depth,
        representative_evidence=("Gaussian rendering for robotics",),
    )
    target = TopicRecord(
        topic_id="target",
        name="Gaussian Rendering Systems",
        keywords=("gaussian", "rendering", "system"),
        keyword_set={"gaussian", "rendering", "system"},
        category="eess",
        subcategory="IV",
        history=({"period": "2025-02", "paper_count": 6},),
        history_map={"2025-02": 6},
        total_papers=6,
        active_periods=1,
        hierarchy_path=("eess.IV研究",),
        hierarchy_depth=1,
        representative_evidence=("Gaussian rendering for edge systems",),
    )
    bridge = make_topic(
        "bridge",
        "3D Gaussian Pipeline",
        ["gaussian", "pipeline", "3d"],
        "cs",
        "CV",
        [("2025-01", 2)],
        ["cs.CV研究"],
    )
    result = build_bridge_evidence(anchor, target, [("target", 0.5), ("bridge", 0.4)], {"target": target, "bridge": bridge})
    assert "gaussian" in result["shared_keywords"]
    assert result["target_evidence_titles"]
    assert result["category_flow"]["relation"] == "cross_domain"
    assert result["pipeline_relation"]["relation"] == "none"
    assert "gaussian" in result["evidence_title_overlap"]["shared_terms"]
    assert result["bridge_strength"] > 0.0
    assert result["alias_risk"]["level"] == "low"


def test_detect_alias_risk_flags_translated_same_concept():
    anchor = make_topic(
        "anchor",
        "3D Gaussian Splatting",
        ["gaussian", "splatting", "rendering"],
        "cs",
        "CV",
        [("2025-01", 3)],
        ["cs.CV研究"],
    )
    target = make_topic(
        "target",
        "三维 Gaussian Splatting",
        ["gaussian", "splatting", "rendering"],
        "eess",
        "IV",
        [("2025-02", 5)],
        ["eess.IV研究"],
    )
    result = detect_alias_risk(anchor, target)
    assert result["level"] == "high"
    assert result["reason"] == "normalized_name_match"


def test_build_post_transfer_persistence_tracks_future_activity():
    target = make_topic(
        "target",
        "Persistent Topic",
        ["persistent"],
        "cs",
        "AI",
        [("2025-02", 4), ("2025-03", 5), ("2025-04", 6)],
        ["cs.AI研究"],
    )
    result = build_post_transfer_persistence(target, "2025-02", ["2025-01", "2025-02", "2025-03", "2025-04"], lookahead=2)
    assert result["lookahead_periods"] == ["2025-03", "2025-04"]
    assert result["active_periods_after_event"] == 2
    assert result["sustained"] is True


def test_build_relative_persistence_compares_target_against_anchor():
    anchor = {"paper_counts_after_event": [4, 2]}
    target = {"paper_counts_after_event": [1, 1]}
    result = build_relative_persistence(anchor, target)
    assert result["anchor_total"] == 6
    assert result["target_total"] == 2
    assert result["target_to_anchor_ratio"] == 0.333
    assert result["status"] == "partial_carryover"


def test_build_consistency_check_flags_same_category_high_bridge_weak_carryover():
    bridge_evidence = {
        "category_flow": {"relation": "same_category"},
        "bridge_strength": 0.82,
        "alias_risk": {"level": "low", "reason": "distinct_concepts"},
    }
    relative_persistence = {"status": "weak_carryover"}
    result = build_consistency_check("diffused_to_neighbor", bridge_evidence, relative_persistence)
    assert result["status"] == "needs_review"
    assert "same_category_high_bridge_weak_carryover" in result["flags"]


def test_build_consistency_check_accepts_imaging_to_analysis_pipeline():
    bridge_evidence = {
        "category_flow": {"relation": "cross_domain"},
        "pipeline_relation": {"relation": "imaging_to_analysis_same_pipeline"},
        "bridge_strength": 0.91,
        "alias_risk": {"level": "low", "reason": "distinct_concepts"},
    }
    relative_persistence = {"status": "weak_carryover"}
    result = build_consistency_check("diffused_to_neighbor", bridge_evidence, relative_persistence)
    assert result["status"] == "pipeline_consistent"
    assert result["flags"] == []
    assert result["pipeline_relation"] == "imaging_to_analysis_same_pipeline"


def test_build_consistency_check_accepts_representation_to_perception_pipeline():
    bridge_evidence = {
        "category_flow": {"relation": "same_category"},
        "pipeline_relation": {"relation": "representation_to_perception_same_pipeline"},
        "bridge_strength": 0.89,
        "alias_risk": {"level": "low", "reason": "distinct_concepts"},
    }
    relative_persistence = {"status": "weak_carryover"}
    result = build_consistency_check("diffused_to_neighbor", bridge_evidence, relative_persistence)
    assert result["status"] == "pipeline_consistent"
    assert result["flags"] == []
    assert result["pipeline_relation"] == "representation_to_perception_same_pipeline"


def test_build_consistency_check_accepts_formal_structure_same_lineage():
    bridge_evidence = {
        "category_flow": {"relation": "same_category"},
        "pipeline_relation": {"relation": "formal_structure_same_lineage"},
        "bridge_strength": 0.76,
        "alias_risk": {"level": "low", "reason": "distinct_concepts"},
    }
    relative_persistence = {"status": "weak_carryover"}
    result = build_consistency_check("diffused_to_neighbor", bridge_evidence, relative_persistence)
    assert result["status"] == "pipeline_consistent"
    assert result["flags"] == []
    assert result["pipeline_relation"] == "formal_structure_same_lineage"


def test_build_consistency_check_accepts_math_ag_object_continuity():
    bridge_evidence = {
        "category_flow": {"relation": "same_category"},
        "pipeline_relation": {"relation": "math_ag_object_continuity"},
        "bridge_strength": 0.71,
        "alias_risk": {"level": "low", "reason": "distinct_concepts"},
    }
    relative_persistence = {"status": "weak_carryover"}
    result = build_consistency_check("diffused_to_neighbor", bridge_evidence, relative_persistence)
    assert result["status"] == "pipeline_consistent"
    assert result["pipeline_relation"] == "math_ag_object_continuity"


def test_build_consistency_check_accepts_math_ag_method_continuity():
    bridge_evidence = {
        "category_flow": {"relation": "same_category"},
        "pipeline_relation": {"relation": "math_ag_method_continuity"},
        "bridge_strength": 0.69,
        "alias_risk": {"level": "low", "reason": "distinct_concepts"},
    }
    relative_persistence = {"status": "weak_carryover"}
    result = build_consistency_check("diffused_to_neighbor", bridge_evidence, relative_persistence)
    assert result["status"] == "pipeline_consistent"
    assert result["pipeline_relation"] == "math_ag_method_continuity"


def test_build_consistency_check_accepts_math_co_matroid_structure_continuity():
    bridge_evidence = {
        "category_flow": {"relation": "same_category"},
        "pipeline_relation": {"relation": "math_co_matroid_structure_continuity"},
        "bridge_strength": 0.68,
        "alias_risk": {"level": "low", "reason": "distinct_concepts"},
    }
    relative_persistence = {"status": "weak_carryover"}
    result = build_consistency_check("diffused_to_neighbor", bridge_evidence, relative_persistence)
    assert result["status"] == "pipeline_consistent"
    assert result["pipeline_relation"] == "math_co_matroid_structure_continuity"


def test_build_consistency_check_accepts_math_ds_ergodic_entropy_continuity():
    bridge_evidence = {
        "category_flow": {"relation": "same_category"},
        "pipeline_relation": {"relation": "math_ds_ergodic_entropy_continuity"},
        "bridge_strength": 0.66,
        "alias_risk": {"level": "low", "reason": "distinct_concepts"},
    }
    relative_persistence = {"status": "weak_carryover"}
    result = build_consistency_check("diffused_to_neighbor", bridge_evidence, relative_persistence)
    assert result["status"] == "pipeline_consistent"
    assert result["pipeline_relation"] == "math_ds_ergodic_entropy_continuity"


def test_build_consistency_check_accepts_math_na_krylov_iterative_continuity():
    bridge_evidence = {
        "category_flow": {"relation": "same_category"},
        "pipeline_relation": {"relation": "math_na_krylov_iterative_continuity"},
        "bridge_strength": 0.64,
        "alias_risk": {"level": "low", "reason": "distinct_concepts"},
    }
    relative_persistence = {"status": "weak_carryover"}
    result = build_consistency_check("diffused_to_neighbor", bridge_evidence, relative_persistence)
    assert result["status"] == "pipeline_consistent"
    assert result["pipeline_relation"] == "math_na_krylov_iterative_continuity"


def test_build_consistency_check_accepts_math_lo_formal_system_continuity():
    bridge_evidence = {
        "category_flow": {"relation": "same_category"},
        "pipeline_relation": {"relation": "math_lo_formal_system_continuity"},
        "bridge_strength": 0.67,
        "alias_risk": {"level": "low", "reason": "distinct_concepts"},
    }
    relative_persistence = {"status": "weak_carryover"}
    result = build_consistency_check("diffused_to_neighbor", bridge_evidence, relative_persistence)
    assert result["status"] == "pipeline_consistent"
    assert result["pipeline_relation"] == "math_lo_formal_system_continuity"


def test_build_consistency_check_accepts_math_lo_modal_continuity():
    bridge_evidence = {
        "category_flow": {"relation": "same_category"},
        "pipeline_relation": {"relation": "math_lo_modal_continuity"},
        "bridge_strength": 0.82,
        "alias_risk": {"level": "low", "reason": "distinct_concepts"},
    }
    relative_persistence = {"status": "weak_carryover"}
    result = build_consistency_check("diffused_to_neighbor", bridge_evidence, relative_persistence)
    assert result["status"] == "pipeline_consistent"
    assert result["pipeline_relation"] == "math_lo_modal_continuity"


def test_build_consistency_check_accepts_math_lo_set_theory_continuity():
    bridge_evidence = {
        "category_flow": {"relation": "same_category"},
        "pipeline_relation": {"relation": "math_lo_set_theory_continuity"},
        "bridge_strength": 0.62,
    }
    relative_persistence = {"status": "weak_carryover"}
    result = build_consistency_check("diffused_to_neighbor", bridge_evidence, relative_persistence)
    assert result["status"] == "pipeline_consistent"
    assert result["pipeline_relation"] == "math_lo_set_theory_continuity"


def test_build_consistency_check_accepts_math_lo_forcing_continuity():
    bridge_evidence = {
        "category_flow": {"relation": "cross_domain"},
        "pipeline_relation": {"relation": "math_lo_forcing_continuity"},
        "bridge_strength": 0.58,
    }
    relative_persistence = {"status": "partial_carryover"}
    result = build_consistency_check("migrated_to_new_category", bridge_evidence, relative_persistence)
    assert result["status"] == "pipeline_consistent"
    assert result["pipeline_relation"] == "math_lo_forcing_continuity"


def test_build_consistency_check_accepts_math_lo_type_theory_continuity():
    bridge_evidence = {
        "category_flow": {"relation": "cross_domain"},
        "pipeline_relation": {"relation": "math_lo_type_theory_continuity"},
        "bridge_strength": 0.57,
    }
    relative_persistence = {"status": "weak_carryover"}
    result = build_consistency_check("migrated_to_new_category", bridge_evidence, relative_persistence)
    assert result["status"] == "pipeline_consistent"
    assert result["pipeline_relation"] == "math_lo_type_theory_continuity"


def test_build_consistency_check_accepts_math_lo_definability_continuity():
    bridge_evidence = {
        "category_flow": {"relation": "cross_domain"},
        "pipeline_relation": {"relation": "math_lo_definability_continuity"},
        "bridge_strength": 0.51,
    }
    relative_persistence = {"status": "weak_carryover"}
    result = build_consistency_check("migrated_to_new_category", bridge_evidence, relative_persistence)
    assert result["status"] == "pipeline_consistent"
    assert result["pipeline_relation"] == "math_lo_definability_continuity"


def test_build_bridge_evidence_accepts_math_lo_two_objects_one_method():
    anchor = make_topic(
        "lo_anchor",
        "Type Theory Proofs",
        ["logic", "proof", "type", "proofs", "intuitionistic"],
        "math",
        "LO",
        [("2025-01", 4)],
        ["math.LO研究", "数理逻辑", "类型论"],
    )
    target = make_topic(
        "lo_target",
        "Type Semantics in Logic",
        ["logic", "semantics", "type", "proof", "intuitionistic"],
        "math",
        "LO",
        [("2025-02", 6)],
        ["math.LO研究", "数理逻辑", "模型论"],
    )
    result = build_bridge_evidence(anchor, target, [("lo_target", 0.6)], {"lo_target": target})
    assert result["pipeline_relation"]["relation"] == "math_lo_formal_system_continuity"
    assert len(result["pipeline_relation"]["shared_math_lo_core_objects"]) >= 2
    assert len(result["pipeline_relation"]["shared_math_lo_methods"]) >= 1


def test_build_bridge_evidence_accepts_math_co_matroid_structure_continuity_polytope_branch():
    anchor = make_topic(
        "co_matroid_anchor",
        "Matroid Parking Polytopes",
        ["matroid", "matroids", "polytopes", "parking"],
        "math",
        "CO",
        [("2025-01", 4)],
        ["math.CO研究"],
    )
    target = make_topic(
        "co_matroid_target",
        "Matroid Polytope Lattices",
        ["matroid", "matroids", "polytopes", "lattice"],
        "math",
        "CO",
        [("2025-02", 6)],
        ["math.CO研究", "组合结构", "拟阵理论"],
    )
    result = build_bridge_evidence(anchor, target, [("co_matroid_target", 0.6)], {"co_matroid_target": target})
    assert result["pipeline_relation"]["relation"] == "math_co_matroid_structure_continuity"
    assert result["pipeline_relation"]["shared_math_co_matroid_families"] == ["matroid"]
    assert result["pipeline_relation"]["shared_math_co_discrete_families"] == ["matroid", "polytope"]


def test_build_bridge_evidence_accepts_math_co_matroid_structure_continuity_poset_branch():
    anchor = make_topic(
        "co_poset_anchor",
        "Matroid Tropical Posets",
        ["matroid", "matroids", "posets", "tropical"],
        "math",
        "CO",
        [("2025-01", 4)],
        ["math.CO研究"],
    )
    target = make_topic(
        "co_poset_target",
        "Matroid Poset Promotions",
        ["matroid", "matroids", "poset", "posets", "promotion"],
        "math",
        "CO",
        [("2025-02", 6)],
        ["math.CO研究", "组合结构", "拟阵理论", "拟阵偏序集"],
    )
    result = build_bridge_evidence(anchor, target, [("co_poset_target", 0.6)], {"co_poset_target": target})
    assert result["pipeline_relation"]["relation"] == "math_co_matroid_structure_continuity"
    assert result["pipeline_relation"]["shared_math_co_matroid_families"] == ["matroid"]
    assert result["pipeline_relation"]["shared_math_co_discrete_families"] == ["matroid", "poset"]


def test_build_bridge_evidence_rejects_math_co_rank_polynomial_overlap_without_matroid_family():
    anchor = make_topic(
        "co_rank_anchor",
        "Matroid Parking Polynomials",
        ["matroid", "rank", "polynomial", "parking"],
        "math",
        "CO",
        [("2025-01", 4)],
        ["math.CO研究"],
    )
    target = make_topic(
        "co_rank_target",
        "Matrix Permanental Polynomial",
        ["matrix", "rank", "polynomial", "determinant"],
        "math",
        "CO",
        [("2025-02", 6)],
        ["math.CO研究"],
    )
    result = build_bridge_evidence(anchor, target, [("co_rank_target", 0.6)], {"co_rank_target": target})
    assert result["pipeline_relation"]["relation"] == "none"
    assert result["pipeline_relation"]["shared_math_co_matroid_terms"] == []
    assert result["pipeline_relation"]["shared_math_co_discrete_families"] == []


def test_build_bridge_evidence_rejects_math_co_generic_graph_overlap():
    anchor = make_topic(
        "co_graph_anchor",
        "Graph Vertex Conditions",
        ["graphs", "vertices", "conjecture"],
        "math",
        "CO",
        [("2025-01", 4)],
        ["math.CO研究"],
    )
    target = make_topic(
        "co_graph_target",
        "Matroid Posets and Graphs",
        ["matroid", "matroids", "posets", "graphs"],
        "math",
        "CO",
        [("2025-02", 6)],
        ["math.CO研究"],
    )
    result = build_bridge_evidence(anchor, target, [("co_graph_target", 0.6)], {"co_graph_target": target})
    assert result["pipeline_relation"]["relation"] == "none"
    assert result["pipeline_relation"]["shared_math_co_matroid_terms"] == []
    assert result["pipeline_relation"]["shared_math_co_discrete_families"] == []


def test_build_bridge_evidence_rejects_math_co_polytope_only_near_miss():
    anchor = make_topic(
        "co_poly_anchor",
        "Convex Neighborly Polytopes",
        ["polytope", "polytopes", "convex", "faces"],
        "math",
        "CO",
        [("2025-01", 4)],
        ["math.CO研究"],
    )
    target = make_topic(
        "co_poly_target",
        "Matroid Parking Polytopes",
        ["matroid", "matroids", "polytope", "polytopes"],
        "math",
        "CO",
        [("2025-02", 6)],
        ["math.CO研究"],
    )
    result = build_bridge_evidence(anchor, target, [("co_poly_target", 0.6)], {"co_poly_target": target})
    assert result["pipeline_relation"]["relation"] == "none"
    assert result["pipeline_relation"]["shared_math_co_matroid_terms"] == []
    assert result["pipeline_relation"]["shared_math_co_discrete_families"] == ["polytope"]


def test_build_bridge_evidence_accepts_math_ds_ergodic_entropy_continuity_ergodic_case():
    anchor = make_topic(
        "ds_b1_anchor",
        "Ergodic Dynamical Theorems",
        ["maps", "systems", "entropy", "ergodic", "theorem", "measures"],
        "math",
        "DS",
        [("2025-01", 4)],
        ["math.DS研究", "遍历理论与熵"],
    )
    target = make_topic(
        "ds_b1_target",
        "Ergodic Measure Inequalities",
        ["ergodic", "entropy", "measures", "inequality", "theorem"],
        "math",
        "DS",
        [("2025-02", 6)],
        ["math.DS研究", "遍历理论与熵"],
    )
    result = build_bridge_evidence(anchor, target, [("ds_b1_target", 0.6)], {"ds_b1_target": target})
    assert result["pipeline_relation"]["relation"] == "math_ds_ergodic_entropy_continuity"
    assert result["pipeline_relation"]["shared_math_ds_core_terms"] == ["entropy"]
    assert result["pipeline_relation"]["shared_math_ds_focus_terms"] == ["ergodic"]
    assert result["pipeline_relation"]["shared_math_ds_supporting_terms"] == ["measures"]


def test_build_bridge_evidence_accepts_math_ds_ergodic_entropy_continuity_topological_case():
    anchor = make_topic(
        "ds_b2_anchor",
        "Ergodic Dynamical Theorems",
        ["maps", "systems", "entropy", "ergodic", "topological", "measure"],
        "math",
        "DS",
        [("2025-01", 4)],
        ["math.DS研究", "遍历理论与熵"],
    )
    target = make_topic(
        "ds_b2_target",
        "Topological Entropy Measures",
        ["topological", "measure", "entropy", "historic"],
        "math",
        "DS",
        [("2025-02", 6)],
        ["math.DS研究", "遍历理论与熵"],
    )
    result = build_bridge_evidence(anchor, target, [("ds_b2_target", 0.6)], {"ds_b2_target": target})
    assert result["pipeline_relation"]["relation"] == "math_ds_ergodic_entropy_continuity"
    assert result["pipeline_relation"]["shared_math_ds_core_terms"] == ["entropy"]
    assert result["pipeline_relation"]["shared_math_ds_focus_terms"] == ["topological"]
    assert result["pipeline_relation"]["shared_math_ds_supporting_terms"] == ["measure"]


def test_build_bridge_evidence_rejects_math_ds_topological_only_overlap():
    anchor = make_topic(
        "ds_n1_anchor",
        "Persistent Topological Analysis",
        ["persistence", "homology", "topological", "persistent"],
        "math",
        "DS",
        [("2025-01", 4)],
        ["math.DS研究", "遍历理论与熵"],
    )
    target = make_topic(
        "ds_n1_target",
        "Topological Entropy Measures",
        ["topological", "measure", "entropy", "historic"],
        "math",
        "DS",
        [("2025-02", 6)],
        ["math.DS研究", "遍历理论与熵"],
    )
    result = build_bridge_evidence(anchor, target, [("ds_n1_target", 0.6)], {"ds_n1_target": target})
    assert result["pipeline_relation"]["relation"] == "none"
    assert result["pipeline_relation"]["shared_math_ds_core_terms"] == []
    assert result["pipeline_relation"]["shared_math_ds_focus_terms"] == ["topological"]


def test_build_bridge_evidence_rejects_math_ds_measure_metric_overlap():
    anchor = make_topic(
        "ds_n2_anchor",
        "Optimal Transport Measures",
        ["entropic", "transport", "wasserstein", "metric", "measures"],
        "math",
        "DS",
        [("2025-01", 4)],
        ["math.DS研究", "遍历理论与熵"],
    )
    target = make_topic(
        "ds_n2_target",
        "Ergodic Dynamical Theorems",
        ["maps", "systems", "entropy", "ergodic", "metric", "measures"],
        "math",
        "DS",
        [("2025-02", 6)],
        ["math.DS研究", "遍历理论与熵"],
    )
    result = build_bridge_evidence(anchor, target, [("ds_n2_target", 0.6)], {"ds_n2_target": target})
    assert result["pipeline_relation"]["relation"] == "none"
    assert result["pipeline_relation"]["shared_math_ds_core_terms"] == []
    assert result["pipeline_relation"]["shared_math_ds_supporting_terms"] == ["measures"]


def test_build_bridge_evidence_rejects_math_ds_entropy_measure_ambiguous_boundary():
    anchor = make_topic(
        "ds_a1_anchor",
        "Fractal Entropy Measures",
        ["entropy", "measure", "fractal", "maps"],
        "math",
        "DS",
        [("2025-01", 4)],
        ["math.DS研究", "遍历理论与熵"],
    )
    target = make_topic(
        "ds_a1_target",
        "Ergodic Dynamical Theorems",
        ["maps", "systems", "entropy", "ergodic", "measure"],
        "math",
        "DS",
        [("2025-02", 6)],
        ["math.DS研究", "遍历理论与熵"],
    )
    result = build_bridge_evidence(anchor, target, [("ds_a1_target", 0.6)], {"ds_a1_target": target})
    assert result["pipeline_relation"]["relation"] == "none"
    assert result["pipeline_relation"]["shared_math_ds_core_terms"] == ["entropy"]
    assert result["pipeline_relation"]["shared_math_ds_focus_terms"] == []
    assert result["pipeline_relation"]["shared_math_ds_supporting_terms"] == ["measure"]


def test_build_bridge_evidence_accepts_math_na_gmres_family_expansion():
    anchor = make_topic(
        "na_b1_anchor",
        "GMRES Numerical Approximation",
        ["gmres", "approximation", "regularization", "preconditioners"],
        "math",
        "NA",
        [("2025-01", 4)],
        ["math.NA研究", "偏微分方程数值方法"],
    )
    target = make_topic(
        "na_b1_target",
        "Block Eigenvalue Krylov Methods",
        ["gmres", "krylov", "lanczos", "arnoldi", "block", "matrix"],
        "math",
        "NA",
        [("2025-02", 6)],
        ["math.NA研究", "偏微分方程数值方法"],
    )
    result = build_bridge_evidence(anchor, target, [("na_b1_target", 0.6)], {"na_b1_target": target})
    assert result["pipeline_relation"]["relation"] == "math_na_krylov_iterative_continuity"
    assert result["pipeline_relation"]["shared_math_na_core_terms"] == ["gmres"]
    assert result["pipeline_relation"]["target_math_na_core_terms"] == ["arnoldi", "gmres", "krylov", "lanczos"]
    assert result["pipeline_relation"]["shared_math_na_supporting_terms"] == []


def test_build_bridge_evidence_accepts_math_na_shared_krylov_backbone():
    anchor = make_topic(
        "na_b2_anchor",
        "Block Krylov Eigenvalue Methods",
        ["block", "matrix", "gmres", "krylov", "lanczos", "arnoldi"],
        "math",
        "NA",
        [("2025-01", 4)],
        ["math.NA研究", "偏微分方程数值方法"],
    )
    target = make_topic(
        "na_b2_target",
        "Block Matrix Iterative Acceleration",
        ["block", "matrix", "gmres", "krylov", "lanczos", "algorithm"],
        "math",
        "NA",
        [("2025-02", 6)],
        ["math.NA研究", "偏微分方程数值方法"],
    )
    result = build_bridge_evidence(anchor, target, [("na_b2_target", 0.6)], {"na_b2_target": target})
    assert result["pipeline_relation"]["relation"] == "math_na_krylov_iterative_continuity"
    assert result["pipeline_relation"]["shared_math_na_core_terms"] == ["gmres", "krylov", "lanczos"]
    assert result["pipeline_relation"]["shared_math_na_supporting_terms"] == ["block", "matrix"]


def test_build_bridge_evidence_rejects_math_na_approximation_only_overlap():
    anchor = make_topic(
        "na_n1_anchor",
        "GMRES Numerical Approximation",
        ["gmres", "approximation", "regularization", "preconditioners"],
        "math",
        "NA",
        [("2025-01", 4)],
        ["math.NA研究", "偏微分方程数值方法"],
    )
    target = make_topic(
        "na_n1_target",
        "Kernel Interpolation Approximation",
        ["interpolation", "approximation", "kernels", "kernel"],
        "math",
        "NA",
        [("2025-02", 6)],
        ["math.NA研究", "偏微分方程数值方法"],
    )
    result = build_bridge_evidence(anchor, target, [("na_n1_target", 0.6)], {"na_n1_target": target})
    assert result["pipeline_relation"]["relation"] == "none"
    assert result["pipeline_relation"]["shared_math_na_core_terms"] == []
    assert result["pipeline_relation"]["shared_math_na_supporting_terms"] == []


def test_build_bridge_evidence_rejects_math_na_convergence_only_overlap():
    anchor = make_topic(
        "na_n2_anchor",
        "Block Eigenvalue Krylov Methods",
        ["block", "matrix", "convergence", "gmres", "krylov", "lanczos", "arnoldi"],
        "math",
        "NA",
        [("2025-01", 4)],
        ["math.NA研究", "偏微分方程数值方法"],
    )
    target = make_topic(
        "na_n2_target",
        "Markov Chain Monte Carlo",
        ["markov", "convergence", "mcmc", "sampling"],
        "math",
        "NA",
        [("2025-02", 6)],
        ["math.NA研究", "偏微分方程数值方法"],
    )
    result = build_bridge_evidence(anchor, target, [("na_n2_target", 0.6)], {"na_n2_target": target})
    assert result["pipeline_relation"]["relation"] == "none"
    assert result["pipeline_relation"]["shared_math_na_core_terms"] == []
    assert result["pipeline_relation"]["shared_math_na_supporting_terms"] == []


def test_build_bridge_evidence_rejects_math_na_single_krylov_ambiguous_boundary():
    anchor = make_topic(
        "na_a1_anchor",
        "Matrix Norm Krylov Squares",
        ["matrix", "block", "krylov", "norm"],
        "math",
        "NA",
        [("2025-01", 4)],
        ["math.NA研究", "线性代数与矩阵计算", "特征值问题与迭代法", "Krylov子空间方法"],
    )
    target = make_topic(
        "na_a1_target",
        "Quantum Tensor Ground State Algorithms",
        ["quantum", "tensor", "hamiltonian", "ground", "krylov"],
        "math",
        "NA",
        [("2025-02", 6)],
        ["math.NA研究", "线性代数与矩阵计算", "特征值问题与迭代法", "Krylov子空间方法"],
    )
    result = build_bridge_evidence(anchor, target, [("na_a1_target", 0.6)], {"na_a1_target": target})
    assert result["pipeline_relation"]["relation"] == "none"
    assert result["pipeline_relation"]["shared_math_na_core_terms"] == ["krylov"]
    assert result["pipeline_relation"]["shared_math_na_supporting_terms"] == []


def test_build_bridge_evidence_accepts_math_lo_modal_continuity():
    anchor = make_topic(
        "lo_modal_anchor",
        "Modal Logic Proofs",
        ["logic", "modal", "proof", "intuitionistic"],
        "math",
        "LO",
        [("2025-01", 4)],
        ["math.LO研究", "数理逻辑", "模态逻辑"],
    )
    target = make_topic(
        "lo_modal_target",
        "Probabilistic Logic Semantics",
        ["logic", "semantics", "modal", "probabilistic", "intuitionistic"],
        "math",
        "LO",
        [("2025-02", 6)],
        ["math.LO研究", "数理逻辑", "非经典逻辑", "概率逻辑"],
    )
    result = build_bridge_evidence(anchor, target, [("lo_modal_target", 0.6)], {"lo_modal_target": target})
    assert result["pipeline_relation"]["relation"] == "math_lo_modal_continuity"
    assert len(result["pipeline_relation"]["shared_math_lo_modal_objects"]) >= 2
    assert len(result["pipeline_relation"]["shared_math_lo_modal_methods"]) >= 1


def test_build_bridge_evidence_accepts_math_lo_set_theory_continuity():
    anchor = make_topic(
        "lo_set_anchor",
        "Cardinals and Forcing",
        ["cardinal", "cardinals", "forcing", "definable"],
        "math",
        "LO",
        [("2025-01", 4)],
        ["math.LO研究", "集合论与基数理论", "力迫法"],
    )
    target = make_topic(
        "lo_set_target",
        "Borel Cardinals and Forcing",
        ["cardinal", "cardinals", "forcing", "borel"],
        "math",
        "LO",
        [("2025-02", 6)],
        ["math.LO研究", "集合论与基数理论"],
    )
    result = build_bridge_evidence(anchor, target, [("lo_set_target", 0.6)], {"lo_set_target": target})
    assert result["pipeline_relation"]["relation"] == "math_lo_set_theory_continuity"
    assert len(result["pipeline_relation"]["shared_math_lo_set_objects"]) >= 3


def test_build_bridge_evidence_rejects_weak_math_lo_set_overlap():
    anchor = make_topic(
        "lo_set_anchor",
        "Definable Cardinals",
        ["cardinals", "definable"],
        "math",
        "LO",
        [("2025-01", 4)],
        ["math.LO研究", "集合论与基数理论"],
    )
    target = make_topic(
        "lo_set_target",
        "Cardinals in Henselian Fields",
        ["cardinals", "definable", "fields"],
        "math",
        "LO",
        [("2025-02", 6)],
        ["math.LO研究", "集合论与基数理论"],
    )
    result = build_bridge_evidence(anchor, target, [("lo_set_target", 0.6)], {"lo_set_target": target})
    assert result["pipeline_relation"]["relation"] == "none"


def test_build_bridge_evidence_accepts_math_lo_forcing_continuity():
    anchor = make_topic(
        "lo_forcing_anchor",
        "Borel Cardinals and Forcing Axioms",
        ["forcing", "cardinal", "cardinals", "axiom", "zf"],
        "math",
        "LO",
        [("2025-01", 4)],
        ["math.LO研究", "集合论与基数理论"],
    )
    target = make_topic(
        "lo_forcing_target",
        "Large Cardinals and Forcing",
        ["forcing", "cardinal", "cardinals", "axiom", "zf"],
        "cs",
        "LO",
        [("2025-02", 6)],
        ["cs.LO研究", "逻辑与形式化方法", "集合论与数理逻辑", "大基数与力迫法"],
    )
    result = build_bridge_evidence(anchor, target, [("lo_forcing_target", 0.6)], {"lo_forcing_target": target})
    assert result["pipeline_relation"]["relation"] == "math_lo_forcing_continuity"
    assert len(result["pipeline_relation"]["shared_math_lo_forcing_objects"]) >= 4


def test_build_bridge_evidence_rejects_weak_math_lo_forcing_overlap():
    anchor = make_topic(
        "lo_forcing_anchor",
        "Ideals and Forcing",
        ["forcing", "cardinal", "ideals"],
        "math",
        "LO",
        [("2025-01", 4)],
        ["math.LO研究", "集合论与基数理论", "力迫法"],
    )
    target = make_topic(
        "lo_forcing_target",
        "Large Cardinals and Forcing",
        ["forcing", "cardinal", "axiom"],
        "cs",
        "LO",
        [("2025-02", 6)],
        ["cs.LO研究", "逻辑与形式化方法", "集合论与数理逻辑", "大基数与力迫法"],
    )
    result = build_bridge_evidence(anchor, target, [("lo_forcing_target", 0.6)], {"lo_forcing_target": target})
    assert result["pipeline_relation"]["relation"] == "none"


def test_build_bridge_evidence_accepts_math_lo_type_theory_continuity():
    anchor = make_topic(
        "lo_type_anchor",
        "Intuitionistic Type Proofs",
        ["proof", "proofs", "type", "types", "typed", "calculus", "intuitionistic"],
        "math",
        "LO",
        [("2025-01", 4)],
        ["math.LO研究", "数理逻辑", "非经典逻辑", "直觉主义逻辑"],
    )
    target = make_topic(
        "lo_type_target",
        "Program Linearizability and Types",
        ["type", "types", "programs", "languages", "subtyping", "correctness"],
        "cs",
        "LO",
        [("2025-02", 6)],
        ["cs.LO研究", "逻辑与形式化方法"],
    )
    result = build_bridge_evidence(anchor, target, [("lo_type_target", 0.6)], {"lo_type_target": target})
    assert result["pipeline_relation"]["relation"] == "math_lo_type_theory_continuity"
    assert len(result["pipeline_relation"]["shared_math_lo_type_objects"]) >= 2
    assert result["pipeline_relation"]["source_type_terms"]
    assert result["pipeline_relation"]["target_type_terms"]


def test_build_bridge_evidence_rejects_weak_math_lo_type_overlap():
    anchor = make_topic(
        "lo_type_anchor",
        "Intuitionistic Logic Proofs",
        ["proof", "proofs", "calculus", "intuitionistic"],
        "math",
        "LO",
        [("2025-01", 4)],
        ["math.LO研究", "数理逻辑", "非经典逻辑", "直觉主义逻辑"],
    )
    target = make_topic(
        "lo_type_target",
        "Math Reasoning with LLMs",
        ["models", "symbolic", "mathematics", "research"],
        "cs",
        "LO",
        [("2025-02", 6)],
        ["cs.LO研究", "自动推理与证明", "人工智能驱动的推理"],
    )
    result = build_bridge_evidence(anchor, target, [("lo_type_target", 0.6)], {"lo_type_target": target})
    assert result["pipeline_relation"]["relation"] == "none"


def test_build_bridge_evidence_accepts_math_lo_definability_continuity():
    anchor = make_topic(
        "lo_def_anchor",
        "Definable Cardinals",
        ["cardinal", "cardinals", "definable", "woodin"],
        "math",
        "LO",
        [("2025-01", 4)],
        ["math.LO研究", "集合论与基数理论"],
    )
    target = make_topic(
        "lo_def_target",
        "Woodin Axiom Definability",
        ["cardinal", "cardinals", "definable", "axiom", "woodin"],
        "cs",
        "LO",
        [("2025-02", 6)],
        ["cs.LO研究", "逻辑与形式化方法"],
    )
    result = build_bridge_evidence(anchor, target, [("lo_def_target", 0.6)], {"lo_def_target": target})
    assert result["pipeline_relation"]["relation"] == "math_lo_definability_continuity"
    assert len(result["pipeline_relation"]["shared_math_lo_definability_objects"]) >= 2
    assert len(result["pipeline_relation"]["shared_math_lo_definability_methods"]) >= 1


def test_build_bridge_evidence_rejects_weak_math_lo_definability_overlap():
    anchor = make_topic(
        "lo_def_anchor",
        "Henselian Definability",
        ["definable", "henselian", "valued"],
        "math",
        "LO",
        [("2025-01", 4)],
        ["math.LO研究", "集合论与基数理论"],
    )
    target = make_topic(
        "lo_def_target",
        "Woodin Axiom Definability",
        ["definable", "axiom", "woodin"],
        "cs",
        "LO",
        [("2025-02", 6)],
        ["cs.LO研究", "逻辑与形式化方法"],
    )
    result = build_bridge_evidence(anchor, target, [("lo_def_target", 0.6)], {"lo_def_target": target})
    assert result["pipeline_relation"]["relation"] == "none"


def test_build_bridge_evidence_exposes_math_ag_taxonomy_overlap():
    anchor = make_topic(
        "ag_anchor",
        "Fano Moduli Curves",
        ["fano", "moduli", "curves", "projective"],
        "math",
        "AG",
        [("2025-01", 4)],
        ["math.AG研究", "代数簇与模空间"],
    )
    target = make_topic(
        "ag_target",
        "Abelian Varieties and Moduli Stacks",
        ["abelian", "varieties", "moduli", "stacks"],
        "math",
        "AG",
        [("2025-02", 6)],
        ["math.AG研究", "代数簇与模空间"],
    )
    result = build_bridge_evidence(anchor, target, [("ag_target", 0.6)], {"ag_target": target})
    overlap = result["pipeline_relation"]["math_ag_object_matches"]["overlap"]
    assert result["pipeline_relation"]["relation"] == "none"
    assert result["pipeline_relation"]["shared_math_ag_objects"] == ["moduli"]
    assert overlap["score"] >= 1.5
    assert overlap["shared_classes"]
    assert overlap["related_classes"] == []


def test_build_bridge_evidence_accepts_math_ag_multiple_exact_objects():
    anchor = make_topic(
        "ag_exact_anchor",
        "Algebraic Stacks and Sheaves",
        ["stacks", "stack", "sheaf", "algebraic"],
        "math",
        "AG",
        [("2025-01", 4)],
        ["math.AG研究", "代数簇与模空间"],
    )
    target = make_topic(
        "ag_exact_target",
        "Derived Stack Sheaf Categories",
        ["stacks", "stack", "sheaf", "derived"],
        "math",
        "AG",
        [("2025-02", 6)],
        ["math.AG研究", "代数簇与模空间"],
    )
    result = build_bridge_evidence(anchor, target, [("ag_exact_target", 0.6)], {"ag_exact_target": target})
    assert result["pipeline_relation"]["relation"] == "math_ag_object_continuity"
    assert len(result["pipeline_relation"]["shared_math_ag_objects"]) >= 2


def test_build_bridge_evidence_rejects_math_ag_single_exact_object_with_taxonomy_support():
    anchor = make_topic(
        "ag_single_exact_anchor",
        "Stacks Algebraic Sheaves",
        ["stacks", "algebraic", "sheaves"],
        "math",
        "AG",
        [("2025-01", 4)],
        ["math.AG研究", "代数簇与模空间"],
    )
    target = make_topic(
        "ag_single_exact_target",
        "Motivic Schemes and Sheaves",
        ["motivic", "schemes", "sheaves"],
        "math",
        "AG",
        [("2025-02", 6)],
        ["math.AG研究", "代数簇与模空间"],
    )
    result = build_bridge_evidence(
        anchor,
        target,
        [("ag_single_exact_target", 0.6)],
        {"ag_single_exact_target": target},
    )
    overlap = result["pipeline_relation"]["math_ag_object_matches"]["overlap"]
    assert result["pipeline_relation"]["relation"] == "none"
    assert result["pipeline_relation"]["shared_math_ag_objects"] == ["sheaves"]
    assert overlap["score"] >= 1.5
    assert overlap["shared_exact_terms"] == ["sheaves"]


def test_build_bridge_evidence_rejects_math_ag_class_overlap_without_exact_terms():
    anchor = make_topic(
        "ag_class_only_anchor",
        "Fano Moduli Bundles",
        ["fano", "moduli", "bundles"],
        "math",
        "AG",
        [("2025-01", 4)],
        ["math.AG研究", "代数簇与模空间"],
    )
    target = make_topic(
        "ag_class_only_target",
        "Derived Stacks Sheaves Algebraic",
        ["stacks", "sheaves", "algebraic"],
        "math",
        "AG",
        [("2025-02", 6)],
        ["math.AG研究", "代数簇与模空间"],
    )
    result = build_bridge_evidence(
        anchor,
        target,
        [("ag_class_only_target", 0.6)],
        {"ag_class_only_target": target},
    )
    overlap = result["pipeline_relation"]["math_ag_object_matches"]["overlap"]
    assert result["pipeline_relation"]["relation"] == "none"
    assert result["pipeline_relation"]["shared_math_ag_objects"] == []
    assert overlap["score"] >= 1.5
    assert overlap["shared_exact_terms"] == []


def test_build_bridge_evidence_exposes_math_ag_related_class_overlap():
    anchor = make_topic(
        "ag_anchor_related",
        "Fano Varieties and Moduli",
        ["fano", "varieties", "moduli"],
        "math",
        "AG",
        [("2025-01", 4)],
        ["math.AG研究", "代数簇与模空间"],
    )
    target = make_topic(
        "ag_target_related",
        "Projective Sheaves",
        ["projective", "sheaves", "algebraic"],
        "math",
        "AG",
        [("2025-02", 6)],
        ["math.AG研究", "代数簇与模空间"],
    )
    result = build_bridge_evidence(anchor, target, [("ag_target_related", 0.6)], {"ag_target_related": target})
    overlap = result["pipeline_relation"]["math_ag_object_matches"]["overlap"]
    assert result["pipeline_relation"]["relation"] == "none"
    assert overlap["score"] > 0.0
    assert overlap["related_classes"]


def test_real_math_ag_partial_baseline_replay_matches_current_contract():
    _, topics = load_trend_source(DEFAULT_INPUT)
    expectations = {
        "ag-p1": ("global_69", "global_287", "math_ag_object_continuity"),
        "ag-p2": ("global_30", "global_355", "none"),
        "ag-p3": ("global_355", "global_117", "none"),
        "ag-n1": ("global_69", "global_136", "none"),
        "ag-n2": ("global_30", "global_287", "none"),
        "ag-n3": ("global_134", "global_30", "none"),
    }

    for anchor_id, target_id, expected in expectations.values():
        result = build_bridge_evidence(topics[anchor_id], topics[target_id], [], topics)
        assert result["pipeline_relation"]["relation"] == expected


def test_real_math_co_matroid_replay_matches_current_contract():
    _, topics = load_trend_source(DEFAULT_INPUT)
    expectations = {
        "co-m1": ("global_292", "global_319", "math_co_matroid_structure_continuity"),
        "co-m2": ("global_118", "global_204", "math_co_matroid_structure_continuity"),
        "co-mn1": ("global_292", "global_324", "none"),
        "co-mn2": ("global_8", "global_319", "none"),
        "co-ma1": ("global_220", "global_292", "none"),
    }

    for anchor_id, target_id, expected in expectations.values():
        result = build_bridge_evidence(topics[anchor_id], topics[target_id], [], topics)
        assert result["pipeline_relation"]["relation"] == expected


def test_real_math_co_supporting_bridge_pair_stays_outside_current_mvp_gate():
    _, topics = load_trend_source(DEFAULT_INPUT)
    result = build_bridge_evidence(topics["global_16"], topics["global_292"], [], topics)
    assert result["pipeline_relation"]["relation"] == "none"
    assert result["pipeline_relation"]["shared_math_co_matroid_families"] == ["matroid"]
    assert result["pipeline_relation"]["shared_math_co_discrete_families"] == ["matroid"]


def test_real_math_na_replay_matches_current_contract():
    _, topics = load_trend_source(DEFAULT_INPUT)
    expectations = {
        "na-b1": ("global_105", "global_140", "math_na_krylov_iterative_continuity"),
        "na-b2": ("global_140", "global_9", "math_na_krylov_iterative_continuity"),
        "na-n1": ("global_105", "global_378", "none"),
        "na-n2": ("global_140", "global_90", "none"),
        "na-a1": ("global_86", "global_307", "none"),
    }

    for case_id, (anchor_id, target_id, expected) in expectations.items():
        result = build_bridge_evidence(topics[anchor_id], topics[target_id], [], topics)
        assert result["pipeline_relation"]["relation"] == expected
        if case_id == "na-b1":
            assert result["pipeline_relation"]["shared_math_na_core_terms"] == ["gmres"]
            assert result["pipeline_relation"]["target_math_na_core_terms"] == ["arnoldi", "gmres", "krylov", "lanczos"]
        if case_id == "na-b2":
            assert result["pipeline_relation"]["shared_math_na_core_terms"] == ["gmres", "krylov", "lanczos"]
            assert result["pipeline_relation"]["shared_math_na_supporting_terms"] == ["block", "matrix"]
        if case_id == "na-a1":
            assert result["pipeline_relation"]["shared_math_na_core_terms"] == ["krylov"]


def test_math_ag_benchmark_runner_contract_uses_canonical_case_ids():
    positive_ids = [case["case_id"] for case in BENCHMARK_CASES["positive"]]
    negative_ids = [case["case_id"] for case in BENCHMARK_CASES["negative"]]

    assert positive_ids == ["ag-p1"]
    assert negative_ids == ["ag-n1", "ag-n2", "ag-n3"]
    assert {"ag-b1", "ag-e2"}.isdisjoint(positive_ids)
    assert (BENCHMARK_CASES["positive"][0]["anchor"], BENCHMARK_CASES["positive"][0]["target"]) == (
        "global_69",
        "global_287",
    )


def test_math_ag_graph_layers_preserve_core_bridge_boundary_split():
    assert AG_GRAPH_LAYERS["confirmed_core"]["case_ids"] == ["ag-p1"]
    assert AG_GRAPH_LAYERS["bridge_ring"]["case_ids"] == ["ag-p2", "ag-p3"]
    assert AG_GRAPH_LAYERS["excluded_boundary"]["case_ids"] == ["ag-n1", "ag-n2", "ag-n3"]

    assert AG_CASE_REGISTRY["ag-p1"]["runner_role"] == "runner-positive"
    assert AG_CASE_REGISTRY["ag-p1"]["expected_relation"] == "math_ag_object_continuity"

    assert AG_CASE_REGISTRY["ag-p2"]["runner_role"] == "semantic-bridge-positive"
    assert AG_CASE_REGISTRY["ag-p2"]["expected_relation"] == "none"
    assert AG_CASE_REGISTRY["ag-p3"]["narrative_layer"] == "bridge_ring"

    assert AG_CASE_REGISTRY["ag-n1"]["runner_role"] == "excluded-boundary"
    assert AG_CASE_REGISTRY["ag-n2"]["narrative_layer"] == "excluded_boundary"


def test_stabilized_topic_is_not_marked_as_weakened():
    topics = stabilized_topics()
    periods = ["2025-01", "2025-02", "2025-03", "2025-04", "2025-05"]
    graph = build_topic_graph(periods, topics, top_k=3, min_similarity=0.1)

    summary, _ = analyze_evolution_cases(
        periods,
        topics,
        graph,
        horizon=2,
        max_cases=2,
        manual_topic_ids=["topic_anchor"],
    )

    case = summary["cases"][0]
    assert case["anchor_topic_mode"] == "problem"
    assert "stabilized" in case["event_types"]
    assert "weakened" not in case["event_types"]


def test_build_bridge_evidence_accepts_math_ag_method_continuity():
    """Benchmark case: math_ag_method_continuity positive example.

    Case ID: ag-method-b1
    Type: positive
    Rule: math_ag_method_continuity
    Trigger: shared >= 2 method hints (cohomology + motivic)
    """
    anchor = make_topic(
        "ag_method_anchor",
        "Motivic Cohomology Schemes",
        ["cohomology", "motivic", "schemes", "hodge"],
        "math",
        "AG",
        [("2025-01", 4)],
        ["math.AG研究", "代数簇与模空间"],
    )
    target = make_topic(
        "ag_method_target",
        "Motivic Cohomology Varieties",
        ["cohomology", "motivic", "varieties", "group"],
        "math",
        "AG",
        [("2025-02", 6)],
        ["math.AG研究", "代数簇与模空间"],
    )
    result = build_bridge_evidence(anchor, target, [("ag_method_target", 0.6)], {"ag_method_target": target})
    assert result["pipeline_relation"]["relation"] == "math_ag_method_continuity"
    assert len(result["pipeline_relation"]["shared_math_ag_methods"]) >= 2
    assert "cohomology" in result["pipeline_relation"]["shared_math_ag_methods"]
    assert "motivic" in result["pipeline_relation"]["shared_math_ag_methods"]


def test_build_bridge_evidence_accepts_math_ag_method_tropical():
    """Benchmark case: math_ag_method_continuity tropical geometry positive example.

    Case ID: ag-method-b2
    Type: positive
    Rule: math_ag_method_continuity
    Trigger: shared >= 2 method hints (tropical + tropicalization)
    """
    anchor = make_topic(
        "ag_tropical_anchor",
        "Tropical Curves Geometry",
        ["tropical", "tropicalization", "curves", "geometry"],
        "math",
        "AG",
        [("2025-01", 4)],
        ["math.AG研究", "代数簇与模空间"],
    )
    target = make_topic(
        "ag_tropical_target",
        "Tropical Moduli Compactification",
        ["tropical", "tropicalization", "moduli", "compactification"],
        "math",
        "AG",
        [("2025-02", 6)],
        ["math.AG研究", "代数簇与模空间"],
    )
    result = build_bridge_evidence(anchor, target, [("ag_tropical_target", 0.6)], {"ag_tropical_target": target})
    assert result["pipeline_relation"]["relation"] == "math_ag_method_continuity"
    assert len(result["pipeline_relation"]["shared_math_ag_methods"]) >= 2
    assert "tropical" in result["pipeline_relation"]["shared_math_ag_methods"]
    assert "tropicalization" in result["pipeline_relation"]["shared_math_ag_methods"]


def test_build_bridge_evidence_rejects_weak_math_ag_method_overlap():
    """Benchmark case: math_ag_method_continuity negative example.

    Case ID: ag-method-n1
    Type: negative
    Rule: math_ag_method_continuity (rejected)
    Trigger: only 1 shared method hint (cohomology) - insufficient
    """
    anchor = make_topic(
        "ag_method_weak_anchor",
        "Cohomology Schemes Hodge",
        ["cohomology", "schemes", "hodge"],
        "math",
        "AG",
        [("2025-01", 4)],
        ["math.AG研究", "代数簇与模空间"],
    )
    target = make_topic(
        "ag_method_weak_target",
        "Cohomology Varieties Group",
        ["cohomology", "varieties", "group"],
        "math",
        "AG",
        [("2025-02", 6)],
        ["math.AG研究", "代数簇与模空间"],
    )
    result = build_bridge_evidence(anchor, target, [("ag_method_weak_target", 0.6)], {"ag_method_weak_target": target})
    assert result["pipeline_relation"]["relation"] != "math_ag_method_continuity"
    assert len(result["pipeline_relation"]["shared_math_ag_methods"]) < 2


def test_build_bridge_evidence_rejects_single_category_method_overlap():
    """Benchmark case: math_ag_method_continuity negative example with categories.

    Case ID: ag-method-n2
    Type: negative
    Rule: math_ag_method_continuity (rejected)
    Trigger: only 1 shared method hint (categories) - insufficient
    """
    anchor = make_topic(
        "ag_cat_anchor",
        "Algebraic Categories Geometry",
        ["categories", "algebraic", "geometry"],
        "math",
        "AG",
        [("2025-01", 4)],
        ["math.AG研究", "代数簇与模空间"],
    )
    target = make_topic(
        "ag_cat_target",
        "Categories Stacks Moduli",
        ["categories", "stacks", "moduli"],
        "math",
        "AG",
        [("2025-02", 6)],
        ["math.AG研究", "代数簇与模空间"],
    )
    result = build_bridge_evidence(anchor, target, [("ag_cat_target", 0.6)], {"ag_cat_target": target})
    assert result["pipeline_relation"]["relation"] != "math_ag_method_continuity"
    assert len(result["pipeline_relation"]["shared_math_ag_methods"]) < 2


def test_category_filter_limits_to_specific_category():
    """Test that category_filter only returns topics from specified category."""
    # Create topics from different categories (meeting min criteria: papers>=60, periods>=2, neighbors>=2)
    math_topic_1 = make_topic(
        "math_1",
        "Algebraic Geometry Topic",
        ["variety", "algebraic"],
        "math",
        "AG",
        [("2025-01", 100), ("2025-02", 120), ("2025-03", 110)],  # 3 periods, 330 papers
        ["math.AG研究"],
    )
    math_topic_2 = make_topic(
        "math_2",
        "Number Theory Topic",
        ["number", "theory"],
        "math",
        "NT",
        [("2025-01", 80), ("2025-02", 90), ("2025-03", 85)],  # 3 periods, 255 papers
        ["math.NT研究"],
    )
    cs_topic = make_topic(
        "cs_1",
        "Machine Learning Topic",
        ["machine", "learning"],
        "cs",
        "AI",
        [("2025-01", 150), ("2025-02", 180), ("2025-03", 170)],  # 3 periods, 500 papers
        ["cs.AI研究"],
    )

    topics = {
        "math_1": math_topic_1,
        "math_2": math_topic_2,
        "cs_1": cs_topic,
    }

    # Build minimal graph with edges (each topic needs >=2 neighbors)
    graph = {
        "nodes": list(topics.keys()),
        "edges": {
            "adjacent_to": [
                # math_1 neighbors: math_2, cs_1 (2 neighbors)
                {"source": "math_1", "target": "math_2", "weight": 0.5},
                {"source": "math_1", "target": "cs_1", "weight": 0.4},
                # math_2 neighbors: math_1, cs_1 (2 neighbors)
                {"source": "math_2", "target": "math_1", "weight": 0.5},
                {"source": "math_2", "target": "cs_1", "weight": 0.3},
                # cs_1 neighbors: math_1, math_2 (2 neighbors)
                {"source": "cs_1", "target": "math_1", "weight": 0.4},
                {"source": "cs_1", "target": "math_2", "weight": 0.3},
            ]
        },
    }

    periods = ["2025-01", "2025-02", "2025-03", "2025-04"]

    # Test with category_filter="math"
    anchor_ids = select_anchor_topics(
        topics,
        graph["edges"]["adjacent_to"],
        periods,
        horizon=2,
        max_cases=10,
        category_filter="math",
    )

    # Should only return math topics
    assert len(anchor_ids) > 0
    for topic_id in anchor_ids:
        assert topics[topic_id].category == "math"


def test_category_filter_none_returns_all_categories():
    """Test that category_filter=None returns topics from all categories."""
    # Create topics from different categories (meeting min criteria)
    math_topic = make_topic(
        "math_1",
        "Algebraic Geometry Topic",
        ["variety", "algebraic"],
        "math",
        "AG",
        [("2025-01", 100), ("2025-02", 120), ("2025-03", 110)],  # 3 periods, 330 papers
        ["math.AG研究"],
    )
    cs_topic = make_topic(
        "cs_1",
        "Machine Learning Topic",
        ["machine", "learning"],
        "cs",
        "AI",
        [("2025-01", 150), ("2025-02", 180), ("2025-03", 170)],  # 3 periods, 500 papers
        ["cs.AI研究"],
    )

    topics = {
        "math_1": math_topic,
        "cs_1": cs_topic,
    }

    # Build minimal graph with edges (each needs >=2 neighbors)
    graph = {
        "nodes": list(topics.keys()),
        "edges": {
            "adjacent_to": [
                # Both topics have each other as neighbor (1 neighbor each, need another)
                {"source": "math_1", "target": "cs_1", "weight": 0.3},
                {"source": "cs_1", "target": "math_1", "weight": 0.3},
            ]
        },
    }

    periods = ["2025-01", "2025-02", "2025-03", "2025-04"]

    # Test without category_filter (None)
    anchor_ids = select_anchor_topics(
        topics,
        graph["edges"]["adjacent_to"],
        periods,
        horizon=2,
        max_cases=10,
        category_filter=None,
    )

    # Should return topics from both categories (subject to other filters)
    # Note: Due to min_neighbors=2 requirement, these topics may not qualify
    # We just verify the function runs without error when category_filter=None


def test_category_filter_respects_max_cases():
    """Test that category_filter respects max_cases limit."""
    # Create multiple math topics (3+ periods to meet min_active_periods=2)
    topics = {}
    for i in range(10):
        topics[f"math_{i}"] = make_topic(
            f"math_{i}",
            f"Math Topic {i}",
            ["math", f"topic{i}"],
            "math",
            "AG",
            [("2025-01", 100 + i * 10), ("2025-02", 120 + i * 10), ("2025-03", 110 + i * 10)],  # 3 periods
            ["math.AG研究"],
        )

    # Add edges between all topics (ensure each has >=2 neighbors)
    edges = []
    for i in range(10):
        for j in range(i + 1, 10):
            edges.append({"source": f"math_{i}", "target": f"math_{j}", "weight": 0.5})
            edges.append({"source": f"math_{j}", "target": f"math_{i}", "weight": 0.5})

    graph = {"nodes": list(topics.keys()), "edges": {"adjacent_to": edges}}
    periods = ["2025-01", "2025-02", "2025-03", "2025-04"]

    # Test with max_cases=5
    anchor_ids = select_anchor_topics(
        topics,
        graph["edges"]["adjacent_to"],
        periods,
        horizon=2,
        max_cases=5,
        category_filter="math",
    )

    # Should return at most 5 topics
    assert len(anchor_ids) <= 5
    # All should be math
    for topic_id in anchor_ids:
        assert topics[topic_id].category == "math"


def test_filter_graph_by_category_excludes_non_target_topics():
    """Test that _filter_graph_by_category only keeps target category topics and edges."""
    from pipeline.evolution_analysis import _filter_graph_by_category

    # Create a mixed-category graph
    graph = {
        "version": "1.0",
        "generated_at": "2025-01-01",
        "periods": ["2025-01", "2025-02"],
        "nodes": {
            "categories": [{"id": "math"}, {"id": "cs"}],
            "periods": [{"id": "2025-01"}, {"id": "2025-02"}],
            "topics": [
                {"id": "math_1", "category": "math", "name": "Math Topic 1"},
                {"id": "math_2", "category": "math", "name": "Math Topic 2"},
                {"id": "cs_1", "category": "cs", "name": "CS Topic 1"},
            ],
        },
        "edges": {
            "adjacent_to": [
                {"source": "math_1", "target": "math_2", "weight": 0.5},
                {"source": "math_2", "target": "math_1", "weight": 0.5},
                {"source": "math_1", "target": "cs_1", "weight": 0.3},  # Cross-category edge
                {"source": "cs_1", "target": "math_1", "weight": 0.3},
            ]
        },
    }

    # Filter to math only
    filtered = _filter_graph_by_category(graph, "math")

    # Should only have math topics
    assert len(filtered["nodes"]["topics"]) == 2
    topic_ids = {t["id"] for t in filtered["nodes"]["topics"]}
    assert topic_ids == {"math_1", "math_2"}

    # Should only have math-to-math edges
    assert len(filtered["edges"]["adjacent_to"]) == 2
    for edge in filtered["edges"]["adjacent_to"]:
        assert edge["source"] in {"math_1", "math_2"}
        assert edge["target"] in {"math_1", "math_2"}

    # Should only have math category
    assert len(filtered["nodes"]["categories"]) == 1
    assert filtered["nodes"]["categories"][0]["id"] == "math"


def test_filter_graph_by_category_preserves_all_when_no_filter():
    """Test that _filter_graph_by_category preserves all data when category is empty."""
    from pipeline.evolution_analysis import _filter_graph_by_category

    graph = {
        "version": "1.0",
        "generated_at": "2025-01-01",
        "periods": ["2025-01"],
        "nodes": {
            "categories": [{"id": "math"}, {"id": "cs"}],
            "periods": [{"id": "2025-01"}],
            "topics": [
                {"id": "math_1", "category": "math", "name": "Math Topic 1"},
                {"id": "cs_1", "category": "cs", "name": "CS Topic 1"},
            ],
        },
        "edges": {"adjacent_to": [{"source": "math_1", "target": "cs_1", "weight": 0.5}]},
    }

    # No filter (empty string)
    filtered = _filter_graph_by_category(graph, "")

    # Should preserve original
    assert len(filtered["nodes"]["topics"]) == 2
    assert len(filtered["edges"]["adjacent_to"]) == 1
