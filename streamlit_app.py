import streamlit as st
import requests
import json
import time

# Page config
st.set_page_config(
    page_title="SWE-Agent Lite 🤖",
    page_icon="🤖",
    layout="wide"
)

# Title
st.title("🤖 SWE-Agent Lite: AI Software Engineer")
st.markdown("*Autonomously fixes GitHub issues using AI (LangGraph + Groq)*")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    api_url = st.text_input("FastAPI URL", value="http://localhost:8000/fix-issue")
    st.markdown("---")
    st.markdown("**How it works:**")
    st.markdown("1️⃣ Planner → Analyzes issue")
    st.markdown("2️⃣ Coder → Generates patch")
    st.markdown("3️⃣ Tester → Runs tests in sandbox")
    st.markdown("4️⃣ Reviewer → Creates PR if tests pass")
    st.markdown("---")
    st.caption("Made with ❤️ using LangGraph, Groq, GitHub API")

# Main input area
col1, col2 = st.columns([3, 1])

with col1:
    repo_url = st.text_input(
        "📦 Repository URL",
        placeholder="https://github.com/owner/repo",
        help="Enter the full GitHub repo URL"
    )

with col2:
    issue_number = st.number_input(
        "🔢 Issue Number",
        min_value=1,
        value=1,
        step=1,
        help="Issue number to fix"
    )

# Fix button
if st.button("🚀 Fix Issue", type="primary", use_container_width=True):
    if not repo_url:
        st.error("❌ Please enter a repository URL")
    else:
        # Payload
        payload = {
            "repo_url": repo_url,
            "issue_number": int(issue_number)
        }
        
        # Show progress
        with st.status("🤖 Agent is working on it...", expanded=True) as status:
            st.write("📡 Sending request to FastAPI backend...")
            
            try:
                # Call FastAPI
                response = requests.post(api_url, json=payload, timeout=300)
                
                if response.status_code == 200:
                    data = response.json()
                    result = data.get("data", {})
                    
                    status.update(label="✅ Agent finished!", state="complete")
                    
                    # Display results in tabs
                    tab1, tab2, tab3, tab4 = st.tabs(["📊 Summary", "💻 Code Diff", "🧪 Test Output", "📝 Full Response"])
                    
                    with tab1:
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            st.metric("Status", result.get("status", "UNKNOWN"))
                        with col_b:
                            st.metric("Tests Passed", "✅ Yes" if result.get("test_passed") else "❌ No")
                        with col_c:
                            if result.get("pr_url"):
                                st.success(f"🔗 [PR Created]({result['pr_url']})")
                            else:
                                st.info("ℹ️ No PR created")
                    
                    with tab2:
                        code_diff = result.get("code_diff", "No diff generated")
                        st.code(code_diff, language="diff")
                    
                    with tab3:
                        test_output = result.get("test_output", "No test output")
                        if result.get("test_passed"):
                            st.success(test_output)
                        else:
                            st.error(test_output)
                    
                    with tab4:
                        st.json(result)
                        
                else:
                    status.update(label="❌ Error!", state="error")
                    st.error(f"FastAPI error (Status {response.status_code}): {response.text}")
                    
            except requests.exceptions.ConnectionError:
                status.update(label="❌ Connection Error!", state="error")
                st.error("🚨 Could not connect to FastAPI server. Make sure it's running on `http://localhost:8000`")
                st.info("💡 Run this in another terminal: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`")
                
            except requests.exceptions.Timeout:
                status.update(label="⏰ Timeout!", state="error")
                st.error("⏰ The agent took too long to respond (timeout: 300s). Try a simpler issue.")
                
            except Exception as e:
                status.update(label="❌ Error!", state="error")
                st.error(f"Unexpected error: {str(e)}")

# Footer
st.markdown("---")
st.caption("⚠️ Note: This agent clones the repo, applies changes, runs tests, and creates a PR. Use on test repos first!")