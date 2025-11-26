#!/usr/bin/env python3
"""
Configuration Test Script

This script verifies that the Pydantic configuration is working correctly.
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from coffeeco.data.config.configuration import Configuration


def main():
    """Test configuration loading"""
    print("Testing Pydantic BaseSettings Configuration")
    print("=" * 50)

    try:
        # Load configuration
        config = Configuration()

        print(f"\n✓ Configuration loaded successfully")
        print(f"\nApplication Name: {config.app_name}")
        print(f"\nSpark Settings:")

        spark_settings = config.spark_settings
        for key, value in sorted(spark_settings.items()):
            print(f"  {key}: {value}")

        print(f"\n✓ Total Spark settings: {len(spark_settings)}")
        print("\n" + "=" * 50)
        print("Configuration validation successful!")

    except Exception as e:
        print(f"\n✗ Configuration error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
