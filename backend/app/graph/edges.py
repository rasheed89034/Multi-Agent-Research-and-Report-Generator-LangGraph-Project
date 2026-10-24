# from langgraph.types import Send
# from app.config import settings


# def fan_out(state):
#     """One researcher per question that still needs work (all on the first pass, only weak ones on retries)."""
#     verdicts = {c["question_id"]: c for c in state.get("critique", [])}
#     sends = []
#     for q in state["outline"]:
#         c = verdicts.get(q["id"])
#         if c is None:
#             sends.append(Send("researcher", {"question": q, "query": q["text"]}))
#         elif c["verdict"] != "supported":
#             sends.append(Send("researcher", {"question": q, "query": c.get("followup_query") or q["text"], "retry": True}))
#     return sends


# def after_critic(state):
#     """Loop back to research while evidence is weak, capped so cost can't run away."""
#     needs_work = any(c["verdict"] != "supported" for c in state["critique"])
#     if needs_work and state["iteration"] <= settings.max_iterations:
#         return fan_out(state)
#     return "writer"


from langgraph.types import Send
from app.config import settings

EVIDENCE_TERMS = "systematic review study evidence"


def search_query(q: dict) -> str:
    """Evaluative questions get evidence-oriented terms so results lean toward reviews and studies, not promotion."""
    return q["text"] if q.get("kind", "factual") == "factual" else f"{q['text']} {EVIDENCE_TERMS}"


def fan_out(state):
    """One researcher per question that still needs work (all on the first pass, only weak ones on retries)."""
    verdicts = {c["question_id"]: c for c in state.get("critique", [])}
    sends = []
    for q in state["outline"]:
        c = verdicts.get(q["id"])
        if c is None:
            sends.append(Send("researcher", {"question": q, "query": search_query(q)}))
        elif c["verdict"] != "supported":
            sends.append(Send("researcher", {"question": q, "query": c.get("followup_query") or search_query(q), "retry": True}))
    return sends


def after_critic(state):
    """Loop back to research while evidence is weak, capped so cost can't run away."""
    needs_work = any(c["verdict"] != "supported" for c in state["critique"])
    if needs_work and state["iteration"] <= settings.max_iterations:
        return fan_out(state)
    return "writer"
