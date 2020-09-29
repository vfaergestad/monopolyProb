#   import lists from other files
from streets import street_list
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
    [Sg.Checkbox("Show Moves"), Sg.Checkbox("Show Progress"), Sg.Checkbox("Show Buy-Able Streets Only")],
    [Sg.Text("Rules:")],
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

if button == "Run":
    Sg.Window.Close(window)

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
prob_list = []
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
    pos = street_list[posIndex]
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
                newPos = street_list[newPosIndex]
                resultList.append(newPos)
                newPosIndex = 0
            if cardDraw == 1:
                newPos = street_list[newPosIndex]
                resultList.append(newPos)
                newPosIndex = 21
            if cardDraw == 2:
                newPos = street_list[newPosIndex]
                resultList.append(newPos)
                newPosIndex = 11
            if cardDraw == 3:
                if newPosIndex == 7 or newPosIndex == 36:
                    newPos = street_list[newPosIndex]
                    resultList.append(newPos)
                    newPosIndex = 12
                if newPosIndex == 22:
                    newPos = street_list[newPosIndex]
                    resultList.append(newPos)
                    newPosIndex = 28
            if cardDraw == 4 or cardDraw == 5:
                if newPosIndex == 7:
                    newPos = street_list[newPosIndex]
                    resultList.append(newPos)
                    newPosIndex = 15
                if newPosIndex == 22:
                    newPos = street_list[newPosIndex]
                    resultList.append(newPos)
                    newPosIndex = 25
                if newPosIndex == 36:
                    newPos = street_list[newPosIndex]
                    resultList.append(newPos)
                    newPosIndex = 5
            if cardDraw == 6:
                newPos = street_list[newPosIndex]
                resultList.append(newPos)
                newPosIndex -= 3
            if cardDraw == 7:
                newPos = street_list[newPosIndex]
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
                newPos = street_list[newPosIndex]
                resultList.append(newPos)
                newPosIndex = 0
            if cardDraw == 1:
                newPos = street_list[newPosIndex]
                resultList.append(newPos)
                newPosIndex = 10
            comChestCardList.pop(cardDraw)
            comChestCardsDrawn += 1
            if comChestCardsDrawn == 16:
                comChestCardList = list(copyComChestCardList)
                comChestCardsDrawn = 0

    #       find landing spot and add to result list
    newPos = street_list[newPosIndex]
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

        event, values = window.Read(timeout=0)
        if event == 'Quit':
            exit()

        progress += 1
        """progressList = list(str(progress))
        lookIndex = len(progressList) - 1
        lookIndex2 = len(progressList) - 2
        if progressList[lookIndex] == "0" and progressList[lookIndex2] == "0":"""
        window.FindElement('_OUTPUT_').Update(progress)
        firstThrow = 1

#   create Probability list
for x in street_list:
    streetOccur = resultList.count(x)
    street_occur_list.append(str(streetOccur))
    streetProb = "%.2f" % float(float(streetOccur / throws) * 100)
    prob_list.append(streetProb)


#   delete all non-streets
if showOnlyStreets:
    del prob_list[38]
    del prob_list[36]
    del prob_list[33]
    del prob_list[30]
    del prob_list[22]
    del prob_list[20]
    del prob_list[17]
    del prob_list[10]
    del prob_list[7]
    del prob_list[4]
    del prob_list[2]
    del prob_list[0]

    del street_list[38]
    del street_list[36]
    del street_list[33]
    del street_list[30]
    del street_list[22]
    del street_list[20]
    del street_list[17]
    del street_list[10]
    del street_list[7]
    del street_list[4]
    del street_list[2]
    del street_list[0]

    del street_colors[38]
    del street_colors[36]
    del street_colors[33]
    del street_colors[30]
    del street_colors[22]
    del street_colors[20]
    del street_colors[17]
    del street_colors[10]
    del street_colors[7]
    del street_colors[4]
    del street_colors[2]
    del street_colors[0]


#   sort, zip and reverse results
results_final = sorted(zip(prob_list, street_list))
results_final.reverse()

results_bar = sorted(zip(prob_list, street_list, street_colors, street_occur_list))

#   Show results
print('Prob \t\tStreet')
for prob, street in results_final:
    print(str(prob) + '        ' + street)

show_results_list = []
for prob, street in results_final:
    show_results_list.append(str(prob) + '      ' + street)

if showOnlyStreets:
    resultsLayout = [
        [Sg.Text("Results:")],
        [Sg.Text('Prob \t\t\tStreet')],
        [Sg.Text(show_results_list[0], size=(15, 1)), Sg.Text(show_results_list[14])],
        [Sg.Text(show_results_list[1], size=(15, 1)), Sg.Text(show_results_list[15])],
        [Sg.Text(show_results_list[2], size=(15, 1)), Sg.Text(show_results_list[16])],
        [Sg.Text(show_results_list[3], size=(15, 1)), Sg.Text(show_results_list[17])],
        [Sg.Text(show_results_list[4], size=(15, 1)), Sg.Text(show_results_list[18])],
        [Sg.Text(show_results_list[5], size=(15, 1)), Sg.Text(show_results_list[19])],
        [Sg.Text(show_results_list[6], size=(15, 1)), Sg.Text(show_results_list[20])],
        [Sg.Text(show_results_list[7], size=(15, 1)), Sg.Text(show_results_list[21])],
        [Sg.Text(show_results_list[8], size=(15, 1)), Sg.Text(show_results_list[22])],
        [Sg.Text(show_results_list[9], size=(15, 1)), Sg.Text(show_results_list[23])],
        [Sg.Text(show_results_list[10], size=(15, 1)), Sg.Text(show_results_list[24])],
        [Sg.Text(show_results_list[11], size=(15, 1)), Sg.Text(show_results_list[25])],
        [Sg.Text(show_results_list[12], size=(15, 1)), Sg.Text(show_results_list[26])],
        [Sg.Text(show_results_list[13], size=(15, 1)), Sg.Text(show_results_list[27])],
        [Sg.Button("Show Graph")]
    ]
else:
    resultsLayout = [
        [Sg.Text("Results:")],
        [Sg.Text('Prob \tStreet')],
        [Sg.Text(show_results_list[0], size=(15, 1)), Sg.Text(show_results_list[20])],
        [Sg.Text(show_results_list[1], size=(15, 1)), Sg.Text(show_results_list[21])],
        [Sg.Text(show_results_list[2], size=(15, 1)), Sg.Text(show_results_list[22])],
        [Sg.Text(show_results_list[3], size=(15, 1)), Sg.Text(show_results_list[23])],
        [Sg.Text(show_results_list[4], size=(15, 1)), Sg.Text(show_results_list[24])],
        [Sg.Text(show_results_list[5], size=(15, 1)), Sg.Text(show_results_list[25])],
        [Sg.Text(show_results_list[6], size=(15, 1)), Sg.Text(show_results_list[26])],
        [Sg.Text(show_results_list[7], size=(15, 1)), Sg.Text(show_results_list[26])],
        [Sg.Text(show_results_list[8], size=(15, 1)), Sg.Text(show_results_list[28])],
        [Sg.Text(show_results_list[9], size=(15, 1)), Sg.Text(show_results_list[29])],
        [Sg.Text(show_results_list[10], size=(15, 1)), Sg.Text(show_results_list[30])],
        [Sg.Text(show_results_list[11], size=(15, 1)), Sg.Text(show_results_list[31])],
        [Sg.Text(show_results_list[12], size=(15, 1)), Sg.Text(show_results_list[32])],
        [Sg.Text(show_results_list[13], size=(15, 1)), Sg.Text(show_results_list[33])],
        [Sg.Text(show_results_list[14], size=(15, 1)), Sg.Text(show_results_list[34])],
        [Sg.Text(show_results_list[15], size=(15, 1)), Sg.Text(show_results_list[35])],
        [Sg.Text(show_results_list[16], size=(15, 1)), Sg.Text(show_results_list[36])],
        [Sg.Text(show_results_list[17], size=(15, 1)), Sg.Text(show_results_list[37])],
        [Sg.Text(show_results_list[18], size=(15, 1)), Sg.Text(show_results_list[38])],
        [Sg.Text(show_results_list[19], size=(15, 1)), Sg.Text(show_results_list[39])],
        [Sg.Button("Show Graph")],
        [Sg.Text("(Closes Window)")]
    ]

resultWindow = Sg.Window("Results").Layout(resultsLayout)
button = resultWindow.Read()

if button[0] == "Show Graph":
    Sg.Window.Close(resultWindow)

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
    plt.show()

