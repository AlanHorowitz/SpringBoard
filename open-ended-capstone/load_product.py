from sqlalchemy import create_engine, MetaData, Table, Column
from sqlalchemy import select, insert, update, delete
from sqlalchemy import Integer, String, Boolean, DECIMAL

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
            elif col_type == 'DATE':
                val = '2021-02-11 12:52:47'
            elif col_type == 'TINYINT':
                val = 0
            else:
                val = "UNKNOWN TYPE"

            d[col.name] = val

        insert_records.append(d)

    stmt = insert(table)
    print('rows inserted', conn.execute(stmt,insert_records).rowcount)

engine = create_engine('mysql+pymysql://alan:alan@localhost/product')
meta = MetaData()
conn = engine.connect()

product = Table('Product', meta, autoload=True, autoload_with=engine)

insert_n(product,1,10)

conn.close()
product.drop(engine)

