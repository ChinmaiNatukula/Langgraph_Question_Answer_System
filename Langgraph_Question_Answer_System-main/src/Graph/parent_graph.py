from src.Graph_State.state import State
from langgraph.graph import StateGraph, START, END
from src.Graph.sub_graph import get_subgraph
from src.Agent.agent import question_generator,answer_generator,pdf_generator,continue_to_answer

def main_graph():
    subgraph = get_subgraph()

    builder = StateGraph(State)

    # ✅ add all nodes
    builder.add_node("question_generator_node", question_generator)
    builder.add_node("answer_generator", answer_generator)
    builder.add_node("subgraph", subgraph)              # ✅ subgraph as node — shared keys exist
    builder.add_node("pdf_generator_node", pdf_generator)

    # ✅ edges
    builder.add_edge(START, "question_generator_node")

    # question_generator uses Command(goto) → continue_to_answer
    # ✅ Send API needs add_conditional_edges NOT add_edge
    builder.add_conditional_edges("question_generator_node", continue_to_answer, ["answer_generator"])
    builder.add_edge("answer_generator", "subgraph")
    app = builder.compile()
    
    return app
