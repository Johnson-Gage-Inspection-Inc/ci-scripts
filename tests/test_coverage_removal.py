"""Test to validate that coverage requirements have been removed."""

import subprocess
import sys
from pathlib import Path


def test_coverage_requirements_removed():
    """Test that pytest no longer fails due to low coverage."""
    # This test verifies that coverage thresholds are removed
    # We expect tests to pass regardless of coverage percentage
    
    project_root = Path(__file__).parent.parent
    
    # Run pytest with coverage but expect it to pass even with low coverage
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests/test_coverage_removal.py::test_dummy_low_coverage",
            "--cov=tests.test_coverage_removal",
            "--cov-report=term-missing",
            "-v"
        ],
        cwd=project_root,
        capture_output=True,
        text=True,
    )
    
    # Test should pass regardless of coverage percentage
    assert result.returncode == 0, f"Test failed: {result.stdout} {result.stderr}"
    
    # Coverage output should be present but not cause failure
    assert "coverage:" in result.stdout.lower()


def test_dummy_low_coverage():
    """A simple test that will have very low coverage in its module."""
    # This function ensures very low coverage in this test file
    def uncovered_function_1():
        return "not tested"
    
    def uncovered_function_2():
        return "also not tested"
    
    def uncovered_function_3():
        return "still not tested"
    
    # Only test one simple thing to keep coverage low
    assert True