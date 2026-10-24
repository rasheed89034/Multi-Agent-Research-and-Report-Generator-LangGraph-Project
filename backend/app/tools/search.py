import asyncio
import logging
from ddgs import DDGS
from app.tools.fetch import fetch_text

log = logging.getLogger(__name__)


def _ddg(query: str, k: int) -> list[dict]:
    return DDGS().text(query, max_results=k)


async def web_search(query: str, k: int = 5) -> list[dict]:
    """Key-free web search (DuckDuckGo). Returns [{url, title, content}].
    Result snippets are short, so each page's text is fetched and used as the content the researcher reads.
    Empty list on failure so one bad search can't kill a run."""
    try:
        hits = await asyncio.to_thread(_ddg, query, k)
    except Exception:
        log.exception("search failed for %r", query)
        return []
    pages = await asyncio.gather(*(fetch_text(h["href"], limit=6000) for h in hits))
    return [
        {"url": h["href"], "title": h.get("title", ""), "content": page or h.get("body", "")}
        for h, page in zip(hits, pages)
    ]
