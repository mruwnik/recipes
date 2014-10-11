#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""editRecipe.py: handles the addition of a recipe"""

from cStringIO import StringIO
import logging

import wx
import wx.aui
import wx.richtext as rt
import wx.lib.scrolledpanel as scrolled
from widgets.ingredients import AddIngredients
import images
import widgets.treeControls as tc


class EditRecipe (wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY,
                          pos=wx.DefaultPosition,
                          size=wx.DefaultSize,
                          style=wx.TAB_TRAVERSAL | wx.VSCROLL)

        self.main_container = wx.BoxSizer(wx.HORIZONTAL)

        self.groups_container = wx.BoxSizer(wx.VERTICAL)

        self.editRecipeGroupsLabel = wx.StaticText(self, wx.ID_ANY,
                                                   u"groups",
                                                   wx.DefaultPosition,
                                                   wx.DefaultSize, 0)
        self.editRecipeGroupsLabel.Wrap(-1)
        self.groups_container.Add(self.editRecipeGroupsLabel, 0, wx.ALL, 5)

        self.editRecipesGroups = tc.ControlsTreeCtrl("Groups", self,
                                                     wx.ID_ANY,
                                                     wx.DefaultPosition,
                                                     wx.DefaultSize,
                                                     wx.TR_DEFAULT_STYLE |
                                                     wx.TR_HIDE_ROOT |
                                                     wx.TR_MULTIPLE)
        self.groups_container.Add(self.editRecipesGroups, 1,
                                  wx.ALL | wx.EXPAND, 5)

        self.main_container.Add(self.groups_container, 1, wx.EXPAND, 5)

        panel1 = scrolled.ScrolledPanel(self, -1, size=(140, 300),
                                        style = wx.TAB_TRAVERSAL |
                                        wx.SUNKEN_BORDER,
                                        name="panel1")

        self.fields_container = wx.FlexGridSizer(11, 2, 0, 0)
        self.fields_container.SetFlexibleDirection(wx.BOTH)
        self.fields_container.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.editRecipeNameLabel = wx.StaticText(panel1, wx.ID_ANY,
                                                 u"name",
                                                 wx.DefaultPosition,
                                                 wx.DefaultSize, 0)
        self.editRecipeNameLabel.Wrap(-1)
        self.fields_container.Add(self.editRecipeNameLabel, 0, wx.ALL, 5)

        self.editRecipeName = wx.TextCtrl(panel1, wx.ID_ANY,
                                          wx.EmptyString,
                                          wx.DefaultPosition,
                                          wx.DefaultSize, 0)
        self.fields_container.Add(self.editRecipeName, 1, wx.EXPAND, 5)

        self.editRecipeDescLabel = wx.StaticText(panel1, wx.ID_ANY,
                                                 u"description",
                                                 wx.DefaultPosition,
                                                 wx.DefaultSize, 0)
        self.editRecipeDescLabel.Wrap(-1)
        self.fields_container.Add(self.editRecipeDescLabel, 0, wx.ALL, 5)

        self.tb = self.MakeToolBar(panel1)
        self.fields_container.Add(self.tb, 0,
                                  wx.ALL | wx.ALIGN_LEFT | wx.EXPAND, 4)
        self.fields_container.AddSpacer((0, 0), 1, wx.EXPAND, 1)

        self.editRecipeDesc = rt.RichTextCtrl(panel1,
                                              style=wx.VSCROLL | wx.HSCROLL)
        self.editRecipeDesc.SetMinSize(wx.Size(-1, 80))
        self.rtc = self.editRecipeDesc

        self.fields_container.Add(self.editRecipeDesc, 2,
                                  wx.ALL | wx.EXPAND, 5)

        self.editRecipeAlgorythmLabel = wx.StaticText(panel1,
                                                      wx.ID_ANY,
                                                      u"recipe",
                                                      wx.DefaultPosition,
                                                      wx.DefaultSize, 0)
        self.editRecipeAlgorythmLabel.Wrap(-1)
        self.fields_container.Add(self.editRecipeAlgorythmLabel, 0, wx.ALL, 5)

        self.editRecipeAlgorythm = rt.RichTextCtrl(panel1,
                                                   style=wx.VSCROLL | wx.HSCROLL)
        self.editRecipeAlgorythm.SetMinSize(wx.Size(900, 420))

        self.fields_container.Add(self.editRecipeAlgorythm, 1,
                                  wx.ALL | wx.EXPAND, 5)

        self.editRecipeIngredientsLabel = wx.StaticText(panel1,
                                                        wx.ID_ANY,
                                                        u"ingredients",
                                                        wx.DefaultPosition,
                                                        wx.DefaultSize, 0)
        self.editRecipeIngredientsLabel.Wrap(-1)
        self.fields_container.Add(self.editRecipeIngredientsLabel, 0,
                                  wx.ALL, 5)

        self.editRecipeIngredients = AddIngredients(panel1)
        self.fields_container.Add(self.editRecipeIngredients, 0, wx.EXPAND, 5)

        self.fields_container.AddSpacer((0, 0), 1, wx.ALL | wx.EXPAND, 5)

        self.editRecipeMoreIngredients = wx.Button(panel1, wx.ID_ANY,
                                                   u"add another ingredient",
                                                   wx.DefaultPosition,
                                                   wx.DefaultSize, 0)
        self.fields_container.Add(self.editRecipeMoreIngredients, 0, wx.ALL, 5)

        self.fields_container.AddSpacer((0, 0), 1, wx.EXPAND, 5)

        self.fields_container.AddSpacer((0, 0), 1, wx.EXPAND, 5)

        self.m_staticText31 = wx.StaticText(panel1, wx.ID_ANY, u"time",
                                            wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.m_staticText31.Wrap(-1)
        self.fields_container.Add(self.m_staticText31, 0, wx.ALL, 5)

        self.editRecipeTime = wx.TextCtrl(panel1, wx.ID_ANY,
                                          wx.EmptyString,
                                          wx.DefaultPosition,
                                          wx.DefaultSize, 0)
        self.fields_container.Add(self.editRecipeTime, 0, wx.ALL, 5)

        self.m_staticText32 = wx.StaticText(panel1, wx.ID_ANY,
                                            u"difficulty",
                                            wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.m_staticText32.Wrap(-1)
        self.fields_container.Add(self.m_staticText32, 0, wx.ALL, 5)

        self.editRecipeDifficulty = wx.TextCtrl(panel1, wx.ID_ANY,
                                                wx.EmptyString,
                                                wx.DefaultPosition,
                                                wx.DefaultSize, 0)
        self.fields_container.Add(self.editRecipeDifficulty, 0, wx.ALL, 5)

        self.editRecipeSave = wx.Button(panel1, wx.ID_ANY,
                                        u"save",
                                        wx.DefaultPosition,
                                        wx.DefaultSize, 0)
        self.fields_container.Add(self.editRecipeSave, 0, wx.ALL, 5)

        panel1.SetSizer(self.fields_container)
        panel1.SetAutoLayout(1)
        panel1.SetupScrolling()

        self.main_container.Add(panel1, 5, wx.EXPAND, 5)

        self.SetSizer(self.main_container)
        self.Layout()
        self.main_container.Fit(self)

        self.Centre(wx.BOTH)

        # Connect Events
        self.editRecipeDesc.Bind(wx.EVT_SET_FOCUS, self.selectTextFocus)
        self.editRecipeAlgorythm.Bind(wx.EVT_SET_FOCUS, self.selectTextFocus)
        self.editRecipesGroups.Bind(wx.EVT_CHAR, self.filterGroups)
        self.editRecipeMoreIngredients.Bind(wx.EVT_BUTTON,
                                            self.editRecipeIngredients.add_ingredients_row)
        self.editRecipeSave.Bind(wx.EVT_BUTTON, self.saveRecipe)

        self.save_action = None

    def OnFileOpen(self, evt):
        # This gives us a string suitable for the file dialog based on
        # the file handlers that are loaded
        wildcard, types = rt.RichTextBuffer.GetExtWildcard(save=False)
        dlg = wx.FileDialog(self, "Choose a filename",
                            wildcard=wildcard,
                            style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            if path:
                fileType = types[dlg.GetFilterIndex()]
                self.rtc.LoadFile(path, fileType)
        dlg.Destroy()

    def OnFileSave(self, evt):
        if not self.rtc.GetFilename():
            self.OnFileSaveAs(evt)
            return
        self.rtc.SaveFile()

    def OnFileSaveAs(self, evt):
        wildcard, types = rt.RichTextBuffer.GetExtWildcard(save=True)

        dlg = wx.FileDialog(self, "Choose a filename",
                            wildcard=wildcard,
                            style=wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            if path:
                fileType = types[dlg.GetFilterIndex()]
                ext = rt.RichTextBuffer.FindHandlerByType(fileType).GetExtension()
                if not path.endswith(ext):
                    path += '.' + ext
                self.rtc.SaveFile(path, fileType)
        dlg.Destroy()

    def OnFileViewHTML(self, evt):
        # Get an instance of the html file handler, use it to save the
        # document to a StringIO stream, and then display the
        # resulting html text in a dialog with a HtmlWindow.
        handler = rt.RichTextHTMLHandler()
        handler.SetFlags(rt.RICHTEXT_HANDLER_SAVE_IMAGES_TO_MEMORY)
        handler.SetFontSizeMapping([7, 9, 11, 12, 14, 22, 100])

        import cStringIO
        stream = cStringIO.StringIO()
        if not handler.SaveStream(self.rtc.GetBuffer(), stream):
            return

        import wx.html
        dlg = wx.Dialog(self, title="HTML",
                        style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        html = wx.html.HtmlWindow(dlg, size=(500, 400),
                                  style=wx.BORDER_SUNKEN)
        html.SetPage(stream.getvalue())
        btn = wx.Button(dlg, wx.ID_CANCEL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(html, 1, wx.ALL | wx.EXPAND, 5)
        sizer.Add(btn, 0, wx.ALL | wx.CENTER, 10)
        dlg.SetSizer(sizer)
        sizer.Fit(dlg)

        dlg.ShowModal()

        handler.DeleteTemporaryImages()

    def OnBold(self, evt):
        self.rtc.ApplyBoldToSelection()

    def OnItalic(self, evt):
        self.rtc.ApplyItalicToSelection()

    def OnUnderline(self, evt):
        self.rtc.ApplyUnderlineToSelection()

    def OnAlignLeft(self, evt):
        self.rtc.ApplyAlignmentToSelection(rt.TEXT_ALIGNMENT_LEFT)

    def OnAlignRight(self, evt):
        self.rtc.ApplyAlignmentToSelection(rt.TEXT_ALIGNMENT_RIGHT)

    def OnAlignCenter(self, evt):
        self.rtc.ApplyAlignmentToSelection(rt.TEXT_ALIGNMENT_CENTRE)

    def OnIndentMore(self, evt):
        attr = rt.RichTextAttr()
        attr.SetFlags(rt.TEXT_ATTR_LEFT_INDENT)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

            attr.SetLeftIndent(attr.GetLeftIndent() + 100)
            attr.SetFlags(rt.TEXT_ATTR_LEFT_INDENT)
            self.rtc.SetStyle(r, attr)

    def OnIndentLess(self, evt):
        attr = rt.RichTextAttr()
        attr.SetFlags(rt.TEXT_ATTR_LEFT_INDENT)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

        if attr.GetLeftIndent() >= 100:
            attr.SetLeftIndent(attr.GetLeftIndent() - 100)
            attr.SetFlags(rt.TEXT_ATTR_LEFT_INDENT)
            self.rtc.SetStyle(r, attr)

    def OnParagraphSpacingMore(self, evt):
        attr = rt.RichTextAttr()
        attr.SetFlags(rt.TEXT_ATTR_PARA_SPACING_AFTER)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

            attr.SetParagraphSpacingAfter(attr.GetParagraphSpacingAfter() + 20)
            attr.SetFlags(rt.TEXT_ATTR_PARA_SPACING_AFTER)
            self.rtc.SetStyle(r, attr)

    def OnParagraphSpacingLess(self, evt):
        attr = rt.RichTextAttr()
        attr.SetFlags(rt.TEXT_ATTR_PARA_SPACING_AFTER)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

            if attr.GetParagraphSpacingAfter() >= 20:
                attr.SetParagraphSpacingAfter(attr.GetParagraphSpacingAfter() - 20)
                attr.SetFlags(rt.TEXT_ATTR_PARA_SPACING_AFTER)
                self.rtc.SetStyle(r, attr)

    def OnLineSpacingSingle(self, evt):
        attr = rt.RichTextAttr()
        attr.SetFlags(rt.TEXT_ATTR_LINE_SPACING)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

            attr.SetFlags(rt.TEXT_ATTR_LINE_SPACING)
            attr.SetLineSpacing(10)
            self.rtc.SetStyle(r, attr)

    def OnLineSpacingHalf(self, evt):
        attr = rt.RichTextAttr()
        attr.SetFlags(rt.TEXT_ATTR_LINE_SPACING)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

            attr.SetFlags(rt.TEXT_ATTR_LINE_SPACING)
            attr.SetLineSpacing(15)
            self.rtc.SetStyle(r, attr)

    def OnLineSpacingDouble(self, evt):
        attr = rt.RichTextAttr()
        attr.SetFlags(rt.TEXT_ATTR_LINE_SPACING)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

            attr.SetFlags(rt.TEXT_ATTR_LINE_SPACING)
            attr.SetLineSpacing(20)
            self.rtc.SetStyle(r, attr)

    def OnFont(self, evt):
        if self.rtc.HasSelection():
            r = self.rtc.GetSelectionRange()
        else:
            r = None
        fontData = wx.FontData()
        fontData.EnableEffects(False)
        attr = rt.RichTextAttr()
        attr.SetFlags(rt.TEXT_ATTR_FONT)
        if self.rtc.GetStyle(self.rtc.GetInsertionPoint(), attr):
            fontData.SetInitialFont(attr.GetFont())

        dlg = wx.FontDialog(self, fontData)
        if dlg.ShowModal() == wx.ID_OK:
            fontData = dlg.GetFontData()
            font = fontData.GetChosenFont()
            if font:
                attr.SetFlags(rt.TEXT_ATTR_FONT)
                attr.SetFont(font)
                if r:
                    self.rtc.SetStyle(r, attr)
                else:
                    self.rtc.BeginStyle(attr)
        dlg.Destroy()

    def OnColour(self, evt):
        colourData = wx.ColourData()
        attr = rt.RichTextAttr()
        attr.SetFlags(rt.TEXT_ATTR_TEXT_COLOUR)
        if self.rtc.GetStyle(self.rtc.GetInsertionPoint(), attr):
            colourData.SetColour(attr.GetTextColour())

        dlg = wx.ColourDialog(self, colourData)
        if dlg.ShowModal() == wx.ID_OK:
            colourData = dlg.GetColourData()
            colour = colourData.GetColour()
            if colour:
                if not self.rtc.HasSelection():
                    self.rtc.BeginTextColour(colour)
                else:
                    r = self.rtc.GetSelectionRange()
                    attr.SetFlags(rt.TEXT_ATTR_TEXT_COLOUR)
                    attr.SetTextColour(colour)
                    self.rtc.SetStyle(r, attr)
        dlg.Destroy()

    def OnUpdateBold(self, evt):
        evt.Check(self.rtc.IsSelectionBold())

    def OnUpdateItalic(self, evt):
        evt.Check(self.rtc.IsSelectionItalics())

    def OnUpdateUnderline(self, evt):
        evt.Check(self.rtc.IsSelectionUnderlined())

    def OnUpdateAlignLeft(self, evt):
        evt.Check(self.rtc.IsSelectionAligned(rt.TEXT_ALIGNMENT_LEFT))

    def OnUpdateAlignCenter(self, evt):
        evt.Check(self.rtc.IsSelectionAligned(rt.TEXT_ALIGNMENT_CENTRE))

    def OnUpdateAlignRight(self, evt):
        evt.Check(self.rtc.IsSelectionAligned(rt.TEXT_ALIGNMENT_RIGHT))

    def ForwardEvent(self, evt):
        # The RichTextCtrl can handle menu and update events for undo,
        # redo, cut, copy, paste, delete, and select all, so just
        # forward the event to it.
        self.rtc.ProcessEvent(evt)

    def MakeToolBar(self, container):
        def doBind(item, handler, updateUI=None):
            self.Bind(wx.EVT_TOOL, handler, item)
            if updateUI is not None:
                self.Bind(wx.EVT_UPDATE_UI, updateUI, item)

        tbar = wx.ToolBar(container, -1)

        doBind(tbar.AddTool(-1, images.get_rt_openBitmap(),
                            shortHelpString="Open"), self.OnFileOpen)
        doBind(tbar.AddTool(-1, images.get_rt_saveBitmap(),
                            shortHelpString="Save"), self.OnFileSave)
        tbar.AddSeparator()
        doBind(tbar.AddTool(wx.ID_CUT, images.get_rt_cutBitmap(),
                            shortHelpString="Cut"), self.ForwardEvent, self.ForwardEvent)
        doBind(tbar.AddTool(wx.ID_COPY, images.get_rt_copyBitmap(),
                            shortHelpString="Copy"), self.ForwardEvent, self.ForwardEvent)
        doBind(tbar.AddTool(wx.ID_PASTE, images.get_rt_pasteBitmap(),
                            shortHelpString="Paste"), self.ForwardEvent, self.ForwardEvent)
        tbar.AddSeparator()
        doBind(tbar.AddTool(wx.ID_UNDO, images.get_rt_undoBitmap(),
                            shortHelpString="Undo"), self.ForwardEvent, self.ForwardEvent)
        doBind(tbar.AddTool(wx.ID_REDO, images.get_rt_redoBitmap(),
                            shortHelpString="Redo"), self.ForwardEvent, self.ForwardEvent)
        tbar.AddSeparator()
        doBind(tbar.AddTool(-1, images.get_rt_boldBitmap(), isToggle=True,
                            shortHelpString="Bold"), self.OnBold, self.OnUpdateBold)
        doBind(tbar.AddTool(-1, images.get_rt_italicBitmap(), isToggle=True,
                            shortHelpString="Italic"), self.OnItalic, self.OnUpdateItalic)
        doBind(tbar.AddTool(-1, images.get_rt_underlineBitmap(), isToggle=True,
                            shortHelpString="Underline"), self.OnUnderline, self.OnUpdateUnderline)
        tbar.AddSeparator()
        doBind(tbar.AddTool(-1, images.get_rt_alignleftBitmap(), isToggle=True,
                            shortHelpString="Align Left"), self.OnAlignLeft, self.OnUpdateAlignLeft)
        doBind(tbar.AddTool(-1, images.get_rt_centreBitmap(), isToggle=True,
                            shortHelpString="Center"), self.OnAlignCenter, self.OnUpdateAlignCenter)
        doBind(tbar.AddTool(-1, images.get_rt_alignrightBitmap(), isToggle=True,
                            shortHelpString="Align Right"), self.OnAlignRight, self.OnUpdateAlignRight)
        tbar.AddSeparator()
        doBind(tbar.AddTool(-1, images.get_rt_indentlessBitmap(),
                            shortHelpString="Indent Less"), self.OnIndentLess)
        doBind(tbar.AddTool(-1, images.get_rt_indentmoreBitmap(),
                            shortHelpString="Indent More"), self.OnIndentMore)
        tbar.AddSeparator()
        doBind(tbar.AddTool(-1, images.get_rt_fontBitmap(),
                            shortHelpString="Font"), self.OnFont)
        doBind(tbar.AddTool(-1, images.get_rt_colourBitmap(),
                            shortHelpString="Font Colour"), self.OnColour)

        tbar.Realize()
        return tbar

    def __del__(self):
        pass

    def get_name(self):
        return self.editRecipeName.GetValue()

    def get_description(self, as_text=False):
        if as_text:
            return self.editRecipeDesc.GetValue()
        else:
            handler = rt.RichTextXMLHandler()
            handler.SetFlags(rt.RICHTEXT_HANDLER_INCLUDE_STYLESHEET)
            stream = StringIO()
            handler.SaveStream(self.editRecipeDesc.GetBuffer(), stream)
            return stream.getvalue()

    def get_algorythm(self, as_text=False):
        if as_text:
            return self.editRecipeAlgorythm.GetValue()
        else:
            handler = rt.RichTextXMLHandler()
            handler.SetFlags(rt.RICHTEXT_HANDLER_INCLUDE_STYLESHEET)
            stream = StringIO()
            handler.SaveStream(self.editRecipeAlgorythm.GetBuffer(), stream)
            return stream.getvalue()

    def get_time(self):
        return self.editRecipeTime.GetValue()

    def get_difficulty(self):
        return self.editRecipeDifficulty.GetValue()

    def get_groups(self):
        """returns all selected groups"""
        return [self.editRecipesGroups.GetPyData(item)
                for item in self.editRecipesGroups.GetChecked()]

    def get_ingredients(self):
        return self.editRecipeIngredients.get_ingredients()

    def set_title(self, value):
        self.editRecipeName.SetValue(value)

    def set_description(self, value):
        if not value.startswith("<?xml"):
            self.editRecipeDesc.SetValue(value)
        else:
            stream = StringIO(value)
            handler = rt.RichTextXMLHandler()
            handler.LoadStream(self.editRecipeDesc.GetBuffer(), stream)
            self.editRecipeDesc.LayoutContent()

    def set_algorythm(self, value):
        if not value.startswith("<?xml"):
            self.editRecipeAlgorythm.SetValue(value)
        else:
            stream = StringIO(value)
            handler = rt.RichTextXMLHandler()
            handler.LoadStream(self.editRecipeAlgorythm.GetBuffer(), stream)
            self.editRecipeAlgorythm.LayoutContent()

    def set_ingredients(self, ingredients):
        for i in ingredients:
            self.editRecipeIngredients.add_ingredients_row(None,
                                                           i.substance and i.substance.name,
                                                           str(i.amount),
                                                           i.unit and i.unit.name)

    def set_time(self, value):
        self.editRecipeTime.SetValue(str(value))

    def set_difficulty(self, value):
        self.editRecipeDifficulty.SetValue(str(value))

    def clear(self):
        self.editRecipeName.SetValue("")
        self.editRecipeDesc.SetValue("")
        self.editRecipeAlgorythm.SetValue("")
        self.editRecipeTime.SetValue("")
        self.editRecipeDifficulty.SetValue("")

        self.editRecipeIngredients.Clear(True)
        self.Layout()

    def addNodesToTree(self, tree, treeNode, parent,
                        normalPic, expandedPic, nameField="name",
                        childrenField="children"):
        """
        Adds a list of objects to the given tree.

        The list of objects can be nested, as long as it is
        consistent in doing so. Each object should be a dictionary
        where the given nameField contains the objects description
        and the childrenField contains a list of children.

        :param wx.TreeCtrl tree: the tree to which the objects are to be added
        :param wx.TreeItemId treeNode: the node to which objects should be
                                        added
        :param integer normalPic: the id of the pic for a normal object
        :param integer expandedPic: the id of the pic for a selected object
        :param str nameField: the field containing an objects name
        :param str childrenField: the field containing an objects children
        """
        for child in parent[childrenField]:
            node = tree.AppendItem(treeNode,
                                   unicode(child[nameField]),
                                   tc.CHECKBOX,
                                   wnd=None, image=normalPic,
                                   selImage=normalPic, data=child.id)
            if child[childrenField]:
                self.addNodesToTree(tree, node, child, normalPic,
                                    expandedPic, nameField, childrenField)

    def setup(self, groups, substance_names, unit_names, recipe=None):
        """
        Sets up the edit screen with the given recipe.

        If no recipe is given, then this simply acts as a "add new recipe"
        screen.

        :param list groups: a list of all available groups
        :param list substance_names: a list of all substance names
        :param list unit_names: a list of all unit names
        :patam models.Recipe recipe: the recipe to be edited
        """
        self.clear()
        self.substance_names = substance_names
        self.unit_names = unit_names

        self.editRecipeIngredients.set_substance_names(self.substance_names)
        self.editRecipeIngredients.set_unit_names(self.unit_names)

        groupsRoot = self.editRecipesGroups.GetRootItem()
        self.editRecipesGroups.DeleteChildren(groupsRoot)
        try:
            self.addNodesToTree(self.editRecipesGroups, groupsRoot,
                                {"children": groups},
                                self.editRecipesGroups.GetIconId(tc.FOLDER_ICON),
                                self.editRecipesGroups.GetIconId(tc.FOLDER_OPEN_ICON))
        except Exception as e:
            print "got exception:", e

        if recipe:
            self.set_recipe(recipe)

        self.editRecipesGroups.ExpandAll()

    # Virtual event handlers, overide them in your derived class
    def filterGroups(self, event):
        event.Skip()

    def selectTextFocus(self, event):
        event.Skip()
        self.rtc = event.GetEventObject()
        print self.rtc.GetValue()

    def saveRecipe(self, event):
        event.Skip()
        if self.save_action:
            self.save_action(self)

    def set_save_action(self, action):
        self.save_action = action

    def set_recipe(self, recipe):
        self.recipeId = recipe.id
        self.set_title(recipe.title)
        self.set_description(recipe.title)
        self.set_algorythm(recipe.algorythm)
        self.set_ingredients(recipe.ingredients)
        self.set_time(recipe.time)
        self.set_difficulty(recipe.difficulty)
        self.editRecipesGroups.CheckById({group.id for group in recipe.groups})

    def get_recipe_id(self):
        try:
            return self.recipeId
        except AttributeError as e:
            logging.error(e)
            return None
