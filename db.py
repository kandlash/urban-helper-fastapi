from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGOURI")
client = AsyncIOMotorClient(MONGO_URI)
db = client.urban_work