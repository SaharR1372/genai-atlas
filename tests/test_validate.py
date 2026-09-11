"""Tests for scripts/validate.py's schema + referential-integrity checks."""


def test_clean_sample_data_has_no_errors(validate_mod, sample_data_dir):
    errors, warnings, n_entities, n_relations = validate_mod.run(data_dir=sample_data_dir)
    assert errors == []
    assert n_entities == 2
    assert n_relations == 1


def test_dangling_relation_target_is_an_error(validate_mod, sample_data_dir):
    (sample_data_dir / "relations" / "generation.yaml").write_text(
        "- from: sd3-2024\n"
        "  to: does-not-exist\n"
        "  type: uses_objective_from\n"
        "  evidence: broken on purpose\n"
        "  confidence: high\n"
        "  added_by: sonnet\n"
        "  status: verified\n"
    )
    errors, warnings, _, _ = validate_mod.run(data_dir=sample_data_dir)
    assert any("does-not-exist" in e for e in errors)


def test_filename_id_mismatch_is_an_error(validate_mod, sample_data_dir):
    bad = sample_data_dir / "concepts" / "wrong-filename.yaml"
    bad.write_text(
        "id: flow-matching-v2\n"
        "type: concept\n"
        "name: Flow matching v2\n"
        "axis: objective\n"
        "one_line: test\n"
    )
    errors, warnings, _, _ = validate_mod.run(data_dir=sample_data_dir)
    assert any("does not match id" in e for e in errors)


def test_duplicate_id_across_files_is_an_error(validate_mod, sample_data_dir):
    dupe = sample_data_dir / "papers" / "sd3-2024-dupe.yaml"
    dupe.write_text(
        "id: sd3-2024\n"
        "type: paper\n"
        "title: Duplicate\n"
        "date: '2024-03'\n"
        "tier: landmark\n"
        "sections: [generation]\n"
        "status: {code: released, weights: released, verified: false}\n"
        "summary: dup.\n"
    )
    errors, warnings, _, _ = validate_mod.run(data_dir=sample_data_dir)
    assert any("duplicate id" in e for e in errors)


def test_invalid_enum_value_is_a_schema_error(validate_mod, sample_data_dir):
    bad = sample_data_dir / "papers" / "bad-tier.yaml"
    bad.write_text(
        "id: bad-tier\n"
        "type: paper\n"
        "title: Bad tier paper\n"
        "date: '2024-03'\n"
        "tier: super-legendary\n"  # not a valid tier
        "sections: [generation]\n"
        "status: {code: released, weights: released, verified: false}\n"
        "summary: test.\n"
    )
    errors, warnings, _, _ = validate_mod.run(data_dir=sample_data_dir)
    assert any("bad-tier.yaml" in e for e in errors)


def test_real_repo_data_validates_clean(validate_mod):
    """Regression test: whatever is currently checked in must pass validation."""
    errors, warnings, n_entities, n_relations = validate_mod.run()
    assert errors == [], f"real data/ has validation errors: {errors}"


def test_line_arc_membership_must_be_declared_on_both_sides(validate_mod, sample_data_dir):
    """A line listing a paper in its arc, without that paper declaring the line, is an error."""
    (sample_data_dir / "lines").mkdir()
    (sample_data_dir / "lines" / "line-test.yaml").write_text(
        "id: line-test\n"
        "type: line\n"
        "name: Test line\n"
        "one_line: A test.\n"
        "core_bet: Testing.\n"
        "primary_axis: objective\n"
        "status: emerging\n"
        "sections: [generation]\n"
        "arc:\n"
        "  - paper: sd3-2024\n"
        "    role: origin\n"
        "    note: sd3 does not declare this line\n"
    )
    errors, _, _, _ = validate_mod.run(data_dir=sample_data_dir)
    assert any("does not declare lines" in e for e in errors)


def test_real_data_every_line_arc_paper_declares_membership(validate_mod):
    """Regression guard on the real atlas: line arcs and paper.lines must not drift apart."""
    errors, _, _, _ = validate_mod.run()
    assert not [e for e in errors if "does not declare lines" in e]


def test_thin_line_is_flagged(validate_mod, sample_data_dir):
    """A line with one or two papers may be a real gap; the atlas must not stay silent about it."""
    (sample_data_dir / "lines").mkdir(exist_ok=True)
    (sample_data_dir / "lines" / "line-thin.yaml").write_text(
        "id: line-thin\ntype: line\nname: Thin line\none_line: A test.\n"
        "core_bet: Testing.\nprimary_axis: objective\nstatus: emerging\n"
        "sections: [generation]\narc:\n  - paper: sd3-2024\n    role: origin\n    note: only one\n"
    )
    # the paper must declare the line, or a different error fires first
    p = sample_data_dir / "papers" / "sd3-2024.yaml"
    p.write_text(p.read_text() + "lines: [line-thin]\n")
    _, warnings, _, _ = validate_mod.run(data_dir=sample_data_dir)
    assert any("only 1 paper" in w for w in warnings)


def test_single_org_line_is_flagged(validate_mod, sample_data_dir):
    """
    A line whose every paper comes from one group is a blind spot. This is the exact failure a
    reader caught in the pixel-space line, where both entries were from the same lab.
    """
    (sample_data_dir / "lines").mkdir(exist_ok=True)
    for i, pid in enumerate(["one-lab-a", "one-lab-b"]):
        (sample_data_dir / "papers" / f"{pid}.yaml").write_text(
            f"id: {pid}\ntype: paper\ntitle: Paper {i}\ndate: '2026-01'\ntier: core\n"
            f"sections: [generation]\norgs: [OneLab]\nlines: [line-onelab]\n"
            "status: {code: none, weights: none, verified: false}\nsummary: test.\n"
        )
    (sample_data_dir / "lines" / "line-onelab.yaml").write_text(
        "id: line-onelab\ntype: line\nname: One lab\none_line: A test.\n"
        "core_bet: Testing.\nprimary_axis: objective\nstatus: emerging\nsections: [generation]\n"
        "arc:\n  - paper: one-lab-a\n    role: origin\n    note: a\n"
        "  - paper: one-lab-b\n    role: improvement\n    note: b\n"
    )
    _, warnings, _, _ = validate_mod.run(data_dir=sample_data_dir)
    assert any("every paper in this line is from OneLab" in w for w in warnings)


def test_sparse_line_over_long_window_is_flagged(validate_mod, sample_data_dir):
    """
    Four papers is not thin by count, but spread across many years it usually means the atlas
    has the endpoints and missed the middle. Modelled on the cascaded-pixel line, where the
    atlas held a 2021 paper and a 2024 paper and nothing between them.
    """
    (sample_data_dir / "lines").mkdir(exist_ok=True)
    for pid, date in [("gap-old", "2019-01"), ("gap-new", "2026-01")]:
        (sample_data_dir / "papers" / f"{pid}.yaml").write_text(
            f"id: {pid}\ntype: paper\ntitle: {pid}\ndate: '{date}'\ntier: core\n"
            f"sections: [generation]\norgs: [LabA, LabB]\nlines: [line-sparse]\n"
            "status: {code: none, weights: none, verified: false}\nsummary: test.\n"
        )
    (sample_data_dir / "lines" / "line-sparse.yaml").write_text(
        "id: line-sparse\ntype: line\nname: Sparse\none_line: A test.\n"
        "core_bet: Testing.\nprimary_axis: objective\nstatus: emerging\nsections: [generation]\n"
        "arc:\n  - paper: gap-old\n    role: origin\n    note: a\n"
        "  - paper: gap-new\n    role: improvement\n    note: b\n"
    )
    _, warnings, _, _ = validate_mod.run(data_dir=sample_data_dir)
    assert any("sparse across this long a window" in w for w in warnings)


def test_stale_ascendant_line_is_flagged(validate_mod, sample_data_dir):
    """
    Calling a line 'ascendant' is a claim about the present. If nothing has been added in
    eighteen months, either the claim is wrong or the atlas stopped following it.
    """
    (sample_data_dir / "lines").mkdir(exist_ok=True)
    for pid, date in [("stale-a", "2020-01"), ("stale-b", "2021-06"),
                      ("stale-c", "2022-01"), ("stale-d", "2022-03"), ("stale-e", "2022-06")]:
        (sample_data_dir / "papers" / f"{pid}.yaml").write_text(
            f"id: {pid}\ntype: paper\ntitle: {pid}\ndate: '{date}'\ntier: core\n"
            f"sections: [generation]\norgs: [LabA, LabB]\nlines: [line-stale]\n"
            "status: {code: none, weights: none, verified: false}\nsummary: test.\n"
        )
    arc = "".join(f"  - paper: stale-{c}\n    role: improvement\n    note: n\n" for c in "abcde")
    (sample_data_dir / "lines" / "line-stale.yaml").write_text(
        "id: line-stale\ntype: line\nname: Stale\none_line: A test.\n"
        "core_bet: Testing.\nprimary_axis: objective\nstatus: ascendant\nsections: [generation]\n"
        "arc:\n" + arc
    )
    _, warnings, _, _ = validate_mod.run(data_dir=sample_data_dir)
    assert any("on a line marked 'ascendant'" in w for w in warnings)
