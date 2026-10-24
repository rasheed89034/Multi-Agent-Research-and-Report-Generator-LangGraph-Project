from app.tools.fetch import contains_quote

PAGE = "Solid-state batteries replace the liquid electrolyte with a solid one, improving safety."


def test_quote_found_ignoring_case_and_punctuation():
    assert contains_quote(PAGE, "replace the liquid electrolyte with a solid one")


def test_invented_quote_rejected():
    assert not contains_quote(PAGE, "double the energy density of lithium-ion cells overnight")


def test_too_short_quote_rejected():
    assert not contains_quote(PAGE, "solid one")
