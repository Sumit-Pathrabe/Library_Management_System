from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2 as psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()
# PostgreSQL Connection
conn = psycopg2.connect(
    host="localhost",
    database="library_db",
    user="postgres",
    password="YOUR_PASSWORD",
    cursor_factory=RealDictCursor
)
cursor = conn.cursor()

# Pydantic Model
class Book(BaseModel):
    title: str
    author: str
    pages: int

# Home Route
@app.get("/")
def home():
    return {"message": "Library Management System API"}

# Add New Book
@app.post("/books")
def add_book(book: Book):

    query = """
    INSERT INTO books (title, author, pages)
    VALUES (%s, %s, %s)
    RETURNING *;
    """

    cursor.execute(
        query,
        (book.title, book.author, book.pages)
    )

    new_book = cursor.fetchone()

    conn.commit()

    return {
        "message": "Book added successfully",
        "book": new_book
    }