from langgraph.graph import END, START, StateGraph

from src.nodes import (
    evaluate_node,
    generate_node,
    retry_node,
    route_after_evaluation,
)
from src.state import AgentState


def build_workflow():
    """Build the self-evaluating lesson workflow."""

    graph = StateGraph(AgentState)

    graph.add_node("generate", generate_node)
    graph.add_node("evaluate", evaluate_node)
    graph.add_node("retry", retry_node)

    graph.add_edge(START, "generate")
    graph.add_edge("generate", "evaluate")

    graph.add_conditional_edges(
        "evaluate",
        route_after_evaluation,
        {
            "ship": END,
            "retry": "retry",
        },
    )

    graph.add_edge("retry", "generate")

    return graph.compile()