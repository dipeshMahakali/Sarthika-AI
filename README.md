# 🧠 Sarthika Autonomous Cognitive Architecture 3.0 (Level-2 Micro-AGI Engine)
## Dual-Process Reasoning, Test-Time Tree Search with Reflexion, and Synaptic Self-Evolution

This workspace contains the state-of-the-art implementation of the Sarthika Cognitive Agent:
📁 **[`AGI_Cognitive_Agent_v2.ipynb`](./AGI_Cognitive_Agent_v2.ipynb)**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dipeshMahakali/Sarthika-AI/blob/main/AGI_Cognitive_Agent_v2.ipynb)

---

## 🌟 What's New in Architecture 3.0

1. **Reflexion Backtracking & Epistemic Gate ($\tau = 0.65$):**
   - The agent never blindly advances past failed steps or empty print statements.
   - If candidate solutions fail or score below $0.65$, System 2 diagnoses the error trace and triggers a self-correction repair loop (up to 3 attempts).
2. **Resilient AST/Grammar Code Synthesizer:**
   - Multi-tier code block parsing that extracts valid Python code regardless of markdown header styles, eliminating silent fallback failures.
3. **Decoupled Transactional Sandbox:**
   - Deep-copied isolated state execution (`fork()` & `commit()`) with math and computational tool integration.
4. **Catastrophic Forgetting Prevention & Tripartite Memory:**
   - **Procedural Skill Bank:** Built-in and dynamically synthesized functions (`prime_factorization`, `gcd`, `collatz_analyzer`, matrix exponents) are persistently cataloged with signatures.
   - **Semantic Knowledge Graph:** Persistent SQLite engine storing discovered constants, theorems, and mathematical assertions.
   - **Episodic Vector Memory:** FAISS + SentenceTransformers embeddings for cross-task experiential transfer.
5. **Synaptic Weight Consolidation (RLVR LoRA Engine):**
   - Verified execution trajectories ($V \ge 0.70$) are harvested and formatted for Parameter-Efficient Fine-Tuning (LoRA rank $r=16$, $\alpha=32$) directly on Google Colab's free T4 GPU.

---

## 🚀 Quickstart: Run in Google Colab

1. Navigate to: **[https://colab.research.google.com/](https://colab.research.google.com/)**
2. In the modal dialog, select the **Upload** tab.
3. Drag and drop **`AGI_Cognitive_Agent_v2.ipynb`** from this repository.
4. Enable GPU acceleration:
   - Click **Runtime** $\rightarrow$ **Change runtime type**.
   - Under *Hardware accelerator*, select **T4 GPU** (Free).
   - Click **Save**.
5. Click **Runtime** $\rightarrow$ **Run all** (or execute cells sequentially).

---

##  Cognitive Modules & Theoretical Foundations

| Module | Core Functionality | Theoretical Origin |
| :--- | :--- | :--- |
| **Cognitive Engine** | 4-bit Quantized `Qwen2.5-7B-Instruct` loaded into Colab's 16GB VRAM. | Foundation Reasoning Model |
| **System 1 (Generator)** | Parallel multi-hypothesis generation (Candidate A, B, C) with diversity sampling. | Dual-Process Theory (Kahneman) |
| **System 2 (Critic)** | Objective verification of execution output, runtime error trapping, and value estimation. | Metacognitive Monitoring & Reflexion |
| **Working Memory** | Dynamic scratchpad, hierarchical subtask tree, and reflexion history. | Cognitive Psychology (Baddeley) |
| **Episodic Memory** | FAISS vector store + SentenceTransformers embedding of past trajectories. | Dual-Process Memory |
| **Semantic Memory** | SQLite relational knowledge base storing persistent entities and domain assertions. | Neuro-symbolic Knowledge Graph |
| **Procedural Memory (Skills)** | Autonomous code synthesis and persistent tool bank (retains old skills, learns new ones). | Voyager / Eureka Paradigm |
| **Synaptic Consolidation** | RLVR trajectory harvesting and LoRA adapter fine-tuning on Colab GPU. | Synaptic Plasticity / Continual Learning |

---

## 🧪 Benchmark Tasks Included

* **Experiment 1 (Algorithmic Discovery):** Computes $F_{60} \pmod{10^9+7}$ using $O(\log n)$ matrix exponentiation, persists functions in memory, and factorizes the result.
* **Experiment 2 (Lifelong Transfer Learning):** Reuses previously synthesized matrix and factorization skills to analyze $F_{35}$ and prime factors of 105 without forgetting.
* **Interactive Terminal:** Enter any arbitrary mathematical, scientific, or code reasoning goal to watch Sarthika synthesize, execute, critique, and self-heal in real time.
