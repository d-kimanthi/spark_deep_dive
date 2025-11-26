"""
Configuration Module

This module handles loading and managing application configuration using Pydantic BaseSettings.
"""

from typing import Dict, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class SparkSettings(BaseSettings):
    """Spark configuration settings"""

    catalog_implementation: str = Field(
        default="hive", alias="spark.sql.catalogImplementation"
    )
    hive_metastore_version: str = Field(
        default="2.3.7", alias="spark.sql.hive.metastore.version"
    )
    hive_metastore_jars: str = Field(
        default="builtin", alias="spark.sql.hive.metastore.jars"
    )
    hive_metastore_shared_prefixes: str = Field(
        default="com.mysql.cj.jdbc,com.mysql.jdbc,org.postgresql,com.microsoft.sqlserver,oracle.jdbc",
        alias="spark.sql.hive.metastore.sharedPrefixes",
    )
    hive_metastore_schema_verification: str = Field(
        default="true", alias="spark.sql.hive.metastore.schema.verification"
    )
    hive_metastore_schema_verification_record_version: str = Field(
        default="true",
        alias="spark.sql.hive.metastore.schema.verification.record.version",
    )
    parquet_compression_codec: str = Field(
        default="snappy", alias="spark.sql.parquet.compression.codec"
    )
    parquet_merge_schema: str = Field(
        default="false", alias="spark.sql.parquet.mergeSchema"
    )
    parquet_filter_pushdown: str = Field(
        default="true", alias="spark.sql.parquet.filterPushdown"
    )
    hadoop_parquet_enable_summary_metadata: str = Field(
        default="false", alias="spark.hadoop.parquet.enable.summary-metadata"
    )
    hadoop_mapreduce_fileoutputcommitter_algorithm_version: str = Field(
        default="2",
        alias="spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version",
    )
    hive_javax_jdo_option_connection_url: str = Field(
        default="jdbc:mysql://mysql:3306/metastore",
        alias="spark.sql.hive.javax.jdo.option.ConnectionURL",
    )
    hive_javax_jdo_option_connection_driver_name: str = Field(
        default="com.mysql.cj.jdbc.Driver",
        alias="spark.sql.hive.javax.jdo.option.ConnectionDriverName",
    )
    hive_javax_jdo_option_connection_user_name: str = Field(
        default="dataeng", alias="spark.sql.hive.javax.jdo.option.ConnectionUserName"
    )
    warehouse_dir: str = Field(
        default="hdfs://PATH/TO/YOUR/spark/sql/warehouse",
        alias="spark.sql.warehouse.dir",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        populate_by_name=True,
        extra="allow",
    )

    def to_spark_config_dict(self) -> Dict[str, str]:
        """
        Convert settings to Spark configuration dictionary

        Returns:
            Dictionary of Spark configuration key-value pairs
        """
        config_dict = {}
        for field_name, field_info in self.model_fields.items():
            alias = field_info.alias
            if alias:
                value = getattr(self, field_name)
                if value is not None:
                    config_dict[alias] = str(value)
        return config_dict


class Configuration(BaseSettings):
    """Application configuration using Pydantic BaseSettings"""

    app_name: str = Field(
        default="spark-event-extractor", description="Application name"
    )

    # Nested Spark settings
    spark: SparkSettings = Field(default_factory=SparkSettings)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="",
        case_sensitive=False,
        extra="allow",
    )

    @property
    def spark_settings(self) -> Dict[str, str]:
        """
        Get Spark configuration settings

        Returns:
            Dictionary of Spark configuration key-value pairs
        """
        return self.spark.to_spark_config_dict()
