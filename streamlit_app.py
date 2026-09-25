# -*- coding: utf-8 -*-
"""
Sarthika Autonomous Cognitive Architecture 3.0 (Level 3 Expert Micro-AGI)
Streamlit Web Application for 100% Free 24/7 Public Hosting on Streamlit Community Cloud.
"""

import os
import json
import streamlit as st
from sarthika_core import (
    create_sarthika_expert,
    GroqEngine,
    OpenAIEngine,
    MockCognitiveEngine,
    run_level3_benchmark
)

st.set_page_config(
    page_title="Sarthika 3.0: Level 3 Expert AGI Engine",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.3rem;
        font-weight: 700;
        color: #6366F1;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #6B7280;
        margin-bottom: 20px;
    }
    .badge-pill {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 8px;
    }
    .badge-purple { background-color: #EDE9FE; color: #6D28D9; }
    .badge-green { background-color: #DEF7EC; color: #03543F; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🧠 Sarthika Autonomous Cognitive Architecture 3.0</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Level-3 Expert Micro-AGI: Dual-Process Reasoning, Causal Mental Simulation & MCTS Lookahead</div>', unsafe_allow_html=True)
st.markdown("""
<div>
    <span class="badge-pill badge-purple">Dual-Process MCTS</span>
    <span class="badge-pill badge-green">Level-3 Expert AGI</span>
    <span class="badge-pill badge-purple">100% Free Cloud Deployment</span>
</div>
<hr style="margin-top: 15px; margin-bottom: 20px;"/>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Cognitive Engine Settings")
    provider = st.selectbox(
        "Inference Provider",
        options=["Groq Cloud API (Free & Fast ~400 t/s)", "OpenRouter Free Tier", "Mock Simulator (Demo Mode)"],
        index=0
    )

    default_env_key = os.getenv("GROQ_API_KEY", "")
    api_key = st.text_input(
        "API Key (Leave empty to use server default or demo mode)",
        type="password",
        value=default_env_key,
        help="Get a free key in 30 seconds with no credit card at console.groq.com/keys"
    )

    model_name = st.text_input(
        "Model Identifier",
        value="llama-3.3-70b-versatile" if "Groq" in provider else "meta-llama/llama-3.3-70b-instruct:free"
    )

    tau_threshold = st.slider(
        "Epistemic Acceptance Gate (τ)",
        min_value=0.50,
        max_value=0.90,
        value=0.65,
        step=0.05,
        help="Candidates scoring below τ are rejected and trigger Reflexion backtracking."
    )

    max_retries = st.slider(
        "Max Retries per Subtask",
        min_value=1,
        max_value=5,
        value=3
    )

    st.markdown("---")
    st.markdown("### 🔗 Architecture Links")
    st.markdown("[📁 GitHub Repository](https://github.com/dipeshMahakali/Sarthika-AI)")
    st.markdown("[📄 Level 3 Technical Whitepaper](https://github.com/dipeshMahakali/Sarthika-AI/blob/main/Sarthika_Expert_AGI_v3_Architecture_and_Evaluation.md)")

tab_terminal, tab_benchmark, tab_whitepaper = st.tabs([
    "🎮 Interactive Cognitive Terminal",
    "🧪 Level 3 Benchmark Audit",
    "🧬 Theoretical Whitepaper"
])

# TAB 1: INTERACTIVE COGNITIVE TERMINAL
with tab_terminal:
    st.subheader("🎯 Define Cognitive Objective")

    col_p1, col_p2, col_p3, col_p4 = st.columns(4)
    with col_p1:
        if st.button("🔢 Matrix Fibonacci F(30)", use_container_width=True):
            st.session_state["goal_preset"] = "Compute the 30th Fibonacci number using matrix doubling and factorize it into prime factors."
    with col_p2:
        if st.button("👑 Lucas-Lehmer 2^31 - 1", use_container_width=True):
            st.session_state["goal_preset"] = "Verify whether 2^31 - 1 is prime using the Lucas-Lehmer sequence and count its decimal digits."
    with col_p3:
        if st.button("📐 Euler Totient phi(120)", use_container_width=True):
            st.session_state["goal_preset"] = "Compute Euler's totient phi(120), factorize it, and test for primitive roots."
    with col_p4:
        if st.button("🌀 Collatz Conjecture n=27", use_container_width=True):
            st.session_state["goal_preset"] = "Compute the Collatz trajectory and stopping time for n=27, finding its maximum peak value."

    default_goal = st.session_state.get(
        "goal_preset",
        "Compute the 30th Fibonacci number using matrix doubling and factorize it into prime factors."
    )

    goal_input = st.text_area(
        "Objective Prompt:",
        value=default_goal,
        height=75
    )

    run_clicked = st.button("🚀 Execute Autonomous Cognitive Loop", type="primary", use_container_width=True)

    if run_clicked:
        if not goal_input.strip():
            st.warning("Please enter a goal statement.")
        else:
            # Engine Selection
            effective_key = api_key.strip() or os.getenv("GROQ_API_KEY", "")
            if "Groq" in provider and effective_key:
                engine = GroqEngine(api_key=effective_key, model=model_name or "llama-3.3-70b-versatile")
                engine_type_desc = f"Groq Cloud API ({model_name})"
            elif "OpenRouter" in provider and effective_key:
                engine = OpenAIEngine(api_key=effective_key, model=model_name or "meta-llama/llama-3.3-70b-instruct:free")
                engine_type_desc = f"OpenRouter ({model_name})"
            else:
                engine = MockCognitiveEngine()
                engine_type_desc = "Mock Simulator (Demo Mode)"
                st.info("💡 Running in Mock Simulator mode. Supply a free Groq API key in the sidebar for live LLM inference.")

            agent = create_sarthika_expert(engine)

            # Execution UI Containers
            st.markdown(f"**Engine Active:** `{engine_type_desc}` | **Acceptance Gate:** `τ = {tau_threshold}`")
            
            subtasks_container = st.container()
            live_trace_container = st.container()
            scorecard_container = st.container()
            code_container = st.container()
            status_container = st.empty()

            with status_container.status("🧠 System 2 Deliberating: Decomposing goal...", expanded=True) as status_box:
                stream = agent.run_stream(
                    objective=goal_input.strip(),
                    max_retries_per_step=int(max_retries),
                    min_acceptance_score=float(tau_threshold)
                )

                for event in stream:
                    etype = event.get("type")

                    if etype == "decomposition":
                        subtasks = event.get("subtasks", [])
                        status_box.update(label=f"📋 Subtasks Planned: {len(subtasks)} steps", state="running")
                        with subtasks_container:
                            st.markdown("### 📋 Causal Subtasks Planned")
                            for idx, t in enumerate(subtasks, 1):
                                st.markdown(f"- ⏳ **Step {idx}:** {t}")

                    elif etype == "step_start":
                        s_idx = event["step_idx"]
                        tot = event["total_steps"]
                        subtask = event["subtask"]
                        att = event["attempt"]
                        status_box.update(
                            label=f"🔄 Step {s_idx}/{tot}: {subtask} (Attempt {att})",
                            state="running"
                        )
                        st.write(f"**Step {s_idx}: {subtask}** *(Attempt {att})* — Generating 3 algorithmic candidates...")

                    elif etype == "phase_4_scorecard":
                        scorecard = event["scorecard"]
                        best_cand = event["best_candidate"]
                        best_score = event["best_score"]
                        
                        with scorecard_container:
                            st.markdown(f"#### 📊 Cognitive Scorecard — Step {event['step_idx']} (Attempt {event['attempt']})")
                            table_data = []
                            for r in scorecard:
                                table_data.append({
                                    "Candidate": r["candidate"],
                                    "Mental Sim": "✅ Safe" if r["mental_sim"] == "Safe" else "⚠️ Warning",
                                    "Execution": "✅ Success" if r["executed"] == "Success" else "❌ Crash",
                                    "Score": f"{r['score']:.2f}",
                                    "UCT Value": f"{r['uct']:.2f}",
                                    "Justification": r["justification"]
                                })
                            st.dataframe(table_data, use_container_width=True)

                    elif etype == "accepted":
                        status_box.write(f"🏆 **ACCEPTED:** {event['candidate']} (Score: `{event['score']:.2f}`) committed to master sandbox.")
                        with code_container:
                            st.markdown(f"### 💻 Verified Solution Code (Step {event['step_idx']})")
                            st.code(event["code"], language="python")
                            if event.get("stdout"):
                                st.markdown("**Execution Output:**")
                                st.code(event["stdout"])

                    elif etype == "reflexion":
                        status_box.write(f"⚠️ **REJECTED (Score < {tau_threshold}):** Increasing temperature and triggering Reflexion...")
                        st.warning(f"Reflexion Critique: {event['feedback']}")

                    elif etype == "complete":
                        status_box.update(label="🎉 Cognitive Run Complete & Formally Verified!", state="complete", expanded=False)
                        st.success(
                            f"🏁 Execution finished. Sandbox Symbols: {event['active_symbols_count']} | "
                            f"Skills in DAG: {event['skills_count']} | Harvested Trajectories: {event['trajectories_count']}"
                        )
                        with st.expander("📦 View Dynamic Procedural Skill Catalog", expanded=False):
                            for s in event["skills_catalog"]:
                                st.markdown(f"- **`{s['name']}`**: {s['docstring']}")


# TAB 2: BENCHMARK SUITE
with tab_benchmark:
    st.subheader("🧪 Formal Level 3 (Expert AGI) Empirical Audit Suite")
    st.markdown("""
    This quantitative evaluation suite runs live empirical tests to verify Level-3 Expert Micro-AGI capabilities:
    1. **Causal Preemption:** Intercepts unsafe serialization/closure imports before execution.
    2. **Skill Graph Composition:** Synthesizes multi-tool pipelines inside a Directed Acyclic Graph.
    3. **MCTS Deliberative Lookahead:** Evaluates actions via Upper Confidence Bound for Trees (UCT).
    4. **Epistemic Grounding:** Rejects crashing code without hallucinating false progress.
    """)

    if st.button("🚀 Run Level 3 Empirical Audit", type="primary"):
        with st.spinner("Executing formal benchmark harness..."):
            res = run_level3_benchmark()
            st.markdown(f"### 🏆 Audit Verdict: `{res['verdict']}` ({res['passed_count']}/{res['total_count']} Passed)")
            
            table_bench = []
            for b in res["scorecard"]:
                table_bench.append({
                    "Benchmark Category": b["benchmark"],
                    "Status": "✅ PASSED" if b["passed"] else "❌ FAILED",
                    "Audit Evidence": b["detail"]
                })
            st.table(table_bench)


# TAB 3: WHITEPAPER
with tab_whitepaper:
    st.subheader("🧬 Sarthika 3.0 Theoretical Architecture")
    st.markdown("""
    ### Dual-Process Reasoning with Causal World Models
    
    * **System 1 (Generator):** Stochastic sampling proposing diverse candidate hypotheses ($A, B, C$) with diversity entropy scaling.
    * **System 2 (Critic):** Deliberative MCTS search with Epistemic Gate threshold $\\tau = 0.65$. Rejects malformed code and triggers Reflexion error diagnosis.
    * **Causal World Model:** Pre-execution symbolic invariant simulation on Python Abstract Syntax Trees (AST).
    * **Transactional Sandbox:** Isolated snapshot branches (`fork()`) and atomic commits (`commit()`).
    * **Tripartite Memory:**
      1. *Working Memory:* Hierarchical scratchpad and active MCTS thought tree.
      2. *Semantic Memory:* SQLite relational store for verified mathematical axioms.
      3. *Episodic Memory:* FAISS vector store for cross-task experience transfer.
    * **Compositional Skill Graph:** Directed Acyclic Graph cataloging learned procedural tools without catastrophic forgetting.
    """)
