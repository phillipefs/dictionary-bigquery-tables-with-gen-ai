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
        You are tasked with documenting a BigQuery table for stakeholders. The table contains the following columns:

        {columns_name}

        Data sample:
        {df}

        Perform a thorough analysis of the column names and the provided sample, and create rich yet concise descriptions to help stakeholders understand the table's purpose.
        The expected output is a JSON containing the name of each column and its corresponding description, as shown below:

        {{
            "Column_Name": "Description",
            "Column_Name": "Description"
            ...
        }}
        """
        return prompt

    def build_dictionary_prompt_1(self, dataframe: DataFrame, columns_name: str):
        df = dataframe.to_string()

        prompt = f"""
        Objetivo: Sua tarefa é documentar as colunas de uma tabela no BigQuery para fornecer um entendimento claro para todos os stakeholders, focando unicamente no propósito ou função de cada coluna. 
        Analise os nomes das colunas e gere descrições que transmitam o papel delas dentro da tabela. É importante evitar discutir o tipo de dado ou dar exemplos do conteúdo dos dados
        Colunas para documentar:

        {columns_name}

        Exemplo das primeiras linhas da tabela:
        {df}

        Orientações:
        - Foque no significado de cada coluna dentro do contexto da tabela e faça uma descrição completa.
        - Exclua qualquer menção a tipos de dados ou exemplos específicos de dados.

        Resultado esperado:

        {{
            "Column_Name": "Description",
            "Column_Name": "Description"
            ...
        }}

        """
        return prompt

    def send_question_gpt(self, prompt:str)->json:

        response = self.openai_client.chat.completions.create(
            model= MODEL_ENGINE, # model = "deployment_name".
            messages=[
                {"role": "system", "content": "You are a Data Analyst specialized in data documentation and data dictionaries."},
                {"role": "user", "content": prompt}
            ]
        )

        response_txt = response.choices[0].message.content

        start_json = response_txt.find("{")
        end_json = response_txt.find("}")

        json_data = json.loads(response_txt[start_json:end_json + 1])

        return json_data