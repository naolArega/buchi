from datetime import datetime, timedelta
import aiohttp
from decouple import config
from fastapi.encoders import jsonable_encoder
from core.buchi_exception import BuchiException

pet_finder_api = "https://api.petfinder.com/v2"
token_type = ""
token = ""
token_expiration_date = datetime.now()

async def get_pet_finder_pets(limit, type, gender, size, age, good_with_children):    
    global token
    animal_endpoint = f"{pet_finder_api}/animals"
    query_parameters = generate_query_string(limit, type, gender, size, age, good_with_children)
    if token == "" or datetime.now() >= token_expiration_date :
        await get_token()
    headers = {
        "Authorization": f"{token_type} {token}"
    }
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(f"{animal_endpoint}{query_parameters}") as response:
                if response.status == 401:
                    token = ""
                    return None
                elif response.status != 200 and response.status == 401:
                    return None
                pets = jsonable_encoder(await response.json())
                return map_pet_finder_response(pets["animals"])
    except:
        return None

async def get_token():
    global token_type
    global token
    global token_expiration_date
    token_endpoint = f"{pet_finder_api}/oauth2/token"
    api_key = config("PETFINDER_API_KEY")
    client_secret = config("PETFINDER_CLIENT_SECRET")
    form_data = {
        "grant_type": "client_credentials",
        "client_id": api_key,
        "client_secret": client_secret
    }
    try:        
        async with aiohttp.ClientSession() as session:
            async with session.post(token_endpoint, data=form_data) as response:
                if response.status != 200:
                    return None           
                token_response = jsonable_encoder(await response.json())
                token_type = token_response["token_type"]
                token = token_response["access_token"]
                token_expiration_date = datetime.now() + timedelta(seconds=token_response["expires_in"])
    except:
        raise BuchiException("Unable to get token")


def map_pet_finder_response(pets):
    pet_finder_pets = []
    if pets != None:
        for pet in pets:
            pet_finder_pets.append({
                "pet_id": pet.get("id", "0"),
                "type": pet.get("type", "Cat"),
                "gender": pet.get("gender", "male"),
                "size": pet.get("size", "small"), 
                "age": pet.get("age", "baby"),
                "good_with_children": pet.get("good_with_children", True),
                "photos": map_photos(pet.get("photos", [])),
                "source": "petfinder"
            })
    return pet_finder_pets

def map_photos(photos):
    normalized_photos = []
    if photos != None:
        for photo in photos:
            if dict.get(photo, "full", None) != None:
                normalized_photos.append({
                    "url": photo["full"]
                })
    return normalized_photos


def generate_query_string(limit, type, gender, size, age, good_with_children):
    query_string = f"?limit={limit}"
    if type != None: query_string + f"&type={type}"
    if gender != None: query_string + f"&gender={gender}"
    if gender != None: query_string + f"&size={size}"
    if gender != None: query_string + f"&age={age}"
    if gender != None: query_string + f"&good_with_children={good_with_children}"
    return query_string