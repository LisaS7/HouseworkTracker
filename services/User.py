from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from models.User import User
from typing import List


class UserModel(BaseModel):
    id: int
    name: str
    email: EmailStr
    active: bool


class UserCreate(BaseModel):
    name: str
    email: EmailStr


class UserUpdate(BaseModel):
    name: str | None
    email: EmailStr | None
    active: bool | None


def get_all_users(db: Session) -> List[User]:
    return db.query(User).all()


def get_user_by_id():
    pass


def create_user(db: Session, user: UserCreate) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user():
    pass


def delete_user():
    pass
