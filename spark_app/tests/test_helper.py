"""
Test Helper Utilities

This module provides helper functions for testing.
"""

import os
from typing import Optional

from pyspark.sql import SparkSession


def get_spark_test_session(app_name: str = "test-app") -> SparkSession:
    """
    Create a SparkSession for testing

    Args:
        app_name: Name for the test application

    Returns:
        Configured SparkSession for testing
    """
    return (
        SparkSession.builder.appName(app_name)
        .master("local[*]")
        .config("spark.sql.shuffle.partitions", "1")
        .config("spark.default.parallelism", "1")
        .config("spark.sql.warehouse.dir", "file:///tmp/spark-warehouse")
        .getOrCreate()
    )


def get_test_resource_path(resource_name: str) -> str:
    """
    Get the full path to a test resource

    Args:
        resource_name: Name of the resource file (e.g., 'customers/customers.json')

    Returns:
        Full path to the test resource
    """
    test_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(test_dir, "resources", resource_name)
