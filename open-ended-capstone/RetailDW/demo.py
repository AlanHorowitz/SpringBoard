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
    """ Initial load product and Stores tables

        Then loop through cycles where
        - Add many in Store Sales facts
        - Add update product information (fewer)
        - Add update store information (even fewer)
        - Extract/Load source to target.

    """
    TableBatch = namedtuple('TableBatch', ['table_object', 'n_inserts', 'n_updates'])

    # get connections and intialize systems

    InitialLoads = [TableBatch(PRODUCT_TABLE, 5000, 0), TableBatch(STORE_TABLE, 40, 0)]

    DailyOperations = [
        (TableBatch(PRODUCT_TABLE, 3, 5), TableBatch(STORE_TABLE, 3, 5)),
        (TableBatch(PRODUCT_TABLE, 10, 10), TableBatch(STORE_TABLE, 13, 52))
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

    create_source_tables(source_connection, [PRODUCT_TABLE, STORE_TABLE, STORE_SALES_TABLE])
    create_target_tables(target_connection, [PRODUCT_TABLE, STORE_TABLE, STORE_SALES_TABLE])

    timestamp = datetime.now()

    for batch in InitialLoads:

        inserted, _ = load_source_table(
                source_connection,
                batch.table_object,
                n_inserts=batch.n_inserts,
                n_updates=batch.n_updates,
                timestamp=timestamp,
                )

        print(f"{inserted} records inserted for table {batch.table_object.get_name()} at source: {timestamp}")
        
    for day in DailyOperations:

        for table in day:

            timestamp = datetime.now()

            inserted, updated = load_source_table(
            source_connection,
            table.table_object,
            n_inserts=table.n_inserts,
            n_updates=table.n_updates,
            timestamp=timestamp,
            )

            print(
            f"{inserted} inserts and {updated} updates for table {table.table_object.get_name()} processed at source."
            )
    
        for table in day:  # does the extract order matter?

            inserted, updated, from_time, to_time = extract_table_to_target(
            source_connection, target_connection, table.table_object)

            print(
                f"{inserted} inserts and {updated} updates for {table.table_object.get_name()} processed at target: From: {from_time} To: {to_time} "
            )

    source_connection.close()
    target_connection.close()