from typing import Literal
import operator
from typing import Annotated
from typing_extensions import TypedDict
from pydantic import BaseModel, field_validator
from src.Utility.load_model import get_model

model = get_model()


# ---- Structured Output ----
class Questions(BaseModel):
    question: list[str]

    # ✅ validator — if Groq returns single string instead of list, convert it
    @field_validator("question", mode="before")
    @classmethod
    def ensure_list(cls, v):
        if isinstance(v, str):
            return [v]      # ✅ wrap single string into list
        return v


structured_llm = model.with_structured_output(Questions)

# ---- Parent State ----
class State(TypedDict):
    domain: str
    no_of_questions: int
    tone: str
    questions: list[str]
    user_feedback: str                              # filled at once via structured output
    answers: Annotated[list[str], operator.add]     # accumulated via Send API + reducer
    qa_pairs: list[dict]                            # merged in subgraph via zip
    pdf_path: str                                   # pdf file path after generation


# ---- Subgraph State ----
class SubgraphState(TypedDict):
    questions: list[str]                            # shared key with parent
    answers: Annotated[list[str], operator.add]     # shared key with parent
    qa_pairs: list[dict]                            # shared key with parent