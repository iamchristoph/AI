# genetic.py

import random
import string

POPULATION_SIZE = 1000
MUTATION_RATE = 100 # represented as a percent

# we should change this to be user input, or generate something random.
target = "SKRa"

# generate random population
def getPopulation(length) :
  population = [getIndividual(length) for x in range(POPULATION_SIZE)]
  return population

def getIndividual(length) :
  individual = [getCharacter() for x in range(length)]
  return ''.join(individual)

def getCharacter() :
  return random.choice(string.letters)

pop = getPopulation(len(target))
def printIt() :
  print 'Target = ', target
  print 'Population: ' 
  count = 0
  for x in pop :
    print x,
    count += 1
    if count > 10:
      print ''
      count = 0
    else :
      print ' |,| ',

# fitness function

def fitness(candidate) :
  fitNumber = 0
  for c in range(len(candidate)) :
    fitNumber -= abs(ord(target[c]) - ord(candidate[c])) * abs(ord(target[c]) - ord(candidate[c]))


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
  for i in range(len(target)) :
    if candidate[i] == target[i] :
      deltaCandidate[i] = candidate[i]
  return ''.join(deltaCandidate)

def getMutation(c) :
  change = 0
  if (random.randint(0, 100) < MUTATION_RATE) :
    change = random.choice([0, 1])
    if change :
      return nextCharacter(c)
    else :
      return prevCharacter(c)
  else :
    return c

def nextCharacter(c) :
  if chr(ord(c) + 1) in string.letters :
    return chr(ord(c) + 1)
  else :
    return c

def prevCharacter(c) :
  if chr(ord(c) - 1) in string.letters :
    return chr(ord(c) - 1)
  else :
    return c

# lets try to apply these methods

#printIt()
iters = 0
while target not in pop :
  pop = tournamentSelection(pop)
  pop = tournamentSelection(pop)
#  pop = tournamentSelection(pop)
#  pop = tournamentSelection(pop)
#  pop = tournamentSelection(pop)
#  pop = tournamentSelection(pop)
  pop = tournamentSelection(pop)
#  pop = tournamentSelection(pop)
  #print 'selection done'
  #printIt()
  pop += [mutate(x) for x in pop]
  pop += [mutate(x) for x in pop]
  pop += [mutate(x) for x in pop]
#  pop += [mutate(x) for x in pop]
#  pop += [mutate(x) for x in pop]
#  pop += [mutate(x) for x in pop]
#  pop += [mutate(x) for x in pop]
#  pop += [mutate(x) for x in pop]
  #printIt()
  iters +=1

print "Number of iterations: ", iters
#printIt()
#print "a", nextCharacter('a')
#print "b, prev, ", prevCharacter('b')
#print string.letters