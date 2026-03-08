"""
Auto-grading tests for Lab 3 — Deliverable Structure

Verifies that required deliverable files exist and contain student work.
"""

import pytest
import json
import os

BASE = os.path.join(os.path.dirname(__file__), "..")
NOTEBOOK = os.path.join(BASE, "lab3_prompt_contract.ipynb")
PROMPT_MD = os.path.join(BASE, "prompt.md")
TESTS_JSON = os.path.join(BASE, "tests.json")


class TestFilesExist:

    def test_notebook_exists(self):
        assert os.path.exists(NOTEBOOK), "lab3_prompt_contract.ipynb not found"

    def test_prompt_md_exists(self):
        assert os.path.exists(PROMPT_MD), "prompt.md not found"

    def test_tests_json_exists(self):
        assert os.path.exists(TESTS_JSON), "tests.json not found"


class TestPromptMd:

    def test_prompt_md_not_template(self):
        """prompt.md should contain student work, not just the template."""
        with open(PROMPT_MD, "r", encoding="utf-8") as f:
            content = f.read()
        # Count remaining TODO markers
        todo_count = content.count("TODO:")
        assert todo_count <= 3, \
            f"prompt.md still has {todo_count} TODO markers. Please fill in your work."

    def test_has_three_versions(self):
        """Should contain V1, V2, and V3."""
        with open(PROMPT_MD, "r", encoding="utf-8") as f:
            content = f.read().lower()
        assert "version 1" in content or "v1" in content or "naive" in content, \
            "prompt.md missing Version 1 / Naive prompt"
        assert "version 2" in content or "v2" in content or "improved" in content, \
            "prompt.md missing Version 2 / Improved prompt"
        assert "version 3" in content or "v3" in content or "hardened" in content, \
            "prompt.md missing Version 3 / Hardened prompt"

    def test_has_mechanistic_justification(self):
        """Should reference at least one mechanistic concept."""
        with open(PROMPT_MD, "r", encoding="utf-8") as f:
            content = f.read().lower()
        mechanism_terms = ["attention", "token", "probability", "distribution",
                           "instruction tuning", "rlhf", "alignment", "context window",
                           "softmax", "pattern matching"]
        found = [t for t in mechanism_terms if t in content]
        assert len(found) >= 2, \
            f"prompt.md should reference mechanistic concepts. Found only: {found}"


class TestNotebook:

    def test_notebook_valid(self):
        if not os.path.exists(NOTEBOOK):
            pytest.skip("Notebook not found")
        with open(NOTEBOOK, "r", encoding="utf-8") as f:
            nb = json.load(f)
        assert "cells" in nb
        assert len(nb["cells"]) >= 15, \
            f"Notebook has only {len(nb['cells'])} cells"

    def test_notebook_executed(self):
        if not os.path.exists(NOTEBOOK):
            pytest.skip("Notebook not found")
        with open(NOTEBOOK, "r", encoding="utf-8") as f:
            nb = json.load(f)
        executed = sum(1 for c in nb["cells"]
                       if c.get("cell_type") == "code" and c.get("outputs"))
        assert executed >= 5, \
            f"Only {executed} code cells have outputs. Run notebook before submitting."
