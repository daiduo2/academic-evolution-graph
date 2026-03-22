#!/usr/bin/env python3
"""
Math Knowledge Graph v1 Exporter

Exports aligned topic hierarchy data to KG v1 format with benchmark annotations.
"""

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any, Optional
from datetime import datetime

try:
    from pipeline.math_ag_benchmark import AG_CASE_REGISTRY, AG_GRAPH_LAYERS
except ModuleNotFoundError:
    from math_ag_benchmark import AG_CASE_REGISTRY, AG_GRAPH_LAYERS


GRAPH_BAND_ORDER = ['baseline', 'bridge', 'boundary', 'review', 'contract', 'deferred']


AG_AMBIGUOUS_CASE = {
    'case_id': 'ag-amb1',
    'anchor': 'global_4',
    'target': 'global_287',
    'expected_relation': 'review-needed',
    'type': 'ambiguous',
    'confidence': 'ambiguous',
    'status': 'ambiguous',
}

AG_GRAPH_CASE_REGISTRY = {
    'ag-p1': {
        **AG_CASE_REGISTRY['ag-p1'],
        'domain_code': 'math.AG',
        'graph_band': 'baseline',
        'graph_layer': 'confirmed_core',
        'graph_role': 'event_baseline',
        'source_doc': 'docs/plans/2026-03-18-math-ag-benchmark.md',
    },
    'ag-p2': {
        **AG_CASE_REGISTRY['ag-p2'],
        'domain_code': 'math.AG',
        'graph_band': 'bridge',
        'graph_layer': 'bridge_ring',
        'graph_role': 'inner_bridge_support',
        'source_doc': 'docs/plans/2026-03-18-math-ag-benchmark.md',
    },
    'ag-p3': {
        **AG_CASE_REGISTRY['ag-p3'],
        'domain_code': 'math.AG',
        'graph_band': 'bridge',
        'graph_layer': 'bridge_ring',
        'graph_role': 'outer_bridge_support',
        'source_doc': 'docs/plans/2026-03-18-math-ag-benchmark.md',
    },
    'ag-n1': {
        **AG_CASE_REGISTRY['ag-n1'],
        'domain_code': 'math.AG',
        'graph_band': 'boundary',
        'graph_layer': 'excluded_boundary',
        'graph_role': 'single_term_boundary',
        'level': 'boundary',
        'source_doc': 'docs/plans/2026-03-18-math-ag-benchmark.md',
    },
    'ag-n2': {
        **AG_CASE_REGISTRY['ag-n2'],
        'domain_code': 'math.AG',
        'graph_band': 'boundary',
        'graph_layer': 'excluded_boundary',
        'graph_role': 'class_overlap_boundary',
        'level': 'boundary',
        'source_doc': 'docs/plans/2026-03-18-math-ag-benchmark.md',
    },
    'ag-n3': {
        **AG_CASE_REGISTRY['ag-n3'],
        'domain_code': 'math.AG',
        'graph_band': 'boundary',
        'graph_layer': 'excluded_boundary',
        'graph_role': 'domain_boundary',
        'level': 'boundary',
        'source_doc': 'docs/plans/2026-03-18-math-ag-benchmark.md',
    },
    'ag-amb1': {
        **AG_AMBIGUOUS_CASE,
        'domain_code': 'math.AG',
        'graph_band': 'review',
        'graph_layer': 'review_boundary',
        'graph_role': 'boundary_dispute',
        'level': 'ambiguous',
        'narrative_note': 'Review-only AG boundary dispute; keep visible in metadata, not inside the default bridge ring.',
        'source_doc': 'docs/plans/2026-03-18-math-ag-benchmark.md',
    },
}

AG_KG_GRAPH_LAYERS = {
    'confirmed_core': {
        'graph_band': 'baseline',
        'label': 'confirmed core',
        'summary': AG_GRAPH_LAYERS['confirmed_core']['summary'],
        'case_ids': AG_GRAPH_LAYERS['confirmed_core']['case_ids'],
    },
    'bridge_ring': {
        'graph_band': 'bridge',
        'label': 'bridge ring',
        'summary': AG_GRAPH_LAYERS['bridge_ring']['summary'],
        'case_ids': AG_GRAPH_LAYERS['bridge_ring']['case_ids'],
    },
    'excluded_boundary': {
        'graph_band': 'boundary',
        'label': 'excluded boundary',
        'summary': AG_GRAPH_LAYERS['excluded_boundary']['summary'],
        'case_ids': AG_GRAPH_LAYERS['excluded_boundary']['case_ids'],
    },
    'review_boundary': {
        'graph_band': 'review',
        'label': 'review-only dispute',
        'summary': 'Boundary dispute kept visible for expert review, but intentionally left outside the default bridge ring.',
        'case_ids': ['ag-amb1'],
    },
}

LO_GRAPH_CASE_REGISTRY = {
    'lo-b1': {
        'case_id': 'lo-b1',
        'anchor': 'global_56',
        'target': 'global_27',
        'expected_relation': 'math_lo_modal_continuity',
        'level': 'event-level',
        'domain_code': 'math.LO',
        'graph_band': 'baseline',
        'graph_layer': 'modal_baseline',
        'graph_role': 'event_baseline',
        'narrative_note': 'Current LO event-level baseline; graph-supported and replay-backed.',
        'source_doc': 'docs/plans/2026-03-12-math-lo-benchmark.md',
    },
    'lo-b2': {
        'case_id': 'lo-b2',
        'anchor': 'global_56',
        'target': 'global_980',
        'expected_relation': 'math_lo_type_theory_continuity',
        'level': 'bridge-level',
        'domain_code': 'math.LO',
        'graph_band': 'bridge',
        'graph_layer': 'bridge_ring',
        'graph_role': 'type_theory_contrast',
        'narrative_note': 'Type-theory contrast branch: lexical bridge only, without graph/event support.',
        'source_doc': 'docs/plans/2026-03-12-math-lo-benchmark.md',
    },
    'lo-b3': {
        'case_id': 'lo-b3',
        'anchor': 'global_313',
        'target': 'global_360',
        'expected_relation': 'math_lo_set_theory_continuity',
        'level': 'bridge-level',
        'domain_code': 'math.LO',
        'graph_band': 'bridge',
        'graph_layer': 'bridge_ring',
        'graph_role': 'set_theory_inner_backbone',
        'narrative_note': 'Set-theory inner backbone: strongest graph-supported LO bridge branch below event-level.',
        'source_doc': 'docs/plans/2026-03-12-math-lo-benchmark.md',
    },
    'lo-b4': {
        'case_id': 'lo-b4',
        'anchor': 'global_51',
        'target': 'global_951',
        'expected_relation': 'math_lo_forcing_continuity',
        'level': 'bridge-level',
        'domain_code': 'math.LO',
        'graph_band': 'bridge',
        'graph_layer': 'bridge_ring',
        'graph_role': 'forcing_outer_branch',
        'narrative_note': 'Forcing outer branch: outward bridge into the large-cardinal/forcing neighborhood, not an event edge.',
        'source_doc': 'docs/plans/2026-03-12-math-lo-benchmark.md',
    },
    'lo-b5': {
        'case_id': 'lo-b5',
        'anchor': 'global_75',
        'target': 'global_778',
        'expected_relation': 'math_lo_definability_continuity',
        'level': 'bridge-level',
        'domain_code': 'math.LO',
        'graph_band': 'bridge',
        'graph_layer': 'bridge_ring',
        'graph_role': 'definability_capstone',
        'narrative_note': 'Definability capstone: narrow branch that closes the forcing/cardinal neighborhood into set-theoretic semantics.',
        'source_doc': 'docs/plans/2026-03-12-math-lo-benchmark.md',
    },
    'lo-n1': {
        'case_id': 'lo-n1',
        'anchor': 'global_51',
        'target': 'global_75',
        'expected_relation': 'not math_lo_forcing_continuity',
        'level': 'boundary',
        'domain_code': 'math.LO',
        'graph_band': 'boundary',
        'graph_layer': 'boundary_negative',
        'graph_role': 'forcing_boundary',
        'narrative_note': 'Keeps the forcing branch from swallowing the set-theory backbone.',
        'source_doc': 'docs/plans/2026-03-12-math-lo-benchmark.md',
    },
    'lo-n2': {
        'case_id': 'lo-n2',
        'anchor': 'global_339',
        'target': 'global_951',
        'expected_relation': 'none',
        'level': 'boundary',
        'domain_code': 'math.LO',
        'graph_band': 'boundary',
        'graph_layer': 'boundary_negative',
        'graph_role': 'set_theory_cluster_boundary',
        'narrative_note': 'Shows that shared cardinal/forcing vocabulary does not license the whole set-theory cluster as a positive branch.',
        'source_doc': 'docs/plans/2026-03-12-math-lo-benchmark.md',
    },
    'lo-n3': {
        'case_id': 'lo-n3',
        'anchor': 'global_167',
        'target': 'global_778',
        'expected_relation': 'none',
        'level': 'boundary',
        'domain_code': 'math.LO',
        'graph_band': 'boundary',
        'graph_layer': 'boundary_negative',
        'graph_role': 'definability_special_object_boundary',
        'narrative_note': 'Definability is not a free pass without the narrower set-theoretic special-object support.',
        'source_doc': 'docs/plans/2026-03-12-math-lo-benchmark.md',
    },
    'lo-n4': {
        'case_id': 'lo-n4',
        'anchor': 'global_361',
        'target': 'global_778',
        'expected_relation': 'none',
        'level': 'boundary',
        'domain_code': 'math.LO',
        'graph_band': 'boundary',
        'graph_layer': 'boundary_negative',
        'graph_role': 'definability_domain_boundary',
        'narrative_note': 'Domain-mismatch boundary for the definability branch.',
        'source_doc': 'docs/plans/2026-03-12-math-lo-benchmark.md',
    },
    'lo-n7': {
        'case_id': 'lo-n7',
        'anchor': 'global_56',
        'target': 'global_977',
        'expected_relation': 'not math_lo_type_theory_continuity',
        'level': 'boundary',
        'domain_code': 'math.LO',
        'graph_band': 'boundary',
        'graph_layer': 'boundary_negative',
        'graph_role': 'type_theory_missing_object_boundary',
        'narrative_note': 'Graph-near intuitionistic logic is still not type-theory without type objects.',
        'source_doc': 'docs/plans/2026-03-12-math-lo-benchmark.md',
    },
    'lo-n8': {
        'case_id': 'lo-n8',
        'anchor': 'global_56',
        'target': 'global_1155',
        'expected_relation': 'not math_lo_type_theory_continuity',
        'level': 'boundary',
        'domain_code': 'math.LO',
        'graph_band': 'boundary',
        'graph_layer': 'boundary_negative',
        'graph_role': 'type_theory_modal_boundary',
        'narrative_note': 'Modal/semantics similarity should remain outside the type-theory branch.',
        'source_doc': 'docs/plans/2026-03-12-math-lo-benchmark.md',
    },
    'lo-a1': {
        'case_id': 'lo-a1',
        'anchor': 'global_75',
        'target': 'global_951',
        'expected_relation': 'review-needed',
        'level': 'ambiguous',
        'domain_code': 'math.LO',
        'graph_band': 'review',
        'graph_layer': 'review_boundary',
        'graph_role': 'forcing_near_miss',
        'narrative_note': 'Near-miss on the forcing outer branch; keep review-only until the branch boundary changes.',
        'source_doc': 'docs/plans/2026-03-12-math-lo-benchmark.md',
    },
    'lo-a2': {
        'case_id': 'lo-a2',
        'anchor': 'global_339',
        'target': 'global_51',
        'expected_relation': 'review-needed',
        'level': 'ambiguous',
        'domain_code': 'math.LO',
        'graph_band': 'review',
        'graph_layer': 'review_boundary',
        'graph_role': 'set_theory_near_miss',
        'narrative_note': 'Near-miss inside the set-theory/forcing neighborhood; visible as a review boundary, not as a positive branch.',
        'source_doc': 'docs/plans/2026-03-12-math-lo-benchmark.md',
    },
}

LO_KG_GRAPH_LAYERS = {
    'modal_baseline': {
        'graph_band': 'baseline',
        'label': 'modal baseline',
        'summary': 'The single event-level LO baseline that stays on the mainline.',
        'case_ids': ['lo-b1'],
    },
    'bridge_ring': {
        'graph_band': 'bridge',
        'label': 'bridge-level ring',
        'summary': 'Stable LO bridge ring: type-theory contrast, set-theory inner backbone, forcing outer branch, definability capstone.',
        'case_ids': ['lo-b2', 'lo-b3', 'lo-b4', 'lo-b5'],
    },
    'boundary_negative': {
        'graph_band': 'boundary',
        'label': 'boundary negatives',
        'summary': 'Boundary negatives that keep the LO ring interpretable instead of absorbing nearby set-theory, modal, or definability neighbors.',
        'case_ids': ['lo-n1', 'lo-n2', 'lo-n3', 'lo-n4', 'lo-n7', 'lo-n8'],
    },
    'review_boundary': {
        'graph_band': 'review',
        'label': 'review near-miss',
        'summary': 'Near-miss cases close to the LO ring that remain review-only.',
        'case_ids': ['lo-a1', 'lo-a2'],
    },
}

CO_GRAPH_CASE_REGISTRY = {
    'co-b1': {
        'case_id': 'co-b1',
        'anchor': 'global_63',
        'target': 'global_308',
        'expected_relation': 'math_co_random_process_continuity',
        'level': 'bridge-level',
        'domain_code': 'math.CO',
        'graph_band': 'deferred',
        'graph_layer': 'deferred_branch',
        'graph_role': 'random_process_bridge',
        'narrative_note': 'Deferred random/percolation bridge branch; documented, but not the landed first-rule contract.',
        'source_doc': 'docs/plans/2026-03-31-math-co-benchmark.md',
    },
    'co-b2': {
        'case_id': 'co-b2',
        'anchor': 'global_16',
        'target': 'global_292',
        'expected_relation': 'math_co_matroid_structure_continuity',
        'level': 'bridge-level',
        'domain_code': 'math.CO',
        'graph_band': 'bridge',
        'graph_layer': 'bridge_support',
        'graph_role': 'matroid_supporting_bridge',
        'narrative_note': 'Supporting matroid bridge positive kept outside the landed MVP gate.',
        'source_doc': 'docs/plans/2026-03-31-math-co-benchmark.md',
    },
    'co-m1': {
        'case_id': 'co-m1',
        'anchor': 'global_292',
        'target': 'global_319',
        'expected_relation': 'math_co_matroid_structure_continuity',
        'level': 'contract',
        'domain_code': 'math.CO',
        'graph_band': 'contract',
        'graph_layer': 'matroid_mvp',
        'graph_role': 'mvp_positive',
        'narrative_note': 'Primary landed matroid MVP positive.',
        'source_doc': 'docs/plans/2026-03-31-math-co-benchmark.md',
    },
    'co-m2': {
        'case_id': 'co-m2',
        'anchor': 'global_118',
        'target': 'global_204',
        'expected_relation': 'math_co_matroid_structure_continuity',
        'level': 'contract',
        'domain_code': 'math.CO',
        'graph_band': 'contract',
        'graph_layer': 'matroid_mvp',
        'graph_role': 'supporting_positive',
        'narrative_note': 'Second landed matroid MVP positive inside the selected contract.',
        'source_doc': 'docs/plans/2026-03-31-math-co-benchmark.md',
    },
    'co-mn1': {
        'case_id': 'co-mn1',
        'anchor': 'global_292',
        'target': 'global_324',
        'expected_relation': 'not math_co_matroid_structure_continuity',
        'level': 'boundary',
        'domain_code': 'math.CO',
        'graph_band': 'boundary',
        'graph_layer': 'excluded_boundary',
        'graph_role': 'rank_polynomial_boundary',
        'narrative_note': 'Rank/polynomial overlap boundary for the matroid MVP.',
        'source_doc': 'docs/plans/2026-03-31-math-co-benchmark.md',
    },
    'co-mn2': {
        'case_id': 'co-mn2',
        'anchor': 'global_8',
        'target': 'global_319',
        'expected_relation': 'none',
        'level': 'boundary',
        'domain_code': 'math.CO',
        'graph_band': 'boundary',
        'graph_layer': 'excluded_boundary',
        'graph_role': 'graph_wide_term_boundary',
        'narrative_note': 'Generic graph-vocabulary boundary that must stay outside the matroid branch.',
        'source_doc': 'docs/plans/2026-03-31-math-co-benchmark.md',
    },
    'co-ma1': {
        'case_id': 'co-ma1',
        'anchor': 'global_220',
        'target': 'global_292',
        'expected_relation': 'review-needed / near-miss',
        'level': 'ambiguous',
        'domain_code': 'math.CO',
        'graph_band': 'review',
        'graph_layer': 'review_boundary',
        'graph_role': 'polytope_only_near_miss',
        'narrative_note': 'Polytope-only near-miss that stays outside the first matroid rule.',
        'source_doc': 'docs/plans/2026-03-31-math-co-benchmark.md',
    },
}

CO_KG_GRAPH_LAYERS = {
    'matroid_mvp': {
        'graph_band': 'contract',
        'label': 'matroid MVP',
        'summary': 'The landed matroid-family MVP contract. This is selected rule metadata, not baseline graph truth.',
        'case_ids': ['co-m1', 'co-m2'],
    },
    'bridge_support': {
        'graph_band': 'bridge',
        'label': 'supporting bridge',
        'summary': 'Graph-facing matroid support kept outside the current MVP gate.',
        'case_ids': ['co-b2'],
    },
    'excluded_boundary': {
        'graph_band': 'boundary',
        'label': 'excluded boundary',
        'summary': 'Boundary negatives that keep the matroid MVP conservative.',
        'case_ids': ['co-mn1', 'co-mn2'],
    },
    'review_boundary': {
        'graph_band': 'review',
        'label': 'review near-miss',
        'summary': 'Near-miss cases parked outside the matroid MVP until a broader rule exists.',
        'case_ids': ['co-ma1'],
    },
    'deferred_branch': {
        'graph_band': 'deferred',
        'label': 'deferred branch',
        'summary': 'Documented bridge branch deferred from the first landed rule.',
        'case_ids': ['co-b1'],
    },
}

DS_GRAPH_CASE_REGISTRY = {
    'ds-b1': {
        'case_id': 'ds-b1',
        'anchor': 'global_154',
        'target': 'global_186',
        'expected_relation': 'math_ds_ergodic_entropy_continuity',
        'level': 'bridge-level',
        'domain_code': 'math.DS',
        'graph_band': 'bridge',
        'graph_layer': 'ergodic_entropy_skeleton',
        'graph_role': 'ergodic_measure_bridge',
        'narrative_note': 'Bridge-level DS positive inside the ergodic/entropy neighborhood; stable enough for metadata, not for baseline topology.',
        'source_doc': 'docs/plans/2026-04-02-math-ds-benchmark.md',
    },
    'ds-b2': {
        'case_id': 'ds-b2',
        'anchor': 'global_154',
        'target': 'global_367',
        'expected_relation': 'math_ds_ergodic_entropy_continuity',
        'level': 'bridge-level',
        'domain_code': 'math.DS',
        'graph_band': 'bridge',
        'graph_layer': 'ergodic_entropy_skeleton',
        'graph_role': 'topological_entropy_extension',
        'narrative_note': 'Second bridge-level DS positive; exposes the local ergodic/entropy stretch without claiming event-level continuity.',
        'source_doc': 'docs/plans/2026-04-02-math-ds-benchmark.md',
    },
    'ds-n1': {
        'case_id': 'ds-n1',
        'anchor': 'global_119',
        'target': 'global_367',
        'expected_relation': 'none',
        'level': 'boundary',
        'domain_code': 'math.DS',
        'graph_band': 'boundary',
        'graph_layer': 'excluded_boundary',
        'graph_role': 'topological_term_boundary',
        'narrative_note': 'Shared topological vocabulary alone should not open the DS ergodic/entropy contract.',
        'source_doc': 'docs/plans/2026-04-02-math-ds-benchmark.md',
    },
    'ds-n2': {
        'case_id': 'ds-n2',
        'anchor': 'global_12',
        'target': 'global_154',
        'expected_relation': 'none',
        'level': 'boundary',
        'domain_code': 'math.DS',
        'graph_band': 'boundary',
        'graph_layer': 'excluded_boundary',
        'graph_role': 'measure_metric_boundary',
        'narrative_note': 'Broad measure/metric overlap should remain outside the DS continuity story.',
        'source_doc': 'docs/plans/2026-04-02-math-ds-benchmark.md',
    },
    'ds-a1': {
        'case_id': 'ds-a1',
        'anchor': 'global_49',
        'target': 'global_154',
        'expected_relation': 'review-needed',
        'level': 'ambiguous',
        'domain_code': 'math.DS',
        'graph_band': 'review',
        'graph_layer': 'review_boundary',
        'graph_role': 'fractal_entropy_near_miss',
        'narrative_note': 'Real DS near-miss between fractal/measure and ergodic/entropy branches; keep review-only.',
        'source_doc': 'docs/plans/2026-04-02-math-ds-benchmark.md',
    },
}

DS_KG_GRAPH_LAYERS = {
    'ergodic_entropy_skeleton': {
        'graph_band': 'bridge',
        'label': 'ergodic/entropy skeleton',
        'summary': 'Bridge-level DS skeleton around ergodic/entropy continuity; graph-facing metadata only, not baseline topology.',
        'case_ids': ['ds-b1', 'ds-b2'],
    },
    'excluded_boundary': {
        'graph_band': 'boundary',
        'label': 'excluded boundary',
        'summary': 'Boundary negatives that keep broad topological or measure overlap from becoming DS continuity truth.',
        'case_ids': ['ds-n1', 'ds-n2'],
    },
    'review_boundary': {
        'graph_band': 'review',
        'label': 'review boundary',
        'summary': 'Near-miss case kept review-only while the DS ergodic/fractal boundary remains unsettled.',
        'case_ids': ['ds-a1'],
    },
}


NA_GRAPH_CASE_REGISTRY = {
    'na-b1': {
        'case_id': 'na-b1',
        'anchor': 'global_105',
        'target': 'global_140',
        'expected_relation': 'math_na_krylov_iterative_continuity',
        'level': 'bridge-level',
        'domain_code': 'math.NA',
        'graph_band': 'bridge',
        'graph_layer': 'krylov_iterative_skeleton',
        'graph_role': 'gmres_to_krylov_bridge',
        'narrative_note': 'Bridge-level NA positive from a narrow GMRES anchor into the broader Krylov family; export as narrative only, not baseline topology.',
        'source_doc': 'docs/plans/2026-04-03-math-na-benchmark.md',
    },
    'na-b2': {
        'case_id': 'na-b2',
        'anchor': 'global_140',
        'target': 'global_9',
        'expected_relation': 'math_na_krylov_iterative_continuity',
        'level': 'bridge-level',
        'domain_code': 'math.NA',
        'graph_band': 'bridge',
        'graph_layer': 'krylov_iterative_skeleton',
        'graph_role': 'krylov_block_acceleration_branch',
        'narrative_note': 'Second bridge-level NA positive along the current Krylov/block-iterative backbone; stable enough for metadata, not for baseline truth.',
        'source_doc': 'docs/plans/2026-04-03-math-na-benchmark.md',
    },
    'na-n1': {
        'case_id': 'na-n1',
        'anchor': 'global_105',
        'target': 'global_378',
        'expected_relation': 'not math_na_krylov_iterative_continuity',
        'level': 'boundary',
        'domain_code': 'math.NA',
        'graph_band': 'boundary',
        'graph_layer': 'excluded_boundary',
        'graph_role': 'approximation_term_boundary',
        'narrative_note': 'Shared approximation vocabulary alone must not pull interpolation/kernel-approximation topics into the Krylov continuity story.',
        'source_doc': 'docs/plans/2026-04-03-math-na-benchmark.md',
    },
    'na-n2': {
        'case_id': 'na-n2',
        'anchor': 'global_140',
        'target': 'global_90',
        'expected_relation': 'none',
        'level': 'boundary',
        'domain_code': 'math.NA',
        'graph_band': 'boundary',
        'graph_layer': 'excluded_boundary',
        'graph_role': 'convergence_term_boundary',
        'narrative_note': 'Shared convergence language should stay outside the Krylov iterative contract.',
        'source_doc': 'docs/plans/2026-04-03-math-na-benchmark.md',
    },
    'na-a1': {
        'case_id': 'na-a1',
        'anchor': 'global_86',
        'target': 'global_307',
        'expected_relation': 'review-needed',
        'level': 'ambiguous',
        'domain_code': 'math.NA',
        'graph_band': 'review',
        'graph_layer': 'review_boundary',
        'graph_role': 'krylov_application_near_miss',
        'narrative_note': 'Real NA near-miss where a single Krylov overlap reaches into quantum/tensor application space; keep review-only.',
        'source_doc': 'docs/plans/2026-04-03-math-na-benchmark.md',
    },
}

NA_KG_GRAPH_LAYERS = {
    'krylov_iterative_skeleton': {
        'graph_band': 'bridge',
        'label': 'krylov iterative skeleton',
        'summary': 'Bridge-level NA skeleton around Krylov/GMRES continuity; graph-facing metadata only until NA has a real event-level or runner-ready baseline.',
        'case_ids': ['na-b1', 'na-b2'],
    },
    'excluded_boundary': {
        'graph_band': 'boundary',
        'label': 'excluded boundary',
        'summary': 'Boundary negatives that keep broad approximation or convergence overlap from becoming NA continuity truth.',
        'case_ids': ['na-n1', 'na-n2'],
    },
    'review_boundary': {
        'graph_band': 'review',
        'label': 'review boundary',
        'summary': 'Near-miss case kept review-only while the Krylov-to-application boundary remains unsettled.',
        'case_ids': ['na-a1'],
    },
}

DOMAIN_KNOWLEDGE_SPECS = {
    'math.LO': {
        'source_doc': 'docs/plans/2026-03-12-math-lo-benchmark.md',
        'export_presence': 'baseline_subgraph',
        'topology_status': 'baseline_topology_included',
        'graph_shape': 'baseline_plus_bridge_ring',
        'summary': 'Modal stays the event-level baseline; type-theory, set theory, forcing, and definability form the bridge-level ring around it.',
        'baseline_truth_layer_keys': ['modal_baseline'],
        'narrative_only_layer_keys': ['bridge_ring', 'boundary_negative', 'review_boundary'],
        'layers': LO_KG_GRAPH_LAYERS,
        'case_registry': LO_GRAPH_CASE_REGISTRY,
    },
    'math.AG': {
        'source_doc': 'docs/plans/2026-03-18-math-ag-benchmark.md',
        'export_presence': 'baseline_subgraph',
        'topology_status': 'baseline_topology_included',
        'graph_shape': 'confirmed_core_plus_bridge_ring_plus_boundary',
        'summary': 'AG keeps one confirmed core in the baseline topology and exposes the bridge ring / excluded boundary as metadata-only narrative support.',
        'baseline_truth_layer_keys': ['confirmed_core'],
        'narrative_only_layer_keys': ['bridge_ring', 'excluded_boundary', 'review_boundary'],
        'layers': AG_KG_GRAPH_LAYERS,
        'case_registry': AG_GRAPH_CASE_REGISTRY,
    },
    'math.CO': {
        'source_doc': 'docs/plans/2026-03-31-math-co-benchmark.md',
        'export_presence': 'docs_only_contract',
        'topology_status': 'not_in_baseline_topology',
        'graph_shape': 'matroid_mvp_contract_plus_supporting_bridge',
        'summary': 'CO stays outside the baseline topology; export metadata only exposes the landed matroid MVP, its supporting bridge, and its boundary cases.',
        'selected_rule': 'math_co_matroid_structure_continuity',
        'baseline_truth_layer_keys': [],
        'narrative_only_layer_keys': ['matroid_mvp', 'bridge_support', 'excluded_boundary', 'review_boundary', 'deferred_branch'],
        'layers': CO_KG_GRAPH_LAYERS,
        'case_registry': CO_GRAPH_CASE_REGISTRY,
    },
    'math.DS': {
        'source_doc': 'docs/plans/2026-04-02-math-ds-benchmark.md',
        'export_presence': 'docs_only_narrative',
        'topology_status': 'not_in_baseline_topology',
        'graph_shape': 'bridge_skeleton_plus_boundary_review',
        'summary': 'DS contributes only a bridge-level benchmark skeleton around ergodic/entropy continuity; no DS nodes or baseline EVOLVES_TO edges are exported yet.',
        'candidate_rule': 'math_ds_ergodic_entropy_continuity',
        'narrative_status': 'benchmark_skeleton_ready',
        'baseline_truth_layer_keys': [],
        'narrative_only_layer_keys': ['ergodic_entropy_skeleton', 'excluded_boundary', 'review_boundary'],
        'layers': DS_KG_GRAPH_LAYERS,
        'case_registry': DS_GRAPH_CASE_REGISTRY,
    },
    'math.NA': {
        'source_doc': 'docs/plans/2026-04-03-math-na-benchmark.md',
        'export_presence': 'docs_only_narrative',
        'topology_status': 'not_in_baseline_topology',
        'graph_shape': 'krylov_bridge_skeleton_plus_boundary_review',
        'summary': 'NA contributes a bridge-level Krylov iterative skeleton plus boundary/review metadata; no NA nodes or baseline EVOLVES_TO edges are exported yet.',
        'candidate_rule': 'math_na_krylov_iterative_continuity',
        'narrative_status': 'benchmark_skeleton_ready',
        'baseline_truth_layer_keys': [],
        'narrative_only_layer_keys': ['krylov_iterative_skeleton', 'excluded_boundary', 'review_boundary'],
        'layers': NA_KG_GRAPH_LAYERS,
        'case_registry': NA_GRAPH_CASE_REGISTRY,
    },
}

GRAPH_CASE_REGISTRY_BY_ID = {}
for _spec in DOMAIN_KNOWLEDGE_SPECS.values():
    GRAPH_CASE_REGISTRY_BY_ID.update(_spec['case_registry'])


def _sort_graph_bands(graph_bands: list[str]) -> list[str]:
    return sorted(graph_bands, key=lambda band: (GRAPH_BAND_ORDER.index(band) if band in GRAPH_BAND_ORDER else len(GRAPH_BAND_ORDER), band))


def _build_case_snapshot(case: dict, *, status: str, confidence: str) -> dict:
    return {
        'case_id': case['case_id'],
        'anchor': case['anchor'],
        'target': case['target'],
        'expected_relation': case['expected_relation'],
        'type': status,
        'confidence': confidence,
        'status': status,
    }


def parse_math_ag_benchmark_cases(content: str) -> list[dict]:
    """Parse the current AG benchmark doc into the runner/export baseline contract."""
    if 'Math.AG Benchmark — v2' not in content and 'Graph Narrative Layers' not in content:
        return parse_benchmark_cases(content)

    return [
        _build_case_snapshot(AG_GRAPH_CASE_REGISTRY['ag-p1'], status='positive', confidence='confirmed'),
        _build_case_snapshot(AG_GRAPH_CASE_REGISTRY['ag-n1'], status='negative', confidence='negative'),
        _build_case_snapshot(AG_GRAPH_CASE_REGISTRY['ag-n2'], status='negative', confidence='negative'),
        _build_case_snapshot(AG_GRAPH_CASE_REGISTRY['ag-n3'], status='negative', confidence='negative'),
        _build_case_snapshot(AG_GRAPH_CASE_REGISTRY['ag-amb1'], status='ambiguous', confidence='ambiguous'),
    ]


def build_domain_knowledge_layers(
    topics: dict[str, dict],
    evolves_to_edges: list[dict],
    target_subcategories: set[str],
) -> dict[str, dict]:
    """Expose graph-facing domain narrative layers without changing topology."""
    encoded_case_ids = {
        edge['benchmark_case_id']
        for edge in evolves_to_edges
        if edge.get('benchmark_case_id')
    }
    target_domain_codes = {f'math.{subcat}' for subcat in target_subcategories}
    domain_layers = {}

    for domain_code, spec in DOMAIN_KNOWLEDGE_SPECS.items():
        case_registry = spec['case_registry']
        case_entries = []
        for case in case_registry.values():
            case_id = case['case_id']
            anchor_in_scope = case['anchor'] in topics
            target_in_scope = case['target'] in topics

            if case_id in encoded_case_ids:
                export_status = 'encoded_as_evolves_to'
            elif domain_code not in target_domain_codes:
                export_status = 'docs_only_outside_export_scope'
            elif anchor_in_scope and target_in_scope:
                export_status = 'in_scope_metadata_only'
            else:
                export_status = 'docs_only_outside_baseline_hierarchy'

            case_entries.append({
                'case_id': case_id,
                'anchor': case['anchor'],
                'target': case['target'],
                'expected_relation': case['expected_relation'],
                'level': case.get('level', ''),
                'graph_band': case['graph_band'],
                'graph_layer': case['graph_layer'],
                'graph_role': case['graph_role'],
                'narrative_note': case.get('narrative_note', case.get('reason', '')),
                'source_doc': case.get('source_doc', spec['source_doc']),
                'export_status': export_status,
                'anchor_in_scope': anchor_in_scope,
                'target_in_scope': target_in_scope,
            })

        case_by_id = {case['case_id']: case for case in case_entries}
        layer_entries = {}
        for layer_key, layer in spec['layers'].items():
            layer_cases = [case_by_id[case_id] for case_id in layer['case_ids'] if case_id in case_by_id]
            layer_entries[layer_key] = {
                'graph_band': layer['graph_band'],
                'label': layer['label'],
                'summary': layer['summary'],
                'case_ids': layer['case_ids'],
                'encoded_case_ids': [case['case_id'] for case in layer_cases if case['export_status'] == 'encoded_as_evolves_to'],
                'metadata_only_case_ids': [
                    case['case_id']
                    for case in layer_cases
                    if case['export_status'] != 'encoded_as_evolves_to'
                ],
                'case_count': len(layer_cases),
                'encoded_case_count': len([case for case in layer_cases if case['export_status'] == 'encoded_as_evolves_to']),
                'metadata_only_case_count': len([case for case in layer_cases if case['export_status'] != 'encoded_as_evolves_to']),
            }

        case_counts_by_graph_band = {}
        case_counts_by_export_status = {}
        for case in case_entries:
            graph_band = case['graph_band']
            export_status = case['export_status']
            case_counts_by_graph_band[graph_band] = case_counts_by_graph_band.get(graph_band, 0) + 1
            case_counts_by_export_status[export_status] = case_counts_by_export_status.get(export_status, 0) + 1

        layer_counts_by_graph_band = {}
        for layer in layer_entries.values():
            graph_band = layer['graph_band']
            layer_counts_by_graph_band[graph_band] = layer_counts_by_graph_band.get(graph_band, 0) + 1

        visible_graph_bands = _sort_graph_bands(list(layer_counts_by_graph_band.keys()))

        domain_layers[domain_code] = {
            'source_doc': spec['source_doc'],
            'export_presence': spec['export_presence'],
            'topology_status': spec['topology_status'],
            'graph_shape': spec['graph_shape'],
            'summary': spec['summary'],
            'selected_rule': spec.get('selected_rule'),
            'candidate_rule': spec.get('candidate_rule'),
            'narrative_status': spec.get('narrative_status'),
            'baseline_truth_layer_keys': spec.get('baseline_truth_layer_keys', []),
            'narrative_only_layer_keys': spec.get('narrative_only_layer_keys', []),
            'visible_graph_bands': visible_graph_bands,
            'layers': layer_entries,
            'case_registry': case_entries,
            'encoded_case_ids': [case['case_id'] for case in case_entries if case['export_status'] == 'encoded_as_evolves_to'],
            'case_count': len(case_entries),
            'case_counts_by_graph_band': {
                band: case_counts_by_graph_band[band]
                for band in visible_graph_bands
                if band in case_counts_by_graph_band
            },
            'case_counts_by_export_status': case_counts_by_export_status,
            'layer_counts_by_graph_band': {
                band: layer_counts_by_graph_band[band]
                for band in visible_graph_bands
                if band in layer_counts_by_graph_band
            },
        }

    return domain_layers


def parse_benchmark_cases(content: str) -> list[dict]:
    """Parse benchmark cases from markdown content."""
    cases = []

    # Find all table rows with case IDs
    # Pattern matches: | `case-id` | `global_XX` ... | `global_XX` ... | `relation` | ... |
    table_pattern = r'\|\s*`?([^|`]+)`?\s*\|\s*`?(global_\d+)`?[^|]*\|\s*`?(global_\d+)`?[^|]*\|\s*`?([^`|]+)`?[^|]*'

    lines = content.split('\n')
    in_table = False

    for line in lines:
        line = line.strip()
        if '| Case ID |' in line or '|---------|' in line:
            in_table = True
            continue

        if not line.startswith('|') or 'Case ID' in line:
            continue

        # Parse table row
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if len(cells) >= 4:
            case_id = cells[0].strip('`').strip()
            anchor = cells[1].split()[0].strip('`').strip()  # Get just the global_XX part
            target = cells[2].split()[0].strip('`').strip()  # Get just the global_XX part
            expected_relation = cells[3].strip('`').strip()

            # Determine case type and confidence
            if case_id.startswith('lo-b') or case_id.startswith('ag-b') or case_id.startswith('ag-e'):
                case_type = 'positive'
                confidence = 'confirmed'
                status = 'positive'
            elif case_id.startswith('lo-n') or case_id.startswith('ag-n') or case_id.startswith('ag-method-n'):
                case_type = 'negative'
                confidence = 'negative'
                status = 'negative'
            elif case_id.startswith('lo-a') or case_id.startswith('ag-a'):
                case_type = 'ambiguous'
                confidence = 'ambiguous'
                status = 'ambiguous'
            elif case_id.startswith('ag-method-p'):
                # Test evidence cases - SKIP (not part of KG-02 baseline)
                continue
            else:
                continue

            # Skip if not a valid global ID
            if not anchor.startswith('global_') or not target.startswith('global_'):
                continue

            cases.append({
                'case_id': case_id,
                'anchor': anchor,
                'target': target,
                'expected_relation': expected_relation,
                'type': case_type,
                'confidence': confidence,
                'status': status
            })

    return cases


def parse_pr_cases(content: str) -> list[dict]:
    """Parse PR curation doc to extract graph-visible positive cases only."""
    cases = []

    # Split on PR-P section headers (positive cases only)
    sections = re.split(r'(?=#### PR-P)', content)

    for section in sections:
        # Match header: #### PR-P1: global_38 → global_100 (also handle ->)
        header_match = re.match(
            r'#### (PR-P(\d+)):\s*(global_\d+)\s*[→\->]+\s*(global_\d+)',
            section.strip()
        )
        if not header_match:
            continue

        pair_id = header_match.group(1)   # e.g. PR-P1
        anchor = header_match.group(3)    # e.g. global_38
        target = header_match.group(4)    # e.g. global_100
        case_id = pair_id.lower().replace('-', '-p').replace('pr-p', 'pr-p')
        # Normalize: pr-p1
        case_id = f"pr-p{header_match.group(2)}"

        # Determine tier from the curation status line only (avoid false positives from later sections)
        curation_status_match = re.search(
            r'\*\*Curation status:\*\*.*?Tier\s+([AB])',
            section
        )
        if curation_status_match:
            curation_tier = curation_status_match.group(1)
        elif 'Tier A' in section:
            curation_tier = 'A'
        elif 'Tier B' in section:
            curation_tier = 'B'
        else:
            curation_tier = 'A'

        # Determine continuity type
        if 'Method continuity' in section or 'method_continuity' in section:
            continuity_type = 'method'
        else:
            continuity_type = 'object'

        cases.append({
            'case_id': case_id,
            'pair_id': pair_id,
            'anchor': anchor,
            'target': target,
            'expected_relation': 'EVOLVES_TO',
            'type': 'positive',
            'confidence': 'inferred',
            'status': 'positive',
            'integration_scope': 'conditional',
            'curation_tier': curation_tier,
            'curation_status': 'positive',
            'human_review_required': True,
            'graph_integration_candidate': 'gate1_eligible',
            'continuity_type': continuity_type,
        })

    return cases


def load_jsonl(filepath: str) -> list[dict]:
    """Load JSONL file."""
    data = []
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            for line in f:
                data.append(json.loads(line.strip()))
    return data


def save_jsonl(filepath: str, data: list[dict]) -> None:
    """Save data to JSONL file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')


def save_json(filepath: str, data: dict) -> None:
    """Save data to JSON file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_period_dates(period: str) -> tuple[str, str]:
    """Get start and end dates for a period (YYYY-MM format)."""
    year, month = period.split('-')
    start_date = f"{year}-{month}-01"
    # Get last day of month
    if month in ['04', '06', '09', '11']:
        end_date = f"{year}-{month}-30"
    elif month == '02':
        end_date = f"{year}-{month}-28"
    else:
        end_date = f"{year}-{month}-31"
    return start_date, end_date


def build_topic_nodes(data: dict, target_subcategories: set[str]) -> dict[str, dict]:
    """Build topic nodes from the aligned data."""
    topics = {}

    # Get baseline topic IDs from hierarchies' topic_assignments
    hierarchies = data.get('hierarchies', {})
    lo_ids = set(hierarchies.get('math.LO', {}).get('topic_assignments', {}).keys())
    ag_ids = set(hierarchies.get('math.AG', {}).get('topic_assignments', {}).keys())
    pr_ids = set(hierarchies.get('math.PR', {}).get('topic_assignments', {}).keys()) if 'PR' in target_subcategories else set()
    all_ids = lo_ids | ag_ids | pr_ids

    # The detailed topic data is under 'trends' key as global_XXX objects
    trends = data.get('trends', {})

    for topic_id in all_ids:
        if not topic_id.startswith('global_'):
            continue

        value = trends.get(topic_id, {})

        # Check if this topic belongs to a target subcategory
        subcategory = value.get('subcategory', '')
        if subcategory not in target_subcategories:
            continue

        history = value.get('history', [])
        active_periods = len(history)
        total_papers = value.get('total_papers', 0)

        # Determine topic_mode based on active_periods
        topic_mode = 'persistent' if active_periods >= 3 else 'transient'

        topics[topic_id] = {
            'id': topic_id,
            'type': 'topic',
            'name': value.get('name', ''),
            'keywords': value.get('keywords', []),
            'category': value.get('category', 'math'),
            'subcategory': subcategory,
            'topic_mode': topic_mode,
            'total_papers': total_papers,
            'active_periods': active_periods,
            'history': history,
            'hierarchy_path': value.get('hierarchy_path', []),
            'hierarchy_depth': value.get('hierarchy_depth', 1)
        }

    return topics


def build_subcategory_nodes(topics: dict[str, dict], target_subcategories: set[str]) -> dict[str, dict]:
    """Build subcategory nodes from topics."""
    subcategories = {}

    subcategory_names = {
        'LO': 'Logic',
        'AG': 'Algebraic Geometry',
        'PR': 'Probability Theory'
    }

    for subcat in target_subcategories:
        subcat_topics = [t for t in topics.values() if t['subcategory'] == subcat]
        topic_count = len(subcat_topics)

        multi_period = sum(1 for t in subcat_topics if t['active_periods'] > 1)
        single_period = sum(1 for t in subcat_topics if t['active_periods'] == 1)

        # Eligible anchors: topics with > 1 active period
        eligible_anchors = sum(1 for t in subcat_topics if t['active_periods'] > 1)

        evidence_quality = 'conditional-inferred' if subcat == 'PR' else 'benchmark-verified'

        subcategories[subcat] = {
            'code': f'math.{subcat}',
            'name': subcategory_names.get(subcat, subcat),
            'discipline': 'math',
            'topic_count': topic_count,
            'multi_period_count': multi_period,
            'single_period_count': single_period,
            'eligible_anchor_count': eligible_anchors,
            'status': 'ready',
            'evidence_quality': evidence_quality
        }

    return subcategories


def build_period_nodes(periods: list[str]) -> list[dict]:
    """Build period nodes."""
    period_nodes = []
    for period in periods:
        start_date, end_date = get_period_dates(period)
        period_nodes.append({
            'id': period,
            'start_date': start_date,
            'end_date': end_date
        })
    return period_nodes


def build_contains_topic_edges(topics: dict[str, dict]) -> list[dict]:
    """Build CONTAINS_TOPIC edges from subcategories to topics."""
    edges = []
    for topic_id, topic in topics.items():
        edges.append({
            'source': f"math.{topic['subcategory']}",
            'target': topic_id,
            'type': 'CONTAINS_TOPIC'
        })
    return edges


def build_active_in_edges(topics: dict[str, dict]) -> list[dict]:
    """Build ACTIVE_IN edges from topics to periods."""
    edges = []
    for topic_id, topic in topics.items():
        for h in topic.get('history', []):
            period = h.get('period')
            if period:
                edges.append({
                    'source': topic_id,
                    'target': period,
                    'type': 'ACTIVE_IN',
                    'paper_count': h.get('paper_count', 0)
                })
    return edges


def build_parent_of_edges(topics: dict[str, dict]) -> list[dict]:
    """Build PARENT_OF edges from hierarchy paths."""
    edges = []
    seen_edges = set()

    for topic_id, topic in topics.items():
        hierarchy_path = topic.get('hierarchy_path', [])

        # Build parent-child relationships from hierarchy path
        for i in range(len(hierarchy_path) - 1):
            parent = hierarchy_path[i]
            child = hierarchy_path[i + 1]

            # Create unique edge key
            edge_key = (parent, child)
            if edge_key not in seen_edges:
                seen_edges.add(edge_key)
                edges.append({
                    'source': parent,
                    'target': child,
                    'type': 'PARENT_OF'
                })

    return edges


def build_neighbor_of_edges(topics: dict[str, dict], data: dict, topic_graph_path: Optional[str] = None) -> list[dict]:
    """Build NEIGHBOR_OF edges from real graph adjacency.

    Uses adjacent_to edges from topic_graph.json instead of generating
    artificial cliques from subcategory membership.
    """
    edges = []
    seen_edges = set()

    # Get set of valid topic IDs (baseline topics)
    valid_topic_ids = set(topics.keys())

    # Load topic_graph.json if path provided
    adjacent_edges = []
    if topic_graph_path and os.path.exists(topic_graph_path):
        with open(topic_graph_path, 'r') as f:
            topic_graph = json.load(f)
        adjacent_edges = topic_graph.get('edges', {}).get('adjacent_to', [])

    # Build neighbor edges from real adjacency
    for adj_edge in adjacent_edges:
        source_id = adj_edge.get('source')
        target_id = adj_edge.get('target')

        # Only include edges where BOTH source and target are in baseline topic set
        if source_id not in valid_topic_ids or target_id not in valid_topic_ids:
            continue

        if source_id == target_id:
            continue

        # Create undirected edge (only one direction in file)
        edge_key = tuple(sorted([source_id, target_id]))
        if edge_key not in seen_edges:
            seen_edges.add(edge_key)

            # Determine subcategory from source topic
            source_topic = topics.get(source_id, {})
            subcategory = source_topic.get('subcategory', '')

            edges.append({
                'source': edge_key[0],
                'target': edge_key[1],
                'type': 'NEIGHBOR_OF',
                'subcategory': f'math.{subcategory}' if subcategory else '',
                'weight': adj_edge.get('weight', 0.0)
            })

    return edges


def build_evolves_to_edges(benchmark_cases: list[dict], topics: dict[str, dict]) -> list[dict]:
    """Build EVOLVES_TO edges from benchmark cases."""
    edges = []

    for case in benchmark_cases:
        anchor = case['anchor']
        target = case['target']

        # Skip if topics don't exist in our filtered set
        if anchor not in topics or target not in topics:
            continue

        if case.get('integration_scope') == 'conditional':
            # PR conditional edge
            edge = {
                'source': anchor,
                'target': target,
                'type': 'EVOLVES_TO',
                'evidence_type': 'provisional',
                'confidence': case['confidence'],
                'benchmark_case_id': case['case_id'],
                'benchmark_status': case['status'],
                'expected_relation': case['expected_relation'],
                'subcategory': f"math.{topics[anchor]['subcategory']}",
                'review_flags': [],
                'integration_scope': case.get('integration_scope', 'baseline'),
                'curation_tier': case.get('curation_tier'),
                'curation_status': case.get('curation_status'),
                'human_review_required': case.get('human_review_required', False),
                'graph_integration_candidate': case.get('graph_integration_candidate'),
                'continuity_type': case.get('continuity_type'),
            }
        else:
            # LO/AG baseline edge
            edge = {
                'source': anchor,
                'target': target,
                'type': 'EVOLVES_TO',
                'evidence_type': 'benchmark-confirmed',
                'confidence': case['confidence'],
                'benchmark_case_id': case['case_id'],
                'benchmark_status': case['status'],
                'expected_relation': case['expected_relation'],
                'subcategory': f"math.{topics[anchor]['subcategory']}",
                'review_flags': []
            }

        graph_case = GRAPH_CASE_REGISTRY_BY_ID.get(case['case_id'])
        if graph_case:
            edge.update({
                'graph_band': graph_case['graph_band'],
                'graph_layer': graph_case['graph_layer'],
                'graph_role': graph_case['graph_role'],
                'narrative_level': graph_case.get('level', ''),
                'narrative_note': graph_case.get('narrative_note', graph_case.get('reason', '')),
                'graph_export_status': 'encoded_as_evolves_to',
            })

        edges.append(edge)

    return edges


def validate_output(nodes: dict, edges: dict, metadata: dict, is_conditional: bool = False) -> dict:
    """Generate validation report matching expected test format."""
    schema_errors = []
    missing_files = []

    # Validate nodes
    for node_type, node_list in nodes.items():
        if isinstance(node_list, dict):
            node_list = list(node_list.values())

        for node in node_list:
            if node_type == 'topics':
                if 'id' not in node:
                    schema_errors.append(f"Topic missing id field")
                if not is_conditional and node.get('subcategory') == 'PR':
                    schema_errors.append(f"PR topic found in output: {node.get('id')}")

            elif node_type == 'subcategories':
                if not is_conditional and node.get('code') == 'math.PR':
                    schema_errors.append("math.PR subcategory found (should be excluded)")

    # Validate edges
    for edge_type, edge_list in edges.items():
        for edge in edge_list:
            if 'source' not in edge or 'target' not in edge:
                schema_errors.append(f"{edge_type} edge missing source or target")
            if 'type' not in edge:
                schema_errors.append(f"{edge_type} edge missing type field")

    # Check node count
    total_nodes = sum(len(v) if isinstance(v, list) else len(v.values()) for v in nodes.values())
    node_count_check = total_nodes > 0

    # Check edge count
    total_edges = sum(len(v) for v in edges.values())
    edge_count_check = total_edges > 0

    # Check benchmark alignment
    evolves_to_count = len(edges.get('evolves_to', []))
    if is_conditional:
        benchmark_alignment_check = evolves_to_count >= 9  # at least baseline LO+AG, plus PR
    else:
        benchmark_alignment_check = evolves_to_count == 9  # Expected: 4 LO + 5 AG (9 of 18 benchmark cases)

    # Overall status
    status = 'valid' if not schema_errors and node_count_check and edge_count_check and benchmark_alignment_check else 'invalid'

    return {
        'schema_version': 'kg_v1',
        'validation_timestamp': datetime.now().isoformat(),
        'schema_errors': schema_errors,
        'missing_files': missing_files,
        'node_count_check': 'pass' if node_count_check else 'fail',
        'edge_count_check': 'pass' if edge_count_check else 'fail',
        'benchmark_alignment_check': 'pass' if benchmark_alignment_check else 'fail',
        'status': status
    }


def main():
    parser = argparse.ArgumentParser(description='Export Math Knowledge Graph v1')
    parser.add_argument('--input', required=True, help='Input aligned_topics_hierarchy.json')
    parser.add_argument('--benchmark-lo', required=True, help='LO benchmark doc')
    parser.add_argument('--benchmark-ag', required=True, help='AG benchmark doc')
    parser.add_argument('--output-dir', required=True, help='Output directory')
    parser.add_argument('--benchmark-pr', required=False, default=None, help='PR benchmark/curation doc (enables conditional PR export)')
    args = parser.parse_args()

    is_conditional = args.benchmark_pr is not None

    print("Loading input data...")

    # Load aligned topics data
    with open(args.input, 'r') as f:
        data = json.load(f)

    # Load benchmark docs
    with open(args.benchmark_lo, 'r') as f:
        lo_content = f.read()

    with open(args.benchmark_ag, 'r') as f:
        ag_content = f.read()

    # Parse benchmark cases
    print("Parsing benchmark cases...")
    lo_cases = parse_benchmark_cases(lo_content)
    ag_cases = parse_math_ag_benchmark_cases(ag_content)

    print(f"  Found {len(lo_cases)} LO benchmark cases")
    print(f"  Found {len(ag_cases)} AG benchmark cases")

    # Parse PR cases if provided
    pr_cases = []
    if args.benchmark_pr:
        with open(args.benchmark_pr, 'r') as f:
            pr_content = f.read()
        pr_cases = parse_pr_cases(pr_content)
        print(f"  Found {len(pr_cases)} PR curated positive cases")

    all_cases = lo_cases + ag_cases + pr_cases

    # Target subcategories
    target_subcategories = {'LO', 'AG'}
    if is_conditional:
        target_subcategories = {'LO', 'AG', 'PR'}

    # Build nodes
    print("Building topic nodes...")
    topics = build_topic_nodes(data, target_subcategories)
    print(f"  Created {len(topics)} topic nodes")

    print("Building subcategory nodes...")
    subcategories = build_subcategory_nodes(topics, target_subcategories)
    print(f"  Created {len(subcategories)} subcategory nodes")

    print("Building period nodes...")
    periods = build_period_nodes(data.get('periods', []))
    print(f"  Created {len(periods)} period nodes")

    # Build edges
    print("Building edges...")

    contains_topic_edges = build_contains_topic_edges(topics)
    print(f"  Created {len(contains_topic_edges)} CONTAINS_TOPIC edges")

    active_in_edges = build_active_in_edges(topics)
    print(f"  Created {len(active_in_edges)} ACTIVE_IN edges")

    parent_of_edges = build_parent_of_edges(topics)
    print(f"  Created {len(parent_of_edges)} PARENT_OF edges")

    # Derive topic_graph path from input path
    input_path = Path(args.input)
    topic_graph_path = input_path.parent / 'topic_graph.json'

    neighbor_of_edges = build_neighbor_of_edges(topics, data, str(topic_graph_path))
    print(f"  Created {len(neighbor_of_edges)} NEIGHBOR_OF edges")

    evolves_to_edges = build_evolves_to_edges(all_cases, topics)
    print(f"  Created {len(evolves_to_edges)} EVOLVES_TO edges")
    domain_knowledge_layers = build_domain_knowledge_layers(topics, evolves_to_edges, target_subcategories)

    # Prepare output
    output_dir = Path(args.output_dir)

    nodes = {
        'topics': topics,
        'subcategories': subcategories,
        'periods': periods
    }

    edges_dict = {
        'contains_topic': contains_topic_edges,
        'active_in': active_in_edges,
        'parent_of': parent_of_edges,
        'neighbor_of': neighbor_of_edges,
        'evolves_to': evolves_to_edges
    }

    # Write output files
    print("Writing output files...")

    # Nodes
    save_jsonl(output_dir / 'nodes' / 'topics.jsonl', list(topics.values()))
    save_jsonl(output_dir / 'nodes' / 'subcategories.jsonl', list(subcategories.values()))
    save_jsonl(output_dir / 'nodes' / 'periods.jsonl', periods)

    # Edges
    save_jsonl(output_dir / 'edges' / 'contains_topic.jsonl', contains_topic_edges)
    save_jsonl(output_dir / 'edges' / 'active_in.jsonl', active_in_edges)
    save_jsonl(output_dir / 'edges' / 'parent_of.jsonl', parent_of_edges)
    save_jsonl(output_dir / 'edges' / 'neighbor_of.jsonl', neighbor_of_edges)
    save_jsonl(output_dir / 'edges' / 'evolves_to.jsonl', evolves_to_edges)

    # Metadata
    # Count benchmark cases by subcategory
    lo_case_count = len([e for e in evolves_to_edges if e.get('subcategory') == 'math.LO'])
    ag_case_count = len([e for e in evolves_to_edges if e.get('subcategory') == 'math.AG'])
    pr_case_count = len([e for e in evolves_to_edges if e.get('subcategory') == 'math.PR'])

    if is_conditional:
        included = ['math.LO', 'math.AG', 'math.PR']
        excluded = ['math.QA', 'math.RA', 'math.RT']
    else:
        included = ['math.LO', 'math.AG']
        excluded = ['math.PR', 'math.QA', 'math.RA', 'math.RT']

    metadata = {
        'version': 'kg_v1_pr_conditional' if is_conditional else 'kg_v1',
        'generated_at': datetime.now().isoformat(),
        'source': {
            'input_file': args.input,
            'benchmark_lo': args.benchmark_lo,
            'benchmark_ag': args.benchmark_ag,
            'benchmark_pr': args.benchmark_pr,
        },
        'scope': {
            'included_subcategories': included,
            'excluded_subcategories': excluded,
            'integration_scope': 'conditional' if is_conditional else 'baseline',
        },
        'topic_count': len(topics),
        'edge_counts': {
            'contains_topic': len(contains_topic_edges),
            'active_in': len(active_in_edges),
            'parent_of': len(parent_of_edges),
            'neighbor_of': len(neighbor_of_edges),
            'evolves_to': len(evolves_to_edges),
            'total': sum(len(e) for e in edges_dict.values())
        },
        'benchmark_case_counts': {
            'math.LO': lo_case_count,
            'math.AG': ag_case_count,
            'total': len(evolves_to_edges)
        },
        'domain_knowledge_layers': domain_knowledge_layers,
    }
    if is_conditional:
        metadata['benchmark_case_counts']['math.PR'] = pr_case_count
    save_json(output_dir / 'metadata.json', metadata)

    # Validation report
    validation = validate_output(nodes, edges_dict, metadata, is_conditional=is_conditional)
    save_json(output_dir / 'validation_report.json', validation)

    print("\nExport complete!")
    print(f"Output directory: {output_dir}")
    print(f"Total topics: {len(topics)}")
    print(f"Total edges: {metadata['edge_counts']['total']}")
    print(f"Benchmark cases encoded: {len(evolves_to_edges)}")

    # Print subcategory breakdown
    for subcat in target_subcategories:
        subcat_topics = [t for t in topics.values() if t['subcategory'] == subcat]
        print(f"  math.{subcat}: {len(subcat_topics)} topics")

    return 0


# Wrapper functions for testing

def load_hierarchy_data(filepath: str) -> dict:
    """Load hierarchy data from JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def parse_benchmark_docs(lo_filepath: str, ag_filepath: str) -> list[dict]:
    """Parse both benchmark documents and return combined cases."""
    with open(lo_filepath, 'r') as f:
        lo_content = f.read()
    with open(ag_filepath, 'r') as f:
        ag_content = f.read()

    lo_cases = parse_benchmark_cases(lo_content)
    ag_cases = parse_math_ag_benchmark_cases(ag_content)

    return lo_cases + ag_cases


def export_kg_v1(input_file: str, benchmark_lo: str, benchmark_ag: str, output_dir: str, benchmark_pr: str = None) -> dict:
    """Export KG v1 and return export statistics."""
    import sys
    # Save original args
    original_args = sys.argv
    try:
        sys.argv = [
            'math_kg_export.py',
            '--input', input_file,
            '--benchmark-lo', benchmark_lo,
            '--benchmark-ag', benchmark_ag,
            '--output-dir', output_dir
        ]
        if benchmark_pr:
            sys.argv.extend(['--benchmark-pr', benchmark_pr])
        result = main()
        return {'success': result == 0}
    finally:
        sys.argv = original_args


def parse_pr_docs(pr_filepath: str) -> list[dict]:
    """Parse PR curation document and return curated positive cases."""
    with open(pr_filepath, 'r') as f:
        content = f.read()
    return parse_pr_cases(content)


if __name__ == '__main__':
    exit(main())
