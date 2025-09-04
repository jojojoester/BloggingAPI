from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")

client = AsyncIOMotorClient(MONGODB_URL)
#database
db = client["Blog"]
#collections
users_collection = db["users"]
posts_collection = db["posts"]
comments_collection = db["comments"]