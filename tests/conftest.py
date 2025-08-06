#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) XLab-Open. All rights reserved.

"""
Pytest configuration and shared fixtures
"""

import pytest
from datachain.core.registry import ClassRegistryFactory


@pytest.fixture(scope="session")
def session_factory():
    """Session-scoped factory for tests that need persistence across test modules"""
    return ClassRegistryFactory("session_test")


@pytest.fixture
def sample_classes():
    """Provide sample classes for testing"""
    class BaseConverter:
        def __init__(self, name="base"):
            self.name = name

        def convert(self, data):
            return f"{self.name}: {data}"

    class CSVConverter(BaseConverter):
        def __init__(self, delimiter=",", **kwargs):
            super().__init__(**kwargs)
            self.delimiter = delimiter

        def convert(self, data):
            return f"CSV{self.delimiter}{data}"

    class JSONConverter(BaseConverter):
        def __init__(self, indent=2, **kwargs):
            super().__init__(**kwargs)
            self.indent = indent

        def convert(self, data):
            return f"JSON{self.indent}{data}"

    class XMLConverter(BaseConverter):
        def convert(self, data):
            return f"XML: {data}"

    return {
        "base": BaseConverter,
        "csv": CSVConverter,
        "json": JSONConverter,
        "xml": XMLConverter
    }


@pytest.fixture
def populated_factory(sample_classes):
    """Factory with pre-populated classes for testing"""
    factory = ClassRegistryFactory("populated_test")

    # Register classes with different configurations
    factory.register(
        name="csv",
        cls=sample_classes["csv"],
        description="CSV format converter",
        tags=["format", "csv", "converter"],
        metadata={"version": "1.0", "author": "test"}
    )

    factory.register(
        name="json",
        cls=sample_classes["json"],
        description="JSON format converter",
        tags=["format", "json", "converter"],
        metadata={"version": "1.0", "author": "test"}
    )

    factory.register(
        name="xml",
        cls=sample_classes["xml"],
        description="XML format converter",
        tags=["format", "xml", "converter"],
        metadata={"version": "1.0", "author": "test"}
    )

    return factory


@pytest.fixture
def mock_logger(mocker):
    """Mock logger for testing logging behavior"""
    return mocker.patch('datachain.core.registry.logging.getLogger')


# Custom markers
def pytest_configure(config):
    """Configure custom pytest markers"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )


# Test collection hooks
def pytest_collection_modifyitems(config, items):
    """Modify test collection to add default markers"""
    for item in items:
        # Add unit marker to tests that don't have any marker
        if not any(item.iter_markers()):
            item.add_marker(pytest.mark.unit)
