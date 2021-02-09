from sqlalchemy import create_engine, MetaData, Table, Column
from sqlalchemy import select, insert, update, delete
from sqlalchemy import Integer, String, Boolean, DECIMAL
engine = create_engine('mysql+pymysql://alan:alan@localhost/album')
meta = MetaData()
conn = engine.connect()
print(engine.table_names())

album = Table('album', meta, autoload=True, autoload_with=engine)

stmt = select([album])
result = conn.execute(stmt).fetchone()
print(result.keys())
print(result)

results = conn.execute(select([album.columns.artist,album.columns.title])).fetchall()

for result in results:
    print(result['artist'], result['title'])

results2 = conn.execute("SELECT artist, title FROM album").fetchall()

for result in results2:
    print(result['artist'], result['title'])

assert(results == results2)

employees = Table('employees', meta,
    Column('id', Integer()),
    Column('name', String(255)),
    Column('salary', DECIMAL()),
    Column('active', Boolean())
)

if not employees.exists(engine):
    meta.create_all(engine)

    emp_records = [
        {'id' : 1, 'name': 'Fred', 'salary': 10000, 'active': True},
        {'id' : 2, 'name': 'Jill', 'salary': 20000, 'active': False},
        {'id' : 3, 'name': 'Mark', 'salary': 30000, 'active': True},
        {'id' : 4, 'name': 'Beth', 'salary': 40000, 'active': False}
    ]

    stmt = insert(employees)
    print('rows inserted', conn.execute(stmt,emp_records).rowcount)

stmt = update(employees).values(salary=25000.00)
stmt = stmt.where(employees.columns.name == 'Jill')
print(conn.execute(stmt).rowcount, 'rows updated')

jill_new_sal = conn.execute(select([employees.columns.salary]).where(
    employees.columns.name == 'Jill')).scalar()

print(f"Jill's new salary is {jill_new_sal}")

conn.close()
employees.drop(engine)














