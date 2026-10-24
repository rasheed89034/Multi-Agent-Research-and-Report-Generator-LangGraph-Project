ACADEMIC_HINTS = (
    "arxiv.org", "pubmed", "ncbi.nlm.nih.gov", "nature.com", "science.org", "sciencedirect.com", "springer.com",
    "wiley.com", "jstor.org", "doi.org", "semanticscholar.org", "plos.org", "thelancet.com", "bmj.com", "nejm.org",
    "openreview.net", "acm.org", "ieee.org", "cochrane.org", "who.int", "oecd.org", "worldbank.org",
)


def source_kind(domain: str) -> str:
    """Cheap, topic-independent label the critic and writer use to weigh sources."""
    d = domain.lower()
    if d.endswith(".edu") or ".edu." in d or ".ac." in d or d.endswith(".gov") or ".gov." in d or any(h in d for h in ACADEMIC_HINTS):
        return "academic/official"
    if "wikipedia.org" in d or "britannica.com" in d:
        return "reference"
    return "general"
