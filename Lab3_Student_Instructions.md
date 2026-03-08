# Lab 3 — The Prompt Contract

## Generative AI & Prompt Engineering — Practical Lab Series

**Module:** 3 — Instruction-Following & Alignment
**Duration:** 90 minutes
**Mode:** Pair programming (driver/navigator, switch at 45 min)
**Fil Rouge:** DevAssist — AI-Powered Developer Documentation Assistant for TaskFlow

---

## 1. Context and Scenario

The TaskFlow team wants DevAssist to handle structured tasks: summarize support tickets, extract fields from job postings, generate acceptance criteria from user stories, and more. But early experiments show that naive prompts produce inconsistent, unparseable outputs. One run gives JSON, the next gives bullets, the next gives a paragraph with extra commentary.

Today you'll learn why this happens mechanistically — instruction tuning makes the model *responsive* to instructions, but *precision* requires engineering. You'll write prompts as **engineering contracts** and build **test suites** that measure reliability across iterations.

---

## 2. Learning Objectives

| ID | Objective | Assessment |
|----|-----------|------------|
| L3.1 | Organize a prompt as a contract with 4 components (objective, constraints, format, evaluation criteria) | prompt.md with all 3 versions |
| L3.2 | Iterate from naive to hardened through systematic failure analysis | V1→V2→V3 progression with justifications |
| L3.3 | Design a test suite with normal, edge, and adversarial cases | tests.json with 10+ cases |
| L3.4 | Connect prompt improvements to alignment mechanisms | Mechanistic justifications in prompt.md |
| L3.5 | Explain sycophancy/hallucination as RLHF failure modes and mitigate via prompt design | Written analysis in notebook |

---

## 3. Lab Structure (90 minutes)

| Phase | Time | Activity |
|-------|------|----------|
| Setup + task selection | 5 min | Choose task, verify environment |
| V1: Naive prompt | 15 min | Write, run on 5 inputs, observe failures |
| V2: Improved prompt | 15 min | Add objective + constraints + format |
| V3: Hardened prompt | 15 min | Full contract + few-shot example |
| Cross-version comparison | 10 min | Fill comparison table |
| Test suite construction | 20 min | Build 10+ test cases in tests.json |
| Run tests + wrap-up | 10 min | Evaluate V3, analyze results |

---

## 4. The Prompt Contract Framework

Every V3 (hardened) prompt must include these 4 components:

| Component | Purpose | Example |
|-----------|---------|---------|
| **Objective** | What should the model do? | "Classify the support ticket into a category and severity level" |
| **Constraints** | What to avoid, boundaries | "Do not infer information not in the ticket. If empty, return default." |
| **Output Format** | Exact structure expected | "Return JSON: {issue_category, severity, synopsis}" |
| **Evaluation Criteria** | How to verify correctness | "severity must be one of: low, medium, high" |

Plus at least **one few-shot example** showing the expected input→output mapping.

---

## 5. Available Tasks

Choose one from `data/sample_tasks.json`:

| # | Task | Output Structure |
|---|------|-----------------|
| 1 | **Ticket Summarizer** | `{issue_category, severity, synopsis}` |
| 2 | **Acceptance Criteria Generator** | Given/When/Then format |
| 3 | **Structured Field Extractor** | `{company, role, location, years_experience, top_3_skills}` |
| 4 | **Code Review Commenter** | `{issue_type, severity, explanation, suggested_fix}` |
| 5 | **Meeting Notes Formatter** | `{date, attendees, decisions, action_items}` |
| 6 | **Email Tone Rewriter** | Professional rewrite preserving facts |

Each task comes with 7 pre-built inputs: 5 normal, 1 edge case (empty/ambiguous), 1 adversarial (prompt injection attempt).

---

## 6. Test Suite Requirements

Your `tests.json` must contain **at least 10 test cases**:

| Category | Minimum | Description |
|----------|---------|-------------|
| Normal | 4 | Standard inputs representing typical use |
| Edge | 3 | Empty fields, very long text, ambiguous input, no relevant content |
| Adversarial | 3 | Prompt injection, misleading content, instruction-like text in data |

Each test case checks **expected properties** (not exact output matching):
- `is_valid_json`: Output parses as valid JSON
- `has_field_X`: JSON contains field named X
- `X_in`: Field X's value is within an allowed set
- `X_max_words`: Field X has at most N words
- `does_not_leak_prompt`: Output doesn't reveal system instructions
- `handles_empty_gracefully`: Doesn't hallucinate content for empty input

---

## 7. Deliverables

| # | Deliverable | Format |
|---|-------------|--------|
| 1 | Completed notebook | `lab3_prompt_contract.ipynb` |
| 2 | Three prompt versions + mechanistic justifications | `prompt.md` |
| 3 | Test suite with 10+ cases | `tests.json` |
| 4 | Cross-version comparison table | In notebook + prompt.md |
| 5 | Test results analysis | In notebook |

---

## 8. Evaluation Criteria

| Criterion | Weight | What We Look For |
|-----------|--------|------------------|
| **Mechanistic understanding** | 25% | Justifications reference instruction tuning, attention, token distributions |
| **Prompt quality** | 25% | Clear V1→V2→V3 progression; V3 has all 4 contract components + example |
| **Evaluation & verification** | 20% | Test suite has 10+ cases across 3 categories; pass rates analyzed |
| **Software engineering** | 20% | tests.json well-structured; comparison table complete; notebook runs |
| **Responsibility & security** | 10% | Adversarial test cases present; prompt injection handling addressed |

---

## 9. Connection to Next Lab

In **Lab 4 — Technique Toolbox**, you'll expand the contract framework with advanced techniques: few-shot prompting (selecting and ordering examples), chain-of-thought (generating intermediate reasoning tokens), self-consistency (sampling + voting), and format constraints (JSON schema validation). Every technique is grounded in the mechanisms from Modules 1–3.

---

*Lab 3 of 8 — DevAssist / TaskFlow Lab Series*
*Previous: Lab 2 — Attention in Action*
*Next: Lab 4 — Technique Toolbox*
