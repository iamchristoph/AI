import time
import sys
from collections import deque

# -------------------------------------------------
# Project by Christopher Terry and Travis Smith
# -------------------------------------------------

# Instructions on use:
#   python uninformed.py <optional file name>
#
# If a file name is not provided, the following will be used instead:
test = (0, 1, 3, 5, 7, 8, 6, 4, 2) 
# _13
# 578
# 642

# True will print out all of the moves taken, while False will not show them. False is very useful for just seeing the program's report
printMoves = False 
# Set to a different number to try a different limit for Depth Limited Search
depthLimitedCap = 21 
# If you want 
maximumMovesToShow = 31 

# Shouldn't need to alter, but provided as a config option none the less
solution = (1, 2, 3, 4, 5, 6, 7, 8, 0) # Option to re-arrange the way the solution is formatted
# 1 2 3
# 4 5 6
# 7 8 _

# -------------------------------------------------
#   End of Config Options
# -------------------------------------------------



# Read a filename, if any, provided on the command line
if len(sys.argv) > 1:
  filename = sys.argv[1]
  text = ""
  with open(filename) as f:
    for line in f:
      for character in line:
        if character in ('12345678_'):
          text += character
          
  text = text.replace("_", "0")
  
  listOfInts = []
  for character in text:
    listOfInts.append(int(character))
  testReplacement = tuple(listOfInts)
  test = testReplacement


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

  #clean up
  def cleanUp() :
    if Puzzle.grids :
      del Puzzle.grids
    Puzzle.grids = {}

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
  print "moves =", p.depth
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

# Informed Searces ----------------------------------------------------------  
# ---------------------------------------------------------------------------
# Heuristics
from math import ceil

def manhattan(grid) :
  value = 0
  for num in grid :
    i = grid.index(num) + 1
    if num is 0 :
      num = 9
    upDnMoves = abs(-(-num/3) - (-(-i//3)))
    x = i%3
    x = x if x else 3
    y = num%3
    y = y if y else 3
    lrMoves = abs(y - x)
    value += upDnMoves + lrMoves
  return value

# A* search
def aStar(start, heuristic, useD) :
  def gethValue(node, useDepth) :
      if useDepth :
        node.hValue = heuristic(node.state) + node.depth
      else :
        node.hValue = heuristic(node.state)
  queue = []
  state = Puzzle(start, 0)
  gethValue(state, useD)
  i = 0
  while i < 50000 :
    i += 1
    if is_goal(state) :
      return (True, i)
    else :
      kids = children(state)
      for kid in kids :
        gethValue(kid, useD)
        queue.append(kid)
      queue.sort(key= lambda x : x.hValue)
      #print [x.hValue for x in queue]
    if not queue :
      return (False, i)
    state = queue.pop(0)
  return (False, i)

# ---------------------------------------------------------------------------
# Run the tests    



originalPuzzle = test

Puzzle.grids = {}

# Start Breadth First Search
start = time.time()
success, nodes = breadth(originalPuzzle)
if success:
  end = time.time()
  print "BFS solution found!\n- Solution found in %s seconds\n- %s nodes searched\n- The solution takes %s moves"%(end - start, nodes, getMoves(Puzzle.grids[solution], maximumMovesToShow))
  if printMoves:
    display(Puzzle.grids[solution], maximumMovesToShow)
else :
  end = time.time()
  print "BFS failed to find solution. Ran for %s seconds and searched %s nodes"%(end - start, nodes)

  
#clean up
del Puzzle.grids
Puzzle.grids = {}

# Start Depth First Search
start = time.time()
success, nodes = depth_limited(originalPuzzle, 100000) 
if success:
  end = time.time()
  print "DFS solution found!\n- Solution found in %s seconds\n- %s nodes searched\n- The solution takes %s moves"%(end - start, nodes, Puzzle.grids[solution].depth + 1)
  if printMoves:
    display(Puzzle.grids[solution], maximumMovesToShow)
else :
  end = time.time()
  print "DFS failed to find solution. Ran for %s seconds and searched %s nodes"%(end - start, nodes)

#clean up
del Puzzle.grids
Puzzle.grids = {}

# Start Depth Limited Search
start = time.time()
success, nodes = depth_limited(originalPuzzle, depthLimitedCap)
end = time.time()
if success:
  print "Depth Limited solution found!\n- Solution found in %s seconds\n- %s nodes searched\n- The solution takes %s moves"%(end - start, nodes, getMoves(Puzzle.grids[solution], maximumMovesToShow))
  if printMoves:
    display(Puzzle.grids[solution], maximumMovesToShow)
else :
  print "Depth Limited failed to find solution. Ran for %s seconds and searched %s nodes"%(end - start, nodes)
  
#clean up
del Puzzle.grids
Puzzle.grids = {}

# Start Iterative Deepening Search
start = time.time()
success, nodes = iterative(originalPuzzle, -1)
end = time.time()
if success:
  print "Iterative Deepening solution found!\n- Solution found in %s seconds\n- %s nodes searched\n- The solution takes %s moves"%(end - start, nodes, getMoves(Puzzle.grids[solution], maximumMovesToShow))
  if printMoves:
    display(Puzzle.grids[solution], maximumMovesToShow)
else :
  print "Iterative Deepening failed to find solution. Ran for %s seconds and searched %s nodes"%(end - start, nodes)


#clean up
del Puzzle.grids
Puzzle.grids = {}

# Bi-Directional Search
start = time.time()
success, nodes = bidirectional(originalPuzzle, solution)
end = time.time()
if success:
  print "Bi-Directional solution found!\n- Solution found in %s seconds\n- %s nodes searched\n- The solution takes %s moves"%(end - start, nodes, getMoves(Puzzle.grids[solution], maximumMovesToShow))
  if printMoves:
    display(Puzzle.grids[solution], maximumMovesToShow)
else :
  print "Bi-Directional failed to find solution. Ran for %s seconds and searched %s nodes"%(end - start, nodes)

#clean up
del Puzzle.grids
Puzzle.grids = {}

# Greedy
start = time.time()
success, nodes = aStar(originalPuzzle, manhattan, 0)
end = time.time()
if success :
  print "Greedy solution found!\n- Solution found in %s seconds\n- %s nodes searched\n- The solution takes %s moves"%(end - start, nodes, Puzzle.grids[solution].depth + 1)
  if printMoves :
    display(Puzzle.grids[solution], maximumMovesToShow)
else :
  print "Greedy failed to find solution. Ran for %s seconds and searched %s nodes"%(end - start, nodes)

del Puzzle.grids
Puzzle.grids = {}

# A*
start = time.time()
success, nodes = aStar(originalPuzzle, manhattan, 1)
end = time.time()
if success :
  print "A* solution found!\n- Solution found in %s seconds\n- %s nodes searched\n- The solution takes %s moves"%(end - start, nodes, Puzzle.grids[solution].depth + 1)
  if printMoves :
    display(Puzzle.grids[solution], maximumMovesToShow)
else :
  print "A* failed to find solution. Ran for %s seconds and searched %s nodes"%(end - start, nodes)
