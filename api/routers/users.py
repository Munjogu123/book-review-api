from typing import AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException

from api.db.users import PostgresDb
from api.models.entry import User, UserCreate, UserUpdate
from api.services.users import UserService

user_router = APIRouter()


async def get_user_service() -> AsyncGenerator[UserService, None]:
    async with PostgresDb() as db:
        yield UserService(db)


@user_router.post("/users/")
async def create_user(
    user_data: UserCreate, user_service: UserService = Depends(get_user_service)
):
    try:
        user = User(username=user_data.username, email=user_data.email)
        user_dict = user.model_dump()
        created_user = await user_service.db.create_user(user_dict)

        return {"detail": "User created successfully", "user": created_user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating entry: {str(e)}")


@user_router.get("/users/{user_id}")
async def get_user(user_id: str, user_service: UserService = Depends(get_user_service)):
    user = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@user_router.get("/users")
async def get_users(user_service: UserService = Depends(get_user_service)):
    try:
        users = await user_service.get_users()
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving entry {str(e)}")


@user_router.patch("/users/{user_id}")
async def update_user(
    user_id: str,
    updated_data: UserUpdate,
    user_service: UserService = Depends(get_user_service),
):
    partial_data = updated_data.model_dump(exclude_unset=True)
    updated_user = await user_service.update_user(user_id, partial_data)
    if not update_user:
        raise HTTPException(status_code=404, detail="Entry not found")

    return updated_user


@user_router.delete("/users/{entry_id}")
async def delete_user(
    user_id: str, user_service: UserService = Depends(get_user_service)
):
    user = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await user_service.delete_user(user_id)
    return {"detail": f"Deleted user {user_id}"}


@user_router.delete("/users")
async def delete_users(user_service: UserService = Depends(get_user_service)):
    await user_service.delete_users()
    return {"detail": "Deleted all users"}
