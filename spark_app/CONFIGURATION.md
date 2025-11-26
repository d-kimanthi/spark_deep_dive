# Configuration Guide

## Overview

This application uses **Pydantic BaseSettings** for configuration management, which provides:

- Type-safe configuration with validation
- Environment variable support
- Clear error messages for missing or invalid configuration
- IDE autocompletion support

## Configuration Sources

Configuration values are loaded in the following order (later sources override earlier ones):

1. Default values in the `Configuration` class
2. `.env` file in the application root
3. Environment variables
4. Programmatic configuration (when instantiating the `Configuration` class)

## Environment Variables

### Naming Convention

Environment variables use double underscores (`__`) to represent nested configuration:

```
SPARK__SQL__CATALOGIMPLEMENTATION → spark.sql.catalogImplementation
SPARK__SQL__HIVE__METASTORE__VERSION → spark.sql.hive.metastore.version
```

### Application Configuration

```bash
# Application name
APP_NAME=spark-event-extractor
```

### Spark SQL Configuration

```bash
# Catalog implementation
SPARK__SQL__CATALOGIMPLEMENTATION=hive

# Warehouse directory
SPARK__SQL__WAREHOUSE__DIR=file:///path/to/warehouse
```

### Hive Metastore Configuration

```bash
# Metastore version
SPARK__SQL__HIVE__METASTORE__VERSION=2.3.7

# Metastore JARs
SPARK__SQL__HIVE__METASTORE__JARS=builtin

# Shared prefixes
SPARK__SQL__HIVE__METASTORE__SHAREDPREFIXES=com.mysql.cj.jdbc,com.mysql.jdbc,org.postgresql

# Schema verification
SPARK__SQL__HIVE__METASTORE__SCHEMA__VERIFICATION=true
SPARK__SQL__HIVE__METASTORE__SCHEMA__VERIFICATION__RECORD__VERSION=true
```

### JDBC Connection Configuration

```bash
# Connection URL
SPARK__SQL__HIVE__JAVAX__JDO__OPTION__CONNECTIONURL=jdbc:mysql://mysql:3306/metastore

# Driver name
SPARK__SQL__HIVE__JAVAX__JDO__OPTION__CONNECTIONDRIVERNAME=com.mysql.cj.jdbc.Driver

# Username
SPARK__SQL__HIVE__JAVAX__JDO__OPTION__CONNECTIONUSERNAME=dataeng

# Password (optional, can be passed via spark-submit --conf)
SPARK__SQL__HIVE__JAVAX__JDO__OPTION__CONNECTIONPASSWORD=your_password
```

### Parquet Configuration

```bash
# Compression codec
SPARK__SQL__PARQUET__COMPRESSION__CODEC=snappy

# Merge schema
SPARK__SQL__PARQUET__MERGESCHEMA=false

# Filter pushdown
SPARK__SQL__PARQUET__FILTERPUSHDOWN=true
```

### Hadoop Configuration

```bash
# Parquet summary metadata
SPARK__HADOOP__PARQUET__ENABLE__SUMMARY_METADATA=false

# File output committer algorithm version
SPARK__HADOOP__MAPREDUCE__FILEOUTPUTCOMMITTER__ALGORITHM__VERSION=2
```

## Using the .env File

1. **Copy the example file**:

   ```bash
   cp .env.example .env
   ```

2. **Edit the `.env` file** with your specific values:

   ```bash
   vim .env
   # or
   nano .env
   ```

3. **Keep sensitive data secure**:
   - The `.env` file is git-ignored by default
   - Never commit `.env` files to version control
   - Use `.env.example` to document required variables

## Programmatic Configuration

You can override configuration programmatically:

```python
from coffeeco.data.config.configuration import Configuration, SparkSettings

# Custom configuration
config = Configuration(
    app_name="my-custom-app",
    spark=SparkSettings(
        warehouse_dir="file:///my/custom/warehouse",
        catalog_implementation="hive"
    )
)

# Access configuration
print(config.app_name)
print(config.spark_settings)
```

## Configuration in Tests

Tests use a separate `.env.test` file with test-specific configuration:

```bash
# tests/.env.test
APP_NAME=spark-event-extractor-test
SPARK__SQL__WAREHOUSE__DIR=file:///tmp/spark-warehouse-test
```

To use test configuration:

```python
import os
os.environ['ENV_FILE'] = 'tests/.env.test'

from coffeeco.data.config.configuration import Configuration
config = Configuration()
```

## Validation

Pydantic automatically validates configuration:

```python
# Invalid configuration will raise validation errors
config = Configuration(
    spark=SparkSettings(
        warehouse_dir=""  # ValidationError: String should have at least 1 character
    )
)
```

## Best Practices

1. **Use .env files for local development**
2. **Use environment variables in production**
3. **Keep sensitive data (passwords, keys) out of .env.example**
4. **Document all required variables in .env.example**
5. **Use type hints for custom configuration classes**
6. **Validate configuration early in application startup**

## Migration from HOCON

If you're migrating from the HOCON configuration:

### Old (HOCON):

```hocon
default {
  appName = "spark-event-extractor"
  spark {
    settings {
      "spark.sql.catalogImplementation" = "hive"
    }
  }
}
```

### New (Environment Variables):

```bash
APP_NAME=spark-event-extractor
SPARK__SQL__CATALOGIMPLEMENTATION=hive
```

## Troubleshooting

### Configuration Not Loading

- Check that `.env` file exists in the application root
- Verify environment variable names match the expected format
- Ensure no typos in variable names (case-insensitive)

### Validation Errors

- Check Pydantic error messages for specific field issues
- Verify all required fields are set
- Check data types match expected types

### Connection Issues

- Verify JDBC connection URL is correct
- Check database credentials
- Ensure database is accessible from the application

## Example Complete Configuration

See `.env.example` for a complete example configuration file.
