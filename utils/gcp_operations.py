
import os
from utils.credentials import GCLOUD_PROJECT, GOOGLE_APPLICATION_CREDENTIALS
from google.cloud import storage, bigquery
import pandas_gbq as pd

os.environ["GCLOUD_PROJECT"] = GCLOUD_PROJECT
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS

class Gcp_Toolkit:

    def _client_storage():
        storage_client = storage.Client()
        return storage_client
    
    def _client_bigquery():
        bigquery_client = bigquery.Client()
        return bigquery_client    

    def get_name_columns_table(self, dataset:str, table_name:str)->str:
        QUERY = f"SELECT * FROM `{dataset}.{table_name}` LIMIT 1"
        df_sample = pd.read_gbq(QUERY)
        columns_str = ", ".join(list(df_sample.columns))
        return columns_str
    
    def get_sample_table_bigquery(self, dataset:str, table_name:str)->str:
        QUERY = f"SELECT * FROM `{dataset}.{table_name}` LIMIT 10"
        df_sample = pd.read_gbq(QUERY)        
        return df_sample.to_string()