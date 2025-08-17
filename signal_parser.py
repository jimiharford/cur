#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Signal Parser for Trading Signals
Handles various signal formats including market/now entries and percentage stops
"""

import re
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

@dataclass
class Signal:
    """Represents a parsed trading signal"""
    symbol: str
    direction: str  # LONG or SHORT
    entry: str     # Can be number, 'market', or 'now'
    target: float
    stop: float
    entry_numeric: Optional[float] = None
    stop_percentage: Optional[float] = None
    original_text: str = ""

class SignalParser:
    """Parser for trading signals from text files"""
    
    def __init__(self, default_stop_percentage: float = 3.0):
        self.default_stop_percentage = default_stop_percentage
        
    def parse_signal_text(self, text: str) -> Optional[Signal]:
        """Parse a single signal from text"""
        try:
            # Clean the text
            lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
            if len(lines) < 4:
                return None
                
            # First line should contain symbol and direction
            first_line = lines[0]
            symbol_match = re.match(r'^([A-Z0-9]+/[A-Z0-9]+)\s+(LONG|SHORT)$', first_line)
            if not symbol_match:
                return None
                
            symbol = symbol_match.group(1)
            direction = symbol_match.group(2)
            
            # Parse entry, target, and stop
            entry = None
            target = None
            stop = None
            
            for line in lines[1:]:
                if line.startswith('Entry:'):
                    entry = line.replace('Entry:', '').strip()
                elif line.startswith('Target:'):
                    target_str = line.replace('Target:', '').strip()
                    try:
                        target = float(target_str)
                    except ValueError:
                        return None
                elif line.startswith('Stop:'):
                    stop_str = line.replace('Stop:', '').strip()
                    stop = self._parse_stop(stop_str)
                    if stop is None:
                        return None
            
            if entry is None or target is None or stop is None:
                return None
                
            # Create signal object
            signal = Signal(
                symbol=symbol,
                direction=direction,
                entry=entry,
                target=target,
                stop=stop,
                original_text=text
            )
            
            # Set additional fields
            if entry.lower() in ['market', 'now']:
                signal.entry_numeric = None
            else:
                try:
                    signal.entry_numeric = float(entry)
                except ValueError:
                    return None
            
            # Set stop percentage if it's a percentage stop
            if signal.stop < 0:
                signal.stop_percentage = abs(signal.stop)
                    
            return signal
            
        except Exception as e:
            print(f"Error parsing signal: {e}")
            return None
    
    def _parse_stop(self, stop_str: str) -> Optional[float]:
        """Parse stop loss value, handling percentages"""
        stop_str = stop_str.strip()
        
        # Check if it's a percentage
        if '%' in stop_str:
            try:
                percentage = float(stop_str.replace('%', ''))
                # For percentage stops, we'll need entry price to calculate actual stop
                # For now, return the percentage as a negative number to indicate it's percentage
                return -percentage
            except ValueError:
                return None
        
        # Check if it's a numeric value
        try:
            return float(stop_str)
        except ValueError:
            return None
    
    def parse_file(self, filename: str) -> List[Signal]:
        """Parse all signals from a file"""
        signals = []
        
        if not os.path.exists(filename):
            print(f"File {filename} not found")
            return signals
            
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Split content into individual signals (separated by double newlines)
            signal_blocks = content.split('\n\n')
            
            for block in signal_blocks:
                if block.strip():
                    signal = self.parse_signal_text(block)
                    if signal:
                        signals.append(signal)
                    else:
                        print(f"Failed to parse signal block:\n{block}\n")
                        
        except Exception as e:
            print(f"Error reading file {filename}: {e}")
            
        return signals
    
    def calculate_stop_price(self, signal: Signal, entry_price: float) -> float:
        """Calculate actual stop price from percentage or absolute value"""
        if signal.stop < 0:  # Percentage stop
            percentage = abs(signal.stop)
            if signal.direction == 'LONG':
                return entry_price * (1 - percentage / 100)
            else:  # SHORT
                return entry_price * (1 + percentage / 100)
        else:  # Absolute stop
            return signal.stop
    
    def validate_signal(self, signal: Signal, entry_price: float = 1000.0) -> Dict[str, any]:
        """Validate a signal and return validation results"""
        result = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'calculated_stop': None
        }
        
        # Check if entry is valid
        if signal.entry.lower() not in ['market', 'now']:
            if signal.entry_numeric is None:
                result['valid'] = False
                result['errors'].append("Invalid entry price")
        
        # Check target vs entry
        if signal.entry_numeric:
            if signal.direction == 'LONG' and signal.target <= signal.entry_numeric:
                result['warnings'].append("Target should be above entry for LONG positions")
            elif signal.direction == 'SHORT' and signal.target >= signal.entry_numeric:
                result['warnings'].append("Target should be below entry for SHORT positions")
        
        # Calculate and validate stop
        if signal.stop < 0:  # Percentage stop
            calculated_stop = self.calculate_stop_price(signal, entry_price)
            result['calculated_stop'] = calculated_stop
            
            # Only validate stop vs entry if we have a numeric entry
            if signal.entry_numeric is not None:
                if signal.direction == 'LONG' and calculated_stop >= signal.entry_numeric:
                    result['warnings'].append("Stop loss should be below entry for LONG positions")
                elif signal.direction == 'SHORT' and calculated_stop <= signal.entry_numeric:
                    result['warnings'].append("Stop loss should be above entry for SHORT positions")
        else:  # Absolute stop
            # Only validate stop vs entry if we have a numeric entry
            if signal.entry_numeric is not None:
                if signal.direction == 'LONG' and signal.stop >= signal.entry_numeric:
                    result['warnings'].append("Stop loss should be below entry for LONG positions")
                elif signal.direction == 'SHORT' and signal.stop <= signal.entry_numeric:
                    result['warnings'].append("Stop loss should be below entry for SHORT positions")
        
        return result
    
    def test_parser(self, test_price: float = 1000.0) -> Dict[str, any]:
        """Test the parser with both signal files"""
        results = {
            'signals_txt': [],
            'newsignal_txt': [],
            'total_signals': 0,
            'successful_parses': 0,
            'failed_parses': 0,
            'validation_results': []
        }
        
        # Test signals.txt
        print("Testing signals.txt...")
        signals1 = self.parse_file('signals.txt')
        results['signals_txt'] = signals1
        results['total_signals'] += len(signals1)
        
        # Test newsignal.txt
        print("Testing newsignal.txt...")
        signals2 = self.parse_file('newsignal.txt')
        results['newsignal_txt'] = signals2
        results['total_signals'] += len(signals2)
        
        # Validate all signals
        all_signals = signals1 + signals2
        for signal in all_signals:
            validation = self.validate_signal(signal, test_price)
            results['validation_results'].append({
                'signal': signal,
                'validation': validation
            })
            
            if validation['valid']:
                results['successful_parses'] += 1
            else:
                results['failed_parses'] += 1
        
        return results

def main():
    """Main function to test the parser"""
    parser = SignalParser(default_stop_percentage=3.0)
    
    print("=== Signal Parser Test ===\n")
    
    # Test with a sample price
    test_price = 1000.0
    results = parser.test_parser(test_price)
    
    print(f"\n=== Test Results ===")
    print(f"Total signals found: {results['total_signals']}")
    print(f"Successfully parsed: {results['successful_parses']}")
    print(f"Failed to parse: {results['failed_parses']}")
    
    print(f"\n=== Detailed Results ===")
    for i, result in enumerate(results['validation_results']):
        signal = result['signal']
        validation = result['validation']
        
        print(f"\nSignal {i+1}: {signal.symbol} {signal.direction}")
        print(f"  Entry: {signal.entry}")
        print(f"  Target: {signal.target}")
        print(f"  Stop: {signal.stop}")
        
        if validation['calculated_stop']:
            print(f"  Calculated Stop: {validation['calculated_stop']:.2f}")
        
        if validation['errors']:
            print(f"  Errors: {', '.join(validation['errors'])}")
        
        if validation['warnings']:
            print(f"  Warnings: {', '.join(validation['warnings'])}")
        
        if validation['valid']:
            print(f"  Status: ✅ Valid")
        else:
            print(f"  Status: ❌ Invalid")
    
    # Calculate success rate
    if results['total_signals'] > 0:
        success_rate = (results['successful_parses'] / results['total_signals']) * 100
        print(f"\n=== Success Rate: {success_rate:.1f}% ===")
        
        if success_rate == 100:
            print("🎉 Parser is working perfectly! All signals parsed successfully.")
        else:
            print("⚠️  Some signals failed to parse. Check the errors above.")
    else:
        print("❌ No signals found to test.")

if __name__ == "__main__":
    main()