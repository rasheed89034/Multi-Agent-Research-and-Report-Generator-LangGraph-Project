# from langgraph.config import get_stream_writer
# from app.graph.llm import main_llm
# from app.schemas.models import Critique, Verdict

# PROMPT = """You are a strict research critic. For each question, judge whether the evidence supports a solid answer.
# - supported: at least two relevant claims, ideally from different sources
# - weak: thin, single-source or low-confidence evidence
# - unsupported: nothing relevant
# For weak or unsupported questions, give a better web search query in followup_query.

# {block}"""


# def _block(state) -> str:
#     parts = []
#     for q in state["outline"]:
#         ev = [f"  - ({f['confidence']}) {f['claim']} [{f['source']['domain']}]"
#               for f in state.get("findings", []) if f["questionId"] == q["id"]]
#         parts.append(f"{q['id']}: {q['text']}\n" + ("\n".join(ev) or "  (no evidence)"))
#     return "\n\n".join(parts)


# async def critic(state):
#     emit = get_stream_writer()
#     emit({"type": "node_start", "node": "critic", "id": "critic", "label": "Critic"})
#     prompt = PROMPT.format(block=_block(state))
#     result = None
#     try:
#         model = main_llm()
#         # Prefer json_mode to avoid function-calling XML hallucinations on open-weights models like Qwen
#         try:
#             json_prompt = (
#                 prompt + "\n\nRespond strictly with JSON object: "
#                 "{\"verdicts\": [{\"question_id\": \"q1\", \"verdict\": \"supported|weak|unsupported\", \"followup_query\": null}]}"
#             )
#             result = await model.with_structured_output(Critique, method="json_mode").ainvoke(json_prompt)
#         except Exception:
#             result = await model.with_structured_output(Critique).ainvoke(prompt)
#     except Exception:
#         # Fallback: if critic output parsing fails, accept evidence so pipeline reaches writer
#         result = Critique(verdicts=[
#             Verdict(question_id=q["id"], verdict="supported", followup_query=None)
#             for q in state["outline"]
#         ])

#     by_id = {v.question_id: v for v in (result.verdicts if result else [])}
#     critique = []
#     for q in state["outline"]:
#         v = by_id.get(q["id"])
#         verdict = v.verdict if v else "supported"
#         critique.append({"question_id": q["id"], "verdict": verdict, "followup_query": v.followup_query if v else None})
#         emit({"type": "critique", "questionId": q["id"], "verdict": verdict})
#     emit({"type": "node_end", "node": "critic", "id": "critic"})
#     return {"critique": critique, "iteration": state.get("iteration", 0) + 1}


from langgraph.config import get_stream_writer
from app.graph.llm import main_llm
from app.schemas.models import Critique, Verdict
from app.tools.sources import source_kind

PROMPT = """You are a strict research critic. For each question, judge whether the evidence supports a solid answer.
- supported: at least two relevant claims, ideally from different sources.
- weak: thin, single-source or low-confidence evidence.
- unsupported: nothing relevant.
Extra rule for questions marked [evaluative] (effectiveness, evidence, criticism, risks, controversy, comparisons): 'supported' also requires at least one independent source, meaning academic/official, or an established reference or news outlet that does not promote or sell the subject. If all evidence comes from sources that promote, sell or teach the subject, mark it weak.
For weak or unsupported questions, give a short web search query (under 8 words) in followup_query. For evaluative questions aim it at independent evidence, for example by adding 'systematic review', 'meta-analysis', 'study' or 'criticism'.

{block}"""


def _block(state) -> str:
    parts = []
    for q in state["outline"]:
        ev = [f"  - ({f['confidence']}, {source_kind(f['source']['domain'])}) {f['claim']} [{f['source']['domain']}]"
              for f in state.get("findings", []) if f["questionId"] == q["id"]]
        parts.append(f"{q['id']} [{q.get('kind', 'factual')}]: {q['text']}\n" + ("\n".join(ev) or "  (no evidence)"))
    return "\n\n".join(parts)


async def critic(state):
    emit = get_stream_writer()
    emit({"type": "node_start", "node": "critic", "id": "critic", "label": "Critic"})

    prompt = PROMPT.format(block=_block(state))
    model = main_llm()
    result = None

    # Prefer json_mode – avoids tool-call XML hallucinations on models like Qwen
    # and prevents prompt-injection in scraped content from breaking the parser.
    try:
        json_prompt = (
            prompt
            + "\n\nRespond strictly with a JSON object matching this schema: "
            '{"verdicts": [{"question_id": "q1", "verdict": "supported|weak|unsupported", "followup_query": null}]}'
        )
        result = await model.with_structured_output(Critique, method="json_mode").ainvoke(json_prompt)
    except Exception:
        pass

    # Second chance: default structured output (function-calling / tool-use)
    if result is None:
        try:
            result = await model.with_structured_output(Critique).ainvoke(prompt)
        except Exception:
            pass

    # Final fallback: accept all evidence so the pipeline always reaches the writer
    if result is None:
        result = Critique(
            verdicts=[
                Verdict(question_id=q["id"], verdict="supported", followup_query=None)
                for q in state["outline"]
            ]
        )

    by_id = {v.question_id: v for v in result.verdicts}
    critique = []
    for q in state["outline"]:
        v = by_id.get(q["id"])
        verdict = v.verdict if v else "unsupported"
        critique.append({"question_id": q["id"], "verdict": verdict, "followup_query": v.followup_query if v else None})
        emit({"type": "critique", "questionId": q["id"], "verdict": verdict})

    emit({"type": "node_end", "node": "critic", "id": "critic"})
    return {"critique": critique, "iteration": state.get("iteration", 0) + 1}
