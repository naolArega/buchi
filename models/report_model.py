from datetime import date
from pydantic import BaseModel, Field

class CustomerModel(BaseModel):
    from_date: date = Field(...)
    to_date: date = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "from_date": "March 22, 2022",
                "to_date": "April 12, 2022"
            }
        }