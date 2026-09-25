# -*- coding: utf-8 -*-
"""
Master Level 3 Expert AGI Cognitive Loop:
- Coordinates MCTS deliberation, Causal Mental Simulation, and Procedural Skill Graph
- Yields fine-grained streaming execution events for live web UI rendering
"""

import re
from typing import Dict, Any, List, Optional, Generator
from .mcts import MCTSNode

class AutonomousCognitiveAgentV3:
    """Level 3 Expert AGI Cognitive Architecture orchestrator."""
    def __init__(self, engine, working_mem, semantic_mem, episodic_mem, skill_graph, master_sandbox, planner, critic, harvester, world_model, mcts):
        self.engine = engine
        self.working_mem = working_mem
        self.semantic_mem = semantic_mem
        self.episodic_mem = episodic_mem
        self.skill_graph = skill_graph
        self.master_sandbox = master_sandbox
        self.planner = planner
        self.critic = critic
        self.harvester = harvester
        self.world_model = world_model
        self.mcts = mcts

    def run_stream(self, objective: str, max_retries_per_step: int = 3, min_acceptance_score: float = 0.65) -> Generator[Dict[str, Any], None, None]:
        """
        Streaming generator that executes the cognitive loop and yields real-time progress events.
        """
        self.working_mem.reset(objective)

        # 1. Retrieve Episodic and Semantic Context
        past_episodes = self.episodic_mem.recall_similar(objective, top_k=2)
        memory_context = ""
        if past_episodes:
            for ep in past_episodes:
                memory_context += f"- Past Task: {ep['task']} | Result: {ep['result'][:80]} | Reflection: {ep['reflection']}\n"

        semantic_facts = "\n".join(self.semantic_mem.get_all_facts())

        # 2. System 2 Goal Decomposition
        subtasks = self.planner.decompose_objective(objective, memory_context, semantic_facts)
        self.working_mem.subtasks = [{"title": t, "done": False} for t in subtasks]

        yield {
            "type": "decomposition",
            "goal": objective,
            "subtasks": subtasks,
            "memory_context": memory_context,
            "semantic_facts": semantic_facts
        }

        root_mcts = MCTSNode(state_description="Root State: Initialized master sandbox")
        current_tree_node = root_mcts

        # 3. Deliberative Execution Loop
        for step_idx, subtask_obj in enumerate(self.working_mem.subtasks, 1):
            subtask = subtask_obj["title"]
            step_verified = False
            attempt = 0
            reflexion_feedback = ""
            temperature = 0.7

            while attempt < max_retries_per_step and not step_verified:
                attempt += 1

                yield {
                    "type": "step_start",
                    "step_idx": step_idx,
                    "total_steps": len(self.working_mem.subtasks),
                    "subtask": subtask,
                    "attempt": attempt,
                    "max_retries": max_retries_per_step,
                    "temperature": temperature
                }

                active_keys = [k for k in self.master_sandbox.namespace if not k.startswith('__')]
                state_summary = f"Vars: {active_keys[:10]}"

                # PHASE 1: System 1 Proposes Hypotheses
                candidates = self.planner.generate_candidate_hypotheses(
                    subtask=subtask,
                    overall_objective=objective,
                    available_skills=self.skill_graph.get_skill_docs(),
                    state_summary=state_summary,
                    reflexion_feedback=reflexion_feedback,
                    temperature=temperature
                )

                yield {
                    "type": "phase_1_hypotheses",
                    "step_idx": step_idx,
                    "candidates": candidates
                }

                # PHASE 2: Causal World Model Pre-Simulation
                branch_evals = {}
                for name, code in candidates.items():
                    sim = self.world_model.simulate_mental_consequence(code, active_keys)
                    branch_evals[name] = {"code": code, "mental_sim": sim}

                yield {
                    "type": "phase_2_mental_simulation",
                    "step_idx": step_idx,
                    "evals": branch_evals
                }

                # PHASE 3: Transactional Fork & Physical Sandbox Execution
                branch_results = {}
                for name, bdata in branch_evals.items():
                    child_sandbox = self.master_sandbox.fork()
                    res = child_sandbox.execute(bdata["code"])
                    branch_results[name] = {
                        "sandbox": child_sandbox,
                        "code": bdata["code"],
                        "exec_result": res,
                        "mental_sim": bdata["mental_sim"]
                    }

                yield {
                    "type": "phase_3_execution",
                    "step_idx": step_idx,
                    "results": {
                        k: {
                            "success": v["exec_result"]["success"],
                            "stdout": v["exec_result"]["stdout"],
                            "stderr": v["exec_result"]["stderr"]
                        } for k, v in branch_results.items()
                    }
                }

                # PHASE 4: Metacognitive Critic & MCTS Node Backpropagation
                scorecard = []
                best_candidate = None
                best_score = -1.0
                best_critique = None

                for name, branch in branch_results.items():
                    critique = self.critic.critique_candidate(subtask, name, branch["code"], branch["exec_result"])
                    branch["critique"] = critique
                    score = critique["score"]

                    if not branch["mental_sim"]["viable"]:
                        score = min(score, 0.20)

                    node = MCTSNode(
                        state_description=f"Step {step_idx} - {name}",
                        code_action=branch["code"],
                        parent=current_tree_node,
                        depth=step_idx
                    )
                    node.terminal_score = score
                    node.execution_result = branch["exec_result"]
                    current_tree_node.add_child(node)
                    branch["node"] = node
                    self.mcts.backpropagate(node, score)

                    scorecard.append({
                        "candidate": name,
                        "mental_sim": "Safe" if branch["mental_sim"]["viable"] else "Warning",
                        "executed": "Success" if branch["exec_result"]["success"] else "Crash",
                        "score": round(score, 2),
                        "uct": round(node.uct_score(), 2),
                        "justification": critique["justification"]
                    })

                    if score > best_score:
                        best_score = score
                        best_candidate = name
                        best_critique = critique

                yield {
                    "type": "phase_4_scorecard",
                    "step_idx": step_idx,
                    "attempt": attempt,
                    "scorecard": scorecard,
                    "best_candidate": best_candidate,
                    "best_score": best_score,
                    "mcts_tree": root_mcts.to_tree_dict()
                }

                # PHASE 5: Threshold Acceptance & Memory Consolidation
                winning_branch = branch_results[best_candidate]
                if best_score >= min_acceptance_score and winning_branch["exec_result"]["success"]:
                    self.master_sandbox.commit(winning_branch["sandbox"])

                    # Register into Skill Graph
                    fn_match = re.search(r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)\((.*?)\)", winning_branch["code"])
                    synthesized_fn = None
                    if fn_match:
                        synthesized_fn = fn_match.group(1)
                        fn_params = [p.strip() for p in fn_match.group(2).split(",") if p.strip()]
                        self.skill_graph.register_skill(
                            name=synthesized_fn,
                            docstring=f"Autonomous skill for: {subtask}",
                            code=winning_branch["code"],
                            inputs=fn_params
                        )

                    # Harvest RLVR Trajectory
                    self.harvester.harvest(
                        goal=objective,
                        subtask=subtask,
                        winning_candidate=best_candidate,
                        code=winning_branch["code"],
                        exec_result=winning_branch["exec_result"],
                        critic_score=best_score,
                        reflection=best_critique["justification"]
                    )

                    # Consolidate Episodic Experience
                    self.episodic_mem.record_episode(
                        task=subtask,
                        action=winning_branch["code"][:200],
                        result=winning_branch["exec_result"]["stdout"][:200],
                        success=True,
                        reflection=best_critique["justification"],
                        reward_score=best_score
                    )

                    # Consolidate Semantic Fact
                    if winning_branch["exec_result"]["stdout"].strip():
                        stdout_snippet = winning_branch["exec_result"]["stdout"].strip().split('\n')[-1][:120]
                        self.semantic_mem.store_fact(f"Step {step_idx}: {subtask[:40]}", stdout_snippet, confidence=best_score)

                    step_verified = True
                    subtask_obj["done"] = True
                    current_tree_node = winning_branch["node"]

                    yield {
                        "type": "accepted",
                        "step_idx": step_idx,
                        "candidate": best_candidate,
                        "score": best_score,
                        "code": winning_branch["code"],
                        "stdout": winning_branch["exec_result"]["stdout"],
                        "synthesized_fn": synthesized_fn,
                        "active_vars": list(self.master_sandbox.namespace.keys())
                    }
                else:
                    temperature = min(1.0, temperature + 0.15)
                    reflexion_feedback = f"Subtask '{subtask}' failed on attempt {attempt}. Reason: {best_critique['justification']}. "
                    if winning_branch['exec_result']['stderr']:
                        reflexion_feedback += f"Error trace: {winning_branch['exec_result']['stderr'].strip().split('\n')[-1]}. "
                    reflexion_feedback += "Write genuine computational code, avoid syntax errors, and print the computed answer."
                    self.working_mem.log_reflexion(reflexion_feedback)

                    yield {
                        "type": "reflexion",
                        "step_idx": step_idx,
                        "attempt": attempt,
                        "score": best_score,
                        "temperature": temperature,
                        "feedback": reflexion_feedback
                    }

            if not step_verified:
                yield {
                    "type": "halt",
                    "step_idx": step_idx,
                    "subtask": subtask,
                    "reason": f"Failed after {max_retries_per_step} attempts."
                }
                break

        active_vars = [k for k in self.master_sandbox.namespace if not k.startswith('__')]
        yield {
            "type": "complete",
            "active_symbols_count": len(active_vars),
            "skills_count": len(self.skill_graph.skills),
            "trajectories_count": self.harvester.get_trajectory_count(),
            "skills_catalog": [s.to_dict() for s in self.skill_graph.skills.values()]
        }
