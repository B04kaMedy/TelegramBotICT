from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("postgresql://myuser:mypass@localhost/mydb")

factory = sessionmaker(bind=engine)
session = scoped_session(factory)

Base = declarative_base()

import models

Base.metadata.create_all(engine)
