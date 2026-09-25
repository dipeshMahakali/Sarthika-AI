# -*- coding: utf-8 -*-
"""
Causal World Model Subsystem:
- Pre-execution symbolic mental simulation engine
- Verifies AST invariants, intercepts illegal system calls, predicts Delta S state changes
"""

import ast
from typing import Dict, Any, List

class CausalWorldModel:
    """Pre-execution symbolic mental simulation engine."""
    def __init__(self):
        self.prohibited_modules = ["os", "sys", "subprocess", "shutil", "socket", "pty", "builtins"]

    def simulate_mental_consequence(self, code: str, current_namespace_keys: List[str]) -> Dict[str, Any]:
        """Performs static symbolic analysis and predicts state transformations."""
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return {
                "viable": False,
                "confidence": 0.0,
                "reason": f"AST Syntax Error: {e.msg} at line {e.lineno}",
                "predicted_state_delta": []
            }

        declared_functions = []
        assigned_variables = []
        imported_modules = []
        has_while_loop = False
        unsafe_calls = []
        has_pickle_risk = False

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                declared_functions.append(node.name)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        assigned_variables.append(target.id)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imported_modules.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imported_modules.append(node.module)
            elif isinstance(node, ast.While):
                has_while_loop = True
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in self.prohibited_modules:
                        unsafe_calls.append(node.func.id)
                    if node.func.id == "pickle":
                        has_pickle_risk = True
                elif isinstance(node.func, ast.Attribute):
                    if isinstance(node.func.value, ast.Name):
                        if node.func.value.id in self.prohibited_modules:
                            unsafe_calls.append(node.func.value.id)
                        if node.func.value.id == "pickle":
                            has_pickle_risk = True

        # Preemptive fault check: Pickling dynamic closures
        if "pickle" in imported_modules or has_pickle_risk:
            return {
                "viable": False,
                "confidence": 0.20,
                "reason": "Causal Invariant Violation: Naive 'pickle' detected for dynamic session objects. Use 'dill' or source reification.",
                "predicted_state_delta": []
            }

        # Check for prohibited modules
        for mod in imported_modules:
            for p in self.prohibited_modules:
                if mod == p or mod.startswith(p + "."):
                    return {
                        "viable": False,
                        "confidence": 0.0,
                        "reason": f"Safety Invariant Violation: Module '{mod}' is prohibited in safe cognitive sandbox.",
                        "predicted_state_delta": []
                    }

        if unsafe_calls:
            return {
                "viable": False,
                "confidence": 0.0,
                "reason": f"Safety Invariant Violation: Call '{unsafe_calls[0]}' is prohibited in sandbox.",
                "predicted_state_delta": []
            }

        predicted_delta = list(set(declared_functions + assigned_variables))

        return {
            "viable": True,
            "confidence": 0.90 if not has_while_loop else 0.75,
            "reason": "Static invariant verification passed. No structural anomalies detected.",
            "predicted_state_delta": predicted_delta,
            "has_while_loop": has_while_loop
        }
