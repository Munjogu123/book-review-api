import logging
from datetime import datetime
from typing import Any, Dict, List

from db.users import PostgresDb

logger = logging.getLogger("__name__")


class UserService:
    def __init__(self, db: PostgresDb):
        self.db = db
        logger.debug("User service initialized with PostgresDb client")

    async def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Creating new entries")
        now = datetime.now()
        user = {**user_data, "created_at": now, "updated_at": now}
        logger.debug("Successfully created a user")

        return user

    async def get_user(self, user_id: str) -> Dict[str, Any]:
        logger.info("Getting user info")
        user_data = await self.db.get_user(user_id)
        if user_data:
            logger.debug("Found user %s", user_id)
        else:
            logger.warning("Could not find user %s", user_id)

        return user_data

    async def get_users(self) -> List[Dict[str, Any]]:
        logger.info("Getting all users info")
        users = await self.db.get_users()
        if users:
            logger.debug("Found all users")
        else:
            logger.warning("No users found")

        return users

    async def update_user(
        self, user_id: str, updated_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        logger.info("Updating user info")
        old_user = await self.db.get_user(user_id)
        if not old_user:
            logger.warning("User %s not found", user_id)
            return None

        new_user = {
            **old_user,
            **updated_data,
            "id": user_id,
            "created_at": old_user["created_at"],
            "updated_at": datetime.now(),
        }
        await self.db.update_user(user_id, new_user)
        logger.debug("Successfully updated user info")

        return new_user

    async def delete_user(self, user_id: str) -> None:
        logger.info("Deleting a user")
        user = await self.db.get_user(user_id)
        if not user:
            logger.warning("User %s not found", user_id)
            return None

        await self.db.delete_user(user_id)
        logger.debug("Successfully deleted a user")

    async def delete_users(self) -> None:
        logger.info("Deleting all users")
        users = await self.db.get_users()
        if not users:
            logger.warning("Users not found")
            return None

        await self.db.delete_users()
        logger.debug("Successfully deleted all users")
