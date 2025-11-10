import random
import matplotlib.pyplot as plt
import csv 
from io import StringIO
columns = "Run Number, Lattice Length, Probability, Survival Time, Starting Position, Final Position"
with open("data.csv", 'w') as f:
    writer = csv.writer(f)
    writer.writerow(columns.split(", "))

finalLine = None
with open("data.csv", 'r') as r:
    for line in r: 
        if line.strip():
            finalLine = line.strip()
if finalLine:
    finalVal = finalLine[0]
    print(finalVal)
else:
    print("Error: File is empty or only contains blank lines. ")
    finalVal = None

def randomWalks(N, q):
    energy = 5
    time = 0
    pos = random.randint(0, N)
    startpos = pos
    while energy > 0:

        if pos == 0 or pos == N:
            
            while random.uniform(0.0, 1.0) <= q:
                
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

    return time, startpos, pos

def writeData(dataRow):
    with open("data.csv", 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(dataRow)

def prevRunNum():
    with open("data.csv", 'r') as f:
        allrows = list(csv.reader(f))
        if not allrows:
            finalVal = "File is empty"
        else:
            lastRow = allrows[-1]
            finalVal = lastRow[0]
        return finalVal

def monteCarloSim(num):
    survivalTimes=[]
    for i in range (num):
        time, startpos, pos = randomWalks(latticeLen, prob)
        survivalTimes.append(time)
        runnum = prevRunNum()
        currentRow = [runnum, latticeLen, prob, time, startpos, pos]
        writeData(currentRow)

    return survivalTimes

latticeLen = int(input("Enter lattice length: "))
prob = float(input("Enter probability: "))
resultTime = randomWalks(latticeLen, prob)
print(f"Total time taken is: {resultTime}")
simNum = int(input("Enter the number of simulations you would like to run: "))
survivalTimes =monteCarloSim(simNum)

plt.hist(survivalTimes)
plt.show()
