"""
Command line argument parsing utilities for clickhouse migration scripts
"""
import os
import argparse

ARGS = {
    'SOURCE_TABLE': {'name': '--source-table', 'required': True},
    'SOURCE_DATABASE': {'name': '--source-database', 'required': False},
    'SOURCE_HOST': {'name': '--source-host', 'required': False},
    'SOURCE_PORT': {'name': '--source-port', 'required': False},
    'SOURCE_ADDRESS': {'name': '--source-address', 'required': False},
    'SOURCE_USERNAME': {'name': '--source-username', 'required': False},
    'SOURCE_PASSWORD': {'name': '--source-password', 'required': False},
    'DESTINATION_TABLE': {'name': '--destination-table', 'required': True},
    'DESTINATION_DATABASE': {'name': '--destination-database', 'required': False},
    'DESTINATION_HOST': {'name': '--destination-host', 'required': False},
    'DESTINATION_PORT': {'name': '--destination-port', 'required': False},
    'DESTINATION_ADDRESS': {'name': '--destination-address', 'required': False},
    'DESTINATION_USERNAME': {'name': '--destination-username', 'required': False},
    'DESTINATION_PASSWORD': {'name': '--destination-password', 'required': False},
}

CLIENT_ARGS = ['host', 'port', 'username', 'database', 'password']

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
    for _, args in ARGS.items():
        parser.add_argument(args['name'], required=args['required'])
    return parser.parse_args().__dict__

def get_config(prefix):
    """
    Return a dictionary of ClickHouse connection parameters with values from environment variables.
    
    The dictionary will contain the following keys: host, port, username, database, password.
    
    The values will be read from environment variables with names equal to the 
    prefix followed by the uppercase key name, for example: 
    prefix='SOURCE' will read from SOURCE_HOST, SOURCE_PORT, SOURCE_USERNAME, 
    SOURCE_DATABASE, SOURCE_PASSWORD.
    """
    return {arg: os.getenv(f'{prefix.upper()}_{arg.upper()}') for arg in CLIENT_ARGS}
