#!/bin/bash
set -e  # Exit on first error

# Run shared authentication & file preparation
source "$(dirname "$0")/auth_and_prepare.sh"

echo "✅ Pre-merge validation passed!"
