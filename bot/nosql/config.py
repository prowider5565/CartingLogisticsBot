import pymongo

from bot.settings import settings


mongo_client = pymongo.MongoClient(
    host=settings.MONGO_HOST,
    port=settings.MONGO_PORT,
    tz_aware=settings.MONGO_TZ_AWARE,
)
mongo_db = mongo_client[settings.MONGO_NAME]
users_collection = mongo_db["users"]
