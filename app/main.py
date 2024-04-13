from fastapi import FastAPI
from routers.auth_router import router as authorization_router
from routers.message_router import router as message_router
from routers.user_router import router as user_router
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from settings import RedisSetings

app = FastAPI()
redis_settings = RedisSetings()

app.include_router(authorization_router)
app.include_router(message_router)
app.include_router(user_router)

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(f"redis://{redis_settings.host}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")