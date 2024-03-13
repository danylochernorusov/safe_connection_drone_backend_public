from fastapi import APIRouter, Depends
from routers.auth import get_current_user
from database import User
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