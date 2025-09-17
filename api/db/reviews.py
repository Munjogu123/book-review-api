import json
import os
from datetime import datetime
from typing import Any, Dict
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

    async def create_review(self, review_data: Dict[str, Any]) -> Dict[str, Any]:
        review_id = review_data["id"] or str(uuid4())
        data_json = json.dumps(review_data, default=PostgresDb.datetime_serialize)

        async with self.pool.acquire() as conn:
            query = """
                INSERT INTO reviews(id, user_id, book_id, rating, comment, data, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                RETURNING *
            """
            row = await conn.fetchrow(
                query,
                review_id,
                review_data["user_id"],
                review_data["book_id"],
                review_data["rating"],
                review_data["comment"],
                data_json,
                review_data["created_at"],
                review_data["updated_at"],
            )
            if row:
                return {
                    "id": row["id"],
                    "user_id": row["user_id"],
                    "book_id": row["book_id"],
                    "rating": row["rating"],
                    "comment": row["comment"],
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"],
                }

            return {}

    async def get_review(self, review_id: str) -> Dict[str, Any]:
        async with self.pool.acquire() as conn:
            query = """
                SELECT * FROM reviews WHERE id = $1
            """
            row = await conn.fetchrow(query, review_id)
            if row:
                return {
                    "id": row["id"],
                    "user_id": row["user_id"],
                    "book_id": row["book_id"],
                    "rating": row["rating"],
                    "comment": row["comment"],
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"],
                }

            return {}

    async def get_book_reviews(self, book_id: str) -> list[Dict[str, Any]]:
        async with self.pool.acquire() as conn:
            query = """
                SELECT * FROM reviews WHERE book_id = $1
            """
            rows = await conn.fetch(query, book_id)
            reviews = []
            if rows:
                for row in rows:
                    reviews.append(
                        {
                            "id": row["id"],
                            "user_id": row["user_id"],
                            "book_id": row["book_id"],
                            "rating": row["rating"],
                            "comment": row["comment"],
                            "created_at": row["created_at"],
                            "updated_at": row["updated_at"],
                        }
                    )

                return reviews

            return None

    async def update_review(self, review_id: str, update_entry: Dict[str, Any]) -> None:
        data_json = json.dumps(update_entry, default=PostgresDb.datetime_serialize)

        async with self.pool.acquire() as conn:
            query = """
                UPDATE reviews
                SET user_id = $2, book_id = $3, rating = $4, comment = $5, data = $6, updated_at = $7
                WHERE id = $1
            """
            await conn.execute(
                query,
                review_id,
                update_entry["user_id"],
                update_entry["book_id"],
                update_entry["rating"],
                update_entry["comment"],
                data_json,
                update_entry["updated_at"],
            )

    async def delete_review(self, review_id: str) -> None:
        async with self.pool.acquire() as conn:
            query = """
                DELETE FROM reviews
                WHERE id = $1
            """
            await conn.execute(query, review_id)
