# kivyNumberInput

Provide NumberPad input for Float/Integer Input widget inherited from kivy.uix.textinput includes
- FloatInput
- IntegerInput

## Features:
 - Support pad input and simple calculator
 - title can be set
 - value range can be set

## Demo
![](https://raw.githubusercontent.com/yinjilong/kivyNumberInput/refs/heads/master/demo/numpad-demo1.gif)

## Known issues:

## Todo


## Changes
[2020/10/01]
 * remove line under title
 * add close button at upper right corner to close input pad

[2020/09/04]
  * To fix the bug that the sign of plus/minus number can not be input, the ```eval(str)``` is used to do calculation.
  * Adjust the font size to fit the window size automatically
  * Add the validity range for numeric input
   


