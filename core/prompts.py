PLANNER_PROMPT = """
You are an expert software architect. 
You are given a GitHub issue and the repository file structure.

Repo Structure:
{repo_structure}

Issue Description:
{issue_body}

Task: Identify which files need to be changed and briefly explain your plan.
Return ONLY a JSON object with:
{{
  "files_to_change": ["file1.py", "file2.py"],
  "plan": "Describe what changes are needed in 2-3 sentences."
}}
"""

CODER_PROMPT = """
You are a senior software engineer. 
Write the exact code changes needed to fix the issue.

Issue: {issue_body}
Plan: {plan}
Target Files: {target_files}

Return ONLY the code diff in unified format (like git diff). 
Make sure to include the full file paths and line changes.
If you need to modify multiple files, separate each file diff with "---" and "+++".
"""

TESTER_PROMPT = """
You are a QA engineer. The code was fixed, but tests failed.

Test Output:
{test_output}

Previous Code Changes:
{code_diff}

Analyze the failure and suggest what needs to be corrected in 1-2 sentences.
"""

REVIEWER_PROMPT = """
You are a code reviewer. 
The AI proposed a fix for the issue: {issue_body}

Code Changes:
{code_diff}

Test Results:
{test_output}

If tests passed, return "APPROVE". If tests failed, return "REJECT" along with a short reason.
"""