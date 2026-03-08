"""
Auto-grading tests for Lab 3 — Test Suite Validation

Verifies that the student's tests.json is well-formed and has adequate coverage.
"""

import pytest
import json
import os

TESTS_JSON = os.path.join(os.path.dirname(__file__), "..", "tests.json")


def load_test_suite():
    if not os.path.exists(TESTS_JSON):
        pytest.skip("tests.json not found")
    with open(TESTS_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


class TestSuiteStructure:

    def test_is_valid_json(self):
        """tests.json must be valid JSON."""
        suite = load_test_suite()
        assert isinstance(suite, list), "tests.json should be a JSON array"

    def test_minimum_10_cases(self):
        """Must have at least 10 test cases."""
        suite = load_test_suite()
        assert len(suite) >= 10, \
            f"Test suite has {len(suite)} cases, minimum is 10"

    def test_each_case_has_required_fields(self):
        """Every test case must have id, category, input, expected_properties."""
        suite = load_test_suite()
        for i, tc in enumerate(suite):
            assert "id" in tc, f"Test case {i} missing 'id'"
            assert "category" in tc, f"Test case {i} ('{tc.get('id', '?')}') missing 'category'"
            assert "input" in tc, f"Test case {i} ('{tc.get('id', '?')}') missing 'input'"
            assert "expected_properties" in tc, \
                f"Test case {i} ('{tc.get('id', '?')}') missing 'expected_properties'"

    def test_categories_valid(self):
        """Categories must be one of: normal, edge, adversarial."""
        suite = load_test_suite()
        valid = {"normal", "edge", "adversarial"}
        for tc in suite:
            cat = tc.get("category", "")
            assert cat in valid, \
                f"Test '{tc.get('id', '?')}' has invalid category '{cat}'. Use: {valid}"

    def test_ids_unique(self):
        """All test case IDs must be unique."""
        suite = load_test_suite()
        ids = [tc.get("id") for tc in suite]
        duplicates = [x for x in ids if ids.count(x) > 1]
        assert len(set(duplicates)) == 0, \
            f"Duplicate test IDs found: {set(duplicates)}"


class TestSuiteCoverage:

    def test_has_normal_cases(self):
        """At least 4 normal cases required."""
        suite = load_test_suite()
        normal = [tc for tc in suite if tc.get("category") == "normal"]
        assert len(normal) >= 4, \
            f"Only {len(normal)} normal cases. Need at least 4."

    def test_has_edge_cases(self):
        """At least 3 edge cases required."""
        suite = load_test_suite()
        edge = [tc for tc in suite if tc.get("category") == "edge"]
        assert len(edge) >= 3, \
            f"Only {len(edge)} edge cases. Need at least 3."

    def test_has_adversarial_cases(self):
        """At least 3 adversarial cases required."""
        suite = load_test_suite()
        adv = [tc for tc in suite if tc.get("category") == "adversarial"]
        assert len(adv) >= 3, \
            f"Only {len(adv)} adversarial cases. Need at least 3."

    def test_expected_properties_non_empty(self):
        """Each test case must check at least one property."""
        suite = load_test_suite()
        for tc in suite:
            props = tc.get("expected_properties", {})
            assert len(props) >= 1, \
                f"Test '{tc.get('id', '?')}' has no expected_properties"
