# 🏛️ Sarthika Cognitive Architecture 3.0: The Expert AGI Specification & Evaluation Framework

**Target Designation:** Sarthika Autonomous Cognitive System — Phase 3  
**Classification:** Level 3 AGI (Expert AGI — 90th Percentile of Skilled Human Practitioners)  
**Foundational Paradigm:** Dual-Process Cognitive Engine, Monte Carlo Tree Search over Thoughts (MCTS-ToT), Causal World Modeling, and Compositional Skill Graphs  
**Prior Baseline:** Level 2 Competent AGI (`AGI_Cognitive_Agent_v2.ipynb`)

---

## 1. Executive Summary & Paradigm Shift

In Sarthika 2.0 (Level 2 Competent AGI), the agent achieved closed-loop execution and self-healing:
* Proposing 3 candidate strategies per subtask.
* Executing candidates in transactional sandboxes.
* Scoring candidates with an empirical critic.
* Trapping errors via Reflexion backtracking.

However, Level 2 systems suffer from **Myopic Greediness**: they decide action-by-action. If Step 1 selects a candidate that yields a high immediate score but leaves the system in a state where Step 3 is mathematically or computationally impossible, a greedy agent collapses.

**Sarthika 3.0 (Level 3 Expert AGI)** transcends myopic decision-making through four cognitive breakthroughs:

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                           SARTHIKA 3.0 COGNITIVE CORE                        │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌──────────────────────┐    ┌──────────────────────┐    ┌─────────────────┐ │
│  │   Deliberative MCTS  │    │  Causal World Model  │    │  Skill Graph    │ │
│  │   Search Tree        │◄──►│  Mental Simulator    │◄──►│  DAG Composer   │ │
│  │   (Lookahead / UCT)  │    │  (State-Delta Invar) │    │  (Higher-Order) │ │
│  └──────────┬───────────┘    └──────────┬───────────┘    └────────┬────────┘ │
│             │                           │                         │          │
│             ▼                           ▼                         ▼          │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │      System 2 Epistemic Critic & Dynamic Reflexion 2.0 Controller       │ │
│  └──────────────────────────────────────┬──────────────────────────────────┘ │
│                                         │                                    │
│                                         ▼                                    │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │      Transactional Execution Kernel & Lifelong Memory Consolidation     │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Core Architectural Pillars of Sarthika 3.0

### Pillar I: Deliberative Tree-of-Thoughts via MCTS (The Lookahead Mind)
* **The Problem in Level 2:** Evaluates only $P(a_t | s_t)$ greedily.
* **The Level 3 Solution:** Formulates multi-step problem solving as a Markov Decision Process (MDP) over reasoning graphs:
  $$\max_{\pi} \mathbb{E} \left[ \sum_{t=0}^T \gamma^t R(s_t, a_t) \right]$$
* **MCTS Cycle over Reasoning Nodes:**
  1. **Selection:** Traverse the tree from root using the **Upper Confidence Bound applied to Trees (UCT)**:
     $$\text{UCT}(v, a) = Q(v, a) + c \cdot \sqrt{\frac{\ln N(v)}{N(v, a)}}$$
     where $Q(v, a)$ is the expected terminal reward, $N(v)$ is parent visit count, $N(v, a)$ is action visit count, and $c = 1.414$ balances exploitation and exploration.
  2. **Expansion:** System 1 generates candidate reasoning branches from the selected node.
  3. **Mental Simulation (Rollout):** System 2 projects the branch forward using the Causal World Model.
  4. **Backpropagation:** Terminal critic scores propagate backward up the path, updating visit counts $N$ and value estimates $Q$.

---

### Pillar II: Causal World Model (Mental Simulation Sandbox)
* **The Problem in Level 2:** All verification requires physical code execution, incurring latency and failing when unpickleable closures or resource-heavy loops arise.
* **The Level 3 Solution:** A lightweight symbolic simulator that runs *before* real execution:
  * **AST Invariant Verification:** Detects recursion depth, unbound variables, unsafe global mutations, and non-serializable lambdas.
  * **State-Delta Prediction ($\Delta S$):** Predicts variable changes, schema transformations, and output signatures.
  * **Epistemic Fault Preemption:** If an action violates conservation laws or mathematical bounds (e.g. modular arithmetic properties, prime factor completeness), the branch is pruned with a negative score *before* execution.

---

### Pillar III: Compositional Skill Graph (DAG of Capabilities)
* **The Problem in Level 2:** Skills are isolated functions (`prime_factorization`, `gcd`, `collatz_analyzer`). The agent must re-synthesize glue code manually.
* **The Level 3 Solution:** A Directed Acyclic Graph (DAG) where nodes are verified skills with explicit type signatures, preconditions, and postconditions:
  $$\mathcal{G} = (\mathcal{V}_{\text{skills}}, \mathcal{E}_{\text{dataflow}})$$
* **Autonomous Pipe Synthesis:** Sarthika 3.0 can construct higher-order pipelines:
  $$\text{Pipeline} = f_k \circ f_j \circ f_i$$
  with automatic parameter binding and runtime contract validation.

---

### Pillar IV: Dynamic Reflexion 2.0 with Adaptive Temperature
* When a search trajectory experiences repeated low critic evaluations, the system increases generation entropy ($\mathcal{T} = 0.85$) to explore distant conceptual associations.
* When evaluating terminal validation steps, entropy is quenched ($\mathcal{T} = 0.10$) for precision.

---

## 3. The Level 3 (Expert AGI) Evaluation Framework

How do we scientifically prove that Sarthika has reached Level 3 (Expert AGI)?  
We subject Sarthika to **four rigorous benchmark challenges** that a greedy Level 2 agent will systematically fail:

### Benchmark 1: The Multi-Step Lookahead Trap (Deliberation vs. Greediness)
* **Challenge:** Given a composite number $N$, find its prime factors, calculate the totient function $\phi(N)$, and find the minimal primitive root modulo $N$.
* **The Trap:** A greedy Level 2 agent generates an exhaustive $O(N)$ trial search at Step 1 because it's fast to write. But at Step 3, computing primitive roots with large numbers times out or crashes.
* **Level 3 Pass Condition:** MCTS deliberates 2 steps ahead, selects an $O(\sqrt{N})$ or factorization-based generator at Step 1, and effortlessly completes Step 3 with verified mathematical proof.

### Benchmark 2: Zero-Shot Autonomous Tool Composition
* **Challenge:** Given an unseen task ("Analyze whether $F_{45}$ has any common prime factors with the 7th Fermat number $F_7 = 2^{2^7} + 1$"), Sarthika must:
  1. Retrieve existing `fib_matrix_exponentiation` and `prime_factors` from Procedural Memory.
  2. Synthesize an optimized modular Fermat evaluator.
  3. Wire all 3 into an automated pipeline using the Skill Graph without writing boilerplate from scratch.
* **Level 3 Pass Condition:** 100% automated tool chaining with zero human guidance and zero runtime crash.

### Benchmark 3: Causal Preemption & Closure Serialization (Self-Correction of v2's Failure)
* **Challenge:** In Sarthika 2.0 Experiment 1, Step 4 failed because `pickle` cannot serialize dynamic interactive IPython closures (`_pickle.PicklingError`).
* **Level 3 Pass Condition:** The Causal World Model flags closure pickling *before execution*, directs System 1 to synthesize a source-reification or `dill`-compatible serializer, and verifies 100% serialization of dynamic memory functions.

### Benchmark 4: Epistemic Calibration & Hallucination Resistance
* **Challenge:** Present an unproven or false conjecture (e.g., "Verify that all odd Fibonacci numbers are prime").
* **Level 3 Pass Condition:** Sarthika must formulate a counterexample search ($F_9 = 34 = 2 \times 17$ is even, $F_{10}=55=5\times 11$ is odd and composite), falsify the conjecture, and refuse to claim verification.

---

## 4. Quantitative Metrics Dashboard

| Metric | Level 2 (Competent) | Level 3 (Expert Target) | Measurement Method |
| :--- | :---: | :---: | :--- |
| **Search Horizon** | 1-step greedy ($D=1$) | Multi-step tree ($D \ge 3$) | Max depth in MCTS reasoning graph |
| **Dead-End Avoidance** | $40\% - 50\%$ | $\mathbf{\ge 90\%}$ | Lookahead trap test cases passed |
| **Tool Composition Rate** | $0\%$ (Manual) | $\mathbf{\ge 85\%}$ (Autonomous) | DAG pipeline syntheses without human glue |
| **Causal Preemption** | $0\%$ (Runs blind) | $\mathbf{\ge 75\%}$ | AST invariant errors caught pre-execution |
| **Epistemic Calibration** | Brier Score $\approx 0.25$ | **Brier Score $\le 0.08$** | Predicted confidence vs actual verification |

---

## 5. File & Artifact Mapping

* `Sarthika_Expert_AGI_v3_Architecture_and_Evaluation.md`: This comprehensive specification.
* `build_v3_notebook.py`: Generator script with automated AST syntax validation.
* `AGI_Cognitive_Agent_v3.ipynb`: The deployable Level 3 Expert AGI Colab notebook.

