from bson import ObjectId
from pydantic import BaseModel, Field
from core.mogodb_object_id import MongoDBObjectId

class PetModel(BaseModel):
    id: MongoDBObjectId = Field(default_factory=MongoDBObjectId, alias="_id")
    type: str = Field(...)
    gender: str = Field(...)
    size: str = Field(...)
    age: str = Field(...)
    photos: list[dict[str, str]] = Field(...)
    good_with_children: bool = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "type": "Cat",
                "gender": "male",
                "size": "medium",
                "age": "baby",
                "photos": [
                    {
                        "data": "in base64",
                        "extension": "png"
                    }
                ],
                "good_with_children": True
            }
        }