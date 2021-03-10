##  second_etl.py

###  This program uses psycopg2 to load and update the Product table of the proposed Postgres ETL source system.  Initial load is of 5000 records and which is followed by five incremental loads, each with 200 inserts and 50 updates.  It may be run repeatedly.

###  Issue the following commands from the open-ended-capstone directory to build and run:

```
docker run --name postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres
docker build -t second_etl .
docker run second_etl
```
###   Expected output:

```
>>> 6000 inserts and 250 updates processed.
```

### To inspect the product table from the Postgres CLI:
```
docker run --rm -it postgres psql -h 172.17.0.1 -U postgres
```
### Enter postgres as password

#### Note: This program depends on the docker host being at address 172.17.0.1
