from datetime import datetime
from time import sleep
from collections import namedtuple

import psycopg2
from psycopg2.extensions import connection

import RetailDW.etlutils
import RetailDW.product
import RetailDW.store
import RetailDW.store_sales

source_connection: connection = psycopg2.connect(
        "dbname=retaildw host=172.17.0.1 user=user1 password=user1"
)

RetailDW.etlutils.create_table(source_connection, RetailDW.product.PRODUCT_CREATE_SQL_PG)
inserted, updated = RetailDW.etlutils.load_source_table(
    source_connection, RetailDW.product.PRODUCT_TABLE, n_inserts=50, n_updates=0)

RetailDW.etlutils.create_table(source_connection, RetailDW.store.STORE_CREATE_SQL_PG)
inserted, updated = RetailDW.etlutils.load_source_table(
    source_connection, RetailDW.store.STORE_TABLE, n_inserts=60, n_updates=0)

RetailDW.etlutils.create_table(source_connection, RetailDW.store_sales.STORE_SALES_CREATE_SQL_PG)
inserted, updated = RetailDW.etlutils.load_source_table(
    source_connection, RetailDW.store_sales.STORE_SALES_TABLE, n_inserts=70, n_updates=0)
