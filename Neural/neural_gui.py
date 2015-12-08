# neural_gui.py
import neural
import Tkinter
import tkMessageBox

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

def evaluateInput() :
  strVal = getString();
  t_Val = strVal.split()
  results = [0,0,0,0,0, 0]
  for p in neural.perceptrons :
    results[p.target] += p.evaluate(t_Val[0])
  tkMessageBox.showinfo("Results", 'sum 1\'s = ' + str(results[1]) + '\nsum 2\'s = ' + str(results[2]) + '\nsum 3\'s = ' + str(results[3]) + '\nsum 4\'s = ' + str(results[4]) + '\nsum 5\'s = ' + str(results[5]) + '\n')

def getString() :
  chars = []
  for y in range(9) :
    for x in range(8) :
      chars.append(pic[y][x].value)
  target = userEntry.get()
  if target :    
    chars.append(' ' + userEntry.get() + '\n')
    return ''.join(chars);
  else :
    tkMessageBox.showinfo("Error", 'you must enter a number')

def storeData( ) :
  strVal = getString()
  if strVal :
    with open('training_example.dat', 'a') as myfile :
      myfile.write(strVal)


pic = []
for y in range(9) :
  pic.append([])
  for x in range(8) :
    pic[y].append(colorChangeButton(Tkinter.Button(picFrame, bg='white', height=1, width=2)))
    pic[y][x].button.grid(row=y, column=x)

evalButton = Tkinter.Button(exFrame, bg='green', text='Evaluate', command=evaluateInput)
evalButton.grid(row=0, column=0);
clearButton = Tkinter.Button(exFrame, bg='red', text='Clear')
clearButton.grid(row=0, column=1)
storeButton = Tkinter.Button(exFrame, bg='blue', text='Store', command=storeData)
storeButton.grid(row=0, column=2)
userEntry = Tkinter.Entry(exFrame, width=1)
userEntry.grid(row=0, column=3)

top.mainloop()