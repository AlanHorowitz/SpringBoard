import random
import psycopg2
import psycopg2.extras

total_inserts = 0
total_updates = 0

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

PRODUCT_CREATE_SQL_PG = \
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

DEFAULT_INSERT_VALUES = { 'INTEGER' : 98,
                          'VARCHAR' : 'AAA',
                          'FLOAT' : 5.0,
                          'REAL'  : 5.0,
                          'DATE'  : '2021-02-11 12:52:47',
                          'TINYINT' : 0,
                          'BOOLEAN' : True }

def create_table_src(conn, create_sql):

    cur = conn.cursor()
    cur.execute(create_sql)
    conn.commit()
    cur.close()

def create_table_trg(conn, table):
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
    global total_inserts
    global total_updates

    primary_key_column = table.get_primary_key()
    
    cur = src_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute(f"SELECT MAX({primary_key_column}) from {table.get_name()};") 
    result = cur.fetchone()
    next_key = 1 if result[0] == None else result[0] + 1
    number_rows = next_key - 1
    
    column_names = ','.join(table.get_column_names())

    if n_updates > 0:

        n_updates = min(n_updates, number_rows)    
        update_keys = ','.join([str(i) for i in random.sample(range(1, next_key),n_updates)])
        cur.execute(f"SELECT {column_names} from {table.get_name()}"\
                    f" WHERE {table.get_primary_key()} IN ({update_keys});")

        result = cur.fetchall()
        
        for r in result:
            key_value = r[primary_key_column]
            update_column_name = table.get_update_column().get_name()
            update_column_value = r[update_column_name]
            cur.execute(f"UPDATE {table.get_name()}"\
                        f" SET {update_column_name} = concat('{update_column_value}', '_UPD')"\
                        f" WHERE {primary_key_column} = {key_value}")
           
    if n_inserts > 0:

        insert_records = []
        for i in range(next_key, next_key + n_inserts):

            d = [] 
            for col in table.get_columns():                
                val = i if col.isPrimaryKey() else DEFAULT_INSERT_VALUES[col.get_type()]
                d.append(val)

            insert_records.append(tuple(d))        
        
        values_substitutions = ','.join(['%s'] * n_inserts)
        
        cur.execute(f"INSERT INTO product ({column_names}) values {values_substitutions}", insert_records)
   
        src_conn.commit()

        total_inserts += n_inserts
        total_updates += n_updates

# etl_project load initial --inserts i
# etl_project load incremental --inserts i --updates j --iterations k 

src_conn = psycopg2.connect("dbname=postgres host=172.17.0.1 user=postgres password=postgres")
trg_conn = None

total_inserts = 0
total_updates = 0

create_table_src(src_conn, PRODUCT_CREATE_SQL_PG)
create_table_trg(trg_conn, None)

incremental_load_src(src_conn, PRODUCT_TABLE, n_inserts=5000, n_updates=0)
extract_src_to_trg(src_conn, trg_conn, PRODUCT_TABLE)   # table for now, generalize to 
                                                        # System of tables.
 
for i in range(5):

    incremental_load_src(src_conn, PRODUCT_TABLE, n_inserts=200, n_updates=50)
    extract_src_to_trg(src_conn, trg_conn, PRODUCT_TABLE)

print(f"{total_inserts} inserts and {total_updates} processed.")

src_conn.close()
# trg_conn.close()