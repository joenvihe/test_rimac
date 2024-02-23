from google.cloud import bigquery, storage
from google.cloud import bigquery
from google.cloud.exceptions import NotFound
import os
import pandas as pd
from pathlib import Path

bigquery_client = bigquery.Client()
dirname = Path(__file__).parent

def create_table_bigquery(big_query_client = bigquery_client):
    
    # Define your dataset ID
    dataset_id = f"{os.environ['GCP_PROJECT_ID']}.{os.environ['DATASET_BIGQUERY']}"

    # Define your table schema
    schema = [
        bigquery.SchemaField("Age", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("Sex", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("ChestPainType", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("RestingBP", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("Cholesterol", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("FastingBS", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("RestingECG", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("MaxHR", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("ExerciseAngina", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("Oldpeak", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("ST_Slope", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("HeartDisease", "INTEGER", mode="REQUIRED"),
        
    ]

    # Define your table ID
    table_id = f"{dataset_id}.{os.environ['TABLE_BIGQUERY']}"
    #table_ref = client.dataset(dataset_id).table('heart_table')
    try: 
        big_query_client.get_table(table_id, retry=bigquery.DEFAULT_RETRY)
        # Delete the table
        big_query_client.delete_table(table_id)
        print(f"Table {table_id} deleted from dataset {dataset_id}.")
    except NotFound:
    # If a NotFound exception is raised, the table does not exist
        print(f"Table {table_id} does not exist in dataset {dataset_id}.")

    table = bigquery.Table(table_id, schema=schema)
    table = big_query_client.create_table(table)  # Make an API request.
    print(
        "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
    )

def load_data_bigquery(filename = os.path.join(dirname, 'fuentes', 'heart.csv')):
    
    table_id = f"{os.environ['GCP_PROJECT_ID']}.{os.environ['DATASET_BIGQUERY']}.{os.environ['TABLE_BIGQUERY']}"

    df = pd.read_csv(filename)

    client = bigquery.Client()

    write_mode = "WRITE_TRUNCATE" # or "WRITE_APPEND"
    job_config = bigquery.LoadJobConfig(write_disposition=write_mode)

    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    result = job.result()

def load_data_storage_to_bigquery():

    table_id = f"{os.environ['GCP_PROJECT_ID']}.{os.environ['DATASET_BIGQUERY']}.{os.environ['TABLE_BIGQUERY']}"
    
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
    )

    uri = f"gs://{os.environ['BUCKET_NAME']}/data/heart.csv"
    load_job = bigquery_client.load_table_from_uri(uri, table_id, job_config=job_config)

    load_job.result()  

    destination_table = bigquery_client.get_table(table_id)
    print("Number of rows", destination_table.num_rows)


def create_bucket(name_bucket = os.environ['BUCKET_NAME']):

    storage_client = storage.Client()
    bucket = storage_client.bucket(name_bucket)
    bucket.storage_class = 'STANDARD'
    bucket = storage_client.create_bucket(bucket, location='us-central1') 

    print(f'Bucket {bucket.name} successfully created.')

def upload_file_bucket(name_bucket = os.environ['BUCKET_NAME'], storage_filename = "datos/heart.csv", local_filename = os.path.join(dirname, 'fuentes', 'heart.csv')):

    storage_client = storage.Client()
    bucket = storage_client.bucket(name_bucket)
    blob = bucket.blob(storage_filename)
    blob.upload_from_filename(local_filename)

    print('Data was uploaded successfully.')


def create_table_bigquery_mlops(big_query_client = bigquery_client):
    
    # Define your dataset ID
    dataset_id = f"{os.environ['GCP_PROJECT_ID']}.{os.environ['DATASET_MLOPS_BIGQUERY']}"

    # Define your table schema
    schema = [
        bigquery.SchemaField("Algo_Name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("Training_Time", "TIMESTAMP", mode="REQUIRED"),
        bigquery.SchemaField("Model_Metrics", "STRING", mode="REQUIRED"),
    ]

    # Define your table ID
    table_id = f"{dataset_id}.{os.environ['TABLE_MLOPS_BIGQUERY']}"
    #table_ref = client.dataset(dataset_id).table('heart_table')
    try: 
        big_query_client.get_table(table_id, retry=bigquery.DEFAULT_RETRY)
        # Delete the table
        big_query_client.delete_table(table_id)
        print(f"Table {table_id} deleted from dataset {dataset_id}.")
    except NotFound:
    # If a NotFound exception is raised, the table does not exist
        print(f"Table {table_id} does not exist in dataset {dataset_id}.")

    table = bigquery.Table(table_id, schema=schema)
    table = big_query_client.create_table(table)  # Make an API request.
    print(
        "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
    )

if __name__ == "__main__":
    # create_table_bigquery()
    # load_data_bigquery()
    # create_bucket()
    # upload_file_bucket()
    create_table_bigquery_mlops()