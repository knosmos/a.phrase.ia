import httpx
import os
import base64
from PIL import Image
from io import BytesIO

# Replace the empty string with your model id below
model_id = ""
baseten_api_key = os.environ["BASETEN_API_KEY"]

# Function used to convert a base64 string to a PIL image
def b64_to_pil(b64_str):
    return Image.open(BytesIO(base64.b64decode(b64_str)))
    
data = {
  "prompt": 'red velvet cake spelling out the words "FLUX SCHNELL", tasty, food photography, dynamic shot'
}
# Call model endpoint
res = httpx.post(
    f"https://model-{model_id}.api.baseten.co/production/predict",
    headers={"Authorization": f"Api-Key {baseten_api_key}"},
    json=data
)
# Get output image
res = res.json()
output = res.get("data")
# Convert the base64 model output to an image
img = b64_to_pil(output)
img.save("output_image.jpg")