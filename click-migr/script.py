import logging
import coloredlogs
import os
from dotenv import load_dotenv
from utils import get_config
import clickhouse_connect

logger = logging.getLogger(__name__)
coloredlogs.install(level="INFO", logger=logger)
load_dotenv()
config_src = get_config("SOURCE")
config_dest = get_config("DESTINATION")
source_client = clickhouse_connect.get_client(**config_src)
destination_client = clickhouse_connect.get_client(**config_dest)
try:
    df = source_client.query_df(f"SELECT * FROM {os.getenv('SOURCE_TABLE')}")
    logger.info("Read %d rows from source", len(df))
except Exception as e:
    logger.error("Error reading data from source: %s", e)

try:
    destination_client.insert_df(
        df=df,
        table=os.getenv("DESTINATION_TABLE"),
        database=config_dest["database"],
    )
    logger.info("Inserted %d rows into destination", len(df))
except Exception as e:
    logger.error("Error inserting data into destination: %s", e)
    raise

logger.info("Migration finished", extra={"color": "green"})
