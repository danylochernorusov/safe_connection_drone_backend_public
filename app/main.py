from fastapi import FastAPI
from message_router import router as message_router
from auth import router as authorization_router
from user_router import router as user_router

app = FastAPI()

app.include_router(authorization_router)
app.include_router(message_router)
app.include_router(user_router)