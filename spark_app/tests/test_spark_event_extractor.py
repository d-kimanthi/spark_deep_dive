"""
Spark Event Extractor Tests

This module contains tests for the SparkEventExtractor class.
"""

from datetime import datetime

import pytest
from coffeeco.data.spark_event_extractor import SparkEventExtractor
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    IntegerType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)

from tests.shared_spark_sql import clean_tables, spark_session
from tests.test_helper import get_test_resource_path


class TestSparkEventExtractor:
    """Test suite for SparkEventExtractor"""

    def test_transform_filters_customer_rating_events(
        self, spark_session, clean_tables
    ):
        """Test that transform filters for CustomerRatingEventType"""

        # Create test customer data
        customer_data = [
            (
                "CUST123",
                "Scott",
                "Haines",
                "scott@coffeeco.com",
                datetime(2021, 4, 18, 16, 28, 13),
            )
        ]
        customer_schema = StructType(
            [
                StructField("customerId", StringType(), False),
                StructField("firstName", StringType(), False),
                StructField("lastName", StringType(), False),
                StructField("email", StringType(), False),
                StructField("created", TimestampType(), False),
            ]
        )
        customer_df = spark_session.createDataFrame(customer_data, customer_schema)
        customer_df.createOrReplaceTempView("customers")

        # Create test event data
        event_data = [
            (
                datetime(2021, 4, 20, 10, 0, 0),
                "CustomerRatingEventType",
                "customer_rating",
                "CUST123",
                5,
                "rating.store",
            ),
            (
                datetime(2021, 4, 20, 11, 0, 0),
                "BasicEvent",
                "basic_event",
                None,
                None,
                None,
            ),
            (
                datetime(2021, 4, 20, 12, 0, 0),
                "CustomerRatingEventType",
                "customer_rating",
                "CUST123",
                4,
                "rating.item",
            ),
        ]
        event_schema = StructType(
            [
                StructField("created", TimestampType(), False),
                StructField("eventType", StringType(), False),
                StructField("label", StringType(), False),
                StructField("customerId", StringType(), True),
                StructField("rating", IntegerType(), True),
                StructField("ratingType", StringType(), True),
            ]
        )
        event_df = spark_session.createDataFrame(event_data, event_schema)

        # Create extractor and transform
        extractor = SparkEventExtractor(spark_session)
        result_df = extractor.transform(event_df)

        # Verify results
        assert result_df.count() == 2, "Should have 2 CustomerRatingEventType events"
        assert "firstName" in result_df.columns, "Should have customer data joined"
        assert "lastName" in result_df.columns, "Should have customer data joined"

        # Verify no BasicEvent records
        basic_events = result_df.filter(result_df.eventType == "BasicEvent")
        assert basic_events.count() == 0, "Should not have BasicEvent records"

    def test_with_customer_data_raises_error_when_table_missing(self, spark_session):
        """Test that with_customer_data raises error when customers table is missing"""

        # Create test event data without customers table
        event_data = [
            (
                datetime(2021, 4, 20, 10, 0, 0),
                "CustomerRatingEventType",
                "customer_rating",
                "CUST123",
                5,
                "rating.store",
            )
        ]
        event_schema = StructType(
            [
                StructField("created", TimestampType(), False),
                StructField("eventType", StringType(), False),
                StructField("label", StringType(), False),
                StructField("customerId", StringType(), False),
                StructField("rating", IntegerType(), False),
                StructField("ratingType", StringType(), False),
            ]
        )
        event_df = spark_session.createDataFrame(event_data, event_schema)

        # Create extractor
        extractor = SparkEventExtractor(spark_session)

        # Verify error is raised
        with pytest.raises(RuntimeError, match="Missing Table: customers"):
            extractor.with_customer_data(event_df)

    def test_transform_with_test_data_files(self, spark_session, clean_tables):
        """Test transform using the actual test data files"""

        # Load customer data from test resources
        customers_path = get_test_resource_path("customers/customers.json")
        customer_df = spark_session.read.json(customers_path)
        customer_df.createOrReplaceTempView("customers")

        # Load customer ratings data from test resources
        ratings_path = get_test_resource_path("customers/customer_ratings.json")
        ratings_df = spark_session.read.json(ratings_path)

        # Create extractor and transform
        extractor = SparkEventExtractor(spark_session)
        result_df = extractor.transform(ratings_df)

        # Verify results
        assert result_df.count() > 0, "Should have results"
        assert "firstName" in result_df.columns, "Should have customer firstName"
        assert "lastName" in result_df.columns, "Should have customer lastName"
        assert "email" in result_df.columns, "Should have customer email"
        assert "joined" in result_df.columns, "Should have customer joined date"
