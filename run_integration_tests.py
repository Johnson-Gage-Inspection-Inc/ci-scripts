#!/usr/bin/env python3
"""
Manual integration test runner for xl-test repository.

This script allows you to manually run integration tests that create
Pull Requests in the xl-test repository to verify CI scripts work end-to-end.

Usage:
    python run_integration_tests.py

Requirements:
    - GITHUB_TOKEN environment variable with repo permissions
    - Access to Johnson-Gage-Inspection-Inc/xl-test repository
"""

import os
import subprocess
import sys
from pathlib import Path


def check_prerequisites():
    """Check that prerequisites are met."""
    # Check for GitHub token
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("❌ GITHUB_TOKEN environment variable is required")
        print(
            "   Please set it to a GitHub personal access token with 'repo' permissions"
        )
        return False

    # Check for requests library
    try:
        import requests  # noqa: F401
    except ImportError:
        print("❌ 'requests' library is required")
        print("   Install with: pip install requests")
        return False

    print("✅ Prerequisites check passed")
    return True


def run_integration_tests():
    """Run the integration tests."""
    if not check_prerequisites():
        return False

    print("\n🚀 Running integration tests against xl-test repository...")
    print("   This will create test branches and Pull Requests")
    print("   All test resources will be cleaned up automatically\n")

    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    # Run integration tests
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "tests/test_integration_xl_test.py",
        "-m",
        "integration",
        "-v",
        "--tb=short",
    ]

    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode == 0
    except KeyboardInterrupt:
        print("\n⚠️  Integration tests interrupted by user")
        print("   Test resources may need manual cleanup")
        return False


def main():
    """Main entry point."""
    print("🧪 Integration Test Runner for CI Scripts")
    print("=" * 50)

    if not run_integration_tests():
        print("\n❌ Integration tests failed or were interrupted")
        sys.exit(1)

    print("\n✅ Integration tests completed successfully!")
    print("   CI scripts are working properly with xl-test repository")


if __name__ == "__main__":
    main()
