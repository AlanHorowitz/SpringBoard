import random
import psycopg2
import psycopg2.extras

class Column():

    def __init__(self, column_name, column_type, isPrimaryKey=False):

        self._name = column_name
        self._type = column_type
        self._isPrimaryKey = isPrimaryKey

    def get_name(self):

        return self._name

    def get_type(self):

        return self._type

    def isPrimaryKey(self):

        return self._isPrimaryKey

class Table():

    def __init__(self, name, *columns):

        self._name = name
        self._columns= [ col for col in columns ] 
        primary_keys = [ col.get_name() for col in columns if col.isPrimaryKey() ] 
        if len(primary_keys) != 1:
            raise Exception("Simulator requires exactly one primary key")
        self._primary_key = primary_keys[0]
        self._update_columns = [col for col in columns if col.get_type() == 'VARCHAR']  # restrict to VARCHAR update
        if len(primary_keys) == 0:
            raise Exception("Need at least one VARCHAR for update")

    def get_name(self):

        return self._name

    def get_columns(self):

        return self._columns

    def get_primary_key(self):

        return self._primary_key

    def get_column_names(self):

        return [col.get_name() for col in self._columns] 

    def get_update_column(self):

        i = random.randint(0,len(self._update_columns)-1)   
        return self._update_columns[i]

CREATE_SQL_PG = \
" CREATE TABLE IF NOT EXISTS Product ("\
" product_id INTEGER NOT NULL,  "\
" product_name VARCHAR(80) NOT NULL,"\
" product_description VARCHAR(255) NULL DEFAULT NULL,"\
" product_category VARCHAR(80) NULL DEFAULT NULL,"\
" product_brand VARCHAR(80) NULL DEFAULT NULL,"\
" product_preferred_supplier_id INTEGER NULL DEFAULT NULL,"\
" product_dimension_length FLOAT(11) NULL DEFAULT NULL,"\
" product_dimension_width FLOAT(11) NULL DEFAULT NULL,"\
" product_dimension_height FLOAT(11) NULL DEFAULT NULL,"\
" product_introduced_date DATE NULL DEFAULT NULL,"\
" product_discontinued BOOLEAN NULL DEFAULT FALSE,"\
" product_no_longer_offered BOOLEAN NULL DEFAULT FALSE,"\
" PRIMARY KEY (product_id));" 

PRODUCT_TABLE = Table('product',
                Column('product_id', 'INTEGER', isPrimaryKey=True),
                Column('product_name', 'VARCHAR'),
                Column('product_description', 'VARCHAR'),
                Column('product_category', 'VARCHAR'),
                Column('product_brand', 'VARCHAR'),
                Column('product_preferred_supplier_id', 'INTEGER'),
                Column('product_dimension_length', 'FLOAT'),
                Column('product_dimension_width', 'FLOAT'),
                Column('product_dimension_height', 'FLOAT'),
                Column('product_introduced_date', 'DATE'),
                Column('product_discontinued', 'BOOLEAN'),
                Column('product_no_longer_offered', 'BOOLEAN'))

def create_table_src(conn, table):

    cur = conn.cursor()
    cur.execute(CREATE_SQL_PG)
    conn.commit()
    cur.close()

def create_table_trg(conn, table):
    pass

def initial_load_source_system(system):
    '''

    Perhaps can take a number of records or more refined dict of

    { table: (n_inserts, num_updates) }  so I can make a canned sequence of updates.

    Get connection, tables, initial data
    for each table in the correct order
    create table
    update data(n_inserts, n_updates)  -- class for table knows how to do it (kwargs)
    '''
    pass

def extract_src_to_trg(source, target, table):
    '''
        moving in the right order, upsert to target system for each table
    '''
    pass

def incremental_load_src(src_conn, table, n_inserts, n_updates):
    '''
    Insert n records of dummy data into table
    '''  
    # Option 1. select n numbers between 1 and count(*)   
    # get one of the non key columns, if numeric, add 1
    # if string append _U
    # log updates
    #

    primary_key_column = table.get_primary_key()
    
    cur = src_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute(f"SELECT MAX({primary_key_column}) from {table.get_name()};") 
    result = cur.fetchone()
    next_key = 1 if result[0] == None else result[0] + 1
    number_rows = next_key - 1
    
    column_names = ','.join(table.get_column_names())

    if n_updates > 0:

        # make n_updates keys

        n_updates = min(n_updates, number_rows)    
        update_keys = ','.join([str(i) for i in random.sample(range(1, next_key),n_updates)])
        cur.execute(f"SELECT {column_names} from {table.get_name()}"\
                    f" WHERE {table.get_primary_key()} IN ({update_keys});")

        result = cur.fetchall()
        # get update column names
        for r in result:
            key_value = r[primary_key_column]
            update_column_name = table.get_update_column().get_name()
            update_column_value = r[update_column_name]
            cur.execute(f"UPDATE {table.get_name()} SET {update_column_name} = concat('{update_column_value}', '_UPD')"
            f" WHERE {primary_key_column} = {key_value}")
            # get random non_key column
            # 
            # print(r['product_id'])           

    if n_inserts > 0:
        insert_records = []
        for i in range(next_key, next_key + n_inserts):

            d = [] 
            for col in table.get_columns():
                col_type = col.get_type()
                if col_type == 'INTEGER':
                    if col.isPrimaryKey():
                        val = i
                    else:
                        val = 98
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
                    val = True
                else:
                    print(f"column type {col_type} not found")
                    val = None

                d.append(val)

            insert_records.append(tuple(d))        
        
        values_substitutions = ','.join(['%s'] * n_inserts)
        
        cur.execute(f"INSERT INTO product ({column_names}) values {values_substitutions}", insert_records)
   
        src_conn.commit()

# initialize with n records
# run incremental with n inserts, m updates q iterations
# run demo -- initialize and load scripted trials

# etl_project load initial --inserts i
# etl_project load incremental --inserts i --updates j --iterations k 


# maybe I need to run a mysql srcipt againnst the default installation to 
# create my database.  You would think it is a common need with docker

src_conn = psycopg2.connect("dbname=postgres host=172.17.0.1 user=postgres password=postgres")
trg_conn = None

create_table_src(src_conn, PRODUCT_TABLE)
create_table_trg(trg_conn, PRODUCT_TABLE)

incremental_load_src(src_conn, PRODUCT_TABLE, n_inserts=5000, n_updates=0)
extract_src_to_trg(src_conn, trg_conn, PRODUCT_TABLE) # table for now, generalize to 
                                              # System of tables.
# for i in structure that controlled start,date, num_update any fooling can be done via kwargs
for i in range(5):
    incremental_load_src(src_conn, PRODUCT_TABLE, n_inserts=200, n_updates=50)
    extract_src_to_trg(src_conn, trg_conn, PRODUCT_TABLE)

src_conn.close()
# trg_conn.close()
