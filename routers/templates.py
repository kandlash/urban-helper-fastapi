from fastapi import APIRouter, HTTPException
from db import db
from models import TemplatePatch

router = APIRouter()

@router.get("/get")
async def get_template(token: str):

    query = {"token": token}
    user = await db.get_collection('urban_collection').find_one(query)

    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    
    template = user.get('template', 'Здравствуйте! Все хорошо, зачет!')
    return {"template": template}

@router.patch("/set")
async def set_template(patch: TemplatePatch):
    query = {"token": patch.token}
    user = await db.get_collection('urban_collection').find_one(query)

    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    
    result = await db.get_collection('urban_collection').update_one(
        {'token': patch.token},
        {'$set': {'template': patch.new_template}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail='Failed to update')
    
    return {"status": "ok", "message": "Template updated successfully"}