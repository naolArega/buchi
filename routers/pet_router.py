from fastapi import APIRouter
from core.buchi_exception import BuchiException
from core.http_utils import Response
from models.pet_model import PetModel
from fastapi.encoders import jsonable_encoder
from services.pet_service import insert_pet, find_pets

router = APIRouter(prefix="/pet", tags=["Pet"])

@router.post("/create_pet", description="This endpoint will add a new pet.")
async def create_pet(pet: PetModel):
    try:            
        pet_id = await insert_pet(jsonable_encoder(pet))
        if pet_id != None:
            return Response("success", "pet_id", pet_id)
        return Response("Error", "message", "pet not added! ")
    except BuchiException as e:
        return Response("error", "message", e.message)
    except:
        return Response("error", "message", "internal server error, please contact the admin.")
        

@router.get("/get_pets", description="This endpoint fetch you a pet based on your criteria.")
async def get_pets(
    limit: int,
    type: str = None,
    gender: str = None,
    size: str = None,
    age: str = None,
    good_with_children: bool = None):
    try:
        pets = await find_pets(limit, type, gender, size, age, good_with_children)
        return Response("success", "pets", pets)
    except BuchiException as e:
        return Response("error", "message", e.message)
    except:
        return Response("error", "message", "internal server error, please contact the admin.")