# -*- coding: utf-8 -*-
"""
Compositional Skill Graph Subsystem:
- Maintains a Directed Acyclic Graph (DAG) of learned procedural skills
- Supports dynamic registration and high-order autonomous tool composition
"""

from typing import Dict, Any, List, Optional

class SkillNode:
    def __init__(self, name: str, docstring: str, code: str, inputs: List[str], outputs: List[str]):
        self.name = name
        self.docstring = docstring
        self.code = code
        self.inputs = inputs
        self.outputs = outputs

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "docstring": self.docstring,
            "code": self.code,
            "inputs": self.inputs,
            "outputs": self.outputs
        }


class CompositionalSkillGraph:
    """Maintains a graph of learned procedural skills and synthesizes composite pipelines."""
    def __init__(self, sandbox):
        self.sandbox = sandbox
        self.skills: Dict[str, SkillNode] = {}
        self.edges: List[tuple] = []
        self._seed_foundational_skills()

    def _seed_foundational_skills(self):
        # 1. Prime Factorization Skill
        self.register_skill(
            name="prime_factors",
            docstring="Factorizes integer n into unique prime factors and prime-power dictionary.",
            code="""def prime_factors(n: int):
    factors = {}
    d = 2
    temp = abs(n)
    while d * d <= temp:
        while temp % d == 0:
            factors[d] = factors.get(d, 0) + 1
            temp //= d
        d += 1
    if temp > 1:
        factors[temp] = factors.get(temp, 0) + 1
    return factors""",
            inputs=["n: int"],
            outputs=["factors: dict"]
        )

        # 2. GCD
        self.register_skill(
            name="gcd",
            docstring="Computes Greatest Common Divisor of integers a and b using Euclidean algorithm.",
            code="""def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)""",
            inputs=["a: int", "b: int"],
            outputs=["result: int"]
        )

        # 3. Fast Modular Exponentiation
        self.register_skill(
            name="mod_pow",
            docstring="Computes (base^exp) % mod in O(log exp) time.",
            code="""def mod_pow(base: int, exp: int, mod: int) -> int:
    return pow(base, exp, mod)""",
            inputs=["base: int", "exp: int", "mod: int"],
            outputs=["result: int"]
        )

    def register_skill(self, name: str, docstring: str, code: str, inputs: Optional[List[str]] = None, outputs: Optional[List[str]] = None) -> bool:
        res = self.sandbox.execute(code)
        if res["success"]:
            node = SkillNode(
                name=name,
                docstring=docstring,
                code=code,
                inputs=inputs or ["*args"],
                outputs=outputs or ["Any"]
            )
            self.skills[name] = node
            return True
        return False

    def compose_pipeline(self, pipeline_name: str, skill_sequence: List[str]) -> Optional[str]:
        """Autonomously constructs an executable pipeline combining multiple skills."""
        for skill in skill_sequence:
            if skill not in self.skills:
                return None

        code_lines = [f"def {pipeline_name}(*args, **kwargs):"]
        code_lines.append(f"    # Autonomously synthesized composite pipeline from: {' -> '.join(skill_sequence)}")

        if len(skill_sequence) == 2:
            s1, s2 = skill_sequence[0], skill_sequence[1]
            code_lines.append(f"    intermediate = {s1}(*args, **kwargs)")
            code_lines.append(f"    return {s2}(intermediate)")
        elif len(skill_sequence) == 3:
            s1, s2, s3 = skill_sequence[0], skill_sequence[1], skill_sequence[2]
            code_lines.append(f"    step1 = {s1}(*args, **kwargs)")
            code_lines.append(f"    step2 = {s2}(step1)")
            code_lines.append(f"    return {s3}(step2)")
        else:
            code_lines.append(f"    res = {skill_sequence[0]}(*args, **kwargs)")
            for s in skill_sequence[1:]:
                code_lines.append(f"    res = {s}(res)")
            code_lines.append("    return res")

        composite_code = "\n".join(code_lines)
        reg_ok = self.register_skill(
            name=pipeline_name,
            docstring=f"Composite pipeline chaining: {' -> '.join(skill_sequence)}",
            code=composite_code
        )
        if reg_ok:
            for i in range(len(skill_sequence) - 1):
                self.edges.append((skill_sequence[i], skill_sequence[i+1]))
            return composite_code
        return None

    def get_skill_docs(self) -> str:
        if not self.skills:
            return "No procedural skills registered."
        return "\n".join([f"- `{s.name}`({', '.join(s.inputs)}) -> {', '.join(s.outputs)}: {s.docstring}" for s in self.skills.values()])
