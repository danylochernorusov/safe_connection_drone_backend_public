from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from repository import UserRepository
from settings import JWTSettings
from typing import Annotated
import jwt

oauth2_sheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")
user_repository = UserRepository()
jwt_settings = JWTSettings()

def get_current_user(token: Annotated[str, Depends(oauth2_sheme)]):
    try:
        json_user = jwt.decode(token, jwt_settings.public_key, algorithms=[jwt_settings.algorithm])
        user = user_repository.search(json_user["username"], json_user["password"])
        return user
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)