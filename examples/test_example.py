#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) XLab-Open. All rights reserved.

"""
Example usage of ClassRegistryFactory with pytest testing
"""

import pytest
from datachain.core.registry import ClassRegistryFactory


class TestRegistryExample:
    """Example test class showing how to use the registry"""

    @pytest.fixture
    def converter_factory(self):
        """Create a factory for data converters"""
        return ClassRegistryFactory("converters")

    def test_basic_registration(self, converter_factory):
        """Example: Basic class registration"""
        # Define a converter class
        class CSVConverter:
            def __init__(self, delimiter=","):
                self.delimiter = delimiter

            def convert(self, data):
                return f"CSV{self.delimiter}{data}"

        # Register the class
        success = converter_factory.register(
            name="csv",
            cls=CSVConverter,
            description="CSV format converter",
            tags=["format", "csv", "converter"]
        )
        assert success is True

        # Create an instance
        converter = converter_factory.create("csv", delimiter=";")
        assert converter is not None
        assert converter.convert("hello") == "CSV;hello"

    def test_decorator_registration(self, converter_factory):
        """Example: Using decorator for registration"""
        @converter_factory.register_decorator("json", tags=["format", "json"])
        class JSONConverter:
            def __init__(self, indent=2):
                self.indent = indent

            def convert(self, data):
                return f"JSON{self.indent}{data}"

        # The class is automatically registered
        assert converter_factory.exists("json")

        # Create instance
        converter = converter_factory.create("json", indent=4)
        assert converter.convert("world") == "JSON4world"

    def test_search_and_filtering(self, converter_factory):
        """Example: Searching and filtering classes"""
        # Register multiple converters
        class XMLConverter:
            def convert(self, data):
                return f"XML: {data}"

        class YAMLConverter:
            def convert(self, data):
                return f"YAML: {data}"

        converter_factory.register("xml", XMLConverter, tags=["format", "xml"])
        converter_factory.register("yaml", YAMLConverter, tags=["format", "yaml"])

        # Search by tag
        format_converters = converter_factory.list_by_tag("format")
        assert len(format_converters) == 2
        assert "xml" in format_converters
        assert "yaml" in format_converters

        # Search by name
        results = converter_factory.search("xml")
        assert "xml" in results

        # Search by tag (using search_fields parameter)
        results = converter_factory.search("format", search_fields=["tags"])
        assert len(results) == 2
        assert "xml" in results
        assert "yaml" in results

    def test_metadata_and_info(self, converter_factory):
        """Example: Working with metadata and class information"""
        class AdvancedConverter:
            """Advanced data converter with metadata"""
            def __init__(self, version="1.0"):
                self.version = version

            def convert(self, data):
                return f"Advanced{self.version}: {data}"

        # Register with metadata
        converter_factory.register(
            name="advanced",
            cls=AdvancedConverter,
            description="Advanced converter with versioning",
            tags=["advanced", "versioned"],
            metadata={
                "version": "1.0.0",
                "author": "Example Author",
                "features": ["versioning", "logging"]
            }
        )

        # Get class information
        info = converter_factory.get_info("advanced")
        assert info.name == "advanced"
        assert info.metadata["version"] == "1.0.0"
        assert info.metadata["author"] == "Example Author"
        assert "advanced" in info.tags

        # Get summary
        summary = converter_factory.get_summary()
        assert summary["total_classes"] >= 1
        assert "advanced" in summary["unique_tags"]


if __name__ == "__main__":
    # Run the example tests
    pytest.main([__file__, "-v"])
