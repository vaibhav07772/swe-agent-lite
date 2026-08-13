# 🤖 SWE-Agent-Lite: AI Software Engineer

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/FastAPI-0.100+-green?style=for-the-badge&logo=fastapi" />
  <img src="https://img.shields.io/badge/LangGraph-Agentic-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Streamlit-UI-red?style=for-the-badge&logo=streamlit" />
  <img src="https://img.shields.io/badge/Groq-LLM-purple?style=for-the-badge" />
</p>

> **An autonomous AI agent that fixes GitHub issues, runs tests in an isolated sandbox, and creates production-ready Pull Requests—just like Devin, but fully open-source!**

---

## 🚀 Overview

**SWE-Agent-Lite** is a multi-agent system built with **LangGraph** that simulates a complete software engineering workflow:

1. **Planner** 🧠 → Analyzes the issue and identifies which files to change.
2. **Coder** 💻 → Generates the exact code patch (unified diff).
3. **Tester** 🧪 → Clones the repo into a sandbox, applies the patch, and runs tests.
4. **Reviewer** ✅ → If tests pass, creates a **Pull Request** automatically.

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Orchestration** | LangGraph (Stateful Multi-Agent) |
| **LLM Backend** | Groq (Llama 3.3 70B) - *Fastest inference* |
| **Backend API** | FastAPI |
| **Frontend UI** | Streamlit (Interactive Dashboard) |
| **Version Control** | PyGithub, GitPython |
| **Sandbox** | Local Temporary Directories (Docker-ready) |

---

## ✨ Key Features

- ✅ **End-to-End Automation**: From Issue to PR in one click.
- ⚡ **Fast Inference**: Powered by Groq's high-speed LLM.
- 🔒 **Sandboxed Testing**: Applies changes in isolated temp directories.
- 📊 **Beautiful UI**: Streamlit dashboard to monitor agent progress live.
- 🧠 **LangGraph Memory**: Retains state across Planner → Coder → Tester → Reviewer.

---

## 📦 Architecture Flow
```mermaid
graph TD
    A[User] -->|Inputs Repo + Issue| B(Streamlit UI)
    B -->|POST /fix-issue| C(FastAPI Server)
    C -->|Invoke Graph| D[LangGraph Agent]
    
    subgraph Agentic Workflow
        D1[1. Planner] -->|Analyzes Codebase| D2[2. Coder]
        D2 -->|Generates Patch| D3[3. Tester]
        D3 -->|Runs Tests| D4[4. Reviewer]
    end
    
    D3 -->|Clones + Applies| E[Isolated Sandbox (Local Temp)]
    D4 -->|Tests Passed?| F[GitHub API]
    F -->|Creates PR| G[Pull Request]


🏁 Getting Started
Prerequisites
Python 3.11+

Groq API Key (Free) - Get here

GitHub Personal Access Token - Create here (Scope: repo + workflow)



1. Clone & Setup
git clone https://github.com/vaibhav07772/swe-agent-lite.git
cd swe-agent-lite


2. Create Conda Environment
conda create -n swe-agent python=3.11 -y
conda activate swe-agent



3. Install Dependencies
pip install -r requirements.txt


4. Set Environment Variables
Create a .env file in the root:
GROQ_API_KEY=gsk_xxxxxxxxxxxx
GITHUB_TOKEN=github_pat_xxxxxxxxxxxx


5. Run the Application
Terminal 1 (Backend - FastAPI):
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


Terminal 2 (Frontend - Streamlit UI):
streamlit run streamlit_app.py


6. Access the UI
Open your browser and go to: http://localhost:8501


🧪 How to Test (Step-by-Step)
Prepare a Test Repo:
Create a dummy public repo (e.g., test-bot-repo).
Add a buggy file (e.g., calculator.py with a typo).
Create a simple test file (test_calculator.py) using pytest.

Create an Issue:
In your repo, create Issue #1 describing the bug.

Run the Agent:
In the Streamlit UI, paste your repo URL and Issue Number.
Click "🚀 Fix Issue".

Watch the Magic:
The agent will process the issue.
If tests pass, a Pull Request will be created automatically in your repo!


📂 Project Structure
swe-agent-lite/
├── app/
│   └── main.py           # FastAPI Endpoints
├── core/
│   ├── graph.py          # LangGraph Workflow Builder
│   ├── nodes.py          # Planner, Coder, Tester, Reviewer
│   ├── prompts.py        # System Prompts for LLM
│   ├── tools.py          # GitHub API, Git, Test Runner
│   └── state.py          # State Schema for LangGraph
├── streamlit_app.py      # Interactive UI
├── .env                  # API Keys (Not committed)
├── requirements.txt      # Python Dependencies
└── README.md



🔮 Future Improvements
□ Docker Sandbox support for secure code execution.
□ Support for JavaScript/Node.js repositories.
□ Loop back to Coder if tests fail (Self-Correction).
□ Integration with Slack/Email for notifications.


🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

📜 License
MIT License - Feel free to use, modify, and distribute.


🙏 Acknowledgements
LangChain/LangGraph for the amazing agentic framework.
Groq for the lightning-fast inference.
Streamlit for the seamless UI.


📬 Connect with Me
Author: Vaibhav Singh
GitHub: vaibhav07772
LinkedIn: Vaibhav Singh

