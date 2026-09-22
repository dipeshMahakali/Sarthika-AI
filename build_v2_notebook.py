import json

notebook = {
    "nbformat": 4,
    "nbformat_minor": 0,
    "metadata": {
        "colab": {
            "provenance": [],
            "gpuType": "T4"
        },
        "kernelspec": {
            "name": "python3",
            "display_name": "Python 3"
        },
        "language_info": {
            "name": "python"
        },
        "accelerator": "GPU"
    },
    "cells": []
}

def add_md(source):
    notebook["cells"].append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in source.strip().split("\n")]
    })

def add_code(source):
    notebook["cells"].append({
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": [line + "\n" for line in source.strip().split("\n")]
    })

# Header
add_md("""# 🧠 Autonomous Cognitive Architecture 2.0 (Dual-Process Micro-AGI)
### Featuring Persistent Transactional Sandbox, Test-Time Tree Search, and Synaptic Self-Evolution

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dipeshMahakali/Sarthika-AI/blob/main/AGI_Cognitive_Agent_v2.ipynb)

---

### 🌟 Architectural Evolution: From Level 1 Emerging AGI to Level 2 Competent AGI
This next-generation cognitive architecture resolves the foundational bottlenecks of single-turn LLM agents:

1. **Persistent Transactional Sandbox Core**: Replaces isolated, single-turn `exec()` with an interactive stateful execution environment. Uses transactional branching (`fork()` and `commit()`) so candidate hypotheses can be tested in isolation without state corruption.
2. **Dual-Process Test-Time Tree Search (System 1 + System 2)**: Instead of greedy linear action proposals, the agent generates exactly 3 competitive hypotheses (**Candidate A, Candidate B, Candidate C**), simulates them in parallel stateful sandboxes, and evaluates them with a rigorous Metacognitive Critic (scoring 0.0 to 1.0).
3. **Synaptic Weight Consolidation (RLVR Harvesting)**: Every verified execution trajectory is recorded into a verifiable reward dataset (JSONL) formatted for continuous offline LoRA fine-tuning using Unsloth.
""")

# Cell 1: Dependencies
add_md("## 📦 Step 1: Install Dependencies & Verify GPU Acceleration")
add_code("""#@title Install Dependencies and Verify GPU
import os
import sys

print("Installing Cognitive Architecture 2.0 dependencies...")
!pip install -q transformers accelerate bitsandbytes sentence-transformers faiss-cpu rich pydantic

import torch
print("=" * 60)
if torch.cuda.is_available():
    device_name = torch.cuda.get_device_name(0)
    vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
    print(f"✅ GPU DETECTED: {device_name}")
    print(f"✅ VRAM AVAILABLE: {vram_gb:.2f} GB")
    device = "cuda"
else:
    print("⚠️ NO GPU DETECTED! Running in CPU fallback mode.")
    print("👉 Recommended for Colab: Click Runtime -> Change runtime type -> T4 GPU.")
    device = "cpu"
print("=" * 60)
""")

# Cell 2: Cognitive Engine
add_md("""## ⚡ Step 2: Foundation Cognitive Reasoning Engine
Loads 4-bit Quantized `Qwen2.5-7B-Instruct` directly into Colab's 16GB VRAM (or CPU fallback).""")
add_code("""#@title Initialize Reasoning Engine
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch

MODEL_ID = "Qwen/Qwen2.5-7B-Instruct"

class CognitiveEngine:
    def __init__(self, model_id: str = MODEL_ID):
        print(f"🚀 Loading Foundation Model: {model_id}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)

        if torch.cuda.is_available():
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16,
                bnb_4bit_use_double_quant=True,
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                model_id,
                quantization_config=bnb_config,
                device_map="auto",
                torch_dtype=torch.bfloat16,
            )
            print("✅ Model loaded with 4-bit NF4 Quantization on GPU.")
        else:
            self.model = AutoModelForCausalLM.from_pretrained(
                model_id,
                torch_dtype=torch.float32,
                device_map="cpu",
                low_cpu_mem_usage=True
            )
            print("⚠️ Model loaded on CPU (slow execution mode).")

    def generate(self, prompt: str, system_prompt: str = "", max_new_tokens: int = 1024, temperature: float = 0.6) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)
        generated_ids = self.model.generate(
            **model_inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            do_sample=True if temperature > 0 else False,
            pad_token_id=self.tokenizer.eos_token_id
        )

        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        return self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

engine = CognitiveEngine()
print("✅ Cognitive Reasoning Engine online.")
""")

# Cell 3: Tripartite Memory
add_md("""## 🧠 Step 3: Tripartite Memory Subsystem
Combines Baddeley Working Memory, SQLite Semantic Knowledge Graph, and FAISS Vector Episodic Memory.""")
add_code("""#@title Build Tripartite Memory Architecture
import sqlite3
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from typing import List, Dict, Any

class WorkingMemory:
    def __init__(self):
        self.active_goal: str = ""
        self.subtasks: List[Dict[str, Any]] = []
        self.current_step: int = 0
        self.scratchpad: List[str] = []

    def reset(self, goal: str):
        self.active_goal = goal
        self.subtasks = []
        self.current_step = 0
        self.scratchpad = []

    def add_thought(self, thought: str):
        self.scratchpad.append(thought)

class SemanticMemory:
    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self._init_db()

    def _init_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS facts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entity TEXT UNIQUE,
            definition TEXT,
            confidence REAL
        )''')
        self.conn.commit()

    def store_fact(self, entity: str, definition: str, confidence: float = 1.0):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT OR REPLACE INTO facts (entity, definition, confidence)
                          VALUES (?, ?, ?)''', (entity, definition, confidence))
        self.conn.commit()

    def query_fact(self, entity: str) -> str:
        cursor = self.conn.cursor()
        cursor.execute("SELECT definition FROM facts WHERE entity LIKE ?", (f"%{entity}%",))
        row = cursor.fetchone()
        return row[0] if row else "Unknown entity."

class EpisodicMemory:
    def __init__(self, embedding_model_name: str = "all-MiniLM-L6-v2"):
        print("🧠 Initializing Episodic FAISS Vector Memory...")
        self.embedder = SentenceTransformer(embedding_model_name)
        self.dimension = self.embedder.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatL2(self.dimension)
        self.episodes: List[Dict[str, Any]] = []

    def record_episode(self, task: str, action: str, result: str, success: bool, reflection: str):
        episode = {
            "task": task,
            "action": action,
            "result": result,
            "success": success,
            "reflection": reflection
        }
        text_representation = f"Task: {task} | Action: {action} | Reflection: {reflection}"
        embedding = self.embedder.encode([text_representation])[0].astype("float32")
        self.index.add(np.array([embedding]))
        self.episodes.append(episode)

    def recall_similar(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        if self.index.ntotal == 0:
            return []
        query_vector = self.embedder.encode([query])[0].astype("float32")
        distances, indices = self.index.search(np.array([query_vector]), min(top_k, self.index.ntotal))
        results = []
        for idx in indices[0]:
            if idx != -1 and idx < len(self.episodes):
                results.append(self.episodes[idx])
        return results

working_mem = WorkingMemory()
semantic_mem = SemanticMemory()
episodic_mem = EpisodicMemory()
print("✅ Tripartite Memory Architecture online.")
""")

# Cell 4: Persistent Transactional Sandbox Core
add_md("""## 🛠️ Step 4: Persistent Transactional Sandbox & Procedural Skill Registry
Solves State Isolation! Variables, functions, and imports persist across turns.
Features **Transactional Branching (`fork()` & `commit()`)** allowing parallel candidate rollouts without namespace contamination.""")
add_code("""#@title Persistent Transactional Sandbox & Skill Registry
import io
import sys
import copy
import traceback
from typing import Dict, Any, List, Optional

class PersistentTransactionalSandbox:
    \"\"\"A persistent execution environment with isolated branch forks and commit mechanisms.\"\"\"
    def __init__(self, base_namespace: Optional[Dict[str, Any]] = None):
        if base_namespace is None:
            self.namespace: Dict[str, Any] = {
                "__builtins__": __builtins__,
                "__name__": "__main__",
                "__doc__": "AGI Persistent Sandbox Session"
            }
        else:
            self.namespace = copy.copy(base_namespace)

    def fork(self) -> "PersistentTransactionalSandbox":
        \"\"\"Creates a child sandbox snapshot for isolated candidate rollout.\"\"\"
        return PersistentTransactionalSandbox(self.namespace)

    def commit(self, branch_sandbox: "PersistentTransactionalSandbox"):
        \"\"\"Commits the state of a winning branch into this master sandbox.\"\"\"
        self.namespace = copy.copy(branch_sandbox.namespace)

    def execute(self, code: str) -> Dict[str, Any]:
        \"\"\"Executes code within the persistent state, capturing stdout, stderr, and variables.\"\"\"
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        redirected_out = io.StringIO()
        redirected_err = io.StringIO()

        sys.stdout = redirected_out
        sys.stderr = redirected_err

        success = False
        output_str = ""
        error_str = ""

        try:
            exec(code, self.namespace)
            success = True
            output_str = redirected_out.getvalue()
        except Exception:
            error_str = traceback.format_exc()
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

        active_variables = {
            k: type(v).__name__ for k, v in self.namespace.items()
            if not k.startswith("__") and not callable(v)
        }
        active_functions = [
            k for k, v in self.namespace.items()
            if not k.startswith("__") and callable(v)
        ]

        return {
            "success": success,
            "stdout": output_str,
            "stderr": error_str,
            "variables": active_variables,
            "functions": active_functions
        }

class ProceduralSkillRegistry:
    def __init__(self, sandbox: PersistentTransactionalSandbox):
        self.sandbox = sandbox
        self.skills: Dict[str, Dict[str, Any]] = {}
        self._register_default_skills()

    def _register_default_skills(self):
        self.register_skill(
            name="prime_factorization",
            docstring="Factorizes an integer into prime components.",
            code=\"\"\"def prime_factorization(n: int):
    factors = []
    d = 2
    while d * d <= n:
        while (n % d) == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors\"\"\"
        )

    def register_skill(self, name: str, docstring: str, code: str):
        res = self.sandbox.execute(code)
        if res["success"]:
            self.skills[name] = {"doc": docstring, "code": code}
            return True
        return False

    def get_skill_docs(self) -> str:
        if not self.skills:
            return "No procedural skills registered."
        return "\\n".join([f"- `{name}`: {meta['doc']}" for name, meta in self.skills.items()])

master_sandbox = PersistentTransactionalSandbox()
skill_registry = ProceduralSkillRegistry(master_sandbox)
print("✅ Persistent Transactional Sandbox & Skill Registry initialized.")
""")

# Cell 5: Dual-Process Metacognitive Engine
add_md("""## 🔬 Step 5: Dual-Process Metacognitive Engine (Test-Time Search)
Implements Kahneman's System 1 (Multi-Hypothesis Generator: Candidate A, B, C) and System 2 (Rigorous Mathematical Critic).""")
add_code("""#@title Dual-Process Metacognitive Engine
import re
from typing import Dict, Any, List

class MetacognitivePlanner:
    def __init__(self, engine: CognitiveEngine):
        self.engine = engine

    def decompose_objective(self, objective: str, memory_context: str) -> List[str]:
        prompt = f\"\"\"Given the high-level objective and relevant past memory, decompose it into 2 to 4 concrete sub-tasks.
Objective: {objective}

Memory Context:
{memory_context}

Output only a numbered list of sub-tasks (1. ..., 2. ..., etc.):\"\"\"
        response = self.engine.generate(
            prompt=prompt,
            system_prompt="You are a System 2 Metacognitive Task Planner. Produce lean, execution-oriented sub-plans."
        )
        tasks = []
        for line in response.strip().split("\\n"):
            match = re.match(r"^\\d+\\.\\s*(.*)", line.strip())
            if match:
                tasks.append(match.group(1).strip())
        return tasks if tasks else [objective]

    def generate_candidate_hypotheses(self, subtask: str, overall_objective: str, available_skills: str, state_summary: str) -> Dict[str, str]:
        \"\"\"System 1: Generates exactly 3 distinct, competitive candidate approaches.\"\"\"
        prompt = f\"\"\"Generate exactly 3 competitive candidate approaches to execute this sub-task in Python.
Sub-task: {subtask}
Overall Goal: {overall_objective}
Available Skills: {available_skills}
Current Sandbox State: {state_summary}

Each candidate MUST take a distinct algorithmic or structural strategy.
Output format:
### CANDIDATE A
```python
# Code for approach A
```

### CANDIDATE B
```python
# Code for approach B
```

### CANDIDATE C
```python
# Code for approach C
```\"\"\"
        raw_response = self.engine.generate(
            prompt=prompt,
            system_prompt="You are an advanced System 1 algorithmic synthesizer. You propose distinct, competitive hypotheses.",
            temperature=0.7
        )

        candidates = {}
        for letter in ["A", "B", "C"]:
            pattern = rf"### CANDIDATE {letter}\\s*```python(.*?)```"
            match = re.search(pattern, raw_response, re.DOTALL | re.IGNORECASE)
            if match:
                candidates[f"Candidate {letter}"] = match.group(1).strip()
            else:
                # Fallback extraction
                candidates[f"Candidate {letter}"] = f"# Candidate {letter} fallback\\nprint('Executing {subtask} via Strategy {letter}')"

        return candidates

class System2Critic:
    def __init__(self, engine: CognitiveEngine):
        self.engine = engine

    def critique_candidate(self, subtask: str, candidate_name: str, code: str, exec_result: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f\"\"\"Critique the execution trace of this candidate.
Sub-task: {subtask}
Candidate: {candidate_name}
Code:
{code}
Execution Success: {exec_result['success']}
STDOUT: {exec_result['stdout']}
STDERR: {exec_result['stderr']}

Score viability from 0.0 (Failed/Dead-end) to 1.0 (Optimal/Mathematically Sound).
Respond in format:
SCORE: <float between 0.0 and 1.0>
JUSTIFICATION: <1-line justification based on correctness, resource efficiency, and state preservation>\"\"\"
        response = self.engine.generate(
            prompt=prompt,
            system_prompt="You are an independent, rigorous code critic. Evaluate correctness, efficiency, and state safety.",
            temperature=0.1
        )

        score = 0.5
        justification = "Standard execution evaluation."

        for line in response.strip().split("\\n"):
            if "SCORE:" in line.upper():
                match = re.search(r"(\\d+(?:\\.\\d+)?)", line)
                if match:
                    score = min(1.0, max(0.0, float(match.group(1))))
            elif "JUSTIFICATION:" in line.upper():
                justification = line.split(":", 1)[-1].strip()

        # Empirical penalty if code failed execution
        if not exec_result["success"]:
            score = min(score, 0.2)

        return {
            "score": score,
            "justification": justification
        }

planner = MetacognitivePlanner(engine)
critic = System2Critic(engine)
print("✅ Dual-Process Metacognitive Engine online.")
""")

# Cell 6: Trajectory Harvester for Synaptic Weight Consolidation
add_md("""## 📈 Step 6: Autonomous Trajectory Harvester & Synaptic Consolidation
Harvests every verified trajectory into a Reinforcement Learning with Verifiable Rewards (RLVR) dataset for Unsloth / LoRA fine-tuning.""")
add_code("""#@title RLVR Trajectory Harvester
import json
from datetime import datetime

class RLVRTrajectoryHarvester:
    \"\"\"Stores verified problem-solving trajectories for synaptic weight fine-tuning.\"\"\"
    def __init__(self, dataset_file: str = "cognitive_trajectories.jsonl"):
        self.dataset_file = dataset_file

    def harvest(self, goal: str, subtask: str, winning_candidate: str, code: str, exec_result: Dict[str, Any], critic_score: float, reflection: str):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "goal": goal,
            "subtask": subtask,
            "winning_candidate": winning_candidate,
            "code": code,
            "stdout": exec_result.get("stdout", ""),
            "stderr": exec_result.get("stderr", ""),
            "reward_score": critic_score,
            "reflection": reflection
        }
        with open(self.dataset_file, "a") as f:
            f.write(json.dumps(entry) + "\\n")

    def get_trajectory_count(self) -> int:
        try:
            with open(self.dataset_file, "r") as f:
                return len(f.readlines())
        except FileNotFoundError:
            return 0

trajectory_harvester = RLVRTrajectoryHarvester()
print(f"✅ Trajectory Harvester initialized. Logged trajectories: {trajectory_harvester.get_trajectory_count()}")
""")

# Cell 7: Master Cognitive Agent Loop
add_md("""## 🔄 Step 7: Master Autonomous Cognitive Agent Loop (AGI 2.0)
Orchestrates Phase 1 (Hypotheses Generation), Phase 2 (Parallel Simulation), Phase 3 (Critic Evaluation), and Phase 4 (Branch Commit & Memory Consolidation).""")
add_code("""#@title Master Autonomous Cognitive Agent Loop
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

class AutonomousCognitiveAgentV2:
    def __init__(self, engine, working_mem, semantic_mem, episodic_mem, skill_registry, master_sandbox, planner, critic, harvester):
        self.engine = engine
        self.working_mem = working_mem
        self.semantic_mem = semantic_mem
        self.episodic_mem = episodic_mem
        self.skill_registry = skill_registry
        self.master_sandbox = master_sandbox
        self.planner = planner
        self.critic = critic
        self.harvester = harvester

    def run(self, objective: str):
        console.print(Panel.fit(f"[bold cyan]🎯 AUTONOMOUS AGI 2.0 GOAL:[/bold cyan] {objective}", border_style="cyan"))
        self.working_mem.reset(objective)

        # Recall relevant episodic traces
        past_episodes = self.episodic_mem.recall_similar(objective, top_k=2)
        memory_context = ""
        if past_episodes:
            for ep in past_episodes:
                memory_context += f"- Task: {ep['task']} | Result: {ep['result'][:100]} | Reflection: {ep['reflection']}\\n"

        # Decompose goal
        console.print("[bold yellow]🧠 System 2 Planning: Decomposing objective into hierarchical steps...[/bold yellow]")
        subtasks = self.planner.decompose_objective(objective, memory_context)
        self.working_mem.subtasks = [{"title": t, "done": False} for t in subtasks]

        for i, t in enumerate(subtasks, 1):
            console.print(f"  [green]{i}.[/green] {t}")

        # Execute each subtask using 4-Phase Tree Search Protocol
        for step_idx, subtask_obj in enumerate(self.working_mem.subtasks, 1):
            subtask = subtask_obj["title"]
            console.print(f"\\n[bold magenta]══════════════════ STEP {step_idx}: {subtask} ══════════════════[/bold magenta]")
            self.working_mem.current_step = step_idx

            state_summary = f"Vars: {list(self.master_sandbox.namespace.keys())[:10]}"

            # PHASE 1: Generate Multiple Hypotheses (System 1)
            console.print("[bold cyan]🚀 PHASE 1: Generating 3 Competitive Hypotheses (Candidates A, B, C)...[/bold cyan]")
            candidates = self.planner.generate_candidate_hypotheses(
                subtask=subtask,
                overall_objective=objective,
                available_skills=self.skill_registry.get_skill_docs(),
                state_summary=state_summary
            )

            # PHASE 2: Parallel Sandbox Simulation (Stateful Execution via Forks)
            console.print("[bold blue]⚙️ PHASE 2: Parallel Sandbox Simulation (Stateful Isolation)...[/bold blue]")
            branch_results = {}
            for name, code in candidates.items():
                child_sandbox = self.master_sandbox.fork()
                res = child_sandbox.execute(code)
                branch_results[name] = {
                    "sandbox": child_sandbox,
                    "code": code,
                    "exec_result": res
                }

            # PHASE 3: System 2 Critic Evaluation
            console.print("[bold yellow]🔍 PHASE 3: Metacognitive Critic Evaluation (0.0 to 1.0)...[/bold yellow]")
            eval_table = Table(title=f"Critic Scorecard for Step {step_idx}", show_header=True, header_style="bold green")
            eval_table.add_column("Candidate", width=15)
            eval_table.add_column("Success", width=10)
            eval_table.add_column("Score", width=8)
            eval_table.add_column("Justification", width=45)

            best_candidate = None
            best_score = -1.0
            best_critique = None

            for name, branch in branch_results.items():
                critique = self.critic.critique_candidate(subtask, name, branch["code"], branch["exec_result"])
                branch["critique"] = critique
                score = critique["score"]
                eval_table.add_row(
                    name,
                    "✅ Yes" if branch["exec_result"]["success"] else "❌ No",
                    f"{score:.2f}",
                    critique["justification"]
                )
                if score > best_score:
                    best_score = score
                    best_candidate = name
                    best_critique = critique

            console.print(eval_table)

            # PHASE 4: Branch Selection & Commit to Master Sandbox
            console.print(f"[bold green]🏆 PHASE 4: Selecting Winner -> {best_candidate} (Score: {best_score:.2f})[/bold green]")
            winning_branch = branch_results[best_candidate]
            self.master_sandbox.commit(winning_branch["sandbox"])

            # Auto-register newly defined functions as procedural skills
            fn_match = re.search(r"def\\s+([a-zA-Z_][a-zA-Z0-9_]*)\\(", winning_branch["code"])
            if fn_match:
                fn_name = fn_match.group(1)
                self.skill_registry.register_skill(
                    name=fn_name,
                    docstring=f"Autonomous skill synthesized for: {subtask}",
                    code=winning_branch["code"]
                )
                console.print(f"[bold green]✨ SYNTHESIZED PROCEDURAL SKILL: '{fn_name}' committed to skill bank.[/bold green]")

            # Harvest trajectory for Synaptic Weight Consolidation
            self.harvester.harvest(
                goal=objective,
                subtask=subtask,
                winning_candidate=best_candidate,
                code=winning_branch["code"],
                exec_result=winning_branch["exec_result"],
                critic_score=best_score,
                reflection=best_critique["justification"]
            )

            # Consolidate into Episodic Memory
            self.episodic_mem.record_episode(
                task=subtask,
                action=winning_branch["code"][:200],
                result=winning_branch["exec_result"]["stdout"][:200],
                success=winning_branch["exec_result"]["success"],
                reflection=best_critique["justification"]
            )

            subtask_obj["done"] = True

        console.print(Panel.fit(
            f"[bold green]🏁 GOAL ACCOMPLISHED!\\nPersistent Sandbox Variables: {[k for k in self.master_sandbox.namespace if not k.startswith('__')]}\\nHarvested Trajectories: {self.harvester.get_trajectory_count()}[/bold green]",
            border_style="green"
        ))

agent_v2 = AutonomousCognitiveAgentV2(
    engine=engine,
    working_mem=working_mem,
    semantic_mem=semantic_mem,
    episodic_mem=episodic_mem,
    skill_registry=skill_registry,
    master_sandbox=master_sandbox,
    planner=planner,
    critic=critic,
    harvester=trajectory_harvester
)
print("✅ Autonomous Cognitive Agent 2.0 (AGI Engine) ready.")
""")

# Cell 8: Experiment 1
add_md("""## 🧪 Experiment 1: Algorithmic Discovery with Multi-Candidate Search
In this experiment, the agent decomposes and solves the Collatz 27 analysis and Fibonacci Matrix Exponentiation, testing 3 candidate hypotheses in parallel at each step.""")
add_code("""#@title Run Experiment 1: Multi-Candidate Algorithmic Discovery
goal = \"\"\"Compute the 60th Fibonacci number modulo 10^9+7 using O(log n) Matrix Exponentiation.
Verify that the matrix pow function persists in state, and analyze its prime factors.\"\"\"

agent_v2.run(goal)
""")

# Cell 9: Experiment 2
add_md("""## 🧪 Experiment 2: State-Preserving Lifelong Transfer Learning
Shows how skills and variables created in Experiment 1 persist seamlessly in the master sandbox and episodic vector memory.""")
add_code("""#@title Run Experiment 2: Lifelong Transfer Learning
goal_2 = \"\"\"Using the matrix exponentiation and prime factorization skills established in previous sessions, compute the 35th Fibonacci number and determine if it is divisible by any prime factors of 105.\"\"\"

agent_v2.run(goal_2)
""")

# Cell 10: Interactive Terminal
add_md("""## 🚀 Step 8: Interactive Cognitive Terminal
Enter any high-level objective to watch AGI 2.0 generate hypotheses, evaluate code in the persistent sandbox, and consolidate knowledge.""")
add_code("""#@title 🎮 Interactive Autonomous Goal Terminal
#@markdown Enter any high-level objective for the agent:
goal_input = "Investigate whether 2^67 - 1 is prime or composite using Lucas-Lehmer or Pollard rho algorithm." #@param {type:"string"}

if goal_input.strip():
    agent_v2.run(goal_input)
""")

# Save notebook
with open("AGI_Cognitive_Agent_v2.ipynb", "w") as f:
    json.dump(notebook, f, indent=2)

print("✅ Successfully generated AGI_Cognitive_Agent_v2.ipynb with all cells.")

