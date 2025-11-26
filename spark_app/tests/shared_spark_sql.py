"""
Shared Spark SQL Testing Utilities

This module provides shared testing utilities for Spark SQL tests.
"""

import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark_session():
    """
    Create a shared SparkSession for all tests

    Yields:
        SparkSession configured for testing
    """
    spark = (
        SparkSession.builder.appName("test-app")
        .master("local[*]")
        .config("spark.sql.shuffle.partitions", "1")
        .config("spark.default.parallelism", "1")
        .config("spark.sql.warehouse.dir", "file:///tmp/spark-warehouse")
        .enableHiveSupport()
        .getOrCreate()
    )

    yield spark

    spark.stop()


@pytest.fixture(scope="function")
def clean_tables(spark_session):
    """
    Clean up tables before each test

    Args:
        spark_session: The shared SparkSession

    Yields:
        SparkSession with clean state
    """
    # Drop any existing test tables
    test_tables = ["customers", "bronze.customerRatings", "silver.customerRatings"]
    for table in test_tables:
        try:
            spark_session.sql(f"DROP TABLE IF EXISTS {table}")
        except:
            pass

    yield spark_session

    # Cleanup after test
    for table in test_tables:
        try:
            spark_session.sql(f"DROP TABLE IF EXISTS {table}")
        except:
            pass
