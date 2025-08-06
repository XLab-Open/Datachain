<div align="center">

<img src="./docs/images/datachain.png" width="600" height="160">

<h2 align="center">AI model deployment based on embedded domain controller platforms</h2>


[<span style="font-size:20px;">**Architecture**</span>](./docs/framework.md)&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[<span style="font-size:20px;">**Documentation**</span>](https://liwuhen.cn/CVDeploy-2D)&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[<span style="font-size:20px;">**Blog**</span>](https://www.zhihu.com/column/c_1839603173800697856)&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[<span style="font-size:20px;">**Roadmap**</span>](./docs/roadmap.md)&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[<span style="font-size:20px;">**Slack**</span>](https://app.slack.com/client/T07U5CEEXCP/C07UKUA9TCJ)

<p align="right">
  🌐 <b>Language</b> | 语言：
  <a href="./docs/README.zh-CN.md">🇨🇳 中文</a>
</p>

---

![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg?style=for-the-badge)
![ARM Linux](https://img.shields.io/badge/ARM_Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![NVIDIA](https://img.shields.io/badge/NVIDIA-%2376B900.svg?style=for-the-badge&logo=nvidia&logoColor=white)
![Performance](https://img.shields.io/badge/Performance-Optimized-red?style=for-the-badge)
![GPU Accelerated](https://img.shields.io/badge/GPU-Accelerated-76B900?style=for-the-badge&logo=nvidia&logoColor=white)

The repository focuses on converting formats across multiple open-source datasets and offers serialization capabilities to unify data representation.
</div>

# Getting Started
Visit our documentation to learn more.
- [Installation](./docs/hpcdoc/source/getting_started/installation.md)
- [Quickstart](./docs/hpcdoc/source/getting_started/Quickstart.md)

# Performances
- Dataset:
    - pascal voc
        > The validation dataset is voc2012.
    - BDD100K
        > The validation dataset is BDD100K, which contains 70000 training samples and 10000 val samples.
    - nuscenes
        > The validation dataset is nuscenes-mini.
- Model: The deployed model is the 's' version of the YOLO multi-task network series.
- Quantize: Quantization was performed using NVIDIA's Post-Training Quantization (PTQ) method.

|srcData|DstData|cpu|
|:-:|:-:|:-:|
|voc|coco|-|
|nuImages|coco|-|
|BDD100K|coco|-|

# ![Contribute](https://img.shields.io/badge/how%20to%20contribute-project-brightgreen) Contributing
Welcome users to participate in these projects. Please refer to [CONTRIBUTING.md](./CONTRIBUTING.md) for the contributing guideline.We encourage you to join the effort and contribute feedback, ideas, and code. You can participate in Working Groups, Working Groups have most of their discussions on [Slack](https://app.slack.com/client/T07U5CEEXCP/C07UKUA9TCJ).

# ![TODO](https://img.shields.io/badge/how%20to%20contribute-project-brightgreen) TODO
- [ ] Add BDD100K
- [ ] Add API support for Caller

# References
- [Vllm: https://github.com/vllm-project/vllm](https://github.com/vllm-project/vllm)

# Datachain

A generic class registration factory for dynamic class management.

## Features

- **Dynamic Class Registration**: Register classes at runtime with metadata
- **Decorator Support**: Use `@factory.register_decorator()` for clean syntax
- **Tag-based Filtering**: Organize classes with tags for easy discovery
- **Search Functionality**: Search classes by name, description, or tags
- **Type Safety**: Full type hints and validation support
- **Comprehensive Testing**: Extensive test suite with pytest

## Installation

```bash
# Install production dependencies
pip install -e .

# Install development dependencies (includes pytest, linting tools, etc.)
pip install -e ".[dev]"
```

## Quick Start

```python
from datachain.core.registry import ClassRegistryFactory

# Create a factory
factory = ClassRegistryFactory("my_factory")


# Method 1: Direct registration
class CSVConverter:
    def __init__(self, delimiter=","):
        self.delimiter = delimiter


factory.register(
    name="csv",
    cls=CSVConverter,
    description="CSV format converter",
    tags=["format", "csv"],
)


# Method 2: Decorator registration
@factory.register_decorator("json", tags=["format", "json"])
class JSONConverter:
    def __init__(self, indent=2):
        self.indent = indent


# Use the factory
csv_instance = factory.create("csv", delimiter=";")
json_instance = factory.create("json", indent=4)

# Search and filter
format_converters = factory.list_by_tag("format")
search_results = factory.search("converter")
```

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

### Test Structure

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── core/
│   ├── test_registry.py     # Basic functionality tests
│   └── test_registry_advanced.py  # Advanced and edge case tests
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

## Development

### Code Quality

```bash
# Format code
make format

# Check code style
make lint

# Type checking
make type-check
```

### Pre-commit Hooks

The project includes pre-commit hooks for automatic code quality checks:

```bash
# Install pre-commit hooks
pre-commit install

# Run all hooks manually
pre-commit run --all-files
```

## API Reference

### ClassRegistryFactory

The main factory class for managing class registrations.

#### Methods

- `register(name, cls, description="", tags=None, metadata=None, override=False)` - Register a class
- `register_decorator(name=None, description=None, tags=None, metadata=None, override=False)` - Decorator for registration
- `get(name)` - Get a registered class
- `create(name, *args, **kwargs)` - Create an instance of a registered class
- `list_all()` - List all registered class names
- `list_by_tag(tag)` - List classes by tag
- `search(query, search_fields=None)` - Search classes
- `exists(name)` - Check if a class is registered
- `unregister(name)` - Unregister a class
- `clear()` - Clear all registrations

### ClassInfo

Data class containing information about a registered class.

#### Attributes

- `name` - The registration name
- `cls` - The registered class
- `description` - Class description
- `tags` - List of tags
- `metadata` - Additional metadata dictionary

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass: `make test`
6. Run code quality checks: `make lint && make type-check`
7. Submit a pull request

## License

MIT License - see LICENSE file for details.
