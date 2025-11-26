# Quick Start Guide - Pydantic Configuration

## Setup (30 seconds)

```bash
# 1. Copy environment template
cp .env.example .env

# 2. Edit configuration (update paths and credentials)
vim .env

# 3. Install dependencies
pip install -r requirements.txt

# 4. Test configuration
python test_config.py
```

## Basic Usage

### Loading Configuration

```python
from coffeeco.data.config.configuration import Configuration

# Load from .env file (automatically)
config = Configuration()

# Access values
print(config.app_name)
print(config.spark.warehouse_dir)

# Get Spark settings dict
spark_settings = config.spark_settings
```

### Setting Environment Variables

```bash
# In your shell
export APP_NAME=my-app
export SPARK__SQL__WAREHOUSE__DIR=/path/to/warehouse

# Or in .env file
echo "APP_NAME=my-app" >> .env
echo "SPARK__SQL__WAREHOUSE__DIR=/path/to/warehouse" >> .env
```

### Programmatic Configuration

```python
from coffeeco.data.config.configuration import Configuration, SparkSettings

config = Configuration(
    app_name="custom-app",
    spark=SparkSettings(
        warehouse_dir="file:///custom/path"
    )
)
```

## Common Configurations

### Local Development

```bash
# .env
APP_NAME=spark-event-extractor-local
SPARK__SQL__WAREHOUSE__DIR=file:///tmp/spark-warehouse
SPARK__SQL__HIVE__JAVAX__JDO__OPTION__CONNECTIONURL=jdbc:mysql://localhost:3306/metastore
```

### Docker/Container

```bash
# .env
APP_NAME=spark-event-extractor
SPARK__SQL__WAREHOUSE__DIR=file:///app/spark-warehouse
SPARK__SQL__HIVE__JAVAX__JDO__OPTION__CONNECTIONURL=jdbc:mysql://mysql:3306/metastore
SPARK__SQL__HIVE__JAVAX__JDO__OPTION__CONNECTIONUSERNAME=dataeng
SPARK__SQL__HIVE__JAVAX__JDO__OPTION__CONNECTIONPASSWORD=${DB_PASSWORD}
```

### Production

```bash
# Set as environment variables in your deployment platform
export APP_NAME=spark-event-extractor-prod
export SPARK__SQL__WAREHOUSE__DIR=hdfs://namenode:9000/spark/warehouse
export SPARK__SQL__HIVE__JAVAX__JDO__OPTION__CONNECTIONURL=jdbc:mysql://prod-db:3306/metastore
```

## Verification

```bash
# Test that configuration loads correctly
python test_config.py

# Run application
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
spark-submit \
  --master "local[*]" \
  --conf "spark.event.extractor.source.table=bronze.customerRatings" \
  --conf "spark.event.extractor.destination.table=silver.customerRatings" \
  src/coffeeco/data/spark_event_extractor_app.py
```

## Troubleshooting

| Issue                      | Solution                                                 |
| -------------------------- | -------------------------------------------------------- |
| `.env` file not found      | Copy `.env.example` to `.env`                            |
| Missing dependencies       | Run `pip install -r requirements.txt`                    |
| Validation errors          | Check all required variables are set in `.env`           |
| Wrong configuration values | Verify environment variable names use double underscores |

## Documentation

- **CONFIGURATION.md** - Complete configuration reference
- **MIGRATION.md** - Migration guide from HOCON
- **README.md** - Full application documentation
- **.env.example** - Configuration template with all options

## Key Points

✓ Configuration uses environment variables (`.env` file or shell exports)
✓ Variable names use double underscores: `SPARK__SQL__CATALOGIMPLEMENTATION`
✓ Type-safe with Pydantic validation
✓ IDE autocomplete support
✓ Clear error messages for invalid configuration
