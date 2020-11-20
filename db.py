from typing import List

from Group import Group
from Role import Role
from User import User
from functions import log

users = dict()
groups = dict()


def has_user(tele_id: int) -> bool:
    return users.__contains__(tele_id)


def create_user(id: int, name: str, tele_id: int, *gr: (Group, List[Role])) -> bool:
    user = User(id, name, tele_id, gr)

    if users.__contains__(tele_id):
        log('There are already existing user with a such telegram-id. '
            'You can not create new user with this telegram-id! '
            'Or you should remove previous user and create new.')
        return False
    else:
        users.update({tele_id: user})
        return True


def update_user(tele_id: int, new_user: User) -> bool:
    if users.__contains__(tele_id):
        users.update({tele_id: new_user})
        return True
    else:
        log('There are no user with a such telegram-id. '
            'You can not update user while it is not existing! '
            'Please, create a user with this telegram-id.')


def remove_user(tele_id: int):
    if users.__contains__(tele_id):
        users.pop(tele_id)
        return True
    else:
        log('There are no user with a such telegram-id. '
            'You can not remove it!')


def get_user(tele_id: int) -> User:
    return users.get(tele_id)
