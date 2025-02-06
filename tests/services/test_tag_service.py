import pytest

from models.Tag import Tag
from services.Tag import *

# ---------- FIXTURES ----------


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


# ---------- TESTS ----------


def test_get_all_tags(test_tags, db):
    tags = get_all_tags(db)
    assert len(tags) == 2
    assert tags[0].name == "Tag1"


def test_get_tag_by_id(test_tags, db):
    tag = get_tag_by_id(db, 2)
    assert tag.name == "Tag2"


def test_tag_not_found(test_tags, db):
    with pytest.raises(TagNotFoundException):
        get_tag_by_id(db, 46)


def test_get_tag_by_name(test_tags, db):
    tag = get_tag_by_name(db, "Tag2")
    assert tag.id == 2


def test_get_tag_by_name_not_found(test_tags, db):
    tag = get_tag_by_name(db, "Tag22222")
    assert not tag


def test_create_tag(db):
    tag = Tag(name="Tag3")
    created_tag = create_tag(db, tag)
    retrieved_tag = db.query(Tag).filter(Tag.id == 1).first()
    assert retrieved_tag.id == created_tag.id
    assert retrieved_tag.name == created_tag.name


def test_update_tag(test_tags, db):
    update_tag(db, 2, {"name": "Updated Tag"})
    retrieved_tag = db.query(Tag).filter_by(name="Updated Tag").first()
    assert retrieved_tag.name == "Updated Tag"
    assert retrieved_tag.id == 2


def test_delete_tag(test_tags, db):
    delete_tag(db, 2)
    tags = db.query(Tag).all()
    deleted_tag = db.query(Tag).filter(Tag.id == 2).first()
    assert len(tags) == 1
    assert not deleted_tag
