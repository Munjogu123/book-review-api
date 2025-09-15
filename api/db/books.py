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

    async def create_book(self, book_data: Dict[str, Any]) -> Dict[str, Any]:
        book_id = book_data["id"] or str(uuid4())
        data_json = json.dumps(book_data, default=PostgresDb.datetime_serialize)

        async with self.pool.acquire() as conn:
            query = """
                INSERT INTO books(id, title, author, isbn, data, created_at)
                VALUES ($1, $2, $3, $4, $5, $6)
                RETURNING *
            """
            row = await conn.fetchrow(
                query,
                book_id,
                book_data["title"],
                book_data["author"],
                book_data["isbn"],
                data_json,
                book_data["created_at"],
            )
            if row:
                return {
                    "id": row["id"],
                    "title": row["title"],
                    "author": row["author"],
                    "isbn": row["isbn"],
                    "created_at": row["created_at"],
                }

            return {}

    async def get_book(self, book_id: str) -> Dict[str, Any]:
        async with self.pool.acquire() as conn:
            query = """
                SELECT * FROM books WHERE id = $1
            """
            row = await conn.fetchrow(query, book_id)
            if row:
                return {
                    "id": row["id"],
                    "title": row["title"],
                    "author": row["author"],
                    "isbn": row["isbn"],
                    "created_at": row["created_at"],
                }

            return None

    async def get_books(self) -> List[Dict[str, Any]]:
        async with self.pool.acquire() as conn:
            query = """
                SELECT * FROM books
            """
            rows = await conn.fetch(query)
            users = []
            for row in rows:
                users.append(
                    {
                        "id": row["id"],
                        "title": row["title"],
                        "author": row["author"],
                        "isbn": row["isbn"],
                        "created_at": row["created_at"],
                    }
                )

            return users

    async def update_book(self, book_id: str, update_entry: Dict[str, Any]) -> None:
        data_json = json.dumps(update_entry, default=PostgresDb.datetime_serialize)

        async with self.pool.acquire() as conn:
            query = """
                UPDATE books
                SET title = $2, author = $3, isbn = $4, data = $5
                WHERE id = $1
            """
            await conn.execute(
                query,
                book_id,
                update_entry["title"],
                update_entry["author"],
                update_entry["isbn"],
                data_json,
            )

    async def delete_book(self, book_id: str) -> None:
        async with self.pool.acquire() as conn:
            query = """
                DELETE FROM books
                WHERE id = $1
            """
            await conn.execute(query, book_id)

    async def delete_books(self) -> None:
        async with self.pool.acquire() as conn:
            query = """
                DELETE FROM books
            """
            await conn.execute(query)
