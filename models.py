from sqlalchemy.orm import relationship
from db import Base, session
from sqlalchemy import Column, Integer, String, Enum as SqlEnum, Table, ForeignKey
from enum import Enum as PythonEnum


class Role(PythonEnum):
    ADMIN_TEACHER = 'Администратор-ученик'
    ADMIN_STUDENT = 'Администратор-студент'
    TEACHER = 'Учитель'
    STUDENT = 'Студент'


class Group_User(Base):
    __tablename__ = 'groups_users'
    group_id = Column(Integer, ForeignKey("groups.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role = Column(SqlEnum(Role))


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(150))

    users = relationship('User', secondary="groups_users", back_populates='groups')
    homeworks = relationship('Homework', back_populates='group')

    def add_role_to_user(self, user: 'User', role: Role):
        relation = Group_User(group_id=self.id, user_id=user.id, role=role)
        session.add(relation)
        session.commit()

    def delete_user(self, user: 'User'):
        session.query(Group_User).filter_by(group_id=self.id, user_id=user.id).delete()

    def user_has_role(self, user: 'User', role: Role):
        return session.query(Group_User).filter_by(group_id=self.id, user_id=user.id, role=role).count() > 0


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    telegram_id = Column(Integer)
    telegram_nickname = Column(String(150))

    groups = relationship('Group', secondary="groups_users", back_populates='users')
    completed_homeworks = relationship('CompletedHomework', back_populates='student')

    inbox = Column(String)

    @staticmethod
    def from_telegram_id(tg_id):
        return session.query(User).filter_by(telegram_id=tg_id).one_or_none()

    @staticmethod
    def from_telegram_nickname(tg_nick):
        return session.query(User).filter_by(telegram_nickname=tg_nick).one_or_none()

    def is_inbox_empty(self) -> bool:
        return self.inbox != '' or self.inbox is not None


class Homework(Base):
    __tablename__ = 'homeworks'
    id = Column(Integer, primary_key=True)
    file_telegram_id = Column(String(150))
    deadline = Column(String(150))

    group_id = Column(Integer, ForeignKey("groups.id"))
    group = relationship('Group', back_populates='homeworks')
    completed_homeworks = relationship('CompletedHomework', back_populates='homework')

    def get_completed_from_student(self, user: User):
        return session.query(CompletedHomework).filter_by(homework=self, student=user).one_or_none()


class CompletedHomework(Base):
    __tablename__ = 'completed_homeworks'
    id = Column(Integer, primary_key=True)
    file_telegram_id = Column(String(150))
    homework_id = Column(Integer, ForeignKey("homeworks.id"))
    homework = relationship('Homework', back_populates='completed_homeworks')

    student_id = Column(Integer, ForeignKey("users.id"))
    student = relationship('User', back_populates='completed_homeworks')

    mark = Column(Integer, nullable=True)
    comment = Column(String, nullable=True)

    def is_checked(self):
        return self.mark is not None

    def has_comment(self):
        return self.comment is not None or self.comment != ''
