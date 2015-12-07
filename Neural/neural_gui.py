# neural_gui.py
#import 'neural.py'
import Tkinter
top = Tkinter.Tk('Perceptron Array Lab', )
canvas = Tkinter.Canvas(top, bg = 'black', height = 9, width = 8)
picFrame = Tkinter.Frame(top)
picFrame.pack()
exFrame = Tkinter.Frame(top)
exFrame.pack()

class colorChangeButton :
  def __init__(this, b) :
    this.value = '0'
    this.button = b
    this.button.configure(command = this.changeColorCallBack)
  def changeColorCallBack(this) :
    if this.value == '0' :
      this.button.configure(bg='black')
      this.value = '1'
    else :
      this.button.configure(bg= 'white')
      this.value = '0'



pic = []
for y in range(9) :
  pic.append([])
  for x in range(8) :
    pic[y].append(colorChangeButton(Tkinter.Button(picFrame, bg='white', height=1, width=2)))
    pic[y][x].button.grid(row=y, column=x)

evalButton = Tkinter.Button(exFrame, bg='green', text='Evaluate')
evalButton.grid(row=0, column=0);
clearButton = Tkinter.Button(exFrame, bg='red', text='Clear')
clearButton.grid(row=0, column=1)
storeButton = Tkinter.Button(exFrame, bg='blue', text='Store')
storeButton.grid(row=0, column=2)
userEntry = Tkinter.Entry(exFrame, width=1)
userEntry.grid(row=0, column=3)

top.mainloop()