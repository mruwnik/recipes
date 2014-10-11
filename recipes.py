#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""recipe.py: the main functionality of this program"""

__author__      = "Daniel O'Connell"
__copyright__   = "BSD-3"

import wx
import wx.richtext as rt
import sqlalchemy.exc

import GUI
from widgets.recipePanel import RecipePanel
from widgets.editRecipe import EditRecipe
from  database import *

class RecipesWindow(GUI.MainWindow):
    def setup(self):
        self.tabs = {"recipes" : 0,
                     "edit" : 1}

        self.database = DBConfig('sqlite:///database.db')

        session = self.database.getSession()
        self.user =  session.query(User).filter(User.name.like('dan')).first()

        session.close()

        self.tabsContainer.SetSelection(self.tabs["edit"])
        self.setupEditRecipe(self.edit_recipe_tab)

        self.recipes_menu_options = ["open in new tab", "edit", "delete"]

        self.setStatusBarText("setup: OK")

    def getSession(self):
        try:
            return self.session
        except:
            self.session = self.database.getSession()
        return self.session

    def findRecipes( self, event ):
        event.Skip()
        name = "%" + self.searchRecipeName.GetValue() + "%"
        self.setupRecipes(self.database
                          .getRecipesByGroups(self.getSession(),
                                               title=name))

    def filterRecipes( self, event ):
        event.Skip()

    def filterGroups( self, event ):
        event.Skip()

    def saveRecipe(self, edit_recipe):
        self.setStatusBarText("saving recipe")
        errors = False

        ingredients = edit_recipe.get_ingredients()
        if ingredients == None:
            errors = True

        title = edit_recipe.get_name()
        if not title:
            errors = True
            #TODO: display error message

        if not errors:
            recipe = edit_recipe.get_recipe()
            if not recipe:
                recipe = Recipe()
            recipe.title=title
            recipe.description=edit_recipe.get_description()
            recipe.algorythm=edit_recipe.get_algorythm()
            recipe.time=edit_recipe.get_time()
            recipe.difficulty=edit_recipe.get_difficulty()
            recipe.user=self.user
            recipe.groups=edit_recipe.get_groups()

            if not recipe.id:
                self.setStatusBarText(self.database.addObject(recipe))
            elif recipe.ingredients:
                for ingredient in recipe.ingredients:
                    self.getSession().delete(ingredient)
                recipe.ingredients = []
                self.getSession().flush()

            for substance, amount, unit in ingredients:
                try:
                    self.database\
                        .addObject(Ingredient(recipe=recipe,
                                            substance=self.database\
                                                .getSubstance(substance,
                                                       self.getSession()),
                                        unit=self.database\
                                                .getUnit(unit, self.getSession()),
                                          amount=amount))
                except sqlalchemy.exc.IntegrityError as e:
                    print e

            self.getSession().commit()

            current = self.tabsContainer.GetSelection()
            self.setupRecipes(self.database.getRecipesByGroups(self.getSession()))
            self.tabsContainer.SetSelection(self.tabs["recipes"])
            #TODO: this should be a delete, but that causes everything to blow up
            self.tabsContainer.RemovePage(current)
        else:
            self.setStatusBarText("errors")

    def setupEditRecipe(self, tab):
        substance_names = [name.name for name in
                                    self.database.getSubstances(self.getSession())]
        unit_names = [name.name for name in
                                    self.database.getUnits(self.getSession())]
        groups = self.database.getGroups(self.getSession())
        tab.setup(groups, substance_names, unit_names)
        tab.set_save_action(self.saveRecipe)

    def edit_recipe(self, recipe):
        tab = wx.Panel(self.tabsContainer, wx.ID_ANY,
                           wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)

        tabs_sizer = wx.BoxSizer(wx.VERTICAL)

        panel = EditRecipe(tab)
        tabs_sizer.Add(panel, 1, wx.ALL|wx.EXPAND, 5)

        tab.SetSizer(tabs_sizer)
        tab.Layout()
        tabs_sizer.Fit(tab)
        self.tabsContainer.AddPage(tab, "edit recipe", True, wx.NullBitmap)

        self.setupEditRecipe(panel)
        panel.set_recipe(recipe)

    def addNodeToTree(self, tree, parent, data, name, normalPic, expandedPic):
        node = tree.AppendItem(parent, name)
        tree.SetPyData(node, data)
        tree.SetItemImage(node, normalPic, wx.TreeItemIcon_Normal)
        tree.SetItemImage(node, expandedPic, wx.TreeItemIcon_Expanded)
        return node

    def addRecipesToTree(self, tree, treeNode, groups, normalPic, expandedPic,
                         recipePic):

        for child, data in groups.iteritems():
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

        isz = (16,16)
        il = wx.ImageList(isz[0], isz[1])
        fldridx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, isz))
        fldropenidx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, isz))
        fileidx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, isz))
        self.recipesList.SetImageList(il)
        self.il = il

        try:
            self.recipesList.DeleteChildren(self.recipesRoot)
        except:
            self.recipesRoot = self.recipesList.AddRoot("Recipes")

        self.addRecipesToTree(self.recipesList, self.recipesRoot, recipes,
                                        fldridx, fldropenidx, fileidx)

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
        if event.GetId() == 0: # open in new tab
            self.open_recipe_tab(self.selected_recipe)
        elif event.GetId() == 1: # edit
            self.edit_recipe(self.selected_recipe)
        elif event.GetId() == 2: # delete
            self.getSession().delete(self.selected_recipe)
            self.getSession().commit()
            self.selected_recipe = None
            self.recipesList.Delete(self.selected_node)
            self.setupRecipes(self.database.getRecipesByGroups(self.getSession()))
            self.Layout()

    def open_recipe_tab(self, recipe):
        tab = wx.Panel(self.tabsContainer, wx.ID_ANY,
                           wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)

        tabs_sizer = wx.BoxSizer(wx.VERTICAL)

        recipe_panel = RecipePanel(tab)
        tabs_sizer.Add(recipe_panel, 1, wx.ALL|wx.EXPAND, 5)

        tab.SetSizer(tabs_sizer)
        tab.Layout()
        tabs_sizer.Fit(tab)
        self.tabsContainer.AddPage(tab, recipe.title, True, wx.NullBitmap)
        self.showRecipe(recipe, recipe_panel)

    def selectRecipe(self, event):
        event.Skip()
        item = event.GetItem()
        if item and not self.recipesList.ItemHasChildren(item):
            self.setStatusBarText(self.recipesList.GetPyData(item))
            self.showRecipe(self.recipesList.GetPyData(item), self.recipe_panel)
        else:
            self.recipesList.Toggle(item)

    def tabChanged( self, event ):
        event.Skip()
#        try:
#            self.session().close()
#        except:
#            pass
        if self.tabs["recipes"] == self.tabsContainer.GetSelection():
            self.setupRecipes(self.database.getRecipesByGroups(self.getSession()))
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

app = wx.App()

AddRTCHandlers()

mainWindow = RecipesWindow(None)
mainWindow.setup()
mainWindow.Show()

app.MainLoop()

session = mainWindow.database.getSession()

session.close()
