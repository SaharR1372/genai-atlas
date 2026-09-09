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
