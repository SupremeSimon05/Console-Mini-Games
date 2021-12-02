import random
rows = ["   |   |   ", "   |   |   ", "   |   |   "] 
rowData = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
playerWon = False
player2Won = False
difficulty = 0
turn = 1
tie = False
UP = "\x1B[1A"
CLR = "\x1B[0K"

#makes the print statement clear the line before printing a new one
oprint = print
def print(this, pre = CLR, pro = "\n"):
    oprint(pre+this, end = pro)

#lets you move the cursor up
def moveUp(times):
    for i in range(times):
        print(UP, pro = "")

#rowData 0=None, 1=player1, 2=player2 or bot. 
#player1 = x, player2 = o
def main():
    global rows
    global playerWon
    global player2Won
    global difficulty
    global rowData
    global turn
    global tie
    print("Tic Tac Toe")
    
    playing = ((input("Would you like to play ") + " ")[0] != "n") 
    while(playing):
        tie = False
        playerWon = False
        player2Won = False
        rowData = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        dataToDefinit()
        difficulty = input("Select difficulty 1-infinity; higher being easier and 1 being most difficult. '2P' will activate two player mode ")
        while(True):
            try:
                int(difficulty)
                break
            except:
                moveUp(1)
                if(difficulty.lower()!="2p".lower()):
                    difficulty = input("Select difficulty 1-infinity; higher being easier and 1 being most difficult. '2P' will activate two player mode ")
                else:
                    break
        moveUp(3)
        kinDupdate()
        while((not playerWon) and (not player2Won) and (not tie)):
            if(turn == 1):
                playerMove(1)
                turn = 2
            else:
                if(difficulty.lower() == "2p".lower()):
                    playerMove(2)
                else:
                    botsMove()
                turn = 1
            kinDupdate()
        playing = ((input("Would you like to play? ") + " ")[0] != "n") 

def showBoard():
    global rows
    
    moveUp(7)
    print(rows[0])
    print("___________")
    print(rows[1])
    print("___________")
    print(rows[2])

def dataToDefinit():
    global rows
    global rowData
    for i in range(3):
        if(rowData[i] == [0,0,0]):
            rows[i] = "   |   |   "
        elif(rowData[i] == [1,0,0]):
            rows[i] = " x |   |   "
        elif(rowData[i] == [2,0,0]):
            rows[i] = " o |   |   "
        elif(rowData[i] == [0,1,0]):
            rows[i] = "   | x |   "    
        elif(rowData[i] == [1,1,0]):
            rows[i] = " x | x |   "
        elif(rowData[i] == [2,1,0]):
            rows[i] = " o | x |   "
        elif(rowData[i] == [0,2,0]):
            rows[i] = "   | o |   "
        elif(rowData[i] == [1,2,0]):
            rows[i] = " x | o |   "
        elif(rowData[i] == [2,2,0]):
            rows[i] = " o | o |   "
        elif(rowData[i] == [0,0,1]):
            rows[i] = "   |   | x "
        elif(rowData[i] == [1,0,1]):
            rows[i] = " x |   | x "
        elif(rowData[i] == [2,0,1]):
            rows[i] = " o |   | x "
        elif(rowData[i] == [0,1,1]):
            rows[i] = "   | x | x "
        elif(rowData[i] == [1,1,1]):
            rows[i] = " x | x | x "
        elif(rowData[i] == [2,1,1]):
            rows[i] = " o | x | x "
        elif(rowData[i] == [0,2,1]):
            rows[i] = "   | o | x "
        elif(rowData[i] == [1,2,1]):
            rows[i] = " x | o | x "
        elif(rowData[i] == [2,2,1]):
            rows[i] = " o | o | x "
        elif(rowData[i] == [0,0,2]):
            rows[i] = "   |   | o "
        elif(rowData[i] == [1,0,2]):
            rows[i] = " x |   | o "
        elif(rowData[i] == [2,0,2]):
            rows[i] = " o |   | o "
        elif(rowData[i] == [0,1,2]):
            rows[i] = "   | x | o "
        elif(rowData[i] == [1,1,2]):
            rows[i] = " x | x | o "
        elif(rowData[i] == [2,1,2]):
            rows[i] = " o | x | o "
        elif(rowData[i] == [0,2,2]):
            rows[i] = "   | o | o "
        elif(rowData[i] == [1,2,2]):
            rows[i] = " x | o | o "
        elif(rowData[i] == [2,2,2]):
            rows[i] = " o | o | o "
        else:
            print("catch ln 135 currently")
        
def playerMove(num):
    global rowData
    print("player " + str(num) + "'s turn. ")
    while(True):
        try:
            choice = input("Where do you want to go? Enter it in order row:column. 11 would put you in the top left corner. ")
            moveUp(1)
            if(rowData[int(choice[0])-1][int(choice[1])-1]==0 and num == 1):
                rowData[int(choice[0])-1][int(choice[1])-1] = 1
                break
            elif(rowData[int(choice[0])-1][int(choice[1])-1]==0 and num == 2):
                rowData[int(choice[0])-1][int(choice[1])-1] = 2
                break
            else:
                moveUp(1)
                print("Try again, there is already a letter in the spot you chose")
        except:
            moveUp(1)
            print("Please enter two numbers to choose your space, make sure they are both under 4 and over 0")
            
def kinDupdate():
    global player2Won
    global playerWon
    global tie
    global difficulty
    
    if(whoWon() == "tie"):
        print("You both tied! ")
        tie = True
    elif(whoWon() == "player1"):
        playerWon = True
        print("player 1 won! ")
    elif(whoWon() == "player2"):
        player2Won = True
        print("player 2 won! ")
    dataToDefinit()
    showBoard()
    
def whoWon():
    global rowData
    if(ofPlayer(1)):
        return "player1"
    elif(ofPlayer(2)):
        return "player2"
    elif(isTie()):
        return "tie"
    
def isTie():
    num = 0
    for i in range(3):
            for a in range(3):
                if(rowData[i][a] == 0):
                    num = num + 1
    if(num==0):
        return True

def ofPlayer(num):
    global rowData
    a = 0 
    c = 0
    if(num == 1):
        for i in range(3):
            if(rowData[i] == [1,1,1]):
                a = a + 1
        for b in range(3):
            if(rowData[0][b] == 1 and rowData[1][b] == 1 and rowData[2][b] == 1):
                c = c + 1
        if(a!=0):
            return True
        elif(c!=0):
            return True
        elif((rowData[0][0] == 1 and rowData[1][1] == 1 and rowData[2][2] == 1) or (rowData[0][2] == 1 and rowData[1][1] == 1 and rowData[2][0] == 1)):
            return True
        else:
            return False
    else:
        for i in range(3):
            if(rowData[i] == [2,2,2]):
                a = a + 1
        for b in range(3):
            if(rowData[0][b] == 2 and rowData[1][b] == 2 and rowData[2][b] == 2):
                c = c + 1
        if(a!=0):
            return True
        elif(c!=0):
            return True
        elif((rowData[0][0] == 2 and rowData[1][1] == 2 and rowData[2][2] == 2) or (rowData[0][2] == 2 and rowData[1][1] == 2 and rowData[2][0] == 2)):
            return True
        else:
            return False

def botsMove():
    global rowData
    global difficulty
    
    if(rowData[0][0] == 2 and rowData[0][1] == 2 and rowData[0][2] == 0 and (int(difficulty) == 1 or int(difficulty) == 2  or int(difficulty) == 3 or random.randrange(0, int(math.sqrt(difficulty))) == 0)):     
        rowData[0][2] = 2
    elif(rowData[1][0] == 2 and rowData[1][1] == 2 and rowData[1][2] == 0):
        rowData[1][2] = 2
    elif(rowData[2][0] == 2 and rowData[2][1] == 2 and rowData[2][2] == 0):
        rowData[2][2] = 2
    elif(rowData[0][1] == 2 and rowData[0][2] == 2 and rowData[0][0] == 0):
        rowData[0][0] = 2
    elif(rowData[1][1] == 2 and rowData[1][2] == 2 and rowData[1][0] == 0):
        rowData[1][0] = 2
    elif(rowData[2][1] == 2 and rowData[2][2] == 2 and rowData[2][0] == 0):
        rowData[2][0] = 2
    elif(rowData[0][0] == 2 and rowData[1][0] == 2 and rowData[2][0] == 0):
        rowData[2][0] = 2
    elif(rowData[0][1] == 2 and rowData[1][1] == 2 and rowData[2][1] == 0):
        rowData[2][1] = 2
    elif(rowData[0][2] == 2 and rowData[1][2] == 2 and rowData[2][2] == 0):
        rowData[2][2] = 2
    elif(rowData[1][0] == 2 and rowData[2][0] == 2 and rowData[0][0] == 0):
        rowData[0][0] = 2
    elif(rowData[1][1] == 2 and rowData[2][1] == 2 and rowData[0][1] == 0):
        rowData[0][1] = 2
    elif(rowData[1][2] == 2 and rowData[2][2] == 2 and rowData[0][2] == 0):
        rowData[0][2] = 2
    elif(rowData[0][2] == 2 and rowData[0][0] == 2 and rowData[0][1] == 0):
        rowData[0][1] = 2
    elif(rowData[1][2] == 2 and rowData[1][0] == 2 and rowData[1][1] == 0):
        rowData[1][1] = 2
    elif(rowData[2][2] == 2 and rowData[2][0] == 2 and rowData[2][1] == 0):
        rowData[2][1] = 2
    elif(rowData[0][0] == 2 and rowData[2][0] == 2 and rowData[1][0] == 0):
        rowData[1][0] = 2
    elif(rowData[0][1] == 2 and rowData[2][1] == 2 and rowData[1][1] == 0):
        rowData[1][1] = 2
    elif(rowData[0][2] == 2 and rowData[2][2] == 2 and rowData[1][2] == 0):
        rowData[1][2] = 2
    elif(rowData[0][0] == 2 and rowData[2][2] == 2 and rowData[1][1] == 0):
        rowData[1][1] = 2
    elif(rowData[0][2] == 2 and rowData[2][0] == 2 and rowData[1][1] == 0):
        rowData[1][1] = 2
    elif(rowData[0][0] == 1 and rowData[0][1] == 1 and rowData[0][2] == 0):
        rowData[0][2] = 2
    elif(rowData[1][0] == 1 and rowData[1][1] == 1 and rowData[1][2] == 0):
        rowData[1][2] = 2
    elif(rowData[2][0] == 1 and rowData[2][1] == 1 and rowData[2][2] == 0):
        rowData[2][2] = 2
    elif(rowData[0][1] == 1 and rowData[0][2] == 1 and rowData[0][0] == 0):
        rowData[0][0] = 2
    elif(rowData[1][1] == 1 and rowData[1][2] == 1 and rowData[1][0] == 0):
        rowData[1][0] = 2
    elif(rowData[2][1] == 1 and rowData[2][2] == 1 and rowData[2][0] == 0):
        rowData[2][0] = 2
    elif(rowData[0][0] == 1 and rowData[1][0] == 1 and rowData[2][0] == 0):
        rowData[2][0] = 2
    elif(rowData[0][1] == 1 and rowData[1][1] == 1 and rowData[2][1] == 0):
        rowData[2][1] = 2
    elif(rowData[0][2] == 1 and rowData[1][2] == 1 and rowData[2][2] == 0):
        rowData[2][2] = 2
    elif(rowData[1][0] == 1 and rowData[2][0] == 1 and rowData[0][0] == 0):
        rowData[0][0] = 2
    elif(rowData[1][1] == 1 and rowData[2][1] == 1 and rowData[0][1] == 0):
        rowData[0][1] = 2
    elif(rowData[1][2] == 1 and rowData[2][2] == 1 and rowData[0][2] == 0):
        rowData[0][2] = 2
    elif(rowData[2][0] == 1 and rowData[0][2] == 1 and rowData[1][1] == 0):
        rowData[1][1] = 2
    elif(rowData[0][0] == 1 and rowData[2][2] == 1 and rowData[1][1] == 0):
        rowData[1][1] = 2
    elif(rowData[0][0] == 1 and rowData[1][1] == 1 and rowData[2][2] == 0):
        rowData[2][2] = 2
    elif(rowData[0][2] == 1 and rowData[1][1] == 1 and rowData[2][0] == 0):
        rowData[2][0] = 2
    elif(rowData[2][0] == 1 and rowData[1][1] == 1 and rowData[0][2] == 0):
        rowData[0][2] = 2
    elif(rowData[2][2] == 1 and rowData[1][1] == 1 and rowData[0][0] == 0):
        rowData[0][0] = 2
    elif(rowData[0][0] == 1 and rowData[0][2] == 1 and rowData[0][1] == 0):
        rowData[0][1] = 2
    elif(rowData[1][0] == 1 and rowData[1][2] == 1 and rowData[1][1] == 0):
        rowData[1][1] = 2
    elif(rowData[2][0] == 1 and rowData[2][2] == 1 and rowData[2][1] == 0):
        rowData[2][1] = 2
    elif(rowData[0][0] == 1 and rowData[2][0] == 1 and rowData[1][0] == 0):
        rowData[1][0] = 2
    elif(rowData[0][1] == 1 and rowData[2][1] == 1 and rowData[1][1] == 0):
        rowData[1][1] = 2
    elif(rowData[0][2] == 1 and rowData[2][2] == 1 and rowData[1][2] == 0):
        rowData[1][2] = 2
    elif(random.randrange(0, int(difficulty)) == 0):
        if(rowData[1][1] == 1 and rowData[0][0] == 0):
            rowData[0][0] = 2
        elif(rowData[1][1] == 1 and rowData[0][2] == 0):
            rowData[0][2] = 2
        elif(rowData[1][1] == 1 and rowData[2][2] == 0):
            rowData[2][2] = 2
        elif(rowData[1][1] == 1 and rowData[2][0] == 0):
            rowData[2][0] = 2
        elif(rowData[0][0] == 1 and rowData[1][1] == 0):
            rowData[1][1] = 2
        elif(rowData[0][2] == 1 and rowData[1][1] == 0):
            rowData[1][1] = 2
        elif(rowData[2][0] == 1 and rowData[1][1] == 0):
            rowData[1][1] = 2
        elif(rowData[2][2] == 1 and rowData[1][1] == 0):
            rowData[1][1] = 2
        elif(rowData[2][2] == 1 and rowData[1][1] == 2 and rowData[0][1] == 0):
            rowData[0][1] = 2
        elif(rowData[2][2] == 1 and rowData[1][1] == 2 and rowData[1][0] == 0):
            rowData[1][0] = 2
        elif(rowData[2][2] == 1 and rowData[1][1] == 2 and rowData[1][2] == 0):
            rowData[1][2] = 2
        elif(rowData[2][2] == 1 and rowData[1][1] == 2 and rowData[2][1] == 0):
            rowData[2][1] = 2
        elif(rowData[0][0] == 1 and rowData[1][1] == 2 and rowData[0][1] == 0):
            rowData[0][1] = 2
        elif(rowData[0][0] == 1 and rowData[1][1] == 2 and rowData[1][0] == 0):
            rowData[1][0] = 2
        elif(rowData[0][0] == 1 and rowData[1][1] == 2 and rowData[1][2] == 0):
            rowData[1][2] = 2
        elif(rowData[0][0] == 1 and rowData[1][1] == 2 and rowData[2][1] == 0):
            rowData[2][1] = 2
        elif(rowData[0][2] == 1 and rowData[1][1] == 2 and rowData[0][1] == 0):
            rowData[0][1] = 2
        elif(rowData[0][2] == 1 and rowData[1][1] == 2 and rowData[1][0] == 0):
            rowData[1][0] = 2
        elif(rowData[0][2] == 1 and rowData[1][1] == 2 and rowData[1][2] == 0):
            rowData[1][2] = 2
        elif(rowData[0][2] == 1 and rowData[1][1] == 2 and rowData[2][1] == 0):
            rowData[2][1] = 2
        elif(rowData[2][0] == 1 and rowData[1][1] == 2 and rowData[0][1] == 0):
            rowData[0][1] = 2
        elif(rowData[2][0] == 1 and rowData[1][1] == 2 and rowData[1][0] == 0):
            rowData[1][0] = 2
        elif(rowData[2][0] == 1 and rowData[1][1] == 2 and rowData[1][2] == 0):
            rowData[1][2] = 2
        elif(rowData[2][0] == 1 and rowData[1][1] == 2 and rowData[2][1] == 0):
            rowData[2][1] = 2
        elif(rowData[0][1] == 1 and rowData[1][1] == 0):
            rowData[1][1] = 2
        elif(rowData[1][0] == 1 and rowData[1][1] == 0):
            rowData[1][1] = 2
        elif(rowData[1][2] == 1 and rowData[1][1] == 0):
            rowData[1][1] = 2
        elif(rowData[2][1] == 1 and rowData[1][1] == 0):
            rowData[1][1] = 2
        elif(rowData[0][1] == 1 and rowData[1][1] == 2 and rowData[0][0] == 0):
            rowData[0][0] = 2
        elif(rowData[0][1] == 1 and rowData[1][1] == 2 and rowData[0][2] == 0):
            rowData[0][2] = 2
        elif(rowData[0][1] == 1 and rowData[1][1] == 2 and rowData[2][0] == 0):
            rowData[2][0] = 2
        elif(rowData[0][1] == 1 and rowData[1][1] == 2 and rowData[2][2] == 0):
            rowData[2][2] = 2
        elif(rowData[1][0] == 1 and rowData[1][1] == 2 and rowData[0][0] == 0):
            rowData[0][0] = 2
        elif(rowData[1][0] == 1 and rowData[1][1] == 2 and rowData[0][2] == 0):
            rowData[0][2] = 2
        elif(rowData[1][0] == 1 and rowData[1][1] == 2 and rowData[2][0] == 0):
            rowData[2][0] = 2
        elif(rowData[1][0] == 1 and rowData[1][1] == 2 and rowData[2][2] == 0):
            rowData[2][2] = 2
        elif(rowData[1][2] == 1 and rowData[1][1] == 2 and rowData[0][0] == 0):
            rowData[0][0] = 2
        elif(rowData[1][2] == 1 and rowData[1][1] == 2 and rowData[0][2] == 0):
            rowData[0][2] = 2
        elif(rowData[1][2] == 1 and rowData[1][1] == 2 and rowData[2][0] == 0):
            rowData[2][0] = 2
        elif(rowData[1][2] == 1 and rowData[1][1] == 2 and rowData[2][2] == 0):
            rowData[2][2] = 2
        elif(rowData[2][1] == 1 and rowData[1][1] == 2 and rowData[0][0] == 0):
            rowData[0][0] = 2
        elif(rowData[2][1] == 1 and rowData[1][1] == 2 and rowData[0][2] == 0):
            rowData[0][2] = 2
        elif(rowData[2][1] == 1 and rowData[1][1] == 2 and rowData[2][0] == 0):
            rowData[2][0] = 2
        elif(rowData[2][1] == 1 and rowData[1][1] == 2 and rowData[2][2] == 0):
            rowData[2][2] = 2
        elif(ifEmptyBoard()):
            rowData[0][0] = 2
            
            
    else:
        while(True):
            naum5 = random.randrange(0,9)
            if(naum5 < 3):
                row = 0
                num = naum5%3
            elif(naum5 < 6):
                row = 2
                num = naum5%3
            else:
                row = 1
                num = naum5%3
            if(rowData[row][num] == 0):
                rowData[row][num] = 2
                break

def ifEmptyBoard():
    global rowData
    nums = 0
    
    for i in range(3):
        for a in range(3):
            if(rowData[i][a] == 1 or rowData[i][a] == 2):
                nums = nums+1
    if(nums == 0):
        return True
    else:
        return False
    
main()





