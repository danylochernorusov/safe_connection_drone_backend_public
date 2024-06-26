from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from repository import UserRepository, MessageRepository
from settings import JWTSettings
from schemas import SUser, Response
from typing import Annotated
import jwt

router = APIRouter(tags=["Auth"])
oauth2_sheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")
user_repository = UserRepository()
message_repository = MessageRepository()
jwt_settings = JWTSettings()

@router.post("/api/v1/login/", status_code=status.HTTP_200_OK)
def login(from_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> dict:
    try:
        user_repository.search(from_data.username, from_data.password)
        json_user = {"username": from_data.username, "password": from_data.password}
        token = jwt.encode(json_user, jwt_settings.private_key, jwt_settings.algorithm)
        return {"access_token": token, "token_type": "bearer"}
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

@router.post("/api/v1/registarion/", status_code=status.HTTP_201_CREATED)
def registarion(user: SUser) -> Response:
    user_repository.add(user.username, user.password)

    response = Response(response="user is created")
    return response