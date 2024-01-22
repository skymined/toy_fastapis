from typing import List

from beanie import PydanticObjectId
from databases.connections import Database
from fastapi import APIRouter, HTTPException, status
from models.users import User

router = APIRouter(tags=['Users'])
user_database = Database(User)

@router.post("/")
async def create_client(body:User) -> dict :
    document = await user_database.save(body)
    return {
        "message":"Event created Successfully"
        , "datas" : document
    }

#     conditions = "{ name: { $regex: '이' } }"

@router.get("/{id}/{pswd}", response_model = User)
async def get_client(id:PydanticObjectId, pswd : str) -> User:
    condition = {"_id":id, "pswd":pswd}
    user = await user_database.getsbyconditions(condition)
    if not user :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    return user[0]

# return값 두개 가능한지

@router.delete("/{id}", response_model=User)
async def delete_client(id:PydanticObjectId) -> User:
    user = await user_database.get(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    user = await user_database.delete(id)

    return {
        "message" : "Event deleted successfully."
        , 'datas' : user
    }