# Signal Parser for Trading Signals

A robust Python parser designed to process trading signals from text files with support for various entry types, stop loss formats, and comprehensive validation.

## Features

- **Flexible Entry Types**: Supports numeric entries, "market", and "now" entries
- **Stop Loss Handling**: Processes both absolute values and percentage-based stops
- **Comprehensive Validation**: Validates signal logic and calculates risk metrics
- **Robust Parsing**: Handles edge cases and malformed signals gracefully
- **Multiple File Support**: Can process multiple signal files simultaneously

## Supported Signal Formats

### Basic Format
```
SYMBOL DIRECTION
Entry: [price|market|now]
Target: [price]
Stop: [price|percentage%]
```

### Examples

#### Numeric Entry with Absolute Stop
```
BTC/USDT LONG
Entry: 45000
Target: 48000
Stop: 44000
```

#### Market Entry with Percentage Stop
```
ETH/USDT SHORT
Entry: market
Target: 3000
Stop: 3%
```

#### Now Entry with Percentage Stop
```
ADA/USDT LONG
Entry: now
Target: 0.55
Stop: 2.5%
```

## Installation

No external dependencies required. The parser uses only Python standard library.

```bash
# Clone or download the files
# Ensure Python 3.6+ is installed
python3 signal_parser.py
```

## Usage

### Basic Usage

```python
from signal_parser import SignalParser

# Initialize parser with default 3% stop loss
parser = SignalParser(default_stop_percentage=3.0)

# Parse a single signal
signal_text = """
BTC/USDT LONG
Entry: 45000
Target: 48000
Stop: 3%
"""
signal = parser.parse_signal_text(signal_text)

# Parse a file
signals = parser.parse_file('signals.txt')

# Validate signals
for signal in signals:
    validation = parser.validate_signal(signal, entry_price=45000)
    if validation['valid']:
        print(f"✅ {signal.symbol} is valid")
    else:
        print(f"❌ {signal.symbol} has errors: {validation['errors']}")
```

### Command Line Usage

```bash
# Test the parser with sample files
python3 signal_parser.py

# Run edge case tests
python3 test_edge_cases.py

# Run real scenario tests
python3 test_real_scenarios.py
```

## Signal Validation

The parser validates:

- **Symbol Format**: Must be in format `XXX/YYY` (e.g., `BTC/USDT`)
- **Direction**: Must be `LONG` or `SHORT`
- **Entry**: Must be numeric, "market", or "now"
- **Target**: Must be numeric
- **Stop**: Must be numeric or percentage (e.g., "3%")

### Validation Rules

- **LONG Positions**: Target should be above entry, stop should be below entry
- **SHORT Positions**: Target should be below entry, stop should be above entry
- **Percentage Stops**: Automatically calculated based on entry price
- **Market/Now Entries**: Entry validation skipped (requires external price data)

## File Structure

```
├── signal_parser.py      # Main parser implementation
├── signals.txt          # Sample signals file
├── newsignal.txt        # Additional sample signals
├── test_edge_cases.py   # Edge case testing
├── test_real_scenarios.py # Real trading scenario tests
├── requirements.txt     # Dependencies (none required)
└── README.md           # This file
```

## Sample Output

```
=== Signal Parser Test ===

Testing signals.txt...
Testing newsignal.txt...

=== Test Results ===
Total signals found: 25
Successfully parsed: 25
Failed to parse: 0

=== Success Rate: 100.0% ===
🎉 Parser is working perfectly! All signals parsed successfully.
```

## Error Handling

The parser gracefully handles:

- **Missing Fields**: Signals with incomplete information are rejected
- **Invalid Formats**: Malformed symbols, directions, or values are caught
- **Type Errors**: Non-numeric values where numbers are expected
- **Edge Cases**: Empty signals, whitespace-only content, etc.

## Performance

- **Parsing Speed**: Processes hundreds of signals per second
- **Memory Usage**: Minimal memory footprint
- **Scalability**: Handles large files efficiently

## Testing

The project includes comprehensive testing:

1. **Basic Parser Test**: `python3 signal_parser.py`
2. **Edge Case Testing**: `python3 test_edge_cases.py`
3. **Real Scenarios**: `python3 test_real_scenarios.py`

All tests should pass with 100% success rate.

## Contributing

To add new features or fix issues:

1. Ensure all tests pass
2. Add new test cases for new functionality
3. Maintain backward compatibility
4. Update documentation

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please check the test files for examples or review the parser implementation in `signal_parser.py`.