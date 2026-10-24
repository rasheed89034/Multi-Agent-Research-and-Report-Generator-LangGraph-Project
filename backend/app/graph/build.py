from langgraph.graph import END, START, StateGraph
from app.graph.edges import after_critic, fan_out
from app.graph.nodes.critic import critic
from app.graph.nodes.planner import approve, planner
from app.graph.nodes.researcher import researcher
from app.graph.nodes.writer import writer
from app.graph.state import State


def build_graph(checkpointer):
    g = StateGraph(State)
    g.add_node("planner", planner)
    g.add_node("approve", approve)
    g.add_node("researcher", researcher)
    g.add_node("critic", critic)
    g.add_node("writer", writer)
    g.add_edge(START, "planner")
    g.add_edge("planner", "approve")
    g.add_conditional_edges("approve", fan_out, ["researcher"])
    g.add_edge("researcher", "critic")
    g.add_conditional_edges("critic", after_critic, ["researcher", "writer"])
    g.add_edge("writer", END)
    return g.compile(checkpointer=checkpointer)
