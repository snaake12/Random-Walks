import random
import matplotlib.pyplot as plt
import csv 
import numpy as np
import pandas as pd
from io import StringIO
import os

filename = "data.csv"
columns = ["Run Number", "Lattice Length", "Probability", "Survival Time", "Starting Position", "Final Position"]

def createCSV():
    #Writes column headers if the file does not exist or is empty
    if not os.path.exists(filename) or os.stat(filename).st_size==0:
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(columns)

def writeData(dataRow):
    #Writes a row of data to the csv
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(dataRow)

def runNum():
    #Fetches previous run number from the csv and returns the next value
    try:

        with open(filename, 'r', newline='') as f:
            reader = csv.reader(f)
            allrows = list(reader)
            if len(allrows)<=1:
                return 1
            else:
                lastRunNum = int(allrows[-1][0])
                return lastRunNum + 1
    except FileNotFoundError:
        return 1
    except (ValueError, IndexError):
        print("There was an error in reading the previous line. Starting to label the run numbers from 1.")
        return 1    

def plotGraph():
    try:
        df = pd.read_csv(filename)
        meanDF = df.groupby(['Lattice Length', 'Probability']).agg(
            meanSurvivalTime = ('Survival Time', 'mean')
        ).reset_index()
    except FileNotFoundError:
        print("Error: file not found.")
        return
    except pd.errors.EmptyDataError:
        print("Error: file is empty.")
        return 
    #Plot 1, effect of lattice length
    plt.figure(figsize=(12,5))

    plt.subplot(1,2,1)
    for prob in meanDF['Probability'].unique():
        subset = meanDF[meanDF['Probability'] == prob]
        plt.scatter(
            subset['Lattice Length'],
            subset['meanSurvivalTime'],
            label = f'q={prob:.2f}'
        )
    plt.title('Effect of Lattice Length on Survival Time')
    plt.xlabel('Lattice Length ($N$)')
    plt.ylabel('Mean Survival Time')
    plt.legend(title ='Boundary Prob. (q)')
    plt.grid(True, linestyle= '--', alpha=0.6)   

    #Plot 2, effect of probability
    plt.subplot(1,2,2)

    for Nval in meanDF['Lattice Length'].unique():
        subset = meanDF[meanDF['Lattice Length']==Nval]
        plt.scatter(
            subset['Probability'],
            subset['meanSurvivalTime'],
            label = f'N={Nval}'
        )
    plt.title('Effect of Boundary Probability on Survival Time')
    plt.xlabel('Boundary Stay Probability')
    plt.ylabel('Mean Survival Time')
    plt.legend(title= 'Lattice Length' )
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

def randomWalks(N, q):
    energy = 5
    maxTime = 1000000
    time = 0
    pos = random.randint(0, N)
    startpos = pos
    while energy >= 0:
        if time>= maxTime:
            break
        if pos == 0 or pos == N:
            
            while random.uniform(0, 1) <= q:
                if time>=maxTime:
                    break
                energy += 1
                time += 1
            if time>=maxTime:
                break
            if energy>0:
                energy -= 1
                time += 1
                if pos == 0:
                    pos += 1

                elif pos == N:
                    pos -= 1
            else:
                break

        elif energy>0:
            if time>=maxTime:
                break
            moveUp = random.random() < 0.5
            energy-=1
            time+=1
            if moveUp:
                pos += 1

            else:
                pos -= 1

        else:
            break

    return time, startpos, pos

def monteCarloSim(num, N, q):
    survivalTimes=[]
    runnum = runNum()
    for i in range (num):
        time, startpos, pos = randomWalks(N, q)
        survivalTimes.append(time)
        
        print("Adding", runnum, "th row to csv")
        currentRow = [runnum, N, q, time, startpos, pos]
        writeData(currentRow)
        runnum+=1

    return survivalTimes

createCSV()

#This section is required to populate the csv with the monte carlo simulations for the given lattice lengths and probabilities, since it has already been populated it is commented out#
"""
Nvalues = list(range(2,51))
Qvalues = np.linspace(0.01, 0.99, 99)
runsPerCombo = 50

for N in Nvalues:
    for q in Qvalues:
        monteCarloSim(runsPerCombo, N, q)
"""
plotGraph()