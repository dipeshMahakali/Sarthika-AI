# -*- coding: utf-8 -*-
"""
Sarthika Autonomous Cognitive Architecture 3.0 (Level 3 Expert Micro-AGI)
Web Interface for Free Community Testing on Hugging Face Spaces / Local Machine.
"""

import os
import json

try:
    import gradio as gr
    HAS_GRADIO = True
except ImportError:
    HAS_GRADIO = False
    gr = None

from sarthika_core import (
    create_sarthika_expert,
    GroqEngine,
    OpenAIEngine,
    MockCognitiveEngine,
    run_level3_benchmark
)

def format_scorecard_markdown(scorecard, best_cand, best_score, step_idx, attempt):
    attempt_str = f" (Attempt {attempt})" if attempt > 1 else ""
    md = [f"### 📊 Cognitive Scorecard — Step {step_idx}{attempt_str}\n"]
    md.append("| Candidate | Causal Sim | Execution | Score | UCT | Justification |")
    md.append("| :--- | :---: | :---: | :---: | :---: | :--- |")
    for r in scorecard:
        sim_icon = "✅ Safe" if r["mental_sim"] == "Safe" else "⚠️ Warning"
        exec_icon = "✅ Success" if r["executed"] == "Success" else "❌ Crash"
        highlight = "**" if r["candidate"] == best_cand else ""
        md.append(f"| {highlight}{r['candidate']}{highlight} | {sim_icon} | {exec_icon} | `{r['score']:.2f}` | `{r['uct']:.2f}` | {r['justification']} |")
    return "\n".join(md)

def run_sarthika_pipeline(
    goal: str,
    provider: str,
    api_key: str,
    model_name: str,
    tau_threshold: float,
    max_retries: int,
    progress=None
):
    if not goal.strip():
        yield "⚠️ Please enter a cognitive goal or select one of the presets.", "", "", "", ""
        return

    # 1. Initialize Engine
    effective_key = api_key.strip() or os.getenv("GROQ_API_KEY", "")
    if provider == "Groq Cloud API (Free & Fast)" and effective_key:
        engine = GroqEngine(api_key=effective_key, model=model_name or "llama-3.3-70b-versatile")
    elif provider == "OpenRouter Free Tier" and effective_key:
        engine = OpenAIEngine(api_key=effective_key, base_url="https://openrouter.ai/api/v1", model=model_name or "meta-llama/llama-3.3-70b-instruct:free")
    else:
        # Fallback to Mock Engine if no key provided
        engine = MockCognitiveEngine()

    agent = create_sarthika_expert(engine)

    subtasks_md = "🧠 **Decomposing Goal into Causal Subtasks...**"
    log_md = f"🎯 **Goal:** {goal}\n\n*Initializing Dual-Process Engine & Transactional Sandbox...*\n"
    scorecard_md = "*Awaiting candidate synthesis...*"
    winning_code = "# Winning code will appear here after verification"
    state_summary_md = "*Sandbox state will update as steps complete.*"

    yield subtasks_md, log_md, scorecard_md, winning_code, state_summary_md

    stream = agent.run_stream(
        objective=goal,
        max_retries_per_step=int(max_retries),
        min_acceptance_score=float(tau_threshold)
    )

    for event in stream:
        etype = event.get("type")

        if etype == "decomposition":
            tasks = event.get("subtasks", [])
            subtasks_md = "### 📋 Causal Subtasks\n"
            for i, t in enumerate(tasks, 1):
                subtasks_md += f"- [ ] **Step {i}:** {t}\n"
            log_md += "\n✅ **Subtasks established by System 2 Planner.**\n"
            yield subtasks_md, log_md, scorecard_md, winning_code, state_summary_md

        elif etype == "step_start":
            s_idx = event["step_idx"]
            subtask = event["subtask"]
            attempt = event["attempt"]
            log_md += f"\n---\n#### 🔄 Step {s_idx}: {subtask}"
            if attempt > 1:
                log_md += f" *(Attempt {attempt}/{event['max_retries']} | Temperature: {event['temperature']:.2f})*"
            log_md += "\n- 🚀 **Phase 1:** Synthesizing 3 diverse algorithmic hypotheses...\n"
            yield subtasks_md, log_md, scorecard_md, winning_code, state_summary_md

        elif etype == "phase_2_mental_simulation":
            log_md += "- 🔮 **Phase 2:** Causal World Model simulating AST invariants...\n"
            yield subtasks_md, log_md, scorecard_md, winning_code, state_summary_md

        elif etype == "phase_3_execution":
            log_md += "- ⚙️ **Phase 3:** Executing isolated sandbox forks...\n"
            yield subtasks_md, log_md, scorecard_md, winning_code, state_summary_md

        elif etype == "phase_4_scorecard":
            scorecard_md = format_scorecard_markdown(
                event["scorecard"],
                event["best_candidate"],
                event["best_score"],
                event["step_idx"],
                event["attempt"]
            )
            log_md += f"- 🔍 **Phase 4:** Evaluated. Best candidate: `{event['best_candidate']}` (Score: `{event['best_score']:.2f}`)\n"
            yield subtasks_md, log_md, scorecard_md, winning_code, state_summary_md

        elif etype == "accepted":
            s_idx = event["step_idx"]
            winning_code = event["code"]
            log_md += f"🏆 **ACCEPTED:** Candidate committed to Master State (Score: `{event['score']:.2f}`).\n"
            if event.get("synthesized_fn"):
                log_md += f"✨ **Skill Registered:** `{event['synthesized_fn']}` added to Skill Graph DAG.\n"
            
            # Update checkmarks in subtasks
            subtasks_lines = subtasks_md.split("\n")
            for i, line in enumerate(subtasks_lines):
                if f"Step {s_idx}:" in line:
                    subtasks_lines[i] = line.replace("- [ ]", "- [x] ✅")
            subtasks_md = "\n".join(subtasks_lines)

            # Update state
            active_vars = [k for k in event.get("active_vars", []) if not k.startswith("__")]
            state_summary_md = f"**Active Sandbox Variables ({len(active_vars)}):** `{', '.join(active_vars[:15])}`\n\n"
            state_summary_md += f"**Latest Output:**\n```text\n{event['stdout'].strip() or '(no stdout)'}\n```"

            yield subtasks_md, log_md, scorecard_md, winning_code, state_summary_md

        elif etype == "reflexion":
            log_md += f"⚠️ **REJECTED (Score < {tau_threshold}):** Triggering Reflexion self-correction loop.\n"
            log_md += f"> 💡 *Reflexion Critique:* {event['feedback']}\n"
            yield subtasks_md, log_md, scorecard_md, winning_code, state_summary_md

        elif etype == "complete":
            log_md += "\n🎉 **COGNITIVE RUN TERMINATED SUCCESSFULLY.**\n"
            log_md += f"- **Active Symbols:** {event['active_symbols_count']}\n"
            log_md += f"- **Procedural Skills in DAG:** {event['skills_count']}\n"
            log_md += f"- **Harvested Trajectories:** {event['trajectories_count']}\n"

            skills_text = "\n".join([f"- `{s['name']}`: {s['docstring']}" for s in event["skills_catalog"]])
            state_summary_md += f"\n\n### 📦 Skill Graph DAG ({event['skills_count']} skills):\n{skills_text}"
            yield subtasks_md, log_md, scorecard_md, winning_code, state_summary_md

    # Save trajectories file for download if exists
    trajectories = agent.harvester.get_all_trajectories()
    if trajectories:
        with open("harvested_trajectories.jsonl", "w") as f:
            for t in trajectories:
                f.write(json.dumps(t) + "\n")


def run_benchmark_audit():
    res = run_level3_benchmark()
    md = ["### 🧪 Sarthika 3.0 (Level 3 Expert AGI) Empirical Audit Scorecard\n"]
    md.append("| Benchmark Category | Status | Empirical Audit Detail |")
    md.append("| :--- | :---: | :--- |")
    for b in res["scorecard"]:
        status_icon = "✅ PASSED" if b["passed"] else "❌ FAILED"
        md.append(f"| **{b['benchmark']}** | {status_icon} | {b['detail']} |")
    md.append(f"\n**Verdict:** 🏆 `{res['verdict']}` ({res['passed_count']}/{res['total_count']} passed)")
    return "\n".join(md)


# Build Gradio Blocks Interface
def build_app():
    if not HAS_GRADIO:
        return None

    theme = gr.themes.Soft(
        primary_hue="purple",
        secondary_hue="indigo",
        neutral_hue="slate"
    )

    with gr.Blocks(theme=theme, title="Sarthika 3.0: Level 3 Expert AGI Engine") as demo:
        gr.Markdown("""
        # 🧠 Sarthika Autonomous Cognitive Architecture 3.0
        ### Level-3 (Expert AGI) Micro-Engine: Dual-Process Reasoning, Causal World Models & MCTS Lookahead
        
        [![GitHub](https://img.shields.io/badge/GitHub-Sarthika--AI-black?logo=github)](https://github.com/dipeshMahakali/Sarthika-AI)
        [![Architecture](https://img.shields.io/badge/Architecture-Dual--Process%20MCTS-purple)](https://github.com/dipeshMahakali/Sarthika-AI)
        [![Status](https://img.shields.io/badge/AGI%20Level-Level%203%20(Expert)-green)](https://github.com/dipeshMahakali/Sarthika-AI)
        """)

        with gr.Tabs():
            with gr.TabItem("🎮 Interactive Cognitive Terminal"):
                with gr.Row():
                    with gr.Column(scale=4):
                        goal_input = gr.Textbox(
                            label="Cognitive Objective / Problem Statement",
                            placeholder="Enter a complex mathematical, algorithmic, or multi-step reasoning goal...",
                            lines=2,
                            value="Compute the 30th Fibonacci number using matrix doubling and factorize it into prime factors."
                        )
                    with gr.Column(scale=1):
                        run_btn = gr.Button("🚀 Run Cognitive Loop", variant="primary", size="lg")

                with gr.Accordion("⚙️ Cognitive Engine & Sandbox Settings", open=False):
                    with gr.Row():
                        provider_dropdown = gr.Dropdown(
                            label="Inference Provider",
                            choices=["Groq Cloud API (Free & Fast)", "OpenRouter Free Tier", "Mock Simulator (Demo Mode)"],
                            value="Groq Cloud API (Free & Fast)"
                        )
                        api_key_box = gr.Textbox(
                            label="API Key (Leave empty to use server default or demo mode)",
                            placeholder="gsk_... or sk-or-...",
                            type="password"
                        )
                        model_box = gr.Textbox(
                            label="Model Identifier",
                            value="llama-3.3-70b-versatile"
                        )
                    with gr.Row():
                        tau_slider = gr.Slider(
                            label="Epistemic Acceptance Threshold (τ)",
                            minimum=0.50,
                            maximum=0.90,
                            step=0.05,
                            value=0.65,
                            info="Candidates scoring below τ are rejected and trigger Reflexion backtracking."
                        )
                        retries_slider = gr.Slider(
                            label="Max Retries per Subtask",
                            minimum=1,
                            maximum=5,
                            step=1,
                            value=3
                        )

                gr.Markdown("**Quick-Start Presets:**")
                with gr.Row():
                    preset1 = gr.Button("🔢 Matrix Fibonacci & Prime Factors", size="sm")
                    preset2 = gr.Button("👑 Lucas-Lehmer Mersenne Primes (2^31 - 1)", size="sm")
                    preset3 = gr.Button("📐 Euler Totient & Primitive Roots", size="sm")
                    preset4 = gr.Button("🌀 Collatz Stopping Time (n=27)", size="sm")

                preset1.click(lambda: "Compute the 30th Fibonacci number using matrix doubling and factorize it into prime factors.", outputs=goal_input)
                preset2.click(lambda: "Verify whether 2^31 - 1 is prime using the Lucas-Lehmer sequence and count its decimal digits.", outputs=goal_input)
                preset3.click(lambda: "Compute Euler's totient phi(120), factorize it, and test for primitive roots.", outputs=goal_input)
                preset4.click(lambda: "Compute the Collatz trajectory and stopping time for n=27, finding its maximum peak value.", outputs=goal_input)

                gr.Markdown("---")

                with gr.Row():
                    with gr.Column(scale=1):
                        subtasks_display = gr.Markdown("### 📋 Causal Subtasks\n*Subtasks will be decomposed upon run.*")
                        state_display = gr.Markdown("### 💾 Sandbox & DAG Memory\n*Master state will be displayed here.*")
                    with gr.Column(scale=2):
                        log_display = gr.Markdown("### 🧠 Deliberative Execution Trace\n*Live System 1 proposals, Causal World Model simulation, and Reflexions will stream here.*")
                        scorecard_display = gr.Markdown("### 📊 Cognitive Scorecard\n*Candidate evaluations and UCT scores will appear here.*")

                with gr.Accordion("💻 Winning Code Block", open=True):
                    winning_code_display = gr.Code(label="Verified Executable Python Code", language="python")

                run_btn.click(
                    fn=run_sarthika_pipeline,
                    inputs=[goal_input, provider_dropdown, api_key_box, model_box, tau_slider, retries_slider],
                    outputs=[subtasks_display, log_display, scorecard_display, winning_code_display, state_display]
                )

            with gr.TabItem("🧪 Level 3 Empirical Benchmark Suite"):
                gr.Markdown("""
                ### Formal Level 3 (Expert AGI) Empirical Audit
                This suite executes 4 quantitative benchmarks verifying that the engine satisfies Level-3 Micro-AGI criteria:
                1. **Causal Preemption:** Intercepts dangerous code closures before runtime execution.
                2. **Skill Graph Composition:** Synthesizes multi-tool composition pipelines into a DAG.
                3. **MCTS Deliberation:** Explores hypothesis trees using UCT value backpropagation.
                4. **Epistemic Grounding:** Rejects crashing or non-computational code with zero hallucination.
                """)
                benchmark_btn = gr.Button("🚀 Run Empirical Audit Benchmark", variant="primary")
                benchmark_output = gr.Markdown("*Click the button to execute the 4 formal benchmarks.*")
                benchmark_btn.click(fn=run_benchmark_audit, outputs=benchmark_output)

            with gr.TabItem("🧬 Theoretical Architecture & Whitepaper"):
                gr.Markdown("""
                ## Sarthika 3.0 Cognitive Architecture Overview
                
                ```
                                        ┌────────────────────────┐
                                        │    User / Meta-Goal    │
                                        └───────────┬────────────┘
                                                    │
                                                    ▼
                                        ┌────────────────────────┐
                                        │   System 2 Deliberator │
                                        │  (Causal Subtask Plan) │
                                        └───────────┬────────────┘
                                                    │
                         ┌──────────────────────────┴──────────────────────────┐
                         ▼                                                     ▼
                ┌─────────────────────┐                               ┌─────────────────────┐
                │ System 1 (Proposer) │                               │ Tripartite Memory   │
                │ Diverse Hypotheses  │                               │ • Working Memory    │
                │ (Cand A, B, C)      │                               │ • Semantic (SQLite) │
                └──────────┬──────────┘                               │ • Episodic (FAISS)  │
                           │                                          └─────────────────────┘
                           ▼
                ┌─────────────────────────────────────────┐
                │   Causal World Model (Mental Sim)       │
                │   AST Invariants & Pre-Execution Checks │
                └──────────────────┬──────────────────────┘
                                   │
                                   ▼
                ┌─────────────────────────────────────────┐
                │   Transactional Sandbox (fork / commit) │
                │   Isolated Execution & Resource Limits  │
                └──────────────────┬──────────────────────┘
                                   │
                                   ▼
                ┌─────────────────────────────────────────┐
                │   System 2 Critic (MCTS & UCT)          │
                │   Epistemic Threshold Gate (τ = 0.65)   │
                └──────┬───────────────────────────┬──────┘
                       │ Score >= τ                │ Score < τ
                       ▼                           ▼
                ┌─────────────────────┐     ┌─────────────────────┐
                │ Commit to Master    │     │ Trigger Reflexion   │
                │ Register DAG Skill  │     │ Increase Entropy    │
                │ Harvest RLVR Data   │     │ Backtrack & Retry   │
                └─────────────────────┘     └─────────────────────┘
                ```

                ### Mathematical Formulations:
                * **UCT Formula:**
                  $$\\text{UCT}(n) = Q(n) + c \\sqrt{\\frac{\\ln N(p)}{N(n)}}$$
                * **Epistemic Acceptance Gate:**
                  $$\\text{Accept}(a) \\iff \\text{Score}(a) \\ge \\tau = 0.65 \\quad \\land \\quad \\text{Success}(a)$$
                * **Lifelong Procedural DAG:**
                  $$\\mathcal{G} = (\\mathcal{V}, \\mathcal{E}), \\quad v_i \\in \\text{Skills}, \\quad e_{ij} = \\text{Composition Dependency}$$
                """)
    return demo

demo = build_app()

if __name__ == "__main__":
    if HAS_GRADIO and demo is not None:
        demo.queue().launch(share=False)
    else:
        print("⚠️ Gradio is not installed in the local environment.")
        print("👉 Install dependencies with: pip install -r requirements.txt")
        print("🚀 When deployed to Hugging Face Spaces, Gradio is pre-installed automatically!")
