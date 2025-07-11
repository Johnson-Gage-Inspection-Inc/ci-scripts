"""Integration tests against the xl-test repository.

This module contains integration tests that create actual Pull Requests
in the xl-test repository to verify that the CI scripts work end-to-end
in a real GitHub Actions environment.

Tests follow this approach:
1. Check out a new branch in xl-test
2. Update Book1.xltx using openpyxl (either valid changes or broken refs)
3. Commit and push changes
4. Create a pull request
5. Assert that the checks pass/fail as expected
6. Clean up (merge valid PRs, close broken ones)
"""

import base64
import os
import sys
import time
from datetime import datetime
from typing import Dict, List

import pytest
import requests
from openpyxl import Workbook


class GitHubIntegrationError(Exception):
    """Custom exception for GitHub integration test failures."""

    pass


class XLTestIntegration:
    """Helper class for integration testing with xl-test repository."""

    def __init__(self):
        self.repo_owner = "Johnson-Gage-Inspection-Inc"
        self.repo_name = "xl-test"
        self.api_base = "https://api.github.com"
        self.token = os.environ.get("GITHUB_TOKEN")

        if not self.token:
            raise GitHubIntegrationError(
                "GITHUB_TOKEN environment variable is required for integration tests"
            )

    @property
    def headers(self) -> Dict[str, str]:
        """HTTP headers for GitHub API requests."""
        return {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "ci-scripts-integration-test",
        }

    def get_file_content(self, file_path: str, branch: str = "main") -> Dict:
        """Get the content and metadata of a file from the repository."""
        url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/contents/{file_path}"
        params = {"ref": branch}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def create_test_branch(self, branch_name: str, base_branch: str = "main") -> str:
        """Create a test branch in the xl-test repository."""
        # Get the SHA of the base branch
        url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/git/refs/heads/{base_branch}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        base_sha = response.json()["object"]["sha"]

        # Create new branch
        url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/git/refs"
        data = {"ref": f"refs/heads/{branch_name}", "sha": base_sha}
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()

        return str(base_sha)

    def create_valid_excel_file(self) -> bytes:
        """Create a valid Excel file with proper structure."""
        wb = Workbook()
        ws = wb.active
        ws.title = "Sheet1"

        # Add some valid data
        ws["A1"] = "Test Data"
        ws["B1"] = "Value"
        ws["A2"] = "Item 1"
        ws["B2"] = 100
        ws["A3"] = "Item 2"
        ws["B3"] = 200

        # Add a valid formula (no #REF! errors)
        ws["C2"] = "=B2*2"
        ws["C3"] = "=B3*2"
        ws["C4"] = "=SUM(C2:C3)"

        # Save to bytes
        from io import BytesIO

        buffer = BytesIO()
        wb.save(buffer)
        return buffer.getvalue()

    def create_broken_excel_file(self) -> bytes:
        """Create an Excel file with #REF! errors."""
        wb = Workbook()
        ws = wb.active
        ws.title = "Sheet1"

        # Add some data
        ws["A1"] = "Test Data"
        ws["B1"] = "Value"
        ws["A2"] = "Item 1"
        ws["B2"] = 100

        # Add formulas that will create #REF! errors
        # These formulas reference cells that don't exist or will be deleted
        ws["C2"] = "=ZZ99999"  # Invalid cell reference
        ws["C3"] = "=#REF!"  # Direct #REF! error
        ws["C4"] = "=SUM(#REF!:C3)"  # Formula with #REF!

        # Save to bytes
        from io import BytesIO

        buffer = BytesIO()
        wb.save(buffer)
        return buffer.getvalue()

    def update_file_in_repo(
        self, file_path: str, content: bytes, branch_name: str, message: str
    ):
        """Update a file in the repository."""
        # Get current file to get its SHA
        try:
            file_info = self.get_file_content(file_path, branch_name)
            current_sha = file_info["sha"]
        except requests.exceptions.HTTPError:
            # File doesn't exist, so no SHA needed
            current_sha = None

        # Encode content to base64
        content_b64 = base64.b64encode(content).decode("utf-8")

        # Update file
        url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/contents/{file_path}"
        data = {"message": message, "content": content_b64, "branch": branch_name}
        if current_sha:
            data["sha"] = current_sha

        response = requests.put(url, json=data, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def create_pull_request(
        self, branch_name: str, title: str, body: str, base_branch: str = "main"
    ) -> int:
        """Create a pull request."""
        url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/pulls"
        data = {"title": title, "body": body, "head": branch_name, "base": base_branch}
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()

        return int(response.json()["number"])

    def get_pull_request_status(self, pr_number: int) -> Dict:
        """Get the current status of a pull request."""
        url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/pulls/{pr_number}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        pr_data = response.json()

        # Get status checks
        sha = pr_data["head"]["sha"]

        # Get both status (legacy) and check runs (modern)
        status_url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/commits/{sha}/status"
        status_response = requests.get(status_url, headers=self.headers)
        status_response.raise_for_status()

        checks_url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/commits/{sha}/check-runs"
        checks_response = requests.get(checks_url, headers=self.headers)
        checks_response.raise_for_status()

        return {
            "pr": pr_data,
            "status": status_response.json(),
            "checks": checks_response.json(),
            "sha": sha,
        }

    def wait_for_checks(self, pr_number: int, timeout: int = 600) -> bool:
        """Wait for CI checks to complete on a pull request."""
        start_time = time.time()
        print(f"Waiting for CI checks on PR #{pr_number}...")

        while time.time() - start_time < timeout:
            status_info = self.get_pull_request_status(pr_number)

            # Check legacy status API
            status_state = status_info["status"]["state"]

            # Check modern check runs API
            check_runs = status_info["checks"]["check_runs"]

            print(f"Status: {status_state}, Check runs: {len(check_runs)}")

            # If we have check runs, check their status
            if check_runs:
                all_completed = all(run["status"] == "completed" for run in check_runs)
                if all_completed:
                    success = all(run["conclusion"] == "success" for run in check_runs)
                    print(f"All checks completed. Success: {success}")
                    return success

            # Fallback to legacy status
            if status_state in ["success", "failure", "error"]:
                success = status_state == "success"
                print(f"Legacy status completed. Success: {success}")
                return success

            # Wait before checking again
            print("Checks still running, waiting 30 seconds...")
            time.sleep(30)

        raise GitHubIntegrationError(
            f"Timeout waiting for CI checks on PR #{pr_number}"
        )

    def merge_pull_request(self, pr_number: int, merge_method: str = "merge"):
        """Merge a pull request."""
        url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/pulls/{pr_number}/merge"
        data = {"merge_method": merge_method}
        response = requests.put(url, json=data, headers=self.headers)
        response.raise_for_status()

    def close_pull_request(self, pr_number: int):
        """Close a pull request."""
        url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/pulls/{pr_number}"
        data = {"state": "closed"}
        response = requests.patch(url, json=data, headers=self.headers)
        response.raise_for_status()

    def delete_branch(self, branch_name: str):
        """Delete a test branch."""
        url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/git/refs/heads/{branch_name}"
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()


@pytest.mark.integration
@pytest.mark.skipif(
    not os.environ.get("GITHUB_TOKEN") or os.environ.get("SKIP_INTEGRATION") == "true",
    reason="GITHUB_TOKEN required and SKIP_INTEGRATION not set",
)
class TestXLIntegration:
    """Integration tests with xl-test repository."""

    def setup_method(self):
        """Set up test instance."""
        self.xl_test = XLTestIntegration()
        self.test_branches: List[str] = []
        self.test_prs: List[int] = []

    def teardown_method(self):
        """Clean up test resources."""
        # Close PRs and delete branches
        for pr_number in self.test_prs:
            try:
                self.xl_test.close_pull_request(pr_number)
                print(f"Closed PR #{pr_number}")
            except Exception as e:
                print(f"Warning: Failed to close PR #{pr_number}: {e}")

        for branch_name in self.test_branches:
            try:
                self.xl_test.delete_branch(branch_name)
                print(f"Deleted branch {branch_name}")
            except Exception as e:
                print(f"Warning: Failed to delete branch {branch_name}: {e}")

    def test_ci_scripts_with_valid_excel_file(self):
        """Test CI scripts work with a valid Excel file."""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        python_version = f"{sys.version_info.major}{sys.version_info.minor}"
        branch_name = f"ci-test-valid-py{python_version}-{timestamp}"

        try:
            print(f"Creating test branch: {branch_name}")

            # 1. Create test branch
            self.xl_test.create_test_branch(branch_name)
            self.test_branches.append(branch_name)

            # 2. Update Book1.xltx with valid changes
            valid_excel_content = self.xl_test.create_valid_excel_file()
            commit_msg = f"test: Update Book1.xltx with valid changes - {timestamp}"

            self.xl_test.update_file_in_repo(
                "Book1.xltx", valid_excel_content, branch_name, commit_msg
            )
            print("Updated Book1.xltx with valid content")

            # 3 & 4. Create pull request
            pr_number = self.xl_test.create_pull_request(
                branch_name,
                f"[CI Test] Valid Excel file test - {timestamp}",
                f"Integration test to verify CI scripts work with valid Excel files.\n\nBranch: {branch_name}\nTimestamp: {timestamp}\nPython: {python_version}",
            )
            self.test_prs.append(pr_number)
            print(f"Created PR #{pr_number}")

            # 5. Wait for CI to complete and assert success
            success = self.xl_test.wait_for_checks(pr_number, timeout=600)  # 10 minutes
            assert (
                success
            ), f"CI checks failed for PR #{pr_number} with valid Excel file"

            # 6. Merge the PR (since it's valid)
            self.xl_test.merge_pull_request(pr_number)
            print(f"Merged PR #{pr_number}")

        except Exception as e:
            pytest.fail(f"Integration test with valid Excel file failed: {e}")

    def test_ci_scripts_detect_broken_references(self):
        """Test CI scripts can detect broken Excel references."""
        # Skip if running in CI matrix to avoid parallel PR creation
        if (
            os.environ.get("CI") == "true"
            and os.environ.get("FORCE_INTEGRATION") != "true"
        ):
            pytest.skip(
                "Skipping integration test in CI matrix to avoid parallel PR conflicts"
            )

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        python_version = f"{sys.version_info.major}{sys.version_info.minor}"
        branch_name = f"ci-test-broken-py{python_version}-{timestamp}"

        try:
            print(f"Creating test branch: {branch_name}")

            # 1. Create test branch
            self.xl_test.create_test_branch(branch_name)
            self.test_branches.append(branch_name)

            # 2. Update Book1.xltx with broken references
            broken_excel_content = self.xl_test.create_broken_excel_file()
            commit_msg = f"test: Update Book1.xltx with broken references - {timestamp}"

            self.xl_test.update_file_in_repo(
                "Book1.xltx", broken_excel_content, branch_name, commit_msg
            )
            print("Updated Book1.xltx with broken references")

            # 3 & 4. Create pull request
            pr_number = self.xl_test.create_pull_request(
                branch_name,
                f"[CI Test] Broken reference detection - {timestamp}",
                f"Integration test to verify CI scripts can detect broken Excel references.\n\nBranch: {branch_name}\nTimestamp: {timestamp}\nPython: {python_version}",
            )
            self.test_prs.append(pr_number)
            print(f"Created PR #{pr_number}")

            # 5. Wait for CI to complete and assert failure
            try:
                success = self.xl_test.wait_for_checks(pr_number, timeout=600)
                # We expect this to fail because of broken references
                assert (
                    not success
                ), f"CI checks should have failed for PR #{pr_number} with broken Excel references"
                print(f"CI correctly detected broken references in PR #{pr_number}")
            except GitHubIntegrationError:
                # If timeout, that's a test failure (CI should complete, even if it fails)
                pytest.fail(f"CI checks timed out for PR #{pr_number}")

            # 6. Close the PR without merging (since it has broken refs)
            self.xl_test.close_pull_request(pr_number)
            print(f"Closed PR #{pr_number} with broken references")

        except Exception as e:
            pytest.fail(f"Integration test with broken Excel references failed: {e}")


@pytest.mark.integration
def test_github_token_available():
    """Test that GitHub token is available for integration tests."""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        pytest.skip("GITHUB_TOKEN not available - integration tests will be skipped")

    # Verify token works
    headers = {"Authorization": f"token {token}"}
    response = requests.get("https://api.github.com/user", headers=headers)

    assert response.status_code == 200, "GitHub token is invalid or expired"


if __name__ == "__main__":
    # Allow running integration tests directly
    pytest.main([__file__, "-v", "-m", "integration"])
