#!/usr/bin/env python3
"""
Test runner script for the media-manipulator service.
Provides convenient test execution with different options.
"""

import sys
import subprocess
from pathlib import Path

def run_tests(test_type="all", verbose=True, coverage=False):
    """
    Run tests with specified options.
    
    Args:
        test_type: Type of tests to run ("all", "unit", "integration")
        verbose: Whether to run in verbose mode
        coverage: Whether to generate coverage report
    """
    
    # Base pytest command
    cmd = ["python3", "-m", "pytest"]
    
    # Add test path based on type
    if test_type == "unit":
        cmd.append("tests/unit/")
    elif test_type == "integration":
        cmd.append("tests/integration/")
    else:  # all
        cmd.append("tests/")
    
    # Add verbose flag
    if verbose:
        cmd.append("-v")
    
    # Add coverage if requested
    if coverage:
        cmd.extend(["--cov=video_editor", "--cov-report=html", "--cov-report=term"])
    
    print(f"Running {test_type} tests...")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 60)
    
    # Run the tests
    result = subprocess.run(cmd)
    return result.returncode

def main():
    """Main function to handle command line arguments."""
    
    if len(sys.argv) < 2:
        print("Usage: python3 run_tests.py [all|unit|integration] [--coverage]")
        print("\nExamples:")
        print("  python3 run_tests.py all          # Run all tests")
        print("  python3 run_tests.py unit         # Run only unit tests")
        print("  python3 run_tests.py integration  # Run only integration tests")
        print("  python3 run_tests.py all --coverage  # Run all tests with coverage")
        return 1
    
    test_type = sys.argv[1].lower()
    coverage = "--coverage" in sys.argv
    
    if test_type not in ["all", "unit", "integration"]:
        print(f"Error: Invalid test type '{test_type}'. Use 'all', 'unit', or 'integration'.")
        return 1
    
    return run_tests(test_type=test_type, coverage=coverage)

if __name__ == "__main__":
    sys.exit(main())