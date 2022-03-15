import motor.motor_asyncio
from decouple import config

cs = config("MONGODB_CS")
client = motor.motor_asyncio.AsyncIOMotorClient(cs)
buchi = client.buchi