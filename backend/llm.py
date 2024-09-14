import json
import requests
from langchain_core.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

api_key = open(".api_key", "r").read()

def run_text(template, **kwargs):
    chat_model = ChatOpenAI(
        openai_api_key=api_key,
        openai_api_base="https://proxy.tune.app/",
        model_name="kaushikaakash04/tune-blob"
    )
    return chat_model.predict(
        PromptTemplate.from_template(
            template
        ).format(**kwargs)
    )