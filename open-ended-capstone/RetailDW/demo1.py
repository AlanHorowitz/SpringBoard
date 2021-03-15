import psycopg2

from RetailDW.etlutils import create_table_src, incremental_load_src
from RetailDW.product import PRODUCT_TABLE, PRODUCT_CREATE_SQL_PG

def run():

    src_conn = psycopg2.connect("dbname=postgres host=172.17.0.1 user=postgres password=postgres")

    total_inserts = 0
    total_updates = 0   

    create_table_src(src_conn, PRODUCT_CREATE_SQL_PG)

    i, u = incremental_load_src(src_conn, PRODUCT_TABLE, n_inserts=5000, n_updates=0)
    total_inserts += i
    total_updates += u
        
    for _ in range(5):
        i, u = incremental_load_src(src_conn, PRODUCT_TABLE, n_inserts=200, n_updates=50)
        total_inserts += i
        total_updates += u
   
    print(f"{total_inserts} inserts and {total_updates} updates processed.")

    src_conn.close()
