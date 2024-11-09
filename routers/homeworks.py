from fastapi import APIRouter, HTTPException
from db import db
from models import HomeWork, User
from datetime import date


router = APIRouter()

@router.post('/add')
async def add_homework(token: str):

    user = await db.get_collection('urban_collection').find_one({'token': token})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    homeworks = user.get('homeworks', [])
    current_date = date.today().isoformat()

    homework_today = next((hw for hw in homeworks if hw['date'] == current_date), None)

    if homework_today:
        homework_today['count'] += 1
    else:
        new_homework = HomeWork(date=current_date, count=1).model_dump()
        homeworks.append(new_homework)

    await db.get_collection('urban_collection').update_one(
        {'token': token},
        {'$set': {'homeworks': homeworks}}
    )
    
    return {'status': 'ok'}

@router.post('/update')
async def update_homework(token: str, date: str, count: int):
    user = User(**await db.get_collection('urban_collection').find_one({'token': token}))
    if not user:
        raise HTTPException(404, 'User not found')
    
    homework = next((hw for hw in user.homeworks if hw.date == date), None)
    if homework:
        pass
    
    
