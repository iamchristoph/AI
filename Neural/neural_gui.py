# neural_gui.py
import neural
import Tkinter
import tkMessageBox

height = 9
width = 8

top = Tkinter.Tk('Perceptron Array Lab', )
canvas = Tkinter.Canvas(top, bg = 'black', height = height, width = width)
pFrame = Tkinter.Frame(top)
pFrame.pack(side = 'left')
picFrame = Tkinter.Frame(top)
picFrame.pack()
exFrame = Tkinter.Frame(top)
exFrame.pack()
nnetwork = neural.neuralnetwork()

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
  if strVal :
    t_Val = strVal.split()
    #results = [0,0,0,0,0, 0]
    results = [0] * len(neural.NUMBERS) # Will adapt to match the 
    for p in nnetwork.perceptrons :
      results[p.target] += p.evaluate(t_Val[0])
   
  output = ""
  bestResult = -5
  for i in range(len(results)):
    output += "\nsum %s's = %s"%(i, results[i])
    if results[i] > bestResult:
      bestResult = results[i]
      
  decision = ""
  if bestResult < -4:
    decision = "Undetermined"
  else:
    accepted = []
    for i in range(len(results)):
      if results[i] == bestResult:
        accepted.append("%s"%i)
    decision = " or ".join(accepted)
    
  output += "\n\nConclusion: %s"%decision  
  
  #output = 'sum 1\'s = ' + str(results[1]) + '\nsum 2\'s = ' + str(results[2]) + '\nsum 3\'s = ' + str(results[3]) + '\nsum 4\'s = ' + str(results[4]) + '\nsum 5\'s = ' + str(results[5]) + '\n\nVerdict = '
  tkMessageBox.showinfo("Results", output)
  
  

def clearInput():
  for y in pic:
    for x in range(width) :
      y[x].value='0'
      y[x].button.configure(bg='white')
  userEntry.delete(0, 'end')
  
def getString() :
  chars = []
  for y in range(height) :
    for x in range(width) :
      chars.append(pic[y][x].value)
  target = userEntry.get()
  if target :    
    chars.append(' ' + userEntry.get() + '\n')
    return ''.join(chars)
  else :
    return ''.join(chars)

def storeData( ) :
  strVal = getString()
  if len(strVal) > neural.SIZE :
    with open('training_example.dat', 'a') as myfile :
      myfile.write(strVal)
  userEntry.delete(0, 'end')
  
def trainPerceptrons() :
  nnetwork.train(5)

def savePerceptrons() :
  nnetwork.save()

def loadPerceptrons() :
  nnetwork.load()

pic = []
for y in range(height) :
  pic.append([])
  for x in range(width) :
    pic[y].append(colorChangeButton(Tkinter.Button(picFrame, bg='white', height=1, width=2)))
    pic[y][x].button.grid(row=y, column=x)

evalButton = Tkinter.Button(exFrame, bg='green', text='Evaluate', command=evaluateInput)
evalButton.grid(row=0, column=0)
clearButton = Tkinter.Button(exFrame, bg='red', text='Clear', command=clearInput)
clearButton.grid(row=0, column=1)
storeButton = Tkinter.Button(exFrame, bg='blue', text='Store', command=storeData)
storeButton.grid(row=0, column=2)
userEntry = Tkinter.Entry(exFrame, width=1, font=16)
userEntry.grid(row=0, column=3)
trainButton = Tkinter.Button(pFrame, bg='green', text='Train', command=trainPerceptrons)
trainButton.pack()
saveButton = Tkinter.Button(pFrame, bg='blue', text='Save', command=savePerceptrons)
saveButton.pack()
loadButton = Tkinter.Button(pFrame, bg='red', text='Load', command=loadPerceptrons)
loadButton.pack()


top.mainloop()