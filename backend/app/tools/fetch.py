import re
import httpx
from bs4 import BeautifulSoup
from app.tools.pdf import pdf_to_text


def _norm(s: str) -> str:
    return re.sub(r"\W+", " ", s).lower().strip()


def contains_quote(text: str, quote: str) -> bool:
    """Whitespace/punctuation-insensitive check that a quote really appears in the text."""
    q = _norm(quote)
    return len(q) >= 15 and q in _norm(text)


async def fetch_text(url: str, limit: int = 200_000) -> str:
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=15, headers={"User-Agent": "ResearchDesk/0.1"}) as c:
            r = await c.get(url)
            r.raise_for_status()
    except httpx.HTTPError:
        return ""
    if "pdf" in r.headers.get("content-type", "") or url.lower().endswith(".pdf"):
        return pdf_to_text(r.content)[:limit]
    soup = BeautifulSoup(r.text, "html.parser")
    for t in soup(["script", "style", "nav", "footer"]):
        t.decompose()
    return soup.get_text(" ", strip=True)[:limit]
