#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Database.py: handles basic database operations + defines the database tables"""

__author__      = "Daniel O'Connell"
__copyright__   = "BSD-3"

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from models import User, Unit, Image, Substance, Ingredient, Group, Recipe
import models

class DBConfig:
    def __init__(self, database, debug=True):
        self.engine = create_engine(database, echo=False)
        self.sessionFactory = sessionmaker(bind=self.engine)

    def createDB(self):
        models.createDB(self.engine) 

    def getSession(self):
        return self.sessionFactory()

    def addObject(self, obj):
        session = self.getSession()
        result = "ok"
        try:
            result = session.add(obj)

            session.commit()
        except Exception, e:
            print e
            session.rollback()
            result = e
        session.close()
        return result

    def addObjects(self, objs):
        session = self.getSession()
        result = "ok"
        try:
            result = session.add_all(objs)

            session.commit()
        except Exception, e:
            print e
            session.rollback()
            result = e
        session.close()
        return result

    def getGroupRecipes(self, group):
        children = filter(self.getGroupRecipes, group.children)
        if not children:
            return group.recipes
        elif not group.recipes:
            return children
        else:
            return children + group.recipes

    def addGroupToTree(self, tree, group):
        if group.parent:
            branch = self.addGroupToTree(tree, group.parent)
        else:
            branch = tree

        try:
            return branch[group]
        except:
            branch[group] = {"recipes": []}
            return branch[group]

    def getRecipesByGroups(self, session, parent=None, title=None):
#        children = filter(self.getGroupRecipes,
#                        session.query(Group).filter(Group.parent_id==None).all())
        query = session.query(Recipe)
        if title:
            print title
            query = query.filter(Recipe.title.like(title))
        recipes = query.all()

        tree = {"recipes": []}
        for recipe in recipes:
            if recipe.groups:
                for group in recipe.groups:
                    self.addGroupToTree(tree, group)["recipes"].append(recipe)
            else:
                tree["recipes"].append(recipe)

        return tree
#        return {"recipes": recipes, "children": children} 

    def getGroups(self, session, parent=None):
        groups = session.query(Group).filter(Group.parent_id==None).all()
        return groups

    def addGroups(self, groups, parent, session):
        print "parent: ", parent
        for params in groups:
            if not "name" in params:
                params["name"] = ""
            if not "description" in params:
                params["description"] = None
            group = Group(name=params["name"],
                            description=params["description"],
                            parent=parent)
            session.add(group)
            if "subgroups" in params:
                self.addGroups(params["subgroups"], group, session)

    def getUnits(self, session):
        return session.query(Unit).all()

    def getUnit(self, name, session):
        if not name:
            return None
        return session.query(Unit).filter(Unit.name==name).one()

    def getSubstances(self, session):
        return session.query(Substance).all()

    def getSubstance(self, name, session):
        try:
            substance = session.query(Substance).filter(Substance.name==name).one()
        except NoResultFound as e:
            print e
            substance = Substance(name=name)
            session.add(substance)
            session.commit()
        return substance

    def getNewerEntries(self, session, date):
        return {"Image":[elem.to_dict for elem in 
                         session.query(Image).filter(Image.updateDate > date).all()],
                "Unit": [elem.to_dict() for elem in 
                        session.query(Unit).filter(Unit.updateDate > date).all()],
                "Substance": [elem.to_dict() for elem in
                    session.query(Substance).filter(Substance.updateDate > date).all()],
                "Recipe": [elem.to_dict() for elem in
                        session.query(Recipe).filter(Recipe.updateDate > date).all()],
                "Ingredient": [elem.to_dict() for elem in
                session.query(Ingredient).filter(Ingredient.updateDate > date).all()]}
