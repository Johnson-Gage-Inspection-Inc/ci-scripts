# Integration Tests

This directory contains integration tests that validate the CI scripts against real repositories.

## XL-Test Integration

The `test_integration_xl_test.py` file contains integration tests that create actual Pull Requests in the [xl-test repository](https://github.com/Johnson-Gage-Inspection-Inc/xl-test) to verify that the CI scripts work end-to-end in a real GitHub Actions environment.

### Prerequisites

1. **GitHub Token**: You need a GitHub personal access token with the following permissions:
   - `repo` (Full control of private repositories)
   - `workflow` (Update GitHub Action workflows)

2. **Environment Variables**:
   ```bash
   export GITHUB_TOKEN="your_github_token_here"
   ```

3. **Dependencies**:
   ```bash
   pip install requests
   ```

### Running Integration Tests

To run the integration tests:

```bash
# Run all integration tests
pytest tests/test_integration_xl_test.py -m integration -v

# Skip integration tests (useful for CI where you don't want to create PRs)
export SKIP_INTEGRATION=true
pytest tests/ -v

# Run only integration tests locally
pytest tests/test_integration_xl_test.py::TestXLIntegration -v
```

### What the Tests Do

1. **test_ci_scripts_with_valid_excel_file**: 
   - Creates a test branch in xl-test
   - Makes a commit that triggers CI
   - Opens a Pull Request
   - Waits for CI to complete successfully
   - Cleans up the branch and PR

2. **test_ci_scripts_detect_broken_references**:
   - Creates a test branch with changes that might have broken references
   - Verifies that CI runs and can detect issues
   - Cleans up afterwards

### Safety and Cleanup

- Tests automatically clean up after themselves by:
  - Closing any created Pull Requests
  - Deleting any created test branches
- Test branch names include timestamps to avoid conflicts
- PRs are clearly marked as `[CI Test]` in the title

### CI Integration

In the main CI pipeline, integration tests are skipped by default to avoid creating unnecessary PRs and prevent conflicts from the Python version matrix (which would try to create 4 parallel PRs). They can be enabled by:

1. Setting `GITHUB_TOKEN` in CI secrets
2. Setting `FORCE_INTEGRATION=true` to override the CI skip logic
3. Removing `SKIP_INTEGRATION=true` from the workflow

**Note**: When enabled in CI matrix, each Python version will create separate branches with version-specific names (e.g., `ci-test-valid-py38-20250711-143022`) to avoid conflicts.

### Troubleshooting

- **GitHub API rate limits**: If you hit rate limits, wait and try again
- **Token permissions**: Ensure your token has `repo` and `workflow` permissions
- **Network issues**: Tests have timeout handling but may need retry logic
- **Repository access**: Ensure the token has access to the xl-test repository
