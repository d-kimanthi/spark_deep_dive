"""
Spark Application Base Class

This module provides the base class for all Spark applications.
"""

from abc import ABC, abstractmethod

from pyspark import SparkConf
from pyspark.sql import SparkSession

from coffeeco.config.configuration import Configuration


class SparkApplication(ABC):
    """Base class for Spark applications"""

    def __init__(self):
        """Initialize the Spark application"""
        self._config = Configuration()
        self.app_name = self._config.app_name
        self._spark_session = None

    @property
    def spark_conf(self) -> SparkConf:
        """
        Create and configure SparkConf

        Returns:
            Configured SparkConf instance
        """
        conf = SparkConf().setAppName(self.app_name)

        # Apply all configuration settings
        for key, value in self._config.spark_settings.items():
            conf.set(key, value)

        return conf

    @property
    def spark_session(self) -> SparkSession:
        """
        Get or create the SparkSession

        Returns:
            SparkSession instance
        """
        if self._spark_session is None:
            self._spark_session = (
                SparkSession.builder.config(conf=self.spark_conf)
                .enableHiveSupport()
                .getOrCreate()
            )
        return self._spark_session

    @abstractmethod
    def validate_config(self) -> bool:
        """
        Ensure that the application can run correctly, and there is no missing or empty config

        Returns:
            True if the application is okay to start

        Raises:
            RuntimeError: If configuration is invalid
        """
        pass

    def run(self):
        """Run the application"""
        self.validate_config()

    def stop(self):
        """Stop the Spark session"""
        if self._spark_session is not None:
            self._spark_session.stop()
