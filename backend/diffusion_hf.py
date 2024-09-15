import requests
import io
import base64
from PIL import Image

API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.content

def gen_emoji(description):
    image_bytes = query({
        "inputs": description + ", realistic shading, white blank background",
    })
    image = Image.open(io.BytesIO(image_bytes))
    image.save("tmp.png")
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("u8")
    return img_str

if __name__ == "__main__":
    gen_emoji(input())