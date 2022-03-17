from datetime import date
from bson import ObjectId
from pydantic import BaseModel, Field
from core.mogodb_object_id import MongoDBObjectId

class AdoptionModel(BaseModel):
    id: MongoDBObjectId = Field(default_factory=MongoDBObjectId, alias="_id")
    customer_id: str = Field(...)
    pet_id: str = Field(...)
    request_date: date = Field(date.today())

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "customer_id": "6231bdaf6d92a353a4b905c2",
                "pet_id": "6231bdd56d92a353a4b905c3"
            }
        }