from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

router = InferringRouter()


@cbv(router)
class ExercisesController:
    @router.get("/")
    def read_root(self):
        return {"message": "Welcome to Exercises API"}
