# genetic.py

import random
import string

POPULATION_SIZE = 1000
MUTATION_RATE = 100 # represented as a percent
CROSSOVER_RATE = 0.05

# we should change this to be user input, or generate something random.
target = "SkRa"

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
  return fitNumber

# select from population to breed

# tournament selection
def tournamentSelection(population) :
  breedingPopulation = [getBreeder(i, population) for i in range (len(population)/2)]
  return breedingPopulation

def fitnessProportionate(population):
    candidateWeights = {}
    lowestWeight = 1000
    for candidate in population:
        weight = fitness(candidate) 
        candidateWeights[candidate] = weight
        if weight < lowestWeight:
            lowestWeight = weight
            
    weights = []
    for c in candidateWeights.keys():
        weights += [c] * (candidateWeights[c] - lowestWeight + 1)
    
    breedingPopulation = set([])
    while len(breedingPopulation) < len(population)/2:
        candidate = random.choice(weights)
        breedingPopulation.add(candidate)
        
    return list(breedingPopulation)
    
    
def rankedSelection(population):
    # worst selection has a weight of 1, second worst weight of 2, best weight of N
    population.sort(sortByRank)
    
    weights = []
    currentWeight = 1
    for c in population:
        weights += [c] * currentWeight
        currentWeight += 1
    
    breedingPopulation = set([])
    while len(breedingPopulation) < len(population)/2:
        candidate = random.choice(weights)
        breedingPopulation.add(candidate)
    return list(breedingPopulation)
  
def sortByRank(a, b):
    aScore = 0
    bScore = 0
    for i in range(len(target)):
        c = target[i]
        if c in a:
            aScore += 5
            if a[i] == c:
                aScore += 10
        if c in b:
            bScore += 5
            if b[i] == c:
                bScore += 10
    
    if aScore > bScore:
        return 1
    elif aScore == bScore:
        return 0
    else:
        return -1
    
  
def getBreeder(i, population) :
  if fitness(population[i]) > fitness(population[i * 2]) :
    return population[i]
  else :
    return population[i * 2]

# crossover

def crossover(boy, girl) :
  point = random.choice(range(len(target)))
  heir = boy[0:point] + girl[point:]
  secondOffspring = girl[0:point] + boy[point:]
  inbredHeir = boy[point:] + girl[0:point]
  inbredSecond = girl[point:] + boy[0:point]
  return [heir, secondOffspring, inbredHeir, inbredSecond]

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

repeatMutate = 1
repeatSelect = 1
#selector = tournamentSelection
selector = fitnessProportionate
#selector = rankedSelection


while target not in pop :

  for i in range(repeatSelect):
    pop = selector(pop)
  
  sex = (int)(len(pop)* CROSSOVER_RATE)
  choices = range(len(pop))
  for i in range(sex) :
    x, y = random.choice(choices), random.choice(choices)
    pop += crossover(pop[x], pop[y])
#  pop = tournamentSelection(pop)
  #print 'selection done'
  #printIt()
  
  for i in range(repeatMutate):
    pop += [mutate(x) for x in pop]
    
  #printIt()
  iters +=1

print "Number of iterations: ", iters
#printIt()
#print "a", nextCharacter('a')
#print "b, prev, ", prevCharacter('b')
#print string.letters