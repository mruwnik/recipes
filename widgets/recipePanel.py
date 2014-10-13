#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cStringIO import StringIO

import wx
import wx.richtext as rt

import i18n
_ = i18n.language.ugettext


class RecipePanel (wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY,
                           pos=wx.DefaultPosition, size=wx.DefaultSize,
                           style=wx.TAB_TRAVERSAL)

        container = wx.BoxSizer(wx.VERTICAL)
        self.container = container

        self.title = wx.StaticText(self, wx.ID_ANY, wx.EmptyString,
                                   wx.DefaultPosition, wx.DefaultSize,
                                   wx.ALIGN_CENTRE)
        self.title.Wrap(-1)
        self.title.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(),
                                   70, 90, 92,
                                   False, wx.EmptyString))
        container.Add(self.title, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        self.description = rt.RichTextCtrl(self, style=wx.TE_READONLY
                                           | wx.NO_BORDER)
        container.Add(self.description, 1, wx.ALL | wx.EXPAND, 5)

        self.algorythm = rt.RichTextCtrl(self, style=wx.VSCROLL | wx.HSCROLL
                                         | wx.TE_READONLY | wx.NO_BORDER)
        container.Add(self.algorythm, 3, wx.ALL | wx.EXPAND, 5)

        self.ingredients = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString,
                                       wx.DefaultPosition, wx.DefaultSize,
                                       wx.TE_MULTILINE | wx.NO_BORDER)
        container.Add(self.ingredients, 0, wx.ALL | wx.EXPAND, 5)

        extra_info = wx.GridSizer(6, 2, 0, 0)

        self.groups_label = wx.StaticText(self, wx.ID_ANY,
                                          _(u"groups:"),
                                          wx.DefaultPosition,
                                          wx.DefaultSize, 0)
        self.groups_label.Wrap(-1)
        extra_info.Add(self.groups_label, 0, wx.ALL, 5)

        self.groups = wx.StaticText(self, wx.ID_ANY, wx.EmptyString,
                                    wx.DefaultPosition,
                                    wx.DefaultSize, 0)
        self.groups.Wrap(-1)
        extra_info.Add(self.groups, 0, wx.ALL, 5)

        self.cost_label = wx.StaticText(self, wx.ID_ANY, _(u"cost:"),
                                        wx.DefaultPosition,
                                        wx.DefaultSize, 0)
        self.cost_label.Wrap(-1)
        extra_info.Add(self.cost_label, 0, wx.ALL, 5)

        self.cost = wx.StaticText(self, wx.ID_ANY, wx.EmptyString,
                                  wx.DefaultPosition,
                                  wx.DefaultSize, 0)
        self.cost.Wrap(-1)
        extra_info.Add(self.cost, 0, wx.ALL, 5)

        self.time_label = wx.StaticText(self, wx.ID_ANY, _(u"time:"),
                                        wx.DefaultPosition,
                                        wx.DefaultSize, 0)
        self.time_label.Wrap(-1)
        extra_info.Add(self.time_label, 0, wx.ALL, 5)

        self.time = wx.StaticText(self, wx.ID_ANY, wx.EmptyString,
                                  wx.DefaultPosition, wx.DefaultSize, 0)
        self.time.Wrap(-1)
        extra_info.Add(self.time, 0, wx.ALL, 5)

        self.difficulty_label = wx.StaticText(self, wx.ID_ANY,
                                              _(u"difficulty:"),
                                              wx.DefaultPosition,
                                              wx.DefaultSize, 0)
        self.difficulty_label.Wrap(-1)
        extra_info.Add(self.difficulty_label, 0, wx.ALL, 5)

        self.difficulty = wx.StaticText(self, wx.ID_ANY, wx.EmptyString,
                                        wx.DefaultPosition, wx.DefaultSize, 0)
        self.difficulty.Wrap(-1)
        extra_info.Add(self.difficulty, 0, wx.ALL, 5)

        container.Add(extra_info, 0, wx.EXPAND, 5)

        self.SetSizerAndFit(container)
        self.Layout()

    def __del__(self):
        pass

    def set_title(self, text):
        self.title.SetLabel(text)

    def set_description(self, text, as_text=False):
        if as_text:
            self.description.SetValue(text)
        else:
            stream = StringIO(text)
            handler = rt.RichTextXMLHandler()
            handler.LoadStream(self.description.GetBuffer(), stream)
            self.description.LayoutContent()

    def set_algorythm(self, text, as_text=False):
        if as_text:
            self.algorythm.SetValue(text)
        else:
            stream = StringIO(text)
            handler = rt.RichTextXMLHandler()
            handler.LoadStream(self.algorythm.GetBuffer(), stream)
            self.algorythm.LayoutContent()

    def set_ingredients(self, text):
        self.ingredients.SetValue(text)

    def set_groups(self, text):
        self.groups.SetLabel(text)

    def set_time(self, text):
        self.time.SetLabel(str(text))

    def set_difficulty(self, text):
        self.difficulty.SetLabel(str(text))

    def set_cost(self, text):
        self.cost.SetLabel(text)

