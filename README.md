# pytest-req-traceability

Minimal working example of marker-based requirement traceability in pytest.

Shows how to link pytest tests to external requirement IDs (e.g. `REQ-101`)
and external test case IDs (e.g. `TC-001`) using standard pytest markers,
then export a JSON coverage report at the end of a test run.

## Core idea

```python
@pytest.mark.requirement("REQ-101")
@pytest.mark.testcase("TC-001")
def test_login_with_valid_credentials():
    assert True
```

A conftest hook collects these markers during the test run and writes a
`req_coverage.json` file mapping each test to its requirements and test cases,
with pass/fail status. A small downstream script can then push the mapping
into a requirements tracker (custom field in your issue tracker, Polarion,
StrictDoc, etc.).

## Run it

```bash
pip install pytest
pytest
cat req_coverage.json
python scripts/summarize_coverage.py
```

Expected `req_coverage.json`:

```json
[
  {
    "test": "tests/test_auth.py::test_login_with_valid_credentials",
    "requirements": ["REQ-101"],
    "testcases": ["TC-001"],
    "passed": true
  },
  ...
]
```

## How it works

Three files do the work:

| File | Purpose |
|------|---------|
| `pyproject.toml` | Registers the two custom markers so pytest doesn't warn |
| `conftest.py` | Hooks `pytest_runtest_makereport` + `pytest_sessionfinish` to collect markers and dump JSON |
| `tests/test_*.py` | Annotate tests with `@pytest.mark.requirement(...)` and `@pytest.mark.testcase(...)` |

Both markers accept **multiple IDs** so one test can cover several requirements
and one test case ID can be attached to a test covering multiple requirements
(n:m mapping).

```python
@pytest.mark.requirement("REQ-101", "REQ-102")
@pytest.mark.testcase("TC-002")
def test_multiple_requirements():
    ...
```

## Integration into an existing project

1. Copy the markers block from `pyproject.toml` into your project's
   `pyproject.toml` (or `pytest.ini`).
2. Merge the hook from `conftest.py` into your existing `conftest.py` — it's
   additive, does not conflict with other hooks.
3. Start annotating tests gradually. Unmarked tests are silently ignored.

The hook does not change test discovery, collection, or execution. It's pure
metadata extraction.

## Pushing coverage to your issue tracker

`scripts/summarize_coverage.py` shows the shape of the downstream step:
aggregate `req_coverage.json` into `{requirement: [test_cases]}` and write it
into a custom field on your issue tracker (e.g. a Labels field). The actual
API call is stubbed — use any client library.

## Why markers instead of test naming conventions

Naming tests like `test_tc_001_login_valid` encodes the test case ID in the
function name. This works, but:

- Renaming a test ID means renaming functions (noisy diffs).
- Parsing requires regex; markers use the standard pytest API.
- Only one ID per test is practical in a name.

Markers keep function names readable, let you attach multiple IDs, and are
trivial to consume from the hook.

## License

MIT
