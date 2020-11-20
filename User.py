from typing import List

from Group import Group
from Role import Role


class User:

    def __init__(self,
                 id: int,
                 name: str,
                 tele_id: int,
                 group_list: List[(Group, List[Role])]):
        self.id = id
        self.name = name
        self.tele_id = tele_id
        self.group_list = group_list
