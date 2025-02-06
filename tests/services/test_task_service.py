import pytest

from models.Task import Task
from models.Tag import Tag
from services.schemas import TaskUpdate
from services.Task import *

from datetime import date, timedelta

TODAY = date.today()


@pytest.fixture
def test_tasks(test_users, db):
    """Dummy tasks for testing"""
    user1, user2 = test_users

    tasks = [
        Task(title="Clean oven", last_completed="2025-01-01", user=user1),
        Task(title="Wash dishes", last_completed="2025-01-01", user=user2),
        Task(title="Feed the cat", last_completed="2025-01-01", user=user2),
    ]

    db.add_all(tasks)
    db.commit()

    for task in tasks:
        db.refresh(task)

    return tasks


@pytest.fixture
def test_tags(db):
    """Dummy tags for testing"""
    tag1 = Tag(name="Tag1")
    tag2 = Tag(name="Tag2")
    db.add_all([tag1, tag2])
    db.commit()
    db.refresh(tag1)
    db.refresh(tag2)
    return [tag1, tag2]


def test_get_all_tasks(test_tasks, db):
    tasks = get_all_tasks(db)
    assert len(tasks) == 3
    assert tasks[0].title == "Clean oven"


def test_get_tasks_by_user(test_tasks, db):
    tasks = get_tasks_by_user(db, 2)
    assert len(tasks) == 2
    for task in tasks:
        assert task.user_id == 2


def test_get_task_by_id(test_tasks, db):
    task = get_task_by_id(db, 2)
    assert task.title == "Wash dishes"


def test_task_not_found(test_tasks, db):
    with pytest.raises(TaskNotFoundException, match="Task not found for id 23"):
        task = get_task_by_id(db, 23)


def test_create_task(test_users, db):
    user = test_users[0]
    task = Task(title="Buy cheese", last_completed="2025-01-30", user_id=user.id)
    created_task = create_task(db, task)
    retrieved_task = db.query(Task).filter_by(title="Buy cheese").first()
    assert retrieved_task.title == created_task.title
    assert retrieved_task.last_completed == created_task.last_completed
    assert retrieved_task.user_id == created_task.user_id


def test_update_task(test_tasks, db):
    data = TaskUpdate(title="Laundry")
    update_task(db, 1, data)
    retrieved_task = db.query(Task).filter(Task.id == 1).first()
    assert retrieved_task.title == "Laundry"


def test_delete_task(test_tasks, db):
    delete_task(db, 2)
    tasks = db.query(Task).all()
    deleted_task = db.query(Task).filter(Task.id == 2).first()
    assert len(tasks) == 2
    assert not deleted_task


# --------------- TAGS ---------------


def test_add_tags_to_task(test_tasks, test_tags, db):
    add_tags_to_task(db, test_tasks[0], test_tags)
    retrieved_task = db.query(Task).filter(Task.id == 1).first()
    assert retrieved_task.tags == test_tags


def test_get_tags_by_task(test_tasks, db):
    tags = [Tag(name="Tag1"), Tag(name="Tag2")]
    test_tasks[0].tags = tags
    retrieved_tags = get_tags_by_task(db, 1)
    assert retrieved_tags == tags


def test_get_tasks_by_tag(test_tasks, test_tags, db):
    test_tasks[0].tags = test_tags
    test_tasks[1].tags = test_tags
    db.commit()
    retrieved_tasks = get_tasks_by_tag(db, test_tags[0])
    assert retrieved_tasks == [test_tasks[0], test_tasks[1]]


def test_get_no_tags(test_tasks, db):
    tags = get_tags_by_task(db, 1)
    assert tags == None


def test_remove_tag_from_task(test_tasks, test_tags, db):
    task = test_tasks[0]
    tag_to_remove = test_tags[0]
    task.tags = test_tags

    updated_task = remove_tag_from_task(db, 1, tag_to_remove)
    retrieved_task = db.query(Task).filter(Task.id == 1).first()

    assert updated_task == retrieved_task
    assert len(retrieved_task.tags) == 1
    assert tag_to_remove not in retrieved_task.tags


# --------------- DATE ---------------


def test_get_overdue_tasks(test_tasks, db):
    test_tasks[0].repeat_interval = 1
    test_tasks[1].repeat_interval = 1
    test_tasks[2].repeat_interval = 1000  # make this one not included
    db.commit()
    tasks = get_all_overdue_tasks(db)

    assert len(tasks) == 2
    for task in tasks:
        assert task.next_due < date.today()


def test_set_next_due(test_tasks, db):
    task = test_tasks[0]
    task.last_completed = TODAY - timedelta(days=5)
    task.repeat_interval = 5
    db.commit()
    db.refresh(task)
    tasks = get_todays_tasks(db)
    assert len(tasks) == 1
    assert tasks[0].next_due == TODAY
