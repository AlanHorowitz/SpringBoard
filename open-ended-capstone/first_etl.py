from sqlalchemy import create_engine, MetaData, Table, Column 
from sqlalchemy import select, insert, update, delete
from sqlalchemy import INTEGER, String, BOOLEAN, DECIMAL, VARCHAR, DATE, REAL
from sqlalchemy.orm import Session

def insert_n(table, start, n):
    '''
    Insert n records into table
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
                # val = "UNKNOWN TYPE"

            d[col.name] = val

        insert_records.append(d)

    stmt = insert(table)
    
    print('rows inserted', conn.execute(stmt,insert_records).rowcount)

engine = create_engine("postgresql+pg8000://postgres:postgres@172.17.0.1:5432/postgres", 
client_encoding ='utf-8')
meta = MetaData()
conn = engine.connect()
session = Session(bind=conn)

product = Table('product', meta,
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

product.drop(engine, checkfirst=True)
product.create(engine)
    
insert_n(product,1,17)

session.commit()
session.close()

conn.execute("COPY product to '/tmp/alanpostgres/test2.csv'")

session.commit()
session.close()

conn.close()

engine2 = create_engine('mysql+pymysql://alan:alan@localhost/edw?local_infile=1') 

meta2 = MetaData()
conn = engine2.connect()
session = Session(bind=conn)

product = Table('product', meta2,
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
product.drop(engine2, checkfirst=True)
product.create(engine2)

session.commit()
session.close()

s = "LOAD DATA LOCAL" \
" INFILE '/home/alan/docker_pgsql_extract/alanpostgres/test2.csv'" \
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
