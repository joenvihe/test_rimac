import numpy as np
import pandas as pd
from joblib import dump, load
from google.cloud import bigquery, storage
import os 
import json
from datetime import datetime


from sklearn.model_selection import KFold,cross_val_score, RepeatedStratifiedKFold,StratifiedKFold
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder,StandardScaler,PowerTransformer, RobustScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.impute import SimpleImputer

from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer, make_column_selector

from sklearn.model_selection import KFold, cross_val_predict, train_test_split,GridSearchCV,cross_val_score
from sklearn.metrics import accuracy_score, classification_report


storage_client = storage.Client()
bucket = storage_client.bucket(os.environ['BUCKET_NAME'])


def get_data():
    
    table_id = f"{os.environ['GCP_PROJECT_ID']}.{os.environ['DATASET_BIGQUERY']}.{os.environ['TABLE_BIGQUERY']}"
    
    query = f"""       
        SELECT *
        FROM {table_id}
        """

    client = bigquery.Client(project=os.environ['GCP_PROJECT_ID'])
    query_job = client.query(query)
    result = query_job.result()
    df = result.to_dataframe()

    return df

def get_pipeline(model):
    ohe= OneHotEncoder()
    rs = RobustScaler()


    ct= make_column_transformer(
        (rs, make_column_selector(dtype_include=np.number)),
        (ohe, make_column_selector(dtype_include=object))
        ,remainder='passthrough')
    
    pipe = make_pipeline(ct, model)

    return pipe

def get_model(model_name):
    if model_name == 'logistic_regression':
        return LogisticRegression(solver='liblinear')
    elif model_name == 'random_forest':
        return RandomForestClassifier(max_depth=2, random_state=0)
    elif model_name == 'gradient_boosting':
        return GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0)
    
    
def write_metrics_to_bigquery(algo_name, training_time, model_metrics):
    client = bigquery.Client()
    table_id = "heartdisease-414803.ml_ops.model_metrics"
    table = bigquery.Table(table_id)

    row = {"algo_name": algo_name, "training_time": training_time.strftime('%Y-%m-%d %H:%M:%S'), "model_metrics": json.dumps(model_metrics)}
    errors = client.insert_rows_json(table, [row])

    if errors == []:
        print("Metrics inserted successfully into BigQuery.")
    else:
        print("Error inserting metrics into BigQuery:", errors)

def save_model(model_name, pipeline):

    artifact_name = model_name+'_model.joblib'
    dump(pipeline, artifact_name)
    model_artifact = bucket.blob('models/'+artifact_name)
    model_artifact.upload_from_filename(artifact_name)
    print('Model was saved successfully.')

def get_report_metrics(y_test, y_pred):
    report = classification_report(y_test, y_pred, output_dict=True)
    accuracy_model = round(accuracy_score(y_test, y_pred),4)
    return accuracy_model, report

def train(model_name = 'logistic_regression'):

    data = get_data()

    X = data.drop('HeartDisease', axis=1)
    y= data['HeartDisease']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    model = get_model(model_name)

    pipe = get_pipeline(model)

    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)

    accuracy_model, report = get_report_metrics(y_test, y_pred)
    print(f"Accuracy of the model training {model_name} is {accuracy_model}")
    training_time = datetime.now()
    print(accuracy_model)
    print(report)
    write_metrics_to_bigquery(model_name, training_time, report)
    save_model(model_name, pipe)

if __name__ == '__main__':
    
    train()
    #train('random_forest')
    #train('gradient_boosting')
    