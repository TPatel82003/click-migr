"""
Command line argument parsing utilities for clickhouse migration scripts
"""

import os
import argparse

ARGS = {
    "SOURCE_TABLE": {"name": "--source-table"},
    "SOURCE_DATABASE": {"name": "--source-database"},
    "SOURCE_HOST": {"name": "--source-host"},
    "SOURCE_PORT": {"name": "--source-port"},
    "SOURCE_USERNAME": {"name": "--source-username"},
    "SOURCE_PASSWORD": {"name": "--source-password"},
    "DESTINATION_TABLE": {"name": "--destination-table"},
    "DESTINATION_DATABASE": {"name": "--destination-database"},
    "DESTINATION_HOST": {"name": "--destination-host"},
    "DESTINATION_PORT": {"name": "--destination-port"},
    "DESTINATION_USERNAME": {"name": "--destination-username"},
    "DESTINATION_PASSWORD": {"name": "--destination-password"},
}

CLIENT_ARGS = ["host", "port", "username", "database", "password"]


def get_args():
    """Return a dictionary of command line arguments parsed from sys.argv.

    The returned dictionary will contain the following keys:

    - source_table
    - source_database
    - source_host
    - source_port
    - source_address
    - source_username
    - source_password
    - destination_table
    - destination_database
    - destination_host
    - destination_port
    - destination_address
    - destination_username
    - destination_password

    The values will be read from sys.argv or from environment variables with names equal to the
    uppercase key name, for example: SOURCE_TABLE, SOURCE_DATABASE, SOURCE_HOST, etc.
    """
    parser = argparse.ArgumentParser()
    for key, args in ARGS.items():
        parser.add_argument(args["name"], default=os.environ.get(key.upper()))
    return parser.parse_args().__dict__


def validate_field():
    """
    Validate that all required environment variables are set.

    If any environment variable is missing, raise a ValueError with a message
    indicating which variables are missing and how to set them.

    Raises:
        ValueError: If any required environment variable is missing.
    """
    if any(os.getenv(key) is None for key in ARGS):
        missing = [key for key in ARGS if os.getenv(key) is None]
        raise ValueError(
            "Missing required environment variables.\n"
            f"Please add the following environment variables: {', '.join(missing)}.\n"
            "You can do this by adding them to your .env file or by setting them in your OS\n"
        )

def get_config(prefix):
    """
    Return a dictionary of ClickHouse connection parameters with values from environment variables.

    The dictionary will contain the following keys: host, port, username, database, password.

    The values will be read from environment variables with names equal to the
    prefix followed by the uppercase key name, for example:
    prefix='SOURCE' will read from SOURCE_HOST, SOURCE_PORT, SOURCE_USERNAME,
    SOURCE_DATABASE, SOURCE_PASSWORD.
    """
    return {arg: os.getenv(f"{prefix.upper()}_{arg.upper()}") for arg in CLIENT_ARGS}
