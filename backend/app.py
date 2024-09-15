from fastapi import FastAPI
from pymongo import MongoClient

from pydantic import BaseModel
from typing import List
from prompts import *
import json
import llm
import diffusion

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

class UpdatePreviousPayload(BaseModel):
    user_id: str
    previous_data: list

app = FastAPI()

MONGODB_URI = "mongodb+srv://zjaden28:Qfr6Oa7QwR3VVnda@users.4zutr.mongodb.net/?retryWrites=true&w=majority&ssl=true&appName=users&tlsCAFile=isrgrootx1.pem"
DB_NAME="users"


@app.get("/")
async def index():
    return "all systems nominal"

@app.post("/sentence-gen")
async def sentence_gen(payload: SentenceGenPayload):
    return llm.run_text(
        SENTENCE_GEN_PROMPT,
        emoji_seq=",".join(payload.emoji_seq)
    )

# @app.post("/image-description")
# async def image_description(payload: ImageDescPayload):
#     text_json = llm.run_multimodal(
#         PICTURE_TO_TEXT_PROMPT,
#         image=payload.b64_image
#     )
#     text_json["emoji"] = diffusion.gen_emoji(
#         "data:image/jpeg;base64," + text_json["short"]
#     )
#     return text_json

# @app.post("/image-gen")
# async def image_gen(payload: ImageGenPayload):
#     return diffusion.gen_emoji(
#         payload.description
#     )

@app.post("/recommend")
async def recommend(payload: RecommendationPayload):
    return "get some sleep"

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(MONGODB_URI)
    app.database = app.mongodb_client[DB_NAME]
    app.collection = app.database["users"]
    print("Connected to the MongoDB database!")
    print(app.collection)

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

'''
from models import User

@app.post("/user")
def create_user(request: Request, user: User = Body(...)):
    print("HI")
    app.mongodb_client = MongoClient(MONGODB_URI)
    app.database = app.mongodb_client[DB_NAME]
    collection = app.database["users"]

    print("HI")
    print(collection)

    new_user = collection.insert_one(user)
    print("HI")

    created_user = collection.find_one(
        {"_id": new_user.inserted_id}
    )

    return created_user
'''

@app.post("/user")
def create_user(uid):
    user = {
        "user_id": uid,
        "previous_data": [],
        "custom_icons": [],
        "constant_icons": []
    }
    app.collection.insert_one(user)