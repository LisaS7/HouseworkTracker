from models.Task import Task
from models.User import User
from services.User import create_user
from DB.session import SessionLocal

db = SessionLocal()


def seed():
    user1 = User(name="Michael", email="michael@dundermifflin.com")
    user2 = User(name="Dwight", email="dwight@dundermifflin.com")

    create_user(db, user1)
    create_user(db, user2)
