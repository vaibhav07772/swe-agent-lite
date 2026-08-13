from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.graph import run_agent
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="SWE-Agent Lite", description="AI Software Engineer that fixes GitHub issues")

class IssueRequest(BaseModel):
    repo_url: str
    issue_number: int

@app.post("/fix-issue")
async def fix_issue(request: IssueRequest):
    try:
        result = run_agent(request.repo_url, request.issue_number)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "SWE-Agent Lite is running! Use POST /fix-issue"}