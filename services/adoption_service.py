from core import mongodb
import pymongo
from datetime import date, timedelta
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

async def get_weekly_adoption_request(from_date: str, to_date: str):
    try:        
        start_date = date.fromisoformat(from_date)
        to_date = date.fromisoformat(to_date)
        end_date = to_date
        weekly_adoption_request_reports = {}
        while start_date < to_date:
            days_until_last_date = (to_date - start_date).days
            if days_until_last_date < 7:
                end_date = start_date + timedelta(days=days_until_last_date)
            else:
                end_date = start_date + timedelta(days=7)
            adoption_request_count = await adoptions_collection.count_documents({
                "request_date": {'$gte': start_date.isoformat(), '$lte': end_date.isoformat()}
            })
            weekly_adoption_request_reports.update({start_date.isoformat(): adoption_request_count})
            start_date = end_date
        return weekly_adoption_request_reports
    except:
        raise BuchiException("unable to generate weekly adoption requests")

def remove_request_date_and_id(adoption_requests: list):
    cleanded_adoption_requests = []
    for adoption_request in adoption_requests:
        adoption_request.pop("request_date")
        adoption_request.pop("_id")
        cleanded_adoption_requests.append(adoption_request)
    return cleanded_adoption_requests