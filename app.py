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
# View All Books
@app.get("/books")
def get_books():

    cursor.execute("SELECT * FROM books;")

    books = cursor.fetchall()

    return books

# View Single Book by ID
@app.get("/books/{book_id}")
def get_book(book_id: int):

    cursor.execute(
        "SELECT * FROM books WHERE id = %s;",
        (book_id,)
    )

    book = cursor.fetchone()

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return book

# Update Book
@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book: Book):

    cursor.execute(
        """
        UPDATE books
        SET title = %s,
            author = %s,
            pages = %s
        WHERE id = %s
        RETURNING *;
        """,
        (
            updated_book.title,
            updated_book.author,
            updated_book.pages,
            book_id
        )
    )

    book = cursor.fetchone()

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    conn.commit()

    return {
        "message": "Book updated successfully",
        "book": book
    }



