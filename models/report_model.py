from datetime import date
from pydantic import BaseModel, Field

class ReportModel(BaseModel):
    from_date: date = Field(...)
    to_date: date = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "from_date": "2022-03-16",
                "to_date": "2022-03-16"
            }
        }