"""
Generation Utilities for Lab 3 — The Prompt Contract

Provides helpers for calling Ollama, comparing outputs, and loading fallback data.
"""

import requests
import json


def generate(prompt, model="llama3.2:3b", temperature=0.3, max_tokens=400, timeout=90):
    """Generate a completion using Ollama."""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False,
                  "options": {"temperature": temperature, "num_predict": max_tokens}},
            timeout=timeout)
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        return f"[Generation failed: {e}]"


def generate_n(prompt, n=5, **kwargs):
    """Generate n completions for the same prompt."""
    return [generate(prompt, **kwargs) for _ in range(n)]


def is_ollama_available():
    """Check if Ollama is reachable."""
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=5)
        return r.status_code == 200
    except Exception:
        return False


def load_precomputed(filepath="data/precomputed_outputs.json"):
    """Load pre-computed outputs as fallback."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠ Pre-computed file not found: {filepath}")
        return {}


def load_test_inputs(filepath="data/sample_tasks.json", task_id=None):
    """
    Load test inputs for a specific task.

    Args:
        filepath: Path to sample_tasks.json
        task_id: One of: "ticket_summarizer", "acceptance_criteria",
                 "field_extractor", "code_review", "meeting_notes", "email_rewriter"

    Returns:
        List of input dicts for the specified task.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        if task_id:
            return data.get("tasks", {}).get(task_id, {}).get("inputs", [])
        return data
    except FileNotFoundError:
        print(f"⚠ File not found: {filepath}")
        return []


def try_parse_json(text):
    """
    Attempt to parse JSON from model output.
    Handles common issues: markdown fences, trailing text.
    """
    text = text.strip()
    # Remove markdown code fences
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()

    # Try parsing
    try:
        return json.loads(text), None
    except json.JSONDecodeError as e:
        # Try finding JSON object within the text
        start = text.find("{")
        end = text.rfind("}") + 1
        if start >= 0 and end > start:
            try:
                return json.loads(text[start:end]), None
            except json.JSONDecodeError:
                pass
        return None, str(e)
