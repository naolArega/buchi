from fastapi import APIRouter
from core.http_utils import Response
from fastapi.encoders import jsonable_encoder
from core.buchi_exception import BuchiException
from models.customer_model import CustomerModel
from services.customer_service import insert_customer

router = APIRouter(prefix="/customer", tags=["Customer"])

@router.post("/add_customer", description="This endpoint will create a new customer and store in the local database.")
async def add_customer(customer: CustomerModel):
   try:
      customer_id = await insert_customer(jsonable_encoder(customer))
      return Response("success", "customer_id", customer_id)
   except BuchiException as e:
      return Response("error", "message", e.message)
   except:
      return Response("error", "message", "internal server error, please contact the admin.")