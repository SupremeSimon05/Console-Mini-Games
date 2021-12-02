#For updating info:
#V1.12
#by 1:55 PM May 27, 2021
import pickle
import random
rows = [[1,1,1,1,1,1,1,1],[1,1,0,0,0,1,0,1],[0,0,0,1,0,0,0,1],[1,1,1,0,0,1,1,1],[1,0,0,0,1,0,0,1],[1,0,1,0,1,0,1,1],[1,0,0,0,0,0,1,1],[1,1,1,2,1,1,1,1]]
finish = [2,0]
UP = "\x1B[1A"
CLR = "\x1B[0K"

#makes the print statement clear the line before printing a new one
if(input("Are you using google colab? Enter 'no' exacly to make it work ").lower()=="no"):
    oprint = print
    def print(this, pre = CLR, end = "\n"):
        oprint(pre+this, end = end)

#lets you move the cursor up
def moveUp(times):
    for i in range(times):
        print(UP, end = "")

print("The Maze Game! ")
try:
    with open("mazeData.pickle", "rb") as f:
        data = pickle.load(f)
except:
    print("A new file called 'mazeData.pickle' should have been added, to erase your saved mazes locate the file and delete it.")
    with open("mazeData.pickle", "wb") as f:
        pickle.dump({}, f)
    with open("mazeData.pickle", "rb") as f:
        data = pickle.load(f)

def main():
    global data
    global rows
    global finish
    
    while(True):
        rows = [[1,1,1,1,1,1,1,1],[1,1,0,0,0,1,0,1],[0,0,0,1,0,0,0,1],[1,1,1,0,0,1,1,1],[1,0,0,0,1,0,0,1],[1,0,1,0,1,0,1,1],[1,0,0,0,0,0,1,1],[1,1,1,2,1,1,1,1]]
        finish = [2,0]
        while(True):
            mazeType = input("1: Default maze, 2: Self made maze, 3: Random maze, 4: Saved Mazes, 5: Clear Data ")
            try:
                if(int(mazeType)<=5 and int(mazeType)>=1):
                    break
                else:
                    print("That is not an option, please try again. ")
            except:
                if(mazeType.lower() == "exit"):
                    break
                print("Please enter numbers only")
        if(mazeType.lower() == "exit"):
            with open("mazeData.pickle", "wb") as f:
                f.close()
            break
        moveUp(3)
        if(mazeType == "2"):
            while(True):
                print("Maze creater: ")
                while(True):
                    sizex = input("How many rows? ")
                    sizey = input("How many columns? ")
                    try:
                        sizex = int(sizex)
                        sizey = int(sizey)
                        break
                    except:
                        print("Please enter integers only. ")
                moveUp(3)
                rows = []
                for i in range(sizex):
                    rows.append([])
                for i in range(sizex):
                    for a in range(sizey):
                        rows[i].append(0)
                while(True):
                    for i in range(sizex):
                        rowstr = ""
                        for a in range(sizey):
                            rowstr = rowstr + str(rows[i][a])
                        print(rowstr)
                    where = input("Where would you like to add a wall? Enter F to finish or R to remove a wall. ")
                    moveUp(sizex+3)
                    if(where.lower() == "f"):
                        break
                    elif(where.lower() == "r"):
                        where = input("Where would you like to remove a wall? ")
                        if("," in where):
                            where = where.split(",")
                            try:
                                where[0] = int(where[0])-1
                                where[1] = int(where[1])-1
                                try:
                                    where[2]
                                    print("Please only enter two numbers. ")
                                except:
                                    rows[where[0]][where[1]] = 0
                            except:
                                print("Please only enter two numbers. ")
                        else:
                            print("Please make sure to seperate the numbers by a comma. ")
                    else:
                        if("," in where):
                            where = where.split(",")
                            try:
                                where[0] = int(where[0])-1
                                where[1] = int(where[1])-1
                                try:
                                    where[2]
                                    print("Please only enter two numbers ")
                                except:
                                    rows[where[0]][where[1]] = 1
                            except:
                                print("Please only enter two numbers. ")
                        else:
                            print("Please make sure to seperate the numbers by a comma. ")
                while(True):
                    for i in range(sizex):
                        rowstr = ""
                        for a in range(sizey):
                            rowstr = rowstr + str(rows[i][a])
                        print(rowstr)
                    finish = input("Where do you want the finish? ")
                    moveUp(sizex+2)
                    if("," in finish):
                        finish = finish.split(",")
                        try:
                            finish[0] = int(finish[0])-1
                            finish[1] = int(finish[1])-1
                            if(rows[finish[0]][finish[1]] != 1):
                                break
                            else:
                                print("You can't end on walls. ")
                        except:
                            print("Please make sure to enter two numbers")
                    else:
                        print("Please put a comma between the two numbers")
                while(True):
                    for i in range(sizex):
                        rowstr = ""
                        for a in range(sizey):
                            rowstr = rowstr + str(rows[i][a])
                        print(rowstr)
                    start = input("Where do you want the start? ")
                    moveUp(sizex+2)
                    if("," in start):
                        start = start.split(",")
                        try:
                            start[0] = int(start[0])-1
                            start[1] = int(start[1])-1
                            if(rows[start[0]][start[1]]!=1):
                                rows[start[0]][start[1]] = 2
                                break
                            else:
                                print("You can't start on walls. ")
                        except:
                            print("Please make sure to enter two numbers")
                    else:
                        print("Please put a comma between the two numbers")
                possible = False
                for i in range(len(rows)):
                    rows[i].append(1)
                    rows[i].insert(0,1)
                borderArrs = []
                for i in range(len(rows[0])):
                    borderArrs.append(1)
                rows.append(borderArrs)
                rows.insert(0,borderArrs)
                finish[0] = finish[0]+1
                finish[1] = finish[1]+1
                while(True):
                    num = 0
                    while(num<=pow(sizey, sizex)):
                        num = num+1
                        direcs = "NESW"
                        direc = random.choice(direcs)
                        if(direc == "N"):
                            num = bW(num)
                        elif(direc == "E"):
                            num = bD(num)
                        elif(direc == "S"):
                            num = bS(num)
                        elif(direc == "W"):
                            num = bA(num)
                        if(location() == finish):
                            possible = True
                            break
                    if(possible):
                        print("This maze is possible")
                        x = location()[0]
                        y = location()[1]
                        rows[x][y] = 0
                        rows[start[0]+1][start[1]+1] = 2
                        if((input("Would you like to save this maze? ")+" ")[0].lower() == "y"):
                            while(True):
                                mazeName = input("What would you like to call this maze? ")
                                if(mazeName == "cancel"):
                                    print("That name is not avalible, sorry. ")
                                else:
                                    if(mazeName in data):
                                        if((input("Are you sure? That maze already exists, making this maze will delete the old one. ")+ " ")[0] == "y"):
                                            data[mazeName] = [rows, finish]
                                            break
                                    else:
                                        data[mazeName] = [rows, finish]
                                        break
                            with open('mazeData.pickle', 'wb') as f:
                                pickle.dump(data, f)
                                print("Maze saved. ")
                                
                        break
                    else:
                        print("The bot could not find a solution. ")
                        if((input("Would you like to have the bot try to finish it again? ") + " ")[0] == "n"):
                            break
                if(possible):
                    break
            moveUp(5)
        elif(mazeType == "3"):
            while(True):
                rows = []
                sizex = random.randrange(3, 11)
                sizey = random.randrange(3, 11)
                for i in range(sizex):
                    rows.append([])
                for i in range(sizex):
                    for a in range(sizey):
                        whatSpot = random.randrange(0,3)
                        if(whatSpot == 2):
                            rows[i].append(0)
                        elif(whatSpot == 0):
                            rows[i].append(0)
                        else:
                            rows[i].append(1)
                rows[len(rows)-1][len(rows[0])-1] = 0
                finish = [random.randrange(0, len(rows)-1), random.randrange(0, len(rows[0])-1)]
                start = [random.randrange(0, len(rows)-1), random.randrange(0, len(rows[0])-1)]
                rows[start[0]][start[1]] = 2
                for i in range(len(rows)):
                    rows[i].append(1)
                    rows[i].insert(0,1)
                borderArrs = []
                for i in range(len(rows[0])):
                    borderArrs.append(1)
                rows.append(borderArrs)
                rows.insert(0,borderArrs)
                finish[0] = finish[0]+1
                finish[1] = finish[1]+1
                start[0] = start[0]+1
                start[1] = start[1]+1
                while(True):
                    possible = False
                    for i in range(len(rows)):
                        rowstr = ""
                        for a in range(len(rows[i])):
                            rowstr = rowstr + str(rows[i][a])
                    num = 0
                    while(num<=1000):
                        num = num+1
                        direcs = "NESW"
                        direc = random.choice(direcs)
                        if(direc == "N"):
                            num = bW(num)
                        elif(direc == "E"):
                            num = bD(num)
                            num = num + 1
                        elif(direc == "S"):
                            num = bS(num)
                            num = num + 1
                        elif(direc == "W"):
                            num = bA(num)
                        if(location() == finish):
                            possible = True
                            break
                    if(possible):
                        x = location()[0]
                        y = location()[1]
                        rows[x][y] = 0
                        rows[start[0]][start[1]] = 2
                        break
                    else:
                        break
                if(possible):
                    break
        elif(mazeType == "4"):
            if(not loadMaze()):
                continue
            else:
                print("Maze loaded")
                
        elif(mazeType == "5"):
            with open("mazeData.pickle", "wb") as f:
                data = {}
                pickle.dump(data, f)
            continue
        for i in range(len(rows)):
            rows[i].append(1)
            rows[i].insert(0,1)
        borderArrs = []
        for i in range(len(rows[0])):
            borderArrs.append(1)
        rows.append(borderArrs)
        rows.insert(0,borderArrs)
        finish[0] = finish[0]+1
        finish[1] = finish[1]+1
                    
        while(True):
            print(" " + str(fF()) + " ")   
            print(str(fL()) + " " + str(fR()))
            print(" " + str(fB()) + " \n")
            inpt = input("Choose W,A,S,D ")
            if (inpt.lower() == "w"):
                W()
            if (inpt.lower() == "a"):
                A()
            if (inpt.lower() == "s"):
                S()
            if (inpt.lower() == "d"):
                D()
            if(location() == finish):
                moveUp(5)
                print("You made it to the finish! ")
                break
        
            
def W():
    moveUp(6)
    x = location()[0]
    y = location()[1]

    if(fF() != 0):
        rows[x-1][y] = 2
        rows[x][y] = 0
    else:
        print("Why did you hit your head off of the wall?")
        
def A():
    moveUp(6)
    x = location()[0]
    y = location()[1]
    
    if(fL() != 0):
        rows[x][y-1] = 2
        rows[x][y] = 0
    else:
        print("Why did you hit your head off of the wall?")



def S():
    moveUp(6)
    x = location()[0]
    y = location()[1]
    
    if(fB() != 0):
        rows[x+1][y] = 2
        rows[x][y] = 0
    else:
        print("Why did you hit your head off of the wall?")



def D():
    moveUp(6)
    x = location()[0]
    y = location()[1]
    
    if(fR() != 0):
        rows[x][y+1] = 2
        rows[x][y] = 0
    else:
        print("Why did you hit your head off of the wall?")


def fF(): 
    global rows 
    num = 0 
    x = location()[0] 
    y = location()[1]

    while(True):
        try:
            if(rows[x-1][y] == 1):
                break
            num = num + 1
        except:
            if(num>=location()[0]):
                num = location()[0]
            break
        x = x-1
    return num
    
def fB(): 
    global rows 
    num = 0 
    x = location()[0] 
    y = location()[1]
    
    while(True):
        try:
            if(rows[x+1][y] == 1):
                break
            num = num + 1
        except:
            if(num>=len(rows)-location()[0]):
                num = len(rows) - location()[0]
            break
        x = x+1
    return num    

def fL(): 
    global rows 
    num = 0 
    x = location()[0] 
    y = location()[1]

    while(True):
        try:
            if(rows[x][y-1] == 1):
                break
            num = num + 1
        except:
            if(num>=location()[1]):
                num = location()[1]
            break
        y = y-1
    return num
    
def fR(): 
    global rows 
    num = 0 
    x = location()[0] 
    y = location()[1]

    while(True):
        try:
            if(rows[x][y+1] == 1):
                break
            num = num + 1
        except:
            if(num>=len(rows[x]) - location()[1]):
                num = len(rows[x]) - location()[1]
            break
        y = y+1
    return num  
    
    
def location(): 
    global rows

    for a in range(len(rows)):
        for b in range(len(rows[a])):
            if(rows[a][b] == 2):
                return [a, b]

def bW(num): 
    x = location()[0]
    y = location()[1]

    if(fF() != 0):
        rows[x-1][y] = 2
        rows[x][y] = 0
        return num
    else:
        return num - 1
        
def bA(num):
    x = location()[0]
    y = location()[1]
    
    if(fL() != 0):
        rows[x][y-1] = 2
        rows[x][y] = 0
        return num
    else:
        return num - 1



def bS(num):
    x = location()[0]
    y = location()[1]
    
    if(fB() != 0):
        rows[x+1][y] = 2
        rows[x][y] = 0
        return num
    else:
        return num - 1


def bD(num):
    x = location()[0]
    y = location()[1]
    
    if(fR() != 0):
        rows[x][y+1] = 2
        rows[x][y] = 0
        return num
    else:
        return num - 1

def loadMaze():
    global rows
    global data
    global finish
    
    
    with open("mazeData.pickle", "rb") as f:
        data = pickle.load(f)
    if(len(data)>0):
        print("You have " + str(len(data)) + " mazes")
        mazeNames = ""
        for i in data:
            mazeNames = mazeNames+ "'" + str(i) + "', "
        print("Your mazes: " + mazeNames)
        while(True):
            whatMaze = input("What maze do you want to load? Enter 'cancel' to cancel. ")
            if(whatMaze in data):
                rows, finish = data[whatMaze]
                return True
                break
            elif(whatMaze.lower() == "cancel"):
                return False
                break
            else:
                print("That maze doesn't currently exist please try again or enter 'cancel' to cancel")
    else:
        print("You have no saved mazes, please try again when you save a maze. ")

main()
