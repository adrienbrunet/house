from apps.users.tests.factories import UserProfileFactory
from .factories import GroupFactory


def test_group_str_method(db):
    group = GroupFactory()
    assert str(group) == group.name


def test_group_get_heads_and_get_members(db):
    group = GroupFactory()
    user1 = UserProfileFactory()
    user2 = UserProfileFactory()
    group.heads.add(user1, user2)
    assert group.get_heads() == f"{user1}, {user2}"

    group.members.add(user1, user2)
    assert group.get_members() == f"{user1}, {user2}"
