from sys import prefix
from fastapi import APIRouter

router = APIRouter(prefix="/report", tags=["Report"])

@router.post("/generate_report", description="This endpoint will create a small report using date range.")
def generate_report():
    pass