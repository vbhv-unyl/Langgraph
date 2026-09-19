from typing import Dict, List, TypedDict
from langgraph.graph import StateGraph, END
import random

class AgentState(TypedDict):
    name: str
    numbers: List[int]
    counter: int

def greeting_node(state: AgentState) -> AgentState:
    """Greeting node which says hi to the person"""

    state["name"] = f"Hi there, {state["name"]}"
    state["counter"] = 0
    return state

def random_node(state: AgentState) -> AgentState:
    """Generates a random number from 0 to 10"""

    state["counter"] += 1
    state["numbers"].append(random.randint(0, 10))
    return state

def should_continue(state: AgentState) -> AgentState:
    """Function to decide what to do next"""

    if state["counter"] < 5:
        print("Entering loop", state["counter"])
        return "loop"
    else:
        return "exit"

graph = StateGraph(AgentState)

graph.add_node("greeting", greeting_node)
graph.add_node("random", random_node)
graph.add_edge("greeting", "random")

graph.add_conditional_edges(
    "random",               # source node
    should_continue,        # routing function
    {
        "loop": "random",   # self-loop back to same node
        "exit": END         # end the graph
    }
)

graph.set_entry_point("greeting")

app = graph.compile()

result = app.invoke({"name": "Doe", "counter": 0, "numbers": []})
print(result["numbers"])