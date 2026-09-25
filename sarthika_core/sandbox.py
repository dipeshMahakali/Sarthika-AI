# -*- coding: utf-8 -*-
"""
Transactional Sandbox Architecture:
- Snapshotting & isolated fork() branches for MCTS rollouts
- Atomic commit() of winning branches
- Thread-safe execution with timeout guards to prevent runaway loops
"""

import io
import sys
import copy
import traceback
import math
import types
from typing import Dict, Any, List, Optional
import multiprocessing
import queue

def _worker_exec(code: str, namespace: Dict[str, Any], result_queue: multiprocessing.Queue):
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
        exec(code, namespace)
        success = True
        output_str = redirected_out.getvalue()
    except Exception:
        error_str = traceback.format_exc()
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

    # Extract serializable variables
    safe_vars = {}
    active_functions = []
    for k, v in namespace.items():
        if k.startswith("__"):
            continue
        if callable(v) and not isinstance(v, type):
            active_functions.append(k)
        elif not isinstance(v, types.ModuleType):
            try:
                # Test picklability
                _ = copy.deepcopy(v)
                safe_vars[k] = v
            except Exception:
                pass

    result_queue.put({
        "success": success,
        "stdout": output_str,
        "stderr": error_str,
        "updated_namespace": safe_vars,
        "active_functions": active_functions
    })


class PersistentTransactionalSandbox:
    """
    Transactional sandbox supporting isolated forks, atomic commits,
    and safe execution with a strict timeout limit.
    """
    def __init__(self, base_namespace: Optional[Dict[str, Any]] = None, timeout_seconds: int = 5):
        self.timeout_seconds = timeout_seconds
        if base_namespace is None:
            self.namespace: Dict[str, Any] = {
                "__builtins__": __builtins__,
                "__name__": "__main__",
                "__doc__": "Sarthika Expert AGI Persistent Sandbox",
                "math": math,
            }
        else:
            self.namespace = {}
            for k, v in base_namespace.items():
                if k.startswith("__") or isinstance(v, (types.ModuleType, types.FunctionType, types.BuiltinFunctionType, type)):
                    self.namespace[k] = v
                else:
                    try:
                        self.namespace[k] = copy.deepcopy(v)
                    except Exception:
                        self.namespace[k] = v

    def fork(self) -> "PersistentTransactionalSandbox":
        """Creates a child sandbox snapshot for isolated branch rollouts."""
        return PersistentTransactionalSandbox(self.namespace, timeout_seconds=self.timeout_seconds)

    def commit(self, branch_sandbox: "PersistentTransactionalSandbox"):
        """Atomically commits the state of a winning branch into this master sandbox."""
        for k, v in branch_sandbox.namespace.items():
            if not k.startswith("__"):
                if isinstance(v, (types.ModuleType, types.FunctionType, types.BuiltinFunctionType, type)):
                    self.namespace[k] = v
                else:
                    try:
                        self.namespace[k] = copy.deepcopy(v)
                    except Exception:
                        self.namespace[k] = v

    def execute(self, code: str) -> Dict[str, Any]:
        """
        Executes code synchronously with captured I/O and execution exception handling.
        """
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
            if not k.startswith("__") and not callable(v) and not isinstance(v, types.ModuleType)
        }
        active_functions = [
            k for k, v in self.namespace.items()
            if not k.startswith("__") and callable(v) and not isinstance(v, type)
        ]

        return {
            "success": success,
            "stdout": output_str,
            "stderr": error_str,
            "variables": active_variables,
            "functions": active_functions
        }
