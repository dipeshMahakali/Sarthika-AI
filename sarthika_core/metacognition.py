# -*- coding: utf-8 -*-
"""
Dual-Process Metacognitive Engine:
- System 1 (MetacognitivePlanner): Fast proposal of diverse algorithmic candidate hypotheses
- System 2 (System2Critic): Rigorous empirical critique, error tracing, and epistemic gating
"""

import re
import ast
from typing import Dict, Any, List

class MetacognitivePlanner:
    def __init__(self, engine):
        self.engine = engine

    def decompose_objective(self, objective: str, memory_context: str, semantic_facts: str) -> List[str]:
        prompt = (
            "Given the high-level objective, relevant episodic memory, and semantic facts, decompose the goal into 2 to 4 concrete executable Python sub-tasks.\n"
            f"Objective: {objective}\n\n"
            f"Semantic Facts:\n{semantic_facts}\n\n"
            f"Episodic Memory Context:\n{memory_context}\n\n"
            "Output only a numbered list of sub-tasks (1. ..., 2. ..., etc.):"
        )
        response = self.engine.generate(
            prompt=prompt,
            system_prompt="You are a System 2 Metacognitive Task Planner. Produce lean, execution-oriented sub-plans."
        )
        tasks = []
        for line in response.strip().split("\n"):
            match = re.match(r"^\d+\.\s*(.*)", line.strip())
            if match:
                tasks.append(match.group(1).strip())
        return tasks if tasks else [objective]

    def generate_candidate_hypotheses(self, subtask: str, overall_objective: str, available_skills: str, state_summary: str, reflexion_feedback: str = "", temperature: float = 0.7) -> Dict[str, str]:
        prompt_parts = [
            "Generate exactly 3 competitive candidate approaches to execute this sub-task in Python.\n",
            f"Sub-task: {subtask}\n",
            f"Overall Goal: {overall_objective}\n",
            f"Available Skills: {available_skills}\n",
            f"Current Sandbox State: {state_summary}\n"
        ]
        if reflexion_feedback:
            prompt_parts.append(
                f"\n[IMPORTANT CRITIC REFLEXION - PREVIOUS ATTEMPT FAILED]:\n{reflexion_feedback}\n"
                "You MUST address the above critique. Do NOT repeat the same mistake.\n"
            )

        prompt_parts.append(
            "\nEach candidate MUST take a distinct algorithmic or structural strategy.\n"
            "Write actual executable code that computes results, defines functions, and prints verified outputs. Do NOT just print placeholder messages.\n\n"
            "Format your response clearly as:\n"
            "--- CANDIDATE A ---\n```python\n# Code for approach A\n```\n\n"
            "--- CANDIDATE B ---\n```python\n# Code for approach B\n```\n\n"
            "--- CANDIDATE C ---\n```python\n# Code for approach C\n```"
        )
        prompt = "".join(prompt_parts)

        raw_response = self.engine.generate(
            prompt=prompt,
            system_prompt="You are an advanced System 1 algorithmic synthesizer. Propose distinct, competitive, runnable Python solutions.",
            temperature=temperature
        )

        return self._extract_candidates_robust(raw_response, subtask)

    def _extract_candidates_robust(self, raw_response: str, subtask: str) -> Dict[str, str]:
        candidates = {}
        letters = ["A", "B", "C"]

        for letter in letters:
            patterns = [
                rf"(?:---|###|\*\*)\s*(?:CANDIDATE|STRATEGY|APPROACH)\s+{letter}" + r"[:\s*\-]*\n*```(?:python)?\s*([\s\S]*?)```",
                rf"(?:Candidate|Strategy|Approach)\s+{letter}" + r"[:\s*\-]*\n*```(?:python)?\s*([\s\S]*?)```",
                rf"\[{letter}\]" + r"[:\s]*```(?:python)?\s*([\s\S]*?)```"
            ]
            for p in patterns:
                m = re.search(p, raw_response, re.IGNORECASE)
                if m and len(m.group(1).strip()) > 10:
                    candidates[f"Candidate {letter}"] = m.group(1).strip()
                    break

        if len(candidates) < 3:
            all_blocks = re.findall(r"```(?:python)?\s*([\s\S]*?)```", raw_response, re.IGNORECASE)
            valid_blocks = [b.strip() for b in all_blocks if len(b.strip()) > 10]
            for i, letter in enumerate(letters):
                cand_key = f"Candidate {letter}"
                if cand_key not in candidates and i < len(valid_blocks):
                    candidates[cand_key] = valid_blocks[i]

        for letter in letters:
            cand_key = f"Candidate {letter}"
            if cand_key not in candidates:
                candidates[cand_key] = f"# Synthesis notice for {letter}\n# No valid code block identified for subtask: {subtask}"

        return candidates


class System2Critic:
    """Empirical Metacognitive Critic enforcing mathematical soundness and penalizing trivial heuristics."""
    def __init__(self, engine):
        self.engine = engine

    def critique_candidate(self, subtask: str, candidate_name: str, code: str, exec_result: Dict[str, Any]) -> Dict[str, Any]:
        if not exec_result["success"]:
            err_line = exec_result['stderr'].strip().split('\n')[-1]
            return {
                "score": 0.10,
                "justification": f"Execution failed with runtime exception: {err_line}"
            }

        lines = [l.strip() for l in code.split('\n') if l.strip() and not l.strip().startswith('#')]
        is_trivial_print = len(lines) <= 2 and any(l.startswith('print(') and ('Executing' in l or 'Candidate' in l) for l in lines)
        if is_trivial_print:
            return {
                "score": 0.05,
                "justification": "Rejected: Code only contains a dummy print statement with zero computational logic."
            }

        prompt = (
            "Critique the execution trace of this candidate code.\n"
            f"Sub-task: {subtask}\n"
            f"Candidate: {candidate_name}\n"
            f"Code:\n{code}\n"
            f"Execution Output:\n{exec_result['stdout']}\n\n"
            "Score viability from 0.0 to 1.0:\n"
            "- 0.0 to 0.3: Failed to compute the required result, returned dummy data, or crashed.\n"
            "- 0.4 to 0.6: Partial solution, inefficient, or unverified.\n"
            "- 0.7 to 1.0: Completely solved the subtask, mathematically and computationally sound.\n\n"
            "Format:\nSCORE: <float between 0.0 and 1.0>\nJUSTIFICATION: <1-line explanation>"
        )
        response = self.engine.generate(
            prompt=prompt,
            system_prompt="You are an uncompromising System 2 Code Verifier. Reward genuine mathematical calculation and penalize placeholders.",
            temperature=0.1
        )

        score = 0.50
        justification = "Execution complete."
        for line in response.strip().split("\n"):
            if "SCORE:" in line.upper():
                match = re.search(r"(\d+(?:\.\d+)?)", line)
                if match:
                    score = min(1.0, max(0.0, float(match.group(1))))
            elif "JUSTIFICATION:" in line.upper():
                justification = line.split(":", 1)[-1].strip()

        return {
            "score": score,
            "justification": justification
        }
