from credentials import OPENAI_KEY, API_VERSION, OPENAI_ENDPOINT, MODEL_ENGINE
from openai import AzureOpenAI
import json


class OpenaiGPT:

    openai_client = AzureOpenAI(
    api_key = OPENAI_KEY,
    api_version = API_VERSION,
    azure_endpoint = OPENAI_ENDPOINT
    )

    def _send_question_gpt(self, prompt:str):
        response = self.openai_client.completions.create(
        model=MODEL_ENGINE,
        temperature=0.5,
        max_tokens=2000,
        prompt= prompt
        )
        return response.choices[0].text