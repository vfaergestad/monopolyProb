while True:
#   import lists from other files
    from streets import streetsList
    from chanceCards import chanceCardList
    from comChestCards import comChestCardList
    import random

#   creating copies of chance- and comChestLists
    copyChanceCardList = list(chanceCardList)
    copyComChestCardList = list(comChestCardList)

#   creating the Result list and the Probabilitylist
    resultList = []
    probList = []

#   User input Throws amount and to show or not show each move
    print("Welcome to this Monopoly Probability program. How many throws do you want to make?")
    runs = int(input())

    print("Do you want to see all the moves? Y/N (Not recommended for more than 100 moves.)")
    answ = input()
    if answ == "Y":
        show = True
    else:
        show = False

#   defining original values for different variables
    newPosIndex = 0
    throws = 0
    chanceCardsDrawn = 0
    comChestCardsDrawn = 0
    progress = 0

#   start loop
    for _ in range(runs):
        same1 = False
        same2 = False
#       throw dice
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        throw = dice1 + dice2
        throws += 1
        if show == True:
            print(throw)

#       Two of same dice
        if dice1 == dice2 and same2 == True:
            newPosIndex = 10
        if dice1 == dice2 and same1 == True:
            same2 == True
        if dice1 == dice2:
            same1 == True

#       general movement
        posIndex = newPosIndex
        pos = streetsList[posIndex]
        if show == True:
            print(pos)
        if same2 == False:
            newPosIndex = posIndex + throw
        if newPosIndex > 39:
            diff = newPosIndex - 40
            newPosIndex = 0 + diff

#       move when chance card draw
        if newPosIndex == 7 or newPosIndex == 22 or newPosIndex == 36:
            cardDraw = random.randint(0, (len(chanceCardList)-1))
            if cardDraw == 0:
                newPosIndex = 0
            if cardDraw == 1:
                newPosIndex = 21
            if cardDraw == 2:
                newPosIndex = 11
            if cardDraw == 3:
                if newPosIndex == 7 or newPosIndex == 36:
                    newPosIndex = 12
                if newPosIndex == 22:
                    newPosIndex = 28
            if cardDraw == 4 or cardDraw == 5:
                if newPosIndex == 7:
                    newPosIndex = 15
                if newPosIndex == 22:
                    newPosIndex = 25
                if newPosIndex == 36:
                    newPosIndex = 5
            if cardDraw == 6:
                newPosIndex -= 3
            if cardDraw == 7:
                newPosIndex = 10
            chanceCardList.pop(cardDraw)
            chanceCardsDrawn += 1
            if chanceCardsDrawn == 16:
                chanceCardList = list(copyChanceCardList)
                chanceCardsDrawn = 0

#       move when com chest cards draw
        if newPosIndex == 2 or newPosIndex == 17 or newPosIndex == 33:
            cardDraw = random.randint(0, (len(comChestCardList) - 1))
            if cardDraw == 0:
                newPosIndex = 0
            if cardDraw == 1:
                newPosIndex = 10
            comChestCardList.pop(cardDraw)
            comChestCardsDrawn += 1
            if comChestCardsDrawn == 16:
                comChestCardList = list(copyComChestCardList)
                comChestCardsDrawn = 0

#       find landing spot and add to result list
        newPos = streetsList[newPosIndex]
        resultList.append(newPos)

#       move - land on prison
        if newPosIndex == 30:
            newPosIndex = 10
#       show end position
        if show == True:
            print(newPos)

#       show progress
        progress += 1
        print(progress)

#   create Probability list
    for x in streetsList:
        streetOccur = resultList.count(x)
        streetProb = float(float(streetOccur / throws) * 100)
        probList.append(streetProb)

#   sort, zip and reverse results
    resultsFinal = sorted(zip(probList, streetsList))
    resultsFinal.reverse()

#   Show results
    print('Prob \t\tStreet')
    for prob, street in resultsFinal:
        print(str(prob) + '\t\t\t' + street)

#   run again?
    print("Want to run the program again? Y/N")
    answ = input()
    if answ == "Y":
        print("Letsgo then")
    else:
        print("k bye")
        exit()