import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from RetailDW.sqltypes import Table, Column

from RetailDW.etlutils import (
    create_table,
    load_source_table,
    extract_table_to_target,
    ETL_HISTORY_CREATE_MYSQL,
)
from RetailDW.product import (
    PRODUCT_TABLE,
    PRODUCT_CREATE_SQL_PG,
    PRODUCT_CREATE_SQL_MYSQL,
)

from RetailDW.store import (
    STORE_TABLE,
    STORE_CREATE_SQL_PG,
    STORE_CREATE_SQL_MYSQL,
)

from RetailDW.store_sales import (
    STORE_SALES_TABLE,
    STORE_SALES_CREATE_SQL_MYSQL,
    STORE_SALES_CREATE_SQL_PG,
)