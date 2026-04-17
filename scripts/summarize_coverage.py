"""Summarize req_coverage.json — example post-processing step.

Shows how to:
- Aggregate test cases per requirement (n:m → req → [test cases])
- Identify failing tests
- Build a mapping ready to push into a custom field on your issue tracker

The actual API call is stubbed out. In a real setup, use an existing
client library for your tracker.
"""
import json
import sys
from collections import defaultdict
from pathlib import Path


def build_requirement_coverage(coverage_path: Path) -> dict[str, list[str]]:
    """Return {requirement_id: [testcase_ids]} from passed tests only."""
    data = json.loads(coverage_path.read_text())
    mapping: dict[str, set[str]] = defaultdict(set)
    for entry in data:
        if not entry["passed"]:
            continue
        for req in entry["requirements"]:
            for tc in entry["testcases"]:
                mapping[req].add(tc)
    return {req: sorted(tcs) for req, tcs in mapping.items()}


def main() -> int:
    coverage = Path("req_coverage.json")
    if not coverage.exists():
        print("No req_coverage.json found — run `pytest` first.")
        return 1

    mapping = build_requirement_coverage(coverage)

    print("Requirement → Test cases (passed only):")
    for req, tcs in sorted(mapping.items()):
        print(f"  {req}: {', '.join(tcs)}")

    failing = [e for e in json.loads(coverage.read_text()) if not e["passed"]]
    if failing:
        print("\nFailing tests:")
        for entry in failing:
            reqs = ", ".join(entry["requirements"]) or "—"
            tcs = ", ".join(entry["testcases"]) or "—"
            print(f"  {entry['test']}  [req: {reqs}] [tc: {tcs}]")

    # To push into your issue tracker (pseudocode):
    #
    #     client = IssueTrackerClient(server=..., token=...)
    #     for req_id, test_cases in mapping.items():
    #         client.update_issue(req_id, fields={
    #             "custom_field_testcases": test_cases,
    #         })

    return 0


if __name__ == "__main__":
    sys.exit(main())
