from kivy.uix.textinput import TextInput

from NumberPad import NumberPad

import re

class NumberInput(TextInput):

    def _on_focus(self, instance, value, *largs):
        # self.setup_keyboard()
        # super(NumberInput, self)._on_focus(instance, value, *largs)
        # # self.background_color=(1.0,0.0,0.0,0.5)
        # pass
        self._kb=NumberPad(init_value=self.text,size_hint=(0.5,0.5),size=(250,250))
        self._kb.set_callback(self._keyboard_close)
        self._kb.open()

    def _keyboard_close(self):
        self.text=self._kb.result
        print("keyboard closed")
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

