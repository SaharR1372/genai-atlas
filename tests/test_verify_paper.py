"""Tests for scripts/verify_paper.py — no real network calls."""

SAMPLE_ATOM = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>http://arxiv.org/abs/2510.11690v1</id>
    <published>2025-10-13T17:59:59Z</published>
    <title>Diffusion Transformers with Representation Autoencoders</title>
    <summary>We revisit the design space of autoencoders used in latent diffusion
models, motivated by the intuition that image latents need not be
optimized for reconstruction alone.</summary>
    <author><name>Boyang Zheng</name></author>
    <author><name>Nanye Ma</name></author>
    <author><name>Shengbang Tong</name></author>
    <author><name>Saining Xie</name></author>
    <link title="pdf" href="http://arxiv.org/pdf/2510.11690v1" rel="related" type="application/pdf"/>
  </entry>
</feed>
"""


class _FakeResponse:
    def __init__(self, text):
        self.text = text

    def raise_for_status(self):
        pass


def test_fetch_arxiv_parses_atom_feed(verify_paper_mod, monkeypatch):
    def fake_get(url, params=None, timeout=None):
        assert params["id_list"] == "2510.11690"
        return _FakeResponse(SAMPLE_ATOM)

    monkeypatch.setattr(verify_paper_mod.requests, "get", fake_get)
    result = verify_paper_mod.fetch_arxiv("2510.11690")

    assert result["title"] == "Diffusion Transformers with Representation Autoencoders"
    assert result["authors"] == ["Boyang Zheng", "Nanye Ma", "Shengbang Tong", "Saining Xie"]
    assert result["published"] == "2025-10-13"
    assert "reconstruction alone" in result["summary"]
    assert result["pdf"] == "http://arxiv.org/pdf/2510.11690v1"


def test_fetch_arxiv_raises_on_error_entry(verify_paper_mod, monkeypatch):
    error_feed = SAMPLE_ATOM.replace(
        "<title>Diffusion Transformers with Representation Autoencoders</title>",
        "<title>Error</title>",
    )

    def fake_get(url, params=None, timeout=None):
        return _FakeResponse(error_feed)

    monkeypatch.setattr(verify_paper_mod.requests, "get", fake_get)
    try:
        verify_paper_mod.fetch_arxiv("0000.00000")
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_verify_one_writes_status_fields(verify_paper_mod, tmp_path, monkeypatch):
    papers_dir = tmp_path / "papers"
    papers_dir.mkdir()
    (papers_dir / "rae-2025.yaml").write_text(
        "id: rae-2025\n"
        "type: paper\n"
        "title: Diffusion Transformers with Representation Autoencoders\n"
        "arxiv: '2510.11690'\n"
        "date: '2025-10'\n"
        "tier: landmark\n"
        "sections: [rae]\n"
        "status: {code: released, weights: released, verified: false}\n"
        "summary: placeholder\n"
    )
    monkeypatch.setattr(verify_paper_mod, "PAPERS_DIR", papers_dir)

    def fake_get(url, params=None, timeout=None):
        return _FakeResponse(SAMPLE_ATOM)

    monkeypatch.setattr(verify_paper_mod.requests, "get", fake_get)

    ok = verify_paper_mod.verify_one("rae-2025", by="sonnet", dry_run=False)
    assert ok

    import yaml
    updated = yaml.safe_load((papers_dir / "rae-2025.yaml").read_text())
    assert updated["status"]["verified"] is True
    assert updated["status"]["verified_by"] == "sonnet"
    assert updated["status"]["verified_on"]  # non-empty date string
