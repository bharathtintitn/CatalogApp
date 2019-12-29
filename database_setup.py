import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String(100), nullable=False)
    picture = Column(String(1000))
    name = Column(String(100), nullable=False)


class Categories(Base):

    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):

        return {
                'name': self.name,
                'id': self.id
            }


class Items(Base):

    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(500), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship(Categories)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):

        return {
                'name': self.name,
                'description': self.description,
                'id': self.id
                }

engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
