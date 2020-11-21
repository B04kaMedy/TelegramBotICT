from sqlalchemy.orm import relationship
from db import Base, session
from sqlalchemy import Column, Integer, String, Enum as SqlEnum, Table, ForeignKey
from enum import Enum as PythonEnum

class Role(PythonEnum):
    ADMIN = 'admin'
    ELDER = 'elder'
    TEACHER = 'teacher'
    MENTOR = 'mentor'
    STUDENT = 'student'

class Group_User(Base):
    __tablename__ = 'groups_users'
    group_id = Column(Integer, ForeignKey("groups.id"), primary_key = True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key = True)
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
    
    def user_has_role(self, user: 'User', role: Role):
        return session.query(Group_User).filter_by(group_id=self.id, user_id=user.id, role=role).count() > 0

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    telegram_id = Column(String)

    groups = relationship('Group', secondary="groups_users", back_populates='users')
    completed_homeworks = relationship('CompletedHomework', back_populates='student')

    @staticmethod
    def from_telegram_id(tg_id):
        return session.query(User).filter_by(telegram_id=tg_id).one_or_none()

class Homework(Base):
    __tablename__ = 'homeworks'
    id = Column(Integer, primary_key=True)
    file_telegram_id = Column(String(150))
    deadline = Column(String(150))

    group_id = Column(Integer, ForeignKey("groups.id"))
    group = relationship('Group', back_populates='homeworks')

class CompletedHomework(Base):
    __tablename__ = 'completed_homeworks'
    id = Column(Integer, primary_key=True)
    file_telegram_id = Column(String(150))

    student_id = Column(Integer, ForeignKey("users.id"))
    student = relationship('User', back_populates='completed_homeworks')