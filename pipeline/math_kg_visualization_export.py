#!/usr/bin/env python3
"""
Math Knowledge Graph v1 Visualization Export

Transforms KG-02 baseline output into frontend-ready visualization bundles.
"""

import argparse
import json
import os
from pathlib import Path
from typing import Any, Iterable, Optional
from datetime import datetime


GRAPH_BAND_ORDER = ['baseline', 'bridge', 'boundary', 'review', 'contract', 'deferred']


def sort_graph_bands(graph_bands: Iterable[str]) -> list[str]:
    """Return graph bands in narrative order."""
    return sorted(
        graph_bands,
        key=lambda band: (GRAPH_BAND_ORDER.index(band) if band in GRAPH_BAND_ORDER else len(GRAPH_BAND_ORDER), band),
    )


def load_jsonl(filepath: str) -> list[dict]:
    """Load JSONL file."""
    data = []
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            for line in f:
                data.append(json.loads(line.strip()))
    return data


def load_json(filepath: str) -> Optional[dict]:
    """Load JSON file."""
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return None


def save_json(filepath: str, data: dict) -> None:
    """Save data to JSON file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def merge_count_maps(count_maps: list[dict[str, int]]) -> dict[str, int]:
    """Merge multiple count maps into one."""
    merged: dict[str, int] = {}
    for count_map in count_maps:
        for key, value in count_map.items():
            merged[key] = merged.get(key, 0) + value
    return merged


def build_node_display_attrs(node: dict) -> dict:
    """Build display attributes for a node."""
    # Determine node type
    if 'code' in node:
        node_type = 'subcategory'
    elif 'start_date' in node:
        node_type = 'period'
    else:
        node_type = 'topic'

    if node_type == 'topic':
        # Calculate display size based on papers and activity
        total_papers = node.get('total_papers', 0)
        active_periods = node.get('active_periods', 1)

        # Size formula: base + log scale for papers, bonus for multi-period
        import math
        display_size = 10 + min(30, math.log(total_papers + 1) * 5)
        if active_periods > 1:
            display_size += 5

        return {
            'id': node['id'],
            'label': node.get('name', node['id']),
            'kind': 'topic',
            'subcategory': node.get('subcategory', ''),
            'category': node.get('category', 'math'),
            'status': 'persistent' if active_periods >= 3 else 'transient',
            'display_size': round(display_size, 1),
            'active_periods': active_periods,
            'total_papers': total_papers,
            'keywords': node.get('keywords', [])[:5],  # Top 5 keywords
            'hierarchy_depth': node.get('hierarchy_depth', 1)
        }
    elif node_type == 'subcategory' or 'code' in node:
        return {
            'id': node.get('code', 'unknown'),
            'code': node.get('code', 'unknown'),
            'label': node.get('name', node.get('code', 'Unknown')),
            'kind': 'subcategory',
            'subcategory': node.get('code', '').replace('math.', ''),
            'status': node.get('status', 'ready'),
            'display_size': 25,  # Fixed larger size for subcategories
            'topic_count': node.get('topic_count', 0),
            'multi_period_count': node.get('multi_period_count', 0),
            'evidence_quality': node.get('evidence_quality', 'unknown')
        }
    else:
        # Period node
        return {
            'id': node.get('id', ''),
            'label': node.get('id', ''),
            'kind': 'period',
            'display_size': 8,
            'start_date': node.get('start_date', ''),
            'end_date': node.get('end_date', '')
        }


def build_edge_display_attrs(edge: dict) -> dict:
    """Build display attributes for an edge."""
    edge_type = edge.get('type', '')

    # Base edge attrs
    display = {
        'source': edge['source'],
        'target': edge['target'],
        'kind': edge_type,
        'display_weight': 1.0
    }

    # Edge-type specific attrs
    if edge_type == 'EVOLVES_TO':
        confidence = edge.get('confidence', 'unknown')
        evidence_type = edge.get('evidence_type', 'unknown')

        # Weight based on confidence
        weight_map = {
            'confirmed': 3.0,
            'positive': 3.0,
            'negative': 1.5,
            'ambiguous': 2.0,
            'inferred': 1.0
        }

        display.update({
            'evidence_type': evidence_type,
            'confidence': confidence,
            'benchmark_status': edge.get('benchmark_status', ''),
            'benchmark_case_id': edge.get('benchmark_case_id', ''),
            'expected_relation': edge.get('expected_relation', ''),
            'subcategory': edge.get('subcategory', ''),
            'graph_band': edge.get('graph_band', ''),
            'graph_layer': edge.get('graph_layer', ''),
            'graph_role': edge.get('graph_role', ''),
            'narrative_level': edge.get('narrative_level', ''),
            'narrative_note': edge.get('narrative_note', ''),
            'graph_export_status': edge.get('graph_export_status', ''),
            'display_weight': weight_map.get(confidence, 1.0),
            'is_bidirectional': False
        })
    elif edge_type == 'NEIGHBOR_OF':
        display.update({
            'evidence_type': 'data-derived',
            'confidence': 'data-derived',
            'weight': edge.get('weight', 0.5),
            'display_weight': 1.0 + (edge.get('weight', 0) * 2),
            'subcategory': edge.get('subcategory', '')
        })
    elif edge_type == 'PARENT_OF':
        display.update({
            'evidence_type': 'hierarchy-derived',
            'confidence': 'data-derived',
            'display_weight': 2.0
        })
    elif edge_type == 'ACTIVE_IN':
        display.update({
            'evidence_type': 'data-derived',
            'paper_count': edge.get('paper_count', 0),
            'display_weight': 1.0
        })
    else:
        # CONTAINS_TOPIC and others
        display.update({
            'evidence_type': 'data-derived',
            'display_weight': 1.5
        })

    return display


def build_graph_bundle(input_dir: str) -> dict:
    """Build the main graph bundle."""
    input_path = Path(input_dir)

    # Load all nodes
    topics = load_jsonl(input_path / 'nodes' / 'topics.jsonl')
    subcategories = load_jsonl(input_path / 'nodes' / 'subcategories.jsonl')
    periods = load_jsonl(input_path / 'nodes' / 'periods.jsonl')

    # Load all edges
    contains_topic = load_jsonl(input_path / 'edges' / 'contains_topic.jsonl')
    active_in = load_jsonl(input_path / 'edges' / 'active_in.jsonl')
    neighbor_of = load_jsonl(input_path / 'edges' / 'neighbor_of.jsonl')
    parent_of = load_jsonl(input_path / 'edges' / 'parent_of.jsonl')
    evolves_to = load_jsonl(input_path / 'edges' / 'evolves_to.jsonl')

    # Load metadata
    metadata = load_json(input_path / 'metadata.json') or {}
    domain_layers = metadata.get('domain_knowledge_layers', {})

    # Transform nodes with display attrs
    display_topics = [build_node_display_attrs(t) for t in topics]
    display_subcategories = [build_node_display_attrs(s) for s in subcategories]
    display_periods = [build_node_display_attrs(p) for p in periods]

    # Transform edges with display attrs
    all_edges = []
    for edge_list in [contains_topic, active_in, neighbor_of, parent_of, evolves_to]:
        all_edges.extend([build_edge_display_attrs(e) for e in edge_list])

    # Build filter metadata
    subcategory_codes = [s.get('code', '') for s in subcategories]
    edge_kinds = list(set(e['kind'] for e in all_edges))
    confidence_levels = list(set(
        e.get('confidence', '') for e in all_edges
        if e.get('confidence')
    ))
    period_ids = [p.get('id', '') for p in periods]
    encoded_graph_bands = {
        e.get('graph_band', '')
        for e in all_edges
        if e.get('graph_band')
    }
    narrative_graph_bands = set(encoded_graph_bands)
    domain_export_presences = set()
    topology_statuses = set()
    narrative_statuses = set()
    for domain_meta in domain_layers.values():
        narrative_graph_bands.update(domain_meta.get('visible_graph_bands', []))
        export_presence = domain_meta.get('export_presence')
        if export_presence:
            domain_export_presences.add(export_presence)
        topology_status = domain_meta.get('topology_status')
        if topology_status:
            topology_statuses.add(topology_status)
        narrative_status = domain_meta.get('narrative_status')
        if narrative_status:
            narrative_statuses.add(narrative_status)

    graph_bands = sort_graph_bands(narrative_graph_bands)
    encoded_graph_bands = sort_graph_bands(encoded_graph_bands)

    evolves_to_by_graph_band = {}
    for edge in evolves_to:
        graph_band = edge.get('graph_band')
        if not graph_band:
            continue
        evolves_to_by_graph_band[graph_band] = evolves_to_by_graph_band.get(graph_band, 0) + 1

    domain_export_presence_counts = {}
    narrative_case_band_counts = []
    narrative_case_export_counts = []
    narrative_layer_band_counts = []
    topology_status_counts = {}
    for domain_meta in domain_layers.values():
        export_presence = domain_meta.get('export_presence')
        if export_presence:
            domain_export_presence_counts[export_presence] = domain_export_presence_counts.get(export_presence, 0) + 1
        topology_status = domain_meta.get('topology_status')
        if topology_status:
            topology_status_counts[topology_status] = topology_status_counts.get(topology_status, 0) + 1
        narrative_case_band_counts.append(domain_meta.get('case_counts_by_graph_band', {}))
        narrative_case_export_counts.append(domain_meta.get('case_counts_by_export_status', {}))
        narrative_layer_band_counts.append(domain_meta.get('layer_counts_by_graph_band', {}))

    return {
        'version': 'kg_v1_visualization',
        'generated_at': datetime.now().isoformat(),
        'source': str(input_path),
        'metadata': metadata,
        'nodes': {
            'topics': display_topics,
            'subcategories': display_subcategories,
            'periods': display_periods,
            'total': len(display_topics) + len(display_subcategories) + len(display_periods)
        },
        'edges': {
            'all': all_edges,
            'by_kind': {
                'CONTAINS_TOPIC': [e for e in all_edges if e['kind'] == 'CONTAINS_TOPIC'],
                'ACTIVE_IN': [e for e in all_edges if e['kind'] == 'ACTIVE_IN'],
                'NEIGHBOR_OF': [e for e in all_edges if e['kind'] == 'NEIGHBOR_OF'],
                'PARENT_OF': [e for e in all_edges if e['kind'] == 'PARENT_OF'],
                'EVOLVES_TO': [e for e in all_edges if e['kind'] == 'EVOLVES_TO']
            },
            'total': len(all_edges)
        },
        'filters': {
            'subcategories': subcategory_codes,
            'edge_kinds': edge_kinds,
            'confidence_levels': confidence_levels,
            'periods': period_ids,
            'graph_bands': graph_bands,
            'encoded_graph_bands': encoded_graph_bands,
            'domain_export_presences': sorted(domain_export_presences),
            'topology_statuses': sorted(topology_statuses),
            'narrative_statuses': sorted(narrative_statuses),
        },
        'stats': {
            'topic_count': len(topics),
            'subcategory_count': len(subcategories),
            'period_count': len(periods),
            'edge_count': len(all_edges),
            'evolves_to_count': len(evolves_to),
            'evolves_to_by_confidence': {
                'confirmed': len([e for e in evolves_to if e.get('confidence') == 'confirmed']),
                'negative': len([e for e in evolves_to if e.get('confidence') == 'negative']),
                'ambiguous': len([e for e in evolves_to if e.get('confidence') == 'ambiguous'])
            },
            'evolves_to_by_graph_band': evolves_to_by_graph_band,
            'domain_count': len(domain_layers),
            'domain_export_presence_counts': domain_export_presence_counts,
            'domain_topology_status_counts': topology_status_counts,
            'narrative_case_count': sum(domain.get('case_count', 0) for domain in domain_layers.values()),
            'narrative_case_counts_by_graph_band': merge_count_maps(narrative_case_band_counts),
            'narrative_case_counts_by_export_status': merge_count_maps(narrative_case_export_counts),
            'narrative_layer_counts_by_graph_band': merge_count_maps(narrative_layer_band_counts),
        }
    }


def build_subgraph(bundle: dict, subcategory: str) -> dict:
    """Build a subgraph for a specific subcategory."""
    domain_code = f'math.{subcategory}'
    domain_meta = bundle.get('metadata', {}).get('domain_knowledge_layers', {}).get(domain_code, {})

    # Filter nodes by subcategory
    topics = [n for n in bundle['nodes']['topics'] if n.get('subcategory') == subcategory]
    topic_ids = {t['id'] for t in topics}

    # Get the subcategory node
    subcat_node = None
    for n in bundle['nodes']['subcategories']:
        if n.get('subcategory') == subcategory or n.get('id') == f'math.{subcategory}':
            subcat_node = n
            break
    subcat_node_id = subcat_node.get('id', '') if subcat_node else ''
    period_ids = {period['id'] for period in bundle['nodes']['periods']}

    # Filter edges that connect topics in this subcategory
    edges = []
    for e in bundle['edges']['all']:
        source = e['source']
        target = e['target']

        # Include edges where both source and target are in the topic set
        # Or edges connecting to the subcategory node
        if source in topic_ids and target in topic_ids:
            edges.append(e)
        elif source == subcat_node_id and target in topic_ids:
            edges.append(e)
        elif source in topic_ids and target in period_ids:
            edges.append(e)

    evolves_to_by_graph_band = {}
    encoded_case_ids = []
    for edge in edges:
        if edge.get('kind') != 'EVOLVES_TO':
            continue
        if edge.get('benchmark_case_id'):
            encoded_case_ids.append(edge['benchmark_case_id'])
        graph_band = edge.get('graph_band')
        if not graph_band:
            continue
        evolves_to_by_graph_band[graph_band] = evolves_to_by_graph_band.get(graph_band, 0) + 1

    return {
        'version': 'kg_v1_visualization',
        'subcategory': subcategory,
        'generated_at': datetime.now().isoformat(),
        'metadata': {
            'domain_code': domain_code,
            'export_presence': domain_meta.get('export_presence'),
            'topology_status': domain_meta.get('topology_status'),
            'graph_shape': domain_meta.get('graph_shape'),
            'summary': domain_meta.get('summary'),
            'selected_rule': domain_meta.get('selected_rule'),
            'candidate_rule': domain_meta.get('candidate_rule'),
            'narrative_status': domain_meta.get('narrative_status'),
            'baseline_truth_layer_keys': domain_meta.get('baseline_truth_layer_keys', []),
            'narrative_only_layer_keys': domain_meta.get('narrative_only_layer_keys', []),
            'visible_graph_bands': domain_meta.get('visible_graph_bands', []),
            'narrative_layers': domain_meta.get('layers', {}),
            'narrative_case_registry': domain_meta.get('case_registry', []),
            'encoded_case_ids': encoded_case_ids,
            'evolves_to_by_graph_band': evolves_to_by_graph_band,
            'case_counts_by_graph_band': domain_meta.get('case_counts_by_graph_band', {}),
            'case_counts_by_export_status': domain_meta.get('case_counts_by_export_status', {}),
            'layer_counts_by_graph_band': domain_meta.get('layer_counts_by_graph_band', {}),
        },
        'nodes': {
            'topics': topics,
            'subcategory': subcat_node,
            'total_topics': len(topics)
        },
        'edges': edges,
        'stats': {
            'topic_count': len(topics),
            'edge_count': len(edges),
            'evolves_to_count': len([e for e in edges if e['kind'] == 'EVOLVES_TO']),
            'evolves_to_by_graph_band': evolves_to_by_graph_band,
            'narrative_case_count': domain_meta.get('case_count', 0),
            'narrative_case_counts_by_graph_band': domain_meta.get('case_counts_by_graph_band', {}),
            'narrative_case_counts_by_export_status': domain_meta.get('case_counts_by_export_status', {}),
            'narrative_layer_counts_by_graph_band': domain_meta.get('layer_counts_by_graph_band', {}),
        }
    }


def build_timeline_summary(bundle: dict) -> dict:
    """Build timeline summary by period."""
    periods = bundle['nodes']['periods']
    active_in_edges = bundle['edges']['by_kind'].get('ACTIVE_IN', [])
    evolves_to_edges = bundle['edges']['by_kind'].get('EVOLVES_TO', [])

    timeline = []
    for period in periods:
        period_id = period['id']

        # Count active topics in this period
        active_topics = set()
        for e in active_in_edges:
            if e['target'] == period_id:
                active_topics.add(e['source'])

        # Count benchmark edges active in this period
        # (Approximation: edges where source is active)
        period_edges = [e for e in evolves_to_edges if e['source'] in active_topics]

        timeline.append({
            'period': period_id,
            'active_topic_count': len(active_topics),
            'benchmark_edge_count': len(period_edges),
            'subcategory_activity': {}
        })

    return {
        'version': 'kg_v1_visualization',
        'generated_at': datetime.now().isoformat(),
        'timeline': sorted(timeline, key=lambda x: x['period'])
    }


def build_legend() -> dict:
    """Build legend/schema definitions for frontend."""
    return {
        'version': 'kg_v1_visualization',
        'generated_at': datetime.now().isoformat(),
        'node_kinds': {
            'topic': {
                'description': 'Research topic from topic model',
                'display_attrs': ['id', 'label', 'status', 'display_size', 'active_periods', 'total_papers']
            },
            'subcategory': {
                'description': 'arXiv subcategory (e.g., math.LO)',
                'display_attrs': ['id', 'label', 'status', 'display_size', 'topic_count']
            },
            'period': {
                'description': 'Time period (month)',
                'display_attrs': ['id', 'label', 'display_size']
            }
        },
        'edge_kinds': {
            'CONTAINS_TOPIC': {
                'description': 'Subcategory contains topic',
                'display_color': '#94a3b8',
                'display_style': 'dashed'
            },
            'ACTIVE_IN': {
                'description': 'Topic active in period',
                'display_color': '#cbd5e1',
                'display_style': 'solid'
            },
            'NEIGHBOR_OF': {
                'description': 'Topics are neighbors',
                'display_color': '#64748b',
                'display_style': 'solid'
            },
            'PARENT_OF': {
                'description': 'Parent-child in hierarchy',
                'display_color': '#475569',
                'display_style': 'solid'
            },
            'EVOLVES_TO': {
                'description': 'Topic evolves to another',
                'display_color': '#3b82f6',
                'display_style': 'solid'
            }
        },
        'evidence_types': {
            'benchmark-confirmed': {
                'description': 'Verified by benchmark',
                'badge': '⭐',
                'color': '#22c55e'
            },
            'data-derived': {
                'description': 'Derived from graph data',
                'badge': '📊',
                'color': '#64748b'
            },
            'hierarchy-derived': {
                'description': 'Derived from hierarchy',
                'badge': '📁',
                'color': '#475569'
            },
            'provisional': {
                'description': 'Curated inferred relation (conditional, requires paper review)',
                'badge': '⚑',
                'color': '#a855f7'
            }
        },
        'integration_scopes': {
            'baseline': {
                'description': 'Included in production baseline (LO+AG benchmark-verified)',
                'color': '#22c55e'
            },
            'conditional': {
                'description': 'Conditional layer only (math.PR curated, not baseline-included)',
                'color': '#a855f7'
            }
        },
        'graph_bands': {
            'baseline': {
                'description': 'Mainline baseline truth already encoded as an EVOLVES_TO edge',
                'color': '#2563eb'
            },
            'bridge': {
                'description': 'Bridge-level support worth narrating around the mainline, without upgrading it to baseline truth',
                'color': '#0f766e'
            },
            'boundary': {
                'description': 'Nearby negative boundary that should stay outside the positive continuity story',
                'color': '#dc2626'
            },
            'review': {
                'description': 'Near-miss or disputed case kept review-only',
                'color': '#d97706'
            },
            'contract': {
                'description': 'Selected rule contract metadata, not baseline graph topology',
                'color': '#7c3aed'
            },
            'deferred': {
                'description': 'Deferred branch noted in metadata only',
                'color': '#6b7280'
            }
        },
        'graph_export_statuses': {
            'encoded_as_evolves_to': {
                'description': 'Present as an exported EVOLVES_TO edge'
            },
            'in_scope_metadata_only': {
                'description': 'Both topics are in the exported subgraph, but the case remains metadata-only'
            },
            'docs_only_outside_baseline_hierarchy': {
                'description': 'Tracked in docs, but at least one endpoint is outside the current baseline hierarchy slice'
            },
            'docs_only_outside_export_scope': {
                'description': 'Tracked in docs, but the domain is not part of the current baseline export scope'
            }
        },
        'domain_export_presence': {
            'baseline_subgraph': {
                'description': 'Domain has exported baseline topology plus narrative metadata'
            },
            'docs_only_narrative': {
                'description': 'Domain is represented through graph-facing narrative metadata only; no baseline nodes or EVOLVES_TO edges are exported'
            },
            'docs_only_contract': {
                'description': 'Domain is represented only through metadata/contract layers in this export'
            }
        },
        'domain_layer_fields': {
            'baseline_truth_layer_keys': {
                'description': 'Layer keys allowed to count as confirmed baseline truth when encoded'
            },
            'narrative_only_layer_keys': {
                'description': 'Layer keys that may be narrated or annotated, but must not be read as confirmed baseline truth'
            },
            'visible_graph_bands': {
                'description': 'Graph bands visible for this domain across encoded edges and metadata-only layers'
            }
        },
        'topology_statuses': {
            'baseline_topology_included': {
                'description': 'Domain contributes nodes/edges to the exported baseline topology'
            },
            'not_in_baseline_topology': {
                'description': 'Domain is visible only through metadata; baseline topology remains unchanged'
            }
        },
        'confidence_levels': {
            'confirmed': {
                'description': 'Confirmed evolution relation',
                'badge': '✓',
                'color': '#22c55e'
            },
            'negative': {
                'description': 'Negative case (no evolution)',
                'badge': '✗',
                'color': '#ef4444'
            },
            'ambiguous': {
                'description': 'Ambiguous relation',
                'badge': '?',
                'color': '#f59e0b'
            },
            'inferred': {
                'description': 'Inferred relation',
                'badge': '~',
                'color': '#3b82f6'
            },
            'data-derived': {
                'description': 'Data-derived relation',
                'badge': '',
                'color': '#64748b'
            }
        },
        'status_values': {
            'persistent': {
                'description': 'Topic active 3+ periods',
                'color': '#22c55e'
            },
            'transient': {
                'description': 'Topic active 1-2 periods',
                'color': '#f59e0b'
            },
            'ready': {
                'description': 'Subcategory ready for analysis',
                'color': '#22c55e'
            },
            'provisional': {
                'description': 'Subcategory needs curation',
                'color': '#f59e0b'
            }
        }
    }


def main():
    parser = argparse.ArgumentParser(description='Export Math KG v1 Visualization Bundle')
    parser.add_argument('--input-dir', required=True, help='Input KG v1 directory')
    parser.add_argument('--output-dir', required=True, help='Output visualization directory')
    args = parser.parse_args()

    print("Building visualization bundle...")

    # Build main bundle
    bundle = build_graph_bundle(args.input_dir)

    # Detect conditional bundle
    is_conditional = 'pr_conditional' in str(args.input_dir)
    bundle['is_conditional'] = is_conditional
    if is_conditional:
        bundle['conditional_scope'] = 'math.PR'
        bundle['gate_status'] = 'gate1_eligible'

    # Build subgraphs
    subgraph_lo = build_subgraph(bundle, 'LO')
    subgraph_ag = build_subgraph(bundle, 'AG')

    # Detect PR topics and conditionally build subgraph_pr
    has_pr_topics = any(
        t.get('subcategory') == 'PR'
        for t in bundle['nodes']['topics']
    )

    # Build timeline summary
    timeline = build_timeline_summary(bundle)

    # Build legend
    legend = build_legend()

    # Write output files
    output_path = Path(args.output_dir)

    save_json(output_path / 'graph_bundle.json', bundle)
    print(f"  Created graph_bundle.json ({bundle['stats']['topic_count']} topics, {bundle['stats']['edge_count']} edges)")

    save_json(output_path / 'subgraph_lo.json', subgraph_lo)
    print(f"  Created subgraph_lo.json ({subgraph_lo['stats']['topic_count']} topics, {subgraph_lo['stats']['evolves_to_count']} evolves_to)")

    save_json(output_path / 'subgraph_ag.json', subgraph_ag)
    print(f"  Created subgraph_ag.json ({subgraph_ag['stats']['topic_count']} topics, {subgraph_ag['stats']['evolves_to_count']} evolves_to)")

    if has_pr_topics:
        subgraph_pr = build_subgraph(bundle, 'PR')
        save_json(output_path / 'subgraph_pr.json', subgraph_pr)
        print(f"  Created subgraph_pr.json ({subgraph_pr['stats']['topic_count']} topics, {subgraph_pr['stats']['evolves_to_count']} evolves_to)")

    save_json(output_path / 'timeline_summary.json', timeline)
    print(f"  Created timeline_summary.json ({len(timeline['timeline'])} periods)")

    save_json(output_path / 'legend.json', legend)
    print("  Created legend.json")

    print(f"\nVisualization export complete!")
    print(f"Output directory: {output_path}")
    print(f"Total nodes: {bundle['nodes']['total']}")
    print(f"Total edges: {bundle['edges']['total']}")
    print(f"EVOLVES_TO edges: {bundle['stats']['evolves_to_count']}")

    return 0


if __name__ == '__main__':
    exit(main())
