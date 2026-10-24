# from typing import Literal, Any
# from pydantic import BaseModel, Field, field_validator

# # ---- LLM structured outputs ----
# class Outline(BaseModel):
#     questions: list[str] = Field(description="Distinct, answerable sub-questions")

# class Claim(BaseModel):
#     claim: str
#     quote: str = Field(description="Exact verbatim quote from the source supporting the claim")
#     source_index: int
#     confidence: Literal["high", "medium", "low"] = "medium"

#     @field_validator("confidence", mode="before")
#     @classmethod
#     def validate_confidence(cls, v: Any) -> str:
#         if isinstance(v, (int, float)):
#             if v >= 0.7:
#                 return "high"
#             if v >= 0.4:
#                 return "medium"
#             return "low"
#         if isinstance(v, str):
#             v_low = v.lower().strip()
#             if v_low in ("high", "medium", "low"):
#                 return v_low
#         return "medium"

# class Extraction(BaseModel):
#     claims: list[Claim]

# class Verdict(BaseModel):
#     question_id: str
#     verdict: Literal["supported", "weak", "unsupported"]
#     followup_query: str | None = Field(default=None, description="Better web search query if not supported")

# class Critique(BaseModel):
#     verdicts: list[Verdict]

# # ---- API bodies ----
# class StartRun(BaseModel):
#     topic: str
#     depth: Literal["Quick", "Standard", "Deep"] = "Standard"
#     run_id: str | None = None

# class SubQuestionIn(BaseModel):
#     id: str
#     text: str
#     status: str = "pending"

# class ResumeRun(BaseModel):
#     outline: list[SubQuestionIn]


from typing import Literal
from pydantic import BaseModel, Field

# ---- LLM structured outputs ----
class PlannedQuestion(BaseModel):
    text: str = Field(description="A self-contained, answerable sub-question")
    kind: Literal["factual", "evaluative"] = Field(
        default="factual",
        description="evaluative = about effectiveness, evidence quality, criticism, risks, controversy or comparisons",
    )

class Outline(BaseModel):
    questions: list[PlannedQuestion]

class Claim(BaseModel):
    claim: str
    quote: str = Field(description="Exact verbatim quote from the source supporting the claim")
    source_index: int
    confidence: Literal["high", "medium", "low"]

class Extraction(BaseModel):
    claims: list[Claim]

class Verdict(BaseModel):
    question_id: str
    verdict: Literal["supported", "weak", "unsupported"]
    followup_query: str | None = Field(default=None, description="Better web search query if not supported")

class Critique(BaseModel):
    verdicts: list[Verdict]

# ---- API bodies ----
class StartRun(BaseModel):
    topic: str
    depth: Literal["Quick", "Standard", "Deep"] = "Standard"
    run_id: str | None = None

class SubQuestionIn(BaseModel):
    id: str
    text: str
    status: str = "pending"
    kind: str = "factual"

class ResumeRun(BaseModel):
    outline: list[SubQuestionIn]
