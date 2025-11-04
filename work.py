import random


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


latticeLen = int(input("Enter lattice length: "))
prob = float(input("Enter probability: "))
resultTime = randomWalks(latticeLen, prob)
print(f"Total time taken is: {resultTime}")
