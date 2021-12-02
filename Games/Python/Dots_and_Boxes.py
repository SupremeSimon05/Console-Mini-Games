import random
rows = [".    .    .    .    .", "", ".    .    .    .    .", "", ".    .    .    .    .", "" , ".    .    .    .    .", "", ".    .    .    .    ."]
rowData = [[0,0,0,0], [0,0,0,0,0], [0,0,0,0], [0,0,0,0,0], [0,0,0,0], [0,0,0,0,0], [0,0,0,0], [0,0,0,0,0], [0,0,0,0]]
players = 0
bots = 0
rowScoreData = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
turn = 1
turnAlreadySetBack = False
UP = "\x1B[1A"
CLR = "\x1B[0K"

#makes the print statement clear the line before printing a new one
oprint = print
def print(this, pre = CLR, end = "\n"):
    oprint(pre+this, end = end)

#lets you move the cursor up
def moveUp(times):
    for i in range(times):
        print(UP, end = "")

'''
Todo:
set up changing lines instead of adding lines
to fix:
'''

def main():
    global rowData
    global rowScoreData
    global rows 
    global turn
    global bots
    global players
    global turnAlreadySetBack
    
    yn = input("Would you like to play? ")
    while(True):
        if((yn + " ")[0] == "n"):
            break
        rows = [".    .    .    .    .", "", ".    .    .    .    .", "", ".    .    .    .    .", "" , ".    .    .    .    .", "", ".    .    .    .    ."]
        rowData = [[0,0,0,0], [0,0,0,0,0], [0,0,0,0], [0,0,0,0,0], [0,0,0,0], [0,0,0,0,0], [0,0,0,0], [0,0,0,0,0], [0,0,0,0]]
        rowScoreData = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
        while(True):
            players = input("How many players? 1-3 is suggested ")
            try:
                players = int(players)
                if(players > 0):
                    break
                else:
                    moveUp(3)
                    print("You need at least 1 player ")
            except:
                if(players == ""):
                    players = 1
                    break
                else:
                    moveUp(3)
                    print("Please enter a number ")
        while(True):
            bots = input("How many bots? 0-2 is suggested ")
            try:
                bots = int(bots)
                if(players > 1 or (players == 1 and bots > 0)):
                    break
                else:
                    moveUp(2)
                    print("You need to have at least one bot when playing with only 1 player ")
            except:
                if(bots == "" and players > 1):
                    bots = 0
                    break
                elif(bots == "" and players == 1):
                    bots = 1
                    break
                else:
                    moveUp(2)
                    print("Please enter a real number ")
        moveUp(20)
        kinDupdate()
        while((not ifFullBoard())):
            if(turn<=players):
                playerTurn()
                kinDupdate()
            elif(turn<=bots+players):
                botTurn()
                kinDupdate()
            else:
                turn = 0
            turn = turn + 1
            if(turnAlreadySetBack):
                turn = turn - 1
            turnAlreadySetBack = False
        whoWon()
        yn = input("Would you like to play again? ")

def showBoard():
    moveUp(20)
    for i in range(9):
        print(rows[i])
    
def kinDupdate():
    dataToDefinit()
    showBoard()
    
    

def ifFullBoard():
    z = 0
    for i in range(9):
        if(i%2 == 0):
            for a in range(4):
                if(rowData[i][a] == 1):
                    z = z + 1
        else:
            for a in range(5):
                if(rowData[i][a] == 1):
                    z = z + 1
    if(z == 40):
        return True
    else:
        return False
        
        
def dataToDefinit():
    global rows
    global rowData
    global rowScoreData
    global players
    
    newRow = ["."]
    newRowStr = ""
    for i in range(5):
        newRow = ["."]
        newRowStr = ""
        for a in range(4):
            if(rowData[i*2][a] == 1):
                newRow.append("____.")
            else:
                newRow.append("    .")
        for a in range(5):
            newRowStr = newRowStr + newRow[a]
        rows[i*2] = newRowStr
        newRowStr = ""
    newRow = []
    newRowStr = ""
    for i in range(4):
        newRowStr = ""
        newRow = [""]
        for a in range(4):
            if(rowData[i*2 + 1][a] == 1):
                if(rowScoreData[i][a]>0 and rowScoreData[i][a]<=players and rowScoreData[i][a]>=10):
                    newRow.append("|P" + str(rowScoreData[i][a]) + " ")
                elif(rowScoreData[i][a]>0 and rowScoreData[i][a]<=players):
                    newRow.append("| P" + str(rowScoreData[i][a]) + " ")
                elif(rowScoreData[i][a]>0 and rowScoreData[i][a]>=10):
                    newRow.append("|B" + str(rowScoreData[i][a]) + " ")
                elif(rowScoreData[i][a]>0):
                    newRow.append("| B" + str(rowScoreData[i][a]) + " ")
                else:
                    newRow.append("|    ")
            else:
                newRow.append("     ")
        for a in range(5):
            newRowStr = newRowStr + newRow[a]
        if(rowData[i * 2 + 1][4] == 1):
            rows[i*2 + 1] = newRowStr + "|"
        else:
            rows[i*2 + 1] = newRowStr
            
    
        

#takes in the row(x) and column(y) of the "A" line (top of the box)
def checkForSquare(x, y):
    global rowData
    global rows
    global rowScoreData
    global turn
    global turnAlreadySetBack

    if(rowData[x+2][y] == 1 and rowData[x+1][y] == 1 and rowData[x+1][y+1] == 1 and rowData[x][y] == 1):
        rowScoreData[int(x/2)][y] = turn
        turnAlreadySetBack = True
    
    
def playerTurn():
    global turn
    global rowData
    worked = True
    print("Player " + str(turn) + "'s turn. ")
    while(True):
        try:
            pos = int(input("Where do you want to place the line? The format is dot:dot dot is written as row:column, 1112 will give you from the top left dot to the top second to leftmost dot.\n"))
            pos1 = int(str(pos)[0] + str(pos)[1])
            pos2 = int(str(pos)[2] + str(pos)[3])
            worked = True
            if(checkHorizontal(11, pos1, pos2) and rowData[0][0] == 0):
                rowData[0][0] = 1
                checkForSquare(0, 0)
            elif(checkHorizontal(12, pos1, pos2) and rowData[0][1] == 0):
                rowData[0][1] = 1
                checkForSquare(0, 1)
            elif(checkHorizontal(13, pos1, pos2) and rowData[0][2] == 0):
                rowData[0][2] = 1
                checkForSquare(0, 2)
            elif(checkHorizontal(14, pos1, pos2) and rowData[0][3] == 0):
                rowData[0][3] = 1
                checkForSquare(0, 3)
            elif(checkHorizontal(21, pos1, pos2) and rowData[2][0] == 0):
                rowData[2][0] = 1
                checkForSquare(2, 0)
                checkForSquare(0, 0)
            elif(checkHorizontal(22, pos1, pos2) and rowData[2][1] == 0):
                rowData[2][1] = 1
                checkForSquare(2, 1)
                checkForSquare(0, 1)
            elif(checkHorizontal(23, pos1, pos2) and rowData[2][2] == 0):
                rowData[2][2] = 1
                checkForSquare(2, 2)
                checkForSquare(0, 2)
            elif(checkHorizontal(24, pos1, pos2) and rowData[2][3] == 0):
                rowData[2][3] = 1
                checkForSquare(2, 3)
                checkForSquare(0, 3)
            elif(checkHorizontal(31, pos1, pos2) and rowData[4][0] == 0):
                rowData[4][0] = 1
                checkForSquare(4, 0)
                checkForSquare(2, 0)
            elif(checkHorizontal(32, pos1, pos2) and rowData[4][1] == 0):
                rowData[4][1] = 1
                checkForSquare(4, 1)
                checkForSquare(2, 1)
            elif(checkHorizontal(33, pos1, pos2) and rowData[4][2] == 0):
                rowData[4][2] = 1
                checkForSquare(4, 2)
                checkForSquare(2, 2)
            elif(checkHorizontal(34, pos1, pos2) and rowData[4][3] == 0):
                rowData[4][3] = 1
                checkForSquare(4, 3)
                checkForSquare(2, 3)
            elif(checkHorizontal(41, pos1, pos2) and rowData[6][0] == 0):
                rowData[6][0] = 1
                checkForSquare(6, 0)
                checkForSquare(4, 0)
            elif(checkHorizontal(42, pos1, pos2) and rowData[6][1] == 0):
                rowData[6][1] = 1
                checkForSquare(6, 1)
                checkForSquare(4, 1)
            elif(checkHorizontal(43, pos1, pos2) and rowData[6][2] == 0):
                rowData[6][2] = 1
                checkForSquare(6, 2)
                checkForSquare(4, 2)
            elif(checkHorizontal(44, pos1, pos2) and rowData[6][3] == 0):
                rowData[6][3] = 1
                checkForSquare(6, 3)
                checkForSquare(4, 3)
            elif(checkHorizontal(51, pos1, pos2) and rowData[8][0] == 0):
                rowData[8][0] = 1
                checkForSquare(6, 0)
            elif(checkHorizontal(52, pos1, pos2) and rowData[8][1] == 0):
                rowData[8][1] = 1
                checkForSquare(6, 1)
            elif(checkHorizontal(53, pos1, pos2) and rowData[8][2] == 0):
                rowData[8][2] = 1
                checkForSquare(6, 2)
            elif(checkHorizontal(54, pos1, pos2) and rowData[8][3] == 0):
                rowData[8][3] = 1
                checkForSquare(6, 3)
            elif(checkVertical(11, pos1, pos2) and rowData[1][0] == 0):
                rowData[1][0] = 1
                checkForSquare(0, 0)
            elif(checkVertical(21, pos1, pos2) and rowData[3][0] == 0):
                rowData[3][0] = 1
                checkForSquare(2, 0)
            elif(checkVertical(31, pos1, pos2) and rowData[5][0] == 0):
                rowData[5][0] = 1
                checkForSquare(4, 0)
            elif(checkVertical(41, pos1, pos2) and rowData[7][0] == 0):
                rowData[7][0] = 1
                checkForSquare(6, 0)
            elif(checkVertical(12, pos1, pos2) and rowData[1][1] == 0):
                rowData[1][1] = 1
                checkForSquare(0, 1)
                checkForSquare(0, 0)
            elif(checkVertical(22, pos1, pos2) and rowData[3][1] == 0):
                rowData[3][1] = 1
                checkForSquare(2, 1)
                checkForSquare(2, 0)
            elif(checkVertical(32, pos1, pos2) and rowData[5][1] == 0):
                rowData[5][1] = 1
                checkForSquare(4, 1)
                checkForSquare(4, 0)
            elif(checkVertical(42, pos1, pos2) and rowData[7][1] == 0):
                rowData[7][1] = 1
                checkForSquare(6, 1)
                checkForSquare(6, 0)
            elif(checkVertical(13, pos1, pos2) and rowData[1][2] == 0):
                rowData[1][2] = 1
                checkForSquare(0, 2)
                checkForSquare(0, 1)
            elif(checkVertical(23, pos1, pos2) and rowData[3][2] == 0):
                rowData[3][2] = 1
                checkForSquare(2, 2)
                checkForSquare(2, 1)
            elif(checkVertical(33, pos1, pos2) and rowData[5][2] == 0):
                rowData[5][2] = 1
                checkForSquare(4, 2)
                checkForSquare(4, 1)
            elif(checkVertical(43, pos1, pos2) and rowData[7][2] == 0):
                rowData[7][2] = 1
                checkForSquare(6, 2)
                checkForSquare(6, 1)
            elif(checkVertical(14, pos1, pos2) and rowData[1][3] == 0):
                rowData[1][3] = 1
                checkForSquare(0, 3)
                checkForSquare(0, 2)
            elif(checkVertical(24, pos1, pos2) and rowData[3][3] == 0):
                rowData[3][3] = 1
                checkForSquare(2, 3)
                checkForSquare(2, 2)
            elif(checkVertical(34, pos1, pos2) and rowData[5][3] == 0):
                rowData[5][3] = 1
                checkForSquare(4, 3)
                checkForSquare(4, 2)
            elif(checkVertical(44, pos1, pos2) and rowData[7][3] == 0):
                rowData[7][3] = 1
                checkForSquare(6, 3)
                checkForSquare(6, 2)
            elif(checkVertical(15, pos1, pos2) and rowData[1][4] == 0):
                rowData[1][4] = 1
                checkForSquare(0, 3)
            elif(checkVertical(25, pos1, pos2) and rowData[3][4] == 0):
                rowData[3][4] = 1
                checkForSquare(2, 3)
            elif(checkVertical(35, pos1, pos2) and rowData[5][4] == 0):
                rowData[5][4] = 1
                checkForSquare(4, 3)
            elif(checkVertical(45, pos1, pos2) and rowData[7][4] == 0):
                rowData[7][4] = 1
                checkForSquare(6, 3)
            else:
                moveUp(20)
                print("Your choice didn't work, please make sure there isn't a line already between those dots. ")
                worked = False
                showBoard()
            if(worked):
                break
        except:
            moveUp(20)
            print("Please make sure to enter 4 integers. ")
            showBoard()
def checkHorizontal(num, pos1, pos2):
    if((pos1 == num and pos2 == num + 1) or (pos1 == num + 1 and pos2 == num)):
        return True
    else:
        return False
        
def checkVertical(num, pos1, pos2):
    if((pos1 == num and pos2 == num + 10) or (pos1 == num + 10 and pos2 == num)):
        return True
    else:
        return False

def botTurn():
    global turn
    global rowData
    isDone = False
    x = 0
    y = 0
    
    print("Bot " + str(turn) + "'s turn. ")
    moveUp(100)
    while(True):
        x = random.randrange(0, 9)
        if(x % 2 == 0):
            y = random.randrange(0, 4)
            if(rowData[x][y] == 0):
                rowData[x][y] = 1
                if(x != 8):
                    checkForSquare(x, y)
                if(x != 0):
                    checkForSquare(x-2, y)
                break
        else:
            y = random.randrange(0, 5)
            if(rowData[x][y] == 0):
                rowData[x][y] = 1
                if(y != 4):
                    checkForSquare(x-1, y)
                if(y != 0):
                    checkForSquare(x-1, y-1)
                break
            
def whoWon():
    global rowScoreData
    global players
    global bots
    nums = []
    b = 0
    c = 0
    d = []
    words = []
    wordsStr = ""
    
    for i in range(players + bots):
        nums.append(0)
    for i in range(4):
        for a in range(4):
            nums[rowScoreData[i][a]-1] = nums[rowScoreData[i][a]-1] + 1
    b = max(nums)
    for i in range(players + bots):
        if(nums[i] == b):
            c = c + 1
            d.append(i)
    if(c == 1):
        if(players>=d[0] + 1):
            print("Player " + str(d[0] + 1) + " won. Congrats!")
        else:
            print("Dang, bot " + str(d[0] + 1) + " won :(")
    else:
        if(d[0]+1 <= players):
            words.append("Player " + str(d[0]+1) + " tied with ")
        else:
            words.append("Bot " + str(d[0]+1) + " tied with ")
        for i in range(len(d)-1):
            if(d[i+1]+1 <= players and i+1!=len(d)-1):
                words.append("player " + str(d[i+1]) + " and ")
            elif(d[i+1]+1 <= players and i+1==len(d)-1):
                words.append("player " + str(d[i+1]+1))
            elif(i+1!=len(d)-1):
                words.append("bot " + str(d[i+1]+1) + " and ")
            else:
                words.append("bot " + str(d[i+1]+1))
        for i in range(len(d)):
            wordsStr = wordsStr + words[i]
        print(wordsStr)
    
    
    
main()













