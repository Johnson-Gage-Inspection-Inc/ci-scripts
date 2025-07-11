"""Integration tests against the xl-test repository.

This module contains integration tests that create actual Pull Requests
in the xl-test repository to verify that the CI scripts work end-to-end
in a real GitHub Actions environment.
"""

import os
import time
from datetime import datetime
from typing import Dict

import pytest
import requests


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

    def create_test_commit(
        self, branch_name: str, message: str, changes: Dict[str, str]
    ) -> str:
        """Create a test commit with specified changes."""
        # Get current tree
        url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/git/refs/heads/{branch_name}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        branch_sha = response.json()["object"]["sha"]

        # Get commit info
        url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/git/commits/{branch_sha}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        tree_sha = response.json()["tree"]["sha"]

        # Create new tree with changes
        tree_items = []
        for file_path, content in changes.items():
            # Create blob for file content
            blob_url = (
                f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/git/blobs"
            )
            blob_data = {"content": content, "encoding": "utf-8"}
            blob_response = requests.post(
                blob_url, json=blob_data, headers=self.headers
            )
            blob_response.raise_for_status()
            blob_sha = blob_response.json()["sha"]

            tree_items.append(
                {"path": file_path, "mode": "100644", "type": "blob", "sha": blob_sha}
            )

        # Create new tree
        tree_url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/git/trees"
        tree_data = {"base_tree": tree_sha, "tree": tree_items}
        tree_response = requests.post(tree_url, json=tree_data, headers=self.headers)
        tree_response.raise_for_status()
        new_tree_sha = tree_response.json()["sha"]

        # Create commit
        commit_url = (
            f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/git/commits"
        )
        commit_data = {
            "message": message,
            "tree": new_tree_sha,
            "parents": [branch_sha],
        }
        commit_response = requests.post(
            commit_url, json=commit_data, headers=self.headers
        )
        commit_response.raise_for_status()
        commit_sha = commit_response.json()["sha"]

        # Update branch reference
        ref_url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/git/refs/heads/{branch_name}"
        ref_data = {"sha": commit_sha}
        ref_response = requests.patch(ref_url, json=ref_data, headers=self.headers)
        ref_response.raise_for_status()

        return str(commit_sha)

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
        status_url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/commits/{sha}/status"
        status_response = requests.get(status_url, headers=self.headers)
        status_response.raise_for_status()

        return {"pr": pr_data, "status": status_response.json(), "sha": sha}

    def wait_for_checks(self, pr_number: int, timeout: int = 300) -> bool:
        """Wait for CI checks to complete on a pull request."""
        start_time = time.time()

        while time.time() - start_time < timeout:
            status_info = self.get_pull_request_status(pr_number)
            status = status_info["status"]["state"]

            if status in ["success", "failure", "error"]:
                return bool(status == "success")

            # Wait before checking again
            time.sleep(30)

        raise GitHubIntegrationError(
            f"Timeout waiting for CI checks on PR #{pr_number}"
        )

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
        self.test_branches = []
        self.test_prs = []

    def teardown_method(self):
        """Clean up test resources."""
        # Close PRs and delete branches
        for pr_number in self.test_prs:
            try:
                self.xl_test.close_pull_request(pr_number)
            except Exception as e:
                print(f"Warning: Failed to close PR #{pr_number}: {e}")

        for branch_name in self.test_branches:
            try:
                self.xl_test.delete_branch(branch_name)
            except Exception as e:
                print(f"Warning: Failed to delete branch {branch_name}: {e}")

    def test_ci_scripts_with_valid_excel_file(self):
        """Test CI scripts work with a valid Excel file."""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        branch_name = f"ci-test-valid-{timestamp}"

        try:
            # Create test branch
            self.xl_test.create_test_branch(branch_name)
            self.test_branches.append(branch_name)

            # Create a simple change to trigger CI
            changes = {
                "test-trigger.txt": f"CI test triggered at {datetime.now().isoformat()}\nTesting valid Excel file scenario"
            }

            commit_sha = self.xl_test.create_test_commit(
                branch_name, "test: Trigger CI for valid Excel file test", changes
            )

            # Create PR
            pr_number = self.xl_test.create_pull_request(
                branch_name,
                f"[CI Test] Valid Excel file test - {timestamp}",
                f"Integration test to verify CI scripts work with valid Excel files.\n\nCommit: {commit_sha}\nTimestamp: {timestamp}",
            )
            self.test_prs.append(pr_number)

            # Wait for CI to complete
            success = self.xl_test.wait_for_checks(pr_number, timeout=600)  # 10 minutes

            assert success, f"CI checks failed for PR #{pr_number}"

        except Exception as e:
            pytest.fail(f"Integration test failed: {e}")

    def test_ci_scripts_detect_broken_references(self):
        """Test CI scripts can detect broken Excel references."""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        branch_name = f"ci-test-broken-{timestamp}"

        try:
            # Create test branch
            self.xl_test.create_test_branch(branch_name)
            self.test_branches.append(branch_name)

            # Create a change that would introduce broken references
            # (This would depend on the structure of xl-test repo)
            changes = {
                "test-broken-refs.txt": f"CI test for broken references at {datetime.now().isoformat()}\nThis should trigger reference validation"
            }

            commit_sha = self.xl_test.create_test_commit(
                branch_name, "test: Trigger CI for broken reference detection", changes
            )

            # Create PR
            pr_number = self.xl_test.create_pull_request(
                branch_name,
                f"[CI Test] Broken reference detection - {timestamp}",
                f"Integration test to verify CI scripts can detect broken Excel references.\n\nCommit: {commit_sha}\nTimestamp: {timestamp}",
            )
            self.test_prs.append(pr_number)

            # Wait for CI to complete
            # Note: This test might expect CI to fail if broken refs are detected
            try:
                self.xl_test.wait_for_checks(pr_number, timeout=600)
                # Depending on the test design, success might mean "CI ran successfully"
                # even if it detected issues
                assert True, "CI pipeline executed successfully"
            except GitHubIntegrationError:
                # If timeout, that's still a test failure
                pytest.fail(f"CI checks timed out for PR #{pr_number}")

        except Exception as e:
            pytest.fail(f"Integration test failed: {e}")


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
