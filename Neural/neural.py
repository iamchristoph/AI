# neural.py

import sys
import random
import pickle

SIZE = 72
ETA = 0.01
NUMBERS = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

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



texamples = []
with open('training_example.dat', 'r') as myfile :
    for line in myfile :
      texamples.append(line.split())

# Shuffle the training examples
random.shuffle(texamples)
class neuralnetwork :
  def __init__(this) :
    this.perceptrons = []
    for x in NUMBERS :
      for y in range(5) : 
        this.perceptrons.append(perceptron(x))

  def train(this, l) :
    limit = l
    while limit :
      for p in this.perceptrons :
        for ex in texamples :
          p.train(ex[0], int(ex[1]))
      limit -= 1

  def save(this) :  
    pickle.dump(this.perceptrons, open('save.p', 'w'))

  def load(this) :  
    print this.perceptrons
    this.perceptrons = pickle.load(open('save.p', 'r'))
    print this.perceptrons
