# Migration to Pydantic BaseSettings - Summary

## What Changed

The configuration system has been migrated from `pyhocon` (HOCON files) to **Pydantic BaseSettings** (environment variables).

## Files Modified

### 1. Dependencies

- **requirements.txt**: Replaced `pyhocon` with `pydantic`, `pydantic-settings`, and `python-dotenv`
- **setup.py**: Updated install_requires to use new dependencies

### 2. Configuration Files

- **src/coffeeco/data/config/configuration.py**: Complete rewrite using Pydantic BaseSettings
  - Removed HOCON parsing
  - Added `SparkSettings` class with Pydantic Field definitions
  - Added `Configuration` class extending BaseSettings
  - Type-safe configuration with validation

### 3. New Files Created

- **.env**: Environment variables file (git-ignored)
- **.env.example**: Example configuration template
- **tests/.env.test**: Test-specific environment configuration
- **CONFIGURATION.md**: Comprehensive configuration documentation
- **test_config.py**: Configuration validation test script

### 4. Documentation

- **README.md**: Updated configuration section to reflect Pydantic usage
- **.gitignore**: Added `.env` to ignore list (keeping `.env.example`)

## Key Benefits

### Type Safety

```python
# Before (pyhocon)
warehouse_dir = config.get("spark", {}).get("settings", {}).get("spark.sql.warehouse.dir", "")

# After (Pydantic)
warehouse_dir = config.spark.warehouse_dir  # Type-checked by IDE and Pydantic
```

### Validation

```python
# Pydantic automatically validates:
# - Required fields are present
# - Data types are correct
# - Values meet constraints
config = Configuration()  # Raises ValidationError if invalid
```

### Environment Variables

```bash
# Simple, standard environment variables
export APP_NAME=my-app
export SPARK__SQL__WAREHOUSE__DIR=/path/to/warehouse

# Or use .env file
echo "APP_NAME=my-app" >> .env
```

### IDE Support

- Autocompletion for configuration fields
- Type hints throughout
- Better refactoring support

## Migration Path

### For Developers

1. **Copy the example environment file**:

   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your settings**:

   ```bash
   vim .env
   ```

3. **Install new dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Test configuration**:
   ```bash
   python test_config.py
   ```

### For Production

1. **Set environment variables** in your deployment environment:

   ```bash
   export APP_NAME=spark-event-extractor
   export SPARK__SQL__WAREHOUSE__DIR=/production/warehouse
   # ... other variables
   ```

2. **Or mount a `.env` file** in your container/VM

## Configuration Mapping

### HOCON to Environment Variables

| HOCON Path                                                  | Environment Variable                   |
| ----------------------------------------------------------- | -------------------------------------- |
| `default.appName`                                           | `APP_NAME`                             |
| `default.spark.settings."spark.sql.catalogImplementation"`  | `SPARK__SQL__CATALOGIMPLEMENTATION`    |
| `default.spark.settings."spark.sql.warehouse.dir"`          | `SPARK__SQL__WAREHOUSE__DIR`           |
| `default.spark.settings."spark.sql.hive.metastore.version"` | `SPARK__SQL__HIVE__METASTORE__VERSION` |

## Backward Compatibility

The old `conf/local.conf` file is retained for reference but is no longer used. The application now exclusively uses Pydantic BaseSettings.

## Testing

Run the configuration test:

```bash
python test_config.py
```

Expected output:

```
Testing Pydantic BaseSettings Configuration
==================================================

✓ Configuration loaded successfully

Application Name: spark-event-extractor

Spark Settings:
  spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version: 2
  spark.hadoop.parquet.enable.summary-metadata: false
  spark.sql.catalogImplementation: hive
  ...

✓ Total Spark settings: 14

==================================================
Configuration validation successful!
```

## Troubleshooting

### Issue: ModuleNotFoundError: No module named 'pydantic_settings'

**Solution**: Install dependencies: `pip install -r requirements.txt`

### Issue: ValidationError on startup

**Solution**: Check `.env` file exists and contains all required variables

### Issue: Configuration not loading

**Solution**: Ensure `.env` is in the application root directory

## Next Steps

1. Review `.env.example` for all available configuration options
2. Set up your local `.env` file
3. Review `CONFIGURATION.md` for detailed documentation
4. Update any custom configuration code to use the new Pydantic classes

## Questions?

Refer to:

- `CONFIGURATION.md` - Detailed configuration guide
- `README.md` - Updated usage instructions
- `.env.example` - Configuration template
