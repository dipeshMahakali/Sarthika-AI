# 🚀 100% Free Hosting Guide: Sarthika AGI 3.0 for Public Testing

> [!NOTE]
> **Why Hugging Face shows "Paid" for Gradio/Docker:**
> Hugging Face recently restricted backend compute instances (Gradio and Docker servers) behind a paid **PRO subscription ($9/mo)** for unverified accounts. Only static client-side spaces remain free on Hugging Face.
> 
> **The Solution:** Use **Streamlit Community Cloud** (sponsored by Snowflake), which is **100% FREE forever**, requires **no credit card**, and connects directly to your GitHub repository to host Python applications 24/7 with a public URL.

---

## 🏛️ The Free Hosting Architecture: Decoupled Cognitive Engine

Running a 7B or 70B foundation model on dedicated cloud GPUs (e.g. AWS or RunPod) typically costs \$50–\$200/month. We eliminate this cost completely:

```
┌────────────────────────────────────────────────────────────────────────┐
│                      1. FRONTEND & ORCHESTRATION                      │
│        Streamlit Community Cloud (100% Free: Unlimited Uptime)         │
│                                                                        │
│   • Streamlit Web App (24/7 Public URL: https://sarthika.streamlit.app)│
│   • Transactional Execution Sandbox (fork / commit)                   │
│   • Causal World Model (AST Invariant Verification)                    │
│   • Episodic Vector Memory (FAISS) & Semantic Memory (SQLite)         │
│   • Compositional Skill Graph DAG                                      │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    │ HTTPS API Calls (Zero Latency)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      2. HIGH-SPEED INFERENCE BACKEND                   │
│            Groq Cloud API (Free Tier: 30 RPM, 14,400 req/day)          │
│                                                                        │
│   • Llama 3.3 70B Versatile / Qwen 2.5 32B                             │
│   • 300 to 500 tokens/second (Sub-second response per candidate)       │
│   • Zero Credit Card Required                                          │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🌟 Method 1: Streamlit Community Cloud (Recommended #1)
* **Cost:** **$0.00 Forever**
* **Credit Card:** **None required**
* **Uptime:** **24/7 Permanent Public URL**
* **Setup Time:** ~3 minutes

### Step 1: Push Sarthika Code to Your GitHub Repository
Ensure your GitHub repo (`dipeshMahakali/Sarthika-AI`) contains the newly created modular files:
* `streamlit_app.py`
* `requirements.txt`
* `sarthika_core/`

In this repository directory, run:
```bash
git add streamlit_app.py app.py requirements.txt sarthika_core/ FREE_HOSTING_GUIDE.md .gitignore
git commit -m "Add Streamlit web app and modular core for free cloud hosting"
git push origin main
```

### Step 2: Get a Free Groq API Key (30 Seconds)
1. Go to [https://console.groq.com/keys](https://console.groq.com/keys).
2. Sign in with GitHub or Google (zero credit card requested).
3. Click **Create API Key** and copy it (`gsk_...`).

### Step 3: Deploy on Streamlit Community Cloud
1. Navigate to **[https://share.streamlit.io/](https://share.streamlit.io/)** (or [streamlit.io/cloud](https://streamlit.io/cloud)).
2. Sign in with your GitHub account.
3. Click **"Create app"** (or **"New app"**).
4. Fill in the deployment fields:
   * **Repository:** `dipeshMahakali/Sarthika-AI`
   * **Branch:** `main`
   * **Main file path:** `streamlit_app.py`
   * **App URL (optional):** e.g., `sarthika-agi` (becomes `sarthika-agi.streamlit.app`)
5. Click **"Advanced settings"** (bottom left):
   * Select Python **3.10** or **3.11**.
   * Under **Secrets**, paste your free Groq API key:
     ```toml
     GROQ_API_KEY = "gsk_your_actual_key_here"
     ```
6. Click **Save**, then click **Deploy!**

Within 60 to 90 seconds, your Sarthika AGI engine is live 24/7 at:
```
https://<your-app-name>.streamlit.app
```

---

## 🌐 Method 2: Embed Sarthika on Your Portfolio Website

Once your Streamlit app is live, you can embed the interactive terminal directly on your portfolio website (`/var/www/html/dipesh/Portfolio`):

```html
<section id="sarthika-demo" style="width: 100%; max-width: 1200px; margin: 40px auto; padding: 0 16px;">
  <h2 style="text-align: center; color: #4F46E5; font-family: system-ui, sans-serif; margin-bottom: 8px;">
    🧠 Sarthika 3.0 (Level 3 Expert AGI) — Live Interactive Terminal
  </h2>
  <p style="text-align: center; color: #6B7280; margin-bottom: 24px;">
    Autonomous dual-process reasoning, MCTS lookahead, and causal mental simulation.
  </p>
  <iframe
    src="https://<your-app-name>.streamlit.app/?embed=true"
    frameborder="0"
    width="100%"
    height="900"
    style="border: 1px solid #E5E7EB; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.08);"
    allow="clipboard-write"
  ></iframe>
</section>
```

---

## 💻 Method 3: Self-Host Locally via Cloudflare Tunnel (100% Free)

If you prefer running the app directly on your local machine and sharing it publicly with anyone worldwide:

1. Launch the Streamlit app locally:
   ```bash
   streamlit run streamlit_app.py
   ```
   *(Running locally on `http://localhost:8501`)*

2. In another terminal tab, run Cloudflare's free quick tunnel (no account or domain required):
   ```bash
   cloudflared tunnel --url http://localhost:8501
   ```
3. Cloudflare gives you an instant, secure public URL: `https://<random-hash>.trycloudflare.com` that anyone on the web can use.

---

## 📓 Method 4: Google Colab Live Temporary Share

If you want to run directly from Google Colab using a free GPU instance:

1. Open `AGI_Cognitive_Agent_v3.ipynb` in Colab.
2. In a cell, run:
   ```python
   !pip install -q streamlit
   !npm install -g localtunnel
   import subprocess
   subprocess.Popen(["streamlit", "run", "streamlit_app.py", "--server.port", "8501"])
   !npx localtunnel --port 8501
   ```
3. Localtunnel will generate a public URL to test live.
