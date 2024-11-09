from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager
from fastapi import HTTPException

from db import db
from routers import homeworks, users

from models import User, HomeWork
from datetime import date


app = FastAPI()
app.include_router(users.router, prefix='/user', tags=["user"])
app.include_router(homeworks.router, prefix='/homework', tags=['homeworks'])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)