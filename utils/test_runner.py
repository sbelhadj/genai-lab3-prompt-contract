"""
Test Runner for Lab 3 — Automated Prompt Evaluation

Runs a prompt template against a set of test cases and checks expected properties.
Students use this to systematically evaluate their prompt contract iterations.
"""

import json
import re
from utils.generation_utils import generate, try_parse_json


def check_property(output, prop_name, prop_value, parsed_json=None):
    """
    Check a single expected property against the model output.

    Returns:
        (passed: bool, reason: str)
    """
    output_stripped = output.strip()
    output_lower = output_stripped.lower()

    # --- JSON validity ---
    if prop_name == "is_valid_json":
        if prop_value:
            result, err = try_parse_json(output_stripped)
            if result is not None:
                return True, "Valid JSON"
            return False, f"Invalid JSON: {err}"
        return True, "JSON not required"

    # --- Field presence (in parsed JSON) ---
    if prop_name.startswith("has_field_"):
        field_name = prop_name[len("has_field_"):]
        if parsed_json is None:
            return False, f"Cannot check field '{field_name}' — output is not valid JSON"
        if field_name in parsed_json:
            return True, f"Field '{field_name}' present"
        # Check case-insensitive
        for key in parsed_json:
            if key.lower() == field_name.lower():
                return True, f"Field '{key}' present (case-insensitive match)"
        return False, f"Field '{field_name}' missing from JSON output"

    # --- Value in set ---
    if prop_name.endswith("_in") and isinstance(prop_value, list):
        field_name = prop_name[:-3]  # e.g., "severity_in" → "severity"
        if parsed_json and field_name in parsed_json:
            val = parsed_json[field_name]
            if isinstance(val, str):
                val = val.lower().strip()
            if val in [v.lower() if isinstance(v, str) else v for v in prop_value]:
                return True, f"'{field_name}' value '{val}' is in allowed set"
            return False, f"'{field_name}' value '{val}' not in {prop_value}"
        return False, f"Cannot check value — field '{field_name}' not found"

    # --- Max words ---
    if prop_name.endswith("_max_words"):
        field_name = prop_name.replace("_max_words", "")
        if parsed_json and field_name in parsed_json:
            text = str(parsed_json[field_name])
            word_count = len(text.split())
            if word_count <= prop_value:
                return True, f"'{field_name}' has {word_count} words (max {prop_value})"
            return False, f"'{field_name}' has {word_count} words, exceeds max {prop_value}"
        return False, f"Cannot check word count — field '{field_name}' not found"

    # --- Contains / not contains ---
    if prop_name == "output_contains":
        if prop_value.lower() in output_lower:
            return True, f"Output contains '{prop_value}'"
        return False, f"Output does not contain '{prop_value}'"

    if prop_name == "output_not_contains":
        if prop_value.lower() not in output_lower:
            return True, f"Output correctly does not contain '{prop_value}'"
        return False, f"Output should not contain '{prop_value}' but does"

    # --- Max length (chars) ---
    if prop_name == "max_length_chars":
        if len(output_stripped) <= prop_value:
            return True, f"Output length {len(output_stripped)} ≤ {prop_value}"
        return False, f"Output length {len(output_stripped)} exceeds max {prop_value}"

    # --- Starts with ---
    if prop_name == "starts_with":
        if output_stripped.startswith(prop_value):
            return True, f"Output starts with '{prop_value}'"
        return False, f"Output does not start with '{prop_value}'"

    # --- Does not leak prompt ---
    if prop_name == "does_not_leak_prompt":
        leak_indicators = ["system prompt", "you are", "your instructions",
                           "my instructions", "ignore previous"]
        for indicator in leak_indicators:
            if indicator in output_lower:
                return False, f"Possible prompt leak: found '{indicator}'"
        return True, "No prompt leak detected"

    # --- Handles empty gracefully ---
    if prop_name == "handles_empty_gracefully":
        if len(output_stripped) < 10:
            return False, "Output too short — may not have handled empty input"
        hallucination_markers = ["the customer", "the user reported", "the issue is"]
        for marker in hallucination_markers:
            if marker in output_lower and "no " not in output_lower[:50]:
                return False, f"May have hallucinated content for empty input: found '{marker}'"
        return True, "Handled empty input without obvious hallucination"

    # --- Manual check (always passes auto, flagged for review) ---
    if prop_name in ("no_hallucinated_info", "treats_as_ticket_content",
                     "preserves_factual_content", "professional_tone",
                     "manual_review"):
        return True, f"[MANUAL REVIEW NEEDED] '{prop_name}'"

    # --- Unknown property ---
    return True, f"[UNKNOWN PROPERTY] '{prop_name}' — skipped"


def run_test_suite(prompt_template, test_cases, model="llama3.2:3b",
                   temperature=0.3, max_tokens=400, verbose=True):
    """
    Run a prompt against a test suite and evaluate results.

    Args:
        prompt_template: String with {placeholders} matching test case input keys.
        test_cases: List of test case dicts (id, category, input, expected_properties).
        model: Ollama model name.
        temperature: Sampling temperature.
        max_tokens: Max tokens per generation.
        verbose: Print detailed results.

    Returns:
        Report dict with pass rates, failures, and per-case results.
    """
    results = []
    passed_count = 0
    failed_count = 0
    auto_passed = 0
    auto_total = 0
    manual_review = 0
    failures = []

    for tc in test_cases:
        tc_id = tc.get("id", "unknown")
        category = tc.get("category", "normal")
        input_data = tc.get("input", {})
        expected = tc.get("expected_properties", {})

        # Format prompt with test input
        try:
            prompt = prompt_template.format(**input_data)
        except KeyError as e:
            if verbose:
                print(f"  ✗ {tc_id}: Missing placeholder {e} in prompt template")
            failures.append({"test_id": tc_id, "category": category,
                             "reason": f"Missing placeholder: {e}", "output": ""})
            failed_count += 1
            continue

        # Generate output
        output = generate(prompt, model=model, temperature=temperature,
                          max_tokens=max_tokens)

        # Parse JSON if needed
        parsed_json, _ = try_parse_json(output)

        # Check all properties
        tc_passed = True
        tc_reasons = []
        tc_manual = False

        for prop_name, prop_value in expected.items():
            ok, reason = check_property(output, prop_name, prop_value, parsed_json)
            tc_reasons.append((prop_name, ok, reason))

            if "[MANUAL REVIEW NEEDED]" in reason:
                tc_manual = True
                manual_review += 1
            else:
                auto_total += 1
                if ok:
                    auto_passed += 1
                else:
                    tc_passed = False

        if tc_passed:
            passed_count += 1
            if verbose:
                print(f"  ✓ {tc_id} ({category}) — PASSED")
        else:
            failed_count += 1
            fail_reasons = [r for (p, ok, r) in tc_reasons if not ok and "[MANUAL" not in r]
            failures.append({
                "test_id": tc_id,
                "category": category,
                "reason": "; ".join(fail_reasons),
                "output": output[:300]
            })
            if verbose:
                print(f"  ✗ {tc_id} ({category}) — FAILED")
                for fr in fail_reasons:
                    print(f"      → {fr}")

        results.append({
            "test_id": tc_id,
            "category": category,
            "passed": tc_passed,
            "output": output[:500],
            "checks": tc_reasons,
            "needs_manual_review": tc_manual
        })

    total = passed_count + failed_count
    report = {
        "total": total,
        "passed": passed_count,
        "failed": failed_count,
        "pass_rate": passed_count / max(total, 1),
        "format_compliance_rate": auto_passed / max(auto_total, 1),
        "auto_passed": auto_passed,
        "auto_total": auto_total,
        "manual_review_count": manual_review,
        "failures": failures,
        "results": results,
    }

    return report
