import json
import requests
import cv2
from PIL import Image
import numpy as np
from io import BytesIO
import base64
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_community.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI

api_key = open(".api_key_tune", "r").read().strip()

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
    
    img = Image.open(BytesIO(base64.b64decode(image)))
    base_width = 300
    wpercent = (base_width / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((base_width, hsize), Image.Resampling.LANCZOS)
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("u8")

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
    resp = chain.invoke({"image": img_str})
    print(resp.content)
    return json.loads(resp.content.replace("```json","").replace("```",""))
