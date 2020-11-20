from Group import Group
from Role import Role


class User:

    def __init__(self,
                 id: int,
                 name: str,
                 tele_id: str,
                 *group_list: (Group, *Role)):
        self.id = id
        self.name = name
        self.tele_id = tele_id
        self.group_list = group_list
