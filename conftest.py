"""Collect requirement coverage from pytest markers.

For every test with @pytest.mark.requirement(...) and/or @pytest.mark.testcase(...),
this hook records: which requirements were covered, which test cases ran, and
the pass/fail result. Results are written to req_coverage.json at session end.
"""
import json
from pathlib import Path

COVERAGE_FILE = Path("req_coverage.json")
_results: list[dict] = []


def pytest_runtest_makereport(item, call):
    if call.when != "call":
        return

    req_ids: list[str] = []
    for marker in item.iter_markers("requirement"):
        req_ids.extend(marker.args)

    tc_ids: list[str] = []
    for marker in item.iter_markers("testcase"):
        tc_ids.extend(marker.args)

    if not req_ids and not tc_ids:
        return

    _results.append({
        "test": item.nodeid,
        "requirements": req_ids,
        "testcases": tc_ids,
        "passed": call.excinfo is None,
    })


def pytest_sessionfinish():
    if _results:
        COVERAGE_FILE.write_text(json.dumps(_results, indent=2))
        print(f"\nRequirement coverage written to {COVERAGE_FILE}")
