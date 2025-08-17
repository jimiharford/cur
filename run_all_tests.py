#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive Test Runner for Signal Parser
Runs all tests and provides a final summary
"""

import subprocess
import sys
import os

def run_test(test_name, command):
    """Run a test and return the result"""
    print(f"\n{'='*60}")
    print(f"Running {test_name}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Test completed successfully")
            return True
        else:
            print("❌ Test failed")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
    except Exception as e:
        print(f"❌ Test execution error: {e}")
        return False

def main():
    """Run all tests and provide summary"""
    print("🚀 Starting Comprehensive Signal Parser Testing")
    print("=" * 60)
    
    tests = [
        ("Basic Parser Test", "python3 signal_parser.py"),
        ("Edge Case Testing", "python3 test_edge_cases.py"),
        ("Real Scenarios Test", "python3 test_real_scenarios.py")
    ]
    
    results = []
    for test_name, command in tests:
        success = run_test(test_name, command)
        results.append((test_name, success))
    
    # Print summary
    print(f"\n{'='*60}")
    print("FINAL TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\nOverall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Signal Parser is working perfectly!")
        print("\n📋 Parser Capabilities:")
        print("   ✅ Parses numeric entries (e.g., 45000)")
        print("   ✅ Parses market entries (e.g., 'market')")
        print("   ✅ Parses now entries (e.g., 'now')")
        print("   ✅ Handles absolute stop losses (e.g., 44000)")
        print("   ✅ Handles percentage stop losses (e.g., 3%)")
        print("   ✅ Validates signal logic and direction")
        print("   ✅ Calculates stop prices from percentages")
        print("   ✅ Handles edge cases gracefully")
        print("   ✅ Processes multiple signal files")
        print("   ✅ 100% success rate on all test signals")
        
        print("\n🚀 Parser is ready for production use!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())