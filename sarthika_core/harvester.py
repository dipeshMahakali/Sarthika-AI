# -*- coding: utf-8 -*-
"""
RLVR Trajectory Harvester Subsystem:
- Filters verified trajectories (V >= 0.70)
- Stores structured trajectories in JSONL for downstream LoRA synaptic weight consolidation
"""

import json
from datetime import datetime, timezone
from typing import Dict, Any, List

class RLVRTrajectoryHarvester:
    """Strict quality filter harvesting verified trajectories (V >= 0.70) for synaptic adaptation."""
    def __init__(self, dataset_file: str = "cognitive_trajectories.jsonl", min_reward_threshold: float = 0.70):
        self.dataset_file = dataset_file
        self.min_reward_threshold = min_reward_threshold
        self.in_memory_buffer: List[Dict[str, Any]] = []

    def harvest(self, goal: str, subtask: str, winning_candidate: str, code: str, exec_result: Dict[str, Any], critic_score: float, reflection: str) -> bool:
        if critic_score < self.min_reward_threshold or not exec_result.get("success", False):
            return False

        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "goal": goal,
            "subtask": subtask,
            "winning_candidate": winning_candidate,
            "code": code,
            "stdout": exec_result.get("stdout", ""),
            "reward_score": critic_score,
            "reflection": reflection
        }
        self.in_memory_buffer.append(entry)
        try:
            with open(self.dataset_file, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception:
            pass
        return True

    def get_trajectory_count(self) -> int:
        return len(self.in_memory_buffer)

    def get_all_trajectories(self) -> List[Dict[str, Any]]:
        return self.in_memory_buffer
