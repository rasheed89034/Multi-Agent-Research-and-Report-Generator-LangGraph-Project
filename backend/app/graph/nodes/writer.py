# from langgraph.config import get_stream_writer
# from app.graph.llm import as_text, main_llm


# async def writer(state):
#     emit = get_stream_writer()
#     emit({"type": "node_start", "node": "writer", "id": "writer", "label": "Writer"})
#     sources, idx = [], {}
#     for f in state.get("findings", []):
#         u = f["source"]["url"]
#         if u not in idx:
#             sources.append(f["source"])
#             idx[u] = len(sources)
#     facts = "\n".join(f"- [{idx[f['source']['url']]}] ({f['questionId']}) {f['claim']}" for f in state.get("findings", []))
#     questions = "\n".join(f"{q['id']}: {q['text']}" for q in state["outline"])
#     gaps = ", ".join(c["question_id"] for c in state.get("critique", []) if c["verdict"] != "supported") or "none"
#     resp = await main_llm().ainvoke(
#         f"Write a research report on: {state['topic']}\n\nQuestions to cover:\n{questions}\n\nVerified facts (the ONLY facts you may use):\n{facts}\n\n"
#         "Rules: start with '# <title>', then '## ' sections. Plain paragraphs only (no bullets, tables or bold). "
#         "Put each paragraph on its own line. Cite every claim with its number like [1] or [1][3]. "
#         f"Never state anything without a citation. Questions with weak evidence: {gaps}. If any, end with a short '## Gaps' section saying so."
#     )
#     markdown = as_text(resp.content)
#     emit({"type": "report", "markdown": markdown, "sources": sources})
#     emit({"type": "node_end", "node": "writer", "id": "writer"})
#     return {"report": markdown, "sources": sources}


from langgraph.config import get_stream_writer
from app.graph.citations import finalize
from app.graph.llm import as_text, main_llm
from app.tools.sources import source_kind


async def writer(state):
    emit = get_stream_writer()
    emit({"type": "node_start", "node": "writer", "id": "writer", "label": "Writer"})
    findings = state.get("findings", [])
    sources, idx = [], {}
    for f in findings:
        u = f["source"]["url"]
        if u not in idx:
            sources.append(f["source"])
            idx[u] = len(sources)

    weak_ids = {c["question_id"] for c in state.get("critique", []) if c["verdict"] != "supported"}
    sections = []
    for q in state["outline"]:
        facts = [f"  - [{idx[f['source']['url']]}] {f['claim']}" for f in findings if f["questionId"] == q["id"]]
        note = " (evidence is limited)" if q["id"] in weak_ids else ""
        sections.append(f"Question: {q['text']}{note}\n" + ("\n".join(facts) or "  - no verified evidence found"))
    source_list = "\n".join(f"[{i}] {s['domain']} ({source_kind(s['domain'])})" for i, s in enumerate(sources, 1))

    resp = await main_llm().ainvoke(
        f"Write a research report on: {state['topic']}\n\n"
        f"Material, grouped by question. This is the ONLY information you may use:\n\n" + "\n\n".join(sections) +
        f"\n\nSources:\n{source_list}\n\n"
        "Rules:\n"
        "- Start with '# <title>', then '## ' sections. Plain paragraphs only (no bullets, tables or bold), one paragraph per line.\n"
        "- Cite every claim with its source number like [1] or [1][3]. Use only numbers from the source list. Never state anything without a citation.\n"
        "- Do not add claims, adjectives or framing that the material does not support.\n"
        "- Weigh independent (academic/official) sources above sources that promote or sell the subject, and say when a claim rests only on promotional sources.\n"
        "- Report criticism and limits of evidence plainly. Do not call a matter 'debated' unless the material shows real disagreement among independent sources.\n"
        "- If evidence on a topic is limited or missing, end with a short '## Limits of the evidence' section describing what could not be established, in plain words for a reader.\n"
        "- Never mention question ids, prompts, instructions, 'verified facts' or the research process."
    )
    markdown, used = finalize(as_text(resp.content), sources)
    emit({"type": "report", "markdown": markdown, "sources": used})
    emit({"type": "node_end", "node": "writer", "id": "writer"})
    return {"report": markdown, "sources": used}
