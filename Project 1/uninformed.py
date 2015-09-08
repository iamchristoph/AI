# uninformed search
# uninformed.py
import time
from collections import deque

printMoves = True
solution = (1, 2, 3, 4, 5, 6, 7, 8, 0) 
# 1 2 3
# 4 5 6
# 7 8 _

class Puzzle :
  #grids = {}
  # list address 
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
    #Puzzle.grids

# Swap the piece at loc + d with the blank. loc = blank's current location
def move(loc, puzzle, d) : 
  moved = puzzle[loc + d]
  chi = [x for x in puzzle]
  chi[loc + d] = 0
  chi[loc] = moved
  child = (chi[0], chi[1], chi[2],chi[3], chi[4], chi[5], chi[6], chi[7], chi[8])
  return child

# Get all the children of a possible puzzle state 
def children(parent) :
  space = parent.blank
  puzzle = parent.state
  depth = parent.depth + 1
  kiddies = []
  for child in parent.kids : # Parent.kids is a list of directions (ints) that are possible to have as kids, not pre-established puzzle states
    kid = Puzzle(move(space, puzzle, child), depth) # Create a new puzzle for each kid
    if kid.state in Puzzle.grids :
      if Puzzle.grids[kid.state].depth > depth :
        Puzzle.grids[kid.state] = parent
        kiddies.append(kid)
    else :
      Puzzle.grids[kid.state] = parent
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

# Get the number of moves taken to reach the goal  
def getMoves(p, max) :
  if p.depth is 0 or max is 0:
    return 1
  else :
    return getMoves(Puzzle.grids[p.state], max - 1) + 1

# Are we there yet?
def is_goal(state) :
  if solution in Puzzle.grids :
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
      #print "nodes searched = ", i
      return (True, i)
    else :
      kids = children(state)
      for kid in kids :
        queue.append(kid)
    if not queue :
      return (False, i)
    state = queue.popleft()
  return (False, i)
    
# Depth first search
def depth(start) :
  stack = deque()
  state = Puzzle(start, 0)
  i = 0
  while i < 50000 :
    i += 1
    if is_goal(state) :
      #print "nodes searched =", i
      return (True,i)
    else :
      kids = children(state)
      for kid in kids :
        stack.append(kid)
    if not stack :
      return (False, i)
    state = stack.pop()
  return (False, i)
  
# Depth limited search
def depth_limited(start, limit) :
  stack = deque()
  state = Puzzle(start, 0)
  i = 0
  if limit == -1:
    limit = 500000
  while i < 500000 :
    i += 1
    #print state.depth,
    if is_goal(state) :
      return (True, i) # Found the goal, this many nodes searched
    else :
      kids = children(state)
      for kid in kids :
        if kid.depth < limit : # Only look at a kid if it has less than 40 depth? 
        # This was taking 17566 nodes to find the solution, without it it takes 12740 nodes
          stack.append(kid)
    if not stack :
      return (False, i) # Did not find the goal, this many nodes searched
    state = stack.pop()
  return (False, limit)
    
# Iterative Deepening search
def iterative(start, limit):
  if limit == -1:
    limit = 500000
  
  for i in range(1, limit+1):
    returned = depth_limited(start, i)
    success, nodes = returned
    if success:
      return (success, nodes)
      
    #clean up
    del Puzzle.grids
    Puzzle.grids = {}

  return (False, limit)
  
# Bi-Directional
def bidirectional(start, end):
  # Both sides to a BFS, stop when one element is in both BFS's
  
  startGrid = {} 
  endGrid = {} 
  
  def get_children(parent, grid):
    space = parent.blank
    puzzle = parent.state
    depth = parent.depth + 1
    kiddies = []
    for child in parent.kids :
      kid = Puzzle(move(space, puzzle, child), depth) # Create a new puzzle for each kid
      if kid.state in grid :
        if grid[kid.state].depth > depth :
          grid[kid.state] = parent
          kiddies.append(kid)
      else :
        grid[kid.state] = parent
        kiddies.append(kid)
    return (kiddies, grid)
  
  
  def goalFound():
    for key in startGrid.keys():
      if key in endGrid:
        return True
        
    return False
    
  def constructPuzzleGrid():
    for key in startGrid.keys():
      if key in endGrid:
        # This is where the two grids meet
        # Add the "tree" for the startGrid to Puzzle Grid
        startTree = key
        while not startGrid[startTree].depth == 0:
          Puzzle.grids[startTree] = startGrid[startTree]
          startTree = startGrid[startTree].state
          
        Puzzle.grids[startTree] = startGrid[startTree]
        
        depthOfStart = startGrid[key].depth
        depthOfEnd = endGrid[key].depth
        endTree = key
        while not endTree == solution:  
          # Needs to convert the endTree's child state -> parent puzzle into parent state -> child puzzle
          Puzzle.grids[endGrid[endTree].state] = Puzzle(endTree, depthOfStart + (depthOfEnd - endGrid[endTree].depth) +1)
          
          endTree = endGrid[endTree].state
        
        return
  
  startQueue = deque()
  startState = Puzzle(start, 0) 
  
  endQueue = deque()
  endState = Puzzle(end, 0)
  
  i = 0
  while i < 50000 :
    i += 1
    # Check if the goal is found
    if goalFound() :
      # Construct the Puzzle Grid
      constructPuzzleGrid()
      return (True, i)
    # Iterate on the start
    else :
      kids, startGrid = get_children(startState, startGrid)
      for kid in kids :
        startQueue.append(kid)
    if not startQueue :
      return (False, i)
    startState = startQueue.popleft()
    
    # Check if the goal is found
    if goalFound() :
      constructPuzzleGrid()
      return (True, i)
    # Iterate on the end
    else :
      kids, endGrid = get_children(endState, endGrid)
      for kid in kids :
        endQueue.append(kid)
    if not endQueue :
      return (False, i)
    endState = endQueue.popleft()
    
  return (False, i)
  
# ---------------------------------------------------------------------------
# Run the tests    

test = (0, 1, 3, 5, 7, 8, 6, 4, 2)
Puzzle.grids = {}
#visited = {test:None}

# Start Breadth First Search
start = time.time()
success, nodes = breadth(test)
if success:
  end = time.time()
  print "BFS solution found!\n- Solution found in %s seconds\n- %s nodes searched\n- The solution takes %s moves"%(end - start, nodes, getMoves(Puzzle.grids[solution], 100))
  if printMoves:
    display(Puzzle.grids[solution], 100)
else :
  end = time.time()
  print "BFS failed to find solution. Ran for %s seconds and searched %s nodes"%(end - start, nodes)

  
#clean up
del Puzzle.grids
Puzzle.grids = {}

# Start Depth First Search
start = time.time()
success, nodes = depth_limited(test, 100000) 
if success:
  end = time.time()
  print "DFS solution found!\n- Solution found in %s seconds\n- %s nodes searched\n- The solution takes %s moves"%(end - start, nodes, getMoves(Puzzle.grids[solution], 100))
  if printMoves:
    display(Puzzle.grids[solution], 100)
else :
  end = time.time()
  print "DFS failed to find solution. Ran for %s seconds and searched %s nodes"%(end - start, nodes)

#clean up
del Puzzle.grids
Puzzle.grids = {}

# Start Depth Limited Search
start = time.time()
success, nodes = depth_limited(test, 21)
end = time.time()
if success:
  print "Depth Limited solution found!\n- Solution found in %s seconds\n- %s nodes searched\n- The solution takes %s moves"%(end - start, nodes, getMoves(Puzzle.grids[solution], 100))
  if printMoves:
    display(Puzzle.grids[solution], 100)
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
  print "Iterative Deepening solution found!\n- Solution found in %s seconds\n- %s nodes searched\n- The solution takes %s moves"%(end - start, nodes, getMoves(Puzzle.grids[solution], 100))
  if printMoves:
    display(Puzzle.grids[solution], 100)
else :
  print "Iterative Deepening failed to find solution. Ran for %s seconds and searched %s nodes"%(end - start, nodes)


#clean up
del Puzzle.grids
Puzzle.grids = {}

# Bi-Directional Search
start = time.time()
success, nodes = bidirectional(test, solution)
end = time.time()
if success:
  print "Bi-Directional solution found!\n- Solution found in %s seconds\n- %s nodes searched\n- The solution takes %s moves"%(end - start, nodes, getMoves(Puzzle.grids[solution], 100))
  if printMoves:
    display(Puzzle.grids[solution], 100)
else :
  print "Bi-Directional failed to find solution. Ran for %s seconds and searched %s nodes"%(end - start, nodes)
