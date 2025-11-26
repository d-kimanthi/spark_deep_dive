"""
Spark Batch Application Base Class

This module provides the base class for batch Spark applications.
"""

from abc import abstractmethod

from pyspark.sql import SaveMode

from coffeeco.spark_application import SparkApplication


class SparkBatchApplication(SparkApplication):
    """Base class for batch Spark applications"""

    def __init__(self):
        """Initialize the batch application"""
        super().__init__()
        self._save_mode = SaveMode.ErrorIfExists

    @property
    def save_mode(self) -> SaveMode:
        """
        Batch applications using the DataFrameWriter have the following options:
        ErrorIfExists, Ignore, Overwrite, Append
        Ensure you protect your endpoints. You must override the save_mode explicitly

        Returns:
            SaveMode for DataFrameWriter operations
        """
        return self._save_mode

    @save_mode.setter
    def save_mode(self, mode: SaveMode):
        """Set the save mode"""
        self._save_mode = mode

    @abstractmethod
    def run_batch(self, save_mode: SaveMode = None):
        """
        Applications should have common behavior, they all run

        Args:
            save_mode: How should the DataFrameWriter operate?
                      ErrorIfExists, Ignore, Overwrite, Append?
        """
        pass

    def run(self):
        """Run the batch application"""
        super().run()
        # If we have a valid config, continue
        self.run_batch(save_mode=self.save_mode)
