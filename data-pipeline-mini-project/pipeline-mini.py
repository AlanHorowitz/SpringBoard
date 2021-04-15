import csv
import mysql.connector
from mysql.connector import connect

CSV_FILEPATH = "third_party_sales_1.csv"

INSERT_SQL = """
INSERT INTO Ticket_Sales (
    ticket_id,
    trans_date,
    event_id,
    event_name,
    event_date,
    event_type,
    event_city,
    customer_id,
    price,
    num_tickets
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""

MOST_POPULAR_SQL = """
SELECT event_name, SUM(num_tickets)
FROM Ticket_Sales
GROUP BY event_name
ORDER BY SUM(num_tickets) DESC LIMIT 3;
"""

def get_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(user='alan',
                                            password='alan',
                                            host='localhost',
                                            port='3306',
                                            database='pipeline')
    except Exception as error:
        print('Error while connecting to database', error)

    return connection

def load_third_party(connection, file_path_csv):
    cursor = connection.cursor()
    
    with open(file_path_csv, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            cursor.execute(INSERT_SQL, tuple(row))

    connection.commit()
    cursor.close()
    return

def query_popular_tickets(connection):
        
    cursor = connection.cursor()
    cursor.execute(MOST_POPULAR_SQL)
    records = cursor.fetchall()
    cursor.close()
    return records


if __name__ == '__main__':

    connection = get_db_connection()
    load_third_party(connection, CSV_FILEPATH)
    records = query_popular_tickets(connection)
    
    print("Here are the most popular tickets in the last month:")
    for rec in records:
        print('-', rec[0])


