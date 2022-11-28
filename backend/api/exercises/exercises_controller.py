import typing
from fastapi import Body, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette.requests import Request
from api.models import ExerciseModel, ExerciseInput
import api.config as config
from api.helper import helper
from model_loader import ModelLoader
import numpy as np
import tensorflow as tf

router = InferringRouter()

db = config.client.proyecto_final


async def get_model(req: Request):
    return req.app.state.model


@cbv(router)
class ExercisesController:
    model: ModelLoader = Depends(get_model)

    @router.get("/")
    def read_root(self):
        return {"message": "Welcome to Exercises API"}

    @router.get("/info")
    def model_info(self):
        """Return model information, version, how to call"""
        return {"name": self.model.name, "version": self.model.version}

    @router.get("/health")
    def service_health(self):
        """Return service health"""
        return "ok"

    @router.get("/list", response_description="List all exercises")
    async def list_exercises(self):
        exercises = []
        async for exercise in db["exercises"].find():
            exercises.append(helper.exercise_helper(exercise))
        return exercises

    @router.post(
        "/", response_description="Add new exercise", response_model=ExerciseModel
    )
    async def create_exercise(self, exercise: ExerciseModel = Body(...)):
        exercise = jsonable_encoder(exercise)
        new_exercise = await db["exercises"].insert_one(exercise)
        created_exercise = await db["exercises"].find_one(
            {"_id": new_exercise.inserted_id}
        )
        return created_exercise

    @router.post("/predict", response_description="Predict exercise")
    async def predict_exercise(self, data: typing.List[ExerciseInput]):
        """Return prediction"""
        info_to_predict = [d.to_list() for d in data]

        len_predict = len(info_to_predict)
        data_to_predict = np.zeros((len_predict, 104, 3))

        for i in range(len_predict):
            data_to_predict[i] = np.array(info_to_predict[i])

        predictions = self.model.predict(data_to_predict)

        data = await self.get_prediction_name(predictions)

        prediction = await self.filter_prediction(data)

        return prediction

    async def get_prediction_name(self, predictions):
        dict_predictions = {}

        dict_predictions["ms_circle_arm"] = predictions[0][0] * 100
        dict_predictions["ms_frontal_arm"] = predictions[0][1] * 100
        dict_predictions["ms_no_movement"] = predictions[0][2] * 100
        dict_predictions["ms_side_arm"] = predictions[0][3] * 100
        dict_predictions["ms_upper_arm"] = predictions[0][4] * 100

        return dict_predictions

    async def filter_prediction(self, predictions):
        dict_prediction = {}
        for i, val in predictions.items():
            if val * 100 > 80:
                dict_prediction[i] = val

        return dict_prediction
