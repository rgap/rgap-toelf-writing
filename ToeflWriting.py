#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import wx.richtext as rt
from wx import adv
import time


class WritingPanel(wx.Panel):

    def __init__(self, parent, *args, **kwargs):

        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        prompt = wx.StaticText(self, size=(self.Size[0]/2-10, -1), label="You must finish your answer in 20/30 minutes.", style=wx.ALIGN_LEFT)
        prompt.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.BOLD))

        # Time
        self.time = 1800
        st = time.strftime("%H:%M:%S", time.gmtime(self.time))
        self.timeleft = wx.StaticText(self, size=(self.Size[0]/2-20, -1), label="TIME LEFT: " + st, style=wx.ALIGN_RIGHT)
        self.timeleft.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.BOLD))

        # Layout
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(prompt, flag=wx.LEFT, border=5)
        hsizer.Add(self.timeleft, flag=wx.RIGHT, border=5)

        vsizer = wx.BoxSizer(wx.VERTICAL)

        # Text editor
        self.multiText = rt.RichTextCtrl(self, 1, "",
                                         size=(self.Size[0], self.Size[1]), style=wx.TE_MULTILINE|wx.BORDER)
        self.multiText.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        self.multiText.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.multiText.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        self.multiText.Bind(wx.EVT_TOOL, self.ShortcutHandler)
        self.multiText.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)
        self.multiText.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)


        # Counter
        self.word_counter = wx.StaticText(self, size=(self.Size[0]/2-70, -1), label="Words: 0", style=wx.ALIGN_RIGHT)
        self.word_counter.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.BOLD))

        # Layout
        copy_button = wx.Button(self, -1, "Copy", style=wx.BU_EXACTFIT)
        paste_button = wx.Button(self, -1, "Paste", style=wx.BU_EXACTFIT)
        cut_button = wx.Button(self, -1, "Cut", style=wx.BU_EXACTFIT)
        cut_button.Bind(wx.EVT_BUTTON, self.OnCut)
        copy_button.Bind(wx.EVT_BUTTON, self.OnCopy)
        paste_button.Bind(wx.EVT_BUTTON, self.OnPaste)

        undo_button = wx.Button(self, -1, "Undo", style=wx.BU_EXACTFIT)
        redo_button = wx.Button(self, -1, "Redo", style=wx.BU_EXACTFIT)
        undo_button.Bind(wx.EVT_BUTTON, self.OnUndo)
        redo_button.Bind(wx.EVT_BUTTON, self.OnRedo)

        sec_hsizer = wx.BoxSizer(wx.HORIZONTAL)
        sec_hsizer.Add(copy_button, flag=wx.RIGHT, border=5)
        sec_hsizer.Add(cut_button, flag=wx.RIGHT, border=5)
        sec_hsizer.Add(paste_button, flag=wx.RIGHT, border=5)
        sec_hsizer.Add(undo_button, flag=wx.RIGHT, border=5)
        sec_hsizer.Add(redo_button, flag=wx.RIGHT, border=5)
        sec_hsizer.Add(self.word_counter, flag=wx.LEFT, border=5)

        vsizer.Add(hsizer,
                   flag=wx.EXPAND | wx.ALL | wx.ALIGN_TOP, border=5)
        vsizer.Add(sec_hsizer,
                   flag=wx.EXPAND | wx.ALL | wx.ALIGN_TOP, border=5)
        vsizer.Add(self.multiText,
                   flag=wx.EXPAND | wx.ALL | wx.ALIGN_TOP, border=5)

        prompt.Wrap(self.Size[0]/2)
        self.timeleft.Wrap(self.Size[0]/2)

        self.SetSizer(vsizer)

        # Timer
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.CountdownUpdate, self.timer)
        self.timer.Start(1000)

    def OnRightClick(self, event):
        pass

    def ShortcutHandler(self, event):
        pass

    def UpdateCounter(self):
        text = self.multiText.GetValue()
        n_words = str(len(text.split()))
        self.word_counter.SetLabel("Words: " + n_words)

    def copyAll(self, event):
        self.multiText.SelectAll()
        self.multiText.Copy()

    def clearAll(self, event):
        self.multiText.SelectAll()
        self.multiText.Clear()
        self.multiText.SetCaretPosition(-1)

    def OnUndo(self, event):
        if self.multiText.CanUndo():
            self.multiText.Undo()
        self.UpdateCounter()

    def OnRedo(self, event):
        if self.multiText.CanRedo():
            self.multiText.Redo()
        self.UpdateCounter()

    def OnCut(self, event):
        self.multiText.Cut()
        self.UpdateCounter()

    def OnCopy(self, event):
        if self.multiText.CanCopy():
            self.multiText.Copy()

    def OnPaste(self, event):
        if self.multiText.CanPaste():
            self.multiText.Paste()
        self.UpdateCounter()

    def OnKeyUp(self, event):
        self.UpdateCounter()

    def OnKeyDown(self, event):
        code = event.GetKeyCode()
        # print(code)
        # If TAB is pressed...
        if code == wx.WXK_TAB:
            return
        # If jumping is pressed...
        if (event.RawControlDown() or event.ControlDown() or event.AltDown()) \
           and (code == wx.WXK_LEFT or code == wx.WXK_RIGHT):
            return

        event.Skip()

    # ----------------------------------------------------------------------
    def CountdownUpdate(self, evt):
        self.tm_min = self.time / 60
        self.tm_sec = self.time % 60
        st = "TIME LEFT: 00:%02d:%02d" % (self.tm_min, self.tm_sec)
        self.timeleft.SetLabel(st)
        self.time -= 1
        if self.time < 0:
            self.timer.Stop()
            # Save the input in self.multiText as a file

    def restartTimer(self, time):
        self.time = time
        if not self.timer.IsRunning():
            self.timer.Start(1000)


class MainFrame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, -1, title=title, size=(500, 600), style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        self.Center()
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        m_exit = fileMenu.Append(wx.ID_EXIT,
                             "E&xit\tAlt-X", "Close window and exit program.")
        self.Bind(wx.EVT_MENU, self.OnClose, m_exit)
        menuBar.Append(fileMenu, "&File")
        copyAll_button = fileMenu.Append(wx.ID_COPY, '&Copy All')
        restart20_button = fileMenu.Append(wx.ID_ANY, '&Restart to 20 min')
        restart30_button = fileMenu.Append(wx.ID_ANY, '&Restart to 30 min')
        clearAll_button = fileMenu.Append(wx.ID_CLEAR, '&Clear')

        self.Bind(wx.EVT_MENU, self.OnRestart20, restart20_button)
        self.Bind(wx.EVT_MENU, self.OnRestart30, restart30_button)
        self.Bind(wx.EVT_MENU, self.copyAll, copyAll_button)
        self.Bind(wx.EVT_MENU, self.clearAll, clearAll_button)

        aboutMenu = wx.Menu()
        m_about = aboutMenu.Append(wx.ID_ABOUT,
                                   "&About", "Information about this program")
        self.Bind(wx.EVT_MENU, self.OnAbout, m_about)
        menuBar.Append(aboutMenu, "&Help")
        self.SetMenuBar(menuBar)

        # self.statusbar = self.CreateStatusBar()
        self.ShowWritingPanel(self.Size)

    def copyAll(self, e):
        self.panel.copyAll(e)

    def clearAll(self, e):
        dlg = wx.MessageDialog(self,
                               "Do you really want to delete all?",
                               "Confirm Exit",
                               wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.panel.clearAll(e)

    def OnRestart20(self, e):
        self.panel.restartTimer(1200)

    def OnRestart30(self, e):
        self.panel.restartTimer(1800)

    def ShowWritingPanel(self, size):
        self.panel = WritingPanel(self, size=size)
        self.panel.Layout()

    def OnClose(self, event):
        dlg = wx.MessageDialog(self,
                               "Do you really want to close this application?",
                               "Confirm Exit",
                               wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()

    def OnAbout(self, event):
        # First we create and fill the info object
        info = adv.AboutDialogInfo()
        info.Name = "TOEFL Writing Simulator"
        info.Version = "1.1"
        info.Copyright = "(C) 2017 Rel Guzman"
        info.WebSite = ("https://www.facebook.com/rel.guzman", "Website")
        # Then we call wx.AboutBox giving it that info object
        wx.adv.AboutBox(info)

if __name__ == '__main__':
    # print(wx.version())
    app = wx.App()
    frame = MainFrame("TOEFL Writing")
    frame.Show()
    app.MainLoop()
