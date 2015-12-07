# neural_gui.py

import Tkinter
top = Tkinter.Tk('Perceptron Array Lab', )
canvas = Tkinter.Canvas(top, bg = 'black', height = 9, width = 8)

class colorChangeButton :
  def __init__(this, b) :
    this.button = b
    this.button.configure(command = this.changeColorCallBack)
  def changeColorCallBack(this) :
    this.button.configure(bg='black')
  def pack(this) :
    this.button.pack()  

pic = []
for x in range(8) :
  pic.append(colorChangeButton(Tkinter.Button(top, bg='white', height=1, width=2)))

b11 = colorChangeButton(Tkinter.Button(top, bg='white', height=1, width=2))
for x in pic :
  x.pack()
b11.pack()
canvas.pack()
top.mainloop()