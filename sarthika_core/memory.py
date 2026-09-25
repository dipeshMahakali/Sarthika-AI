# -*- coding: utf-8 -*-
"""
Tripartite Memory Architecture:
1. Working Memory (Hierarchical goal scratchpad, MCTS active node, reflexion history)
2. Semantic Memory (SQLite-backed relational knowledge graph for formal axioms)
3. Episodic Memory (FAISS vector store with lightweight TF-IDF / lexical fallback)
"""

import sqlite3
import json
import math
import re
from typing import List, Dict, Any, Optional

class WorkingMemory:
    """Dynamic short-term memory buffer maintaining search trees, goals, and active hypotheses."""
    def __init__(self):
        self.active_goal: str = ""
        self.subtasks: List[Dict[str, Any]] = []
        self.current_step: int = 0
        self.scratchpad: List[str] = []
        self.reflexion_history: List[str] = []
        self.active_search_tree: Dict[str, Any] = {}

    def reset(self, goal: str):
        self.active_goal = goal
        self.subtasks = []
        self.current_step = 0
        self.scratchpad = []
        self.reflexion_history = []
        self.active_search_tree = {}

    def add_thought(self, thought: str):
        self.scratchpad.append(thought)

    def log_reflexion(self, reflection: str):
        self.reflexion_history.append(reflection)


class SemanticMemory:
    """Relational knowledge graph storing verified axioms, mathematical theorems, and domain constants."""
    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_db()
        self._seed_foundational_axioms()

    def _init_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS facts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entity TEXT UNIQUE,
            definition TEXT,
            confidence REAL
        )''')
        self.conn.commit()

    def _seed_foundational_axioms(self):
        axioms = [
            ("Fibonacci Matrix Doubling", "[[1,1],[1,0]]^n computes F(n+1), F(n) in O(log n) time via binary exponentiation.", 1.0),
            ("Euler Totient Function", "phi(n) = n * prod(1 - 1/p) for each unique prime factor p dividing n.", 1.0),
            ("Primitive Root Invariant", "g is a primitive root modulo n iff g^(phi(n)/p) != 1 (mod n) for all prime factors p of phi(n).", 1.0),
            ("Mersenne & Lucas-Lehmer", "M_p = 2^p - 1 is prime iff S_{p-2} = 0 mod M_p where S_0 = 4, S_i = S_{i-1}^2 - 2.", 1.0),
            ("Collatz Stopping Time", "T(n) is the number of steps to reach 1: n/2 if even, 3n+1 if odd.", 1.0),
        ]
        for ent, defn, conf in axioms:
            self.store_fact(ent, defn, conf)

    def store_fact(self, entity: str, definition: str, confidence: float = 1.0):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT OR REPLACE INTO facts (entity, definition, confidence)
                          VALUES (?, ?, ?)''', (entity, definition, confidence))
        self.conn.commit()

    def query_fact(self, entity: str) -> str:
        cursor = self.conn.cursor()
        cursor.execute("SELECT definition FROM facts WHERE entity LIKE ?", (f"%{entity}%",))
        row = cursor.fetchone()
        return row[0] if row else ""

    def get_all_facts(self) -> List[str]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT entity, definition FROM facts ORDER BY id DESC LIMIT 20")
        rows = cursor.fetchall()
        return [f"- {r[0]}: {r[1]}" for r in rows]


class EpisodicMemory:
    """FAISS Vector Store for cross-task experience retrieval, with zero-dependency fallback."""
    def __init__(self, embedding_model_name: str = "all-MiniLM-L6-v2"):
        self.episodes: List[Dict[str, Any]] = []
        self.has_faiss = False
        try:
            from sentence_transformers import SentenceTransformer
            import faiss
            import numpy as np
            self.np = np
            self.embedder = SentenceTransformer(embedding_model_name)
            try:
                self.dimension = self.embedder.get_embedding_dimension()
            except AttributeError:
                self.dimension = self.embedder.get_sentence_embedding_dimension()
            self.index = faiss.IndexFlatL2(self.dimension)
            self.has_faiss = True
        except ImportError:
            self.has_faiss = False

    def record_episode(self, task: str, action: str, result: str, success: bool, reflection: str, reward_score: float = 1.0):
        episode = {
            "task": task,
            "action": action,
            "result": result,
            "success": success,
            "reflection": reflection,
            "reward_score": reward_score
        }
        self.episodes.append(episode)
        if self.has_faiss:
            text_rep = f"Task: {task} | Success: {success} | Reflection: {reflection}"
            embedding = self.embedder.encode([text_rep])[0].astype("float32")
            self.index.add(self.np.array([embedding]))

    def recall_similar(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        if not self.episodes:
            return []
        if self.has_faiss:
            query_vector = self.embedder.encode([query])[0].astype("float32")
            distances, indices = self.index.search(self.np.array([query_vector]), min(top_k, len(self.episodes)))
            results = []
            for idx in indices[0]:
                if idx != -1 and idx < len(self.episodes):
                    results.append(self.episodes[idx])
            return results
        else:
            # Lexical keyword similarity fallback
            q_words = set(re.findall(r"\w+", query.lower()))
            scored = []
            for ep in self.episodes:
                ep_words = set(re.findall(r"\w+", (ep["task"] + " " + ep["reflection"]).lower()))
                overlap = len(q_words.intersection(ep_words))
                scored.append((overlap, ep))
            scored.sort(key=lambda x: x[0], reverse=True)
            return [ep for score, ep in scored[:top_k]]
