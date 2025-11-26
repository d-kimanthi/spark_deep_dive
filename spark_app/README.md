## CoffeeCo: Chapter 7 : Structured Reference Application (Python Implementation)

This is a Python implementation of the Scala Spark application from Chapter 7, providing the same functionality using PySpark.

### Project Structure

```
app-py/
├── .env                        # Environment variables (git-ignored)
├── .env.example                # Example environment configuration
├── conf/
│   └── local.conf              # Legacy configuration (optional)
├── src/
│   └── coffeeco/
│       └── data/
│           ├── config/
│           │   └── configuration.py    # Pydantic Settings configuration
│           ├── models/
│           │   ├── customer.py         # Customer data models
│           │   ├── event.py            # Event data models
│           │   ├── item.py             # Item data models
│           │   ├── rating.py           # Rating data models
│           │   └── store.py            # Store data models
│           ├── dataframe_transformer.py    # Base transformer interface
│           ├── spark_application.py        # Base Spark application
│           ├── spark_batch_application.py  # Batch application base
│           ├── spark_event_extractor.py    # Event extraction logic
│           └── spark_event_extractor_app.py # Main application entry point
├── tests/
│   ├── resources/
│   │   └── customers/
│   │       ├── customers.json          # Test customer data
│   │       └── customer_ratings.json   # Test rating data
│   ├── shared_spark_sql.py            # Shared test utilities
│   ├── test_helper.py                  # Test helper functions
│   └── test_spark_event_extractor.py  # Unit tests
├── requirements.txt            # Python dependencies
├── requirements-dev.txt        # Development dependencies
└── setup.py                    # Package setup
```

### Prerequisites

- Python 3.7 or higher
- Apache Spark 3.1.1 or higher
- MySQL (for Hive Metastore)
- Java 11

### Installation

1. **Create a virtual environment** (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **For development** (includes testing tools):

   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Install the package** (optional):
   ```bash
   pip install -e .
   ```

### Configuration

The application now uses **Pydantic BaseSettings** for configuration management, which provides better type safety and validation.

#### Configuration with Environment Variables

1. **Copy the example environment file**:

   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` to match your environment**:

   ```bash
   # Application Configuration
   APP_NAME=spark-event-extractor
   This application is an example batch application that reuses the Hive Metastore you created in Chapter 6. You need to either:

   ```

3. Run MySQL on Docker (using `ch-06/docker/`), or
4. Run MySQL locally and bootstrap the environment
5. Update the `.env` file to include the correct JDBC connection URL for your MySQL host
   SPARK**SQL**HIVE**JAVAX**JDO**OPTION**CONNECTIONPASSWORD=your_password

   # Spark Warehouse Configuration

   SPARK**SQL**WAREHOUSE\_\_DIR=file:///path/to/your/spark/sql/warehouse

   ```

   ```

6. **Key Configuration Variables**:
   - `APP_NAME`: Application name
   - `SPARK__SQL__HIVE__JAVAX__JDO__OPTION__CONNECTIONURL`: Your MySQL connection URL
   - `SPARK__SQL__WAREHOUSE__DIR`: Path to your Spark SQL warehouse directory
   - Environment variables use double underscores (`__`) to represent nested configuration

#### Environment Variable Naming Convention

The configuration uses a hierarchical naming with double underscores:

- `SPARK__SQL__CATALOGIMPLEMENTATION` → `spark.sql.catalogImplementation`
- `SPARK__SQL__HIVE__METASTORE__VERSION` → `spark.sql.hive.metastore.version`

#### Programmatic Configuration

You can also configure the application programmatically:

```python
from coffeeco.data.config.configuration import Configuration

config = Configuration(
    app_name="my-custom-app",
    spark=SparkSettings(
        warehouse_dir="file:///my/custom/path"
    )
)
```

### Reuse What You've Learned

This application is an example batch application that reuses the Hive Metastore you created in Chapter 6. You need to either:

1. Run MySQL on Docker (using `ch-06/docker/`), or
2. Run MySQL locally and bootstrap the environment
3. Update the `conf/local.conf` to include the correct JDBC connection URL for your MySQL host

### Adding the Bronze and Silver Databases

Working with distributed data can be easier when you follow the medallion architecture:

1. Use the notion of a `bronze` database for raw data
2. Use the notion of a `silver` database for reliable data
3. Use the notion of a `gold` database for production data

### Preparing the Data

Before running the application, you need to populate the required tables:

1. **Populate the `default.customers` table** (see `tests/resources/customers/customers.json`)
2. **Populate the `bronze.customerRatings` table** (see `tests/resources/customers/customer_ratings.json`)

You can load these using Spark SQL or the Spark DataFrame API.

### Running the Application

Use `spark-submit` to run the application. You'll need to update the paths and configurations:

```bash
spark-submit \
  --master "local[*]" \
  --deploy-mode "client" \
  --packages org.mariadb.jdbc:mariadb-java-client:2.7.2 \
  --conf "spark.event.extractor.source.table=bronze.customerRatings" \
  --conf "spark.event.extractor.destination.table=silver.customerRatings" \
  --conf "spark.sql.hive.javax.jdo.option.ConnectionDriverName=org.mariadb.jdbc.Driver" \
  --conf "spark.event.extractor.save.mode=ErrorIfExists" \
  --conf "spark.sql.hive.javax.jdo.option.ConnectionPassword=dataengineering_user" \
  --conf "spark.sql.warehouse.dir=file:///PATH/TO/spark-moderndataengineering/ch-06/docker/spark/sql/warehouse" \
  --py-files src/coffeeco/data/spark_event_extractor_app.py \
  src/coffeeco/data/spark_event_extractor_app.py
```

#### Alternative: Using SPARK_HOME and PYTHONPATH

If you have installed the package, you can also run it directly:

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

spark-submit \
  --master "local[*]" \
  --deploy-mode "client" \
  --packages org.mariadb.jdbc:mariadb-java-client:2.7.2 \
  --conf "spark.event.extractor.source.table=bronze.customerRatings" \
  --conf "spark.event.extractor.destination.table=silver.customerRatings" \
  --conf "spark.event.extractor.save.mode=ErrorIfExists" \
  --conf "spark.sql.warehouse.dir=file:///PATH/TO/spark-moderndataengineering/ch-06/docker/spark/sql/warehouse" \
  src/coffeeco/data/spark_event_extractor_app.py
```

**Note**: Configuration is now primarily loaded from the `.env` file. Spark-specific runtime configurations like source/destination tables are still passed via `--conf` flags.

### Configuration Options

The application accepts the following Spark configurations:

- `spark.event.extractor.source.table`: Source table name (e.g., `bronze.customerRatings`)
- `spark.event.extractor.destination.table`: Destination table name (e.g., `silver.customerRatings`)
- `spark.event.extractor.save.mode`: Save mode for the DataFrameWriter
  - `ErrorIfExists` (default): Fail if the table already exists
  - `Append`: Append data to existing table
  - `Overwrite`: Overwrite existing table
  - `Ignore`: Silently ignore if table exists

### Running Tests

Run the test suite using pytest:

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest -v tests/

# Run specific test file
pytest tests/test_spark_event_extractor.py

# Run with coverage
pytest --cov=coffeeco tests/
```

### Differences from Scala Implementation

While functionally equivalent, this Python implementation has some differences from the Scala version:

1. **Configuration**: Uses **Pydantic BaseSettings** for type-safe configuration with environment variables
2. **Testing**: Uses `pytest` instead of ScalaTest
3. **Type System**: Uses Python type hints and dataclasses instead of Scala case classes
4. **Imports**: Python-style imports and package structure
5. **Logging**: Uses Python's standard `logging` module instead of Log4j
6. **Logging**: Uses Python's standard `logging` module instead of Log4j

### Architecture

The application follows a layered architecture:

1. **SparkApplication**: Base class for all Spark applications
2. **SparkBatchApplication**: Extension for batch processing applications
3. **DataFrameTransformer**: Interface for DataFrame transformations
4. **SparkEventExtractor**: Concrete implementation of event extraction logic
5. **SparkEventExtractorApp**: Main application entry point

### Key Features

- **Configuration-driven**: All settings configurable via environment variables using Pydantic BaseSettings
- **Type-safe**: Uses Python dataclasses for data models and Pydantic for configuration validation
- **Testable**: Comprehensive test suite with pytest
- **Modular**: Clean separation of concerns
- **Production-ready**: Includes error handling and logging
- **Production-ready**: Includes error handling and logging

### Troubleshooting

**Issue**: `ModuleNotFoundError: No module named 'coffeeco'`
**Solution**: Make sure you've set the `PYTHONPATH` or installed the package with `pip install -e .`

**Issue**: `RuntimeError: Missing Table: customers`
**Solution**: Ensure the customers table exists in your Hive Metastore

**Issue**: Configuration not loading
**Solution**: Ensure the `.env` file exists in the application root directory, or set environment variables directly

**Issue**: Pydantic validation errors
**Solution**: Check that all required environment variables are set correctly in your `.env` file. Use `.env.example` as a reference.

### License

See the main repository LICENSE file.
