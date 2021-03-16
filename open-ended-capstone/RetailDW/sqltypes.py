import random

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

