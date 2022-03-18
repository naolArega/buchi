import pymongo
from core import mongodb
from datetime import date
from services.pet_service import find_pet
from core.buchi_exception import BuchiException
from services.customer_service import find_customer

adoptions_collection = mongodb.buchi.get_collection('adoptions')

async def insert_adoption_request(adoption: dict):
    customer = await find_customer(adoption["customer_id"])
    if customer == None:
        raise BuchiException("customer doesn't exist")
    pet = await find_pet(adoption["pet_id"])
    if pet == None:
        raise BuchiException("pet doesn't exist")
    customer.pop("_id")
    adoption.update(customer)
    pet.pop("photos")
    pet.pop("_id")
    adoption.update(pet)
    try:        
        result = await adoptions_collection.insert_one(adoption)
        return result.inserted_id
    except:
        raise BuchiException("unable to add adoption request")

async def find_adoption_requests(from_date: date, to_date: date):
    try:
        adoption_requests = await adoptions_collection.find({
            "request_date": {'$lte': to_date.isoformat(), '$gte': from_date.isoformat()}
        }).sort("request_date", pymongo.DESCENDING).to_list(length=None)
        return remove_request_date_and_id(adoption_requests)
    except:
        raise BuchiException("unable to fetch adoptions requests")

def remove_request_date_and_id(adoption_requests: list):
    cleanded_adoption_requests = []
    for adoption_request in adoption_requests:
        adoption_request.pop("request_date")
        adoption_request.pop("_id")
        cleanded_adoption_requests.append(adoption_request)
    return cleanded_adoption_requests