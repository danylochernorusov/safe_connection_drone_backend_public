from fastapi import APIRouter, Depends, status, HTTPException
from get_current_user import get_current_user
from sqlalchemy import text
from database import User, engine
from repository import UserRepository
from schemas import Response
from typing import Annotated

router = APIRouter(prefix="/api/v1/users", tags=["Users"])
user_repository = UserRepository()

@router.get("", status_code=status.HTTP_200_OK)
def get_users(current_user: Annotated[User, Depends(get_current_user)]) -> list:
    users = user_repository.get_all()
    list_users = []
    for user in users:
        list_users.append(user.get_json_without_password())

    return list_users

@router.delete("", status_code=status.HTTP_200_OK)
def delete_my_account(current_user: Annotated[User, Depends(get_current_user)], password: str) -> Response:
    try:
        user_repository.search(current_user.get_username(), password)
        user_repository.delete(current_user.id)

        response = Response(response="the account has been deleted")
        return response
    except:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@router.get("/search", status_code=status.HTTP_200_OK)
def search_user(current_user: Annotated[User, Depends(get_current_user)], username: str) -> list:
    with engine.connect() as connect:
        response = connect.execute(text(f"SELECT * FROM users WHERE username LIKE '%{username}%'"))

    users = []
    for user in response:
        users.append({"id": user[0], "username": user[1]})
    
    return users