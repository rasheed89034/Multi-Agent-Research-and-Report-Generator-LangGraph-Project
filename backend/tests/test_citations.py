from app.graph.citations import finalize

SRC = [{"url": f"https://s{i}.com", "domain": f"s{i}.com", "snippet": "x"} for i in (1, 2, 3)]


def test_invented_citation_removed():
    text, used = finalize("A claim [1]. Another [4].", SRC)
    assert "[4]" not in text and "[1]" in text and len(used) == 1


def test_renumbers_by_first_appearance_and_keeps_only_cited():
    text, used = finalize("X [3]. Y [1][3].", SRC)
    assert text == "X [1]. Y [2][1]."
    assert [s["domain"] for s in used] == ["s3.com", "s1.com"]


def test_markdown_link_citations_normalised():
    text, _ = finalize("Fact [2](https://s2.com).", SRC)
    assert text == "Fact [1]."


def test_comma_citations_split():
    text, used = finalize("Fact [1, 2].", SRC)
    assert text == "Fact [1][2]." and len(used) == 2
