from utils.credentials import OPENAI_KEY, API_VERSION, OPENAI_ENDPOINT, MODEL_ENGINE
from openai import AzureOpenAI
from pandas import DataFrame
import json


class OpenaiGPT:

    openai_client = AzureOpenAI(
    api_key = OPENAI_KEY,
    api_version = API_VERSION,
    azure_endpoint = OPENAI_ENDPOINT
    )

    def build_dictionary_prompt(self, dataframe: DataFrame, columns_name: str):
        df = dataframe.to_string()

        prompt = f"""
        Você está encarregado de documentar uma tabela no BigQuery para os stakeholders. A tabela possui as seguintes colunas:

        {columns_name}

        Exemplo dos dados:
        {df}

        Faça uma analise profunda dos nome das colunas e do exemplo enviado, e crie descrições ricas porem objetivas, para auxiliar stackholders a entenderem o propósito da tabela. 
        A saída esperada é um JSON contendo o nome de cada coluna e sua descrição correspondente, conforme exemplificado abaixo:

        {{
            "Nome_da_Coluna": "Descrição",
            "Nome_da_Coluna": "Descrição"
            ...
        }}
        """
        return prompt

    def send_question_gpt(self, prompt:str)->json:
        response = self.openai_client.completions.create(
        model=MODEL_ENGINE,
        temperature=1,
        max_tokens=2000,
        prompt= prompt
        )
        json_data = json.loads(response.choices[0].text)
        return json.dumps(json_data, indent=4, ensure_ascii=False)