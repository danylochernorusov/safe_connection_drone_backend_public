from fastapi import APIRouter, Depends
from get_current_user import get_current_user
from sqlalchemy import text
from database import User, engine
from repository import UserRepository
from typing import Annotated

router = APIRouter(prefix="/api/v1/users", tags=["Users"])
user_repository = UserRepository()

@router.get("")
def get_users(current_user: Annotated[User, Depends(get_current_user)]):
    users = user_repository.get_all()
    list_users = []
    for user in users:
        list_users.append(user.get_json_without_password())

    return list_users

@router.delete("")
def delete_my_account(current_user: Annotated[User, Depends(get_current_user)], password: str):
    try:
        user_repository.search(current_user.get_username(), password)
        user_repository.delete(current_user.id)

        return True
    except:
        return False

@router.get("/search")
def search_user(current_user: Annotated[User, Depends(get_current_user)], username: str):
    with engine.connect() as connect:
        response = connect.execute(text(f"SELECT * FROM users WHERE username LIKE '%{username}%'"))

    users = []
    for user in response:
        users.append({"id": user[0], "username": user[1]})
    
    return users