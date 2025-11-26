"""
Spark Event Extractor

This module provides the event extraction and transformation logic.
"""

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col

from coffeeco.dataframe_transformer import DataFrameTransformer


class SparkEventExtractor(DataFrameTransformer):
    """Extract and transform customer rating events"""

    def __init__(self, spark: SparkSession):
        """
        Initialize the event extractor

        Args:
            spark: SparkSession instance
        """
        self.spark = spark

    def transform(self, df: DataFrame) -> DataFrame:
        """
        Transform the input DataFrame by filtering for CustomerRatingEventType
        and joining with customer data

        Args:
            df: Input DataFrame containing events

        Returns:
            Transformed DataFrame with customer data joined
        """
        return df.filter(col("eventType") == "CustomerRatingEventType").transform(
            self.with_customer_data
        )

    def with_customer_data(self, df: DataFrame) -> DataFrame:
        """
        Join event data with customer information

        Args:
            df: Input DataFrame containing customer events

        Returns:
            DataFrame with customer information joined

        Raises:
            RuntimeError: If customers table does not exist
        """
        if self.spark.catalog.tableExists("customers"):
            customer_df = self.spark.table("customers").select(
                col("customerId"),
                col("firstName"),
                col("lastName"),
                col("email"),
                col("created").alias("joined"),
            )
            return customer_df.join(df, on="customerId", how="inner")
        else:
            raise RuntimeError("Missing Table: customers")
