from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from prompts import *
import json
import llm
import diffusion_hf as diffusion
import ngram
import mongo

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
    mongo.collection.update_one({
        "uid": payload.user_id
    }, {
        "$addToSet" : {
            "history": payload.emoji_seq
        }
    })
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
    mongo.collection.update_one({
        "uid": payload.user_id
    }, {
        "$addToSet" : {
            "custom_emoji": text_json
        }
    })
    return text_json

@app.post("/image-gen")
async def image_gen(payload: ImageGenPayload):
    res = diffusion.gen_emoji(
        payload.description
    )
    return res

@app.post("/recommend")
async def recommend(payload: RecommendationPayload):
    live_list = set()
    for i in payload.emoji_seq:
        try:
            live_list |= ngram.get_results(i, 2)
        except:
            pass
    live_list = list(live_list)
    n = max(0, 40 - len(live_list))
    return live_list + ngram.get_initial(n)

@app.post("/create-user")
async def create_user(uid):
    mongo.collection.insert_one({
        "uid": uid,
        "custom_emoji": [],
        "history": []
    })

@app.get("/load-user")
async def load_user(uid):
    data = mongo.collection.find_one({"uid": uid})
    ngram.load_lines(data.history)
    return data