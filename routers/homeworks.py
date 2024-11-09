from fastapi import APIRouter, HTTPException
from db import db
from models import HomeWork, User, HWPatch
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

@router.get('/get')
async def get_homework(token: str):
    filter_query = {
        'token': token,
        'homeworks.date': date.today().isoformat()
    }

    result = await db.get_collection('urban_collection').find_one(filter_query)
    if not result:
        raise HTTPException(status_code=404, detail='User or homework not found')
    
    homework_list = result.get('homeworks', [])
    today_homework = [hw for hw in homework_list if hw['date'] == date.today().isoformat()]
    return today_homework[0]

@router.patch('/patch')
async def update_homework(patch: HWPatch):
    filter_query = {
        'token': patch.token,
        'homeworks.date': patch.date
    }

    update_query = {
        '$set':
        {
            'homeworks.$.count': patch.count
        }
    }

    result = await db.get_collection('urban_collection').update_one(filter_query, update_query)

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail='User or homework with specified data not found')
    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail='Failed to update homework')
    
    return {"status": "ok", "message": "Homework updated successfully"}
