# 🎯 Interview Q&A Generator — Powered by LangGraph

An AI-powered Interview Q&A Generator built using **LangGraph's Command primitive**, **Send API**, and **Subgraph** architecture. Users input a domain, difficulty level, and number of questions — the system generates structured interview questions, concurrently generates answers, merges them, and delivers a **styled downloadable PDF**.

---

## 🚀 Demo

> Enter domain → Select level → Click Generate → Download PDF instantly!

---

## 🧠 LangGraph Concepts Applied

| Concept | Where Used |
|---|---|
| `Command(update)` | Stores questions from structured output into state |
| `Command(goto)` | Routes `question_generator` → `continue_to_answer` |
| `Send API` | Fires concurrent answer generation per question |
| `Reducer (operator.add)` | Accumulates answers from Send API into `list[str]` |
| `Subgraph` | ZIP merges questions + answers into Q&A pairs |
| `Command.PARENT` | Exits subgraph back to parent graph |
| `LangSmith` | Traces every node execution end-to-end |

---

## ⚙️ Architecture

```
User Input (Streamlit)
  domain | no_of_questions | tone
        │
        ▼
┌─────────────────────────┐
│   Question Generator     │  ← Structured Output (list[str])
│   Command(update+goto)   │
└─────────────────────────┘
        │
        ▼
┌─────────────────────────┐
│   Send API Dispatcher    │  ← Fires one Send per question
└─────────────────────────┘
        │
        ▼ (concurrent)
┌─────────────────────────┐
│   Answer Generator       │  ← Groq LLM | Reducer accumulates answers
└─────────────────────────┘
        │
        ▼
┌─────────────────────────┐
│      SUBGRAPH            │
│   QA Merger (ZIP)        │  ← [{Q1: q, A1: a}, {Q2: q, A2: a}...]
│   Command.PARENT         │  ← Exits back to parent graph
└─────────────────────────┘
        │
        ▼
┌─────────────────────────┐
│   PDF Generator          │  ← Styled PDF with headers, colors, sections
└─────────────────────────┘
        │
        ▼
  📥 Download PDF (Streamlit)
```

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![LangGraph](https://img.shields.io/badge/LangGraph-Agentic-orange)
![LangChain](https://img.shields.io/badge/LangChain-Framework-green)
![LangSmith](https://img.shields.io/badge/LangSmith-Tracing-purple)
![Groq](https://img.shields.io/badge/Groq-LLM-red)
![Pydantic](https://img.shields.io/badge/Pydantic-Validation-pink)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-teal)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)
![fpdf2](https://img.shields.io/badge/fpdf2-PDF-grey)

---

## 📁 Project Structure

```
Langgraph_Question_Answer_System/
├── fastapi_app.py              # FastAPI backend — POST /generate
├── streamlit_app.py            # Streamlit frontend — UI + Download
├── requirements.txt
├── .env.example
└── src/
    ├── states/
    │   └── state.py            # State, SubgraphState, Questions (Pydantic)
    ├── nodes/
    │   └── nodes.py            # All LangGraph nodes
    ├── graph/
    │   └── graph.py            # Parent graph + Subgraph builder
    └── utils/
        └── model_loader.py     # Groq LLM + Structured Output loader
```

---

## 🔧 Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/ChinmaiNatukula/Langgraph_Question_Answer_System.git
cd Langgraph_Question_Answer_System
```

### 2. Create virtual environment
```bash
uv init .
uv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
uv add -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
```
Add your keys to `.env`:
```
GROQ_API_KEY=your_groq_api_key
LANGSMITH_API_KEY=your_langsmith_api_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=QA-Generator
```

---

## ▶️ Run the Application

### Terminal 1 — Start FastAPI
```bash
uvicorn fastapi_app:app --reload
```

### Terminal 2 — Start Streamlit
```bash
streamlit run main.py
```

Open `http://localhost:8501` in your browser 🚀

---

## 📄 Sample Output

| Field | Value |
|---|---|
| Domain | Machine Learning |
| Level | Intermediate |
| Questions | 5 |

Generated PDF includes styled Q&A pairs with:
- 🔵 Blue question blocks
- 🟢 Green answer blocks
- Separator lines between each pair
- Header with domain + level
- Page numbers in footer

---

## 👨‍💻 Author

- 💼 Actively looking for **AI Internship** or **Junior Agentic AI** roles

---

## 📌 Key Learnings

> `Command` is not just a return value — it's a **remote control** for your entire graph execution.
> Combining `update + goto + subgraph + Send API` unlocks truly dynamic agentic workflows.

---

⭐ **If you found this useful, give it a star!**

