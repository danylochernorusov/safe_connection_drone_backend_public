from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from repository import UserRepository, MessageRepository
from settings import JWTSetings
from schemas import SUser
from typing import Annotated
import jwt

router = APIRouter(tags=["Auth"])
oauth2_sheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")
user_repository = UserRepository()
message_repository = MessageRepository()
jwt_settings = JWTSetings()

def get_current_user(token: Annotated[str, Depends(oauth2_sheme)]):
    try:
        json_user = jwt.decode(token, jwt_settings.public_key, algorithms=[jwt_settings.algorithm])
        user = user_repository.search(json_user["username"], json_user["password"])
        return user
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@router.post("/api/v1/login/")
def login(from_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        user_repository.search(from_data.username, from_data.password)
        json_user = {"username": from_data.username, "password": from_data.password}
        token = jwt.encode(json_user, jwt_settings.private_key, jwt_settings.algorithm)
        return {"access_token": token, "token_type": "bearer"}
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

@router.post("/api/v1/registarion/")
def registarion(user: SUser):
    user_repository.add(user.username, user.password)

    return True