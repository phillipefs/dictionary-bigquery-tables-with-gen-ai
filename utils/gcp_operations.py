
import os
import json
from utils.credentials import GCLOUD_PROJECT, GOOGLE_APPLICATION_CREDENTIALS
from google.cloud import storage, bigquery
from google.cloud.bigquery import SchemaField
import pandas_gbq as pd
from pandas import DataFrame

os.environ["GCLOUD_PROJECT"] = GCLOUD_PROJECT
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS


class GcpToolkit:
    def __init__(self):
        self.storage_client = storage.Client()
        self.bigquery_client = bigquery.Client()

    def get_sample_table_bigquery(self, dataset: str, table_name: str, n_rows: int = 1000) -> DataFrame:
        """
        Get a sample of data from a BigQuery table.

        Args:
            dataset (str): The dataset ID.
            table_name (str): The table name.

        Returns:
            str: A string representation of the sample data.
        """
        try:
            print("Getting sample data...")
            query = f"SELECT * FROM `{dataset}.{table_name}` LIMIT {n_rows}"
            df_sample = pd.read_gbq(query)        
            return df_sample
        except Exception as e:
            print(f"Error in get_sample_table_bigquery: {str(e)}")
            raise e
        
     
    def execute_update_descriptions(self, dataset, table_name, json_descriptions)->None:
        """
        Updates the descriptions of the fields in a BigQuery table schema based on a provided JSON.

        Args:
            - dataset (str): The name of the dataset containing the table.
            - table_name (str): The name of the table to update.
            - json_descriptions (dict): A dictionary where the keys are field names and the values are the descriptions to update.

        Returns:
            None: This function does not return anything.
        """

        try:
     
            client = bigquery.Client()
            table_ref = client.dataset(dataset).table(table_name)
            table = client.get_table(table_ref)

            # Update Schema
            new_schema = []
            for field in table.schema:
                if field.name in json_descriptions:
                    # Only update the description if the field name exists in json_descriptions
                    new_field_description = json_descriptions.get(field.name, field.description)
                else:
                    new_field_description = field.description
                    
                new_field = SchemaField(
                    name=field.name, 
                    field_type=field.field_type, 
                    mode=field.mode, 
                    description=new_field_description, 
                    fields=field.fields
                )
                new_schema.append(new_field)

            table.schema = new_schema
            client.update_table(table, ["schema"])

            print("Table schema updated successfully")

        except Exception as e:
            raise Exception(f"An unexpected error occurred: {e}")
        
    def upload_to_gcloud(self, json_descriptions: dict, bucket_name:str, dataset:str, table_name:str)->None:
        """
        Upload Dict Descriptons to Storage
        Args:
            - data (dict): Dict with descriptions
        Returns:
            None
        """          
        try:
            storage_client = storage.Client()
            bucket = storage_client.get_bucket(bucket_name)
            
            path_file_bucket = dataset + '/' + table_name + '/' + table_name + '.json'
            blob = bucket.blob(path_file_bucket)
            blob.upload_from_string(json.dumps(json_descriptions), content_type="application/json")
            print("Upload Descriptions to bucket...")

        except Exception as e:
            raise Exception(f"An unexpected error occurred: {e}")

