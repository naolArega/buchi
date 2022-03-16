import aiohttp
from decouple import config
from fastapi.encoders import jsonable_encoder
from core.buchi_exception import BuchiException

pet_finder_api = "https://api.petfinder.com/v2"
bearer_token = None

async def get_pet_finder_pets(limit, type, gender, size, age, good_with_children):
    animal_endpoint = f"{pet_finder_api}/animals"
    query_parameters = generate_query_string(limit, type, gender, size, age, good_with_children)
    try:
        if bearer_token == None:
            bearer_token = await get_token()
        headers = {
            "Authorization": f"Bearer {bearer_token}"
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(f"{animal_endpoint}{query_parameters}") as response:
                if response.status == 401:
                    bearer_token = None
                    return None
                elif response.status != 200 and response.status == 401:
                    return None
                pets = jsonable_encoder(await response.json())
                return map_pet_finder_response(pets["animals"])
    except:
        return None

async def get_token():
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
                return token_response["access_token"]
    except:
        raise BuchiException("Unable to get token")


def map_pet_finder_response(pets):
    pet_finder_pets = []
    if pets != None:
        for pet in pets:
            pet_finder_pets.append({
                "_id": pet["id"],
                "type": pet["type"],
                "gender": pet["gender"],
                "size": pet["size"], 
                "age": pet["age"],
                "good_with_children": pet["good_with_children"],
                "photos": map_photos(pet["photos"]),
                "source": "petfinder"
            })

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