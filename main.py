
import wx
import os
from subprocess import run
from subprocess import Popen, PIPE
import _thread


class VariableClass(object):
    def __init__(self, *args):
      print("init")

    # 写变量
    def write_variable(self, key, value):
      #devnull = open(os.devnull, 'wb')
      #run('setx '+key+' "'+value+'"', shell=True,stdout=PIPE, stderr=PIPE, stdin=devnull)
      run('setx '+key+' "'+value+'"', shell=True)

    # 读变量
    def read_variable(self, key):
      return os.getenv(key)
    
    def del_variable(self,key):
        # REG delete HKCU\Environment /F /V key
        run('REG delete HKCU\Environment /F /V '+key, shell=True)

class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='系统工具箱', size=(
            529, 80), name='frame', style=541072384)
        self.guix = wx.Panel(self)
        self.Centre()
        self.hr = wx.TextCtrl(self.guix, size=(506, 5), pos=(
            3, 31), value='', name='text', style=0)
        self.hr.Disable()
        self.hr.SetOwnBackgroundColour((0, 0, 0, 255))
        self.porxy_title = wx.StaticText(self.guix, size=(100, 14), pos=(
            1, 9), label='终端代理(http)：', name='staticText', style=2321)
        self.porxy_edit = wx.TextCtrl(self.guix, size=(
            172, 23), pos=(92, 5), value='', name='text', style=0)
        self.clear_button = wx.Button(self.guix, size=(
            61, 26), pos=(445, 4), label='取消代理', name='button')
        self.clear_button.Bind(wx.EVT_BUTTON, self.clear_button_click)
        self.arr_button = wx.Button(self.guix, size=(
            67, 26), pos=(373, 4), label='应用代理', name='button')
        self.arr_button.Bind(wx.EVT_BUTTON, self.arr_button_click)
        self.def_button = wx.Button(self.guix, size=(
            52, 26), pos=(318, 4), label='默认值', name='button')
        self.def_button.Bind(wx.EVT_BUTTON, self.def_button_click)
        self.porxy_staust = wx.StaticText(self.guix, size=(38, 20), pos=(
            272, 9), label='未使用', name='staticText', style=2321)
        self.porxy_staust.SetForegroundColour((255, 0, 0, 255))

        # 读系统变量 HTTP_PORXY
        try:
          self.variable = VariableClass()
          porxy = self.variable.read_variable('HTTP_PORXY')
          porxys = self.variable.read_variable('HTTPS_PORXY')
          if len(porxy) > 7:
            self.porxy_edit.SetValue(porxy)
            self.porxy_staust.SetForegroundColour((25, 161, 95))
            self.porxy_staust.SetLabel('已使用')

          if len(porxys) > 7:
            self.porxy_edit.SetValue(porxys)
            self.porxy_staust.SetForegroundColour((25, 161, 95))
            self.porxy_staust.SetLabel('已使用')
        except:
          pass


    def clear_button_click(self, event):
        print('取消代理')
        self.porxy_staust.SetForegroundColour((255, 0, 0, 255))
        self.porxy_staust.SetLabel('关闭中')
        _thread.start_new_thread(
            self.variable.del_variable, ('HTTP_PORXY', ))
        _thread.start_new_thread(
            self.variable.del_variable, ('HTTPS_PORXY', ))
        self.porxy_staust.SetLabel('未使用')  

    def arr_button_click(self, event):
        print('应用代理')
        porxy_title_value = self.porxy_edit.GetValue()
        print(porxy_title_value)
        self.porxy_staust.SetForegroundColour((25, 161, 95))
        self.porxy_staust.SetLabel('启用中')
        _thread.start_new_thread(
            self.variable.write_variable, ('HTTP_PORXY', porxy_title_value, ))
        _thread.start_new_thread(
            self.variable.write_variable, ('HTTPS_PORXY', porxy_title_value, ))
        self.porxy_staust.SetLabel('已使用')
        

    def def_button_click(self, event):
        print('默认代理')
        self.porxy_edit.SetValue('http://127.0.0.1:10809')


class myApp(wx.App):
    def OnInit(self):
        self.frame = Frame()
        self.frame.Show(True)
        return True


if __name__ == '__main__':
  app = myApp()
  app.MainLoop()
  vc = VariableClass()
