#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) XLab-Open. All rights reserved.

import pytest
from datachain.core.registry import ClassRegistryFactory, ClassInfo


class TestClassRegistryFactory:
    """Test cases for ClassRegistryFactory"""

    @pytest.fixture
    def factory(self):
        """Create a fresh factory instance for each test"""
        return ClassRegistryFactory("test_factory")

    @pytest.fixture
    def sample_class(self):
        """Sample class for testing"""
        class SampleClass:
            def __init__(self, value=0):
                self.value = value

            def get_value(self):
                return self.value

        return SampleClass

    def test_factory_initialization(self, factory):
        """Test factory initialization"""
        assert factory.name == "test_factory"
        assert factory.count() == 0
        assert factory.list_all() == []

    def test_register_class_success(self, factory, sample_class):
        """Test successful class registration"""
        result = factory.register(
            name="sample",
            cls=sample_class,
            description="A sample class",
            tags=["test", "sample"],
            metadata={"version": "1.0"}
        )

        assert result is True
        assert factory.exists("sample")
        assert factory.count() == 1
        assert "sample" in factory.list_all()

    def test_register_class_duplicate(self, factory, sample_class):
        """Test duplicate registration without override"""
        factory.register("sample", sample_class)
        result = factory.register("sample", sample_class)

        assert result is False  # Should not override

    def test_register_class_with_override(self, factory, sample_class):
        """Test registration with override"""
        factory.register("sample", sample_class)
        result = factory.register("sample", sample_class, override=True)

        assert result is True

    def test_register_invalid_class(self, factory):
        """Test registering non-class objects"""
        result = factory.register("invalid", "not_a_class")
        assert result is False

    def test_get_registered_class(self, factory, sample_class):
        """Test getting registered class"""
        factory.register("sample", sample_class)
        retrieved_class = factory.get("sample")

        assert retrieved_class == sample_class

    def test_get_nonexistent_class(self, factory):
        """Test getting non-existent class"""
        result = factory.get("nonexistent")
        assert result is None

    def test_get_class_info(self, factory, sample_class):
        """Test getting class information"""
        factory.register(
            name="sample",
            cls=sample_class,
            description="Test description",
            tags=["test"],
            metadata={"key": "value"}
        )

        info = factory.get_info("sample")
        assert isinstance(info, ClassInfo)
        assert info.name == "sample"
        assert info.cls == sample_class
        assert info.description == "Test description"
        assert info.tags == ["test"]
        assert info.metadata == {"key": "value"}

    def test_create_instance(self, factory, sample_class):
        """Test creating class instances"""
        factory.register("sample", sample_class)
        instance = factory.create("sample", value=42)

        assert instance is not None
        assert instance.value == 42
        assert instance.get_value() == 42

    def test_create_nonexistent_instance(self, factory):
        """Test creating instance of non-existent class"""
        instance = factory.create("nonexistent")
        assert instance is None

    def test_unregister_class(self, factory, sample_class):
        """Test unregistering a class"""
        factory.register("sample", sample_class)
        assert factory.exists("sample")

        result = factory.unregister("sample")
        assert result is True
        assert not factory.exists("sample")
        assert factory.count() == 0

    def test_unregister_nonexistent_class(self, factory):
        """Test unregistering non-existent class"""
        result = factory.unregister("nonexistent")
        assert result is False

    def test_list_by_tag(self, factory, sample_class):
        """Test listing classes by tag"""
        factory.register("sample1", sample_class, tags=["tag1", "common"])
        factory.register("sample2", sample_class, tags=["tag2", "common"])
        factory.register("sample3", sample_class, tags=["tag3"])

        common_classes = factory.list_by_tag("common")
        assert len(common_classes) == 2
        assert "sample1" in common_classes
        assert "sample2" in common_classes

    def test_list_by_type(self, factory):
        """Test listing classes by base type"""
        class BaseClass:
            pass

        class SubClass1(BaseClass):
            pass

        class SubClass2(BaseClass):
            pass

        class UnrelatedClass:
            pass

        factory.register("sub1", SubClass1)
        factory.register("sub2", SubClass2)
        factory.register("unrelated", UnrelatedClass)

        base_classes = factory.list_by_type(BaseClass)
        assert len(base_classes) == 2
        assert "sub1" in base_classes
        assert "sub2" in base_classes

    def test_search_functionality(self, factory, sample_class):
        """Test search functionality"""
        factory.register("test_class", sample_class, description="A test class for testing")
        factory.register("other_class", sample_class, description="Another class")

        # Search by name
        results = factory.search("test")
        assert "test_class" in results

        # Search by description
        results = factory.search("testing")
        assert "test_class" in results

        # Search by tag
        factory.register("tagged_class", sample_class, tags=["special", "test"])
        results = factory.search("special", search_fields=["tags"])
        assert "tagged_class" in results

    def test_clear_registry(self, factory, sample_class):
        """Test clearing the registry"""
        factory.register("sample1", sample_class)
        factory.register("sample2", sample_class)
        assert factory.count() == 2

        factory.clear()
        assert factory.count() == 0
        assert factory.list_all() == []

    def test_get_summary(self, factory, sample_class):
        """Test getting registry summary"""
        factory.register("sample1", sample_class, tags=["tag1", "tag2"])
        factory.register("sample2", sample_class, tags=["tag2", "tag3"])

        summary = factory.get_summary()
        assert summary["name"] == "test_factory"
        assert summary["total_classes"] == 2
        assert "tag1" in summary["unique_tags"]
        assert "tag2" in summary["unique_tags"]
        assert "tag3" in summary["unique_tags"]
        assert "sample1" in summary["class_names"]
        assert "sample2" in summary["class_names"]

    def test_validate_registration(self, factory, sample_class):
        """Test registration validation"""
        # Valid registration
        result = factory.validate_registration("valid", sample_class)
        assert result is True

        # Invalid name
        result = factory.validate_registration("", sample_class)
        assert result is False

        # Invalid class
        result = factory.validate_registration("invalid", "not_a_class")
        assert result is False

    def test_validate_registration_with_custom_validator(self, factory, sample_class):
        """Test registration validation with custom validator"""
        def custom_validator(name, cls):
            return name.startswith("valid_")

        # Valid with custom validator
        result = factory.validate_registration("valid_name", sample_class, custom_validator)
        assert result is True

        # Invalid with custom validator
        result = factory.validate_registration("invalid_name", sample_class, custom_validator)
        assert result is False


class TestClassRegistryFactoryDecorator:
    """Test cases for decorator functionality"""

    @pytest.fixture
    def factory(self):
        """Create a fresh factory instance for each test"""
        return ClassRegistryFactory("decorator_test")

    def test_decorator_registration(self, factory):
        """Test decorator registration"""
        @factory.register_decorator("decorated_class")
        class DecoratedClass:
            def __init__(self, value=0):
                self.value = value

        assert factory.exists("decorated_class")
        assert factory.get("decorated_class") == DecoratedClass

    def test_decorator_with_description(self, factory):
        """Test decorator with description"""
        @factory.register_decorator("described_class", description="A described class")
        class DescribedClass:
            """This is a docstring"""
            pass

        info = factory.get_info("described_class")
        assert info.description == "A described class"

    def test_decorator_without_description_uses_docstring(self, factory):
        """Test decorator uses docstring when no description provided"""
        @factory.register_decorator("docstring_class")
        class DocstringClass:
            """This is the docstring description"""
            pass

        info = factory.get_info("docstring_class")
        assert info.description == "This is the docstring description"

    def test_decorator_with_tags(self, factory):
        """Test decorator with tags"""
        @factory.register_decorator("tagged_class", tags=["tag1", "tag2"])
        class TaggedClass:
            pass

        info = factory.get_info("tagged_class")
        assert "tag1" in info.tags
        assert "tag2" in info.tags

    def test_decorator_with_metadata(self, factory):
        """Test decorator with metadata"""
        @factory.register_decorator(
            "metadata_class",
            metadata={"version": "1.0", "author": "test"}
        )
        class MetadataClass:
            pass

        info = factory.get_info("metadata_class")
        assert info.metadata["version"] == "1.0"
        assert info.metadata["author"] == "test"

    def test_decorator_returns_original_class(self, factory):
        """Test that decorator returns the original class"""
        @factory.register_decorator("return_test")
        class ReturnTestClass:
            def method(self):
                return "test"

        # The class should still be usable
        instance = ReturnTestClass()
        assert instance.method() == "test"
        assert factory.exists("return_test")


class TestClassInfo:
    """Test cases for ClassInfo dataclass"""

    def test_class_info_initialization(self):
        """Test ClassInfo initialization"""
        class TestClass:
            pass

        info = ClassInfo(
            name="test",
            cls=TestClass,
            description="Test description",
            tags=["tag1", "tag2"],
            metadata={"key": "value"}
        )

        assert info.name == "test"
        assert info.cls == TestClass
        assert info.description == "Test description"
        assert info.tags == ["tag1", "tag2"]
        assert info.metadata == {"key": "value"}

    def test_class_info_default_values(self):
        """Test ClassInfo default values"""
        class TestClass:
            pass

        info = ClassInfo(name="test", cls=TestClass)

        assert info.description == ""
        assert info.tags == []
        assert info.metadata == {}

    def test_class_info_post_init(self):
        """Test ClassInfo post_init behavior"""
        class TestClass:
            pass

        # Test with None values
        info = ClassInfo(name="test", cls=TestClass, tags=None, metadata=None)

        assert info.tags == []
        assert info.metadata == {}


@pytest.mark.integration
class TestClassRegistryFactoryIntegration:
    """Integration tests for ClassRegistryFactory"""

    def test_complete_workflow(self):
        """Test complete workflow from registration to usage"""
        factory = ClassRegistryFactory("workflow_test")

        # Register classes using different methods
        class CSVConverter:
            def __init__(self, delimiter=","):
                self.delimiter = delimiter

            def convert(self, data):
                return f"CSV{self.delimiter}{data}"

        @factory.register_decorator("json", tags=["format", "json"])
        class JSONConverter:
            def __init__(self, indent=2):
                self.indent = indent

            def convert(self, data):
                return f"JSON{self.indent}{data}"

        # Direct registration
        factory.register(
            name="csv",
            cls=CSVConverter,
            description="CSV format converter",
            tags=["format", "csv"]
        )

        # Test all functionality
        assert factory.count() == 2
        assert factory.exists("csv")
        assert factory.exists("json")

        # Create instances
        csv_instance = factory.create("csv", delimiter=";")
        json_instance = factory.create("json", indent=4)

        assert csv_instance.convert("test") == "CSV;test"
        assert json_instance.convert("test") == "JSON4test"

        # Search and filter
        format_converters = factory.list_by_tag("format")
        assert len(format_converters) == 2

        search_results = factory.search("converter")
        assert len(search_results) == 1

        # Summary
        summary = factory.get_summary()
        assert summary["total_classes"] == 2
        assert "format" in summary["unique_tags"]
