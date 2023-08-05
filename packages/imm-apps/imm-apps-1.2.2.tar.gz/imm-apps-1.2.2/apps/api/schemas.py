from pydantic import BaseModel, EmailStr
from model.common.user import User


def user_schema(user):
    return {
        "_id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "phone": user["phone"],
        "password": user["password"],
        "role": user.get("role"),
        "permission": user.get("permission"),
    }


def users_schema(users):
    return [user_schema(user) for user in users]


class ShowUser(BaseModel):
    _id: str
    username: str
    email: EmailStr
    phone: str
    password: str
    role: str
    permission: list


class Login(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
