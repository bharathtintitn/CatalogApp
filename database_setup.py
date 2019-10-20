import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Categories(Base):

    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class Items(Base):

    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(500), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship(Categories)

    @property
    def serialize(self):

        return {
                'name': self.name,
                'description': self.description,
                'id': self.id
                }


engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
