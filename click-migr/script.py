"""
Data migration script for ClickHouse.

This script reads data from a source ClickHouse table and inserts it into a destination
ClickHouse table.

Environment variables required:

- SOURCE_TABLE: Name of the source table.
- SOURCE_DATABASE: Name of the source database.
- SOURCE_HOST: Hostname of the source ClickHouse server.
- SOURCE_PORT: Port number of the source ClickHouse server.
- SOURCE_USERNAME: Username for the source ClickHouse server.
- SOURCE_PASSWORD: Password for the source ClickHouse server.

- DESTINATION_TABLE: Name of the destination table.
- DESTINATION_DATABASE: Name of the destination database.
- DESTINATION_HOST: Hostname of the destination ClickHouse server.
- DESTINATION_PORT: Port number of the destination ClickHouse server.
- DESTINATION_USERNAME: Username for the destination ClickHouse server.
- DESTINATION_PASSWORD: Password for the destination ClickHouse server.
"""

import logging
import coloredlogs
import os
from dotenv import load_dotenv
from utils import get_config, validate_field
import clickhouse_connect


load_dotenv()

logger = logging.getLogger(__name__)
coloredlogs.install(level="INFO", logger=logger)
validate_field()

# Get the source table and read the data
source_table = os.getenv("SOURCE_TABLE")
source_client = clickhouse_connect.get_client(**get_config("SOURCE"))
try:
    df = source_client.query_df(f"SELECT * FROM {source_table}")
    logger.info(f"Successfully read {len(df)} rows from source table {source_table}")
except ValueError as e:
    logger.error(
        f"Error reading data from source table {source_table}: {e}", exc_info=True
    )

# Get the destination table and insert the data
destination_table = os.getenv("DESTINATION_TABLE")
destination_client = clickhouse_connect.get_client(**get_config("DESTINATION"))
try:
    destination_client.insert_df(
        df=df,
        table=destination_table,
        database=os.getenv("DESTINATION_DATABASE"),
    )
    logger.info(
        f"Successfully inserted {len(df)} rows into destination table {destination_table}"
    )
except ValueError as e:
    logger.error(
        f"Error inserting data into destination table {destination_table}: {e}",
        exc_info=True,
    )

logger.info("Data migration finished successfully", extra={"color": "green"})
