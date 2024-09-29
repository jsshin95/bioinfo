import random


sRandom = ""
for _ in range(500):
    n = random.randint(1,4)
    if n == 1 : sRandom += 'A'
    elif n == 2 : sRandom += 'T'
    elif n == 3 : sRandom += 'G'
    elif n == 4 : sRandom += 'C'

print(sRandom)