from typing import List

from Group import Group
from Role import Role
from User import User
from functions import *

users = dict()
groups = dict()


def create_db():
    create_user(0, 'test-user', 0, (Group(0, 'test-group'), Role.WORKER))


# Users ##################################################
def has_user(tele_id: int) -> bool:
    return users.__contains__(tele_id)


def create_user(user_id: int, name: str, tele_id: int, gr: dict[Group: List[Role]]) -> bool:
    user = User(user_id, name, tele_id, gr)

    if not users.__contains__(tele_id):
        users.update({tele_id: user})
        return True
    else:
        log('There are already existing user with a such telegram-id. '
            'You can not create new user with this telegram-id! '
            'Or you should remove previous user and create new.')
        return False


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
        if get_answer():
            users.pop(tele_id)
            return True
        else:
            return False
    else:
        log('There are no user with a such telegram-id. '
            'You can not remove it!')


def get_user(pointer) -> User:
    if pointer is int:
        if users.__contains__(pointer):
            return users.get(pointer)
        else:
            log('There are no user with a such telegram-id!')
    elif pointer is str:
        for _, user in users:
            if user.name == pointer:
                return user

        log('There are no user with a such telegram-id!')
    else:
        log('Please, give me concrete pointer!')


# Groups ##################################################
def create_group(group_id: int, name: str) -> bool:
    group = Group(group_id, name)

    if not groups.__contains__(group_id):
        groups.update({group_id: group})
        return True
    else:
        log('There are already exists a group with a such id. '
            'You can not create another one!')
        return False


def get_group(pointer) -> Group:
    if pointer is int:
        if groups.__contains__(pointer):
            return groups.get(pointer)
        else:
            log('There are no group with a such id!')
    elif pointer is str:
        for _, group in groups:
            if group.name == pointer:
                return group

        log('There are no group with a such id!')
    else:
        log('Please, give me concrete pointer!')


def remove_group(group_id: int) -> bool:
    if groups.__contains__(group_id):
        if get_answer():
            groups.pop(group_id)
            return True
        else:
            return False
    else:
        log('There are already exists a group with a such id. '
            'You can not create another one!')
        return False


# Others ##################################################
class unchecked:

    def __init__(self, function):
        log('This method \'' + str(function) + '\' is unchecked!')


@unchecked
def add_user_to_group(user_tele_id: int, group_id: str, *roles: Role) -> bool:
    user = get_user(user_tele_id)
    group = get_group(group_id)

    gr, rs = zip(*user.group_list)
    if not gr.__contains__(group_id):
        user.add_to_group(group, *roles)
        return True
    else:
        log('There are already exists a group with a such id. '
            'You can not create another one!')
        return False


@unchecked
def remove_user_from_group(user_pointer, group_pointer) -> bool:
    user = get_user(user_pointer)
    group = get_group(group_pointer)

    gr, rs = zip(*user.group_list)
    if not gr.__contains__(group):
        user.remove_from_group(group)
        return True
    else:
        log('This user are not a member of this group. '
            'You can not remove him from it!')
        return False


@unchecked
def add_role_in_group_to_user(user_pointer, group_pointer, role: Role) -> bool:
    user = get_user(user_pointer)
    group = get_group(group_pointer)

    if user.group_list.__contains__(group):
        user[user.group_list.index(group)]
        return True
