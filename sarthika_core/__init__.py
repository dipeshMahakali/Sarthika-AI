# -*- coding: utf-8 -*-
"""
Sarthika Cognitive Architecture 3.0: Modular Micro-AGI Framework
"""

from .engine import BaseCognitiveEngine, GroqEngine, OpenAIEngine, MockCognitiveEngine, LocalTransformersEngine
from .memory import WorkingMemory, SemanticMemory, EpisodicMemory
from .sandbox import PersistentTransactionalSandbox
from .skill_graph import CompositionalSkillGraph, SkillNode
from .world_model import CausalWorldModel
from .mcts import MCTSNode, MonteCarloThoughtSearch
from .metacognition import MetacognitivePlanner, System2Critic
from .harvester import RLVRTrajectoryHarvester
from .agent import AutonomousCognitiveAgentV3

from .benchmark import run_level3_benchmark

def create_sarthika_expert(engine: BaseCognitiveEngine) -> AutonomousCognitiveAgentV3:
    """Convenience factory to instantiate a fully wired Sarthika 3.0 Expert AGI instance."""
    working_mem = WorkingMemory()
    semantic_mem = SemanticMemory()
    episodic_mem = EpisodicMemory()
    master_sandbox = PersistentTransactionalSandbox()
    skill_graph = CompositionalSkillGraph(master_sandbox)
    world_model = CausalWorldModel()
    mcts_engine = MonteCarloThoughtSearch(world_model)
    planner = MetacognitivePlanner(engine)
    critic = System2Critic(engine)
    harvester = RLVRTrajectoryHarvester()

    return AutonomousCognitiveAgentV3(
        engine=engine,
        working_mem=working_mem,
        semantic_mem=semantic_mem,
        episodic_mem=episodic_mem,
        skill_graph=skill_graph,
        master_sandbox=master_sandbox,
        planner=planner,
        critic=critic,
        harvester=harvester,
        world_model=world_model,
        mcts=mcts_engine
    )

__all__ = [
    "BaseCognitiveEngine",
    "GroqEngine",
    "OpenAIEngine",
    "MockCognitiveEngine",
    "LocalTransformersEngine",
    "WorkingMemory",
    "SemanticMemory",
    "EpisodicMemory",
    "PersistentTransactionalSandbox",
    "CompositionalSkillGraph",
    "SkillNode",
    "CausalWorldModel",
    "MCTSNode",
    "MonteCarloThoughtSearch",
    "MetacognitivePlanner",
    "System2Critic",
    "RLVRTrajectoryHarvester",
    "AutonomousCognitiveAgentV3",
    "create_sarthika_expert",
    "run_level3_benchmark"
]
