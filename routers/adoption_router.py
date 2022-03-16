from datetime import date
from fastapi import APIRouter

router = APIRouter(prefix="/adoption", tags=["Adoption"])

@router.post("/adopt", description="This endpoint will create an adoption requested to adopt a pet.")
def adopt():
    pass

@router.get("/get_adoption_requests", description="This endpoint will fetch all adoption requests in date range.")
def get_adoption_requests(from_date: date, to_date: date):
    pass