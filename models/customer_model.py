from bson import ObjectId
from pydantic import BaseModel, Field
from core.mogodb_object_id import MongoDBObjectId

class CustomerModel(BaseModel):
    id: MongoDBObjectId = Field(default_factory=MongoDBObjectId, alias="_id")
    name: str = Field(...)
    phone: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "phone": "0911121314"
            }
        }