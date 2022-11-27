from fastapi import Body, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from api.models import InferenceModel
import api.config as config
from api.helper import helper

router = InferringRouter()

db = config.client.proyecto_final


@cbv(router)
class InferenceController:
    @router.get("/")
    def read_root(self):
        return {"message": "Welcome to Inferences API"}

    @router.get("/health")
    def service_health(self):
        """Return service health"""
        return "ok"

    @router.get("/list", response_description="List all inferences")
    async def list_inferences(self):
        inferences = []
        async for inference in db["inferences"].find():
            inferences.append(helper.inference_helper(inference))
        return inferences

    @router.post(
        "/",
        response_description="inference input",
        response_model=InferenceModel,
    )
    async def store_inference(self, inference: InferenceModel = Body(...)):
        inference = jsonable_encoder(inference)
        new_inference_input = await db["inferences"].insert_one(inference)
        created_inference_input = await db["inferences"].find_one(
            {"_id": new_inference_input.inserted_id}
        )
        return JSONResponse(
            status_code=status.HTTP_201_CREATED, content=created_inference_input
        )

    @router.get("/count")
    async def count_inferences(self):
        counter = await db["inferences"].count_documents({})
        return {"Total Inferences": counter}

    @router.get("/count-by-type")
    async def count_inferences_by_type(self):
        list_counter = []
        inferences = await self.list_inferences()

        for item in inferences:
            del item["id"]
            del item["created_at"]

            for key, val in item.items():
                val = float(val) * 100
                if val >= 80:
                    list_counter.append(key)

        dict_counter = {i: list_counter.count(i) for i in list_counter}

        return dict_counter
