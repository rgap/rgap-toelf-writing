import wx
import wx.richtext as rt
from wx import adv


class MultiText(rt.RichTextCtrl):
    def __init__(self, *args, **kwargs):

        rt.RichTextCtrl.__init__(self, *args, **kwargs)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.EVT_TOOL, self.Copy)

    def OnKeyDown(self, event):
        code = event.GetKeyCode()
        print(code)

        # If TAB is pressed... --> this works
        if code == wx.WXK_TAB:
            return
        # If Ctrl+O is pressed... --> this workd
        if event.ControlDown() and code == ord('O'):
            print("CLTR + O")
            return
        # If Ctrl+A is pressed... --> this doesn't
        if event.ControlDown() and code == ord('A'):
            print("CLTR + A")
            return
        event.Skip()

    def Copy(self, event):  # --> this doesn't work
        print("Copy called.")
        # super().Copy()


class MainFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, size=(500, 600), style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        self.multiText = MultiText(self, size=(500, 600), style=wx.TE_MULTILINE|wx.BORDER)


if __name__ == '__main__':
    # print(wx.version())
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
