from typing import List

from Group import Group
from Role import Role


class User:

    def __init__(self,
                 id: int,
                 name: str,
                 tele_id: int,
                 group_list: dict[Group: List[Role]]):
        self.id = id
        self.name = name
        self.tele_id = tele_id
        self.group_list = group_list

    def add_to_group(self, group: Group, roles: List[Role]):
        new_user_group = {group: roles}
        self.group_list.append(new_user_group)

    def remove_from_group(self, group: Group):
        self.group_list.remove(group)
