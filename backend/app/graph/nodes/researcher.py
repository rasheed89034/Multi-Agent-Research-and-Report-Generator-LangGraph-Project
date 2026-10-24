import asyncio
from urllib.parse import urlparse
from langgraph.config import get_stream_writer
from app.graph.llm import fast_llm
from app.schemas.models import Extraction
from app.tools.fetch import contains_quote, fetch_text
from app.tools.search import web_search


async def researcher(state):
    emit = get_stream_writer()
    q, query = state["question"], state["query"]
    nid = f"r-{q['id']}"
    label = f"Researcher {q['id'][1:]}" + (" (retry)" if state.get("retry") else "")
    emit({"type": "node_start", "node": "researcher", "id": nid, "label": label})

    results = await web_search(query)
    findings: list[dict] = []
    if results:
        sources = "\n\n".join(f"[{i}] {r['url']}\n{r['content']}" for i, r in enumerate(results))
        try:
            ext = await fast_llm().with_structured_output(Extraction).ainvoke(
                f"Question: {q['text']}\n\nSources:\n{sources}\n\n"
                "Extract up to 3 factual claims that answer the question. For each give the claim, an EXACT verbatim "
                "quote (under 30 words) copied from that source, the source number and your confidence (high, medium, or low). "
                "Use only what the sources say. If they don't answer the question, return no claims."
            )
        except Exception:
            try:
                ext = await fast_llm().with_structured_output(Extraction, method="json_mode").ainvoke(
                    f"Question: {q['text']}\n\nSources:\n{sources}\n\n"
                    "Extract up to 3 factual claims in JSON format matching 'claims': [{'claim': '...', 'quote': '...', 'source_index': 0, 'confidence': 'high|medium|low'}]."
                )
            except Exception:
                ext = Extraction(claims=[])
        used = sorted({c.source_index for c in ext.claims if 0 <= c.source_index < len(results)})
        pages = dict(zip(used, await asyncio.gather(*(fetch_text(results[i]["url"]) for i in used))))
        for c in ext.claims:
            if c.source_index not in pages:
                continue
            r = results[c.source_index]
            # Citation grounding: keep a claim only if its quote really appears in the page (or search excerpt).
            if not (contains_quote(pages[c.source_index], c.quote) or contains_quote(r["content"], c.quote)):
                continue
            f = {
                "questionId": q["id"], "claim": c.claim, "confidence": c.confidence,
                "source": {"url": r["url"], "domain": urlparse(r["url"]).netloc.removeprefix("www."), "snippet": c.quote},
            }
            findings.append(f)
            emit({"type": "finding", **f})

    emit({"type": "node_end", "node": "researcher", "id": nid})
    return {"findings": findings}
