# Autonomous Cognitive Architecture (Micro-AGI Engine)
## Google Colab GPU-Accelerated Implementation

This workspace contains the complete, ready-to-run Jupyter Notebook:
📁 **[`AGI_Cognitive_Agent.ipynb`](./AGI_Cognitive_Agent.ipynb)**

---

## 🚀 How to Run in Google Colab (Immediate Setup)

1. Open your browser and go to: **[https://colab.research.google.com/](https://colab.research.google.com/)**
2. In the modal dialog, select the **Upload** tab.
3. Drag and drop **`AGI_Cognitive_Agent.ipynb`** from this directory (`/var/www/html/dipesh/Portfolio/sarthika/AGI_Cognitive_Agent.ipynb`).
4. In Colab, enable GPU acceleration:
   - Click **Runtime** in the top menu $\rightarrow$ **Change runtime type**.
   - Under *Hardware accelerator*, select **T4 GPU** (Free).
   - Click **Save**.
5. Click **Runtime** $\rightarrow$ **Run all** (or run cells sequentially from top to bottom).

---

## 🧠 Cognitive Capabilities Implemented

| Module | Core Functionality | Theoretical Origin |
| :--- | :--- | :--- |
| **Cognitive Engine** | 4-bit Quantized `Qwen2.5-7B-Instruct` loaded directly into Colab's 16GB VRAM. | Foundation Reasoning Model |
| **Working Memory** | Dynamic scratchpad, active sub-task tree, and attention budgeting. | Cognitive Psychology (Baddeley) |
| **Episodic Memory** | FAISS vector store + SentenceTransformers embedding of past actions and outcomes for cross-task transfer learning. | Dual-Process Memory |
| **Semantic Memory** | SQLite relational knowledge base storing persistent entities and domain assertions. | Neuro-symbolic Knowledge Graph |
| **Procedural Memory (Skills)** | Autonomous code synthesis: The agent writes Python tools, runs them in an execution sandbox, catches bugs, and registers them dynamically into a persistent tool registry. | Voyager / Eureka Paradigm |
| **Metacognition (Critic)** | System 2 self-reflection module verifying execution outputs, identifying errors, and adjusting hypotheses. | Kahneman System 1 & System 2 |

