def customHeuristic(grid):
  value = 0
  for i in range(len(grid)):
    piece = grid[i]
    if (i+1) == piece or (piece == 0 and (i+1) == 9):
      value += 0 # the piece is in the right place
    else:
      goalIndex = piece -1
      goalIndex = goalIndex if goalIndex >=0 else 8
      
      # Essentially checks for if they're in different rows and columns
      x = abs((goalIndex/3) - (i/3))
      y = abs((goalIndex %3) - (i%3))
      
      distance = x+y
      # doubles what the Manhattan score would be for out of place tiles
      if distance > 2:
        if distance == 3:
          value += 4
          print 4
        if distance == 4:
          value += 8
          print 8
      else:
        value += distance
        print distance
  
  return value
  
# 1,2,3
# 4,5,6
# 7,8,0  
grid = [3,4,8,1,2,5,0,6,7]
# 2,2,3
# 1,1,1
# 2,2,2

# distance from ideal
# 2,2,3
# 1,1,1
# 2,2,2
print "total: %s"%customHeuristic(grid)