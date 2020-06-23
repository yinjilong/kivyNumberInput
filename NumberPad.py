# provide a number pad to accept number input
# with calculator functions

from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

import functools
import re

class NumberPad(Popup):

    def __init__(self,init_value='',size=None,**kwargs):
        super(NumberPad,self).__init__(**kwargs)

        self._vbox = BoxLayout(orientation='vertical')
        self._vbox.padding=(8,8,8,8)

        self._hbox1=BoxLayout(orientation='horizontal',size_hint_y=0.2)
        # self._labValue=Label(text='Value',size_hint_x=0.2)
        self._inpValue=TextInput(readonly=True,multiline=False,size_hint_x=0.8)
        # self._hbox1.add_widget(self._labValue)
        self._hbox1.add_widget(self._inpValue)
        self._vbox.add_widget(self._hbox1)


        btns=[ ['7','8','9','+','DEL'],
               ['4','5','6','-','AC'],
               ['1','2','3','*','='],
               ['0','e','.','/','ENT']]
        self._grid=GridLayout(rows=4,cols=5)
        self._btns={}
        for one_row in btns:
            for b in one_row:
                self._btns[b]=Button(text=b)
                self._grid.add_widget(self._btns[b])
                if b =='1' or b =='2' or b=='3' or b=='4' or b=='5' or b=='6' or b=='7' or b=='8' or b=='9' or b=='0' or b=='e' or b=='.':
                    self._btns[b].bind(on_release=functools.partial(self.set_value,b))
                elif b=='+' or b=='-' or b=='*' or b=='/':
                    self._btns[b].bind(on_release=functools.partial(self.set_operation,b))
                elif b=='DEL':
                    self._btns[b].bind(on_release=self.delete)
                elif b=='AC':
                    self._btns[b].bind(on_release=self.clear)
                elif b=='=':
                    self._btns[b].bind(on_release=self.equal)
                elif b=='ENT':
                    self._btns[b].bind(on_release=self.accept)

        self._vbox.add_widget(self._grid)

        if size is None:
            self.size_hint = (1,1)
        else:
            self.size_hint = (None, None)

        if size is None:
            self.size=(400,400)
        else:
            self.size=tuple(size)

        Window.bind(on_key_down=self.key_action)

        self.content=self._vbox
        self.auto_dismiss = True
        self.title="Enter a number"
        self._response = None

        self._value1 = None
        self._value2 = None
        self._operation = None
        self._last = None
        self._callback = None

        if init_value:
            self._inpValue.text = init_value
            self._init_value=init_value

        # check validity of the input
        self._regex=re.compile('^[-+]?([0-9]+(\.[0-9]*)?|\.[0-9]+)([eE][-+]?[0-9]?)?$')

    def key_action(self,*args):
        keys={41:'ESC',42:'DEL',84:'/',85:'*',86:'-',87:'+',88:'RETURN',89:'1',90:'2',91:'3',92:'4',93:'5',94:'6',95:'7',96:'8',97:'9',98:'0',99:'.'}
        keyboard,keycode,text=args[0:3]
        keycode=args[1]
        text=args[2]
        if text in keys:
            b=keys[text]
        else:
            return
        if b == '1' or b == '2' or b == '3' or b == '4' or b == '5' or b == '6' or b == '7' or b == '8' or b == '9' or b == '0' or b == 'e' or b == '.':
            self.set_value(b)
        elif b == '+' or b == '-' or b == '*' or b == '/':
            self.set_operation(b)
        elif b=='RETURN':
            self.equal()
        elif b=='DEL':
            self.delete()
        elif b=='ESC':
            self.dismiss()

    def set_callback(self,foo):
        self._callback=foo

    def accept(self,*kwargs):
        if self._regex.match(self._inpValue.text):
            self.result=self._inpValue.text
            self.dismiss()
            self._callback()

    def set_value(self,b,*kwargs):
        if self._last and self._last in '+-*/':
                self._inpValue.text = ''

        if not self._regex.match(self._inpValue.text+b):
            print('not match float')
        else:
            self._inpValue.text += b
            self._last=b
        pass

    def set_operation(self,b,*kwargs):
        self._operation = b
        if self.checkOP():
            self._last = b
        pass

    def delete(self,*kwargs):
        if not self._regex.match(self._inpValue.text):
            self._inpValue.text=''
        else:
            tmp=len(self._inpValue.text)
            self._inpValue.text = self._inpValue.text[:tmp-1]
        pass

    def clear(self,*kwargs):
        self._operation=''
        self._value1=None
        self._value2=None
        self._inpValue.text=''
        pass

    def checkOP(self):
        try:
            if self._value1 == None:
                self._value1 = float(self._inpValue.text)
            elif self._operation != None:
                self.equal()
            return True
        except:
            return False

    def equal(self,*kwargs):
        if self._value1 != None and self._operation != None:
            result = None
            self._value2 = float(self._inpValue.text)
            try:
                if self._operation == "+":
                    result = self._value1 + self._value2
                elif self._operation == "-":
                    result = self._value1 - self._value2
                elif self._operation == "*":
                    result = self._value1 * self._value2
                elif self._operation == "/":
                    result = self._value1 / self._value2
                self._inpValue.text = str(result)
                # self._inpValue.text = '%f'%(result)
                self._value1 = None  # result
                self._value2 = None
                self._operation = None
            except:
                self._value1 = None  # result
                self._value2 = None
                self._operation = None
                self._inpValue.text='ERROR'
        pass

