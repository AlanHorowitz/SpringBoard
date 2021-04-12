import psycopg2

import mysql.connector
from mysql.connector import connect

import pytest

from .context import create_table, PRODUCT_CREATE_SQL_MYSQL, PRODUCT_CREATE_SQL_PG, PRODUCT_TABLE
from .context import STORE_CREATE_SQL_MYSQL, STORE_CREATE_SQL_PG, STORE_TABLE
from .context import STORE_SALES_CREATE_SQL_MYSQL, STORE_SALES_CREATE_SQL_PG, STORE_SALES_TABLE

def checkConnection(docker_ip):
    '''Called by pytest-docker plugin.  Returns True when connections to databases are available'''

    try:
        pg_source_connection = psycopg2.connect(
            dbname="retaildw", host=docker_ip, user="user1", password="user1")
        pg_source_connection.close()
        try:
            mysql_target_connection = connect(
            host=docker_ip,
            user="user1",
            password="user1",
            database="retaildw",
            charset="utf8",
            )
            mysql_target_connection.close()
            return True
        except:
            return False        
    except Exception:
        return False

@pytest.fixture(scope='session')
def getdocker(docker_ip, docker_services):
    ''' issue docker-compose up on docker-compose.yml in tests directory'''

    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: checkConnection(docker_ip)
    )   

@pytest.fixture(scope='session')
def pg1(docker_ip, getdocker):
        
    postgres_connection = psycopg2.connect(
        dbname="retaildw", host=docker_ip, user="user1", password="user1"
    )
    return postgres_connection   

@pytest.fixture(scope='session')
def mysql1(docker_ip, getdocker):
        
    mysql_connection = connect(
            host=docker_ip,
            user="user1",
            password="user1",
            database="retaildw",
            charset="utf8",
            )            
    return mysql_connection

def create_and_test_table(conn, table, sql):

    create_table(conn, sql)
    cur = conn.cursor()
    cur.execute(
        f"SELECT COUNT(*) from {table.get_name()};")
    r = cur.fetchone()
    assert r[0] == 0  # new table is empty
    cur.close()

# tests

def test_product_postgres(pg1):
    create_and_test_table(pg1, PRODUCT_TABLE, PRODUCT_CREATE_SQL_PG)

def test_product_mysql(mysql1):
    create_and_test_table(mysql1, PRODUCT_TABLE, PRODUCT_CREATE_SQL_MYSQL)

def test_store_postgres(pg1):
    create_and_test_table(pg1, STORE_TABLE, STORE_CREATE_SQL_PG)

def test_store_mysql(mysql1):
    create_and_test_table(mysql1, STORE_TABLE, STORE_CREATE_SQL_MYSQL)

def test_store_sales_postgres(pg1):
    create_and_test_table(pg1, STORE_SALES_TABLE, STORE_SALES_CREATE_SQL_PG)

def test_store_sales_mysql(mysql1):
    create_and_test_table(mysql1, STORE_SALES_TABLE, STORE_SALES_CREATE_SQL_MYSQL)