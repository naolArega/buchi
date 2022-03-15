from core import mongodb

pets = mongodb.buchi.pets

async def get_pets():
    return await pets.find_one()