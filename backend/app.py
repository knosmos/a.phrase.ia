from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from prompts import *
import json
import llm
import diffusion_hf

class SentenceGenPayload(BaseModel):
    user_id: str
    emoji_seq: List[str]

class ImageDescPayload(BaseModel):
    user_id: str
    b64_image: str

class ImageGenPayload(BaseModel):
    user_id: str
    description: str

class RecommendationPayload(BaseModel):
    user_id: str
    emoji_seq: List[str]

app = FastAPI()

@app.get("/")
async def index():
    return "all systems nominal"

@app.post("/sentence-gen")
async def sentence_gen(payload: SentenceGenPayload):
    return llm.run_text(
        SENTENCE_GEN_PROMPT,
        emoji_seq=",".join(payload.emoji_seq)
    )

@app.post("/image-description")
async def image_description(payload: ImageDescPayload):
    text_json = llm.run_multimodal(
        PICTURE_TO_TEXT_PROMPT,
        image=payload.b64_image
    )
    text_json["emoji"] = diffusion.gen_emoji(
        "data:image/jpeg;base64," + text_json["long"]
    )
    return text_json

@app.post("/image-gen")
async def image_gen(payload: ImageGenPayload):
    return diffusion.gen_emoji(
        payload.description
    )

@app.post("/recommend")
async def recommend(payload: RecommendationPayload):
    return "get some sleep"
