import array
import random

allClassInfo = {
    "SLA100A": [50, ("Glen", "Lock", "Banks", "Zeldin"), ("Numen", "Richards")],
    "SLA100B": [50, ("Glen", "Lock", "Banks", "Zeldin"), ("Numen", "Richards")],
    "SLA191A": [50, ("Glen", "Lock", "Banks", "Zeldin"), ("Numen", "Richards")],
    "SLA191B": [50, ("Glen", "Lock", "Banks", "Zeldin"), ("Numen", "Richards")],
    "SLA201": [50, ("Glen", "Banks", "Zeldin", "Shaw"), ("Numen", "Richards", "Singer")],
    "SLA291": [50, ("Lock", "Banks", "Zeldin", "Singer"), ("Numen", "Richards", "Shaw", "Tyler")],
    "SLA303": [60, ("Glen", "Zeldin", "Banks"), ("Numen", "Singer", "Shaw")],
    "SLA304": [25, ("Glen", "Banks", "Tyler"), ("Numen", "Singer", "Shaw", "Richards", "Uther", "Zeldin")],
    "SLA394": [20, ("Tyler", "Singer"), ("Richards", "Zeldin")],
    "SLA449": [60, ("Tyler", "Singer", "Shaw"), ("Zeldin", "Uther")],
    "SLA451": [100, ("Tyler", "Singer", "Shaw"), ("Zeldin", "Uther", "Richards", "Banks")]
    }


allFac = {
    "Lock",
    "Glen",
    "Banks",
    "Richards",
    "Shaw",
    "Singer",
    "Uther",
    "Numen",
    "Zeldin",
    "Tyler"
    }

rooms = {
    "Slater 003": 45,
    "Roman 216": 30,
    "Loft 206": 75,
    "Roman 201": 50,
    "Loft 310": 108,
    "Beach 201": 60,
    "Beach 301": 75,
    "Logos 325": 450,
    "Frank 119": 60
    }

times = {
    "10AM",
    "11AM",
    "12PM",
    "1PM",
    "2PM",
    "3PM"
    }

def randomClassSchedule():
    temp_class = [None] * 44
    temp_class[0] = "SLA100A"
    temp_class[4] = "SLA100B"
    temp_class[8] = "SLA191A"
    temp_class[12] = "SLA191B"
    temp_class[16] = "SLA201"
    temp_class[20] = "SLA291"
    temp_class[24] = "SLA303"
    temp_class[28] = "SLA304"
    temp_class[32] = "SLA394"
    temp_class[36] = "SLA449"
    temp_class[40] = "SLA451"
    for x in range(0,44,4):
        temp_class[x+1] = random.choice(list(allFac))
        temp_class[x+2] = random.choice(list(rooms.keys()))
        temp_class[x+3] = random.choice(list(times))
    return temp_class

def timeMath(t1, t2):
    difference = 0
    if(t1 == "9AM"):
        difference += 9
    elif(t1 == "10AM"):
        difference += 10
    elif(t1 == "11AM"):
        difference += 11
    elif(t1 == "12PM"):
        difference += 12
    elif(t1 == "1PM"):
        difference += 13
    elif(t1 == "2PM"):
        difference += 14
    elif(t1 == "3PM"):
        difference += 15

    if(t2 == "9AM"):
        difference -= 9
    elif(t2 == "10AM"):
        difference -= 10
    elif(t2 == "11AM"):
        difference -= 11
    elif(t2 == "12PM"):
        difference -= 12
    elif(t2 == "1PM"):
        difference -= 13
    elif(t2 == "2PM"):
        difference -= 14
    elif(t2 == "3PM"):
        difference -= 15
    return abs(difference)

def fitnessFunction(array):
    #Initalize score to 0
    tempScore = 0
    #Check if a class is scheduled at the same time AND room as another class
    for x in range(0,44,4):
        for y in range(x+4, 44, 4):
            if((array[x+2] == array[y+2]) and (array[x+3] == array[y+3])):
                tempScore -= .5
                #Check statement to see if it works. WORKS AS OF 10/16/24
                #print(array[x+2] + " and " + array[y+2] + ". Time: " + array[x+3] +" and " + array[y+3] + "Score: " + str(tempScore))


    #Check room size for classes
    for x in range(0,44,4):
        #Too small for expected enrollment
        if(allClassInfo[array[x]][0] > rooms[array[x+2]]):
            tempScore -= .5
        #Room is greater than 3*expected
        elif(rooms[array[x+2]] > (3*allClassInfo[array[x]][0])):
            tempScore -= .2
        #Room is greater than 6*expected
        elif(rooms[array[x+2]] > (6*allClassInfo[array[x]][0])):
            tempScore -= .4
        else:
            tempScore += .3
    
    #Is facilitator preferred or not
    for x in range(0,44,4):
        if(array[x+1] in allClassInfo[array[x]][1]):
            tempScore += .5
        elif(array[x+1] in allClassInfo[array[x]][2]):
            tempScore += .2
        else:
            tempScore -= .1

    #Facilitator load
    #print("CHECKING FACILITATOR LOAD")
    #Facilitator has 4+ classes overall
    for x in allFac:
        if(array.count(x) >= 4):
            tempScore -= .5

    #Facilitator has 2+ classes at same time
    for x in allFac:
        timeChecker = []
        for y in range(0,44,4):
            if(array[y+1] == x):
                if(array[y+3] in timeChecker):
                    tempScore -= .2
                    timeChecker.append(array[y+3])
                    #print("Duplicate time for " + x + " at " + array[y+3])
                    break
                else:
                    timeChecker.append(array[y+3])
                
        #If it went through everything and never found a dupe time, the length will be equal to set length
        #print(str(len(timeChecker)) + " " + str(len(set(timeChecker))))
        if(len(timeChecker) == len(set(timeChecker))):
            tempScore += .2

    for x in list(allFac)[:-1]:
        if(array.count(x) == 1 or array.count(x) == 2):
            #print(x + " has only 1 or two classes")
            tempScore -= .4

    #If a facilitator has 2 classes in a row, +.5 UNLESS ones in Beach/Roman and the other isnt then -.4
    #Generate temp array of times and rooms
    for x in allFac:
        timeChecker = []
        for y in range (0,44,4):
            if(array[y+1] == x):
                timeChecker.append(array[y+3])
                timeChecker.append(array[y+2])
        #For each time found for professor, compare it to other times
        for y in range (0,len(timeChecker), 2):
            for z in range(y+2, len(timeChecker), 2):
                #If they are consecutive, diff = 1
                if(timeMath(timeChecker[y], timeChecker[z]) == 1):
                    #if ones in roman and the other isnt, -.4
                    if "Roman" in timeChecker[y+1] and "Roman" not in timeChecker[z+1] or "Roman" not in timeChecker[y+1] and "Roman" in timeChecker[z+1]:
                        tempScore -= .4
                    #if ones in beach and the other isnt, -.4
                    elif "Beach" in timeChecker[y+1] and "Beach" not in timeChecker[z+1] or "Beach" not in timeChecker[y+1] and "Beach" in timeChecker[z+1]:
                        tempScore -= .4
                    #otherwise +.5
                    else:
                        tempScore += .5

    #SLA100 A and B are > 4 hours apart
    if(timeMath(array[3], array[7]) > 4):
        #print("SLA100A and B are far apart")
        tempScore += .5
    #if theyre in the same timeslot
    elif(array[3] == array[7]):
        #print("SLA100A and B are at the same time")
        tempScore -= .5

    if(timeMath(array[11], array[15]) > 4):
        #print("SLA191A and B are far apart")
        tempScore += .5
    elif(array[11] == array[15]):
        #print("SLA191A and B are at the same time")
        tempScore -= .5

    #A section of SLA 191 and a section of SLA 101 are overseen in consecutive time slots. Lots of extra stuff
    if(timeMath(array[3],array[11]) == 1): #100A and 191A
        if "Roman" in array[2] and "Roman" not in array[10] or "Roman" not in array[2] and "Roman" in array[10]:
            tempScore -= .4
        elif "Beach" in array[2] and "Beach" not in array[10] or "Beach" not in array[2] and "Beach" in array[10]:
            tempScore -= .4
        else:
            tempScore += .5
    if(timeMath(array[3],array[15]) == 1): #100A and 191B
        if "Roman" in array[2] and "Roman" not in array[14] or "Roman" not in array[2] and "Roman" in array[14]:
            tempScore -= .4
        elif "Beach" in array[2] and "Beach" not in array[14] or "Beach" not in array[2] and "Beach" in array[14]:
            tempScore -= .4
        else:
            tempScore += .5
    if(timeMath(array[7],array[11]) == 1): #100B and 191A
        if "Roman" in array[6] and "Roman" not in array[10] or "Roman" not in array[6] and "Roman" in array[10]:
            tempScore -= .4
        elif "Beach" in array[6] and "Beach" not in array[10] or "Beach" not in array[6] and "Beach" in array[10]:
            tempScore -= .4
        else:
            tempScore += .5
    if(timeMath(array[7],array[15]) == 1): #100B and 191B
        if "Roman" in array[6] and "Roman" not in array[14] or "Roman" not in array[6] and "Roman" in array[14]:
            tempScore -= .4
        elif "Beach" in array[6] and "Beach" not in array[14] or "Beach" not in array[6] and "Beach" in array[14]:
            tempScore -= .4
        else:
            tempScore += .5
    #A section of SLA 191 and a section of SLA 101 are taught separated by 1 hour. +.25
    if(timeMath(array[3],array[11]) == 2): #100A and 191A
        tempScore += .25
    if(timeMath(array[3],array[15]) == 2): #100A and 191B
        tempScore += .25
    if(timeMath(array[7],array[11]) == 2): #100B and 191A
        tempScore += .25
    if(timeMath(array[7],array[15]) == 2): #100B and 191B
        tempScore += .25
    #A section of SLA 191 and a section of SLA 101 are taught in the same time slot: -.25
    if(timeMath(array[3],array[11]) == 0): #100A and 191A
        tempScore -= .25
    if(timeMath(array[3],array[15]) == 0): #100A and 191B
        tempScore -= .25
    if(timeMath(array[7],array[11]) == 0): #100B and 191A
        tempScore -= .25
    if(timeMath(array[7],array[15]) == 0): #100B and 191B
        tempScore -= .25
    #return the fitness score for schedule
    return tempScore

def crossbreedSchedules(array1, array2):
    splitter = random.randrange(0,44)
    tempArray1 = [None] * 44
    tempArray2 = [None] * 44
    for x in range(0,splitter):
        tempArray1[x] = array1[x]
        tempArray2[x] = array2[x]
    for x in range(splitter, 44):
        tempArray1[x] = array2[x]
        tempArray2[x] = array1[x]

    return tempArray1, tempArray2

def mutateSchedule(array, mutationRate):
    #Mutation rate
    for x in range(0,44):
        mutate = random.uniform(0,1000)
        if(mutate <= mutationRate):
            if(x % 4 == 1):
                array[x] = random.choice(list(allFac))
            if(x % 4 == 2):
                array[x] = random.choice(list(rooms.keys()))
            if(x % 4 == 3):
                array[x] = random.choice(list(times))
    

#BEGIN RANDOM POPULATION HERE
schedulePopulation = [[None, None] for _ in range(500)]
for x in range(500):
    schedulePopulation[x][0] = randomClassSchedule()

# #Print a schedule here
# for x in schedulePopulation[0][0]:
#     print(x)
genCount = 0
averageFitness = 0
prevAvgFitness = 0
userIn = "Y"
mutationRate = 10
while(userIn != "N"):

    #Evaluate the current generation
    for x in range(500):
        schedulePopulation[x][1] = fitnessFunction(schedulePopulation[x][0])
        #print(str(x) + ": " + str(schedulePopulation[x][1]))

    schedulePopulation = sorted(schedulePopulation, key=lambda x: x[1], reverse=True)

    genCount += 1
    print("Generation: " + str(genCount))
    print("Mutation Rate: " + str(mutationRate))
    for x in range(500):
        print(str(x) + ": " + str(schedulePopulation[x][1]))
        averageFitness += schedulePopulation[x][1]

    averageFitness /= 500

    if(genCount > 100 and userIn != "N"):
        userIn = input("Type N to stop")

    if(genCount < 100 or userIn != "N"):
        #Clear the bottom 50%
        for x in range (250, 500):
            schedulePopulation[x][0] = [None]
            schedulePopulation[x][1] = None

        for x in range (0, 250, 2):
            schedulePopulation[x+250][0], schedulePopulation[x+251][0] = crossbreedSchedules(schedulePopulation[x][0], schedulePopulation[x+1][0])
            
            mutateSchedule(schedulePopulation[x+250][0], mutationRate)
            mutateSchedule(schedulePopulation[x+251][0], mutationRate)
        if(averageFitness < 1.01*prevAvgFitness and genCount > 99):
            userIn = "N"
            #PRINT BEST FITNESS
            print("Best Fitness: " + str(schedulePopulation[0][1]))
            #PRINT TO FILE
            with open("CS461Output.txt", "w") as text:
                for x in range(0,44):
                    text.write(schedulePopulation[0][0][x] + "\n")

        if(averageFitness > prevAvgFitness):
            mutationRate /= 2
        # else:
        #     mutationRate *= 2
        prevAvgFitness = averageFitness
