#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) XLab-Open. All rights reserved.
"""
Generic class registration factory
Supports dynamic registration, instantiation, and management of different types of classes
"""

import inspect
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type, TypeVar, Union, Callable
from dataclasses import dataclass
import logging

# Type variable
T = TypeVar('T')

@dataclass
class ClassInfo:
    """Class information data class"""
    name: str
    cls: Type
    description: str = ""
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.metadata is None:
            self.metadata = {}


class ClassRegistryFactory:
    """
    Generic Class Registration Factory

    Features:
        a). Dynamically register classes
        b). Lookup classes by name or tags
        c). Automatic instantiation
        d). Support for inheritance checks
        e). Support for metadata and tag management
        f). Support for validation and constraints
    """

    def __init__(self, name: str = "default"):
        self.name = name
        self._registry: Dict[str, ClassInfo] = {}
        self._logger = logging.getLogger(f"{__name__}.{name}")

    def register(self,
                name: str,
                cls: Type[T],
                description: str = "",
                tags: Optional[List[str]] = None,
                metadata: Optional[Dict[str, Any]] = None,
                override: bool = False) -> bool:
        """
        Register a class.

        Args:
            name (str): The name of the class in the registry.
            cls (type): The class to register.
            description (str, optional): A description of the class.
            tags (List[str], optional): A list of tags associated with the class.
            metadata (Dict[str, Any], optional): Additional metadata for the class.
            override (bool, optional): Whether to allow overriding an existing registration.

        Returns:
            bool: Whether the registration was successful.
        """
        if not override and name in self._registry:
            self._logger.warning(f"Class '{name}' already exists, skipping registration")
            return False

        if not inspect.isclass(cls):
            self._logger.error(f"'{cls}' is not a valid class")
            return False

        class_info = ClassInfo(
            name=name,
            cls=cls,
            description=description,
            tags=tags or [],
            metadata=metadata or {}
        )

        self._registry[name] = class_info
        self._logger.info(f"Successful registration class '{name}' -> {cls.__name__}")
        return True

    def register_decorator(self,
                          name: Optional[str] = None,
                          description: Optional[str] = None,
                          tags: Optional[List[str]] = None,
                          metadata: Optional[Dict[str, Any]] = None,
                          override: bool = False):
        """
        Decorator registration of classes.
        Usage:
            @factory.register_decorator("my_class", description="My class")
            class MyClass:
                pass
        """
        def decorator(cls: Type[T]) -> Type[T]:
            class_name = name or cls.__name__
            class_description = description or (cls.__doc__ or "")
            self.register(
                name=class_name,
                cls=cls,
                description=class_description,
                tags=tags,
                metadata=metadata,
                override=override
            )
            return cls
        return decorator

    def unregister(self, name: str) -> bool:
        """
        Unregister a class.

        Args:
            name: The name of the class to unregister.

        Returns:
            bool: Whether the unregistration was successful.
        """
        if name in self._registry:
            del self._registry[name]
            self._logger.info(f"Successfully unregistered class '{name}'")
            return True
        return False

    def get(self, name: str) -> Optional[Type[T]]:
        """
        Get a registered class.

        Args:
            name: The name of the class.

        Returns:
            Type[T]: The registered class, or None if it doesn't exist.
        """
        class_info = self._registry.get(name)
        return class_info.cls if class_info else None

    def get_info(self, name: str) -> Optional[ClassInfo]:
        """
        Get the detailed information of a registered class.

        Args:
            name: The name of the class.

        Returns:
            ClassInfo: The class information, or None if it doesn't exist.
        """
        return self._registry.get(name)

    def create(self,
               name: str,
               *args,
               **kwargs) -> Optional[T]:
        """
        Create an instance of a class.

        Args:
            name: The name of the class.
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            T: The class instance, or None if creation fails.
        """
        cls: Optional[Type[T]] = self.get(name)
        if cls is None:
            self._logger.error(f"Class '{name}' does not exist")
            return None

        try:
            instance = cls(*args, **kwargs)
            self._logger.debug(f"Successfully created instance '{name}'")
            return instance
        except Exception as e:
            self._logger.error(f"Failed to create instance '{name}': {e}")
            return None

    def list_all(self) -> List[str]:
        """
        List all registered class names.

        Returns:
            List[str]: The list of class names.
        """
        return list(self._registry.keys())

    def list_by_tag(self, tag: str) -> List[str]:
        """
        List class names by tag.

        Args:
            tag: The tag.

        Returns:
            List[str]: The list of class names matching the tag.
        """
        return [
            name for name, info in self._registry.items()
            if info.tags is not None and tag in info.tags
        ]

    def list_by_type(self, base_class: Type) -> List[str]:
        """
        List class names by base class type.

        Args:
            base_class: The base class.

        Returns:
            List[str]: The list of class names inheriting from the specified base class.
        """
        return [
            name for name, info in self._registry.items()
            if issubclass(info.cls, base_class)
        ]

    def search(self,
               query: str,
               search_fields: Optional[List[str]] = None) -> List[str]:
        """
        Search classes.

        Args:
            query: The search query.
            search_fields: The list of search fields, default search name and description.

        Returns:
            List[str]: The list of class names matching the query.
        """
        if search_fields is None:
            search_fields = ['name', 'description']

        results = []
        query_lower = query.lower()

        for name, info in self._registry.items():
            for field in search_fields:
                if field == 'name' and query_lower in name.lower():
                    results.append(name)
                    break
                elif field == 'description' and query_lower in info.description.lower():
                    results.append(name)
                    break
                elif field == 'tags':
                    if info.tags is not None and any(query_lower in tag.lower() for tag in info.tags):
                        results.append(name)
                        break

        return list(set(results))  # Remove duplicates

    def exists(self, name: str) -> bool:
        """
        Check if a class is registered.

        Args:
            name: The name of the class.

        Returns:
            bool: Whether the class exists.
        """
        return name in self._registry

    def count(self) -> int:
        """
        Get the number of registered classes.

        Returns:
            int: The number of registered classes.
        """
        return len(self._registry)

    def clear(self):
        """Clear all registered classes."""
        self._registry.clear()
        self._logger.info("All registered classes have been cleared")

    def get_summary(self) -> Dict[str, Any]:
        """
        Get the summary information of the registry.

        Returns:
            Dict[str, Any]: The summary information.
        """
        all_tags = set()
        for info in self._registry.values():
            if info.tags is not None:
                all_tags.update(info.tags)

        return {
            "name": self.name,
            "total_classes": len(self._registry),
            "unique_tags": list(all_tags),
            "class_names": list(self._registry.keys())
        }

    def validate_registration(self,
                            name: str,
                            cls: Type[T],
                            validator: Optional[Callable[[str, Type[T]], bool]] = None) -> bool:
        """
        Validate class registration.

        Args:
            name: The name of the class.
            cls: The class to validate.
            validator: A custom validation function.

        Returns:
            bool: Whether the validation passed.
        """
        # Basic validation
        if not name or not name.strip():
            self._logger.error("Class name cannot be empty")
            return False

        if not inspect.isclass(cls):
            self._logger.error(f"'{cls}' is not a valid class")
            return False

        # Custom validation
        if validator:
            try:
                result = validator(name, cls)
                if not result:
                    self._logger.error(f"Custom validation failed: {name}")
                    return False
            except Exception as e:
                self._logger.error(f"Custom validator raised exception: {e}")
                return False

        return True
