from utils.gcp_operations import GcpToolkit
from utils.openai_gpt import OpenaiGPT
import time


start_time = time.time()


if __name__ == "__main__":

    ########################## GCP ##########################
        
    GCP_TOOLKIT = GcpToolkit()    
    table_columns = GCP_TOOLKIT.get_name_columns_table(dataset="REFINED", 
                                   table_name="SAMPLE")
    sample_table = GCP_TOOLKIT.get_sample_table_bigquery(dataset="REFINED", 
                                    table_name="SAMPLE")
    

    ########################## OPENAI ##########################
    GPT = OpenaiGPT()
    prompt = GPT.build_dictionary_prompt_1(
        dataframe = sample_table,
        columns_name = table_columns
    )

    dictionary_gpt = GPT.send_question_gpt(prompt=prompt)  

    GCP_TOOLKIT.execute_update_descriptions(table_name="SAMPLE", 
                                            dataset="REFINED", json_descriptions=dictionary_gpt)


    end_time = time.time()
    duration = (end_time - start_time) / 60

    print(f"Execution time: {duration} minutes")