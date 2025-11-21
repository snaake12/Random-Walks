import random
import matplotlib.pyplot as plt
import csv 
import numpy as np
import pandas as pd
from io import StringIO
import os
import matplotlib.cm as cm
import matplotlib.colors as colors
filename = "data.csv"
columns = ["Run Number", "Lattice Length", "Probability", "Survival Time", "Starting Position", "Final Position", "Initial Energy", "Maximum Time"]

def addColumnOne():
    df = pd.read_csv(filename)
    df['Maximum Energy'] = 1000
    df.to_csv(filename, index=False)

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
        #df_filtered = df[df['Starting Position']!=0]
        df_filtered = df[df['Starting Position']!=df['Lattice Length']]
        #df_filtered = df_filtered[(df_filtered['Lattice Length']>=27) & (df_filtered['Lattice Length']<=50)]
        meanDF = df_filtered.groupby(['Lattice Length', 'Probability']).agg(
            meanSurvivalTime = ('Survival Time', 'mean')
        ).reset_index()
    except FileNotFoundError:
        print("Error: file not found.")
        return
    except pd.errors.EmptyDataError:
        print("Error: file is empty.")
        return 
    #Plot 1, effect of lattice length
    probs = sorted(meanDF['Probability'].unique())
    cmapProb = cm.get_cmap('viridis')
    normProb = colors.Normalize(vmin=min(probs), vmax=max(probs))
    plt.figure(figsize=(12,5))

    plt.subplot(1,2,1)
    for prob in probs:
        subset = meanDF[meanDF['Probability'] == prob]
        plot_color = cmapProb(normProb(prob))
        plt.scatter(
            subset['Lattice Length'],
            subset['meanSurvivalTime'],
            color=plot_color,
            label = f'q={prob:.2f}'
        )
    plt.title('Effect of Lattice Length on Survival Time')
    plt.xlabel('Lattice Length ($N$)')
    plt.ylabel('Mean Survival Time')
    plt.legend(title ='Boundary Prob. (q)')
    plt.grid(True, linestyle= '--', alpha=0.6)   

    sm_prob = cm.ScalarMappable(cmap=cmapProb, norm=normProb)
    sm_prob.set_array([]) 
    cbar_prob = plt.colorbar(sm_prob, ax=plt.gca(), orientation='vertical', pad=0.05)
    cbar_prob.set_label('Boundary Probability ($q$)')
    #Plot 2, effect of probability
    plt.subplot(1,2,2)
    Nvals = sorted(meanDF['Lattice Length'].unique())
    cmapN = cm.get_cmap('plasma')
    normN = colors.Normalize(vmin=min(Nvals), vmax=max(Nvals))

    for Nval in Nvals:
        subset = meanDF[meanDF['Lattice Length']==Nval]
        plotColor = cmapN(normN(Nval))
        plt.scatter(
            subset['Probability'],
            subset['meanSurvivalTime'],
            color=plotColor,
            label = f'N={Nval}'
        )
    plt.title('Effect of Boundary Probability on Survival Time')
    plt.xlabel('Boundary Probability')
    plt.ylabel('Mean Survival Time')
    plt.legend(title= 'Lattice Length' )
    plt.grid(True, linestyle='--', alpha=0.6)
    sm_N = cm.ScalarMappable(cmap=cmapN, norm=normN)
    sm_N.set_array([])
    cbar_N = plt.colorbar(sm_N, ax=plt.gca(), orientation='vertical', pad=0.05)
    cbar_N.set_label('Lattice Length ($N$)')
    plt.tight_layout()
    plt.show()

def randomWalks(N, q, initialEnergy):
    energy = initialEnergy
    maxTime = 98
    time = 0
    pos = random.choice([0, N])
    startpos = pos
    while energy > 0 and time<maxTime:   
        if pos == 0 or pos == N: 
            while random.uniform(0, 1) <= q:
                if time>=maxTime:
                    break
                energy += 1
                time += 1
            if time>=maxTime:
                break
            
            energy -= 1
            time += 1
            if pos == 0:
                pos += 1

            elif pos == N:
                pos -= 1 
        else:
            moveUp = random.random() < 0.5
            energy-=1
            time+=1
            if moveUp:
                pos += 1

            else:
                pos -= 1


    return time, startpos, pos, maxTime

def monteCarloSim(num, N, q, initialEnergy):
    survivalTimes=[]
    runnum = runNum()
    for i in range (num):
        time, startpos, pos, maxTime = randomWalks(N, q, initialEnergy)
        survivalTimes.append(time)
        
        print("Adding", runnum, "th row to csv")
        currentRow = [runnum, N, q, time, startpos, pos, initialEnergy, maxTime]
        writeData(currentRow)
        runnum+=1

    return survivalTimes

createCSV()

#This section is required to populate the csv with the monte carlo simulations for the given lattice lengths and probabilities, since it has already been populated it is commented out#
#Nvalues = list(range(2,10))
#Qvalues = np.linspace(0.1, 0.9, 9)
"""
Nvalues = 4,5,6
Qvalues = 0.8, 0.83333, 0.857143
runsPerCombo = 10

for N in Nvalues:
    for q in Qvalues:
        monteCarloSim(runsPerCombo, N, q)
"""
monteCarloSim(1, 5, 0.7, 50)
#addColumnOne()
plotGraph()