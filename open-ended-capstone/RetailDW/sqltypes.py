import random
from typing import List, Tuple, Dict
from psycopg2.extensions import cursor

from datetime import datetime

DEFAULT_INSERT_VALUES: Dict[str, object] = {
    "INTEGER": 98,
    "VARCHAR": "AAA",
    "FLOAT": 5.0,
    "REAL": 5.0,
    "DATE": "2021-02-11 12:52:47",
    "TINYINT": 0,
    "BOOLEAN": True,
}

class Column:
    """Database Column metadata"""

    def __init__(
        self,
        column_name: str,
        column_type: str,
        isPrimaryKey: bool = False,
        isInsertedAt: bool = False,
        isUpdatedAt: bool = False,
        xref_table: str = None,
        xref_column: str = None 
    ):

        self._name = column_name
        self._type = column_type
        self._isPrimaryKey = isPrimaryKey
        self._isInsertedAt = isInsertedAt
        self._isUpdatedAt = isUpdatedAt
        self._xref_table = xref_table
        self._xref_column = xref_column

    def get_name(self) -> str:

        return self._name

    def get_type(self) -> str:

        return self._type

    def isPrimaryKey(self) -> bool:

        return self._isPrimaryKey

    def isInsertedAt(self) -> bool:

        return self._isInsertedAt

    def isUpdatedAt(self) -> bool:

        return self._isUpdatedAt


class Table:
    """Database Table metadata"""

    def __init__(self, name: str, *columns: Column):
        """Instatiate a table metadata object.

        Note: Source system tables in RetailDW must have a single column integer primary key
        and at least one VARCHAR column.
        """

        self._name = name
        self._columns = [col for col in columns]
        primary_keys = [col.get_name() for col in columns if col.isPrimaryKey()]
        inserted_ats = [col.get_name() for col in columns if col.isInsertedAt()]
        updated_ats = [col.get_name() for col in columns if col.isUpdatedAt()]
        if (len(primary_keys), len(inserted_ats), len(updated_ats)) != (1, 1, 1):
            raise Exception(
                "Simulator requires exactly one primary key, inserted_at and updated_at column"
            )
        self._primary_key = primary_keys[0]
        self._inserted_at = inserted_ats[0]
        self._updated_at = updated_ats[0]

        self._update_columns = [
            col for col in columns if col.get_type() == "VARCHAR"
        ]  # restrict to VARCHAR update
        if len(primary_keys) == 0:
            raise Exception("Need at least one VARCHAR for update")

    def preload(self, cur: cursor) -> None:
        pass

    def postload(self) -> None:
        pass

    def getNewRow(self, pk : int, timestamp: datetime = datetime.now()) -> Tuple:

        d: List[object] = []
        for col in self.get_columns():
            if col.isPrimaryKey():
                d.append(pk)
            elif col.isInsertedAt() or col.isUpdatedAt():
                d.append(timestamp)
            else:
                d.append(DEFAULT_INSERT_VALUES[col.get_type()])
        return tuple(d)

    def get_name(self) -> str:

        return self._name

    def get_columns(self) -> List[Column]:
        """ Return a complete list of Column objects for the table."""

        return self._columns

    def get_primary_key(self) -> str:

        return self._primary_key

    def get_updated_at(self) -> str:

        return self._updated_at

    def get_column_names(self) -> List[str]:
        """ Return a complete list of Column names for the table."""
        return [col.get_name() for col in self._columns]

    def get_update_column(self) -> Column:
        """ Return a random eligible update column."""
        i = random.randint(0, len(self._update_columns) - 1)
        return self._update_columns[i]


