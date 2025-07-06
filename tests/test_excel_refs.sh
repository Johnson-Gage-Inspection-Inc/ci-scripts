#!/bin/bash

# Test suite for Excel reference validation
echo "=== Excel Reference Validation Test Suite ==="
echo ""

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_TOTAL=0

# Test function
run_test() {
    local test_name="$1"
    local command="$2"
    local expected_exit_code="$3"
    local expected_output="$4"
    
    TESTS_TOTAL=$((TESTS_TOTAL + 1))
    echo "Running: $test_name"
    
    # Run the command and capture output and exit code
    output=$(eval "$command" 2>&1)
    exit_code=$?
    
    # Check exit code
    if [ "$exit_code" -eq "$expected_exit_code" ]; then
        # Check output if provided
        if [ -n "$expected_output" ]; then
            if echo "$output" | grep -q "$expected_output"; then
                echo "✅ PASSED: $test_name"
                TESTS_PASSED=$((TESTS_PASSED + 1))
            else
                echo "❌ FAILED: $test_name (output mismatch)"
                echo "   Expected: $expected_output"
                echo "   Got: $output"
                TESTS_FAILED=$((TESTS_FAILED + 1))
            fi
        else
            echo "✅ PASSED: $test_name"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        fi
    else
        echo "❌ FAILED: $test_name (exit code mismatch)"
        echo "   Expected exit code: $expected_exit_code"
        echo "   Got exit code: $exit_code"
        echo "   Output: $output"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
    echo ""
}

# Test 1: No file specified
run_test "No file specified" \
         "python check_excel_refs.py" \
         1 \
         "No Excel file specified"

# Test 2: Non-existent file
run_test "Non-existent file" \
         "python check_excel_refs.py 'nonexistent.xlsx'" \
         1 \
         "File not found"

# Test 3: Unsupported file type
run_test "Unsupported file type" \
         "python check_excel_refs.py 'test.txt'" \
         1 \
         "Unsupported file type"

# Test 4: File with broken references
run_test "File with broken references" \
         "python check_excel_refs.py 'tests/test_files/has_broken_ref.xltm'" \
         1 \
         "Found 1 #REF! errors"

# Test 5: File with no errors
run_test "File with no errors" \
         "python check_excel_refs.py 'tests/test_files/has_no_errors.xltm'" \
         0 \
         "No #REF! errors found"

# Test 6: Export functionality
run_test "Export sheets functionality" \
         "EXPORT_SHEETS=true python check_excel_refs.py 'tests/test_files/has_no_errors.xltm'" \
         0 \
         "Sheets exported to"

# Summary
echo "=== Test Results ==="
echo "Total tests: $TESTS_TOTAL"
echo "Passed: $TESTS_PASSED"
echo "Failed: $TESTS_FAILED"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo "🎉 All tests passed!"
    exit 0
else
    echo "❌ Some tests failed."
    exit 1
fi
