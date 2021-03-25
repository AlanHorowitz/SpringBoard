from datetime import datetime, timedelta

import psycopg2
from psycopg2.extensions import connection

from RetailDW.etlutils import create_table, incremental_load
from RetailDW.product import PRODUCT_TABLE, PRODUCT_CREATE_SQL_PG


def demo1() -> None:
    """Initial and incremental load into product table.

    Create the product table and load 5000 rows.  Then run a loop of 5 incremental loads, each having 200 
    inserts and 50 updates.
    """
    source_connection: connection = psycopg2.connect(
        "dbname=postgres host=172.17.0.1 user=postgres password=postgres"
    )

    total_inserts = 0
    total_updates = 0

    create_table(source_connection, PRODUCT_CREATE_SQL_PG)

    inserted, updated = incremental_load(
        source_connection, PRODUCT_TABLE, n_inserts=5000, n_updates=0
    )
    total_inserts += inserted
    total_updates += updated

    for _ in range(5):
        inserted, updated = incremental_load(
            source_connection, PRODUCT_TABLE, n_inserts=200, n_updates=50
        )
        total_inserts += inserted
        total_updates += updated

    print(f"{total_inserts} inserts and {total_updates} updates processed.")

    source_connection.close()


def demo2() -> None:
    """Initial and incremental load into product table.

    Create the product table and load 5000 rows.  Then run a loop of 5 incremental loads, each having 200 
    inserts and 50 updates.
    """
    source_connection: connection = psycopg2.connect(
        "dbname=postgres host=172.17.0.1 user=postgres password=postgres"
    )

    total_inserts_source = 0
    total_updates_source = 0
    total_inserts_target = 0
    total_updates_target = 0
    timestamp = datetime(2021, 1, 11, 12, 0, 0)

    create_table(source_connection, PRODUCT_CREATE_SQL_PG)
    create_table(target_connection, PRODUCT_CREATE_SQL_MYSQL)
    create_table(target_connection, ETL_HISTORY)

    inserted, updated = incremental_load(
        source_connection,
        PRODUCT_TABLE,
        n_inserts=5000,
        n_updates=0,
        timestamp=timestamp,
    )

    print(f"{inserted} inserts processed. Initial load {timestamp}")

    total_inserts_source += inserted
    total_updates_source += updated
    timestamp += timedelta(days=1)
    
    for _ in range(5):
        inserted, updated = incremental_load(
            source_connection,
            PRODUCT_TABLE,
            n_inserts=200,
            n_updates=50,
            timestamp=timestamp
        )

        print(f"{inserted} inserts and {updated} processed. Incremental load {timestamp}")

        total_inserts_source += inserted
        total_updates_source += updated
        
        inserted, updated, from_time, to_time = extract_to_target(
            source_connection,
            target_connection,
            PRODUCT_TABLE            
        )

        print(f"{inserted} inserts and {updated} extracted to target. From: {from_time} To: {to_time} ")

        total_inserts_target += inserted
        total_updates_target += updated
        timestamp += timedelta(days=1)

    print(f"{total_inserts_source} inserts and {total_updates_source} updates loaded to source system.")
    print(f"{total_inserts_target} inserts and {total_updates_target} updates extracted to target system.")

    source_connection.close()
