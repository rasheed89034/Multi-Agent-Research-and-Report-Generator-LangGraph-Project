"""Headless eval: python -m evals.citation_check
Auto-approves the outline, then reports coverage (questions supported) and citation validity (quotes found on the live page)."""
import asyncio
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from app.graph.build import build_graph
from app.tools.fetch import contains_quote, fetch_text

TOPICS = ["Solid-state batteries in 2026", "How retrieval-augmented generation fails", "Sodium-ion vs lithium-ion costs"]


async def run(topic: str) -> dict:
    g, cfg = build_graph(InMemorySaver()), {"configurable": {"thread_id": topic}}
    await g.ainvoke({"topic": topic, "depth": "Quick"}, cfg)
    outline = (await g.aget_state(cfg)).values["outline"]
    await g.ainvoke(Command(resume=outline), cfg)
    return (await g.aget_state(cfg)).values


async def main():
    for topic in TOPICS:
        v = await run(topic)
        crit = v.get("critique", [])
        coverage = sum(c["verdict"] == "supported" for c in crit) / max(len(crit), 1)
        pages: dict[str, str] = {}
        valid = 0
        for f in v["findings"]:
            u = f["source"]["url"]
            pages[u] = pages.get(u) or await fetch_text(u)
            valid += contains_quote(pages[u], f["source"]["snippet"])
        print(f"{topic}: coverage={coverage:.0%} citations_valid={valid}/{len(v['findings'])}")


if __name__ == "__main__":
    asyncio.run(main())
