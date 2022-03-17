from core import mongodb
from core.buchi_exception import BuchiException

customers_collection = mongodb.buchi.customers

async def insert_customer(customer: dict):
    try:
        previous_customer = await customers_collection.find_one({"phone": customer["phone"]})
        if previous_customer != None:
            return previous_customer["_id"]    
        result = await customers_collection.insert_one(customer)
        return result.inserted_id
    except:
        raise BuchiException("Unable to insert customer, please contact the admin.")

async def find_customer(id: str):
    try:
        return await customers_collection.find_one({"_id": id})
    except:
        raise BuchiException("unable to fetch customer")
