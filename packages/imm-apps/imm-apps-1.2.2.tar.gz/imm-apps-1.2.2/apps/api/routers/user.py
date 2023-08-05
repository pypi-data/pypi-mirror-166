from model.common.user import User
from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId
from apps.config import Default, db
from typing import List
import schemas
from apps.api.hashing import Hash
from apps.api import oauth2
from pprint import pprint
from apps.api import schemas

user_collection = db.user

router = APIRouter(
    prefix="/user", tags=["Users"], responses={404: {"description": "Nof found"}}
)


def email_existed(email: str):
    return user_collection.find_one({"email": email})


@router.get("/")
async def read_users(current_user: User = Depends(oauth2.get_current_user)):
    users = list(user_collection.find())
    users1 = schemas.users_schema(users)
    return {"status_code": status.HTTP_200_OK, "data": users1}


@router.get("/{id}")
async def retrieve(id: str, current_user: User = Depends(oauth2.get_current_user)):
    user = user_collection.find_one({"_id": ObjectId(id)})
    return {"status_code": status.HTTP_200_OK, "data": schemas.user_schema(user)}


@router.post("/")
async def create(user: User):
    if email_existed(user.email):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"{user.email} is existed in the system.",
        )
    user.password = Hash.hash(user.password)
    user.permission.extend(Default.user_permission)
    new_id = user_collection.insert_one(user.dict()).inserted_id
    new_user = user_collection.find_one({"_id": new_id})
    return {"status_code": status.HTTP_200_OK, "data": schemas.user_schema(new_user)}


@router.put("/{id}")
async def update(
    id: str, user: User, current_user: User = Depends(oauth2.get_current_user)
):
    user_collection.update_one({"_id": ObjectId(id)}, {"$set": user.dict()})
    updated_one = user_collection.find_one({"_id": ObjectId(id)})
    return {"status_code": status.HTTP_200_OK, "data": schemas.user_schema(updated_one)}


@router.delete("/{id}")
async def delete(id: str, current_user: User = Depends(oauth2.get_current_user)):
    print(current_user)
    if current_user.get("role") != "admin":
        return {
            "status_code": status.HTTP_401_UNAUTHORIZED,
            "detail": "Only admin can delete records",
        }
    try:
        res = user_collection.delete_one({"_id": ObjectId(id)})
        if res.deleted_count > 0:
            return {"status_code": status.HTTP_204_NO_CONTENT, "data": []}
        return {
            "status_code": status.HTTP_404_NOT_FOUND,
            "detail": "Delete unseccessfully.",
        }
    except Exception as e:
        return {
            "status_code": status.HTTP_404_NOT_FOUND,
            "detail": "Delete unseccessfully.",
        }
