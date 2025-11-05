import random
import matplotlib.pyplot as plt
import csv 
from io import StringIO
columns = "Run Number, Lattice Length, Probability, Survival Time, Starting Position, Final Position"
with open("data.csv", 'w') as f:
    writer = csv.writer(f)
    writer.writerow(columns.split(", "))

with open("data.csv", 'r') as r:
    for line in r: pass
    finalLine = list(line)
    finalVal = finalLine[0]
print(finalVal)

def randomWalks(N, q):
    energy = 5
    maxEn = 100
    time = 0
    pos = random.randint(0, N)
    while energy > 0:

        if pos == 0 or pos == N:
            
            while random.uniform(0.0, 1.0) <= q:
                if energy>=maxEn:
                    break
                energy += 1
                time += 1

            energy -= 1
            time += 1
            if pos == 0:
                pos += 1

            elif pos == N:
                pos -= 1

        else:
            moveUp = random.random() < 0.5
            if moveUp:
                pos += 1

            else:
                pos -= 1

    return time

def monteCarloSim(num):
    survivalTimes=[]
    for i in range (num):
        time = randomWalks(latticeLen, prob)
        survivalTimes.append(time)
    return survivalTimes

latticeLen = int(input("Enter lattice length: "))
prob = float(input("Enter probability: "))
resultTime = randomWalks(latticeLen, prob)
print(f"Total time taken is: {resultTime}")
simNum = int(input("Enter the number of simulations you would like to run: "))
survivalTimes =monteCarloSim(simNum)

plt.hist(survivalTimes)
plt.show()
