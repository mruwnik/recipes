import wx
import wx.lib.customtreectrl

RADIO_BUTTON = 2
CHECKBOX = 1
NORMAL = 0

FOLDER_ICON = 1
FOLDER_OPEN_ICON = 2
FILE_ICON = 3


class ControlsTreeCtrl(wx.lib.customtreectrl.CustomTreeCtrl):
    """A tree control with checkboxes next to each item."""

    def __init__(self, name, *args, **kwargs):
        super(ControlsTreeCtrl, self).__init__(*args, **kwargs)

#        self.Bind(wx.lib.customtreectrl.EVT_TREE_ITEM_CHECKED,
#                  self.OnItemChecked)

        self.Bind(wx.EVT_TREE_SEL_CHANGED,
                  self.ItemSelected)
        self.AddRoot(name)

        isz = (16, 16)
        il = wx.ImageList(isz[0], isz[1])
        self.icons = {
            FOLDER_ICON: il.Add(wx.ArtProvider_GetBitmap(
                                                        wx.ART_FOLDER,
                                                        wx.ART_OTHER, isz)),
            FOLDER_OPEN_ICON: il.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN,
                                                              wx.ART_OTHER, isz)),
            FILE_ICON: il.Add(wx.ArtProvider_GetBitmap(
                                                        wx.ART_NORMAL_FILE,
                                                        wx.ART_OTHER, isz))}
        self.SetImageList(il)

    def GetIconId(self, icon):
        return self.icons[icon]

    def ItemSelected(self, event):
        """Checks a selected item."""
        item = event.GetItem()
        item.Check(not item.IsChecked())
        self.RefreshLine(item)

    def GetChecked(self):
        """Returns a list of checked items."""
        def FillArray(item, array):
            if item.IsChecked():
                array.append(item)

            if item.HasChildren():
                for child in item.GetChildren():
                    array = FillArray(child, array)

            return array

        array = []
        idRoot = self.GetRootItem()
        if idRoot:
            array = FillArray(idRoot, array)

        return array


