#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Edge Case Testing for Signal Parser (Updated for new Signal class)
"""

from signal_parser import SignalParser, Signal

def test_edge_cases():
    """Test various edge cases and signal formats"""
    parser = SignalParser(default_stop_percentage=3.0)
    
    print("=== Testing Edge Cases ===\n")
    
    # Test case 1: Signal with missing fields (no stop) -> should now be handled by default
    print("Test 1: Signal with missing stop")
    incomplete_signal = "BTC/USDT LONG\nEntry: 45000\nTarget: 48000"
    result = parser.parse_signal_text(incomplete_signal)
    if result and result.stop[0] == -3.0:
        print("✅ Correctly parsed and applied default stop")
    else:
        print("❌ Failed to apply default stop")
    print()
    
    # Test case 2: Signal with invalid symbol format
    print("Test 2: Invalid symbol format")
    invalid_symbol = "BTCUSDT LONG\nEntry: 45000\nTarget: 48000\nStop: 44000"
    result = parser.parse_signal_text(invalid_symbol)
    if result is None:
        print("✅ Correctly rejected invalid symbol format")
    else:
        print(f"❌ Should have rejected invalid symbol format, but got {result}")
    print()

    # Test case 3: Signal with invalid direction
    print("Test 3: Invalid direction")
    invalid_direction = "BTC/USDT BUY\nEntry: 45000\nTarget: 48000\nStop: 44000"
    result = parser.parse_signal_text(invalid_direction)
    # The new parser is more flexible and should handle 'BUY' as 'LONG'
    if result and result.direction == 'LONG':
        print("✅ Correctly interpreted 'BUY' as 'LONG'")
    else:
        print("❌ Failed to interpret 'BUY' as 'LONG'")
    print()

    # Test case 4: Signal with non-numeric target
    print("Test 4: Non-numeric target")
    invalid_target = "BTC/USDT LONG\nEntry: 45000\nTarget: high\nStop: 44000"
    result = parser.parse_signal_text(invalid_target)
    if result and not result.targets:
        print("✅ Correctly handled non-numeric target")
    else:
        print("❌ Failed to handle non-numeric target")
    print()

    # Test case 5: Signal with invalid stop format
    print("Test 5: Invalid stop format")
    invalid_stop = "BTC/USDT LONG\nEntry: 45000\nTarget: 48000\nStop: invalid"
    result = parser.parse_signal_text(invalid_stop)
    if result and result.stop[0] < 0: # Should default
        print("✅ Correctly handled invalid stop by applying default")
    else:
        print("❌ Failed to handle invalid stop")
    print()

    # Test case 6: Signal with very high percentage stop
    print("Test 6: Very high percentage stop")
    high_percentage = "BTC/USDT LONG\nEntry: 45000\nTarget: 48000\nStop: 50%"
    result = parser.parse_signal_text(high_percentage)
    if result and result.stop[0] == -50.0:
        print("✅ Successfully parsed high percentage stop")
        print(f"   Stop value: {result.stop[0]}%")
    else:
        print("❌ Failed to parse high percentage stop")
    print()

    # Test case 7: Signal with decimal percentage stop
    print("Test 7: Decimal percentage stop")
    decimal_percentage = "BTC/USDT LONG\nEntry: 45000\nTarget: 48000\nStop: 2.75%"
    result = parser.parse_signal_text(decimal_percentage)
    if result and result.stop[0] == -2.75:
        print("✅ Successfully parsed decimal percentage stop")
        print(f"   Stop value: {result.stop[0]}%")
    else:
        print("❌ Failed to parse decimal percentage stop")
    print()

    # Test case 8: Signal with very small numbers
    print("Test 8: Very small numbers")
    small_numbers = "SHIB/USDT LONG\nEntry: 0.00001234\nTarget: 0.00001500\nStop: 0.00001000"
    result = parser.parse_signal_text(small_numbers)
    if result:
        print("✅ Successfully parsed very small numbers")
        print(f"   Entry: {result.entry}")
        print(f"   Targets: {result.targets}")
        print(f"   Stop: {result.stop}")
    else:
        print("❌ Failed to parse very small numbers")
    print()

    # Test case 9: Signal with very large numbers
    print("Test 9: Very large numbers")
    large_numbers = "BTC/USDT LONG\nEntry: 100000.50\nTarget: 120000.00\nStop: 95000.00"
    result = parser.parse_signal_text(large_numbers)
    if result:
        print("✅ Successfully parsed very large numbers")
        print(f"   Entry: {result.entry}")
        print(f"   Targets: {result.targets}")
        print(f"   Stop: {result.stop}")
    else:
        print("❌ Failed to parse very large numbers")
    print()

    # Test case 10: Empty and whitespace-only signals
    print("Test 10: Empty and whitespace signals")
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