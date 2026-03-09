from langchain_core.prompts import ChatPromptTemplate
from typing import Literal
import os
import operator
from typing import Annotated
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from fpdf import FPDF
from src.Graph_State.state import State,structured_llm
from langgraph.types import Send,Command
from langgraph.graph import StateGraph, START, END
from src.Utility.load_model import get_model

model = get_model()

load_dotenv()
def question_generator(state: State):
    domain = state["domain"]
    no_of_questions = state["no_of_questions"]
    tone = state["tone"]

    prompt = ChatPromptTemplate.from_messages([
        ("system", f"""You are an expert technical interviewer specializing in {domain}.
Your task is to generate exactly {no_of_questions} unique interview questions.
Strict Rules:
- Questions must be strictly within {domain} only
- Do NOT include related or adjacent domains (e.g., if domain is Machine Learning, do NOT include Deep Learning, Neural Networks, NLP)
- Every question must be completely unique — no repetition or rephrasing of same concept
- Questions must be clear, concise and to the point
- Questions must be suitable for {tone} level candidates
- Questions must be in proper interview style (e.g., "What is...?", "How does...?", "Why is...?", "Explain the concept of...?")
- Do NOT generate any programming, coding or implementation based questions
- Do NOT ask to write functions, algorithms or code snippets"""),

        ("human", f"""Generate exactly {no_of_questions} unique {tone} level interview questions
strictly for the domain: {domain}.
Remember: 
- No repeated concepts
- Strictly {domain} only
- No coding or programming questions
- Interview style questions only""")
    ])

    response = structured_llm.invoke(prompt.format_messages(
        domain=domain,
        no_of_questions=no_of_questions,
        tone=tone
    ))

    # ✅ Command(update) — stores all questions at once into state
    return {"questions": response.question}


def continue_to_answer(state: State):
    return [
        Send("answer_generator", {
            "questions": q,
            "domain": state["domain"],
            "tone": state["tone"]
        })
        for q in state["questions"]
    ]



def answer_generator(state: State):
    question = state["questions"]
    domain = state["domain"]

    prompt = ChatPromptTemplate.from_messages([
        ("system", f"You are a {domain} expert. Answer in 2-3 sentences. No code. Direct and concise."),
        ("human", f"{question}")
    ])

    response = model.invoke(prompt.format_messages(
        domain=domain,
        question=question
    ))

    # ✅ reducer (operator.add) merges each answer into answers list
    return {"answers": [response.content]}


def pdf_generator(state: State):
    print("PDF GENERATOR CALLED")          # check if node runs
    print("qa_pairs:", state["qa_pairs"])   # check if qa_pairs is populated
    qa_pairs = state["qa_pairs"]
    domain = state["domain"]
    tone = state["tone"]

    class PDF(FPDF):
        def header(self):
            # ✅ styled header with background color
            self.set_fill_color(33, 97, 140)        # dark blue
            self.set_text_color(255, 255, 255)       # white
            self.set_font("Arial", "B", 18)
            self.cell(0, 15, f"{domain} Interview Q&A", ln=True, align="C", fill=True)
            self.set_font("Arial", "I", 11)
            self.cell(0, 8, f"Level: {tone.capitalize()}", ln=True, align="C", fill=True)
            self.ln(5)

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.set_text_color(150, 150, 150)
            self.cell(0, 10, f"Page {self.page_no()}", align="C")

    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    for pair in qa_pairs:
        for key, value in pair.items():
            if key.startswith("Q"):
                # ✅ Question section — blue background
                pdf.set_fill_color(214, 234, 248)   # light blue
                pdf.set_text_color(21, 67, 96)       # dark blue text
                pdf.set_font("Arial", "B", 12)
                pdf.multi_cell(0, 10, f"{key}. {value}", fill=True)
                pdf.ln(2)

            elif key.startswith("A"):
                # ✅ Answer section — green background
                pdf.set_fill_color(234, 250, 241)    # light green
                pdf.set_text_color(30, 132, 73)      # dark green text
                pdf.set_font("Arial", "", 11)
                pdf.multi_cell(0, 9, f"{key}. {value}", fill=True)
                pdf.ln(5)

        # ✅ separator line between QA pairs
        pdf.set_draw_color(189, 195, 199)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(4)

    # ✅ save PDF
    os.makedirs("src/outputs", exist_ok=True)
    pdf_path = f"src/outputs/{domain.replace(' ', '_')}_QA.pdf"
    pdf.output(pdf_path)

    return Command(
        update={"pdf_path": pdf_path},
        goto=END
    )