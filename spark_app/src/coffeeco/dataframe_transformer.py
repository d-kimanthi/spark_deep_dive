"""
DataFrame Transformer Interface

This module provides the abstract base class for DataFrame transformations.
"""

from abc import ABC, abstractmethod

from pyspark.sql import DataFrame


class DataFrameTransformer(ABC):
    """Abstract base class for DataFrame transformations"""

    @abstractmethod
    def transform(self, df: DataFrame) -> DataFrame:
        """
        Transform a DataFrame

        Args:
            df: Input DataFrame to transform

        Returns:
            Transformed DataFrame
        """
        pass
