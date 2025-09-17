# 📚 Book Review API

The Book Review API is an asynchronous RESTful API built with FastAPI and PostgreSQL. It lets you manage users, books, and reviews in a clean and scalable way.

## 🚀 Features

- User management (create, fetch, update, delete users).
- Book management (add, fetch, update, delete books).
- Review management tied directly to books (add, list, update, delete reviews).
- Fully async using asyncpg for performance.

## 🗂 Project Structure

```markdown

book-review-api/  
├── api/              # Routers & services  
├── setup.sql         # Database schema setup  
├── requirements.txt  # Dependencies  
├── docker-compose.yml  
├── Dockerfile  
└── .env.sample  
```

## ⚙️ Installation & Running Locally

### 1️⃣ Clone the repository

```sh
git clone https://github.com/Munjogu123/book-review-api.git
cd book-review-api
```

### 2️⃣ Setup environment variables

```sh
cp .env.sample .env
```

### 3️⃣ Run with Docker

```docker
docker-compose up --build
```

This spins up FastAPI + PostgreSQL.

Visit the docs at <http://localhost:8000/docs>.

### 4️⃣ Manual (without Docker)

- Create a virtual environment:

```bash
python -m venv .venv
```

- Activate the virtual environment:

```bash
source .venv/bin/activate
```

- Install dependencies:

```bash
pip install -r requirements.txt
```

- Start PotsgreSQL locally and run `setup.sql`.

- Run FastAPI:

```bash
uvicorn api.main:app --reload
```

## 🧪 Testing

With the server running, you can test using curl or visit the Swagger UI at <http://localhost:8000/docs>

## 🛣 Routers & Endpoints

### Users

| Method | Endpoint           | Description             |
|--------|--------------------|-------------------------|
| POST   | `/users/`           | Create a new user       |
| GET    | `/users/{user_id}`  | Get a single user by ID |
| GET    | `/users`            | Get all users           |
| PATCH  | `/users/{user_id}`  | Update a user (partial) |
| DELETE | `/users/{user_id}`  | Delete a single user    |
| DELETE | `/users`            | Delete all users        |

### Books

| Method | Endpoint           | Description             |
|--------|--------------------|-------------------------|
| POST   | `/books/`           | Create a new bookbooks       |
| GET    | `/books/{book_id}`  | Get a single bookbooks by ID |
| GET    | `/books`            | Get all books           |
| PATCH  | `/books/{book_id}`  | Update a bookbooks (partial) |
| DELETE | `/books/{book_id}`  | Delete a single bookbooks    |
| DELETE | `/books`            | Delete all books        |

### Reviews

| Method | Endpoint                      | Description                                 |
|--------|-------------------------------|---------------------------------------------|
| POST   | `/books/{book_id}/reviews`     | Create a new review for a specific book     |
| GET    | `/books/{book_id}/reviews`     | Get all reviews for a specific book         |
| PATCH  | `/reviews/{review_id}`         | Update an existing review (partial update)  |
| DELETE | `/reviews/{review_id}`         | Delete a specific review by its ID          |

## 📝 Notes

- Replace `user_id`, `book_id`, and `review_id` with actual IDs returned from POST requests.
- All endpoints return JSON responses.
- Use the built-in FastAPI docs for interactive testing at /docs.
