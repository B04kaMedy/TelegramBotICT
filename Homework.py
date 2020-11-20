from datetime import datetime
from typing import Optional

from functions import *


class Homework:

    def __init__(self,
                 task: str,
                 deadline: datetime,
                 complete: bool,
                 checked: bool,
                 mark: Optional[int]):
        self.task = task
        self.deadline = deadline
        self.complete = complete
        self.checked = checked
        self.mark = mark

    def set_checked(self, mark):
        if self.checked:
            out('Are you sure, that you want to change the mark?')
            if get_answer():
                self.checked = False
                self.set_checked(mark)
        else:
            self.checked = True
            self.mark = mark

    def submit(self):
        if self.complete:
            out('Are you sure? Your last submission will be deleted!')
            if get_answer():
                self.complete = False

                self.submit()
        else:
            today = datetime.today()

            if today.timestamp() <= self.deadline.timestamp():
                self.complete = True

                if bot.push(self):
                    out('Ok, your submission completed successfully!')
                else:
                    out('Something went wrong(((')
            else:
                out('You can not submit, because this task is over: deadline ended...')
