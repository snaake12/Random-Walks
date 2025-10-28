import random
def randomWalks(N,q):
    energy = 0
    time = 0
    pos = random.randint(0, N)
    state = True
    while state:
        if time !=0 and energy == 0:
            state = False
            break
        if pos == 0 or pos == N:
            stays = True
            while stays == True:
                stays = random.random()<q
                energy +=1
                time+=1
        else:
            moveUp = random.random()<0.5
            if moveUp:
                pos+=1
                energy -=1
                time+=1
            else:
                pos-=1
                energy-=1
                time+=1
    return time
len = int(input("Enter lattice length: "))
prob =float(input("Enter probability: "))
resultTime = randomWalks(len, prob)
print(f"Total time taken is: {resultTime}")
            
