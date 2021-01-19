from sqlalchemy import create_engine, MetaData, Table, select

engine = create_engine('mysql+pymysql://alan:alan@localhost/album')
meta = MetaData()
conn = engine.connect()
# print(engine.table_names())

album = Table('album', meta, autoload=True, autoload_with=engine)

stmt = select([album])
result = conn.execute(stmt).fetchone()
print(result.keys())
print(result)

results = conn.execute(select([album.columns.artist,album.columns.title])).fetchall()

for result in results:
    print(result['artist'], result['title'])

results = conn.execute("SELECT artist, title FROM album").fetchall()

for result in results:
    print(result['artist'], result['title'])
