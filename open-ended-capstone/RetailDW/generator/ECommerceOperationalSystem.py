from util.sqltypes import Table, Column
from typing import List
from .OperationalSystem import OperationalSystem

import psycopg2
from psycopg2.extras import DictCursor, DictRow
from psycopg2.extensions import connection, cursor

from util.etlutils import create_table


class eCommerceOperationalSystem(OperationalSystem):
    def __init__(self) -> None:
        # open connection to postgres
        self.connection: connection = psycopg2.connect(
        "dbname=retaildw host=172.17.0.1 user=user1 password=user1"
        )

        self.cur: cursor = self.connection.cursor(cursor_factory=DictCursor)
        self.cur.execute("CREATE SCHEMA ECOMMERCE;")
        self.cur.execute("SET SEARCH_PATH TO ECOMMERCE;")
        self.connection.commit()
       
        pass

    def add_tables(self, tables : List[Table]) -> None:
        # create all the postgres tables
        for table in tables:
            table.setOperationalSystem(self)
            create_table(self.connection, table.get_create_sql_postgres())         

    def remove_tables():
        pass

    def open(table : Table) -> None:
        pass

    def close(table):
        pass

    def insert(table, records):
        pass

    def update(table, records):
        pass