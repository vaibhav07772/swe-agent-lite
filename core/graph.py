from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import planner_node, coder_node, tester_node, reviewer_node

def build_graph():
    builder = StateGraph(AgentState)
    
    builder.add_node("planner", planner_node)
    builder.add_node("coder", coder_node)
    builder.add_node("tester", tester_node)
    builder.add_node("reviewer", reviewer_node)
    
    builder.set_entry_point("planner")
    builder.add_edge("planner", "coder")
    builder.add_edge("coder", "tester")
    builder.add_edge("tester", "reviewer")
    builder.add_edge("reviewer", END)
    
    return builder.compile()

def run_agent(repo_url: str, issue_number: int):
    """Helper function to run the agent with initial state"""
    initial_state = {
        "repo_url": repo_url,
        "issue_number": issue_number,
        "issue_body": "",
        "repo_structure": "",
        "target_files": [],
        "code_diff": "",
        "test_command": "",
        "test_output": "",
        "test_passed": False,
        "pr_url": None,
        "error_log": None,
        "iteration": 0,
        "status": "PLANNING"
    }
    
    graph = build_graph()
    final_state = graph.invoke(initial_state)
    
    return {
        "status": final_state["status"],
        "pr_url": final_state.get("pr_url"),
        "test_passed": final_state.get("test_passed"),
        "test_output": final_state.get("test_output"),
        "code_diff": final_state.get("code_diff")
    }