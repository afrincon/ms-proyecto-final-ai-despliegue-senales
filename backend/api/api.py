from fastapi import Body, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mqtt import FastMQTT, MQTTConfig
from fastapi.encoders import jsonable_encoder

from .inferences import router as inferences_router
from .exercises import router as exercises_router
from .models import InferenceModel
from model_loader import ModelLoader
from .config import client

import os
import json

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    app.state.model = ModelLoader(path="modelo.h5", name="model inferences api")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# mqtt
mqtt_config = MQTTConfig(
    host=os.environ.get("HOST", "192.168.1.1"), port=os.environ.get("PORTMQTT", 1883)
)
mqtt = FastMQTT(config=mqtt_config)
mqtt.init_app(app)


@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("/fastapi/mqtt/#")  # subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)


@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    if topic == "/fastapi/mqtt/inference":
        inference_input = InferenceModel(**json.loads(payload))
        await save_inference_message(inference_input)


@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")


@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)


@app.get("/")
def read_root():
    return {"message": "Welcome to proyecto final API"}


app.include_router(
    inferences_router,
    prefix="/inferences",
    tags=["inferences"],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    exercises_router,
    prefix="/exercises",
    tags=["exercises"],
    responses={404: {"description": "Not found"}},
)

## save messages to database

db = client["proyecto_final"]


async def save_inference_message(inference: InferenceModel = Body(...)):
    inference = jsonable_encoder(inference)
    new_inference_input = await db["inferences"].insert_one(inference)
    created_inference_input = await db["inferences"].find_one(
        {"_id": new_inference_input.inserted_id}
    )
    print("Inference message saved: ", created_inference_input)
