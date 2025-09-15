import json
import os
from datetime import datetime
from typing import Any, Dict, List
from uuid import uuid4

import asyncpg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("POSTGRES_URL")
if not DATABASE_URL:
    raise ValueError(
        "Database string connection not found. Please include it in the '.env' file"
    )


class PostgresDb:
    @staticmethod
    def datetime_serialize(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} is not serializable")

    async def __aenter__(self):
        self.pool = await asyncpg.create_pool(DATABASE_URL)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.pool.close()

    async def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        user_id = user_data["id"] or str(uuid4())
        data_json = json.dumps(user_data, default=PostgresDb.datetime_serialize)

        async with self.pool.acquire() as conn:
            query = """
                INSERT INTO users(id, username, email, data, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5, $6)
                RETURNING *
            """
            row = await conn.fetchrow(
                query,
                user_id,
                user_data["username"],
                user_data["email"],
                data_json,
                user_data["created_at"],
                user_data["updated_at"],
            )
            if row:
                return {
                    "id": row["id"],
                    "username": row["username"],
                    "email": row["email"],
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"],
                }

            return {}

    async def get_user(self, user_id: str) -> Dict[str, Any]:
        async with self.pool.acquire() as conn:
            query = """
                SELECT * FROM users WHERE id = $1
            """
            row = await conn.fetchrow(query, user_id)
            if row:
                return {
                    "id": row["id"],
                    "username": row["username"],
                    "email": row["email"],
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"],
                }

            return None

    async def get_users(self) -> List[Dict[str, Any]]:
        async with self.pool.acquire() as conn:
            query = """
                SELECT * FROM users
            """
            rows = await conn.fetch(query)
            users = []
            for row in rows:
                users.append(
                    {
                        "id": row["id"],
                        "username": row["username"],
                        "email": row["email"],
                        "created_at": row["created_at"],
                        "updated_at": row["updated_at"],
                    }
                )

            return users

    async def update_user(self, user_id: str, update_entry: Dict[str, Any]) -> None:
        data_json = json.dumps(update_entry, default=PostgresDb.datetime_serialize)
        update_entry["updated_at"] = datetime.now()

        async with self.pool.acquire() as conn:
            query = """
                UPDATE users
                SET username = $2, email = $3, data = $4, updated_at = $5
                WHERE id = $1
            """
            await conn.execute(
                query,
                user_id,
                update_entry["username"],
                update_entry["email"],
                data_json,
                update_entry["updated_at"],
            )

    async def delete_user(self, user_id: str) -> None:
        async with self.pool.acquire() as conn:
            query = """
                DELETE FROM users
                WHERE id = $1
            """
            await conn.execute(query, user_id)

    async def delete_users(self) -> None:
        async with self.pool.acquire() as conn:
            query = """
                DELETE FROM users
            """
            await conn.execute(query)
