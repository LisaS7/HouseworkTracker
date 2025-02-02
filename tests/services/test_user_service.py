import pytest

from models.User import User
from services.User import *


def test_get_all_users(test_users, db):
    users = get_all_users(db)
    assert len(users) == 2
    assert users[0].name == "Michael"
    assert users[1].name == "Dwight"


def test_get_user_by_id(test_users, db):
    user = get_user_by_id(db, 1)
    assert user.name == "Michael"


def test_user_id_invalid(test_users, db):
    with pytest.raises(UserNotFoundException, match="User not found for id 5"):
        get_user_by_id(db, 5)


def test_create_user(db):
    user = User(name="Pam", email="pam@dundermifflin.com")
    created_user = create_user(db, user)
    retrieved_user = db.query(User).filter_by(name="Pam").first()
    assert retrieved_user == created_user


def test_update_user(test_users, db):
    update_user(db, 1, {"name": "Creed"})
    retrieved_user = db.query(User).filter(User.id == 1).first()
    assert retrieved_user.name == "Creed"
    assert retrieved_user.email == "michael@dundermifflin.com"


def test_delete_user(test_users, db):
    delete_user(db, 1)
    users = db.query(User).all()
    assert len(users) == 1
    assert users[0].name == "Dwight"
