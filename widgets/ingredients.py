#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ingredients.py: a widget to add ingredients"""

from collections import OrderedDict

import wx
from TextCtrlAutoComplete import TextCtrlAutoComplete

import i18n
_ = i18n.language.ugettext


class FindIngredients(TextCtrlAutoComplete):
    """Allows to autocomplete a list of items seperated by ';'."""
    def __init__(self, *args, **kwargs):
        if 'choices' not in kwargs and 'multiChoices' not in kwargs:
            kwargs['choices'] = ['']
        super(FindIngredients, self).__init__(*args, **kwargs)
        self._itemsCallback = kwargs.get('itemsCallback')

    def onEnteredText(self, event):
        """Shows autocompletion for the word in which the cursor is.

        The text that precedes the current text position, up to any
        found ';', is autocompleted.
        """

        text = event.GetString()
        start = text.rfind(";", 0, self.GetInsertionPoint()) + 1

        event = wx.CommandEvent()
        event.SetString(text[start:self.GetInsertionPoint() + 1].strip())

        super(FindIngredients, self).onEnteredText(event)
        event.Skip()

    def onKeyDown(self, event):
        """Called when a key is pressed.

        :param wx.KeyEvent event: the raised event
        """
        super(FindIngredients, self).onKeyDown(event)
        event.Skip()

    def _setValueFromSelected(self):
        """Autocompletes the word in which the cursor is.

        Called when a word from the autocomplete list is selected. The text
        that is surrounding the current text position, up to any found ';',
        is replaced with the selected word. After being selected, all
        duplicates are removed and the list is tidied up
        """
        text = self.GetValue()
        start = text.rfind(";", 0, self.GetInsertionPoint())
        end = text.find(";", self.GetInsertionPoint())

        super(FindIngredients, self)._setValueFromSelected()
        value = ''
        if start >= 0:
            value = text[:start].strip() + ";"
        value += self.GetValue()
        if end >= 0:
            value += text[end:]

        words = list(OrderedDict
                     .fromkeys(filter(None,
                                      [w.strip() for w in value.split(";")])))
        if self._itemsCallback:
            self._itemsCallback(words)

        self.SetValue("; ".join(words) + "; ")
        self.SetInsertionPointEnd()

    def GetItems(self):
        """Get a list of all entered values

        :return list: a list of all items
        """
        if not self.GetValue():
            return []
        return list(OrderedDict
                    .fromkeys(filter(None,
                                     [w.strip() for w in
                                      self.GetValue().split(";")])))

    def SetItemsCallback(self, fc=None):
        """Set a callback for when an item is completed

        :param function(list) fc: the callback
        """
        self._itemsCallback = fc


class AddIngredients(wx.Panel):

    def __init__(self, parent, substance_names=[], unit_names=[],
                 **therest):

        wx.Panel.__init__(self, parent, **therest)

        self.substance_names = substance_names
        self.unit_names = unit_names

        self.edit_recipe_ingredients_container = wx.BoxSizer(wx.VERTICAL)

        self.SetSizer(self.edit_recipe_ingredients_container)

    def Clear(self, flag):
        """Remove all ingredients"""
        self.edit_recipe_ingredients_container.Clear(flag)

    def set_substance_names(self, names):
        """Set the substance names list

        (used for autocompletion)

        """
        self.substance_names = names

    def set_unit_names(self, names):
        """Set the unit names list

        (used for autocompletion)

        """
        self.unit_names = names

    def add_ingredients_row(self, event, nameVal="", amountVal="", unitVal=""):
        """Add an ingredient row.

        The ingredient row is fully connected with autocompletion and a
        'remove' button.

        """
        if event:
            event.Skip()

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        name = TextCtrlAutoComplete(self,
                                    choices=self.substance_names,
                                    selectCallback=self.selectCallback,
                                    name=_("name"))

        name.SetEntryCallback(self.find_ingredients)
        name.SetMatchFunction(self.match_function)
        if nameVal:
            name.SetValue(nameVal)

        sizer.Add(name, 3, wx.ALL, 5)

        amount_desc = wx.StaticText(self, wx.ID_ANY, _(u"amount"),
                                    wx.DefaultPosition, wx.DefaultSize, 0)
        amount_desc.Wrap(-1)
        sizer.Add(amount_desc, 0, wx.ALL, 5)

        ingredients_amount = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString,
                                         wx.DefaultPosition, wx.DefaultSize,
                                         0, name=_("amount"))
        sizer.Add(ingredients_amount, 1, wx.ALL, 5)
        if amountVal:
            ingredients_amount.SetValue(amountVal)

        unit_desc = wx.StaticText(self, wx.ID_ANY, _(u"unit"),
                                  wx.DefaultPosition, wx.DefaultSize, 0)
        unit_desc.Wrap(-1)
        sizer.Add(unit_desc, 0, wx.ALL, 5)

        unit = TextCtrlAutoComplete(self,
                                    choices=self.unit_names,
                                    selectCallback=self.selectCallback,
                                    name=_("unit"))
        unit.SetEntryCallback(self.find_units)
        unit.SetMatchFunction(self.match_function)
        if unitVal:
            unit.SetValue(unitVal)

        sizer.Add(unit, 1, wx.ALL, 5)

        remove_ingredient = wx.Button(self, wx.ID_ANY, _(u"remove ingredient"),
                                      wx.DefaultPosition, wx.DefaultSize, 0)
        sizer.Add(remove_ingredient, 0, wx.ALL, 5)

        self.edit_recipe_ingredients_container.Add(sizer, 0, wx.EXPAND, 5)
        self.GetParent().GetParent().Layout()

        remove_ingredient.Bind(wx.EVT_BUTTON, self.remove_ingredient)

    def find_ingredients(self, ctrl):
        """Set the autocomplete list for substances on the basis of the given
        string"""
        text = ctrl.GetValue().lower()

        current_choices = ctrl.GetChoices()
        choices = [choice for choice in self.substance_names
                   if self.match_function(text, choice)]
        if choices != current_choices:
            ctrl.SetChoices(choices)

    def match_function(self, text, choice):
        t = text.lower()
        c = choice.lower()
        return c.startswith(t)

    def selectCallback(self, values):
        """ Simply function that receive the row values when the
            user select an item
        """
#        print "Select Callback called...:",  values
        pass

    def find_units(self, ctrl):
        """Search the units list for the currently input string

        (this is used for autocompletion)

        """
        text = ctrl.GetValue().lower()

        current_choices = ctrl.GetChoices()
        choices = [choice for choice in self.unit_names
                   if self.match_function(text, choice)]
        if choices != current_choices:
            ctrl.SetChoices(choices)

    def signal_error(self, elem, ingredients):
        """Display an error message for the given ingredient"""
        #TODO: show an error message for this elem
        pass

    def get_ingredient(self, elem, validate=True):
        """Extract the ingredient's information

        Returns it as the following tuple: (name, amount, unit). If all fields
        are empty, None is returned. If validation is selected and the name is
        empty, False is returned and an error is displayed

        """
        for child in elem.GetChildren():
            if child.IsWindow():
                item = child.GetWindow()
                if item.GetName() == _("name"):
                    name = item.GetValue()
                elif item.GetName() == _("unit"):
                    unit = item.GetValue()
                elif item.GetName() == _("amount"):
                    amount = item.GetValue()
        if not name and not amount and not unit:
            return None
        if name or not validate:
            if not unit:
                unit = None
            if not amount:
                amount = 1
            return (name, amount, unit)
        else:
            self.signal_error(elem, (name, amount, unit))
            return False

    def get_ingredients(self, validate=True):
        """Return a list of ingredients.

        Each ingredient is a tuple
        (name, amount, unit). if validation is selected and an error is found,
        then None is returned

        """
        errors = False
        ingredients = []
        names = set()
        for child in self.edit_recipe_ingredients_container.GetChildren():
            if child.IsSizer():
                ingredient = self.get_ingredient(child.GetSizer(), validate)
                if ingredient and ingredient[0] not in names:
                    ingredients.append(ingredient)
                    names.add(ingredient[0])
                elif ingredient is False:
                    errors = True
        if validate and errors:
            return None
        else:
            return ingredients

    def remove_ingredient(self, event):
        """Remove the given ingredient from the view."""
        sizer = event.GetEventObject().GetContainingSizer()
        self.edit_recipe_ingredients_container.RemoveSizer(sizer)
        self.GetParent().Layout()
