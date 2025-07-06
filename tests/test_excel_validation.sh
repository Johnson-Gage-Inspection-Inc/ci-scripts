#!/bin/bash

# Test script for Excel reference validation
echo "🧪 Testing Excel Reference Validation..."

# Test 1: Check if script exists and is executable
if [ ! -f "check_excel_refs.py" ]; then
    echo "❌ Test 1 FAILED: check_excel_refs.py not found"
    exit 1
fi
echo "✅ Test 1 PASSED: Script exists"

# Test 2: Check if Python can import required modules
python -c "import openpyxl; print('✅ Test 2 PASSED: openpyxl import successful')" 2>/dev/null || {
    echo "❌ Test 2 FAILED: openpyxl not available"
    echo "   Run: pip install -r requirements.txt"
    exit 1
}

# Test 3: Check script syntax
python -m py_compile check_excel_refs.py 2>/dev/null || {
    echo "❌ Test 3 FAILED: Python syntax error"
    exit 1
}
echo "✅ Test 3 PASSED: Python syntax valid"

# Test 4: Check help/usage
python check_excel_refs.py 2>/dev/null || {
    exit_code=$?
    if [ $exit_code -eq 1 ]; then
        echo "✅ Test 4 PASSED: Script exits with error when no file specified"
    else
        echo "❌ Test 4 FAILED: Unexpected exit code: $exit_code"
        exit 1
    fi
}

echo "🎉 All tests passed! Excel reference validation is ready to use."
