from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from number_inputbox import FloatInput,IntegerInput

class TestFloatInput(App):
    def build(self):
        instance = Builder.load_string('''
<TestFloatBox@BoxLayout>
    orientation:'vertical'
    BoxLayout:
        orientation:'horizontal'
        Label:
            text:'Input a float number'
        FloatInput:
            id:_float_input_
    BoxLayout:
        orientation:'horizontal'
        Label:
            text:'Input an integer number'
        IntegerInput:
            id:_integer_input_
            text:'123'
TestFloatBox:       

''')
        return instance


if __name__ == '__main__':
    print("TestFloatInput")
    TestFloatInput().run()