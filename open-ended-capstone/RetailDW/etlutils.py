import random
import psycopg2
import psycopg2.extras
from psycopg2.extensions import connection  

DEFAULT_INSERT_VALUES = { 'INTEGER' : 98,
                          'VARCHAR' : 'AAA',
                          'FLOAT' : 5.0,
                          'REAL'  : 5.0,
                          'DATE'  : '2021-02-11 12:52:47',
                          'TINYINT' : 0,
                          'BOOLEAN' : True }

def create_table_src(conn : connection , create_sql : str) -> None:

    cur = conn.cursor()
    cur.execute(create_sql)
    conn.commit()
    cur.close()

def incremental_load_src(src_conn, table, n_inserts, n_updates):
    '''
    Insert or update records of dummy data  
    '''  

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

        return n_inserts, n_updates
        
