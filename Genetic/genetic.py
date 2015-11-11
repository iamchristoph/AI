# genetic.py

import random
import string

POPULATION_SIZE = 100

# we should change this to be user input, or generate something random.
target = "SKRadD"

# generate random population
def getPopulation(length) :
  population = [getIndividual(length) for x in range(POPULATION_SIZE)]
  return population

def getIndividual(length) :
  individual = [getCharacter() for x in range(length)]
  return ''.join(individual)

def getCharacter() :
  return random.choice(string.printable)

pop = getPopulation(len(target))
def printIt() :
  print 'Target = ', target
  print 'Population: ' 
  for x in pop :
    print x

# fitness function

def fitness(candidate) :
  fitNumber = 0
  for c in range(len(candidate)) :
    fitNumber -= abs(ord(target[c]) - ord(candidate[c]))


# select from population to breed

# tournament selection
def tournamentSelection(population) :
  breedingPopulation = [getBreeder(i, population) for i in range (len(population)/2)]
  return breedingPopulation

def getBreeder(i, population) :
  if fitness(population[i]) > fitness(population[i * 2]) :
    return population[i]
  else :
    return population[i * 2]

# mutate

def mutate(candidate) :
  deltaCandidate = [getMutation(c) for c in candidate]
  #print 'candidate: ', candidate, 'mutation : ', ''.join(deltaCandidate)
  return ''.join(deltaCandidate)

def getMutation(c) :
  change = random.randint(-1, 1)
  if change > 0 :
    return nextCharacter(c)
  elif change < 0 :
    return prevCharacter(c)
  else :
    return c

def nextCharacter(c) :
  if ord(c) + 1 in range(len(string.printable)) :
    return string.printable[ord(c)+1]
  else :
    return c

def prevCharacter(c) :
  if ord(c) + 1 in range(len(string.printable)) :
    return string.printable[ord(c)-1]
  else :
    return c

# lets try to apply these methods

printIt()
iters = 0
while target not in pop :
  pop = tournamentSelection(pop)
  #print 'selection done'
  #printIt()
  pop += [mutate(x) for x in pop]
  #printIt()
  iters +=1

print "Number of iterations: ", iters
printIt()