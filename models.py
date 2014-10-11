#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""models.py: contains model definitions"""

__author__ = "Daniel O'Connell"
__copyright__ = "BSD-3"

from sqlalchemy import Integer, String, DateTime, Text, Float
from sqlalchemy import Column, Sequence, ForeignKey
from sqlalchemy.schema import Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(100))
    fullname = Column(String(100))
    password = Column(String(255))
    creationDate = Column(DateTime(timezone=True))
    updateDate = Column("updateDate", DateTime, onupdate=datetime.datetime.now)
    recipies = relationship("Recipe", backref="user",
                            cascade="all, delete, delete-orphan")

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" %\
                (self.name, self.fullname, self.password)


class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, Sequence('image_id_seq'), primary_key=True)
    path = Column(String(1024))
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    creationDate = Column(DateTime(timezone=True))
    updateDate = Column("updateDate", DateTime,onupdate=datetime.datetime.now)

    def __repr__(self):
        return "<Image(path='%s'>" % (self.path)

    def to_dict(self):
        result = {'id': self.id,
                'path': self.path,
                'recipe_id': self.recipe_id}
        if self.updateDate:
            result['updateDate'] = self.updateDate
        if self.creationDate:
            result['creationDate'] = self.creationDate
        return result

class Unit(Base):
    __tablename__ = 'units'

    id = Column(Integer, Sequence('unit_id_seq'), primary_key=True)
    name = Column(String(200))
    ingredients = relationship("Ingredient", backref="unit")

    siUnit_id = Column(Integer, ForeignKey('units.id'))
    siUnit = relationship('Unit', remote_side=[id], backref="children")
    conversion = Column(Float)
    updateDate = Column(DateTime,onupdate=datetime.datetime.now)

    def __repr__(self):
        return "<Unit(name='%s', siunitId='%s'>" % (self.name, self.siUnit_id)

    def to_dict(self):
        result = {'id':self.id,
                'name':self.name,
                'conversion': self.conversion}
        if self.updateDate:
            result['updateDate'] = self.updateDate
        if self.siUnit_id:
            result['siUnit_id'] = self.siUnit_id
        return result

class Substance(Base):
    __tablename__ = 'substances'

    id = Column(Integer, Sequence('substance_id_seq'), primary_key=True)
    name = Column(String(200))
    ingredients = relationship("Ingredient", backref="substance")
    description = Column(Text)
    updateDate = Column(DateTime, onupdate=datetime.datetime.now)

    def __repr__(self):
        return "<Substance(name='%s', description='%s'>" % (self.name,
                                                            self.description)
    def to_dict(self):
        result = {'id':self.id,
                'name':self.name,
                'description': self.description}
        if self.updateDate:
            result['updateDate'] = self.updateDate
        return result


class Ingredient(Base):
    __tablename__ = "ingredients"

    recipe_id = Column(Integer, ForeignKey('recipes.id'), primary_key=True)
    substance_id = Column(Integer, ForeignKey('substances.id'), primary_key=True)
    amount = Column(Float)
    unit_id = Column(Integer, ForeignKey('units.id'))
    creationDate = Column(DateTime(timezone=True))
    updateDate = Column("updateDate", DateTime,onupdate=datetime.datetime.now)

    def standardise_amount(self):
        result = str(self.amount)
        if self.unit:
            if len(self.unit.name) > 2:
                result += " "
            result += self.unit.name
        return result

    def __repr__(self):
        return "<Ingredients<amount='%s', unit='%s', recipe='%s', substance='%s'>" % \
                (self.amount, self.unit_d, self.recipe_id, self.substance_id)

    def __unicode__(self):
        return u"%s: %s" % (self.substance.name, self.standardise_amount())

    def to_dict(self):
        result = {'recipe_id':self.recipe_id,
                'substance_id':self.substance_id,
                'amount': self.amount}
        if self.unit_id:
            result['unit_id'] = self.unit_id
        if self.creationDate:
            result['creationDate'] = self.creationDate
        if self.updateDate:
            result['updateDate'] = self.updateDate
        return result

association_table = Table('association', Base.metadata,
                          Column('group_id',
                                 Integer,
                                 ForeignKey('recipes.id')),
                          Column('recipe_id',
                                 Integer,
                                 ForeignKey('groups.id')))

class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, Sequence('group_id_seq'), primary_key=True)
    name = Column(String(200))
    description = Column(Text)
    recipes = relationship("Recipe", secondary=association_table, backref="groups")

    parent_id = Column(Integer, ForeignKey('groups.id'))
    parent = relationship('Group', remote_side=[id], backref="children")
    updateDate = Column("updateDate", DateTime,onupdate=datetime.datetime.now)

    def __getitem__(self, item):
        if item == "name":
            return self.name
        elif item == "description":
            return self.description
        elif item == "recipies":
            return self.recipies
        elif item == "parent":
            return self.parent
        elif item == "children":
            return self.children

    def __repr__(self):
        return u"<Group(name='%s', parent='%s'>" % (self.name, self.parent_id)

    def __unicode__(self):
        return u"<Group(name='%s', parent='%s'>" % (self.name, self.parent_id)

    def __str__(self):
            return unicode(self).encode('utf-8')

    def to_dict(self):
        result = {'id':self.id,
                'name':self.name,
                'description':self.description}
        if self.parent_id:
            result['parent_id'] = self.parent_id
        if self.updateDate:
            result['updateDate'] = self.updateDate
        return result


class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, Sequence('recipies_id_seq'), primary_key=True)
    title = Column(String(500))
    description = Column(Text)
    algorythm = Column(Text)
    pics = relationship("Image", backref="recipie",
                        cascade="all, delete, delete-orphan")
    ingredients = relationship("Ingredient", backref="recipe",
                               cascade="all, delete, delete-orphan")
    time = Column(Integer)
    difficulty = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    creationDate = Column(DateTime(timezone=True))
    updateDate = Column("updateDate", DateTime,
                        onupdate=datetime.datetime.now)

    def __repr__(self):
        return "<Recipe(title='%s', description='%s', algorythm='%s')>" % \
            (self.title, self.description, self.algorythm)

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u"<Recipe(title='%s', description='%s', algorythm='%s')>" % \
            (self.title, self.description, self.algorythm)

    def to_dict(self):
        result = {'id': self.id,
               'title': self.title,
               'description': self.description,
               'algorythm': self.algorythm}
        if self.difficulty:
            result['difficulty'] = self.difficulty
        if self.time:
            result['time'] = self.time
        if self.user_id:
            result['user_id'] = self.user_id
        if self.creationDate:
            result['creationDate'] = self.creationDate
        if self.updateDate:
            result['updateDate'] = self.updateDate
        if self.groups:
            result['groups'] = str([group.id for group in self.groups])
        return result

def createDB(engine):
    Base.metadata.create_all(engine)
