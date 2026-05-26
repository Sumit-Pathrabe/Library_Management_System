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