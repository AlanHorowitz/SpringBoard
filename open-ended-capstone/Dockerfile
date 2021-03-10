FROM python:3.8-slim
RUN pip install psycopg2-binary==2.8.6

COPY second_etl.py .

CMD ["second_etl.py"]

ENTRYPOINT ["python"]
