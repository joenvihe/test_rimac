from fastapi import FastAPI

from google.cloud import bigquery
from google.cloud.exceptions import NotFound

app = FastAPI()

client = bigquery.Client()

# Define a root `/` endpoint
@app.get('/')
def index():
    return {'ok': True}


@app.get('/predict')
def predict():
    return {'wait': 64}


@app.get('/load_data')
def load_datos():

    table_id = "heartdisease-414803.heartdataset.heart_table"
    
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
    )

    uri = "gs://mybucket-heartdisease-20245/datos/heart.csv"
    load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)

    load_job.result()  

    destination_table = client.get_table(table_id)
    return {"data": destination_table.num_rows}