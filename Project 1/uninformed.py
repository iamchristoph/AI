# uninformed search
# uninformed.py

# load puzzle
# 1 2 3
# 4 5 6
# 7 8 _

solution = 1, 2, 3, 4, 5, 6, 7, 8, 0

from collections import deque

class Puzzle :
  grids = {}
  def getOffspring(self) :
    s = self.s
    if s is 0 : 
      return 1, 3
    elif s is 1 : 
      return -1, 1, 3
    elif s is 2 :
      return -1, 3
    elif s is 3 :
      return -3, 1, 3
    elif s is 4 :
      return -3, -1, 1, 3
    elif s is 5 :
      return -3, -1, 3
    elif s is 6 :
      return -3, 1
    elif s is 7 :
      return -3, -1, 1
    elif s is 8 :
      return -3, -1
  def __init__(self, puzz, dep) :
    self.p = puzz
    self.d = dep
    self.s = puzz.index(0)
    self.kids = Puzzle.getOffspring(self)
    Puzzle.grids

test = (0, 1, 3, 5, 7, 8, 6, 4, 2)

visited = {test:None}
def move(loc, puzzle, d) :
    moved = puzzle[loc + d]
    chi = [x for x in puzzle]
    chi[loc + d] = 0
    chi[loc] = moved
    child = (chi[0], chi[1], chi[2],chi[3], chi[4], chi[5], chi[6], chi[7], chi[8])
    return child

def children(p) :
  space = p.s
  puzzle = p.p
  d = p.d + 1
  kiddies = []
  for child in p.kids :
    kid = Puzzle(move(space, puzzle, child), d)
    if kid.p in Puzzle.grids :
      if Puzzle.grids[kid.p].d > d :
        Puzzle.grids[kid.p] = p
    else :
      Puzzle.grids[kid.p] = p
      kiddies.append(kid)
  return kiddies


def display(p, max) :
  if p.d is 0 or max is 0:
    pass
  else :
    display(Puzzle.grids[p.p], max - 1)
  print "depth =", p.d
  print p.p[0:3]
  print p.p[3:6]
  print p.p[6:]

def is_goal(state) :
  if (1, 2, 3, 4, 5, 6, 7, 8, 0) in Puzzle.grids :
    return True
  return False

#breadth first
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

def depth_limited(start) :
  stack = deque()
  state = Puzzle(start, 0)
  i = 0
  while i < 500000 :
    i += 1
    if is_goal(state) :
      print "nodes searched =", i
      return True
    else :
      kids = children(state)
      for kid in kids :
        if kid.d < 40 :
          stack.append(kid)
    if not stack :
      print "Nodes searched =", i
      return False
    state = stack.pop()

if breadth(test) :
  print "BFS solution found!!"
  display(Puzzle.grids[solution], 100)
else :
  print "Failed to find solution"

#clean up
del Puzzle.grids
Puzzle.grids = {}

if depth(test) :
  print "DFS solution found!!"
  display(Puzzle.grids[solution], 100)
else :
  print "Failed to find solution"

#clean up
del Puzzle.grids
Puzzle.grids = {}

if depth_limited(test) :
  print "Depth Limited solution found!!"
  display(Puzzle.grids[solution], 100)
else :
  print "Failed to find solution"