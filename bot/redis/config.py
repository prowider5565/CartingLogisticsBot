import redis as redis_sdk

from bot.settings import settings


redis = redis_sdk.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
