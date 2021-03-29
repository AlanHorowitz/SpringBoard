import random
from typing import Tuple, Dict, List
from datetime import datetime

from psycopg2.extras import DictCursor, DictRow
from psycopg2.extensions import connection, cursor

from RetailDW.sqltypes import Table, Column

DEFAULT_INSERT_VALUES: Dict[str, object] = {
    "INTEGER": 98,
    "VARCHAR": "AAA",
    "FLOAT": 5.0,
    "REAL": 5.0,
    "DATE": "2021-02-11 12:52:47",
    "TINYINT": 0,
    "BOOLEAN": True,
}

DATE_LOW = datetime(1980, 1, 1)

def create_table(conn: connection, create_sql: str) -> None:

    cur: cursor = conn.cursor()
    cur.execute(create_sql)
    conn.commit()
    cur.close()


def incremental_load(
    conn: connection,
    table: Table,
    n_inserts: int,
    n_updates: int,
    timestamp: datetime = datetime.now(),
) -> Tuple[int, int]:
    """
    Insert and update the given numbers of sythesized records to a table.

    For update, a random sample of n_updates keys is generated and the corresponding records 
    read.  A random selection of one the string columns of the table is written back to the table with 
    '_UPD' appended. 

    For insert, n_insert dummy records are written to the table. The primary key is a sequence of
    incrementing integers, starting at the prior maximum value + 1.

    Args:
        conn: a psycopg2 db connection.
        table: a RetailDW.sqltypes.Table object to be loaded.
        n_inserts: quantity to insert.
        n_updates: quantity to update

    Returns:
        A tuple, (n_inserted, n_updated), representing the number of rows inserted and updated. 
        In the future these may differ from the input values.
    """

    table_name = table.get_name()
    primary_key_column = table.get_primary_key()
    updated_at_column = table.get_updated_at()
    column_names = ",".join(table.get_column_names())  # for SELECT statements

    cur: cursor = conn.cursor(cursor_factory=DictCursor)

    cur.execute(f"SELECT COUNT(*), MAX({primary_key_column}) from {table_name};")
    result: DictRow = cur.fetchone()
    row_count = result[0]
    next_key = 1 if result[1] == None else result[1] + 1

    if n_updates > 0:

        n_updates = min(n_updates, row_count)
        update_keys = ",".join(
            [str(i) for i in random.sample(range(1, next_key), n_updates)]
        )
        cur.execute(
            f"SELECT {column_names} from {table_name}"
            f" WHERE {primary_key_column} IN ({update_keys});"
        )

        result = cur.fetchall()

        for r in result:
            key_value = r[primary_key_column]
            update_column = table.get_update_column().get_name()
            update_column_value = r[update_column]
            cur.execute(
                f"UPDATE {table_name}"
                f" SET {update_column} = concat('{update_column_value}', '_UPD'),"
                f" {updated_at_column} = %s"
                f" WHERE {primary_key_column} = {key_value}",
                [timestamp],
            )

    if n_inserts > 0:

        insert_records = []
        for pk in range(next_key, next_key + n_inserts):

            d: List[object] = []
            for col in table.get_columns():
                if col.isPrimaryKey():
                    d.append(pk)
                elif col.isInsertedAt() or col.isUpdatedAt():
                    d.append(timestamp)
                else:
                    d.append(DEFAULT_INSERT_VALUES[col.get_type()])

            insert_records.append(tuple(d))

        values_substitutions = ",".join(
            ["%s"] * n_inserts
        )  # each %s holds one tuple row

        cur.execute(
            f"INSERT INTO {table_name} ({column_names}) values {values_substitutions}",
            insert_records,
        )

        conn.commit()

    return n_inserts, n_updates

def get_last_timestamp(trg_cursor, table_name):

    trg_cursor.execute("SELECT MAX(to_timestamp) FROM etl_history WHERE table_name = %s;", (table_name,))
    from_time = trg_cursor.fetchone()[0]
    return from_time if from_time else DATE_LOW 

def insert_etl_history(trg_cursor, table_name, n_inserts, n_updates,from_timestamp, to_timestamp):
    
    trg_cursor.execute("INSERT INTO etl_history "
    "(table_name, n_inserts, n_updates,from_timestamp, to_timestamp) "
    "VALUES (%s, %s, %s, %s, %s);", (table_name, n_inserts, n_updates,from_timestamp, to_timestamp))
    
    

def extract_to_target(src_conn: connection, trg_conn: connection, table: Table):
    """
    Extract records more recent than prior update from source system and UPSERT to target system.

    Returns:
        A tuple, (n_inserted,  # records inserted
                  n_updated,   # records updated
                  from_time,   # timestamp < source record update time 
                  to_time      # timestamp >= source record update time  
    """

    # read source
    # write target

    n_inserts = 0
    n_updates = 0

    table_name = table.get_name()
    column_names = ",".join(table.get_column_names())  # for SELECT statements
    values_substitutions = ",".join(["%s"] * len(table.get_column_names())) # each %s holds one tuple row

    src_cursor: cursor = src_conn.cursor(name='pgread')
    src_cursor.arraysize = 1000

    trg_cursor = trg_conn.cursor()
    from_timestamp = get_last_timestamp(trg_cursor, table.get_name())
        
    src_cursor.execute(f"SELECT {column_names} from {table_name} "
                       f"WHERE {table.get_updated_at()} > %s;", 
                       (from_timestamp,))

    while True:

        r = src_cursor.fetchmany()
        if len(r) == 0:
            break

        trg_cursor.executemany(f"REPLACE INTO {table_name} ({column_names}) values ({values_substitutions})",r)

        n_inserts += 2*len(r) - trg_cursor.rowcount
        n_updates += trg_cursor.rowcount - len(r)    
        trg_conn.commit()

    # Populate row of ETL_history   
    
    trg_cursor.execute(f"SELECT MAX({table.get_updated_at()}) FROM {table_name};")
    to_timestamp = trg_cursor.fetchone()[0]
    insert_etl_history(trg_cursor, table.get_name(), n_inserts, n_updates, from_timestamp, to_timestamp)   
        
    return (n_inserts, n_updates, from_timestamp, to_timestamp)