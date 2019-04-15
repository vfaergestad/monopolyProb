#   import lists from other files
from streets import streetsList
from chanceCards import chanceCardList
from comChestCards import comChestCardList
import random
import PySimpleGUI as Sg

# Creating input layout
layout = [
    [Sg.Text("How many throws do you want to make?")],
    [Sg.Input(1000)],
    [Sg.Checkbox("Show Moves"), Sg.Checkbox("Show Progress"), Sg.Checkbox("Show Streets Only")],
    [Sg.Checkbox("Jail", default=True), Sg.Checkbox("Triple Dice Jail", default=True),
     Sg.Checkbox("Community Chest Cards", default=True), Sg.Checkbox("Chance Cards", default=True)],
    [Sg.Text("(Showing Progress will make the calculation slower)")],
    [Sg.Submit("Run"), Sg.CloseButton("Exit")]
]

# Showing input window
window = Sg.Window("Monopoly Probability").Layout(layout)
button, values = window.Read()

if button == "Exit":
    exit()

# Defining user inputs
runs = int(values[0])
showMoves = values[1]
showProgress = values[2]
showOnlyStreets = values[3]
jail = values[4]
tripleJail = values[5]
comChestCards = values[6]
chanceCards = values[7]

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
progressShow = 0
firstThrow = 0

#   start loop
for _ in range(runs):
    same1 = False
    same2 = False
    #       throw dice
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    throw = dice1 + dice2
    throws += 1
    if showMoves:
        print("Rolled " + str(throw))

    #       Two of same dice
    if tripleJail:
        if dice1 == dice2 and same2:
            newPosIndex = 10
        if dice1 == dice2 and same1:
            same2 = True
        if dice1 == dice2:
            same1 = True

    #       general movement
    posIndex = newPosIndex
    pos = streetsList[posIndex]
    if showMoves:
        print("Moved from " + pos)
    if not same2:
        newPosIndex = posIndex + throw
    if same2:
        newPosIndex = 10
    if newPosIndex > 39:
        diff = newPosIndex - 40
        newPosIndex = 0 + diff

    #       move when chance card draw
    if chanceCards:
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
    if comChestCards:
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
    if jail:
        if newPosIndex == 30:
            newPosIndex = 10
        #       show end position
        if showMoves:
            print("Moved to " + newPos)

    #       show progress
    if showProgress:
        print(progress)

        progressLayout = [[Sg.Text('Progress', size=(20, 2), justification='center')],
                          [Sg.Text('', size=(10, 2), font=('Helvetica', 20), justification='center', key='_OUTPUT_')],
                          [Sg.T(' ' * 5), Sg.Quit()]]

        if firstThrow == 0:
            window = Sg.Window('Progress').Layout(progressLayout)

        event, values = window.Read(timeout=10)  # Please try and use a timeout when possible
        if event == 'Quit':  # if user closed the window using X or clicked Quit button
            exit()

        progress += 1
        progressList = list(str(progress))
        lookIndex = len(progressList) - 1
        if progressList[lookIndex] == "0":
            window.FindElement('_OUTPUT_').Update(progress)
            firstThrow = 1



#   create Probability list
for x in streetsList:
    streetOccur = resultList.count(x)
    streetProb = "%.2f" % float(float(streetOccur / throws) * 100)
    probList.append(streetProb)

#   delete all non-streets
if showOnlyStreets:
    del probList[38]
    del probList[36]
    del probList[33]
    del probList[7]
    del probList[30]
    del probList[22]
    del probList[20]
    del probList[17]
    del probList[10]
    del probList[4]
    del probList[2]
    del probList[0]

    del streetsList[38]
    del streetsList[36]
    del streetsList[33]
    del streetsList[30]
    del streetsList[22]
    del streetsList[20]
    del streetsList[17]
    del streetsList[10]
    del streetsList[7]
    del streetsList[4]
    del streetsList[2]
    del streetsList[0]

#   sort, zip and reverse results
resultsFinal = sorted(zip(probList, streetsList))
resultsFinal.reverse()

#   Show results
print('Prob \t\tStreet')
for prob, street in resultsFinal:
    print(str(prob) + '        ' + street)

showResultsList = []
for prob, street in resultsFinal:
    showResultsList.append(str(prob) + '      ' + street)

if showOnlyStreets:
    resultsLayout = [
                    [Sg.Text('Prob \t\t\tStreet')],
                    [Sg.Text(showResultsList[0], size=(15, 1)), Sg.Text(showResultsList[14])],
                    [Sg.Text(showResultsList[1], size=(15, 1)), Sg.Text(showResultsList[15])],
                    [Sg.Text(showResultsList[2], size=(15, 1)), Sg.Text(showResultsList[16])],
                    [Sg.Text(showResultsList[3], size=(15, 1)), Sg.Text(showResultsList[17])],
                    [Sg.Text(showResultsList[4], size=(15, 1)), Sg.Text(showResultsList[18])],
                    [Sg.Text(showResultsList[5], size=(15, 1)), Sg.Text(showResultsList[19])],
                    [Sg.Text(showResultsList[6], size=(15, 1)), Sg.Text(showResultsList[20])],
                    [Sg.Text(showResultsList[7], size=(15, 1)), Sg.Text(showResultsList[21])],
                    [Sg.Text(showResultsList[8], size=(15, 1)), Sg.Text(showResultsList[22])],
                    [Sg.Text(showResultsList[9], size=(15, 1)), Sg.Text(showResultsList[23])],
                    [Sg.Text(showResultsList[10], size=(15, 1)), Sg.Text(showResultsList[24])],
                    [Sg.Text(showResultsList[11], size=(15, 1)), Sg.Text(showResultsList[25])],
                    [Sg.Text(showResultsList[12], size=(15, 1)), Sg.Text(showResultsList[26])],
                    [Sg.Text(showResultsList[13], size=(15, 1)), Sg.Text(showResultsList[27])],
                    ]
else:
    resultsLayout = [
                    [Sg.Text('Prob \t\t\tStreet')],
                    [Sg.Text(showResultsList[0], size=(15, 1)), Sg.Text(showResultsList[20])],
                    [Sg.Text(showResultsList[1], size=(15, 1)), Sg.Text(showResultsList[21])],
                    [Sg.Text(showResultsList[2], size=(15, 1)), Sg.Text(showResultsList[22])],
                    [Sg.Text(showResultsList[3], size=(15, 1)), Sg.Text(showResultsList[23])],
                    [Sg.Text(showResultsList[4], size=(15, 1)), Sg.Text(showResultsList[24])],
                    [Sg.Text(showResultsList[5], size=(15, 1)), Sg.Text(showResultsList[25])],
                    [Sg.Text(showResultsList[6], size=(15, 1)), Sg.Text(showResultsList[26])],
                    [Sg.Text(showResultsList[7], size=(15, 1)), Sg.Text(showResultsList[26])],
                    [Sg.Text(showResultsList[8], size=(15, 1)), Sg.Text(showResultsList[28])],
                    [Sg.Text(showResultsList[9], size=(15, 1)), Sg.Text(showResultsList[29])],
                    [Sg.Text(showResultsList[10], size=(15, 1)), Sg.Text(showResultsList[30])],
                    [Sg.Text(showResultsList[11], size=(15, 1)), Sg.Text(showResultsList[31])],
                    [Sg.Text(showResultsList[12], size=(15, 1)), Sg.Text(showResultsList[32])],
                    [Sg.Text(showResultsList[13], size=(15, 1)), Sg.Text(showResultsList[33])],
                    [Sg.Text(showResultsList[14], size=(15, 1)), Sg.Text(showResultsList[34])],
                    [Sg.Text(showResultsList[15], size=(15, 1)), Sg.Text(showResultsList[35])],
                    [Sg.Text(showResultsList[16], size=(15, 1)), Sg.Text(showResultsList[36])],
                    [Sg.Text(showResultsList[17], size=(15, 1)), Sg.Text(showResultsList[37])],
                    [Sg.Text(showResultsList[18], size=(15, 1)), Sg.Text(showResultsList[38])],
                    [Sg.Text(showResultsList[19], size=(15, 1)), Sg.Text(showResultsList[39])],
                    ]

resultWindow = Sg.Window("Results").Layout(resultsLayout)
resultWindow.Read()
