# neural.py

import sys
import random

SIZE = 72
ETA = 0.02
NUMBER = 5

t_ex = '000110000001100000011000000110000001100000011000000110000001100000011000'
t_ex1 = '001100000011000000110000001100000011000000110000001100000011000000110000'
t_ex2 = '000100000001110000011100000110000001110000011100000110000001100000111000'
t_ex3 = '111111111100000111000001111000111100000111100011111000111110001111111111'
t_ex4 = '000011000001110000111000000111000011100000111000000110000001110000111000'

class perceptron :
  def __init__(this, target) :
    this.weights = [random.random() for x in range(SIZE + 1)]
    this.target = target
    this.inputs = [0 for x in range(SIZE + 1)]
    this.changed = True
    this.output = 0
  def train(this, example, target) :
    this.changed = False
    this.evaluate(example)
    if this.target == target :
      goal = 1
    else :
      goal = -1
    if this.output != goal :
      this.changed = True
      for i in range(len(this.weights)) :
        this.weights[i] += ETA * (goal - this.output) * this.inputs[i]
    return this.output

  def evaluate(this, example) :
    for i in range(len(example)) :
      this.inputs[i] = int(example[i])
    this.inputs[-1] = 1
    out = sum([this.inputs[i] * this.weights[i] for i in range(len(this.inputs))])
    if out > 0 :
      this.output = 1
    else :
      this.output = -1
    return this.output


perceptrons = []
for x in range(NUMBER) :
  for y in range(5) : 
    perceptrons.append(perceptron(x+1))


texamples = []
with open('training_example.dat', 'r') as myfile :
    for line in myfile :
      texamples.append(line.split())



limit = 20
while perceptrons[0].changed is True or limit:
  for p in perceptrons :
    #print p.target, p.output
    
    # Shuffle the training examples
    random.shuffle(texamples)
    for ex in texamples :
      p.train(ex[0], int(ex[1]))

#  p1.train(t_ex, 1)
#  print int(p.output)
#  p1.train(t_ex1, 1)
#  print int(p1.output)
#  p1.train(t_ex2, 1)
#  print int(p1.output)
#  p1.train(t_ex3, 0)
#  print int(p1.output)
#  p1.train(t_ex4, 1)
  limit -= 1

#print int(p1.evaluate(t_ex4))

#print int(p1.evaluate(t_ex1))
#print int(p1.evaluate(t_ex2))
#print int(p1.evaluate(t_ex3))
