from RetailDW.sqltypes import Table, Column
from typing import List
from RetailDW.generator.OperationalSystem import OperationalSystem

class ECommerceOperationalSystem(OperationalSystem):
    def __init__(self) -> None:
        # open connection to postgres
        pass

    def add_tables(tables : List[Table]) -> None:
        # create all the postgres tables
        pass

    def open(table : Table) -> None:
        pass

    def close(table):
        pass

    def insert(table, records):
        pass

    def update(table, records):
        pass