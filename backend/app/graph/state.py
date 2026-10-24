from operator import add
from typing import Annotated, TypedDict

DEPTH_QUESTIONS = {"Quick": 3, "Standard": 4, "Deep": 6}


class State(TypedDict, total=False):
    topic: str
    depth: str
    outline: list[dict]                       # {id, text, status}
    findings: Annotated[list[dict], add]      # reducer: parallel researchers append safely
    critique: list[dict]                      # {question_id, verdict, followup_query}
    iteration: int
    report: str
    sources: list[dict]
