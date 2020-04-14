from math import comb
import random
import matplotlib.pyplot as plt
import numpy as np

def myFunction(n, m, p, k):
    
    # Check n requirements.
    if ((n % 4) != 0):
        print("Unable to divide n equally between four types of players.")
    else:
        
        # Set up data structure to hold player information
        # Format: [playerNumber, type, lastMove, grudger, cumulativePoints]
        # Note: 0 = T4T, 1 = Grudger, 2 = AC, 3 = AD
        playerPoints = []

        # Question 2a: 5% AD, 5% Grudger, 90% AC
        for a in range(0, n):
            typeToAppend = 2
            if (0 <= a <= 4):
                typeToAppend = 1
            elif (5 <= a <= 9):
                typeToAppend = 3
            playerPoints.append([a, typeToAppend, 0, 0, 0])

        # Question 2b: 1 TFT, 33 AC, 33 AD, 33 Grudger
        #for a in range(0, n):
        #    typeToAppend = 0
        #    if (0 <= a <= 32):
        #        typeToAppend = 1
        #    elif (33 <= a <= 65):
        #        typeToAppend = 2
        #    elif (66 <= a <= 98):
        #        typeToAppend = 3
        #    playerPoints.append([a, typeToAppend, 0, 0, 0])

        # Question 2c: 40 AD, 30 TFT,  20 AC, 10 Grudger
        #for a in range(0, n):
        #    typeToAppend = 3
        #    if (0 <= a <= 29):
        #        typeToAppend = 0
        #    elif (30 <= a <= 49):
        #        typeToAppend = 2
        #    elif (50 <= a <= 59):
        #        typeToAppend = 1
        #    playerPoints.append([a, typeToAppend, 0, 0, 0])
        
        # Initialize variables to store information across generations
        tftPercPlot = []
        gPercPlot = []
        acPercPlot = []
        adPercPlot = []
        tftTotalPlot = []
        gTotalPlot = []
        acTotalPlot = []
        adTotalPlot = []
        tftAvgPlot = []
        gAvgPlot = []
        acAvgPlot = []
        adAvgPlot = []
        totalPlot = []

        # Iterate through all generations
        for c in range(0, k):

            # At the beginning of each generation, reset relevant information
            for d in range(0, n):
                playerPoints[d][2] = 0 # Reset last move
                playerPoints[d][3] = 0 # Reset grudge toggle
                playerPoints[d][4] = 0 # Reset cumulative points (because new generation)

            # Simulate nC2 repeated games
            for a in range(0, n):
                for b in range(a, n):
                    if (b > a):
                        # Games are repeated m times
                        for e in range(0, m):
                            # Get the payoff for current players
                            roundResult = payoffMatrix(playerPoints[a], playerPoints[b], e)
                            playerPoints[a][4] = playerPoints[a][4] + roundResult[0]
                            playerPoints[b][4] = playerPoints[b][4] + roundResult[1]
                        # After each player pair, reset player's lastMove and grudge status
                        playerPoints[a][2] = 0
                        playerPoints[a][3] = 0
                        playerPoints[b][2] = 0
                        playerPoints[b][3] = 0
            
            
            # Initialize variables used to calculate output
            tftCount = 0
            gCount = 0
            acCount = 0
            adCount = 0
            tftSum = 0
            gSum = 0
            acSum = 0
            adSum = 0

            # Iterate through the player array and increment variables
            for a in range(0, n):
                if (playerPoints[a][1] == 0):
                    tftCount = tftCount + 1
                    tftSum = tftSum + playerPoints[a][4]
                elif (playerPoints[a][1] == 1):
                    gCount = gCount + 1
                    gSum = gSum + playerPoints[a][4]
                elif (playerPoints[a][1] == 2):
                    acCount = acCount + 1
                    acSum = acSum + playerPoints[a][4]
                elif (playerPoints[a][1] == 3):
                    adCount = adCount + 1
                    adSum = adSum + playerPoints[a][4]
                elif (playerPoints[a][1] == 4):
                    randomCount = randomCount + 1
                    randomSum = randomSum + playerPoints[a][4]
            tftPerc = tftCount / n * 100
            gPerc = gCount / n * 100
            acPerc = acCount / n * 100
            adPerc = adCount / n * 100
            totalSum = tftSum + gSum + acSum + adSum

            # Add data for graphing later
            tftPercPlot.append(tftPerc)
            gPercPlot.append(gPerc)
            acPercPlot.append(acPerc)
            adPercPlot.append(adPerc)
            tftTotalPlot.append(tftSum)
            gTotalPlot.append(gSum)
            acTotalPlot.append(acSum)
            adTotalPlot.append(adSum)
            totalPlot.append(totalSum)
            tftAvgPlot.append(round(weirdDiv(tftSum, tftCount) / (n - 1) / m, 2))
            gAvgPlot.append(round(weirdDiv(gSum, gCount) / (n - 1) / m, 2))
            acAvgPlot.append(round(weirdDiv(acSum, acCount) / (n - 1) / m, 2))
            adAvgPlot.append(round(weirdDiv(adSum, adCount) / (n - 1) / m, 2))

            # Toggle to print info generation by generation
            if (c > (-1)):
                print("Gen", (c + 1), ": T4T:", round(tftPerc, 1), "%, G:", round(gPerc, 1), "%, AC:", round(acPerc, 1), "%, AD:", round(adPerc, 1), "%")
                print("Gen", (c + 1), ": T4T:", tftSum, ", G:", gSum, ", AC:", acSum, ", AD:", adSum, ", Total:", totalSum)
                print("Gen", (c + 1), ": T4T:", round(weirdDiv(tftSum, tftCount) / (n - 1) / m, 2), ", G:", round(weirdDiv(gSum, gCount) / (n - 1) / m, 2), ", AC:", round(weirdDiv(acSum, acCount) / (n - 1) / m, 2), ", AD:", round(weirdDiv(adSum, adCount) / (n - 1) / m, 2), "")
                print("")
            
            # Rank the players according to their cumulative payoffs
            rankPlayerPoints = sorted(playerPoints, key = lambda x: x[4], reverse = True)
            howMany = int(p / 100 * n)

            # Choosing which players to replicate (Max)
            finalMaxSample = []
            maxValue = rankPlayerPoints[0][4]
            howManyMax = 0
            howManyMaxOffset = 0
            findingMaxs = True
            while (findingMaxs):
                for i in range(0, n):
                    if (rankPlayerPoints[i][4] == maxValue):
                        howManyMax = howManyMax + 1
                if (howManyMax >= howMany):
                    maxPlayerSample = rankPlayerPoints[howManyMaxOffset:howManyMax]
                    randomMaxSample = random.sample(maxPlayerSample, (howMany - howManyMaxOffset))
                    for j in range(0, len(randomMaxSample)):
                        finalMaxSample.append(randomMaxSample[j])
                    findingMaxs = False
                else:
                    for j in range(howManyMaxOffset, howManyMax):
                        finalMaxSample.append(rankPlayerPoints[j])
                    maxValue = rankPlayerPoints[howManyMax][4]
                    howManyMaxOffset = howManyMax

            # Choosing which players to remove (Min)
            finalMinSample = []
            minValue = rankPlayerPoints[n - 1][4]
            howManyMin = 0
            howManyMinOffset = 0
            stillFinding = True
            while (stillFinding):
                for a in range(0, n):
                    if (rankPlayerPoints[a][4] == minValue):
                        howManyMin = howManyMin + 1
                if (howManyMin >= howMany):
                    minPlayerSample = rankPlayerPoints[(n - howManyMin):(n - howManyMinOffset)]
                    randomMinSample = random.sample(minPlayerSample, (howMany - howManyMinOffset))
                    for b in range(0, len(randomMinSample)):
                        finalMinSample.append(randomMinSample[b])
                    stillFinding = False
                else:
                    for b in range(howManyMinOffset, howManyMin):
                        finalMinSample.append(rankPlayerPoints[n - 1 - b])
                    minValue = rankPlayerPoints[n - 1 - howManyMin][4]
                    howManyMinOffset = howManyMin

            # Replace randomly-selected min players with randomly-selected
            # max player strategies.
            for a in range(0, howMany):
                for b in range(0, n):
                    if (finalMinSample[a][0] == rankPlayerPoints[b][0]):
                        rankPlayerPoints[b][1] = finalMaxSample[a][1]

            playerPoints = rankPlayerPoints
            

        width = 0.35
        xPlot = range(1, 21)
        
        # Perc Bar Graph Code
        plt.figure(1)
        plt.axis([0, 21, 0, 100])
        plt.bar(xPlot, tftPercPlot, width, label = "T4T")
        plt.bar(xPlot, gPercPlot, width, bottom = tftPercPlot, label = "Grudger")
        plt.bar(xPlot, acPercPlot, width, bottom = np.array(tftPercPlot) + np.array(gPercPlot), label = "AC")
        plt.bar(xPlot, adPercPlot, width, bottom = np.array(tftPercPlot) + np.array(gPercPlot) + np.array(acPercPlot), label = "AD")
        plt.xticks(np.arange(1, 21, 1))
        plt.title("Type Percentage vs. Generations")
        plt.xlabel("Generations")
        plt.ylabel("Percentage of Population by Type")
        plt.legend(loc = "center left", bbox_to_anchor = (1, 0.5))

        # Total Bar Graph Code
        plt.figure(2)
        plt.bar(xPlot, tftTotalPlot, width, label = "T4T")
        plt.bar(xPlot, gTotalPlot, width, bottom = tftTotalPlot, label = "Grudger")
        plt.bar(xPlot, acTotalPlot, width, bottom = np.array(tftTotalPlot) + np.array(gTotalPlot), label = "AC")
        plt.bar(xPlot, adTotalPlot, width, bottom = np.array(tftTotalPlot) + np.array(gTotalPlot) + np.array(acTotalPlot), label = "AD")
        plt.xticks(np.arange(1, 21, 1))
        plt.title("Type Total Payoff vs. Generations")
        plt.xlabel("Generations")
        plt.ylabel("Total Payoff by Type")
        plt.legend(loc = "center left", bbox_to_anchor = (1, 0.5))

        # Avg Bar Graph Code
        plt.figure(3)
        r1 = xPlot
        r2 = [x + 0.2 for x in r1]
        r3 = [x + 0.2 for x in r2]
        r4 = [x + 0.2 for x in r3]
        plt.bar(r1, tftAvgPlot, width = 0.2, edgecolor = "white", label = "T4T")
        plt.bar(r2, gAvgPlot, width = 0.2, edgecolor = "white", label = "Grudger")
        plt.bar(r3, acAvgPlot, width = 0.2, edgecolor = "white", label = "AC")
        plt.bar(r4, adAvgPlot, width = 0.2, edgecolor = "white", label = "AD")
        plt.xticks(np.arange(1, 21, 1))
        plt.title("Type Avg Payoff vs. Generations")
        plt.xlabel("Generations")
        plt.ylabel("Avg Payoff by Type")
        plt.legend(loc = "center left", bbox_to_anchor = (1, 0.5))
        
        plt.show()
        

def payoffMatrix(a, b, r):
    # a and b are the player structures
    # get their types
    
    a_action = -1
    b_action = -1

    if (a[1] == 0):
        if (r == 0):
            a_action = 0
        else:
            a_action = b[2]
    elif (a[1] == 1): # If Player A is a Grudger
        if (a[3] == 1): # Check if holding a grudge
            a_action = 1 
        else :
            a_action = 0
    elif (a[1] == 2): # If Player A is AC
        a_action = 0
    elif (a[1] == 3): # IF Player A is AD
        a_action = 1
    elif (a[1] == 4): # If Player A is a random player
        a_action = random.randint(0, 1)

    if (b[1] == 0):
        if (r == 0):
            b_action = 0
        else:
            b_action = a[2]
    elif (b[1] == 1): # If Player B is a Grudger
        if (b[3] == 1): # Check if holding a grudge
            b_action = 1 
        else :
            b_action = 0
    elif (b[1] == 2):
        b_action = 0
    elif (b[1] == 3):
        b_action = 1
    elif (b[1] == 4):
        b_action = random.randint(0, 1)

    a[2] = a_action
    b[2] = b_action

    if (b_action == 1):
        a[3] = 1
    if (a_action == 1):
        b[3] = 1
    
    # Assume 0 = cooperate, 1 = defect
    if (a_action == 0):
        if (b_action == 0):
            return [3, 3]
        else:
            return [0, 5]
    else:
        if (b_action == 0):
            return [5, 0]
        else:
            return [1, 1]

def weirdDiv(n, d):
    #print(n, "-", d)
    return (n / d) if d else 0

myFunction(100, 5, 5, 20)

