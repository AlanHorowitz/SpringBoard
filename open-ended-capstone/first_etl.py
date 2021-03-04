from sqlalchemy import create_engine, MetaData, Table, Column 
from sqlalchemy import select, insert, update, delete
from sqlalchemy import INTEGER, String, BOOLEAN, DECIMAL, VARCHAR, DATE, REAL
from sqlalchemy.orm import Session

import shutil
import os

def insert_n(table,conn,start, n):
    '''
    Insert n records of dummy data into table
    '''  
    insert_records = []
    for i in range(start, start + n):

        d = {} 
        for col in table.columns:

            col_type = col.type.__visit_name__
            if col_type == 'INTEGER':
                val = i
            elif col_type == 'VARCHAR':
                val = 'AAA'
            elif col_type == 'FLOAT':
                val = 5.0
            elif col_type == 'REAL':
                val = 5.0
            elif col_type == 'DATE':
                val = '2021-02-11 12:52:47'
            elif col_type == 'TINYINT':
                val = 0
            elif col_type == 'BOOLEAN':
                val = 1
            else:
                print(f"column type {col_type} not found")
                val = None

            d[col.name] = val

        insert_records.append(d)

    stmt = insert(table)
    
    print('rows inserted', conn.execute(stmt,insert_records).rowcount)

def load_source_system(engine, table):

    conn = engine.connect()
    session = Session(bind=conn)

    table.drop(engine, checkfirst=True)
    table.create(engine)
    insert_n(product,conn,1,1000)

    session.commit()
    session.close()
    conn.close()

def extract_source_system_to_csv(engine, table, directory):

    conn = engine.connect()
    session = Session(bind=conn)

    # postgres command writes .csv to a readable mapped directory on docker host
    conn.execute("COPY product to '/tmp/postgres_out/first_etl.csv'")

    session.commit()
    session.close()
    conn.close()

    # copy file to etl input directory
    shutil.copy('pgsql_tmp/postgres_out/first_etl.csv', directory)
    shutil.move

def transform_load_from_csv(engine, table, directory):
    
    conn = engine.connect()
    session = Session(bind=conn)

    product.drop(engine, checkfirst=True)
    product.create(engine)

    infile = directory + "/first_etl.csv"

    s = "LOAD DATA LOCAL" \
    f" INFILE '{infile}'" \
    " INTO TABLE product" \
    " FIELDS terminated by '\t'" \
    " enclosed by '\"' " \
    "(product_id," \
    "product_name," \
    "product_description," \
    "product_category," \
    "product_brand," \
    "product_preferred_supplier_id," \
    "product_dimension_length," \
    "product_dimension_width," \
    "product_dimension_height," \
    "product_introduced_date," \
    "@product_discontinued," \
    "@product_no_longer_offered)" \
    "SET product_discontinued = CASE when @product_discontinued = 't' then 1 ELSE 0 END," \
    "    product_no_longer_offered = CASE when @product_no_longer_offered = 't' then 1 ELSE 0 END;"

    conn.execute(s)
    session.commit()
    session.close()

    conn.close()

    os.remove(infile)

if __name__ == '__main__':    
    '''
    Create and load a new Product table on Postgres.  Use copy command to dump to csv
    Create and load a new Product table on MySQL.  Use LOAD DATA to import csv.  Handle mismatch in Boolean type
    '''

    engine_source = create_engine("postgresql+pg8000://postgres:postgres@172.17.0.1:5432/postgres", 
            client_encoding ='utf-8')

    engine_warehouse = create_engine('mysql+pymysql://alan:alan@localhost/edw?local_infile=1') 

    product = Table('product', MetaData(),
        Column('product_id', INTEGER(), primary_key=True, nullable=False),
        Column('product_name', VARCHAR(length=80), nullable=False),
        Column('product_description', VARCHAR(length=255)),
        Column('product_category', VARCHAR(length=80)),
        Column('product_brand', VARCHAR(length=80)),
        Column('product_preferred_supplier_id', INTEGER()),
        Column('product_dimension_length', REAL()),
        Column('product_dimension_width', REAL()),
        Column('product_dimension_height', REAL()),
        Column('product_introduced_date', DATE()),
        Column('product_discontinued', BOOLEAN(), default=False),
        Column('product_no_longer_offered', BOOLEAN(),default=False)
    )    

    load_source_system(engine_source, product)
    extract_source_system_to_csv(engine_source, product, 'mysql_in')
    transform_load_from_csv(engine_warehouse, product, 'mysql_in')