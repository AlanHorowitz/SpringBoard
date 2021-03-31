FROM python:3.8-slim
RUN pip install psycopg2-binary==2.8.6

COPY RetailDW/* RetailDW/

CMD ["demo1"]

ENTRYPOINT ["python", "-m", "RetailDW"]
