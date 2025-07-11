# Integration Test Setup

## Overview

The integration tests in `tests/test_integration_xl_test.py` create real Pull Requests in the [xl-test](https://github.com/Johnson-Gage-Inspection-Inc/xl-test) repository to verify that the CI scripts work end-to-end.

## Required Setup

### 1. Personal Access Token

Create a fine-grained Personal Access Token with these permissions for the `xl-test` repository:

- **Contents**: Read and write (to update Book1.xltx)
- **Pull requests**: Write (to create and manage PRs)
- **Actions**: Read (to monitor workflow status)  
- **Metadata**: Read (mandatory)

### 2. Repository Secret

Add the token as a repository secret in the ci-scripts repository:

1. Go to ci-scripts → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `INTEGRATION_GITHUB_TOKEN`
4. Value: paste the Personal Access Token

### 3. Integration Test Execution

Integration tests will only run when:
- `GITHUB_TOKEN` environment variable is available
- `SKIP_INTEGRATION` is not set to `"true"`
- In CI, they only run on Python 3.11 to avoid parallel PR creation

## What the Tests Do

### Parallel Creation + Sequential Handling Workflow

The integration test uses an optimized approach for faster execution while avoiding merge conflicts:

**Phase 1: Parallel Creation (fast setup)**
1. Creates both branches simultaneously in xl-test
2. Updates Book1.xltx with broken references in first branch
3. Updates Book1.xltx with valid content in second branch  
4. Creates both PRs at the same time

**Phase 2: Sequential Handling (conflict-free processing)**
1. Waits for broken reference PR to fail CI (240s timeout - expects quick failure)
2. Closes the broken PR (clears the way for clean merge)
3. Waits for valid Excel PR to pass CI (360s timeout - allows full pipeline)
4. Merges the valid PR (tests post-merge pipeline)

**Performance Optimizations:**
- ⚡ **Adaptive polling** - starts with 15s intervals, increases to 30s once checks begin
- 📊 **Progress reporting** - shows elapsed time, running checks, and failure details
- ⏱️ **Optimized timeouts** - shorter for expected failures, longer for complete validation
- 🔄 **Parallel creation** - both PRs created simultaneously before sequential processing

**Benefits:**
- ⚡ **Faster execution** - parallel PR creation + adaptive polling intervals
- 🚫 **No merge conflicts** - sequential close/merge operations  
- ✅ **Complete validation** - tests both failure and success scenarios
- 🔄 **Post-merge testing** - validates pipeline after merge
- 📊 **Better monitoring** - detailed progress and failure reporting
- ⏱️ **Smart timeouts** - optimized for expected completion times

The test creates **2 PRs per run** but handles them intelligently to avoid conflicts.

## Debugging

Use the debug script to test skip logic:
```bash
python debug_integration_skip.py
```

Run integration tests manually:
```bash
export GITHUB_TOKEN="your_token_here"
export SKIP_INTEGRATION=false
pytest tests/test_integration_xl_test.py -v -m integration
```

## Safety Features

- Tests only run on Python 3.11 in CI matrix
- Branch names include timestamp to avoid conflicts
- Automatic cleanup in teardown methods
- Graceful error handling for API failures
- Tests are skipped if token permissions are insufficient

## ✅ Status: WORKING

Integration tests are successfully creating PRs in xl-test repository and validating the CI pipeline end-to-end.

**Recent test results:**
- ✅ PR #54: Valid Excel → Tests passed → **Merged**
- ✅ PR #55: Valid Excel → Tests passed → **Closed** (cleanup)
- ✅ PR #56: Broken Excel → Tests failed → **Closed** (as intended)
- ⚠️ PR #57: Merge conflict on Book1.xltx (expected due to parallel updates)

## Monitoring Integration Tests

Check the [xl-test Pull Requests](https://github.com/Johnson-Gage-Inspection-Inc/xl-test/pulls) to see active integration test runs.

PR naming pattern: `[CI Test] <test-type> - <timestamp>`
- Valid Excel tests should pass CI and be merged
- Broken Excel tests should fail CI and be closed

## Handling Merge Conflicts

When multiple integration tests run simultaneously, they may create merge conflicts on Book1.xltx. This is expected and can be resolved by:
1. Manually resolving conflicts in conflicted PRs, or
2. Closing conflicted PRs (the test validation is already complete)
