#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) XLab-Open. All rights reserved.

"""
Advanced test cases for ClassRegistryFactory
"""

import pytest
from datachain.core.registry import ClassRegistryFactory, ClassInfo


class TestClassRegistryFactoryAdvanced:
    """Advanced test cases for ClassRegistryFactory"""

    @pytest.fixture
    def factory(self):
        return ClassRegistryFactory("advanced_test")

    def test_registration_with_empty_strings(self, factory):
        """Test registration with empty strings and edge cases"""
        class TestClass:
            pass

        # Empty name should be allowed (current implementation doesn't validate this)
        result = factory.register("", TestClass)
        assert result is True

        # Whitespace-only name should be allowed
        result = factory.register("   ", TestClass)
        assert result is True

        # Empty description should be allowed
        result = factory.register("test", TestClass, description="")
        assert result is True

    def test_registration_with_special_characters(self, factory):
        """Test registration with special characters in names and descriptions"""
        class TestClass:
            pass

        # Special characters in name
        result = factory.register("test-class_123", TestClass)
        assert result is True

        # Special characters in description
        result = factory.register("test2", TestClass, description="Test with émojis 🚀 and symbols @#$%")
        assert result is True

        info = factory.get_info("test2")
        assert "émojis" in info.description
        assert "🚀" in info.description

    def test_large_number_of_registrations(self, factory):
        """Test performance with large number of registrations"""
        class TestClass:
            pass

        # Register many classes
        for i in range(1000):
            factory.register(f"class_{i}", TestClass, tags=[f"tag_{i % 10}"])

        assert factory.count() == 1000

        # Test search performance
        results = factory.search("class_500")
        assert "class_500" in results

        # Test tag filtering performance
        results = factory.list_by_tag("tag_5")
        assert len(results) == 100  # 1000 / 10 tags

    def test_nested_class_registration(self, factory):
        """Test registration of nested classes"""
        class OuterClass:
            class InnerClass:
                def __init__(self, value=0):
                    self.value = value

        # Register nested class
        result = factory.register("inner", OuterClass.InnerClass)
        assert result is True

        # Create instance
        instance = factory.create("inner", value=42)
        assert instance.value == 42

    def test_abstract_base_class_registration(self, factory):
        """Test registration of abstract base classes"""
        from abc import ABC, abstractmethod

        class AbstractConverter(ABC):
            @abstractmethod
            def convert(self, data):
                pass

        class ConcreteConverter(AbstractConverter):
            def convert(self, data):
                return f"converted: {data}"

        # Register abstract class (should work)
        result = factory.register("abstract", AbstractConverter)
        assert result is True

        # Register concrete class
        result = factory.register("concrete", ConcreteConverter)
        assert result is True

        # Create instance of concrete class
        instance = factory.create("concrete")
        assert instance.convert("test") == "converted: test"

    def test_registration_with_complex_metadata(self, factory):
        """Test registration with complex metadata structures"""
        class TestClass:
            pass

        complex_metadata = {
            "version": "1.0.0",
            "dependencies": ["numpy", "pandas"],
            "config": {
                "timeout": 30,
                "retries": 3,
                "features": ["feature1", "feature2"]
            },
            "tags": ["production", "stable"],
            "author": {
                "name": "John Doe",
                "email": "john@example.com"
            }
        }

        result = factory.register(
            "complex",
            TestClass,
            metadata=complex_metadata,
            tags=["complex", "metadata"]
        )
        assert result is True

        info = factory.get_info("complex")
        assert info.metadata["version"] == "1.0.0"
        assert info.metadata["config"]["timeout"] == 30
        assert info.metadata["author"]["name"] == "John Doe"

    def test_case_sensitive_search(self, factory):
        """Test case sensitivity in search functionality"""
        class TestClass:
            pass

        factory.register("TestClass", TestClass, description="A test class")
        factory.register("testclass", TestClass, description="Another test class")

        # Search is case-insensitive (current implementation)
        results = factory.search("test")
        assert "TestClass" in results
        assert "testclass" in results

        results = factory.search("Test")
        assert "TestClass" in results
        assert "testclass" in results

    def test_search_with_multiple_fields(self, factory):
        """Test search across multiple fields"""
        class TestClass:
            pass

        factory.register(
            "converter",
            TestClass,
            description="A data converter",
            tags=["data", "converter", "processing"]
        )

        # Search in name and description
        results = factory.search("converter", search_fields=["name", "description"])
        assert "converter" in results

        # Search in tags only
        results = factory.search("data", search_fields=["tags"])
        assert "converter" in results

        # Search in all fields
        results = factory.search("processing", search_fields=["name", "description", "tags"])
        assert "converter" in results

    def test_registration_validation_edge_cases(self, factory):
        """Test edge cases in registration validation"""
        class TestClass:
            pass

        # Test with None values
        result = factory.validate_registration(None, TestClass)
        assert result is False

        result = factory.validate_registration("test", None)
        assert result is False

        # Test with function instead of class
        def test_function():
            pass

        result = factory.validate_registration("test", test_function)
        assert result is False

        # Test with instance instead of class
        instance = TestClass()
        result = factory.validate_registration("test", instance)
        assert result is False

    def test_custom_validator_edge_cases(self, factory):
        """Test edge cases with custom validators"""
        class TestClass:
            pass

        # Validator that raises exception - should be caught and return False
        def raising_validator(name, cls):
            raise ValueError("Validation error")

        result = factory.validate_registration("test", TestClass, raising_validator)
        assert result is False

        # Validator that returns non-boolean - in Python, non-empty strings are truthy
        def non_boolean_validator(name, cls):
            return "not a boolean"

        result = factory.validate_registration("test", TestClass, non_boolean_validator)
        assert result is True  # "not a boolean" is truthy in Python

        # Validator that returns falsy value
        def falsy_validator(name, cls):
            return ""

        result = factory.validate_registration("test", TestClass, falsy_validator)
        assert result is False  # Empty string is falsy

    def test_concurrent_access_simulation(self, factory):
        """Simulate concurrent access patterns"""
        class TestClass:
            pass

        # Rapid registration and unregistration
        for i in range(100):
            factory.register(f"class_{i}", TestClass)
            assert factory.exists(f"class_{i}")
            factory.unregister(f"class_{i}")
            assert not factory.exists(f"class_{i}")

        assert factory.count() == 0

    def test_memory_cleanup(self, factory):
        """Test memory cleanup after unregistration"""
        import gc
        import weakref

        class TestClass:
            pass

        # Create weak reference to track object lifecycle
        ref = weakref.ref(TestClass)

        factory.register("test", TestClass)
        assert factory.exists("test")

        factory.unregister("test")
        assert not factory.exists("test")

        # Force garbage collection
        gc.collect()

        # The class should still exist (it's not the factory's responsibility to delete it)
        assert ref() is not None

    @pytest.mark.slow
    def test_stress_test(self, factory):
        """Stress test with many operations"""
        class TestClass:
            pass

        # Register many classes
        for i in range(1000):
            factory.register(f"class_{i}", TestClass, tags=[f"tag_{i % 5}"])

        # Perform many operations
        for i in range(100):
            # Search
            results = factory.search(f"class_{i}")
            assert f"class_{i}" in results

            # Get info
            info = factory.get_info(f"class_{i}")
            assert info is not None

            # Create instance
            instance = factory.create(f"class_{i}")
            assert instance is not None

            # List by tag
            tag_results = factory.list_by_tag(f"tag_{i % 5}")
            assert len(tag_results) > 0

        # Get summary
        summary = factory.get_summary()
        assert summary["total_classes"] == 1000
        assert len(summary["unique_tags"]) == 5

        # Clear and verify
        factory.clear()
        assert factory.count() == 0


class TestClassRegistryFactoryErrorHandling:
    """Test error handling scenarios"""

    @pytest.fixture
    def factory(self):
        return ClassRegistryFactory("error_test")

    def test_create_instance_with_invalid_args(self, factory):
        """Test creating instances with invalid arguments"""
        class TestClass:
            def __init__(self, required_arg):
                self.required_arg = required_arg

        factory.register("test", TestClass)

        # Missing required argument
        instance = factory.create("test")
        assert instance is None

        # Wrong argument type
        instance = factory.create("test", required_arg="string")
        assert instance is not None  # Should work if the class accepts it

    def test_create_instance_with_exception(self, factory):
        """Test creating instances that raise exceptions"""
        class ExceptionClass:
            def __init__(self):
                raise ValueError("Initialization failed")

        factory.register("exception", ExceptionClass)

        instance = factory.create("exception")
        assert instance is None

    def test_logging_behavior(self, factory, mock_logger):
        """Test logging behavior during operations"""
        class TestClass:
            pass

        # Test successful registration logging
        factory.register("test", TestClass)
        mock_logger.assert_called()

        # Test duplicate registration logging
        factory.register("test", TestClass)
        mock_logger.assert_called()

        # Test unregistration logging
        factory.unregister("test")
        mock_logger.assert_called()

    def test_invalid_search_fields(self, factory):
        """Test search with invalid search fields"""
        class TestClass:
            pass

        factory.register("test", TestClass, description="test description")

        # Invalid search field
        results = factory.search("test", search_fields=["invalid_field"])
        assert results == []

        # Empty search fields
        results = factory.search("test", search_fields=[])
        assert results == []

        # None search fields (should use defaults)
        results = factory.search("test", search_fields=None)
        assert "test" in results
