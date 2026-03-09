
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from src.Graph.parent_graph import main_graph
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
graph = main_graph()


# ---- Request Schema ----
class QARequest(BaseModel):
    domain: str
    no_of_questions: int
    tone: str

# ---- POST /generate ----
# ✅ generate PDF and directly return FileResponse — no separate GET needed
@app.post("/generate")
def generate_qa(request: QARequest):
    result = graph.invoke({
        "domain": request.domain,
        "no_of_questions": request.no_of_questions,
        "tone": request.tone,
        "questions": [],
        "answers": [],
        "qa_pairs": [],
        "pdf_path": ""
    })

    pdf_path = result.get("pdf_path", "")

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=os.path.basename(pdf_path)
    )