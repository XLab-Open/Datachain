## Testing

This project uses pytest for comprehensive testing. Here are the available test commands:

### Basic Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=datachain --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=datachain --cov-report=html
```

### Test Categories

```bash
# Run only unit tests (fast)
pytest -m "not integration and not slow"

# Run only integration tests
pytest -m integration

# Run only slow tests
pytest -m slow
```

### Using Makefile

For convenience, a Makefile is provided:

```bash
# Show all available commands
make help

# Install development dependencies
make install-dev

# Run all tests
make test

# Run tests with coverage
make test-cov

# Generate HTML coverage report
make test-html

# Run code formatting
make format

# Run linting checks
make lint

# Run type checking
make type-check

# Clean up generated files
make clean
```
### Test Coverage

The test suite covers:

- ✅ Basic registration and retrieval
- ✅ Decorator functionality
- ✅ Tag-based filtering
- ✅ Search functionality
- ✅ Instance creation
- ✅ Error handling
- ✅ Edge cases and boundary conditions
- ✅ Performance with large datasets
- ✅ Memory management
- ✅ Logging behavior
