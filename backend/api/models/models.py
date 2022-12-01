import datetime
from bson import ObjectId
from pydantic import BaseModel, Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class ExerciseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    axis_x: float = Field(...)
    axis_y: float = Field(...)
    axis_z: float = Field(...)
    created_at: datetime.datetime = datetime.datetime.now()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "axis_x": -3660,
                "axis_y": 14988,
                "axis_z": -9908,
                "date": "2021-05-22 11:25",
            }
        }


class InferenceModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    ms_circle_arm: float = Field(...)
    ms_frontal_arm: float = Field(...)
    ms_no_movement: float = Field(...)
    ms_side_arm: float = Field(...)
    ms_upper_arm: float = Field(...)
    created_at: datetime.datetime = datetime.datetime.now()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "ms_circle_arm": -3660,
                "ms_frontal_arm": 14988,
                "ms_no_movement": -9908,
                "ms_side_arm": -9908,
                "ms_upper_arm": -9908,
                "date": "2021-05-22 11:25",
            }
        }


class ExerciseInput(BaseModel):
    axis_x: float
    axis_y: float
    axis_z: float

    def to_list(self):
        return [self.axis_x, self.axis_y, self.axis_z]
