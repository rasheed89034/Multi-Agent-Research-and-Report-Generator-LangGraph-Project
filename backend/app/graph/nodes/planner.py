# from langgraph.config import get_stream_writer
# from langgraph.types import interrupt
# from app.graph.llm import main_llm
# from app.graph.state import DEPTH_QUESTIONS
# from app.schemas.models import Outline


# async def planner(state):
#     emit = get_stream_writer()
#     emit({"type": "node_start", "node": "planner", "id": "planner", "label": "Planner"})
#     n = DEPTH_QUESTIONS.get(state.get("depth", "Standard"), 4)
#     out = await main_llm().with_structured_output(Outline).ainvoke(
#         f"Break this research topic into {n} distinct, answerable sub-questions that together cover it.\nTopic: {state['topic']}"
#     )
#     outline = [{"id": f"q{i + 1}", "text": q, "status": "pending"} for i, q in enumerate(out.questions[:n])]
#     emit({"type": "node_end", "node": "planner", "id": "planner"})
#     return {"outline": outline, "iteration": 0, "findings": [], "critique": []}


# def approve(state):
#     """Human-in-the-loop: pauses the graph until the user resumes with an edited outline.
#     Keep this node free of side effects: it re-runs from the top on resume."""
#     edited = interrupt({"kind": "outline_approval", "outline": state["outline"]})
#     return {"outline": edited}


from langgraph.config import get_stream_writer
from langgraph.types import interrupt
from app.graph.llm import main_llm
from app.graph.state import DEPTH_QUESTIONS
from app.schemas.models import Outline

PROMPT = """Break this research topic into {n} distinct, answerable sub-questions that together cover it.
Rules:
- Each question must be self-contained.
- Label each one 'factual' or 'evaluative'. Evaluative means it asks about effectiveness, evidence quality, criticism, risks, controversy or comparisons.
- At least one question must be evaluative: ask what independent evidence, studies or experts say, including criticism and limitations. Do this for every topic, even ones that seem uncontroversial, so the report is balanced.

Topic: {topic}"""


async def planner(state):
    emit = get_stream_writer()
    emit({"type": "node_start", "node": "planner", "id": "planner", "label": "Planner"})
    n = DEPTH_QUESTIONS.get(state.get("depth", "Standard"), 4)
    out = await main_llm().with_structured_output(Outline).ainvoke(PROMPT.format(n=n, topic=state["topic"]))
    outline = [{"id": f"q{i + 1}", "text": q.text, "kind": q.kind, "status": "pending"} for i, q in enumerate(out.questions[:n])]
    emit({"type": "node_end", "node": "planner", "id": "planner"})
    return {"outline": outline, "iteration": 0, "findings": [], "critique": []}


def approve(state):
    """Human-in-the-loop: pauses the graph until the user resumes with an edited outline.
    Keep this node free of side effects: it re-runs from the top on resume."""
    edited = interrupt({"kind": "outline_approval", "outline": state["outline"]})
    return {"outline": edited}
