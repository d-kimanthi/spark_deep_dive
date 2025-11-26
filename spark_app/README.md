# Spark Event Extractor Application

A production-ready PySpark batch application for extracting and transforming customer rating events. This application demonstrates a clean, layered architecture for building scalable Spark applications with type-safe configuration management using Pydantic.

## What This Application Does

The Spark Event Extractor processes customer rating events through a medallion architecture pipeline:

- **Reads** raw customer rating events from a source table (e.g., `bronze.customerRatings`)
- **Filters** for specific event types (`CustomerRatingEventType`)
- **Enriches** the data by joining with customer information
- **Writes** the transformed data to a destination table (e.g., `silver.customerRatings`)

## Architecture Overview

The application follows a **layered inheritance pattern** with four core Python files that build upon each other:

### 1. `dataframe_transformer.py` - Base Interface

The foundation of the transformation pipeline. Defines an abstract base class with a single method:

```python
class DataFrameTransformer(ABC):
    @abstractmethod
    def transform(self, df: DataFrame) -> DataFrame:
        """Transform a DataFrame"""
```

**Purpose**: Establishes a contract for all DataFrame transformations, promoting consistency and testability.

### 2. `spark_application.py` - Spark Application Base

Builds on the transformer concept by adding Spark session management and configuration:

```python
class SparkApplication(ABC):
    def __init__(self):
        self._config = Configuration()  # Loads Pydantic settings
        self._spark_session = None

    @property
    def spark_session(self) -> SparkSession:
        """Get or create SparkSession with Hive support"""

    @abstractmethod
    def validate_config(self) -> bool:
        """Validate application configuration"""
## Prerequisites

- Python 3.7 or higher
- Apache Spark 3.1.1 or higher
- MySQL database (for Hive Metastore)
- Java 11

## Quick Start(self):
        super().__init__()
        self._save_mode = SaveMode.ErrorIfExists

    @abstractmethod
    def run_batch(self, save_mode: SaveMode = None):
        """Execute batch processing logic"""

    def run(self):
        """Validate config, then run batch"""
```

**Purpose**: Adds DataFrame write modes (Append, Overwrite, ErrorIfExists) and batch execution workflow. Use this as the base for any batch processing application.

### 4. `spark_event_extractor_app.py` - Concrete Implementation

The actual business logic that inherits from `SparkBatchApplication`:

```python
class SparkEventExtractorApp(SparkBatchApplication):
    def validate_config(self) -> bool:
        """Ensure source/destination tables are valid"""

    def run_batch(self, save_mode: SaveMode = None):
        """Extract events, transform, and write results"""
```

**Purpose**: Implements the specific event extraction logic. Reads from source table, applies `SparkEventExtractor` transformation, writes to destination.

**Inheritance Chain**: `DataFrameTransformer` ← `SparkApplication` ← `SparkBatchApplication` ← `SparkEventExtractorApp`

### Project Structure

```
spark_app/
├── .env                        # Environment variables (git-ignored)
├── .env.example                # Example environment configuration
├── src/
│   └── coffeeco/
│       └── data/
│           ├── config/
│           │   └── configuration.py    # Pydantic Settings configuration
│           ├── models/                 # Data models (Customer, Event, Rating, etc.)
│           ├── dataframe_transformer.py    # [1] Base transformer interface
│           ├── spark_application.py        # [2] Spark application base
│           ├── spark_batch_application.py  # [3] Batch processing base
│           ├── spark_event_extractor.py    # Event transformation logic
│           └── spark_event_extractor_app.py # [4] Main application entry point
├── tests/                      # Test suite with pytest
├── requirements.txt            # Python dependencies
└── setup.py                    # Package setup
```

### Prerequisites

- Python 3.7 or higher
- Apache Spark 3.1.1 or higher
- MySQL (for Hive Metastore)
- Java 11

### Installation

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
vim .env  # Edit with your settings

# 4. Verify configuration
python test_config.py

# 5. Run the application
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
spark-submit \
  --master "local[*]" \
  --conf "spark.event.extractor.source.table=bronze.customerRatings" \
  --conf "spark.event.extractor.destination.table=silver.customerRatings" \
  src/coffeeco/data/spark_event_extractor_app.py
```

## Configuration

The application uses **Pydantic BaseSettings** for type-safe configuration management via environment variables.

### Setup Configuration

1. **Copy the example file**:

   ```bash
   cp .env.example .env
   ```

2. **Edit key settings in `.env`**:

   ```bash
   # Application
   APP_NAME=spark-event-extractor

   # Database Connection
   SPARK__SQL__HIVE__JAVAX__JDO__OPTION__CONNECTIONURL=jdbc:mysql://localhost:3306/metastore
   SPARK__SQL__HIVE__JAVAX__JDO__OPTION__CONNECTIONUSERNAME=your_username
   SPARK__SQL__HIVE__JAVAX__JDO__OPTION__CONNECTIONPASSWORD=your_password

   # Warehouse Location
   SPARK__SQL__WAREHOUSE__DIR=file:///path/to/spark/warehouse
   ```

3. **Key Configuration Variables**:
   - `APP_NAME` - Application name
   - `SPARK__SQL__HIVE__JAVAX__JDO__OPTION__CONNECTIONURL` - MySQL metastore connection
   - `SPARK__SQL__WAREHOUSE__DIR` - Spark SQL warehouse directory path

### Environment Variable Naming

The configuration uses a hierarchical naming with double underscores:

- `SPARK__SQL__CATALOGIMPLEMENTATION` → `spark.sql.catalogImplementation`
- `SPARK__SQL__HIVE__METASTORE__VERSION` → `spark.sql.hive.metastore.version`

#### Programmatic Configuration

You can also configure the application programmatically:

````python
Environment variables use double underscores (`__`) to represent nested Spark configuration:
- `SPARK__SQL__CATALOGIMPLEMENTATION` → `spark.sql.catalogImplementation`
- `SPARK__SQL__WAREHOUSE__DIR` → `spark.sql.warehouse.dir`

See `CONFIGURATION.md` for complete configuration reference.

## Data Setup

### Medallion Architecture

The application implements a **medallion architecture** for data quality:
- **Bronze** - Raw, unprocessed data
- **Silver** - Cleaned, validated data
- **Gold** - Business-ready, aggregated data

### Preparing Tables
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
````

#### Alternative: Using SPARK_HOME and PYTHONPATH

If you have installed the package, you can also run it directly:

````bash
Create and populate the required tables:

1. **Customer table** (`default.customers`) - Contains customer information
2. **Source table** (`bronze.customerRatings`) - Raw customer rating events

Sample data is available in `tests/resources/customers/` for reference.

## Running the Application

### Basic Execution
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
````

### Differences from Scala Implementation

While functionally equivalent, this Python implementation has some differences from the Scala version:

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

spark-submit \
  --master "local[*]" \
  --packages org.mariadb.jdbc:mariadb-java-client:2.7.2 \
  --conf "spark.event.extractor.source.table=bronze.customerRatings" \
  --conf "spark.event.extractor.destination.table=silver.customerRatings" \
  --conf "spark.event.extractor.save.mode=ErrorIfExists" \
  src/coffeeco/data/spark_event_extractor_app.py
```

### Runtime Configuration Options

### Key Features

- **Configuration-driven**: All settings configurable via environment variables using Pydantic BaseSettings
- **Type-safe**: Uses Python dataclasses for data models and Pydantic for configuration validation
- **Testable**: Comprehensive test suite with pytest
  Pass these via `--conf` flags to `spark-submit`:

| Configuration                             | Description                   | Default         |
| ----------------------------------------- | ----------------------------- | --------------- |
| `spark.event.extractor.source.table`      | Source table to read from     | Required        |
| `spark.event.extractor.destination.table` | Destination table to write to | Required        |
| `spark.event.extractor.save.mode`         | Write mode (see below)        | `ErrorIfExists` |

**Save Modes**:

- `ErrorIfExists` - Fail if destination table exists (safe default)
- `Append` - Add data to existing table
- `Overwrite` - Replace existing table

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest -v tests/

# Run specific test
pytest tests/test_spark_event_extractor.py

# Run with coverage
pytest --cov=coffeeco tests/
```

## Key Features| Issue | Solution |

|-------|----------|
| `ModuleNotFoundError: No module named 'coffeeco'` | Set `PYTHONPATH` or install: `pip install -e .` |
| `RuntimeError: Missing Table: customers` | Create and populate the customers table in your Hive Metastore |
| Configuration not loading | Ensure `.env` file exists in application root |
| Pydantic validation errors | Verify all required variables in `.env` match `.env.example` |
| JDBC connection errors | Check MySQL is running and credentials in `.env` are correct |

## Additional Documentation

- **CONFIGURATION.md** - Complete configuration reference and environment variable guide
- **QUICKSTART.md** - Fast setup guide with common configurations
- **MIGRATION.md** - Notes on the Pydantic configuration system

## Development

### Installing Development Dependencies

```bash
pip install -r requirements-dev.txt
```

### Running the Test Configuration Script

```bash
python test_config.py
```

### Project Structure for Developers

The codebase follows a clear separation of concerns:

- **config/** - Configuration management with Pydantic
- **models/** - Data models as Python dataclasses
- **Core files** - Application base classes in inheritance order
- **Business logic** - Event extraction and transformation

## License

See the repository LICENSE file.
