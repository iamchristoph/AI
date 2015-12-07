# neural.py

import sys
import random

SIZE = 72
ETA = 0.015

t_ex = '000110000001100000011000000110000001100000011000000110000001100000011000'
t_ex1 = '001100000011000000110000001100000011000000110000001100000011000000110000'
t_ex2 = '000100000001110000011100000110000001110000011100000110000001100000111000'
t_ex3 = '111111111100000111000001111000111100000111100011111000111110001111111111'


class perceptron :
  def __init__(this, size) :
    this.weights = [random.random() for x in range(size + 1)]
    this.target = 0
    this.inputs = [0 for x in range(size + 1)]
    this.changed = True
  def train(this, example, target) :
    this.changed = False
    for i in range(len(example)) :
      this.inputs[i] = int(example[i])
    this.inputs[-1] = 1
    this.output = sum([this.inputs[i] * this.weights[i] for i in range(len(this.inputs))])
    if int(this.output) != target :
      this.changed = True
      for i in range(len(this.weights)) :
        this.weights[i] += ETA * (target - this.output) * this.inputs[i]
    return this.output

p1 = perceptron(SIZE)

limit = 50
while p1.changed is True and limit:
  p1.train(t_ex, 1)
  print int(p1.output)
  p1.train(t_ex1, 1)
  print int(p1.output)
  p1.train(t_ex2, 1)
  print int(p1.output)
  p1.train(t_ex3, 0)
  limit -= 1

