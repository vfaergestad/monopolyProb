#   import lists from other files
from streets import streetsList
from chanceCards import chanceCardList
from comChestCards import comChestCardList
import random
import PySimpleGUI as sg

layout = [
    [sg.Text("How many throws do you want to make?")],
    [sg.Input()],
    [sg.Checkbox("Show Moves"), sg.Checkbox("Show Progress"), sg.Checkbox("Jail")],
    [sg.Checkbox("Triple Dice Jail"), sg.Checkbox("Community Chest Cards"), sg.Checkbox("Chance Cards")],
    [sg.Text("(Showing Progress will make the calculation slower)")],
    [sg.Submit("Run"), sg.ReadButton("Read")]
]


window = sg.Window("Test ass").Layout(layout)
button, values = window.Read()

#   User input Throws amount and to show or not show each move

runs = int(values[0])
showMoves = values[1]
showProgress = values[2]
jail = values[3]
tripleJail = values[4]
comChestCards = values[5]
chanceCards = values[6]

#   creating copies of chance- and comChestLists
copyChanceCardList = list(chanceCardList)
copyComChestCardList = list(comChestCardList)

#   creating the Result list and the ProbabilityList
resultList = []
probList = []

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
    if showMoves == True:
        print("Rolled " + str(throw))

#       Two of same dice
    if tripleJail == True:
        if dice1 == dice2 and same2 == True:
            newPosIndex = 10
        if dice1 == dice2 and same1 == True:
            same2 = True
        if dice1 == dice2:
            same1 = True

#       general movement
    posIndex = newPosIndex
    pos = streetsList[posIndex]
    if showMoves == True:
        print("Moved from " + pos)
    if same2 == False:
        newPosIndex = posIndex + throw
    if same2 == True:
        newPosIndex = 10
    if newPosIndex > 39:
        diff = newPosIndex - 40
        newPosIndex = 0 + diff

#       move when chance card draw
    if chanceCards == True:
        if newPosIndex == 7 or newPosIndex == 22 or newPosIndex == 36:
            cardDraw = random.randint(0, (len(chanceCardList)-1))
            if cardDraw == 0:
                newPos = streetsList[newPosIndex]
                resultList.append(newPos)
                newPosIndex = 0
            if cardDraw == 1:
                newPos = streetsList[newPosIndex]
                resultList.append(newPos)
                newPosIndex = 21
            if cardDraw == 2:
                newPos = streetsList[newPosIndex]
                resultList.append(newPos)
                newPosIndex = 11
            if cardDraw == 3:
                if newPosIndex == 7 or newPosIndex == 36:
                    newPos = streetsList[newPosIndex]
                    resultList.append(newPos)
                    newPosIndex = 12
                if newPosIndex == 22:
                    newPos = streetsList[newPosIndex]
                    resultList.append(newPos)
                    newPosIndex = 28
            if cardDraw == 4 or cardDraw == 5:
                if newPosIndex == 7:
                    newPos = streetsList[newPosIndex]
                    resultList.append(newPos)
                    newPosIndex = 15
                if newPosIndex == 22:
                    newPos = streetsList[newPosIndex]
                    resultList.append(newPos)
                    newPosIndex = 25
                if newPosIndex == 36:
                    newPos = streetsList[newPosIndex]
                    resultList.append(newPos)
                    newPosIndex = 5
            if cardDraw == 6:
                newPos = streetsList[newPosIndex]
                resultList.append(newPos)
                newPosIndex -= 3
            if cardDraw == 7:
                newPos = streetsList[newPosIndex]
                resultList.append(newPos)
                newPosIndex = 10
            chanceCardList.pop(cardDraw)
            chanceCardsDrawn += 1
            if chanceCardsDrawn == 16:
                chanceCardList = list(copyChanceCardList)
                chanceCardsDrawn = 0

#       move when com chest cards draw
    if comChestCards == True:
        if newPosIndex == 2 or newPosIndex == 17 or newPosIndex == 33:
            cardDraw = random.randint(0, (len(comChestCardList) - 1))
            if cardDraw == 0:
                newPos = streetsList[newPosIndex]
                resultList.append(newPos)
                newPosIndex = 0
            if cardDraw == 1:
                newPos = streetsList[newPosIndex]
                resultList.append(newPos)
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
    if jail == True:
        if newPosIndex == 30:
            newPosIndex = 10
    #       show end position
        if showMoves == True:
            print("Moved to " + newPos)

#       show progress
    if showProgress == True:
        sg.OneLineProgressMeter('One Line Meter Example', progress, runs, 'key')
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
def Results():
    print('Prob \t\tStreet')
    for prob, street in resultsFinal:
        print(str(prob) + '\t\t\t' + street)

sg.Popup(Results(), values)

#   run again?
#    print("Want to run the program again? Y/N")
#    answ = input()
#    if answ == "Y":
#        print("Letsgo then")
#    else:
#        print("k bye")
#        exit()