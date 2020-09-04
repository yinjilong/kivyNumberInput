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

    _font_size=12
    _err_msgs=["EVAL ERROR","OUT OF RANGE"]

    def __init__(self,init_value='',size=None, range=(None,None),**kwargs):
        super(NumberPad,self).__init__(**kwargs)

        if size is None:
            self.size_hint = (1,1)
        else:
            self.size_hint = (None, None)

        if size is None:
            self.size=(200,200)
            self._font_size = 16
        else:
            self.size=tuple(size)
            self._font_size = self.size[0]/15
        if range is None:
            self.range = (None,None)
        else:
            self.range = range

        self._vbox = BoxLayout(orientation='vertical')
        self._vbox.padding=(8,8,8,8)

        self._hbox1=BoxLayout(orientation='horizontal',size_hint_y=0.2)
        # self._labValue=Label(text='Value',size_hint_x=0.2)
        self._inpValue=TextInput(readonly=True,multiline=False,size_hint_x=0.8,font_size=self._font_size)
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
                self._btns[b]=Button(text=b,font_size=self._font_size)
                self._grid.add_widget(self._btns[b])
                if b in ['0','1','2','3','4','5','6','7','8','9','0','e','.','+','-','*','/']:
                    self._btns[b].bind(on_release=functools.partial(self.set_value,b))
                elif b=='DEL':
                    self._btns[b].bind(on_release=self.delete)
                elif b=='AC':
                    self._btns[b].bind(on_release=self.clear)
                elif b=='=':
                    self._btns[b].bind(on_release=self.equal)
                elif b=='ENT':
                    self._btns[b].bind(on_release=self.accept)

        self._vbox.add_widget(self._grid)

        Window.bind(on_key_down=self.key_action)

        self.content=self._vbox
        self.auto_dismiss = True
        self.title="Enter a number"
        self._response = None

        self._value1 = None
        self._value2 = None
        self._operation = None
        self._last = None
        self._callback_close = None
        self._callback_escape = None

        if init_value:
            self._inpValue.text = init_value
            self._init_value=init_value

        # check validity of the input
        self._regex=re.compile('^[-+]?([0-9]+(\.[0-9]*)?|\.[0-9]+)([eE][-+]?[0-9]?)?$')

    def key_action(self,*args):
        keys={41:'ESC',42:'DEL',84:'/',85:'*',86:'-',87:'+',88:'RETURN',89:'1',90:'2',91:'3',92:'4',93:'5',94:'6',95:'7',96:'8',97:'9',98:'0',99:'.'}
        # print('got a key',*args)
        keyboard=args[0]
        keycode=args[1]
        text=args[2]
        # print(keyboard, keycode, text,type(text))
        if text in keys:
            b=keys[text]
        else:
            return
        if b in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'e','.','+','-','*','/']:
            self.set_value(b)
        elif b=='RETURN':
            self.equal()
        elif b=='DEL':
            self.delete()
        elif b=='ESC':
            self.dismiss()
            self._callback_escape()
            # self.dismiss()

    def set_callback(self,foo_close,foo_escape):
        self._callback_close=foo_close
        self._callback_escape=foo_escape

    def accept(self,*kwargs):
        self.equal()
        if self._regex.match(self._inpValue.text):
            bRange = True
            if self.range[0] is not None and self.range[0] > float(self._inpValue.text):
                bRange = False
            if self.range[1] is not None and  self.range[1] < float(self._inpValue.text):
                bRange = False
            if bRange:
                self.result=self._inpValue.text
                self.dismiss()
                self._callback_close()
            else:
                self._inpValue.text = self._err_msgs[1]

    def set_value(self,b,*kwargs):
        if self._inpValue.text in self._err_msgs:
            self._inpValue.text = ""

        self._inpValue.text += b

    def delete(self,*kwargs):
        if self._inpValue.text in self._err_msgs:
            self._inpValue.text = ""
            return

        if not self._regex.match(self._inpValue.text):
            self._inpValue.text=''
        else:
            tmp=len(self._inpValue.text)
            self._inpValue.text = self._inpValue.text[:tmp-1]
        pass

    def clear(self,*kwargs):
        self._inpValue.text=''
        pass

    def equal(self,*kwargs):
        calc_entry =  self._inpValue.text
        try:
            ans = str(eval(calc_entry))
            self._inpValue.text = ans
        except Exception as error:
            self._inpValue.text = "EVAL ERROR"
        pass

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        '''
        Act when a key is pressed down
        :param keyboard: The keyboard object
        :param keycode: The pressed key code
        :param text: The text that was pressed
        :param modifiers: A list of keyboard modifiers
        :return: True to accept the key, or False to ignore it
        '''
        if keycode[1] == 'escape':
            # Dismiss popup upon 'Esc'
            self.dismiss()

            # Call the cancel_callback if we have it
            if self.cancel_callback is not None:
                self.cancel_callback()

        # Grag all keyboard events so that the base app doesn't get anything
        return True