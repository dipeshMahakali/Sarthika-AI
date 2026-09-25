# -*- coding: utf-8 -*-
"""
Sarthika Cognitive Engine Abstraction
Supports:
1. Free High-Speed Serverless API (Groq: Qwen 2.5 32B, Llama 3.3 70B, etc.)
2. OpenAI-compatible endpoints (OpenRouter Free Tier, Sambanova, Ollama)
3. Local Hugging Face Transformers (T4 GPU / CPU)
4. Offline Mock Engine (for architectural unit tests)
"""

import os
import json
import urllib.request
import urllib.error
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any

class BaseCognitiveEngine(ABC):
    @abstractmethod
    def generate(self, prompt: str, system_prompt: str = "", max_new_tokens: int = 1024, temperature: float = 0.6) -> str:
        pass


class GroqEngine(BaseCognitiveEngine):
    """
    High-Speed Free Inference using Groq Cloud API.
    Zero-dependency implementation using standard library urllib, with optional groq SDK fallback.
    Free tier: 30 RPM, 14,400 requests/day, ~300-500 tokens/sec.
    """
    def __init__(self, api_key: Optional[str] = None, model: str = "llama-3.1-8b-instant"):
        self.api_key = api_key or os.getenv("GROQ_API_KEY", "")
        self.model = model or "llama-3.1-8b-instant"
        self.endpoint = "https://api.groq.com/openai/v1/chat/completions"

    @staticmethod
    def get_available_models(api_key: str) -> List[str]:
        """Fetches live available models from Groq API."""
        default_models = [
            "llama-3.1-8b-instant",
            "llama-3.3-70b-specdec",
            "llama-3.1-70b-versatile",
            "mixtral-8x7b-32768",
            "gemma2-9b-it",
            "deepseek-r1-distill-llama-70b"
        ]
        if not api_key:
            return default_models
        req = urllib.request.Request(
            "https://api.groq.com/openai/v1/models",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                models = [m["id"] for m in data.get("data", []) if m.get("active", True)]
                return models if models else default_models
        except Exception:
            return default_models

    def generate(self, prompt: str, system_prompt: str = "", max_new_tokens: int = 1024, temperature: float = 0.6) -> str:
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is not configured. Please supply an API key or use MockEngine.")

        import time
        import re

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_new_tokens,
            "temperature": max(0.0, min(1.0, temperature)),
        }

        req = urllib.request.Request(
            self.endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "Sarthika-Cognitive-Agent/3.0"
            }
        )

        max_attempts = 4
        for attempt in range(max_attempts):
            try:
                with urllib.request.urlopen(req, timeout=35) as response:
                    result = json.loads(response.read().decode("utf-8"))
                    return result["choices"][0]["message"]["content"]
            except urllib.error.HTTPError as e:
                err_body = e.read().decode("utf-8", errors="replace")
                if e.code == 429 and attempt < max_attempts - 1:
                    wait_sec = 6.0 * (attempt + 1)
                    match = re.search(r"try again in ([\d\.]+)s", err_body, re.IGNORECASE)
                    if match:
                        wait_sec = float(match.group(1)) + 1.0
                    time.sleep(wait_sec)
                    continue

                if "model_not_found" in err_body:
                    raise RuntimeError(
                        f"Groq Model '{self.model}' not found on your account. "
                        "Please select 'llama-3.1-8b-instant', 'llama-3.1-70b-versatile', or 'mixtral-8x7b-32768'."
                    )
                raise RuntimeError(f"Groq API Error {e.code}: {err_body}")
            except Exception as e:
                if attempt < max_attempts - 1:
                    time.sleep(2.0)
                    continue
                raise RuntimeError(f"Inference Connection Error: {str(e)}")


class OpenAIEngine(BaseCognitiveEngine):
    """
    Universal OpenAI-Compatible Engine (OpenRouter, Sambanova, Ollama, etc.)
    """
    def __init__(self, api_key: str, base_url: str = "https://openrouter.ai/api/v1", model: str = "meta-llama/llama-3.3-70b-instruct:free"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/") + "/chat/completions"
        self.model = model

    def generate(self, prompt: str, system_prompt: str = "", max_new_tokens: int = 1024, temperature: float = 0.6) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_new_tokens,
            "temperature": temperature,
        }

        req = urllib.request.Request(
            self.base_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "Sarthika-Cognitive-Agent/3.0"
            }
        )

        with urllib.request.urlopen(req, timeout=35) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"]


class MockCognitiveEngine(BaseCognitiveEngine):
    """
    Deterministic Simulator for zero-latency testing, CI/CD, and demo fallback.
    """
    def generate(self, prompt: str, system_prompt: str = "", max_new_tokens: int = 1024, temperature: float = 0.6) -> str:
        if "Metacognitive Task Planner" in system_prompt:
            return "1. Compute initial mathematical foundation.\n2. Execute core algorithmic computation.\n3. Validate results and verify formal invariants."
        elif "System 1" in system_prompt:
            return '''--- CANDIDATE A ---
```python
def compute_solution():
    # Candidate A: Optimized algorithmic approach
    import math
    results = [x**2 for x in range(1, 11)]
    return {"sum": sum(results), "items": results}

ans = compute_solution()
print(f"Verified Computation: {ans}")
```

--- CANDIDATE B ---
```python
def compute_solution_b():
    # Candidate B: Functional approach
    total = sum(map(lambda x: x*x, range(1, 11)))
    return total

print("Result B:", compute_solution_b())
```

--- CANDIDATE C ---
```python
# Candidate C: Closed form formula n(n+1)(2n+1)/6
n = 10
formula_ans = n * (n + 1) * (2 * n + 1) // 6
print(f"Closed Form Result: {formula_ans}")
```'''
        elif "System 2" in system_prompt:
            return "SCORE: 0.95\nJUSTIFICATION: Execution verified with valid mathematical output."
        return "Standard Engine Output."


class LocalTransformersEngine(BaseCognitiveEngine):
    """
    Local Transformers Engine (For Google Colab T4 GPU or local RTX workstation).
    """
    def __init__(self, model_id: str = "Qwen/Qwen2.5-7B-Instruct"):
        import torch
        from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        if torch.cuda.is_available():
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16,
                bnb_4bit_use_double_quant=True,
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                model_id,
                quantization_config=bnb_config,
                device_map="auto",
                torch_dtype=torch.bfloat16,
            )
        else:
            self.model = AutoModelForCausalLM.from_pretrained(
                model_id,
                torch_dtype=torch.float32,
                device_map="cpu",
                low_cpu_mem_usage=True
            )

    def generate(self, prompt: str, system_prompt: str = "", max_new_tokens: int = 1024, temperature: float = 0.6) -> str:
        import torch
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)

        gen_kwargs = {
            "max_new_tokens": max_new_tokens,
            "pad_token_id": self.tokenizer.eos_token_id,
        }
        if temperature > 0:
            gen_kwargs["do_sample"] = True
            gen_kwargs["temperature"] = temperature
        else:
            gen_kwargs["do_sample"] = False

        generated_ids = self.model.generate(**model_inputs, **gen_kwargs)
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        return self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
