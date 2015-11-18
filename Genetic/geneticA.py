# genetic.py

import random
import string

GENERATIONS = 10000
POPULATION_SIZE = 100
MUTATION_RATE = 0.05 # represented as a percent
#CROSSOVER_RATE = 0.05

# we should change this to be user input, or generate something random.
target = "Awesome"

class mutt :
  def __init__(this, s=None) :
    if s :
      this.gene = s #some string like this 1100100100011110001110010100101
    else :
      this.gene = [random.choice('01') for i in range(random.randint(7, 140))]
    
    
  def getIt(this) :
    s = []
    for i in range(len(this.gene)/7) :
      z = 7 * i
      x = ''.join(this.gene[z:z+7])
      s.append(int(x, 2))
    return ''.join([chr(c) for c in s]) #the string made from the gene
# mutate

  def mutate(this) :
    choice = random.choice(range(len(this.gene)))
    if this.gene[choice] == '0' :
      this.gene[choice] = '1'
    else :
      this.gene[choice] = '0'


# generate random population
def getPopulation(length) :
  population = [mutt() for x in range(POPULATION_SIZE)]
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
    print x.getIt(),
    count += 1
    if count > 10:
      print ''
      count = 0
    else :
      print ', ',

# fitness function

def fitness(c) :
  f = 0
  candidate = c.getIt()
  if len(target) == len(candidate) :
    f += 10000
  else :
    f -= abs(len(target) - len(candidate)) * 10000
  for c in range(min(len(target),len(candidate))) :
    f -= (ord(target[c]) - ord(candidate[c])) * (ord(target[c]) - ord(candidate[c]))
  return f

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

# crossover

def crossover(boy, girl) :
  point = random.choice(range(min(len(boy.gene), len(girl.gene))))
  heir = mutt(boy.gene[0:point] + girl.gene[point:])
  secondOffspring = mutt(girl.gene[0:point] + boy.gene[point:])
  inbredHeir = mutt(boy.gene[point:] + girl.gene[0:point])
  inbredSecond = mutt(girl.gene[point:] + boy.gene[0:point])
  return [heir, secondOffspring, inbredHeir, inbredSecond]



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
results = [x.getIt() for x in pop]
while target not in results :
  pop = tournamentSelection(pop)
  
  
  choices = range(len(pop))
  while len(pop) < POPULATION_SIZE :
    x, y = random.choice(choices), random.choice(choices)
    pop += crossover(pop[x], pop[y])

  #printIt()
  for p in pop :
    if (random.randint(0, POPULATION_SIZE) < int(POPULATION_SIZE * MUTATION_RATE)) :
      p.mutate()
  iters +=1
  results = [x.getIt() for x in pop]
  if iters > GENERATIONS :
    break

print "Number of iterations: ", iters
printIt()
#print "a", nextCharacter('a')
#print "b, prev, ", prevCharacter('b')
#print string.letters