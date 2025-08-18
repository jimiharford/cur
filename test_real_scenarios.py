#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Trading Scenarios Test for Signal Parser (Updated for new Signal class)
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
        "BTC/USDT LONG\nEntry: 45000\nTarget: 50000\nStop: 2%",
        "ETH/USDT LONG\nEntry: 3200\nTarget: 3800\nStop: 3%",
        "ADA/USDT LONG\nEntry: market\nTarget: 0.60\nStop: 4%"
    ]
    
    for i, signal_text in enumerate(bull_signals, 1):
        signal = parser.parse_signal_text(signal_text)
        if signal:
            print(f"✅ Bull signal {i}: {signal.symbol} {signal.direction}")
            print(f"   Entry: {signal.entry}, Targets: {signal.targets}, Stop: {signal.stop}")
            if signal.stop and signal.stop[0] < 0:
                print(f"   Stop percentage: {abs(signal.stop[0])}%")
        else:
            print(f"❌ Bull signal {i}: Failed to parse")
    print()
    
    # Scenario 2: Bear market signals
    print("Scenario 2: Bear Market Signals")
    bear_signals = [
        "BTC/USDT SHORT\nEntry: 50000\nTarget: 45000\nStop: 2.5%",
        "ETH/USDT SHORT\nEntry: now\nTarget: 2800\nStop: 3%",
        "SOL/USDT SHORT\nEntry: 100\nTarget: 85\nStop: 4%"
    ]
    
    for i, signal_text in enumerate(bear_signals, 1):
        signal = parser.parse_signal_text(signal_text)
        if signal:
            print(f"✅ Bear signal {i}: {signal.symbol} {signal.direction}")
            print(f"   Entry: {signal.entry}, Targets: {signal.targets}, Stop: {signal.stop}")
            if signal.stop and signal.stop[0] < 0:
                print(f"   Stop percentage: {abs(signal.stop[0])}%")
        else:
            print(f"❌ Bear signal {i}: Failed to parse")
    print()
    
    # Scenario 3: High volatility signals
    print("Scenario 3: High Volatility Signals")
    volatile_signals = [
        "DOGE/USDT LONG\nEntry: 0.08\nTarget: 0.12\nStop: 6%",
        "SHIB/USDT SHORT\nEntry: 0.00002\nTarget: 0.000015\nStop: 8%",
        "GME/USDT LONG\nEntry: market\nTarget: 25\nStop: 10%"
    ]
    
    for i, signal_text in enumerate(volatile_signals, 1):
        signal = parser.parse_signal_text(signal_text)
        if signal:
            print(f"✅ Volatile signal {i}: {signal.symbol} {signal.direction}")
            print(f"   Entry: {signal.entry}, Targets: {signal.targets}, Stop: {signal.stop}")
            if signal.stop and signal.stop[0] < 0:
                print(f"   Stop percentage: {abs(signal.stop[0])}%")
        else:
            print(f"❌ Volatile signal {i}: Failed to parse")
    print()
    
    print("=== Real Scenarios Test Complete ===")

if __name__ == "__main__":
    test_real_scenarios()