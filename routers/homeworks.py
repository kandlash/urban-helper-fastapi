from fastapi import APIRouter, HTTPException
from db import db
from models import HomeWork, User, HWPatch
from datetime import date


router = APIRouter()

@router.post('/add')
async def add_homework(token: str, date_str: str):
    user = await db.get_collection('urban_collection').find_one({'token': token})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    homeworks = user.get('homeworks', [])

    homework_for_date = next((hw for hw in homeworks if hw['date'] == date_str), None)

    if homework_for_date:
        homework_for_date['count'] += 1
    else:
        new_homework = HomeWork(date=date_str, count=1).model_dump()
        homeworks.append(new_homework)

    await db.get_collection('urban_collection').update_one(
        {'token': token},
        {'$set': {'homeworks': homeworks}}
    )

    return {'status': 'ok'}

@router.get('/get')
async def get_homework(token: str, date_str: str):

    filter_query = {
        'token': token,
        'homeworks.date': date_str
    }

    result = await db.get_collection('urban_collection').find_one(filter_query)
    if not result:
        raise HTTPException(status_code=404, detail='User or homework not found')

    homework_list = result.get('homeworks', [])
    date_homework = next((hw for hw in homework_list if hw['date'] == date_str), None)

    if not date_homework:
        raise HTTPException(status_code=404, detail='Homework for specified date not found')

    return date_homework

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
