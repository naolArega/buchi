from fastapi import APIRouter
from core.http_utils import Response
from models.customer_model import CustomerModel

router = APIRouter(prefix="/customer", tags=["Customer"])

@router.post("/add_customer", description="This endpoint will create a new customer and store in the local database.")
def add_customer(customer: CustomerModel):
   return Response("success", "customer_id", customer.id)