import random
from typing import Tuple, Dict, List
from datetime import datetime

import psycopg2


from psycopg2.extras import DictCursor, DictRow
from psycopg2.extensions import connection, cursor

import mysql.connector
from mysql.connector import connect, Error

temp_date = datetime(2022, 3, 22, 14, 30, 0)

conn = psycopg2.connect(
    "dbname=postgres host=172.17.0.1 user=postgres password=postgres"
)

target_connection = connect(
    host="localhost",
    user="admin",
    password="admin",
    database="retaildw",
    charset="utf8",
)
mysql_cur = target_connection.cursor()

cur = conn.cursor(name="alan1")
cur.arraysize = 200


cur.execute("select * from product;")

r = cur.fetchall()
print(len(r))

mysql_cur.execute("Select MAX(product_updated_at) from Product")
ss = mysql_cur.fetchone()
print(len(ss))
print(ss)
print(ss[0])
print(type(ss[0]))

for _ in range(3):
    r = cur.fetchmany(1)
    print(len(r))
    print(type(r))

    column_names = """
    product_id, product_name ,product_description,
product_category,
product_brand,
product_preferred_supplier_id,
product_dimension_length,
product_dimension_width,
product_dimension_height,
product_introduced_date,
product_discontinued,
product_no_longer_offered,
product_inserted_at,
product_updated_at 
    """
    values_substitutions = ",".join(["%s"] * 14)  # each %s holds one tuple row
    mysql_cur.executemany(
        f"REPLACE INTO Product ({column_names}) values ({values_substitutions})", r,
    )
    print(" affected rows", mysql_cur.rowcount)

# i = 0
# for row in cur:
#     if i < 5:
#         print(type(row))
#         print(row)
#     i += 1
target_connection.commit()
conn.commit()
