from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from models.User import User
from typing import List


class UserNotFoundException(Exception):
    def __init__(self, id: int):
        self.message = f"User not found for id {id}"
        self.status_code = 404
        super().__init__(self.message)


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


def get_user_by_id(db: Session, id: int) -> User:
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise UserNotFoundException(id)
    return user


def create_user(db: Session, user: UserCreate) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, id: int, user: UserUpdate) -> User:
    existing_user = get_user_by_id(db, id)

    for key, value in user.items():
        setattr(existing_user, key, value)

    db.commit()
    db.refresh(existing_user)

    return existing_user


def delete_user(db: Session, id: int):
    existing_user = get_user_by_id(db, id)
