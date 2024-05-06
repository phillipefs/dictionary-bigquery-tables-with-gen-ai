
import json
from google.cloud import storage, bigquery, secretmanager
from google.cloud.bigquery import SchemaField
import google_crc32c
import pandas_gbq as pd
from pandas import DataFrame


class GcpToolkit:
    def __init__(self):
        self.storage_client = storage.Client()
        self.bigquery_client = bigquery.Client()
        self.secret_manager_client = secretmanager.SecretManagerServiceClient()

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
     
            client = self.bigquery_client
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
        
    def access_secret_version(self, project_id: str, secret_id: str, version_id: str= "latest"
        ) -> secretmanager.AccessSecretVersionResponse:
        """
        Access the payload for the given secret version if one exists. The version
        can be a version number as a string (e.g. "5") or an alias (e.g. "latest").
        """

        # Create the Secret Manager client.
        client_secret_manager = self.secret_manager_client

        # Build the resource name of the secret version.
        name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

        # Access the secret version.
        response = client_secret_manager.access_secret_version(request={"name": name})

        # Verify payload checksum.
        crc32c = google_crc32c.Checksum()
        crc32c.update(response.payload.data)
        if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
            print("Data corruption detected.")
            return response

        secret = response.payload.data.decode("UTF-8")
        return secret

