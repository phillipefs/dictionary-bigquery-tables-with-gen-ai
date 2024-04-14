
import os
from utils.credentials import GCLOUD_PROJECT, GOOGLE_APPLICATION_CREDENTIALS
from google.cloud import storage, bigquery
import pandas_gbq as pd
from pandas import DataFrame

os.environ["GCLOUD_PROJECT"] = GCLOUD_PROJECT
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS


class GcpToolkit:
    def __init__(self):
        self.storage_client = storage.Client()
        self.bigquery_client = bigquery.Client()

    def get_name_columns_table(self, dataset: str, table_name: str) -> str:
        """
        Get names of columns in a BigQuery table.

        Args:
            dataset (str): The dataset ID.
            table_name (str): The table name.

        Returns:
            str: A string containing column names separated by commas.
        """
        try:
            query = f"SELECT * FROM `{dataset}.{table_name}` LIMIT 1"
            df_sample = pd.read_gbq(query)
            columns_str = ", ".join(list(df_sample.columns))
            return columns_str
        except Exception as e:
            print(f"Error in get_name_columns_table: {str(e)}")
            raise e

    def get_sample_table_bigquery(self, dataset: str, table_name: str) -> DataFrame:
        """
        Get a sample of data from a BigQuery table.

        Args:
            dataset (str): The dataset ID.
            table_name (str): The table name.

        Returns:
            str: A string representation of the sample data.
        """
        try:
            query = f"SELECT * FROM `{dataset}.{table_name}` LIMIT 10"
            df_sample = pd.read_gbq(query)        
            return df_sample
        except Exception as e:
            print(f"Error in get_sample_table_bigquery: {str(e)}")
            raise e