# -*- coding: utf-8 -*-
"""
Monte Carlo Thought Search (MCTS-ToT):
- Tree search over cognitive reasoning nodes
- UCT-based node selection and multi-candidate backpropagation
"""

import math
from typing import Dict, Any, List, Optional

class MCTSNode:
    """A node in the Monte Carlo Thought Search Tree."""
    def __init__(self, state_description: str, code_action: str = "", parent: Optional["MCTSNode"] = None, depth: int = 0):
        self.state_description = state_description
        self.code_action = code_action
        self.parent = parent
        self.children: List["MCTSNode"] = []
        self.depth = depth
        self.visits: int = 0
        self.value_sum: float = 0.0
        self.terminal_score: float = 0.0
        self.is_terminal: bool = False
        self.execution_result: Optional[Dict[str, Any]] = None

    @property
    def q_value(self) -> float:
        return self.value_sum / self.visits if self.visits > 0 else 0.0

    def uct_score(self, exploration_constant: float = 1.414) -> float:
        """Upper Confidence Bound applied to Trees (UCT)."""
        if self.visits == 0:
            return float("inf")
        exploitation = self.q_value
        parent_visits = max(1, self.parent.visits) if self.parent else 1
        exploration = exploration_constant * math.sqrt(math.log(parent_visits) / self.visits)
        return exploitation + exploration

    def add_child(self, child_node: "MCTSNode") -> "MCTSNode":
        self.children.append(child_node)
        return child_node

    def to_tree_dict(self) -> Dict[str, Any]:
        """Recursive dictionary serialization for front-end tree rendering."""
        return {
            "name": self.state_description,
            "q_value": round(self.q_value, 2),
            "visits": self.visits,
            "terminal_score": round(self.terminal_score, 2),
            "children": [c.to_tree_dict() for c in self.children]
        }


class MonteCarloThoughtSearch:
    """Deliberative MCTS Lookahead Engine for multi-step reasoning."""
    def __init__(self, world_model, exploration_weight: float = 1.414):
        self.world_model = world_model
        self.c = exploration_weight

    def select(self, node: MCTSNode) -> MCTSNode:
        curr = node
        while curr.children and not curr.is_terminal:
            best_child = max(curr.children, key=lambda c: c.uct_score(self.c))
            curr = best_child
        return curr

    def backpropagate(self, node: MCTSNode, value: float):
        curr = node
        while curr is not None:
            curr.visits += 1
            curr.value_sum += value
            curr = curr.parent
