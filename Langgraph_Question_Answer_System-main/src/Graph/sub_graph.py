from src.Graph_State.state import SubgraphState
from langgraph.graph import StateGraph, START, END
from src.Subgraph.subgraph_agent import qa_merger 

def get_subgraph():
    sub_builder = StateGraph(SubgraphState)
    sub_builder.add_node("qa_merger_node", qa_merger)
    sub_builder.add_edge(START, "qa_merger_node")

    subgraph = sub_builder.compile()
    return subgraph