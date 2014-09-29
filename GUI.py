# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Sep  8 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.aui
from widgets.editRecipe import EditRecipe
from widgets.recipePanel import RecipePanel
import wx.richtext as rt

###########################################################################
## Class MainWindow
###########################################################################

class MainWindow ( wx.Frame ):
    
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"recipe",
                           pos=wx.DefaultPosition, size=wx.DefaultSize,# wx.Size( 1280,800 ),
                           style = wx.CLOSE_BOX|wx.DEFAULT_FRAME_STYLE|wx.MAXIMIZE|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.TAB_TRAVERSAL)
        
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        
        self.m_menubar1 = wx.MenuBar( 0 )
        self.SetMenuBar( self.m_menubar1 )
        
        self.m_statusBar1 = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        
        self.tabsContainer = wx.aui.AuiNotebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.aui.AUI_NB_DEFAULT_STYLE)
        self.recipesTab = wx.Panel( self.tabsContainer, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer2 = wx.BoxSizer( wx.VERTICAL )
        
        bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.searchRecipeNameLabel = wx.StaticText( self.recipesTab, wx.ID_ANY, u"recipe name", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.searchRecipeNameLabel.Wrap( -1 )
        bSizer5.Add( self.searchRecipeNameLabel, 0, wx.ALL, 5 )
        
        self.searchRecipeName = wx.TextCtrl( self.recipesTab, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer5.Add( self.searchRecipeName, 1, wx.ALL|wx.EXPAND, 5 )
        
        self.m_staticText2 = wx.StaticText( self.recipesTab, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )
        bSizer5.Add( self.m_staticText2, 0, wx.ALL, 5 )
        
        self.m_textCtrl31 = wx.TextCtrl( self.recipesTab, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer5.Add( self.m_textCtrl31, 1, wx.ALL|wx.EXPAND, 5 )
        
        bSizer2.Add( bSizer5, 0, wx.ALIGN_LEFT, 5 )
        
        bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.searchRecipeCostLabel = wx.StaticText( self.recipesTab, wx.ID_ANY, u"cost", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.searchRecipeCostLabel.Wrap( -1 )
        bSizer6.Add( self.searchRecipeCostLabel, 0, wx.ALL, 5 )
        
        self.searchRecipeCost = wx.TextCtrl( self.recipesTab, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.searchRecipeCost, 0, wx.ALL, 5 )
        
        self.m_staticText4 = wx.StaticText( self.recipesTab, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )
        bSizer6.Add( self.m_staticText4, 0, wx.ALL, 5 )
        
        self.m_textCtrl3 = wx.TextCtrl( self.recipesTab, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.m_textCtrl3, 0, wx.ALL, 5 )
        
        self.searchButton = wx.Button( self.recipesTab, wx.ID_ANY, u"search", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.searchButton, 0, wx.ALL, 5 )
        
        bSizer2.Add( bSizer6, 0, wx.EXPAND, 5 )
        
        bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.recipesList = wx.TreeCtrl( self.recipesTab, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE|wx.TR_HIDE_ROOT )
        bSizer7.Add( self.recipesList, 0, wx.ALIGN_LEFT|wx.ALIGN_TOP|wx.ALL|wx.EXPAND, 5 )
        
        self.recipe_panel = RecipePanel(self.recipesTab)
        bSizer7.Add(self.recipe_panel, 1, wx.ALL|wx.EXPAND, 5)
        
        bSizer2.Add( bSizer7, 1, wx.EXPAND, 5 )
        
        self.recipesTab.SetSizer( bSizer2 )
        self.recipesTab.Layout()
        bSizer2.Fit( self.recipesTab )
        self.tabsContainer.AddPage( self.recipesTab, u"recipes", False, wx.NullBitmap )
        
        self.addRecipeTab = wx.Panel( self.tabsContainer, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer91 = wx.BoxSizer( wx.HORIZONTAL )
        self.edit_recipe_tab = EditRecipe(self.addRecipeTab)
        bSizer91.Add(self.edit_recipe_tab, 1, wx.ALL|wx.EXPAND, 5 )
        
        self.addRecipeTab.SetSizer( bSizer91 )
        self.addRecipeTab.Layout()
        bSizer91.Fit( self.addRecipeTab )
        self.tabsContainer.AddPage( self.addRecipeTab, u"addRecipe", True, wx.NullBitmap )
        bSizer1.Add( self.tabsContainer, 1, wx.EXPAND |wx.ALL, 5 )
        self.SetSizer( bSizer1 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        # Connect Events
        self.tabsContainer.Bind( wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.tabChanged )
        self.searchButton.Bind( wx.EVT_BUTTON, self.findRecipes )
        self.recipesList.Bind( wx.EVT_CHAR, self.filterRecipes )
        self.recipesList.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.showRecipesMenu)
        self.recipesList.Bind( wx.EVT_TREE_SEL_CHANGED, self.selectRecipe )

#        self.editRecipesGroups.Bind( wx.EVT_CHAR, self.filterGroups )
#        self.editRecipeMoreIngredients.Bind( wx.EVT_BUTTON, self.add_ingredients_row )
#        self.editRecipeSave.Bind( wx.EVT_BUTTON, self.saveRecipe )
        
    def __del__( self ):
        pass
    
    
    # Virtual event handlers, overide them in your derived class
    def tabChanged( self, event ):
        event.Skip()
    
    def findRecipes( self, event ):
        event.Skip()
    
    def filterRecipes( self, event ):
        event.Skip()
    
    def selectRecipe( self, event ):
        event.Skip()
    
    def filterGroups( self, event ):
        event.Skip()
    
    def find_ingredient( self, event ):
        event.Skip()
    
    def find_unit( self, event ):
        event.Skip()
    
    def remove_ingredient( self, event ):
        event.Skip()
    
    def add_ingredients_row( self, event ):
        event.Skip()
    
    def saveRecipe( self, event ):
        event.Skip()
    

