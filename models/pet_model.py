from fastapi import Body
from bson import ObjectId
from pydantic import BaseModel, Field
from core.py_object_id import PyObjectId

class PetModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    type: str = Field(...)
    gender: str = Field(...)
    size: str = Field(...)
    age: str = Field(...)
    photo: list[str] = Body([])
    good_with_children: bool = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "type": "Jane Doe",
                "gender": "male",
                "size": "small",
                "age": 5,
                "photo": ["Binary file"],
                "good_with_children": True
            }
        }