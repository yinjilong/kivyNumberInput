# The following lines for test
from kivy.app import App
from kivy.lang import Builder

from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
from kivy.properties import NumericProperty

from NumberPad import NumberPad

import re

class NumberInput(TextInput):

    title = StringProperty("Enter a number")
    min_value = NumericProperty(None)
    max_value = NumericProperty(None)

    def _on_focus(self, instance, value, *largs):
        self._kb=NumberPad(init_value=self.text,size_hint=(0.5,0.5),size=(400,400), range=(self.min_value,self.max_value))
        self._kb.title= self.title
        self._kb.set_callback(self._keyboard_close,self._keyboard_escape,self)
        self._kb.open()

    def _keyboard_escape(self):
        self.focus = False
        self._kb.dismiss()
        pass


    def _keyboard_close(self):
        self.text=self._kb.result
        self.focus = False
        self._kb.dismiss()
        pass

    def on_title(self, instance, _title_):
        self.title=_title_
        pass

class FloatInput(NumberInput):

    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])
        return super(FloatInput, self).insert_text(s, from_undo=from_undo)

class IntegerInput(NumberInput):

    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        s = re.sub(pat, '', substring)
        return super(IntegerInput, self).insert_text(s, from_undo=from_undo)


class TestFloatInput(App):
    def build(self):
        instance = Builder.load_string('''
<TestFloatBox@BoxLayout>
    orientation:'vertical'
    BoxLayout:
        orientation:'horizontal'
        Label:
            text:'Float number'
        FloatInput:
            id:_float_input_
            write_tab:True
            min_value:0.0
            max_value:10.0
    BoxLayout:
        orientation:'horizontal'
        Label:
            text:'Integer number'
        IntegerInput:
            id:_integer_input_
            text:'123'
            write_tab:True
            title:'Width'
TestFloatBox:       
        
''')
        return instance


if __name__ == '__main__':
    TestFloatInput().run()