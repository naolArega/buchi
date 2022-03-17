import asyncio
from decouple import config
from motor.motor_asyncio import AsyncIOMotorClient

cs = config("MONGODB_CS")
client = AsyncIOMotorClient(cs)
client.get_io_loop = asyncio.get_running_loop
buchi = client.get_database('buchi')