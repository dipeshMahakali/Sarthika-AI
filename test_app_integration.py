# -*- coding: utf-8 -*-
"""
End-to-End Integration Test for Sarthika 3.0 Web App & Modular Core
"""

import sys
from sarthika_core import (
    create_sarthika_expert,
    MockCognitiveEngine,
    run_level3_benchmark
)
from app import run_sarthika_pipeline, run_benchmark_audit

def test_full_pipeline_stream():
    print("🧪 Testing Sarthika Pipeline Stream...")
    generator = run_sarthika_pipeline(
        goal="Compute Euler Totient phi(120)",
        provider="Mock Simulator (Demo Mode)",
        api_key="",
        model_name="mock-model",
        tau_threshold=0.65,
        max_retries=2
    )

    steps_yielded = 0
    for subtasks_md, log_md, scorecard_md, winning_code, state_summary_md in generator:
        steps_yielded += 1

    print(f"✅ Pipeline streamed {steps_yielded} UI state updates successfully.")
    assert steps_yielded >= 5, "Expected multiple streaming events"

def test_benchmark_audit_runner():
    print("🧪 Testing Benchmark Audit Runner...")
    res_md = run_benchmark_audit()
    print("✅ Benchmark output formatted correctly:")
    print(res_md[:200] + "...")
    assert "LEVEL 3: EXPERT AGI READY" in res_md or "PASSED" in res_md

if __name__ == "__main__":
    test_full_pipeline_stream()
    test_benchmark_audit_runner()
    print("\n🎉 ALL INTEGRATION TESTS PASSED WITH ZERO ERRORS!")
