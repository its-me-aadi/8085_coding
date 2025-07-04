# Testing Documentation

This document describes the comprehensive test suite for the media-manipulator service.

## Test Overview

The test suite includes **75 tests** covering all aspects of the service:

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test end-to-end workflows and component interactions
- **Edge Cases**: Handle invalid inputs, error conditions, and boundary cases

## Test Statistics

```
✅ 75 tests total
✅ 100% pass rate  
✅ 0.18s execution time
✅ All components covered
```

## Test Structure

```
tests/
├── conftest.py                    # Pytest fixtures and configuration
├── unit/                          # Unit tests (isolated component testing)
│   ├── test_command.py            # Command data structure tests
│   ├── test_interpreter.py        # Request parsing and validation tests
│   ├── test_processor.py          # Command processing orchestration tests
│   ├── test_strategies.py         # Individual strategy implementation tests
│   └── test_strategy_factory.py   # Strategy selection logic tests
└── integration/                   # Integration tests (end-to-end workflows)
    └── test_api.py                # Main API entry point tests
```

## Running Tests

### Quick Start

```bash
# Run all tests
python3 -m pytest tests/ -v

# Or use the test runner script
python3 run_tests.py all
```

### Test Categories

```bash
# Unit tests only
python3 run_tests.py unit

# Integration tests only  
python3 run_tests.py integration

# All tests with coverage
python3 run_tests.py all --coverage
```

### Manual Pytest Commands

```bash
# Verbose output with detailed results
python3 -m pytest tests/ -v

# Run specific test file
python3 -m pytest tests/unit/test_command.py -v

# Run specific test method
python3 -m pytest tests/unit/test_command.py::TestCommand::test_get_strategy_key -v

# Run tests with coverage report
python3 -m pytest tests/ --cov=video_editor --cov-report=html

# Run tests and stop on first failure
python3 -m pytest tests/ -x

# Run tests with minimal output
python3 -m pytest tests/ -q
```

## Test Coverage

### Component Coverage

| Component | Tests | Coverage |
|-----------|-------|----------|
| Command | 9 tests | ✅ Complete |
| Interpreter | 13 tests | ✅ Complete |
| Processor | 8 tests | ✅ Complete |
| Strategies | 20 tests | ✅ Complete |
| Strategy Factory | 10 tests | ✅ Complete |
| API Integration | 15 tests | ✅ Complete |

### Feature Coverage

**✅ Supported Operations**
- Text + Text addition (concatenation)
- Text + Video overlay (watermarking)
- Video + Audio overlay
- Video + Video concatenation
- Audio + Audio concatenation/mixing

**✅ Error Handling**
- Invalid request structure
- Missing required fields
- Unsupported operation combinations
- Strategy execution failures
- Exception handling throughout the pipeline

**✅ Edge Cases**
- Empty text values
- Special characters (Unicode, symbols)
- Multiple request independence
- Performance timing validation

## Test Types

### Unit Tests (60 tests)

**Command Tests (9 tests)**
- Object creation and data access
- Strategy key generation
- String representation
- Missing field handling

**Interpreter Tests (13 tests)**
- Valid request parsing
- Request validation
- Error handling for invalid inputs
- All supported operations validation

**Processor Tests (8 tests)**
- Command processing orchestration
- Strategy selection and execution
- Error handling and recovery
- Mock testing for failure scenarios

**Strategy Tests (20 tests)**
- Individual strategy execution
- Support validation for different command types
- Result formatting and metadata generation
- Base strategy functionality

**Strategy Factory Tests (10 tests)**
- Strategy registration and retrieval
- Priority-based strategy selection
- Unsupported combination handling
- Dynamic strategy registration

### Integration Tests (15 tests)

**End-to-End API Tests**
- Complete workflow testing from JSON input to final result
- All supported operation combinations
- Performance and timing validation
- Multiple request independence
- Real-world scenarios with special characters

## Test Fixtures

Common test data is provided through pytest fixtures in `conftest.py`:

```python
@pytest.fixture
def sample_text_add_request():
    return {
        "operation": "add",
        "left": {"type": "text", "value": "Hello"},
        "right": {"type": "text", "value": " World"}
    }
```

Available fixtures:
- `sample_text_add_request`
- `sample_text_overlay_request` 
- `sample_video_audio_overlay_request`
- `invalid_request_missing_field`
- `invalid_request_bad_operation`
- `sample_command`
- `interpreter`
- `processor`
- `unsupported_command`

## Mocking and Test Isolation

Tests use Python's `unittest.mock` for:
- **Strategy execution simulation**: Testing processor behavior without actual media processing
- **Component isolation**: Testing individual components without dependencies
- **Failure scenario testing**: Simulating errors and exceptions
- **External dependency mocking**: Avoiding real file system operations

## Test Configuration

**pytest.ini** provides standardized configuration:
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers --strict-config --disable-warnings
```

## Continuous Integration

The test suite is designed for CI/CD integration:

```bash
# CI command that fails on any test failure
python3 -m pytest tests/ --tb=short -x

# Generate JUnit XML for CI reporting
python3 -m pytest tests/ --junitxml=test-results.xml
```

## Adding New Tests

### For New Strategies

1. Add strategy tests to `tests/unit/test_strategies.py`
2. Test both `supports()` and `execute()` methods
3. Include positive and negative test cases
4. Update strategy factory tests if needed

### For New Operations

1. Add unit tests for new components
2. Add integration tests for end-to-end workflows
3. Update fixtures in `conftest.py` if needed
4. Test error handling scenarios

### Test Naming Convention

```python
def test_[component]_[scenario]_[expected_outcome]():
    """Clear description of what is being tested"""
    # Arrange
    # Act  
    # Assert
```

## Performance Testing

Basic performance validation is included:
- Tests ensure processing completes within reasonable time limits
- Timing information is logged for monitoring
- Tests validate that the service remains responsive

## Test Data

Tests use:
- **Mock data**: Simulated file paths and content
- **Sample requests**: Realistic JSON payloads
- **Edge case inputs**: Empty strings, special characters, invalid structures
- **Unicode support**: Emoji and international characters

## Debugging Tests

```bash
# Run with debugging output
python3 -m pytest tests/ -v -s

# Run specific failing test with full traceback
python3 -m pytest tests/unit/test_command.py::TestCommand::test_get_strategy_key -vv --tb=long

# Enter debugger on failure
python3 -m pytest tests/ --pdb
```

## Future Test Enhancements

- **Performance benchmarking**: Detailed timing and memory usage tests
- **Load testing**: Multiple concurrent request handling
- **Real media testing**: Integration with actual media files
- **Property-based testing**: Using Hypothesis for more comprehensive input testing
- **Contract testing**: API contract validation

---

*The test suite ensures the media-manipulator service is robust, reliable, and ready for production use.*