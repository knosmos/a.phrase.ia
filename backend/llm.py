import json
import requests
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_community.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI

api_key = open(".api_key_tune", "r").read()

def run_text(template, **kwargs):
    chat_model = ChatOpenAI(
        openai_api_key=api_key,
        openai_api_base="https://proxy.tune.app/",
        model_name="kaushikaakash04/tune-blob"
    )
    prompt = PromptTemplate.from_template(template)
    chain = prompt | chat_model
    resp = chain.invoke(kwargs)
    return resp.content

def run_multimodal(template, image, **kwargs):
    chat_model = ChatOpenAI(
        openai_api_key=api_key,
        openai_api_base="https://proxy.tune.app/",
        model_name="mistral/pixtral-12B-2409"
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", template),
            ("user",
                [
                    {
                        "type": "image_url",
                        "image_url": {"url": "data:image/jpeg;base64,{image}"},
                        # "image_url": {"url": "{image}"},
                    }
                ],
            ),
        ]
    )
    chain = prompt | chat_model
    resp = chain.invoke({"image": image})
    print(resp.content)
    return json.loads(resp.content.replace("```json","").replace("```",""))