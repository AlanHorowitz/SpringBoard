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
            f"INSERT INTO product ({column_names}) values {values_substitutions}",
            insert_records,
        )

        conn.commit()

    return n_inserts, n_updates
