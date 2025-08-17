#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Trading Scenarios Test for Signal Parser
Tests the parser with realistic trading scenarios and market conditions
"""

from signal_parser import SignalParser
import random

def test_real_scenarios():
    """Test parser with realistic trading scenarios"""
    parser = SignalParser(default_stop_percentage=3.0)
    
    print("=== Real Trading Scenarios Test ===\n")
    
    # Scenario 1: Bull market signals
    print("Scenario 1: Bull Market Signals")
    bull_signals = [
        """
BTC/USDT LONG
Entry: 45000
Target: 50000
Stop: 2%
""",
        """
ETH/USDT LONG
Entry: 3200
Target: 3800
Stop: 3%
""",
        """
ADA/USDT LONG
Entry: market
Target: 0.60
Stop: 4%
"""
    ]
    
    for i, signal_text in enumerate(bull_signals, 1):
        signal = parser.parse_signal_text(signal_text)
        if signal:
            print(f"✅ Bull signal {i}: {signal.symbol} {signal.direction}")
            print(f"   Entry: {signal.entry}, Target: {signal.target}, Stop: {signal.stop}")
            if signal.stop < 0:
                print(f"   Stop percentage: {signal.stop_percentage}%")
        else:
            print(f"❌ Bull signal {i}: Failed to parse")
    print()
    
    # Scenario 2: Bear market signals
    print("Scenario 2: Bear Market Signals")
    bear_signals = [
        """
BTC/USDT SHORT
Entry: 50000
Target: 45000
Stop: 2.5%
""",
        """
ETH/USDT SHORT
Entry: now
Target: 2800
Stop: 3%
""",
        """
SOL/USDT SHORT
Entry: 100
Target: 85
Stop: 4%
"""
    ]
    
    for i, signal_text in enumerate(bear_signals, 1):
        signal = parser.parse_signal_text(signal_text)
        if signal:
            print(f"✅ Bear signal {i}: {signal.symbol} {signal.direction}")
            print(f"   Entry: {signal.entry}, Target: {signal.target}, Stop: {signal.stop}")
            if signal.stop < 0:
                print(f"   Stop percentage: {signal.stop_percentage}%")
        else:
            print(f"❌ Bear signal {i}: Failed to parse")
    print()
    
    # Scenario 3: High volatility signals
    print("Scenario 3: High Volatility Signals")
    volatile_signals = [
        """
DOGE/USDT LONG
Entry: 0.08
Target: 0.12
Stop: 6%
""",
        """
SHIB/USDT SHORT
Entry: 0.00002
Target: 0.000015
Stop: 8%
""",
        """
GME/USDT LONG
Entry: market
Target: 25
Stop: 10%
"""
    ]
    
    for i, signal_text in enumerate(volatile_signals, 1):
        signal = parser.parse_signal_text(signal_text)
        if signal:
            print(f"✅ Volatile signal {i}: {signal.symbol} {signal.direction}")
            print(f"   Entry: {signal.entry}, Target: {signal.target}, Stop: {signal.stop}")
            if signal.stop < 0:
                print(f"   Stop percentage: {signal.stop_percentage}%")
        else:
            print(f"❌ Volatile signal {i}: Failed to parse")
    print()
    
    # Scenario 4: Conservative signals
    print("Scenario 4: Conservative Signals")
    conservative_signals = [
        """
USDT/USDT LONG
Entry: 1.00
Target: 1.02
Stop: 1%
""",
        """
BUSD/USDT SHORT
Entry: 1.00
Target: 0.99
Stop: 0.5%
""",
        """
DAI/USDT LONG
Entry: market
Target: 1.01
Stop: 1.5%
"""
    ]
    
    for i, signal_text in enumerate(conservative_signals, 1):
        signal = parser.parse_signal_text(signal_text)
        if signal:
            print(f"✅ Conservative signal {i}: {signal.symbol} {signal.direction}")
            print(f"   Entry: {signal.entry}, Target: {signal.target}, Stop: {signal.stop}")
            if signal.stop < 0:
                print(f"   Stop percentage: {signal.stop_percentage}%")
        else:
            print(f"❌ Conservative signal {i}: Failed to parse")
    print()
    
    # Scenario 5: Test with realistic market prices
    print("Scenario 5: Realistic Market Price Calculations")
    test_signal = """
BTC/USDT LONG
Entry: 45000
Target: 50000
Stop: 3%
"""
    
    signal = parser.parse_signal_text(test_signal)
    if signal:
        print(f"✅ Test signal: {signal.symbol} {signal.direction}")
        
        # Test with different entry prices (simulating market conditions)
        test_prices = [44000, 45000, 46000, 47000]
        for price in test_prices:
            validation = parser.validate_signal(signal, price)
            calculated_stop = validation.get('calculated_stop')
            if calculated_stop:
                risk_amount = abs(price - calculated_stop)
                risk_percentage = (risk_amount / price) * 100
                print(f"   Entry at {price}: Stop at {calculated_stop:.2f}, Risk: {risk_percentage:.2f}%")
    print()
    
    # Scenario 6: Batch processing test
    print("Scenario 6: Batch Processing Test")
    
    # Create a batch of mixed signals
    batch_signals = []
    for i in range(10):
        direction = "LONG" if i % 2 == 0 else "SHORT"
        entry_type = random.choice(["market", "now", str(100 + i * 10)])
        target = 100 + i * 15
        stop_type = random.choice(["2%", "3%", "4%", str(95 + i * 5)])
        
        # Use valid symbol format
        symbol = f"TEST{i:02d}/USDT"
        
        signal_text = f"""{symbol} {direction}
Entry: {entry_type}
Target: {target}
Stop: {stop_type}"""
        batch_signals.append(signal_text)
    
    print(f"Created {len(batch_signals)} test signals")
    
    # Create a temporary batch file
    batch_content = "\n\n".join(batch_signals)
    # Remove trailing newlines to match the working format
    batch_content = batch_content.rstrip('\n')
    with open("temp_batch_signals.txt", "w") as f:
        f.write(batch_content)
    
    # Debug: show the content
    print("Generated batch file content:")
    print("=" * 50)
    print(batch_content)
    print("=" * 50)
    
    # Parse the batch file
    parsed_signals = parser.parse_file("temp_batch_signals.txt")
    
    print(f"Successfully parsed {len(parsed_signals)} out of {len(batch_signals)} signals")
    
    # Validate all parsed signals
    valid_count = 0
    for signal in parsed_signals:
        validation = parser.validate_signal(signal, 1000.0)
        if validation['valid']:
            valid_count += 1
    
    print(f"Validation: {valid_count} valid out of {len(parsed_signals)} parsed signals")
    
    # Clean up temporary file
    import os
    if os.path.exists("temp_batch_signals.txt"):
        os.remove("temp_batch_signals.txt")
    
    print()
    
    print("=== Real Scenarios Test Complete ===")

if __name__ == "__main__":
    test_real_scenarios()