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
  PRIMARY KEY (product_id));  