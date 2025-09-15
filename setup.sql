-- Creating users table
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR PRIMARY KEY,
    username VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    data JSONB NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- Creates indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_user_id ON users(id);
CREATE INDEX IF NOT EXISTS idx_user_data ON users USING GIN (data);


-- Creating a book table
CREATE TABLE IF NOT EXISTS books (
    id VARCHAR PRIMARY KEY,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    isbn VARCHAR,
    data JSONB NOT NULL,
    created_at TIMESTAMP NOT NULL,
);

CREATE INDEX IF NOT EXISTS idx_book_id ON books(id);
CREATE INDEX IF NOT EXISTS idx_book_data ON books USING GIN (data);


-- Creating the reviews table
CREATE TABLE IF NOT EXISTS reviews (
    id VARCHAR PRIMARY KEY,
    user_id VARCHAR NOT NULL,
    book_id VARCHAR NOT NULL,
    rating DECIMAL(2, 1),
    comment VARCHAR,
    data JSONB NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (book_id) REFERENCES books (id)
);

CREATE INDEX IF NOT EXISTS idx_book_id ON reviews(id);
CREATE INDEX IF NOT EXISTS idx_book_data ON reviews USING GIN (data);
