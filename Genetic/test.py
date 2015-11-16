import random

c = 'SKrayd'
d = 'Duckie'
p = random.choice(range(len(c)))
cd = c[0:p] + d[p:]
print cd