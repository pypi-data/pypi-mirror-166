"""
    Dummy conftest.py for taccjm.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""

import pytest


def pytest_addoption(parser):
    parser.addoption("--mfa", action="store",
            default="012345", help="MFA token. Must be provided")

@pytest.fixture
def mfa(request):
    return request.config.getoption("--mfa")
