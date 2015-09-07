# uninformed search
# uninformed.py
import time
from collections import deque

solution = 1, 2, 3, 4, 5, 6, 7, 8, 0

class Puzzle :
  grids = {}
  # Grid
  # 0 1 2
  # 3 4 5
  # 6 7 8
  def getOffspring(self) :
    # Returns the positions (relative to the blank's position in the list) of pieces that can be swapped with the blank
    blank = self.blank
    if blank is 0 : # The blank can move right or down
      return 1, 3
    elif blank is 1 : # The blank can move left, right, or down
      return -1, 1, 3
    elif blank is 2 : # The blank can move left or down
      return -1, 3
    elif blank is 3 : # The blank can move up, right, or down
      return -3, 1, 3
    elif blank is 4 : # The blank can move up, left, right, or down
      return -3, -1, 1, 3
    elif blank is 5 : # The blank can move up, left, or down
      return -3, -1, 3
    elif blank is 6 : # The blank can move up or right
      return -3, 1
    elif blank is 7 : # The blank can move up, left, or right
      return -3, -1, 1
    elif blank is 8 : # The blank can move up or left
      return -3, -1
      
  def __init__(self, puzz, dep) :
    self.state = puzz
    self.depth = dep
    self.blank = puzz.index(0)
    self.kids = Puzzle.getOffspring(self)
    Puzzle.grids

# Swap the piece at loc + d with the blank. loc = blank's current location
def move(loc, puzzle, d) : 
  moved = puzzle[loc + d]
  chi = [x for x in puzzle]
  chi[loc + d] = 0
  chi[loc] = moved
  child = (chi[0], chi[1], chi[2],chi[3], chi[4], chi[5], chi[6], chi[7], chi[8])
  return child

# Get all the children of a possible puzzle state 
def children(p) :
  space = p.blank
  puzzle = p.state
  d = p.depth + 1
  kiddies = []
  for child in p.kids :
    kid = Puzzle(move(space, puzzle, child), d)
    if kid.state in Puzzle.grids :
      if Puzzle.grids[kid.state].depth > d :
        Puzzle.grids[kid.state] = p
    else :
      Puzzle.grids[kid.state] = p
      kiddies.append(kid)
  return kiddies

# Print the puzzle
def display(p, max) :
  if p.depth is 0 or max is 0:
    pass
  else :
    display(Puzzle.grids[p.state], max - 1)
  print "depth =", p.depth
  print p.state[0:3]
  print p.state[3:6]
  print p.state[6:]

# Are we there yet?
def is_goal(state) :
  if (1, 2, 3, 4, 5, 6, 7, 8, 0) in Puzzle.grids :
    return True
  return False

# Breadth first search
def breadth(start) :
  queue = deque()
  state = Puzzle(start, 0)
  i = 0
  while i < 50000 :
    i += 1
    if is_goal(state) :
      print "nodes searched = ", i
      return True
    else :
      kids = children(state)
      for kid in kids :
        queue.append(kid)
    if not queue :
      return False
    state = queue.popleft()

# Depth first search
def depth(start) :
  stack = deque()
  state = Puzzle(start, 0)
  i = 0
  while i < 50000 :
    i += 1
    if is_goal(state) :
      print "nodes searched =", i
      return True
    else :
      kids = children(state)
      for kid in kids :
        stack.append(kid)
    if not stack :
      return False
    state = stack.pop()

# Depth limited search
def depth_limited(start, limit) :
  stack = deque()
  state = Puzzle(start, 0)
  i = 0
  if limit == -1:
    limit = 500000
  while i < limit :
    i += 1
    if is_goal(state) :
      return (True, i) # Found the goal, this many nodes searched
      #print "nodes searched =", i
      #return True
    else :
      kids = children(state)
      for kid in kids :
        #if kid.depth < 40 : # Only look at a kid if it has less than 40 depth? 
        # This was taking 17566 nodes to find the solution, without it it takes 12740 nodes
          stack.append(kid)
    if not stack :
      return (False, i) # Did not find the goal, this many nodes searched
      #print "Nodes searched =", i
      #return False
    state = stack.pop()
  return (False, limit)
    
# Iterative Deepening search
def iterative(start, limit):
  if limit == -1:
    limit = 500000
  
  #returned = depth_limited(start, 12739)
  #print returned
  #exit()
  for i in range(1, limit+1):
    returned = depth_limited(start, i)
    success, nodes = returned
    if success:
      return (success, nodes)
    #clean up
    del Puzzle.grids
    Puzzle.grids = {}
      
  return (False, limit)
  
# ---------------------------------------------------------------------------
# Run the tests    

test = (0, 1, 3, 5, 7, 8, 6, 4, 2)
#visited = {test:None}

# Start Breadth First Search
start = time.time()
if breadth(test) :
  end = time.time()
  print "BFS solution found! Solution found in %s seconds."%(end - start)
  #display(Puzzle.grids[solution], 100)
else :
  end = time.time()
  print "BFS failed to find solution. Ran for %s seconds."%(end - start)

#clean up
del Puzzle.grids
Puzzle.grids = {}

# Start Depth First Search
start = time.time()
if depth(test) :
  end = time.time()
  print "DFS solution found! Solution found in %s seconds."%(end - start)
  #display(Puzzle.grids[solution], 100)
else :
  end = time.time()
  print "DFS failed to find solution. Ran for %s seconds."%(end - start)

#clean up
del Puzzle.grids
Puzzle.grids = {}

# Start Depth Limited Search
start = time.time()
success, nodes = depth_limited(test, -1)
end = time.time()
if success:
  print "Depth Limited solution found! Solution found in %s seconds after searching %s nodes"%(end - start, nodes)
  #display(Puzzle.grids[solution], 100)
else :
  print "Depth Limited failed to find solution. Ran for %s seconds and searched %s nodes"%(end - start, nodes)
  
#clean up
del Puzzle.grids
Puzzle.grids = {}

# Start Iterative Deepening Search
start = time.time()
success, nodes = iterative(test, -1)
end = time.time()
if success:
  print "Iterative Deepening solution found! Solution found in %s seconds after searching %s nodes"%(end - start, nodes)
  #display(Puzzle.grids[solution], 100)
else :
  print "Iterative Deepening failed to find solution. Ran for %s seconds and searched %s nodes"%(end - start, nodes)
