from app.tools.sources import source_kind


def test_kinds():
    assert source_kind("www.ncbi.nlm.nih.gov") == "academic/official"
    assert source_kind("cs.ox.ac.uk") == "academic/official"
    assert source_kind("mit.edu") == "academic/official"
    assert source_kind("en.wikipedia.org") == "reference"
    assert source_kind("toolshero.com") == "general"
