from core import mongodb
from core.buchi_exception import BuchiException
from models.customer_model import CustomerModel

customers = mongodb.buchi.customers

async def insert_customer(customer: CustomerModel):
    try:
        previous_customer = await customers.find_one({"phone": customer["phone"]})
        if previous_customer != None:
            return previous_customer["_id"]    
        result = await customers.insert_one(customer)
        return result.inserted_id
    except:
        raise BuchiException("Unable to insert customer, please contact the admin.")