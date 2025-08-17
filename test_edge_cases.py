#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Edge Case Testing for Signal Parser
Tests various signal formats and edge cases to ensure robustness
"""

from signal_parser import SignalParser, Signal

def test_edge_cases():
    """Test various edge cases and signal formats"""
    parser = SignalParser(default_stop_percentage=3.0)
    
    print("=== Testing Edge Cases ===\n")
    
    # Test case 1: Signal with missing fields
    print("Test 1: Signal with missing fields")
    incomplete_signal = """
BTC/USDT LONG
Entry: 45000
Target: 48000
"""
    result = parser.parse_signal_text(incomplete_signal)
    if result is None:
        print("✅ Correctly rejected incomplete signal")
    else:
        print("❌ Should have rejected incomplete signal")
    print()
    
    # Test case 2: Signal with invalid symbol format
    print("Test 2: Invalid symbol format")
    invalid_symbol = """
BTCUSDT LONG
Entry: 45000
Target: 48000
Stop: 44000
"""
    result = parser.parse_signal_text(invalid_symbol)
    if result is None:
        print("✅ Correctly rejected invalid symbol format")
    else:
        print("❌ Should have rejected invalid symbol format")
    print()
    
    # Test case 3: Signal with invalid direction
    print("Test 3: Invalid direction")
    invalid_direction = """
BTC/USDT BUY
Entry: 45000
Target: 48000
Stop: 44000
"""
    result = parser.parse_signal_text(invalid_direction)
    if result is None:
        print("✅ Correctly rejected invalid direction")
    else:
        print("❌ Should have rejected invalid direction")
    print()
    
    # Test case 4: Signal with non-numeric target
    print("Test 4: Non-numeric target")
    invalid_target = """
BTC/USDT LONG
Entry: 45000
Target: high
Stop: 44000
"""
    result = parser.parse_signal_text(invalid_target)
    if result is None:
        print("✅ Correctly rejected non-numeric target")
    else:
        print("❌ Should have rejected non-numeric target")
    print()
    
    # Test case 5: Signal with invalid stop format
    print("Test 5: Invalid stop format")
    invalid_stop = """
BTC/USDT LONG
Entry: 45000
Target: 48000
Stop: invalid
"""
    result = parser.parse_signal_text(invalid_stop)
    if result is None:
        print("✅ Correctly rejected invalid stop format")
    else:
        print("❌ Should have rejected invalid stop format")
    print()
    
    # Test case 6: Signal with very high percentage stop
    print("Test 6: Very high percentage stop")
    high_percentage = """
BTC/USDT LONG
Entry: 45000
Target: 48000
Stop: 50%
"""
    result = parser.parse_signal_text(high_percentage)
    if result is not None:
        print("✅ Successfully parsed high percentage stop")
        print(f"   Stop percentage: {result.stop_percentage}%")
    else:
        print("❌ Failed to parse high percentage stop")
    print()
    
    # Test case 7: Signal with decimal percentage stop
    print("Test 7: Decimal percentage stop")
    decimal_percentage = """
BTC/USDT LONG
Entry: 45000
Target: 48000
Stop: 2.75%
"""
    result = parser.parse_signal_text(decimal_percentage)
    if result is not None:
        print("✅ Successfully parsed decimal percentage stop")
        print(f"   Stop percentage: {result.stop_percentage}%")
    else:
        print("❌ Failed to parse decimal percentage stop")
    print()
    
    # Test case 8: Signal with very small numbers
    print("Test 8: Very small numbers")
    small_numbers = """
SHIB/USDT LONG
Entry: 0.00001234
Target: 0.00001500
Stop: 0.00001000
"""
    result = parser.parse_signal_text(small_numbers)
    if result is not None:
        print("✅ Successfully parsed very small numbers")
        print(f"   Entry: {result.entry}")
        print(f"   Target: {result.target}")
        print(f"   Stop: {result.stop}")
    else:
        print("❌ Failed to parse very small numbers")
    print()
    
    # Test case 9: Signal with very large numbers
    print("Test 9: Very large numbers")
    large_numbers = """
BTC/USDT LONG
Entry: 100000.50
Target: 120000.00
Stop: 95000.00
"""
    result = parser.parse_signal_text(large_numbers)
    if result is not None:
        print("✅ Successfully parsed very large numbers")
        print(f"   Entry: {result.entry}")
        print(f"   Target: {result.target}")
        print(f"   Stop: {result.stop}")
    else:
        print("❌ Failed to parse very large numbers")
    print()
    
    # Test case 10: Signal with mixed entry types
    print("Test 10: Mixed entry types")
    mixed_entries = [
        """
BTC/USDT LONG
Entry: market
Target: 48000
Stop: 3%
""",
        """
ETH/USDT SHORT
Entry: now
Target: 3000
Stop: 2.5%
""",
        """
ADA/USDT LONG
Entry: 0.50
Target: 0.55
Stop: 0.45
"""
    ]
    
    for i, signal_text in enumerate(mixed_entries, 1):
        result = parser.parse_signal_text(signal_text)
        if result is not None:
            print(f"✅ Signal {i}: Successfully parsed {result.entry} entry")
        else:
            print(f"❌ Signal {i}: Failed to parse")
    print()
    
    # Test case 11: Validation with different test prices
    print("Test 11: Validation with different test prices")
    test_signal = """
BTC/USDT LONG
Entry: 45000
Target: 48000
Stop: 3%
"""
    result = parser.parse_signal_text(test_signal)
    if result is not None:
        test_prices = [1000, 45000, 100000]
        for price in test_prices:
            validation = parser.validate_signal(result, price)
            calculated_stop = validation.get('calculated_stop')
            if calculated_stop:
                print(f"   Test price {price}: Calculated stop = {calculated_stop:.2f}")
    print()
    
    # Test case 12: Empty and whitespace-only signals
    print("Test 12: Empty and whitespace signals")
    empty_signals = ["", "   ", "\n\n\n", "  \n  \n  "]
    for i, signal_text in enumerate(empty_signals, 1):
        result = parser.parse_signal_text(signal_text)
        if result is None:
            print(f"✅ Empty signal {i}: Correctly rejected")
        else:
            print(f"❌ Empty signal {i}: Should have been rejected")
    print()
    
    print("=== Edge Case Testing Complete ===")

if __name__ == "__main__":
    test_edge_cases()