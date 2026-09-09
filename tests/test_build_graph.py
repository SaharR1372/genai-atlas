"""Tests for scripts/build_graph.py."""


def test_build_produces_matching_node_and_edge_counts(build_graph_mod, sample_data_dir):
    graph = build_graph_mod.build(data_dir=sample_data_dir)
    assert graph["node_count"] == 2
    assert graph["edge_count"] == 1
    ids = {n["id"] for n in graph["nodes"]}
    assert ids == {"flow-matching", "sd3-2024"}


def test_build_edge_has_expected_shape(build_graph_mod, sample_data_dir):
    graph = build_graph_mod.build(data_dir=sample_data_dir)
    edge = graph["edges"][0]
    assert edge["from"] == "sd3-2024"
    assert edge["to"] == "flow-matching"
    assert edge["type"] == "uses_objective_from"


def test_build_node_carries_nodeType_and_label(build_graph_mod, sample_data_dir):
    graph = build_graph_mod.build(data_dir=sample_data_dir)
    by_id = {n["id"]: n for n in graph["nodes"]}
    assert by_id["sd3-2024"]["nodeType"] == "papers"
    assert "Rectified Flow" in by_id["sd3-2024"]["label"]
    assert by_id["flow-matching"]["nodeType"] == "concepts"


def test_build_is_json_serializable(build_graph_mod, sample_data_dir, tmp_path):
    import json
    graph = build_graph_mod.build(data_dir=sample_data_dir)
    out = tmp_path / "graph.json"
    out.write_text(json.dumps(graph))
    assert json.loads(out.read_text())["node_count"] == 2
