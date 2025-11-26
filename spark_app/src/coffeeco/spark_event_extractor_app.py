"""
Spark Event Extractor Application

This is the main application entry point for the event extractor.
"""

import logging

from pyspark.sql import SaveMode

from coffeeco.spark_batch_application import SparkBatchApplication
from coffeeco.spark_event_extractor import SparkEventExtractor

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("com.coffeeco.data.SparkEventExtractorApp")


class SparkEventExtractorApp(SparkBatchApplication):
    """Main application for extracting and transforming customer rating events"""

    # Configuration keys
    SOURCE_TABLE_NAME = "spark.event.extractor.source.table"
    DESTINATION_TABLE_NAME = "spark.event.extractor.destination.table"
    SAVE_MODE_NAME = "spark.event.extractor.save.mode"

    def __init__(self):
        """Initialize the event extractor application"""
        super().__init__()
        self._source_table = None
        self._destination_table = None

    @property
    def source_table(self) -> str:
        """Get the source table name from Spark configuration"""
        if self._source_table is None:
            self._source_table = self.spark_session.conf.get(self.SOURCE_TABLE_NAME, "")
        return self._source_table

    @property
    def destination_table(self) -> str:
        """Get the destination table name from Spark configuration"""
        if self._destination_table is None:
            self._destination_table = self.spark_session.conf.get(
                self.DESTINATION_TABLE_NAME, ""
            )
        return self._destination_table

    def _get_save_mode(self) -> SaveMode:
        """
        Get the save mode from Spark configuration

        Returns:
            SaveMode enum value
        """
        mode_str = self.spark_session.conf.get(self.SAVE_MODE_NAME, "ErrorIfExists")

        mode_map = {
            "Append": SaveMode.Append,
            "Ignore": SaveMode.Ignore,
            "Overwrite": SaveMode.Overwrite,
            "ErrorIfExists": SaveMode.ErrorIfExists,
        }

        return mode_map.get(mode_str, SaveMode.ErrorIfExists)

    def validate_config(self) -> bool:
        """
        Validate the application configuration

        Returns:
            True if configuration is valid

        Raises:
            RuntimeError: If configuration is invalid
        """
        is_valid = (
            len(self.source_table) > 0
            and len(self.destination_table) > 0
            and self.source_table != self.destination_table
            and self.spark_session.catalog.tableExists(self.source_table)
        )

        if not is_valid:
            raise RuntimeError(
                f"{self.SOURCE_TABLE_NAME} or {self.DESTINATION_TABLE_NAME} are empty, "
                f"or the {self.source_table} is missing from the spark warehouse"
            )

        return True

    def run_batch(self, save_mode: SaveMode = None):
        """
        Run the batch processing job

        Args:
            save_mode: How to save the output data (ErrorIfExists, Append, Overwrite, Ignore)
        """
        # Override save mode from configuration if not explicitly provided
        if save_mode is None:
            save_mode = self._get_save_mode()
        else:
            self._save_mode = save_mode

        logger.info(f"Starting event extraction from {self.source_table}")
        logger.info(f"Writing to {self.destination_table} with mode: {save_mode}")

        # Create the extractor and run the transformation
        extractor = SparkEventExtractor(self.spark_session)

        # Read source data, transform, and write to destination
        (
            extractor.transform(self.spark_session.table(self.source_table))
            .write.mode(save_mode)
            .saveAsTable(self.destination_table)
        )

        logger.info("Event extraction completed successfully")


def main():
    """Main entry point for the application"""
    app = SparkEventExtractorApp()
    try:
        # Always use run() to trigger the application
        # This enables the config validation to run before triggering the batch
        app.run()
    except Exception as e:
        logger.error(f"Application failed: {str(e)}", exc_info=True)
        raise
    finally:
        app.stop()


if __name__ == "__main__":
    main()
