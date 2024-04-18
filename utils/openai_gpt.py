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

        response = self.openai_client.chat.completions.create(
            model= MODEL_ENGINE, # model = "deployment_name".
            messages=[
                {"role": "system", "content": "Você Data Analyst expecialista em documentação e discionário de dados."},
                {"role": "user", "content": prompt}
            ]
        )

        response_txt = response.choices[0].message.content

        start_json = response_txt.find("{")
        end_json = response_txt.find("}")

        json_data = json.loads(response_txt[start_json:end_json + 1])

        return json.dumps(json_data, indent=4, ensure_ascii=False)