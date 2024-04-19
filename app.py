from utils.gcp_operations import GcpToolkit
from utils.openai_gpt import OpenaiGPT


if __name__ == "__main__":

    ########################## GCP ##########################
        
    GCP_TOOLKIT = GcpToolkit()    
    table_columns = GCP_TOOLKIT.get_name_columns_table(dataset="RAW", 
                                   table_name="FUEL_SAMPLE")
    sample_table = GCP_TOOLKIT.get_sample_table_bigquery(dataset="RAW", 
                                    table_name="FUEL_SAMPLE")
    

    ########################## OPENAI ##########################
    GPT = OpenaiGPT()
    prompt = GPT.build_dictionary_prompt(
        dataframe = sample_table,
        columns_name = table_columns
    )

    dictionary_gpt = GPT.send_question_gpt(prompt=prompt)


    print(dictionary_gpt)


