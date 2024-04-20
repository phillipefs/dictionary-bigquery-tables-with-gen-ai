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

    def build_dictionary_prompt(self, dataframe: DataFrame):

        columns_str = ", ".join(list(dataframe.columns))
        df_sample = dataframe.sample(n=20).to_string()

        prompt = f"""
        Objetivo: Sua tarefa é analisar os nomes das colunas e fornecer descrições para cada um delas. 
        Por descrição, queremos um entendimento claro da finalidade ou função da coluna. Por favor, não inclua exemplos dos dados na coluna ou o tipo de dados que ela contém."
        Colunas para documentar:      

        {columns_str}

        Conteúdo da tabela:
        {df_sample}

        Orientações:
            1 - Analise a tabela, e classifique-a dentro de um contexto.
            2 - Com o contexto definido, analise os dados e o nome da coluna, e crie descrição para cada coluna.
            3 - Não exponha conteúdo da coluna na descrição, nem mesmo para exemplificar, também não é necessário expor data types dos dados.

        Resultado esperado:

        {{
            "Column_Name": "Description",
            "Column_Name": "Description"
            ...
        }}

        """
        return prompt
    
    def build_data_quality_prompt(self, dataframe: DataFrame):
        
        df_sample = dataframe.sample(n=20).to_string()

        prompt = f"""
        Objetivo: Melhorar a descrição da resposta anterior utilizando uma nova amostragem.
        As duas regras abaixo são de extrema importância e devem ser respeitadas.

        Regras Importantes:
            1 - Não utilizar exemplos dos dados e nem informações sobre datatypes nas descrição das colunas. 
            2 - Colunas com nome não amigáveis, entenda o contexto da tabela, e a amostra dos dados para criar a descrição.

        Nova Amostragem:
        {df_sample}
        """
        return prompt
    
    def send_question_gpt(self, prompt_dictionary:str, prompt_data_quality:str)->json:

        response = self.openai_client.chat.completions.create(
            model= MODEL_ENGINE, # model = "deployment_name".
            messages=[
                {"role": "system", "content": "You are a Data Analyst specialized in data documentation and data dictionaries."},
                {"role": "user", "content": prompt_dictionary},
                {"role": "user", "content": prompt_data_quality}
            ], 
        )

        response_txt = response.choices[0].message.content

        start_json = response_txt.find("{")
        end_json = response_txt.find("}")

        json_data = json.loads(response_txt[start_json:end_json + 1])

        return json_data