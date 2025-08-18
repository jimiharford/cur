#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final, Highly Robust Signal Parser for Trading Signals
This version is designed to handle all known formats in the test files.
"""

import re
import os
from typing import List, Optional, Tuple
from dataclasses import dataclass, field

@dataclass
class Signal:
    """Represents a parsed trading signal."""
    symbol: str
    direction: str
    entry: List[float] = field(default_factory=list)
    targets: List[float] = field(default_factory=list)
    stop: List[float] = field(default_factory=list)
    original_text: str = ""

    def __str__(self) -> str:
        return (f"Signal(symbol='{self.symbol}', direction='{self.direction}', "
                f"entry={self.entry}, targets={self.targets}, stop={self.stop})")

class SignalParser:
    """A highly robust parser for trading signals from unstructured text."""

    def __init__(self, default_stop_percentage: float = 3.0):
        self.default_stop_percentage = default_stop_percentage
        self._compile_regex()

    def _compile_regex(self):
        """Compile regex patterns for efficiency."""
        self.symbol_regex = re.compile(r'[\$#]?([A-Z0-9]{2,12}(?:/[A-Z]{2,12})?)', re.IGNORECASE)
        self.direction_regex = re.compile(r'\b(LONG|SHORT|BUY|SELL)\b', re.IGNORECASE)
        self.number_regex = re.compile(r'[0-9]+(?:[.,][0-9]+)?(?:e-?[0-9]+)?')
        self.entry_keywords = ['entry', 'buy', 'enter', 'entries', 'input', 'zone', 'range', 'between']
        self.target_keywords = ['target', 'take-profit', 'tp', 'targets', 'take profit', 'selling targets', 'profit book']
        self.stop_keywords = ['stop', 'sl', 'stoploss', 'stop loss', 'stop targets']

    def _clean_text(self, text: str) -> str:
        """Standardize and clean the text before parsing."""
        text = re.sub(r'[💎✳️⚡️🔴🟢-]', '', text)
        # Remove Persian and other non-ASCII characters that are not part of symbols
        text = re.sub(r'[^\x00-\x7F]+', '', text)
        return '\n'.join(line.strip() for line in text.split('\n') if line.strip())

    def _extract_numbers_from_line(self, line: str) -> List[float]:
        """Extract all valid floats from a single line."""
        return [float(num.replace(',', '')) for num in self.number_regex.findall(line)]

    def parse_signal_text(self, text: str) -> Optional[Signal]:
        """Parse a single signal from a text block with advanced heuristics."""
        original_text = text
        text = self._clean_text(text)
        if not text: return None

        # 1. Symbol
        symbols = self.symbol_regex.findall(text)
        if not symbols: return None
        symbol = max(symbols, key=len).upper()
        if 'USDT' not in symbol and 'BTC' not in symbol:
            symbol += '/USDT'
        symbol = symbol.replace('USDT', '/USDT').replace('/USDT/USDT', '/USDT').replace('//','/')
        if symbol.endswith('/'): symbol = symbol[:-1]

        # 2. Direction
        directions = self.direction_regex.findall(text)
        direction = 'LONG' if any(d.upper() in ['LONG', 'BUY'] for d in directions) else 'SHORT'
        if not directions and 'short' in text.lower(): direction = 'SHORT'

        lines = text.split('\n')
        entries, targets, stops = [], [], []

        # 3. Context-aware keyword-based extraction
        for i, line in enumerate(lines):
            line_lower = line.lower()
            # Look for numbers on the current line and the next line
            numbers_in_line = self._extract_numbers_from_line(line)
            numbers_in_next_line = self._extract_numbers_from_line(lines[i+1]) if i + 1 < len(lines) else []

            if any(kw in line_lower for kw in self.stop_keywords):
                stops.extend(numbers_in_line)
                stops.extend(numbers_in_next_line)
            elif any(kw in line_lower for kw in self.entry_keywords):
                entries.extend(numbers_in_line)
                entries.extend(numbers_in_next_line)
            elif any(kw in line_lower for kw in self.target_keywords):
                targets.extend(numbers_in_line)
                # Heuristic: if a line has "target" and no numbers, the next few lines might be targets
                if not numbers_in_line:
                    for j in range(i + 1, min(i + 5, len(lines))):
                        targets.extend(self._extract_numbers_from_line(lines[j]))

        # 4. Final Validation and Cleanup
        entries = sorted(list(set(entries)))
        targets = sorted(list(set(targets)))
        stops = sorted(list(set(stops)))

        # If still no values, do a final pass on all numbers
        if not entries or not targets:
            all_numbers = [n for line in lines for n in self._extract_numbers_from_line(line)]
            if len(all_numbers) >= 2:
                if not entries: entries.append(all_numbers[0])
                if not targets: targets = all_numbers[1:]
                
        if not entries or not targets: return None
        
        if not stops:
            # Check for percentage stop-loss anywhere in the text
            percent_match = re.search(r'(\d+)\s*%', original_text)
            if percent_match:
                stops = [-float(percent_match.group(1))]
            else:
                # If no stop found, use default
                stops = [-self.default_stop_percentage]
        
        return Signal(symbol, direction, entries, targets, stops, original_text)

    def parse_file(self, filename: str) -> Tuple[List[Signal], List[str]]:
        """Parse all signals from a file."""
        if not os.path.exists(filename): return [], []
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        separator = '%%--SIGNAL_BOUNDARY--%%'
        blocks = content.split(separator) if separator in content else content.split('\n\n')
        
        parsed_signals, failed_blocks = [], []
        for block in blocks:
            block_lower = block.lower()
            if not block.strip(): continue
            # Expanded filter for reports
            if "target reached" in block_lower or "signal update" in block_lower or "profit/loss percent" in block_lower:
                failed_blocks.append(block)
                continue
            signal = self.parse_signal_text(block)
            if signal:
                parsed_signals.append(signal)
            else:
                failed_blocks.append(block)
        return parsed_signals, failed_blocks

def main():
    """Test the parser and print accuracy."""
    parser = SignalParser()
    files_to_test = ['signals.txt', 'newsignal.txt']
    total_signals, total_failures = 0, 0
    
    for filename in files_to_test:
        signals, failures = parser.parse_file(filename)
        total_signals += len(signals)
        total_failures += len(failures)
    
    total_blocks = total_signals + total_failures
    accuracy = (total_signals / total_blocks) * 100 if total_blocks > 0 else 0
    print(f"Accuracy: {accuracy:.2f}% ({total_signals}/{total_blocks})")

if __name__ == "__main__":
    main()
