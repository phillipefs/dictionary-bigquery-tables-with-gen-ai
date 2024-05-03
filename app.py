from utils.gcp_operations import GcpToolkit
from utils.openai_gpt import OpenaiGPT
import time


start_time = time.time()

LIST_TABLES = [
    {
        "dataset_name":"REFINED",
        "table_name":"FUEL_SAMPLE",
        "rows_sample": 20
    }
]

if __name__ == "__main__":
        
    GCP_TOOLKIT = GcpToolkit()
    GPT = OpenaiGPT()

    for table in LIST_TABLES:


        sample_table = GCP_TOOLKIT.get_sample_table_bigquery(
            dataset= table["dataset_name"],
            table_name= table["table_name"]
        )

        prompt_dictionary = GPT.build_dictionary_prompt(
            dataframe= sample_table
        )
        
        response_gpt = GPT.send_question_gpt(
            prompt_dictionary= prompt_dictionary
        )

        GCP_TOOLKIT.upload_to_gcloud(
            json_descriptions=response_gpt,
            bucket_name="data-dictionary-bigquery",
            dataset= table["dataset_name"],
            table_name= table["table_name"]            
        )

        GCP_TOOLKIT.execute_update_descriptions(
            dataset= table["dataset_name"],
            table_name= table["table_name"],
            json_descriptions= response_gpt
        )     

    end_time = time.time()
    duration = (end_time - start_time) / 60
    print(f"Execution time: {duration} minutes")