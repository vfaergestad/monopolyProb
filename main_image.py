#   import lists from other files
from streets import streetsList
from streets import street_colors
from chanceCards import chanceCardList
from comChestCards import comChestCardList
import random
import PySimpleGUI as Sg
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
from tqdm import tqdm

style.use("ggplot")

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
street_occur_list = []

#   defining original values for different variables
newPosIndex = 0
throws = 0
chanceCardsDrawn = 0
comChestCardsDrawn = 0
progress = 0
firstThrow = 0

#   start loop
for _ in tqdm(range(runs)):
    same1 = False
    same2 = False
    #       throw dice
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    throw = dice1 + dice2
    throws += 1

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

    #   create Probability list
    for x in streetsList:
        streetOccur = resultList.count(x)
        street_occur_list.append(str(streetOccur))
        streetProb = "%.2f" % float(float(streetOccur / throws) * 100)
        probList.append(streetProb)

    #   sort, zip and reverse results
    resultsFinal = sorted(zip(probList, streetsList))
    resultsFinal.reverse()

    results_bar = sorted(zip(probList, streetsList, street_colors, street_occur_list))

    common_streets = [topic[1] for topic in results_bar]
    y_pos = np.arange(len(common_streets))
    street_prob_1 = [topic[0] for topic in results_bar]
    street_prob = []
    for x in street_prob_1:
        street_prob.append(float(x))
    bar_color = [topic[2] for topic in results_bar]
    street_occur_1 = [topic[3] for topic in results_bar]
    street_occur = []
    for x in street_occur_1:
        street_occur.append(int(x))

    plt.figure(figsize=(12, 7))
    plt.bar(y_pos, street_prob, align="center", alpha=1, color=bar_color)

    plt.xticks(y_pos, common_streets, rotation="vertical")
    plt.ylabel("Probability %")

    for i in range(len(y_pos)):
        plt.text(x=y_pos[i]-0.1, y=street_prob[i] + 0.1, s=street_occur[i], size=6, rotation="vertical")

    plt.title(f"Monopoly Streets Probability \n {runs} throws")
    plt.savefig(f"graph_video/images/{throws}.png")
    plt.close()

    probList = []
    street_occur = []
    street_prob = []


