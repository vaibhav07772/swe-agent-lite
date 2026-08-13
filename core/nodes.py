from dotenv import load_dotenv
load_dotenv()  # <-- YE SABSE PEHLE CHAHIYE!

from .state import AgentState
from .prompts import PLANNER_PROMPT, CODER_PROMPT, TESTER_PROMPT, REVIEWER_PROMPT
from .tools import get_issue_details, get_repo_structure, clone_repo, apply_diff_and_run_tests, create_pull_request
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
import json
import os
import tempfile
import shutil

llm = ChatGroq(
    model="llama-3.3-70b-versatile",  # Fast and free
    temperature=0.2,
    api_key=os.getenv("GROQ_API_KEY")
)

def planner_node(state: AgentState):
    """PLANNER: Understands the issue and decides which files to change."""
    issue_details = get_issue_details(state["repo_url"], state["issue_number"])
    state["issue_body"] = issue_details["body"]
    
    structure = get_repo_structure(issue_details["repo_full_name"])
    state["repo_structure"] = structure
    
    prompt = PLANNER_PROMPT.format(
        repo_structure=structure,
        issue_body=state["issue_body"]
    )
    
    messages = [
        SystemMessage(content="You are a software architect. Respond only in valid JSON."),
        HumanMessage(content=prompt)
    ]
    response = llm.invoke(messages)
    
    try:
        # Extract JSON from response
        response_text = response.content
        start = response_text.find('{')
        end = response_text.rfind('}') + 1
        json_str = response_text[start:end]
        plan_data = json.loads(json_str)
        state["target_files"] = plan_data.get("files_to_change", [])
        state["status"] = "CODING"
    except:
        state["target_files"] = []
        state["status"] = "CODING"
    
    return state

def coder_node(state: AgentState):
    """CODER: Generates the code diff."""
    prompt = CODER_PROMPT.format(
        issue_body=state["issue_body"],
        plan="Fix the issue based on the description.",
        target_files=state["target_files"]
    )
    
    messages = [
        SystemMessage(content="You are a senior engineer. Generate a unified diff."),
        HumanMessage(content=prompt)
    ]
    response = llm.invoke(messages)
    state["code_diff"] = response.content
    state["status"] = "TESTING"
    return state

def tester_node(state: AgentState):
    """TESTER: Applies diff, runs tests, returns result."""
    # Clone repo into a temp sandbox
    temp_dir = tempfile.mkdtemp()
    try:
        clone_repo(state["repo_url"], temp_dir)
        
        # Try to detect test command (simple heuristic)
        test_cmd = "pytest"
        if os.path.exists(os.path.join(temp_dir, "package.json")):
            test_cmd = "npm test"
        elif os.path.exists(os.path.join(temp_dir, "pytest.ini")):
            test_cmd = "pytest"
        elif os.path.exists(os.path.join(temp_dir, "manage.py")):
            test_cmd = "python manage.py test"
        else:
            test_cmd = "pytest"  # default
        
        state["test_command"] = test_cmd
        
        # Apply diff and run tests
        result = apply_diff_and_run_tests(temp_dir, state["code_diff"], test_cmd)
        
        state["test_output"] = result["output"]
        state["test_passed"] = result["success"]
        state["status"] = "REVIEWING"
        
    except Exception as e:
        state["test_output"] = str(e)
        state["test_passed"] = False
        state["status"] = "REVIEWING"
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    return state

def reviewer_node(state: AgentState):
    """REVIEWER: Decides if PR should be created or loop back."""
    if state["test_passed"]:
        state["status"] = "DONE"
        # Create PR
        temp_dir = tempfile.mkdtemp()
        try:
            clone_repo(state["repo_url"], temp_dir)
            pr_url = create_pull_request(
                state["repo_url"], 
                state["issue_number"], 
                state["code_diff"], 
                temp_dir
            )
            state["pr_url"] = pr_url
        except Exception as e:
            state["error_log"] = str(e)
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
    else:
        state["status"] = "FAILED"
        # We can loop back to CODER with feedback here (simplified, we'll just stop for demo)
    
    return state