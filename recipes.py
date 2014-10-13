#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""recipe.py: the main functionality of this program"""

__author__ = "Daniel O'Connell"
__copyright__ = "BSD-3"

import logging

import wx
import wx.richtext as rt
import sqlalchemy.exc

import GUI
from widgets.recipePanel import RecipePanel
from widgets.editRecipe import EditRecipe
from widgets.treeControls import FILE_ICON, FOLDER_ICON, FOLDER_OPEN_ICON
from database import DBConfig
from database import session_scope
from models import *

import i18n
_ = i18n.language.ugettext

logging.basicConfig(filename='recipes.log', level=logging.DEBUG)


class RecipesWindow(GUI.MainWindow):
    def setup(self):
        self.tabs = {"recipes": 0,
                     "edit": 1}

        self.database = DBConfig('sqlite:///database.db')

        session = self.database.getSession()
        self.userId = session.query(User)\
            .filter(User.name.like('dan')).first().id

        session.close()

        self.tabsContainer.SetSelection(self.tabs["recipes"])
        isz = (16, 16)
        self.il = wx.ImageList(isz[0], isz[1])
        self.icons = {
            FOLDER_ICON: self.il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER,
                                                              wx.ART_OTHER, isz)),
            FOLDER_OPEN_ICON: self.il.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN,
                                                                   wx.ART_OTHER,
                                                              isz)),
            FILE_ICON: self.il.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE,
                                                            wx.ART_OTHER, isz))}
        self.recipesList.SetImageList(self.il)
        self.getRecipes()
        with session_scope(self.database) as session:
            substance_names = [name.name for name in
                               self.database.getSubstances(session)]
            self.searchIngredients.SetChoices(substance_names)

        self.searchIngredients.SetItemsCallback(self.filterIngredients)

        self.setupEditRecipe(self.edit_recipe_tab)

        self.recipes_menu_options = [_("open in new tab"), _("edit"),
                                     _("new"), _("delete")]

        self.setStatusBarText(_("setup: OK"))

    def getRecipes(self, name=None, ingredients=None, groups=None):
        print name, ingredients
        with session_scope(self.database) as session:
            self.setupRecipes(self.database.
                              getRecipesByGroups(session,
                                                 title=name,
                                                 ingredients=ingredients))
        if name or ingredients:
            self.recipesList.ExpandAllChildren(self.recipesList.GetRootItem())
        else:
            self.recipesList.CollapseAllChildren(self.recipesList.GetRootItem())

    def filterIngredients(self, items):
        name = None
        if self.searchRecipeName.GetValue():
            name = "%" + self.searchRecipeName.GetValue() + "%"
        self.getRecipes(name, items)

    def filterRecipes(self, event):
        event.Skip()
        name = None
        if event.GetString():
            name = '%' + event.GetString() + '%'
        self.getRecipes(name, self.searchIngredients.GetItems())

    def filterGroups(self, event):
        event.Skip()

    def saveRecipe(self, edit_recipe):
        self.setStatusBarText(_("saving recipe"))
        errors = False

        ingredients = edit_recipe.get_ingredients()
        if ingredients is None:
            errors = True

        title = edit_recipe.get_name()
        if not title:
            errors = True
            #TODO: display error message

        if not errors:
            with session_scope(self.database) as session:
                logging.debug("user %s" % session.query(User).get(self.userId))
                recipe = None
                if edit_recipe.get_recipe_id():
                    recipe = session.query(Recipe)\
                        .get(edit_recipe.get_recipe_id())
                if not recipe:
                    recipe = Recipe()
                recipe.title = title
                recipe.description = edit_recipe.get_description()
                recipe.algorythm = edit_recipe.get_algorythm()
                recipe.time = edit_recipe.get_time()
                recipe.difficulty = edit_recipe.get_difficulty()
                recipe.groups = session.query(Group)\
                    .filter(Group.id.in_(edit_recipe.get_groups())).all()
                recipe.user = session.query(User).get(self.userId)

                if not recipe.id:
                    self.setStatusBarText(session.add(recipe))
                elif recipe.ingredients:
                    for ingredient in recipe.ingredients:
                        session.delete(ingredient)
                    recipe.ingredients = []
                    session.flush()

                for substance, amount, unit in ingredients:
                    try:
                        session.add(Ingredient(recipe=recipe,
                                               substance=self.database
                                               .getSubstance(substance,
                                                             session),
                                               unit=self.database
                                               .getUnit(unit,
                                                        session),
                                               amount=amount))
                    except sqlalchemy.exc.IntegrityError as e:
                        logging.error(e)

            current = self.tabsContainer.GetSelection()
            self.tabsContainer.SetSelection(self.tabs["recipes"])
         #TODO: this should be a delete, but that causes everything to blow up
            self.tabsContainer.RemovePage(current)
        else:
            self.setStatusBarText(_("errors"))

    def setupEditRecipe(self, tab):
        with session_scope(self.database) as session:
            substance_names = [name.name for name in
                               self.database.getSubstances(session)]
            unit_names = [name.name for name in
                          self.database.getUnits(session)]
            groups = self.database.getGroups(session)
            tab.setup(groups, substance_names, unit_names)
            tab.set_save_action(self.saveRecipe)

    def edit_recipe(self, recipe=None):
        tab = wx.Panel(self.tabsContainer, wx.ID_ANY,
                       wx.DefaultPosition, wx.DefaultSize,
                       wx.TAB_TRAVERSAL)

        tabs_sizer = wx.BoxSizer(wx.VERTICAL)

        panel = EditRecipe(tab)
        tabs_sizer.Add(panel, 1, wx.ALL | wx.EXPAND, 5)

        tab.SetSizer(tabs_sizer)
        tab.Layout()
        tabs_sizer.Fit(tab)
        if recipe:
            title = _("edit recipe")
        else:
            title = _("add recipe")
        self.tabsContainer.AddPage(tab, title, True, wx.NullBitmap)

        self.setupEditRecipe(panel)
        if recipe:
            panel.set_recipe(recipe)

    def addNodeToTree(self, tree, parent, data, name, normalPic, expandedPic):
        node = tree.AppendItem(parent, name)
        tree.SetPyData(node, data.id)
        tree.SetItemImage(node, normalPic, wx.TreeItemIcon_Normal)
        tree.SetItemImage(node, expandedPic, wx.TreeItemIcon_Expanded)
        return node

    def addRecipesToTree(self, tree, treeNode, groups, normalPic, expandedPic,
                         recipePic):

        for child, data in iter(sorted(groups.items())):
            if child != "recipes":
                node = self.addNodeToTree(tree, treeNode,  child, child.name,
                                          normalPic, expandedPic)
                self.addRecipesToTree(tree, node, data,
                                      normalPic, expandedPic, recipePic)

        try:
            for recipe in groups["recipes"]:
                self.addNodeToTree(tree, treeNode, recipe, recipe.title,
                                   recipePic, expandedPic)
        except:
            pass

    def setupRecipes(self, recipes, selected=None):
        tree = self.recipesList

        try:
            tree.DeleteChildren(self.recipesRoot)
        except:
            self.recipesRoot = tree.AddRoot(_("Recipes"))

        if recipes["recipes"]:
            self.addRecipesToTree(tree, self.recipesRoot, recipes,
                                  self.icons[FOLDER_ICON],
                                  self.icons[FOLDER_OPEN_ICON],
                                  self.icons[FILE_ICON])

            item, cookie = tree.GetFirstChild(tree.GetRootItem())
            while item and tree.ItemHasChildren(item):
                item, cookie = tree.GetFirstChild(item)
            with session_scope(self.database) as session:
                recipe = session.query(Recipe)\
                    .get(self.recipesList.GetPyData(item))

                self.setStatusBarText(recipe)
                self.showRecipe(recipe, self.recipe_panel)
        else:
            self.clearRecipe(self.recipe_panel)

    def showRecipe(self, recipe, panel):
        panel.set_title(recipe.title)

        panel.set_description(recipe.description,
                              not recipe.description.startswith("<?xml"))
        panel.set_algorythm(recipe.algorythm,
                            not recipe.algorythm.startswith("<?xml"))

        ingredients = ""
        for i in recipe.ingredients:
            print i.standardise_amount()
            ingredients += unicode(i) + "\r\n"
        panel.set_ingredients(ingredients)

        groups = ""
        for group in recipe.groups:
            if groups:
                groups += ", "
            groups += group.name

        panel.set_groups(groups)
        panel.set_time(recipe.time)
        panel.set_difficulty(recipe.difficulty)

    def clearRecipe(self, panel):
        panel.set_title('')
        panel.set_description('', True)
        panel.set_algorythm('', True)
        panel.set_ingredients('')
        panel.set_groups('')
        panel.set_time('')
        panel.set_difficulty('')

    def showRecipesMenu(self, event):
        event.Skip()

        item = event.GetItem()
        if item and not self.recipesList.ItemHasChildren(item):
            self.selected_recipe = self.recipesList.GetPyData(item)
            self.selected_node = item
            menu = wx.Menu()
            for id in range(0, len(self.recipes_menu_options)):
                menu.Append(id, self.recipes_menu_options[id])
                wx.EVT_MENU(menu, id, self.recipe_options)

            self.PopupMenu(menu, event.GetPoint())
            menu.Destroy()

    def recipe_options(self, event):
        with session_scope(self.database) as session:
            recipe = session.query(Recipe).get(self.selected_recipe)
            if event.GetId() == 0:  # open in new tab
                self.open_recipe_tab(recipe)
            elif event.GetId() == 1:  # edit
                self.edit_recipe(recipe)
            elif event.GetId() == 2:  # new
                self.edit_recipe()
            elif event.GetId() == 3:  # delete
                session.delete(recipe)
                session.commit()
                self.selected_recipe = None
                self.setupRecipes(self.database.getRecipesByGroups(session))
            self.Layout()

    def open_recipe_tab(self, recipe):
        tab = wx.Panel(self.tabsContainer, wx.ID_ANY,
                       wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)

        tabs_sizer = wx.BoxSizer(wx.VERTICAL)

        recipe_panel = RecipePanel(tab)
        tabs_sizer.Add(recipe_panel, 1, wx.ALL | wx.EXPAND, 5)

        tab.SetSizer(tabs_sizer)
        tab.Layout()
        tabs_sizer.Fit(tab)
        self.tabsContainer.AddPage(tab, recipe.title, True, wx.NullBitmap)
        self.showRecipe(recipe, recipe_panel)

    def selectRecipe(self, event):
        event.Skip()
        item = event.GetItem()
        if item and not self.recipesList.ItemHasChildren(item):
            with session_scope(self.database) as session:
                recipe = session.query(Recipe)\
                    .get(self.recipesList.GetPyData(item))

                self.setStatusBarText(recipe)
                self.showRecipe(recipe, self.recipe_panel)
        else:
            self.recipesList.Toggle(item)

    def tabChanged(self, event):
        event.Skip()
        if self.tabs["recipes"] == self.tabsContainer.GetSelection():
            name = None
            if self.searchRecipeName.GetValue():
                name = "%" + self.searchRecipeName.GetValue() + "%"
            self.getRecipes(name, self.searchIngredients.GetItems())
#        elif self.tabs["edit"] == self.tabsContainer.GetSelection():
#            self.setupEditRecipe(self.edit_recipe_tab)

    def setStatusBarText(self, text):
        self.m_statusBar1.SetStatusText(unicode(text))


def AddRTCHandlers():
        # make sure we haven't already added them.
        if rt.RichTextBuffer.FindHandlerByType(rt.RICHTEXT_TYPE_HTML) is not None:
            return

        rt.RichTextBuffer.AddHandler(rt.RichTextHTMLHandler())
        rt.RichTextBuffer.AddHandler(rt.RichTextXMLHandler())

        # This is needed for the view as HTML option since we tell it
        # to store the images in the memory file system.
        wx.FileSystem.AddHandler(wx.MemoryFSHandler())


logging.debug("creating app")
app = wx.App()

AddRTCHandlers()
logging.debug("added RTC handlers")

mainWindow = RecipesWindow(None)
mainWindow.setup()
logging.debug("setup done")
mainWindow.Show()
logging.debug("showing window")

logging.debug("starting main loop")
app.MainLoop()

session = mainWindow.database.getSession()

session.close()
