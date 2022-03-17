from datetime import date
from fastapi import APIRouter
from core.buchi_exception import BuchiException
from core.http_utils import Response
from fastapi.encoders import jsonable_encoder
from models.adoption_model import AdoptionModel
from services.adoption_service import insert_adoption_request, find_adoption_requests

router = APIRouter(prefix="/adoption", tags=["Adoption"])

@router.post("/adopt", description="This endpoint will create an adoption requested to adopt a pet.")
async def adopt(adoption: AdoptionModel):
    try:        
        adoption_id = await insert_adoption_request(jsonable_encoder(adoption))
        return Response("success", "addoption_id", adoption_id)
    except BuchiException as e:
        return Response("error", "message", e.message)
    except:
        return Response("error", "message", "internal server error, please contact the admin.")

@router.get("/get_adoption_requests", description="This endpoint will fetch all adoption requests in date range.")
async def get_adoption_requests(from_date: date, to_date: date):
    try:
        adoption_requests = await find_adoption_requests(from_date, to_date)
        return Response("success", "data", adoption_requests)
    except BuchiException as e:
        return Response("error", "message", e.message)
    except:
        return Response("error", "message", "internal server error, please contact the admin.")