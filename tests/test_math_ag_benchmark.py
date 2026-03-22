try:
    from pipeline.math_benchmark import evaluate_expected
except ModuleNotFoundError:
    import sys
    sys.path.insert(0, "/Users/daiduo2/.codex/worktrees/2124/academic-trend-monitor")
    from pipeline.math_benchmark import evaluate_expected


def test_evaluate_expected_accepts_exact_match():
    passed, reason = evaluate_expected("math_ag_object_continuity", "math_ag_object_continuity")
    assert passed is True
    assert reason == "ok"


def test_evaluate_expected_rejects_mismatch():
    passed, reason = evaluate_expected("none", "math_ag_object_continuity")
    assert passed is False
    assert reason == "mismatch"


def test_evaluate_expected_accepts_forbidden_relation_when_different():
    passed, reason = evaluate_expected("math_ag_object_continuity", "not math_ag_method_continuity")
    assert passed is True
    assert reason == "ok"


def test_evaluate_expected_rejects_forbidden_relation_when_equal():
    passed, reason = evaluate_expected("math_ag_method_continuity", "not math_ag_method_continuity")
    assert passed is False
    assert reason == "forbidden_relation"


def test_evaluate_expected_marks_review_needed_as_pass():
    passed, reason = evaluate_expected("none", "review-needed")
    assert passed is True
    assert reason == "review_only"


def test_evaluate_expected_accepts_none_when_expected_none():
    passed, reason = evaluate_expected("none", "none")
    assert passed is True
    assert reason == "ok"
