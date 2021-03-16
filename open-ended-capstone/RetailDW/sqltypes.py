import random
from typing import List

class Column():
    """Database Column metadata"""

    def __init__(self, column_name : str, column_type : str, isPrimaryKey : bool=False):

        self._name = column_name
        self._type = column_type
        self._isPrimaryKey = isPrimaryKey

    def get_name(self) -> str:

        return self._name

    def get_type(self) -> str:

        return self._type

    def isPrimaryKey(self) -> bool:

        return self._isPrimaryKey

class Table():
    """Database Table metadata"""

    def __init__(self, name : str, *columns : Column):
        """Instatiate a table metadata object.

        Note: Source system tables in RetailDW must have a single column integer primary key
        and at least one VARCHAR column.
        """

        self._name = name
        self._columns = [ col for col in columns ] 
        primary_keys = [ col.get_name() for col in columns if col.isPrimaryKey() ] 
        if len(primary_keys) != 1:
            raise Exception("Simulator requires exactly one primary key")
        self._primary_key = primary_keys[0]
        self._update_columns = [col for col in columns if col.get_type() == 'VARCHAR']  # restrict to VARCHAR update
        if len(primary_keys) == 0:
            raise Exception("Need at least one VARCHAR for update")

    def get_name(self) -> str:

        return self._name

    def get_columns(self) -> List[Column]:
        """ Return a complete list of Column objects for the table."""

        return self._columns

    def get_primary_key(self) -> str:

        return self._primary_key

    def get_column_names(self) -> List[str]:
        """ Return a complete list of Column names for the table."""
        return [col.get_name() for col in self._columns] 

    def get_update_column(self) -> Column:
        """ Return a random eligible update column."""
        i = random.randint(0,len(self._update_columns)-1)   
        return self._update_columns[i]

