"""Example tests demonstrating requirement traceability markers.

Each test uses two markers:
- @pytest.mark.requirement(...) — which requirement(s) this test covers
- @pytest.mark.testcase(...)    — the external test case ID

Multiple IDs per marker are supported (n:m mapping).
"""
import pytest


@pytest.mark.requirement("REQ-101")
@pytest.mark.testcase("TC-001")
def test_login_with_valid_credentials():
    """User can log in with correct username and password."""
    assert True


@pytest.mark.requirement("REQ-101", "REQ-102")
@pytest.mark.testcase("TC-002")
def test_login_rejects_invalid_password():
    """Login fails for wrong password (REQ-101) and is rate-limited (REQ-102).

    Covers two requirements with one test case.
    """
    assert True


@pytest.mark.requirement("REQ-103")
@pytest.mark.testcase("TC-003")
def test_logout_clears_session():
    """Logging out invalidates the session token."""
    assert True


@pytest.mark.requirement("REQ-104")
@pytest.mark.testcase("TC-004")
def test_failing_example():
    """Demonstrates a failing test — appears in coverage with passed=false."""
    assert 1 == 2


def test_unmarked_example():
    """Tests without markers are ignored by the coverage hook."""
    assert True
