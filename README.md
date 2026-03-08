# Lab 3 — The Prompt Contract

**Generative AI & Prompt Engineering — A Mechanistic Approach**

Module 3: Instruction-Following & Alignment | Duration: 90 minutes

---

## Overview

In this lab, you'll learn to write prompts as **engineering contracts** — structured specifications with a clear objective, explicit constraints, a defined output format, and testable acceptance criteria. You'll write three versions of a prompt for a TaskFlow task (naive → improved → hardened), build a test suite, and measure improvement across iterations.

**Core principle:** *Instruction tuning makes the model responsive to instructions, but a vague instruction still produces vague output. The prompt contract is how you engineer reliability.*

---

## Quick Start

### Option A: GitHub Codespaces (Recommended)

1. Click **"Code"** → **"Codespaces"** → **"Create codespace on main"**
2. Wait for environment build (~3–5 minutes)
3. Open `lab3_prompt_contract.ipynb`

### Option B: Local Setup

```bash
git clone <your-repo-url>
cd genai-lab3-prompt-contract
pip install requests pytest jsonschema jupyter matplotlib numpy nbformat
ollama serve &
ollama pull llama3.2:3b
jupyter notebook
```

---

## Repository Structure

```
genai-lab3-prompt-contract/
├── .devcontainer/devcontainer.json
├── .github/workflows/autograding.yml
├── lab3_prompt_contract.ipynb          # ← YOUR MAIN WORKSPACE
├── utils/
│   ├── __init__.py
│   ├── generation_utils.py             # generate(), compare_outputs()
│   └── test_runner.py                  # run_test_suite() — automated prompt evaluation
├── data/
│   ├── sample_tasks.json               # TaskFlow-themed test inputs (6 tasks)
│   └── precomputed_outputs.json        # Fallback if Ollama unavailable
├── tests/
│   ├── __init__.py
│   ├── test_deliverables.py            # Auto-graded: checks deliverable files exist
│   └── test_suite_validation.py        # Auto-graded: validates tests.json structure
├── prompt.md                           # ← YOUR DELIVERABLE: 3 prompt versions + justifications
├── tests.json                          # ← YOUR DELIVERABLE: 10+ test cases
├── README.md
└── .gitignore
```

---

## What to Do

1. Open `lab3_prompt_contract.ipynb`
2. **Choose a task** from `data/sample_tasks.json` (or propose your own)
3. Write **V1** (naive prompt) → run on 5 inputs → observe failures
4. Write **V2** (improved: objective + constraints + format) → compare
5. Write **V3** (hardened: full contract + few-shot example) → compare
6. Build **test suite** (10+ cases) in `tests.json`
7. Run test suite against V3 and analyze results
8. Write final prompt versions + justifications to `prompt.md`

---

## Deliverables

| # | What | Where |
|---|------|-------|
| 1 | Completed notebook | `lab3_prompt_contract.ipynb` |
| 2 | 3 prompt versions + mechanistic justifications | `prompt.md` |
| 3 | Test suite with 10+ cases | `tests.json` |
| 4 | Test results analysis | In notebook |
| 5 | Cross-version comparison table | In notebook |

---

## Submitting

```bash
git add -A
git commit -m "Lab 3 complete"
git push
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Ollama unavailable | Use `data/precomputed_outputs.json` — fallback cells in notebook |
| JSON parsing fails on model output | Wrap in try/except; this is expected — it's why you need format constraints |
| Test runner errors | Check `tests.json` follows the schema (see examples in notebook) |
| 0% pass rate | Normal for V1. That's the point — iterate toward V3. |

---

*Lab 3 of 8 — DevAssist / TaskFlow Lab Series*
