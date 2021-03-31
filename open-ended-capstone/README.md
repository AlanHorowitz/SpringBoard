##  RetailDW Module

###  A simulated data warehouse in the retail domain.  Add records to a product table on a postgres source system and extract them to a MySQL target system.

### Prerequisites: docker, docker-compose

###  Issue the following commands from the open-ended-capstone directory to start the databases, build and run:

```
docker-compose up -d
docker build -t retail_dw .
docker run -t retail_dw [demo1/demo2]
```

### Demo 1 
Initial load of 5000 records followed by five incremental loads, each with 200 inserts and 50 updates.  The demo may be run repeatedly.

###   Expected output on clean system :

```
6000 inserts and 250 updates processed.
```

### Demo 2 
Initial load of 5000 records followed by five incremental loads, each with 200 inserts and 50 updates.  Following each of the incremental loads, extract data from the source system and apply it to the target system. The demo may be run repeatedly.

###   Expected output on clean system :

```
5000 inserts and 0 updates processed at source: 2021-03-31 01:44:15.664063.
200 inserts and 50 updates processed at source: 2021-03-31 01:44:19.262280.
5200 inserts and 0 updates processed at target: From: 1980-01-01 00:00:00 To: 2021-03-31 01:44:19.262280 
200 inserts and 50 updates processed at source: 2021-03-31 01:44:24.846703.
200 inserts and 50 updates processed at target: From: 2021-03-31 01:44:19.262280 To: 2021-03-31 01:44:24.846703 
200 inserts and 50 updates processed at source: 2021-03-31 01:44:28.009200.
200 inserts and 50 updates processed at target: From: 2021-03-31 01:44:24.846703 To: 2021-03-31 01:44:28.009200 
200 inserts and 50 updates processed at source: 2021-03-31 01:44:31.171240.
200 inserts and 50 updates processed at target: From: 2021-03-31 01:44:28.009200 To: 2021-03-31 01:44:31.171240 
200 inserts and 50 updates processed at source: 2021-03-31 01:44:34.388203.
200 inserts and 50 updates processed at target: From: 2021-03-31 01:44:31.171240 To: 2021-03-31 01:44:34.388203 
6000 inserts and 250 updates processed at source.
6000 inserts and 200 updates processed at target.

```
### To inspect the product table from the Postgres CLI:
```
docker run --rm -it postgres psql -h 172.17.0.1 -d retaildw -U user1

Enter user1 as password
``` 

### To inspect the product table from the MySQL CLI:
```
docker run -it mysql:8.0.23 mysql -h 172.17.0.1 -D retaildw -u user1 -p

Enter user1 as password

### Note: This program depends on the docker host being at address 172.17.0.1

