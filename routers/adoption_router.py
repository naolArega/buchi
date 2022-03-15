from fastapi import APIRouter

router = APIRouter(prefix="/adoption", tags=["Adoption"])

@router.post("/adopt", description="This endpoint will create an adoption requested to adopt a pet.")
def adopt():
    pass