from langgraph.types import Command
from src.Graph_State.state import SubgraphState

def qa_merger(state: SubgraphState):
    questions = state["questions"]
    answers = state["answers"]

    # ✅ zip combines Q+A pairs with Q1/A1 formatting
    qa_pairs = [
        {f"Q{i}": q, f"A{i}": a}
        for i, (q, a) in enumerate(zip(questions, answers), 1)
    ]

    # ✅ Command.PARENT — exit subgraph, land on pdf_generator in parent graph

    return Command(
        update={"qa_pairs": qa_pairs},
        graph=Command.PARENT,
        goto="pdf_generator_node"
    )