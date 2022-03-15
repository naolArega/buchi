from fastapi import APIRouter
from models.pet_model import PetModel
from core.http_utils import Response

router = APIRouter(prefix="/pet", tags=["Pet"])

@router.post("/create_pet", description="This endpoint will add a new pet.")
def create_pet(pet: PetModel):
    return Response("success", "pet_id", pet.id)

@router.get("/get_pets", description="This endpoint fetch you a pet based on your criteria.")
def get_pets(
    type: str = None,
    gender: str = None,
    size: str = None,
    age: int = None,
    good_with_children: bool = None,
    limit: int = None):
    return Response("success", "pets", "123123123")