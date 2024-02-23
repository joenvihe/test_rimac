# !pip3 install xgboost

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import pandas as pd
from google.cloud import storage
import gcsfs,json
from datetime import datetime
from google.cloud import bigquery
from google.cloud import logging

from joblib import dump, load
import json
from training import get_model, get_pipeline, get_report_metrics, save_model, write_metrics_to_bigquery
# from bank_campaign_model_training import (
#     encode_categorical, apply_bucketing, preprocess_features,write_metrics_to_bigquery,
#     get_classification_report, save_model_artifact,train_model
# )

# logging_client = logging.Client()
# logger = logging_client.logger('bank-campaign-training-logs')

def validate_csv():
    # Load data
    fs = gcsfs.GCSFileSystem()
    with fs.open('gs://mybucket-heartdisease-20245/datos/heart.csv') as f:
        df = pd.read_csv(f)
    
    # Define expected columns
    expected_cols = [
        'Age','Sex','ChestPainType','RestingBP','Cholesterol','FastingBS','RestingECG',
        'MaxHR','ExerciseAngina','Oldpeak','ST_Slope','HeartDisease']
        
    # Check if the loaded columns are same as expected columns
    if list(df.columns) == expected_cols:
        return True
    else:
        # logger.log_struct({
        #     'keyword': 'Bank_Campaign_Model_Training',
        #     'description': 'This log captures the last run for Model Training',
        #     'training_timestamp': datetime.now().isoformat(),
        #     'model_output_msg': "Input Data is not valid",
        #     'training_status':0
        # })
        raise ValueError(f'CSV does not have expected columns. Columns in CSV are: {list(df.columns)}')

def read_last_training_metrics(model_name = 'logistic_regression'):
    client = bigquery.Client()
    table_id = "heartdisease-414803.ml_ops.model_metrics"
    query = f"""
        SELECT *
        FROM `{table_id}`
        where algo_name='{model_name}'
        ORDER BY training_time DESC
        LIMIT 1
    """
    result = client.query(query).result()
    latest_row = next(result)
    return json.loads(latest_row[2])


def evaluate_model():
    # Load data for evaluation
    fs = gcsfs.GCSFileSystem()

    with fs.open('gs://mybucket-heartdisease-20245/datos/heart.csv') as f:
        df = pd.read_csv(f, sep=",")
    
    X = df.drop('HeartDisease', axis=1)
    y= df['HeartDisease']
    
    # Train the model on new data 
    model_name = "logistic_regression"
    model = get_model(model_name)
    pipe = get_pipeline(model)

    pipe.fit(X, y)
    y_pred = pipe.predict(X)

    accuracy_model, model_metrics = get_report_metrics(y, y_pred)

    # Get current metric for evaluation
    precision = model_metrics['0']['precision']
    recall = model_metrics['0']['recall']

    # Get the last/existing model metrics for comparison
    last_model_metrics = read_last_training_metrics(model_name)
    last_precision = last_model_metrics['0.0']['precision']
    last_recall = last_model_metrics['0.0']['recall']

    # Define the threshold values for precision and recall
    precision_threshold = 0.8
    recall_threshold = 0.8
    
    # Save the model artifact if metrics are above the thresholds
    if (precision >=precision_threshold and recall >=recall_threshold) and (precision >= last_precision and recall >= last_recall):
        save_model(model_name, pipe)
        write_metrics_to_bigquery(model_name,datetime.now(), model_metrics)
        # logger.log_struct({
        #     'keyword': 'Bank_Campaign_Model_Training',
        #     'description': 'This log captures the last run for Model Training',
        #     'training_timestamp': datetime.now().isoformat(),
        #     'model_output_msg': "Model artifact saved",
        #     'training_status':1
        # })
    else:
        # logger.log_struct({
        #     'keyword': 'Bank_Campaign_Model_Training',
        #     'description': 'This log captures the last run for Model Training',
        #     'training_timestamp': datetime.now().isoformat(),
        #     'model_output_msg': "Model metrics do not meet the defined threshold",
        #     'model_metrics':model_metrics,
        #     'training_status':0
        # })
        pass

# Define the default_args dictionary
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 1,
}

# Instantiate the DAG
dag = DAG(
    'dag_heart_disease_continuous_training',
    default_args=default_args,
    description='A not so simple training DAG',
    schedule_interval=None,
)

# Define the tasks/operators
validate_csv_task = PythonOperator(
    task_id='validate_csv',
    python_callable=validate_csv,
    dag=dag,
)

evaluation_task = PythonOperator(
    task_id='model_evaluation',
    python_callable=evaluate_model,
    dag=dag,
)

validate_csv_task >> evaluation_task