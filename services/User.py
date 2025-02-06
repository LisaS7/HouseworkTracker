from sqlalchemy.orm import Session
from models.User import User
from typing import List
from services.schemas import UserCreate, UserUpdate, UserModel
from config import logger


class UserNotFoundException(Exception):
    def __init__(self, id: int):
        self.message = f"User not found for id {id}"
        self.status_code = 404
        logger.error(f"UserNotFoundException: {self.message}")
        super().__init__(self.message)


def get_all_users(db: Session) -> List[UserModel]:
    return db.query(User).all()


def get_user_by_id(db: Session, id: int) -> UserModel:
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise UserNotFoundException(id)
    return user


def create_user(db: Session, user: UserCreate) -> UserModel:
    db_user = User(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"Created {db_user}")
    return db_user


def update_user(db: Session, id: int, user: UserUpdate) -> UserModel:
    existing_user = get_user_by_id(db, id)
    logger.info(f"Updating old User: {existing_user}")

    for key, value in user.items():
        setattr(existing_user, key, value)

    db.commit()
    db.refresh(existing_user)
    logger.info(f"Updated to new User: {existing_user}")

    return existing_user


def delete_user(db: Session, id: int):
    existing_user = get_user_by_id(db, id)
    logger.info(f"Deleting {existing_user}")
    db.delete(existing_user)
    db.commit()
