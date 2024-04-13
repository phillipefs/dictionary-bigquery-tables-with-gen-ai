from utils.gcp_operations import Gcp_Toolkit
from utils.openai_gpt import OpenaiGPT

GCP_TOOLKIT = Gcp_Toolkit()


table_columns = GCP_TOOLKIT.get_name_columns_table(dataset="gasolina_brasil", 
                                   table_name="tb_historico_combustivel_brasil")

sample_table = GCP_TOOLKIT.get_sample_table_bigquery(dataset="gasolina_brasil", 
                                   table_name="tb_historico_combustivel_brasil")


# text_prompt = f"""
# Você é um experiente analista de dados. 
# Tenho uma tabela com as seguintes colunas: {table_columns}. Por favor, me forneça um JSON contendo o nome de cada coluna e uma descrição do que ela representa na tabela.
# Exemplo dos dados:
# {sample_table}

# Exemplo de saída esperada:
# {{
#     "Nome da coluna (Exatamente como informada no prompt)":"Descrição",
#     "Nome da coluna (Exatamente como informada no prompt)":"Descrição",
#     "Nome da coluna (Exatamente como informada no prompt)":"Descrição",
#     ...
# }}
# """
text_prompt = f"""
Você está encarregado de documentar uma tabela no BigQuery para os stakeholders. A tabela possui as seguintes colunas:

{table_columns}

Exemplo dos dados:
{sample_table}

Faça uma analise profunda dos nome das colunas e do exemplo enviado, e crie descrições ricas e objetivas, para auxiliar stackholders a entenderem o propósito da tabela. 
A saída esperada é um JSON contendo o nome de cada coluna e sua descrição correspondente, conforme exemplificado abaixo:

{{
    "Nome_da_Coluna": "Descrição",
    "Nome_da_Coluna": "Descrição",
    "Nome_da_Coluna": "Descrição",
    ...
}}
"""


GPT = OpenaiGPT()

print(GPT._send_question_gpt(text_prompt))