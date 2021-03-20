from RetailDW.sqltypes import Column, Table

PRODUCT_CREATE_SQL_PG = """
CREATE TABLE IF NOT EXISTS Product (
product_id INTEGER NOT NULL,
product_name VARCHAR(80) NOT NULL,
product_description VARCHAR(255) NULL DEFAULT NULL,
product_category VARCHAR(80) NULL DEFAULT NULL,
product_brand VARCHAR(80) NULL DEFAULT NULL,
product_preferred_supplier_id INTEGER NULL DEFAULT NULL,
product_dimension_length FLOAT(11) NULL DEFAULT NULL,
product_dimension_width FLOAT(11) NULL DEFAULT NULL,
product_dimension_height FLOAT(11) NULL DEFAULT NULL,
product_introduced_date DATE NULL DEFAULT NULL,
product_discontinued BOOLEAN NULL DEFAULT FALSE,
product_no_longer_offered BOOLEAN NULL DEFAULT FALSE,
product_inserted_at TIMESTAMP NOT NULL,
product_updated_at TIMESTAMP NOT NULL,
PRIMARY KEY (product_id));
"""

PRODUCT_TABLE = Table(
    "product",
    Column("product_id", "INTEGER", isPrimaryKey=True),
    Column("product_name", "VARCHAR"),
    Column("product_description", "VARCHAR"),
    Column("product_category", "VARCHAR"),
    Column("product_brand", "VARCHAR"),
    Column("product_preferred_supplier_id", "INTEGER"),
    Column("product_dimension_length", "FLOAT"),
    Column("product_dimension_width", "FLOAT"),
    Column("product_dimension_height", "FLOAT"),
    Column("product_introduced_date", "DATE"),
    Column("product_discontinued", "BOOLEAN"),
    Column("product_no_longer_offered", "BOOLEAN"),
    Column("product_inserted_at", "TIMESTAMP", isInsertedAt=True),
    Column("product_updated_at", "TIMESTAMP", isUpdatedAt=True),
)
