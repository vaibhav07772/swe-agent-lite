from typing import TypedDict, List, Optional, Dict

class AgentState(TypedDict):
    repo_url: str
    issue_number: int
    issue_body: str
    repo_structure: str          # File tree summary
    target_files: List[str]      # Files to modify
    code_diff: str               # Proposed code changes (unified diff)
    test_command: str            # e.g., "pytest tests/"
    test_output: str             # Output of test run
    test_passed: bool
    pr_url: Optional[str]
    error_log: Optional[str]
    iteration: int
    status: str                  # PLANNING, CODING, TESTING, REVIEWING, DONE