from datetime import datetime
from time import sleep
from collections import namedtuple

import psycopg2
from psycopg2.extensions import connection

import mysql.connector
from mysql.connector import connect

from RetailDW.etlutils import (
    create_table,
    create_source_tables,
    create_target_tables,
    load_source_table,
    extract_table_to_target,
    ETL_HISTORY_CREATE_MYSQL,
)
from RetailDW.product import (
    PRODUCT_TABLE,
    PRODUCT_CREATE_SQL_PG,
    PRODUCT_CREATE_SQL_MYSQL,
)

from RetailDW.store import (
    STORE_TABLE,
    STORE_CREATE_SQL_PG,
    STORE_CREATE_SQL_MYSQL,
)

from RetailDW.store_sales import (
    STORE_SALES_TABLE,
    STORE_SALES_CREATE_SQL_PG,
    STORE_SALES_CREATE_SQL_MYSQL,
)


def demo1() -> None:
    """Initial and incremental load into product table.

    Create the product table and load 5000 rows.  Then run a loop of 5 incremental loads, each having 200 
    inserts and 50 updates.
    """
    source_connection: connection = psycopg2.connect(
        "dbname=retaildw host=172.17.0.1 user=user1 password=user1"
    )

    total_inserts = 0
    total_updates = 0

    create_table(source_connection, PRODUCT_CREATE_SQL_PG)

    inserted, updated = load_source_table(
        source_connection, PRODUCT_TABLE, n_inserts=5000, n_updates=0
    )
    total_inserts += inserted
    total_updates += updated

    for _ in range(5):
        inserted, updated = load_source_table(
            source_connection, PRODUCT_TABLE, n_inserts=200, n_updates=50
        )
        total_inserts += inserted
        total_updates += updated

    print(f"{total_inserts} inserts and {total_updates} updates processed.")

    source_connection.close()


def demo2() -> None:
    """Load Product records to source system and extract to target system. 

    Create the product table and load 5000 rows to the source system.  Then run a loop of 5 incremental loads, each
    having 200 inserts and 50 updates. After each incremental load, extract records from the source system to the 
    target system. The extract only reads data updated since the prior extract.
    
    Insert and update counts are printed after each operation.
    """
    source_connection: connection = psycopg2.connect(
        dbname="retaildw", host="172.17.0.1", user="user1", password="user1"
    )
    target_connection: connection = connect(
        host="172.17.0.1",
        user="user1",
        password="user1",
        database="retaildw",
        charset="utf8",
    )

    total_inserts_source = 0
    total_updates_source = 0
    total_inserts_target = 0
    total_updates_target = 0

    timestamp = datetime.now()

    create_table(source_connection, PRODUCT_CREATE_SQL_PG)
    create_table(target_connection, PRODUCT_CREATE_SQL_MYSQL)
    create_table(target_connection, ETL_HISTORY_CREATE_MYSQL)

    inserted, updated = load_source_table(
        source_connection,
        PRODUCT_TABLE,
        n_inserts=5000,
        n_updates=0,
        timestamp=timestamp,
    )

    print(f"{inserted} inserts and {updated} updates processed at source: {timestamp}.")

    total_inserts_source += inserted
    total_updates_source += updated

    for _ in range(5):

        sleep(3)
        timestamp = datetime.now()
        inserted, updated = load_source_table(
            source_connection,
            PRODUCT_TABLE,
            n_inserts=200,
            n_updates=50,
            timestamp=timestamp,
        )

        print(
            f"{inserted} inserts and {updated} updates processed at source: {timestamp}."
        )

        total_inserts_source += inserted
        total_updates_source += updated

        inserted, updated, from_time, to_time = extract_table_to_target(
            source_connection, target_connection, PRODUCT_TABLE
        )

        print(
            f"{inserted} inserts and {updated} updates processed at target: From: {from_time} To: {to_time} "
        )

        total_inserts_target += inserted
        total_updates_target += updated

    print(
        f"{total_inserts_source} inserts and {total_updates_source} updates processed at source."
    )
    print(
        f"{total_inserts_target} inserts and {total_updates_target} updates processed at target."
    )

    source_connection.close()
    target_connection.close()


def demo3() -> None:
    """ Demonstrate three days operation of ETL system using product, store and store_sales tables.

        Day 1: Load 5000 products and 40 stores to source system
               Extract and load all to target. 

        Day 2: Load 5 new products and update 50 existing products to source system
               Load 0 new stores and update 2 existing stores to source system 
               Load 50000 new store_sales records
               Extract and load all to target. 

        Day 3: Load 10 new products and update 30 existing products to source system
               Load 1 new stores and update 0 existing stores to source system 
               Load 50000 new store_sales records
               Extract and load all to target.
                
    """
    # represent batch of inserts and updates on a table.
    TableBatch = namedtuple("TableBatch", ["table_object", "n_inserts", "n_updates"])

    DailyOperations = [
        (TableBatch(PRODUCT_TABLE, 5000, 0), TableBatch(STORE_TABLE, 40, 0)),
        (
            TableBatch(PRODUCT_TABLE, 5, 50),
            TableBatch(STORE_TABLE, 0, 2),
            TableBatch(STORE_SALES_TABLE, 50000, 0),
        ),
        (
            TableBatch(PRODUCT_TABLE, 10, 30),
            TableBatch(STORE_TABLE, 1, 0),
            TableBatch(STORE_SALES_TABLE, 50000, 0),
        ),
    ]

    source_connection: connection = psycopg2.connect(
        dbname="retaildw", host="172.17.0.1", user="user1", password="user1"
    )

    target_connection: connection = connect(
        host="172.17.0.1",
        user="user1",
        password="user1",
        database="retaildw",
        charset="utf8",
    )

    create_source_tables(
        source_connection, [PRODUCT_TABLE, STORE_TABLE, STORE_SALES_TABLE]
    )
    create_target_tables(
        target_connection, [PRODUCT_TABLE, STORE_TABLE, STORE_SALES_TABLE]
    )

    timestamp = datetime.now()
    day = 1

    for batch_list in DailyOperations:

        print(f"Day {day} of operations")

        for batch in batch_list:

            timestamp = datetime.now()

            inserted, updated = load_source_table(
                source_connection,
                batch.table_object,
                n_inserts=batch.n_inserts,
                n_updates=batch.n_updates,
                timestamp=timestamp,
            )

            print(
                f"{inserted} inserts and {updated} updates for table {batch.table_object.get_name()} processed at source: {timestamp}"
            )

        for batch in batch_list:

            inserted, updated, from_time, to_time = extract_table_to_target(
                source_connection, target_connection, batch.table_object
            )

            print(
                f"{inserted} inserts and {updated} updates for {batch.table_object.get_name()} processed at target: From: {from_time} To: {to_time} "
            )

        day += 1

    source_connection.close()
    target_connection.close()
