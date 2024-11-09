from fastapi import APIRouter, HTTPException
from db import db
from models import User

router = APIRouter()

@router.get("/get_user")
async def get_user(t_id: int):
    user = await db.get_collection('urban_collection').find_one({'telegram_id': t_id})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = User(**user)
    return user

@router.post("/create")
async def create_user(user: User):
    user_ex = await db.get_collection('urban_collection').find_one({'telegram_id': user.telegram_id})
    if user_ex:
        return {'status': 'exists', 'message': 'User already exists'}
    
    await db.get_collection('urban_collection').insert_one(user.model_dump())
    return {'status': 'ok'}

