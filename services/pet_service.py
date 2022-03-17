import os
import aiofiles
from hashlib import md5
from core import mongodb
from decouple import config
from base64 import b64decode
from core.buchi_exception import BuchiException
from services.pet_finder_service import get_pet_finder_pets

pets_collection = mongodb.buchi.get_collection('pets')
host = config("HOST")
port = config("PORT")

async def insert_pet(pet: dict):
    photo_urls = []
    for photo in pet['photos']:
        if dict.get(photo, "data", None) == None or dict.get(photo, "extension", None) == None:
            raise BuchiException("photo doesn't include data or extension")
        try:
            url = await save_photo(photo['data'], photo['extension'])
            if url == None:
                raise Exception()
        except:
            raise BuchiException("Unable to save photo to the database, please check if you send a correct photo format.")
        photo_urls.append({"url": url})
    pet['photos'] = photo_urls
    try:
        result = await pets_collection.insert_one(pet)
        return result.inserted_id
    except:
        raise BuchiException("Unable to added pet, please contact the admin.")

async def find_pets(limit, type, gender, size, age, good_with_children):
    pets_list = []
    try:
        pets_cursor = pets_collection.find(pet_search_criterias(type, gender, size, age, good_with_children)).limit(limit)
        pets_list.extend(map_local_source(await pets_cursor.to_list(length=None)))
    except:
        raise BuchiException("Unable to fetch pets, please contact the admin.")
    pet_finder_pets = await get_pet_finder_pets(limit, type, gender, size, age, good_with_children)
    if pet_finder_pets != None:
        pets_list.extend(pet_finder_pets)
    if len(pets_list) > limit:
        pets_list = pets_list[0:limit]
    return pets_list

async def find_pet(id: str):
    try:
        return await pets_collection.find_one({"_id": id})
    except:
        raise BuchiException("unable to fetch pet")

async def get_adopted_pet_types():
    try:        
        pet_report = {}
        distinct_pets_types = await pets_collection.distinct("type")
        for type in distinct_pets_types:
            pet_count = await pets_collection.count_documents({"type": type})
            pet_report.update({type: pet_count})
        return pet_report
    except:
        raise BuchiException("unable to generate pet report")

def map_local_source(pets_list: list[dict]):
    if pets_list != None:
        local_pets = []
        for pet in pets_list:
            pet.setdefault("pet_id", pet.pop("_id"))
            pet.setdefault("source", "local")
            local_pets.append(pet)
        return local_pets
    return None

def pet_search_criterias(type, gender, size, age, good_with_children):
    criteria = {}
    if type != None: criteria.setdefault("type", type)
    if gender != None: criteria.setdefault("gender", gender)
    if size != None: criteria.setdefault("size", size)
    if age != None: criteria.setdefault("size", size)
    if good_with_children != None: criteria.setdefault("good_with_children", good_with_children)
    return criteria

async def save_photo(data: str, extension: str) -> str:
    binary_data = b64decode(data)
    md5_checksum = generate_md5(binary_data)
    file_name = f"{md5_checksum}.{extension}"
    cdn_path = os.path.abspath('cdn\\photos')
    try:
        async with aiofiles.open(f"{cdn_path}\\{file_name}", mode="w") as f:
            await f.write(binary_data.decode('utf-8'))
        return generate_photo_url(file_name)
    except:
        return None

def generate_md5(data: str):
    return md5(data).hexdigest()

def generate_photo_url(file_name):
    return f"http://localhost:{port}/cdn/photos/{file_name}"
