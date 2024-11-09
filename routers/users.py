from fastapi import APIRouter, HTTPException, Query
from db import db
from models import User, TemplatePatch

router = APIRouter()

@router.post("/create")
async def create_user(user: User):
    user_ex = await db.get_collection('urban_collection').find_one({'telegram_id': user.telegram_id})
    if user_ex:
        raise HTTPException(status_code=500, detail='User already exists')
    await db.get_collection('urban_collection').insert_one(user.model_dump())
    return {'status': 'ok'}


@router.get("/get")
async def get_user(telegram_id: int = Query(None), token: str = Query(None)):
    if not token and not telegram_id:
        raise HTTPException(status_code=400, detail="Either 't_id' or 'token' must be provided")

    query = {}
    if token:
        query = {'token': token}
    if telegram_id:
        query = {'telegram_id': telegram_id}

    user = await db.get_collection('urban_collection').find_one(query)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = User(**user)
    return user



    
