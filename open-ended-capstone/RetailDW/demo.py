import psycopg2
from psycopg2.extensions import connection 

from RetailDW.etlutils import create_table_src, incremental_load_src
from RetailDW.product import PRODUCT_TABLE, PRODUCT_CREATE_SQL_PG

def demo1() -> None:

    source_connection: connection = psycopg2.connect("dbname=postgres host=172.17.0.1 user=postgres password=postgres")
    
    total_inserts = 0
    total_updates = 0   

    create_table_src(source_connection, PRODUCT_CREATE_SQL_PG)

    inserted, updated = incremental_load_src(source_connection, PRODUCT_TABLE, n_inserts=5000, n_updates=0)
    total_inserts += inserted
    total_updates += updated
        
    for _ in range(5):
        inserted, updated = incremental_load_src(source_connection, PRODUCT_TABLE, n_inserts=200, n_updates=50)
        total_inserts += inserted
        total_updates += updated

    print(f"{total_inserts} inserts and {total_updates} updates processed.")

    source_connection.close()
