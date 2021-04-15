import pytest

from .context import Table, Column


def test_initXrefDict():

    cols1 = [
        Column("product_description", "VARCHAR"),
        Column("product_category", "VARCHAR"),
        Column("product_brand", "VARCHAR"),
    ]

    xref_dict = Table._initXrefDict(cols1)
    assert len(xref_dict) == 0

    cols2 = [
        Column(
            "product_description", "VARCHAR", xref_table="table1", xref_column="column1"
        ),
        Column(
            "product_category", "VARCHAR", xref_table="table1", xref_column="column2"
        ),
        Column("product_brand", "VARCHAR", xref_table="table2", xref_column="column3"),
    ]

    xref_dict = Table._initXrefDict(cols2)
    assert len(xref_dict) == 2
    assert len(xref_dict["table1"]._column_list) == 2
    assert len(xref_dict["table2"]._column_list) == 1
    assert "column1" in xref_dict["table1"]._column_list
    assert "column2" in xref_dict["table1"]._column_list
    assert "column3" in xref_dict["table2"]._column_list

    cols3 = [
        Column("product_description", "VARCHAR", xref_table="table1"),
        Column("product_category", "VARCHAR", xref_column="column2"),
    ]

    xref_dict = Table._initXrefDict(cols3)
    assert len(xref_dict) == 0
