try:
    from IPython.core.display import HTML
    display(HTML("<style>pre { white-space: pre !important; }</style>"))
except:
    pass

import tty, sys, termios, threading, time
import random
import json

#this makes the keys run simotaniously to the rest of the engine
class myThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        keycode.keyCollecter()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#makes the whole keyboard inputs work
class keycode:
    #the key you enter
    key = 0
    #this is so the arrow keys work as well, for some reason they show up as three different keys but this works anyway
    keystroke = [0,0,0]
    #sets the key variable to whatever you enter with some variations
    def keyCollecter():
        #does something to keep you from having to press enter
        filedescriptors = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        while 1:
            #codedly sets the key to the key you enter
            keycode.key = sys.stdin.read(1)
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            #moves the keystroke back one place and adds key to the end. the first gets deleted
            keycode.keystroke[0] = keycode.keystroke[1]
            keycode.keystroke[1] = keycode.keystroke[2]
            keycode.keystroke[2] = keycode.key
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            #goes through the keystrokes to find out if they make a pattern for a different key, such as the arrowkeys or 
            #enter keys or backspace
            if(keycode.keystroke[0] == "\x1b" and keycode.keystroke[1] == "[" and keycode.keystroke[2] == "D"):
                keycode.key = "leftAr"
            elif(keycode.keystroke[0] == "\x1b" and keycode.keystroke[1] == "[" and keycode.keystroke[2] == "A"):
                keycode.key = "upAr"
            elif(keycode.keystroke[0] == "\x1b" and keycode.keystroke[1] == "[" and keycode.keystroke[2] == "B"):
                keycode.key = "downAr"
            elif(keycode.keystroke[0] == "\x1b" and keycode.keystroke[1] == "[" and keycode.keystroke[2] == "C"):
                keycode.key = "rightAr"
            elif(keycode.key == "\n"):
                keycode.key = "enter"
            elif(keycode.key == "\x7f"):
                keycode.key = "backspace"
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #honestly have no idea what this is
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN,filedescriptors)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    #returns what key is being pressed if the attribute is left empty, an empty string if nothing is pressed
    #if the attribute is used then it will return true or false depending on if the entered key is being pressed
    def keydown(ofWhat = "empty"):
        if(ofWhat == "empty"):
            #when the return keyword is used the function breaks, for this reason we assign the ret value to 
            #keycode.key then reset the  keycode.key value and return the ret variable
            ret = keycode.key
            #resets key variable so it doesn't constantly return true
            keycode.key = ""
            return ret
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        elif(keycode.key == ofWhat):
            #resets key variable so it doesn't constantly return true
            keycode.key = ""
            return True
        else:
            return False
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
#makes the colors sorta global
#the colors are escape codes, when printed the background of a printed string turns those colors
class color:
    green = "\033[1;32;1m"
    #we do not disclude here
    gray="\033[1;37;1m"
    grey="\033[1;37;1m"
    #~~~~~~~~~~~~~~~~~~~~~~~
    red="\033[1;31;1m"
    yellow="\033[1;33;1m"
    blue="\033[1;34;1m"
    purple="\033[1;35;1m"
    cyan="\033[1;36;1m"
    white="\u001b[0m"
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




rowData = [[" ",0,0,0," "], [0,"G","G","G",0], [0,"G","H","G",0], [0,"G","G","G",0], [" ",0,0,0," "]]
people = [[0, "unemployed"],[0, "unemployed"],[0, "unemployed"],[0, "unemployed"],[0, "unemployed"]]
food = 500
ifExit = False
name = ""
tasks = []
wood = 0
metal = 0
woodIncreaseAmount = 10
metalIncreaseAmount = 10
maxAge = 10
woodToReceive = 0
metalToReceive = 0
researchAndFarm = []
peoplePerFarm = 1
foodToReceive = 0
researchBools = [False, False, False, False, False, False, False, False, False, False, False, False, False]
peoplePerLab = 1
treeRespawnChance = 1
chanceOfTwins = 0
materialRefundDivision = 10
data = {"rowData":rowData, "people":people, "food":food, "name":name, "tasks":tasks, "wood":wood, "metal":metal, "woodIncreaseAmount":woodIncreaseAmount, "metalIncreaseAmount":metalIncreaseAmount, "maxAge":maxAge, "peoplePerFarm":peoplePerFarm, "researchBools":researchBools, "peoplePerLab":peoplePerLab, "treeRespawnChance":treeRespawnChance, "chanceOfTwins":chanceOfTwins, "materialRefundDivision":materialRefundDivision}

'''
W = water
T = trees
D = docks
H = house
G = grass
M = mountain
F = fields
L = lab
'''
'''
Todo list:


Notes:
There might be a problem with the save system, some variables might not save properly.
'''
def main():
 global rowData
 global ifExit
 global people
 global food
 global name
 global maxAge
 global tasks
 global researchAndFarm
 global wood
 global metal
 if(not loadData()):
     name1 = randomCityName()
     name = input("Hello new king, this country needs a name what do you want it to be named? Suggested name: " + name1 + ". ")
     if(name == ""):
         name = name1
 while(not(ifExit)):
      update()
      while(True):
          if(len(people)<=0 or food<0):
              ifExit = True
              if(len(people)<=0):
                  print("All your people are dead. Game over.")
              else:
                  print("Your people have ran out of food and died. Game over")
          researchAndFarmStr = ""
          for i in range(len(researchAndFarm)):
              if(researchAndFarm[i][2] == "farming"):
                  researchAndFarmStr = researchAndFarmStr + "Farm " + str(i+1) + ": Row " + str(researchAndFarm[i][0] + 1) + ", column " + str(researchAndFarm[i][1] + 1) + ", people left that can work on this farm " + str(researchAndFarm[i][3]) + ". "
              else:
                  researchAndFarmStr = researchAndFarmStr + "Research " + str(i+1) + ": Row " + str(researchAndFarm[i][0] + 1) + ", column " + str(researchAndFarm[i][1] + 1) + ", people left that can work at this lab " + str(researchAndFarm[i][3]) + ". "
          if(len(researchAndFarm) > 0):
              print("Research and farming in progress: " + researchAndFarmStr)
          else:
              print("No research or farming in progress")
          print("Food amount: " + str(food))
          print("Wood amount: " + str(wood))
          print("Metal amount: " + str(metal))
          peepstr = "The people of " + str(name) + ": "
          for i in range(len(people)):
              peepstr = peepstr + "\nPerson " + str(i + 1) + ": Their age is " + str(people[i][0]) + " turns out of " + str(maxAge) + " turns, and they are " + str(people[i][1] + ". ")
          print(peepstr)
      
          inpt = input("What would you like your people to do? Enter T to see the tutorial. ")
          if(inpt == "^["):
              ifExit = True
              break
          elif(inpt.lower() == "t"):
              showTutorial()
          elif(inpt.lower() == "escape"):
              print("Enter escape code '^[' to exit program")
          elif(inpt.lower() == "w"):
              work()
          elif(inpt.lower() == "b"):
              build()
          elif(inpt.lower() == "n"):
              newLife()
          elif(inpt.lower() == "r"):
              research()
          elif(inpt.lower() == "d"):
              demolition()
          elif(inpt.lower() == "h"):
              hiring()
          elif(inpt.lower() == "f"):
              firing()
          elif(inpt.lower() == "e"):
              break
          showBoard(True)
          num = 0
          for i in range(len(tasks)):
              if(tasks[i - num][3] == 0):
                  tasks.remove(tasks[i-num])
                  num = num + 1
          if(len(tasks) > 0):
              taskStr = ""
              for i in range(len(tasks)):
                  taskStr = str(taskStr) + "Task " + str(i+1) + ": row " + str(tasks[i][0] + 1) + ", column " + str(realToAvalible(tasks[i][0], tasks[i][1])) + ", the task is " + str(tasks[i][2]) + ", turns left to complete " + str(tasks[i][3]) + ". "
              print("Tasks in progress: " + str(taskStr))
          else:
              print("No tasks in progress ")
          
          
def randomCityName():
  names1 = ["Lazy", "Strong", "Important", "Destructive", "Invincible", "Random", "Tiger", "Monkey", "Pug", "Dirt", "Litteral", "Virtual", "Fake", "Real", "My", "Grass", "Grape", "The Best"]
  names2 = [" Land", " Range", " Valley", " Country", " Utopia"]
  name1 = names1[random.randrange(0, len(names1))]
  name2 = names2[random.randrange(0, len(names2))]
  return name1 + name2
  
def showBoard(duringTurn = False):
    print("\033[2J")
    global rowData
    global name
    lens = []
    dashesStr = ""
    for i in range(len(rowData)):
        lens.append(len(rowData[i]))
    for i in range(max(lens)):
        dashesStr = dashesStr + "~"
    if(duringTurn):
        print("\nA map of " + str(name) + " at the end of your turn\n" + str(dashesStr))
    else:
        print("\nA map of " + str(name) + "\n" + str(dashesStr))
    for i in range(len(rowData)):
        for a in range(len(rowData[i])):
            if(rowData[i][a]=="T"):
                print(color.green, end="")
            elif(rowData[i][a]=="M"):
                print(color.grey, end="")
            elif(rowData[i][a]=="W"):
                print(color.blue, end="")
            elif(rowData[i][a]=="D"):
                print(color.red, end="")
            elif(rowData[i][a]=="H"):
                print(color.red, end="")
            elif(rowData[i][a]=="G"):
                print(color.green, end="")
            elif(rowData[i][a]=="F"):
                print(color.yellow, end="")
            elif(rowData[i][a]=="L"):
                print(color.grey, end="")
            else:
                print(color.white, end="")
            print(str(rowData[i][a]), end="")
        print(color.white)
    print(dashesStr+"\n")

#this function is called every turn 
def update():
  global name
  global rowData
  global tasks
  global people
  global wood
  global metal
  global metalToReceive
  global woodToReceive
  global food
  global foodToReceive
  global researchAndFarm
  global maxAge
  global treeRespawnChance
  global peoplePerLab
  global peoplePerFarm
  global researchBools
  global woodIncreaseAmount
  global metalIncreaseAmount
  global chanceOfTwins
  global materialRefundDivision
  num = 0
  
  food = food + foodToReceive
  foodToReceive = 0
  food = food - len(people)
  wood = wood + woodToReceive
  metal = metal + metalToReceive
  metalToReceive = 0
  woodToReceive = 0
  researchAndFarm = []
  for i in range(treeRespawnChance):
      rouw = random.randrange(0,len(rowData))
      rouw1 = random.randrange(0, len(rowData[rouw]))
      if(rowData[rouw][rouw1] == "G"):
          rowData[rouw][rouw1] = "T"
  for i in range(len(people)):
      people[i][0] = people[i][0] + 1
  for a in range(len(people)):
      try:
          for i in range(len(people)):
              if(people[i][0] > maxAge):
                  people.pop(i)
      except:
          pass
  for a in range(len(tasks)):
      if(tasks[a][2] == "new life"):
        tasks[a][3] = tasks[a][3] - 1

  for i in range(len(tasks)):
      if(tasks[i][2] == "new life" and tasks[i][3] == 0):
          for i in range(chanceOfTwins):
              num = random.randrange(0, len(rowData))
              num1 = random.randrange(0, len(rowData[num]))
              if(rowData[num][num1] == "H"):
                  people.append([0, "unemployed"])
          people.append([0, "unemployed"])
          for a in range(len(people)):
              if(people[a][1] == "pregnant"):
                  people[a][1] = "unemployed"
                  break
  for i in range(len(rowData)):
      while(True):
          if(rowData[i][len(rowData[i])-1] == " "):
              rowData[i].pop(len(rowData[i])-1)
          else:
              break
  for i in range(len(rowData)):
      for a in range(len(rowData[i])):
          num = num + 1
  for i in range(num*115):
      explore()
  doJobs()
  for i in range(num*115):
      explore()
  showBoard()
  num = 0
  for i in range(len(tasks)):
          if(tasks[i - num][3] == 0):
              tasks.remove(tasks[i-num])
              num = num + 1
  if(len(tasks) > 0):
      taskStr = ""
      for i in range(len(tasks)):
          taskStr = taskStr + "Task " + str(i+1) + ": row " + str(tasks[i][0] + 1) + ", column " + str(realToAvalible(tasks[i][0], tasks[i][1])) + ", the task is " + str(tasks[i][2]) + ", turns left to complete " + str(tasks[i][3])
      print("Tasks in progress: " + str(taskStr))
  else:
      print("No tasks in progress ")
  for i in range(len(people)):
      if(people[i][1] == "busy"):
          people[i][1] = "unemployed"
  data = {"rowData":rowData, "people":people, "food":food, "name":name, "tasks":tasks, "wood":wood, "metal":metal, "woodIncreaseAmount":woodIncreaseAmount, "metalIncreaseAmount":metalIncreaseAmount, "maxAge":maxAge, "peoplePerFarm":peoplePerFarm, "researchBools":researchBools, "peoplePerLab":peoplePerLab, "treeRespawnChance":treeRespawnChance, "chanceOfTwins":chanceOfTwins, "materialRefundDivision":materialRefundDivision}
  saveData()
#this is the function that makes it so the board can spread
def explore():
  global rowData
  global tasks
  naturalBlocks = ["G", "W", "T", "M", "T", "T", "M"]
  addThisToI = 0
  nums = []
  highestNum = 0
  for i in range(len(rowData)):
      nums.append(len(rowData[i]))
  highestNum = max(nums)
  for i in range(len(rowData)):
      while(True):
          if(len(rowData[i])>=highestNum):
              break
          else:
              rowData[i].append(" ")
  for i in range(len(rowData)):
      for a in range(len(rowData[i])):
          #Start of fail safe
          while(True):
              try:
                  rowData[i + addThisToI][a] == "G" or rowData[i + addThisToI][a] == "D"
                  break
              except:
                  rowData[i + addThisToI].append(" ")
          #End of fail safe
           
          if(rowData[i + addThisToI][a] == "G" or rowData[i + addThisToI][a] == "D"):
              if(i-1 < 0):
                  rowData.insert(0, [])
                  taskMoveDown()
                  for b in range(a):
                      rowData[0].append(" ")
                  rowData[0].append(0)
                  for b in range(len(rowData[1]) - a):
                      rowData[0].append(" ")
                  addThisToI = addThisToI+1
               
              try:
                  if(rowData[i-1 + addThisToI][a] == " "):
                      rowData[i-1 + addThisToI][a] = 0
              except:
                  pass
               
              try:
                  if(rowData[i + addThisToI][a+1] == " "):
                      rowData[i + addThisToI][a+1] = 0
              except:
                  for b in range(len(rowData)):
                      if(rowData[b][len(rowData[b])-1] == "G" or rowData[b][len(rowData[b])-1] == "D"):
                          rowData[b].append(0)
                      else:
                          rowData[b].append(" ")
              try:
                  if(rowData[i+1 + addThisToI][a] == " "):
                      rowData[i+1 + addThisToI][a] = 0
              except:
                  rowData.append([])
                  for b in range(a):
                      rowData[len(rowData)-1].append(" ")
                  rowData[len(rowData)-1].append(0)
                  for b in range(len(rowData[1]) - a):
                      rowData[len(rowData)-1].append(" ")
                  addThisToI = addThisToI+1
              if(a-1<0):
                  for b in range(len(rowData)):
                      if(rowData[b][len(rowData[b])-1] == "G" or rowData[b][len(rowData[b])-1] == "D"):
                          rowData[b].insert(0, 0)
                          for c in range(len(tasks)):
                              if(tasks[c][0] == b):
                                  tasks[c][1] = tasks[c][1] + 1
                      else:
                          rowData[b].insert(0, " ")
                          for c in range(len(tasks)):
                              if(tasks[c][0] == b):
                                  tasks[c][1] = tasks[c][1] + 1
              if(rowData[i + addThisToI][a-1] == " "):
                  rowData[i + addThisToI][a-1] = 0
      
  for i in range(len(rowData)):
      for a in range(len(rowData[i])):             
          if(rowData[i][a] == 0):
              rowData[i][a] = naturalBlocks[random.randrange(0, len(naturalBlocks))]
def showTutorial():
  while(True):
      choice = input("\nEnter the number that corresponds to what you would like to know more about .\n1: Map, 2: People, 3: Spots, 4: Research, 5: Command List, 6: Employment, 7: Tasks. ")
      try:
          choice = int(choice)
          if(choice<=7 and choice>0):
              break
          else:
              print("That is not a valid option")
      except:
          if(choice == "^["):
              ifExit = True
              break
          elif(choice.lower() == "escape"):
              print("The escape code is ^[")
          else:
              print("Please enter numbers only.")
  if(choice == 1):
      print("Map:\nThe map is the base of the game, to be able to do anything you need to be able to read the map.\nThe map is divided into rows and columns. Rows always go first, then columns. The topmost then leftmost place on the map is '1,1', as in row 1 column 1.\nThere are different letters for different spots on the map. W for water, T for trees, D for docks, H for house, G for grass, M for mountain, F for fields, L for lab")        
  if(choice == 2):
      print("People:\nThe people are what make the world go round, without them you wouldn't be able to do anything.\nWhen it shows you your people there are three different values that show up for each person. The first one is the person's age, the second is their job, the third is the amount of times left that they can reproduce.\nTo get more people you need to put two people in a house. After that one of the people will be employed as pregnant and will stay that way for 2 turns, after that a new person with age 0 will be added to the list of people.\nAt the start of the game, each person can live for 10 turns. Through research that amount can be increased\nEvery turn each person consumes 1 food, use fields to get more food.")
  if(choice == 3):
      print("Spots:\nThere are many different spots that will let you do different things. Water is just a bad thing, you can't do anything with water except build Docks on it so you can access land on the other side and build a house over it. You can't build a field over a dock unless a house is built then destroyed over it. Docks cost 150 wood and take 15 turns to build. Trees give you wood, wood is used to build different buildings. Trees give you 10 wood each to start but can be upgraded through research. Trees take one turn to remove.\nGrass allows you to build buildings and fields on. Houses let you get more people, check the tutorial for people for a little more information. Houses cost 100 wood and take 10 turns to build.\nMountains give you metal, metal can be used to build things. At the start of the game you get 10 metal per mountain, this can be upgraded with research. Mountains take 2 turns to remove.\nLabs are used to do research. Labs cost 200 metal and take 20 turns to build. Visit the research tutorial for more information.\nFields give you food, 5 food per turn per person. At the start of the game only 1 person can work in a field at a time. This can be upgraded through research. Each field costs 50 wood and take 3 turns to build.")
  if(choice == 4):
      print("Research:\nResearch just lets you upgrade certain things in the game. When you choose to do research you will see the research tree.\nThis will show you what can and will be able to upgrade. If it has a number letter or symbol to it instead of just the '?' then you are able to upgrade it.\nTo choose what you want to upgrade you just enter its name. After doing so it will show you the price and ask if you are sure about upgrading it. \nResearch is extreamly expensive. You should hold off on it until you explore at least 100 spots on the map. ")
  if(choice == 5):
      print("For the main prompt, the one that asks you what you want your people to do, these are the commands for the people.\nT to see this tutorial, 'Escape' to see the code to end the program, B to build, D to destroy, W to have your people work, H to hire, F to fire, R to do research, N to have your people reproduce, E to end turn")
  if(choice == 6):
      print("Hiring people will make it so a bot will have the people do whatever they are hired to do. To activate hiring for certain jobs you must research it in the research tree. You can only control people that are unemployed, to make a person unemployed you must fire them from their job")
  if(choice == 7):
      print("The task list shows you the tasks that your people have already started. You can do an infinite amount of tasks at a time, when hiring the bot will try to have the people complete already started tasks before starting a new task.")
   
def work():
  global rowData
  global people
  global tasks
  global wood
  global metal
  global woodIncreaseAmount
  global metalIncreaseAmount
  global woodToReceive
  global metalToReceive
  global researchAndFarm
  global peoplePerFarm
  global foodToReceive
  peepstr = ""
  end = False
  peepstr = "Age " + str(people[0][0]) + ", is " + str(people[0][1])
  print("Working includes removing trees, removing mountains and working in fields")
  while(True):
      who = input("\nWho do you want to have work? Enter the number that the person appears in the list that says 'the people of your country:'\nRight now if you were to enter 1 you would get " + str(peepstr) + ". Enter 'cancel' to cancel. ")
      try:
          who = int(who)-1
          if(who<len(people) and who>=0):
              if(people[who][1] == "unemployed"):
                  break
              else:
                  print("Currently that person is " + str(people[who][1]) + ". They must be unemployed to do work.")
          else:
              print("Please choose a person that actually exists. ")
      except:
          if(who.lower() == "cancel"):
              end = True
              break
          else:
              print("Please enter numbers only")
  for i in range(len(rowData)):
      rowData[i].append(" ")
  while(not(end)):
      where = input("\nAt what spot do you want this person to work? Right now 1,1 is " + str(rowData[0][avalibleToReal(1, 1)]) + ". Enter 'cancel' to cancel. ")
      if("," in where):
          where = where.split(",")
          if(type(avalibleToReal(int(where[0]), int(where[1]))) == int):
              where = str(int(where[0])-1) +","+ str(avalibleToReal(int(where[0]), int(where[1])))
              where = where.split(",")
              if(rowData[int(where[0])][int(where[1])] == "T"):
                  rowData[int(where[0])][int(where[1])] = "G"
                  woodToReceive = woodToReceive + woodIncreaseAmount
                  break
              elif(rowData[int(where[0])][int(where[1])] == "M"):
                  if(isTaskInProgress(int(where[0]), int(where[1]))):
                      tasks[tasks.index([int(where[0]), int(where[1]), "mountain", 1])][3] = 0
                      rowData[int(where[0])][int(where[1])] = "G"
                      metalToReceive = metalToReceive + metalIncreaseAmount
                      break
                  else:
                      tasks.append([int(where[0]), int(where[1]), "mountain", 1])
                      break
              elif(rowData[int(where[0])][int(where[1])] == "F"):
                  whatFarm = -1
                  for i in range(len(researchAndFarm)):
                      if(researchAndFarm[i][0] == int(where[0]) and researchAndFarm[i][1] == int(where[1]) and researchAndFarm[i][2] == "farming"):
                          whatFarm = i
                  if(whatFarm == -1):
                      researchAndFarm.append([int(where[0]), int(where[1]), "farming", peoplePerFarm - 1])
                      foodToReceive = foodToReceive + 5
                      break
                  else:
                      if(researchAndFarm[whatFarm][3] > 0):
                          researchAndFarm[whatFarm][3] = researchAndFarm[whatFarm][3] - 1
                          foodToReceive = foodToReceive + 5
                          break
                      else:
                          print("No more people are allowed to work at this farm")
              else:
                  print(where)
                  print("You cannot work on " + rowData[int(where[0])][int(where[1])] + "s.")
          else:
              print("The numbers you entered did not work. Please try again ")
      else:
          if(where.lower() == "cancel"):
              end = True
              break
          else:
              print("Please make sure to enter two numbers separated by a comma")
  if(not end):
      people[who][1] = "busy"
      
def avalibleToReal(x, y):
  global rowData
  num = 0
  num1 = 0
  x = x-1
  for i in range(len(rowData[x])):
      if(num == y):
          return i - 1
          num1 = num1 + 1
      elif(rowData[x][i] != " "):
          num = num + 1
  if(num1 == 0):
      print(rowData[x])
      if(len(rowData[x]) == y):
          return y - 1
      else:
          return False
def isTaskInProgress(x, y):
  global tasks
  num = 0
  for i in range(len(tasks)):
      if(tasks[i][0] == x and tasks[i][1] == y):
          num = num + 1
  if(num == 0):
      return False
  else:
      return True
def taskMoveDown():
  global tasks
  for i in range(len(tasks)):
      tasks[i][0] = tasks[i][0] + 1
      
def build():
  global rowData
  global people
  global tasks
  global wood
  global metal
  global woodIncreaseAmount
  global metalIncreaseAmount
  global woodToReceive
  global metalToReceive
  end = False
  askforWhat = False
  peepstr = "Age " + str(people[0][0]) + ", is " + str(people[0][1])
  print("You can build Labs, Docks, Houses, and Fields. ")
  while(True):
      who = input("\nWho do you want to have build? Enter the number that the person appears in the list that says 'the people of your country:'.\nRight now if you were to enter 1 you would get " + str(peepstr) + ". Enter 'cancel' to cancel. ")
      try:
          who = int(who)-1
          if(who<len(people) and who>=0):
              if(people[who][1] == "unemployed"):
                  break
              else:
                  print("Currently that person is " + str(people[who][1]) + ". They must be unemployed to build.")
          else:
              print("Please choose a person that actually exists. ")
      except:
          if(who.lower() == "cancel"):
              end = True
              break
          else:
              print("Please enter numbers only")
  while(not(end)):
      where = input("\nAt what spot do you want this person to build? Right now 2,2 is " + str(rowData[1][avalibleToReal(2, 2)]) + ". Enter 'cancel' to cancel. ")
      if("," in where):
          where = where.split(",")
          if(type(avalibleToReal(int(where[0]), int(where[1]))) == int):
              where = str(int(where[0])-1) +","+ str(avalibleToReal(int(where[0]), int(where[1])))
              where = where.split(",")
              if((rowData[int(where[0])][int(where[1])] == "G") or (rowData[int(where[0])][int(where[1])] == "D") or (rowData[int(where[0])][int(where[1])] == "W")):
                  if(isTaskInProgress(int(where[0]), int(where[1]))):
                      for i in range(len(tasks)):
                          if(int(tasks[i][0]) == int(where[0]) and int(tasks[i][1]) == int(where[1])):
                              tasks[i][3] = tasks[i][3] - 1
                              if(tasks[i][3] <= 0):
                                  if(tasks[i][2] == "building fields"):
                                      rowData[int(where[0])][int(where[1])] = "F"
                                  elif(tasks[i][2] == "building docks"):
                                      rowData[int(where[0])][int(where[1])] = "D"
                                  elif(tasks[i][2] == "building house"):
                                      rowData[int(where[0])][int(where[1])] = "H"
                                  elif(tasks[i][2] == "building lab"):
                                      rowData[int(where[0])][int(where[1])] = "L"
                  else:
                      askforWhat = True
                  break
              else:
                  print("You cannot build on " + rowData[int(where[0])][int(where[1])] + "s.")
          else:
              print("The numbers you entered did not work. Please try again ")
      else:
          if(where.lower() == "cancel"):
              end = True
              break
          else:
              print("Please make sure to enter two numbers separated by a comma")
           
  while((not end) and askforWhat):
      whatToBuild = input("What would you like to build? H for House, D for Docks, F for Field, L for lab. ")
      whatToBuild = whatToBuild.upper()
      if(whatToBuild == "D" and rowData[int(where[0])][int(where[1])] == "W"):
          if(wood>= 150):
              tasks.append([int(where[0]), int(where[1]), "building docks", 15])
              wood = wood - 150
              break
          else:
              print("You don't have enough wood to do that. ")
      elif(whatToBuild == "H" and (rowData[int(where[0])][int(where[1])] == "D" or rowData[int(where[0])][int(where[1])] == "G")):
          if(wood >= 100):
              tasks.append([int(where[0]), int(where[1]), "building house", 10])
              wood = wood - 100
              break
          else:
              print("You don't have enough wood to do that. ")
      elif(whatToBuild == "F" and rowData[int(where[0])][int(where[1])] == "G"):
          if(wood >= 50):
              tasks.append([int(where[0]), int(where[1]), "building fields", 3])
              wood = wood - 50
              break
          else:
              print("You don't have enough wood to do that. ")
      elif(whatToBuild == "L" and (rowData[int(where[0])][int(where[1])] == "D" or rowData[int(where[0])][int(where[1])] == "G")):
          if(metal >= 200):
              tasks.append([int(where[0]), int(where[1]), "building lab", 20])
              metal = metal - 200
              break
          else:
              print("You don't have enough metal to do that. ")
      else:
          if(whatToBuild.lower() == "cancel"):
              break
          else:
              print("You can't build " + str(whatToBuild) + "s on " + str(rowData[int(where[0])][int(where[1])]))
  if(not end):
      people[who][1] = "busy"
   
def realToAvalible(x, y):
  global rowData
  num = 0
  try:
      for i in range(len(rowData[x])):
          if(rowData[x][i] != " "):
              num = num + 1
          if(y == i):
              return num
              break
  except:
      pass
  
def newLife():
  global rowData
  global people
  global tasks
  peepstr = "Age " + str(people[0][0]) + ", is " + str(people[0][1])
  appendTask = False
  end = False
  while(True):
      where = input("\nAt what spot do you want to have the people mate? 2,2 is " + str(rowData[1][avalibleToReal(2, 2)]) + ". Enter 'cancel' to cancel. ")
      if("," in where):
          where = where.split(",")
          if(type(avalibleToReal(int(where[0]), int(where[1]))) == int):
              where = str(int(where[0])-1) +","+ str(avalibleToReal(int(where[0]), int(where[1])))
              where = where.split(",")
              if(rowData[int(where[0])][int(where[1])] == "H"):
                  if(not(isTaskInProgress(int(where[0]), int(where[1])))):
                      appendTask = True
                      break
                  else:
                      print("People are either pregnant or mating here, please choose a different location ")
              else:
                  print("You cannot have your people mate on " + rowData[int(where[0])][int(where[1])] + "s.")
          else:
              print("The numbers you entered did not work. Please try again ")
      else:
          if(where.lower() == "cancel"):
              end = True
              break
          else:
              print("Please make sure to enter two numbers separated by a comma")
  while(not end):
      who = input("\nWho is the first person that you want to have mate? Enter the number that the person appears in the list that says 'the people of your country:'.\nRight now if you were to enter 1 you would get " + str(peepstr) + ". Enter 'cancel' to cancel. ")
      try:
          who = int(who)-1
          if(who<len(people) and who>=0):
              if(people[who][1] == "unemployed"):
                  break
              else:
                  print("Currently that person is " + str(people[who][1]) + ". They must be unemployed to build.")
          else:
              print("Please choose a person that actually exists. ")
      except:
          if(who.lower() == "cancel"):
              end = True
              break
          else:
              print("Please enter numbers only")
  while(not end):
      who1 = input("\nWho is the second person that you want to have mate? Enter the number that the person appears in the list that says 'the people of your country:'.\nRight now if you were to enter 1 you would get " + str(peepstr) + ". Enter 'cancel' to cancel. ")
      try:
          who1 = int(who1)-1
          if(who1<len(people) and who1>=0 and who1 != who):
              if(people[who1][1] == "unemployed"):
                  break
              else:
                  print("Currently that person is " + str(people[who1][1]) + ". They must be unemployed to build.")
          else:
              print("Please choose a person that actually exists and isn't already choosen. ")
      except:
          if(who1.lower() == "cancel"):
              end = True
              break
          else:
              print("Please enter numbers only")
  if((not end) and appendTask):
      people[who][1] = "pregnant"
      people[who1][1] = "busy"
      tasks.append([int(where[0]), int(where[1]), "new life", 2])
  
def research():
  global researchBools
  global researchAndFarm
  global peoplePerLab
  global metal
  global wood
  global tasks
  global woodIncreaseAmount
  global metalIncreaseAmount
  global chanceOfTwins
  global materialRefundDivision
  global maxAge
  global treeRespawnChance
  global peoplePerFarm

  peepstr = ""
  end = False
  peepstr = "Age " + str(people[0][0]) + ", is " + str(people[0][1])
  print("Research lets you upgrade certain things. ")
  while(True):
      who = input("\nWho do you want to have do the research? Enter the number that the person appears in the list that says 'the people of your country:'.\nRight now if you were to enter 1 you would get " + str(peepstr) + ". Enter 'cancel' to cancel. ")
      try:
          who = int(who)-1
          if(who<len(people) and who>=0):
              if(people[who][1] == "unemployed"):
                  break
              else:
                  print("Currently that person is " + str(people[who][1]) + ". They must be unemployed to do work.")
          else:
              print("Please choose a person that actually exists. ")
      except:
          if(who.lower() == "cancel"):
              end = True
              break
          else:
              print("Please enter numbers only")
  for i in range(len(rowData)):
      rowData[i].append(" ")
  while(not(end)):
      where = input("\nAt what spot do you want this person to do the research? Right now 1,1 is " + str(rowData[0][avalibleToReal(1, 1)]) + ". Enter 'cancel' to cancel. ")
      if("," in where):
          where = where.split(",")
          if(type(avalibleToReal(int(where[0]), int(where[1]))) == int):
              where = str(int(where[0])-1) +","+ str(avalibleToReal(int(where[0]), int(where[1])))
              where = where.split(",")
              if(rowData[int(where[0])][int(where[1])] == "L"):
                  whatLab = -1
                  for i in range(len(researchAndFarm)):
                      if(researchAndFarm[i][0] == int(where[0]) and researchAndFarm[i][1] == int(where[1]) and researchAndFarm[i][2] == "researching"):
                          whatLab = i
                  if(whatLab == -1):
                      break
                  else:
                      if(researchAndFarm[whatLab][3] > 0):
                          break
                      else:
                          print("No more people are allowed to research at this lab")
              else:
                  print("You cannot do research on " + rowData[int(where[0])][int(where[1])] + "s.")
          else:
              print("The numbers you entered did not work. Please try again ")
      else:
          if(where.lower() == "cancel"):
              end = True
              break
          else:
              print("Please make sure to enter two numbers separated by a comma")
  while((not end)):
      print("    ---------")
      print("    |       |")
      if(researchBools[0] and researchBools[2]):
          print("   -3-7---- |")
      elif(researchBools[0]):
          print("   -3-?---- |")
      else:
          print("   -?-?---- |")
      print("   |      | |")
      if(researchBools[5] and researchBools[8] and researchBools[10] and researchBools[9]):
          print("-1--2-6-A-B-9")
      elif(researchBools[5] and researchBools[2] and researchBools[3]):
          print("-1--2-6-A-?-9")
      elif(researchBools[1] and researchBools[2] and researchBools[3]):
          print("-1--2-6-?-?-9")
      elif(researchBools[0] and researchBools[2] and researchBools[3]):
          print("-1--2-?-?-?-9")
      elif(researchBools[5]):
          print("-1--2-6-A-?-?")
      elif(researchBools[1]):
          print("-1--2-6-?-?-?")
      elif(researchBools[0]):
          print("-1--2-?-?-?-?")
      else:
          print("-1--?-?-?-?-?")
      print("   |      | |")
      if(researchBools[3]):
          print("   -4-!---- |")
      elif(researchBools[0]):
          print("   -4-?---- |")
      else:
          print("   -?-?---- |")
      print("   ||       |")
      print("   |---------")
      if(researchBools[7]):
          print("   --5-8-C")
      elif(researchBools[4]):
          print("   --5-8-?")
      elif(researchBools[0]):
          print("   --5-?-?")
      else:
          print("   --?-?-?")
      print("1: People per lab increase. 2: Wood per tree increase. 3: Metal per mountain increase. 4: People per farm increase. 5: Life expectancy increase. 6: Tree respawn chance increase.\n7: Enable hiring for mountains. 8: Increased chance of multiple people on birth. 9: Increased refunds on building demolition. !: Hiring enabled for farms. A: Hiring enabled for trees. B: Hiring enabled for building. C: Hiring enabled for mating")
      whatToUpgrade = input("What would you like to upgrade? If it shows up as a '?' you cannot yet upgrade it. To unlock certain upgrades you need to upgrade already unlocked upgrades.\nYou will get to see the price after you select an option. Enter 'cancel' to cancel. ")
      toBreak = False
      can = True
      print()
      if(((whatToUpgrade == "2" or whatToUpgrade == "3" or whatToUpgrade == "4" or whatToUpgrade == "5") and not researchBools[0]) or (whatToUpgrade == "7" and not researchBools[2]) or (whatToUpgrade == "6" and not researchBools[1]) or (whatToUpgrade == "!" and not researchBools[3]) or (whatToUpgrade == "8" and not researchBools[4]) or (whatToUpgrade.lower() == "a" and not researchBools[5]) or (whatToUpgrade.lower() == "b" and not (researchBools[10] or researchBools[6] or researchBools[9] or researchBools[8])) or (whatToUpgrade == "9" and not (researchBools[3] or researchBools[2])) or (whatToUpgrade.lower() == "c" and not researchBools[7])):
          can = False
      if(not can):
          print("You can't upgrade that yet. Please try again. ")
      turnAmount = 0
      while(can):
          apend = True
          try:
              whatToUpgrade = int(whatToUpgrade)
              yn = ""
              if(whatToUpgrade == 1):
                  if(wood>= 50 and metal>= 50):
                      yn = (input("This upgrade costs 50 wood and 50 metal and takes 1 turn. Are you sure you would like to buy this? ") + " ")[0]
                      toBreak = True
                      if(yn.lower() == "y"):
                          wood = wood - 50
                          metal = metal - 50
                          turnAmount = 1
                          for i in range(len(tasks)):
                              if(tasks[i][2] == "Researching #1"):
                                  if(tasks[i][3] <= 1):
                                      researchBools[0] = True
                                      peoplePerLab = peoplePerLab + 1
                                  apend = False
                                  tasks[i][3] = tasks[i][3]-1
                          if(apend):
                              tasks.append([int(where[0]), int(where[1]), "Researching #1", 1])
                          break
                      elif(yn.lower() == "n"):
                          end = True
                          break
                      else:
                          print("Only write 'yes' or 'no'")
                  else:
                      print("This upgrade costs 50 wood and 50 metal and takes 1 turn, you don't have enough materials. Please try again later")
                      break
              elif(whatToUpgrade == 2):
                  if(wood>= 55 and metal>= 55):
                      yn = (input("This upgrade costs 55 wood and 55 metal and takes 2 turns. Are you sure you would like to buy this? ") + " ")[0]
                      toBreak = True
                      if(yn.lower() == "y"):
                          wood = wood -55
                          metal = metal -55
                          turnAmount = 2
                          for i in range(len(tasks)):
                              if(tasks[i][2] == "Researching #2"):
                                  if(tasks[i][3] <= 1):
                                      researchBools[1] = True
                                      woodIncreaseAmount = woodIncreaseAmount + 1
                                  apend = False
                                  tasks[i][3] = tasks[i][3]-1
                          if(apend):
                              tasks.append([int(where[0]), int(where[1]), "Researching #2", 2])
                          break
                      elif(yn.lower() == "n"):
                          end = True
                          break
                      else:
                          end = True
                          print("Only write 'yes' or 'no'")
                  else:
                      print("This upgrade costs 55 wood and 55 metal and takes 2 turns, you don't have enough materials. Please try again later")
                      break
              elif(whatToUpgrade == 3):
                  if(wood>= 60 and metal>= 60):
                      yn = (input("This upgrade costs 60 wood and 60 metal and takes 3 turns. Are you sure you would like to buy this? ") + " ")[0]
                      toBreak = True
                      if(yn.lower() == "y"):
                          wood = wood -60
                          metal = metal - 60
                          turnAmount = 3
                          for i in range(len(tasks)):
                              if(tasks[i][2] == "Researching #3"):
                                  if(tasks[i][3] <= 1):
                                      researchBools[2] = True
                                      metalIncreaseAmount = metalIncreaseAmount + 1
                                  apend = False
                                  tasks[i][3] = tasks[i][3]-1
                          if(apend):
                              tasks.append([int(where[0]), int(where[1]), "Researching #3", 3])
                          break
                      elif(yn.lower() == "n"):
                          end = True
                          break
                      else:
                          end = True
                          print("Only write 'yes' or 'no'")
                  else:
                      print("This upgrade costs 60 wood and 60 metal and takes 3 turns, you don't have enough materials. Please try again later")
                      break
              elif(whatToUpgrade == 4):
                  if(wood>= 65 and metal>= 65):
                      yn = (input("This upgrade costs 65 wood and 65 metal and takes 4 turns. Are you sure you would like to buy this? ") + " ")[0]
                      toBreak = True
                      if(yn.lower() == "y"):
                          wood = wood - 65
                          metal = metal - 65
                          turnAmount = 4
                          for i in range(len(tasks)):
                              if(tasks[i][2] == "Researching #4"):
                                  if(tasks[i][3] <= 1):
                                      researchBools[3] = True
                                      peoplePerFarm = peoplePerFarm + 1
                                  apend = False
                                  tasks[i][3] = tasks[i][3]-1
                          if(apend):
                              tasks.append([int(where[0]), int(where[1]), "Researching #4", 4])
                          break
                      elif(yn.lower() == "n"):
                          end = True
                          break
                      else:
                          print("Only write 'yes' or 'no'")
                  else:
                      print("This upgrade costs 65 wood and 65 metal and takes 4 turns, you don't have enough materials. Please try again later")
                      break
              elif(whatToUpgrade == 5):
                  if(wood>= 70 and metal>= 70):
                      yn = (input("This upgrade costs 70 wood and 70 metal and takes 5 turns. Are you sure you would like to buy this? ") + " ")[0]
                      toBreak = True
                      if(yn.lower() == "y"):
                          wood = wood -70
                          metal = metal - 70
                          turnAmount = 5
                          for i in range(len(tasks)):
                              if(tasks[i][2] == "Researching #5"):
                                  if(tasks[i][3] <= 1):
                                      researchBools[4] = True
                                      maxAge = maxAge + 1
                                  apend = False
                                  tasks[i][3] = tasks[i][3]-1
                          if(apend):
                              tasks.append([int(where[0]), int(where[1]), "Researching #5", 5])
                          break
                      elif(yn.lower() == "n"):
                          end = True
                          break
                      else:
                          print("Only write 'yes' or 'no'")
                         
                  else:
                      print("This upgrade costs 70 wood and 70 metal and takes 5 turns, you don't have enough materials. Please try again later")
                      break
              elif(whatToUpgrade == 6):
                  if(wood>= 75 and metal>= 75):
                      yn = (input("This upgrade costs 75 wood and 75 metal and takes 6 turns. Are you sure you would like to buy this? ") + " ")[0]
                      toBreak = True
                      if(yn.lower() == "y"):
                          wood = wood -75
                          metal = metal - 75
                          turnAmount = 6
                          for i in range(len(tasks)):
                              if(tasks[i][2] == "Researching #6"):
                                  if(tasks[i][3] <= 1):
                                      researchBools[5] = True
                                      treeRespawnChance = treeRespawnChance + 1
                                  apend = False
                                  tasks[i][3] = tasks[i][3]-1
                          if(apend):
                              tasks.append([int(where[0]), int(where[1]), "Researching #6", 6])
                          break
                      elif(yn.lower() == "n"):
                          end = True
                          break
                      else:
                          print("Only write 'yes' or 'no'")
                         
                  else:
                      print("This upgrade costs 75 wood and 75 metal and takes 6 turns, you don't have enough materials. Please try again later")
                      break
              elif(whatToUpgrade == 7):
                  if(wood>= 80 and metal>= 80):
                      yn = (input("This upgrade costs 80 wood and 80 metal and takes 7 turns. Are you sure you would like to buy this? ") + " ")[0]
                      toBreak = True
                      if(yn.lower() == "y"):
                          wood = wood -80
                          metal = metal - 80
                          turnAmount = 7
                          for i in range(len(tasks)):
                              if(tasks[i][2] == "Researching #7"):
                                  if(tasks[i][3] <= 1):
                                      researchBools[6] = True
                                      #here
                                  apend = False
                                  tasks[i][3] = tasks[i][3]-1
                          if(apend):
                              tasks.append([int(where[0]), int(where[1]), "Researching #7", 7])
                          break
                      elif(yn.lower() == "n"):
                          end = True
                          break
                      else:
                          print("Only write 'yes' or 'no'")
                         
                  else:
                      print("This upgrade costs 80 wood and 80 metal and takes 7 turns, you don't have enough materials. Please try again later")
                      break
              elif(whatToUpgrade == 8):
                  if(wood>= 85 and metal>= 85):
                      yn = (input("This upgrade costs 85 wood and 85 metal and takes 8 turns. Are you sure you would like to buy this? ") + " ")[0]
                      toBreak = True
                      if(yn.lower() == "y"):
                          wood = wood -85
                          metal = metal - 85
                          turnAmount = 8
                          for i in range(len(tasks)):
                              if(tasks[i][2] == "Researching #8"):
                                  if(tasks[i][3] <= 1):
                                      researchBools[7] = True
                                      chanceOfTwins = chanceOfTwins + 1
                                  apend = False
                                  tasks[i][3] = tasks[i][3]-1
                          if(apend):
                              tasks.append([int(where[0]), int(where[1]), "Researching #8", 8])
                          break
                      elif(yn.lower() == "n"):
                          end = True
                          break
                      else:
                          print("Only write 'yes' or 'no'")
                         
                  else:
                      print("This upgrade costs 85 wood and 85 metal and takes 8 turns, you don't have enough materials. Please try again later")
                      break
              elif(whatToUpgrade == 9):
                  if(wood>= 90 and metal>= 90):
                      yn = (input("This upgrade costs 90 wood and 90 metal and takes 9 turns. Are you sure you would like to buy this? ") + " ")[0]
                      toBreak = True
                      if(yn.lower() == "y"):
                          wood = wood -90
                          metal = metal - 90
                          turnAmount = 9
                          for i in range(len(tasks)):
                              if(tasks[i][2] == "Researching #9"):
                                  if(tasks[i][3] <= 1):
                                      researchBools[8] = True
                                      materialRefundDivision = materialRefundDivision - 1
                                  apend = False
                                  tasks[i][3] = tasks[i][3]-1
                          if(apend):
                              tasks.append([int(where[0]), int(where[1]), "Researching #9", 9])
                          break
                      elif(yn.lower() == "n"):
                          end = True
                          break
                      else:
                          print("Only write 'yes' or 'no'")
                         
                  else:
                      print("This upgrade costs 90 wood and 90 metal and takes 9 turns, you don't have enough materials. Please try again later")
                      break
              elif(whatToUpgrade == 10):
                  if(wood>= 95 and metal>= 95):
                      yn = (input("This upgrade costs 95 wood and 95 metal and takes 10 turns. Are you sure you would like to buy this? ") + " ")[0]
                      toBreak = True
                      if(yn.lower() == "y"):
                          wood = wood -95
                          metal = metal - 95
                          turnAmount = 10
                          for i in range(len(tasks)):
                              if(tasks[i][2] == "Researching #!"):
                                  if(tasks[i][3] <= 1):
                                      researchBools[9] = True
                                      #here
                                  apend = False
                                  tasks[i][3] = tasks[i][3]-1
                          if(apend):
                              tasks.append([int(where[0]), int(where[1]), "Researching #!", 10])
                          break
                      elif(yn.lower() == "n"):
                          end = True
                          break
                      else:
                          print("Only write 'yes' or 'no'")
                         
                  else:
                      print("This upgrade costs 95 wood and 95 metal and takes 10 turns, you don't have enough materials. Please try again later")
                      break
              elif(whatToUpgrade == 11):
                  if(wood>= 100 and metal>= 100):
                      yn = (input("This upgrade costs 100 wood and 100 metal and takes 11 turns. Are you sure you would like to buy this? ") + " ")[0]
                      toBreak = True
                      if(yn.lower() == "y"):
                          wood = wood -100
                          metal = metal - 100
                          turnAmount = 11
                          for i in range(len(tasks)):
                              if(tasks[i][2] == "Researching #A"):
                                  if(tasks[i][3] <= 1):
                                      researchBools[10] = True
                                      #here
                                  apend = False
                                  tasks[i][3] = tasks[i][3]-1
                          if(apend):
                              tasks.append([int(where[0]), int(where[1]), "Researching #A", 11])
                          break
                      elif(yn.lower() == "n"):
                          end = True
                          break
                      else:
                          print("Only write 'yes' or 'no'")
                         
                  else:
                      print("This upgrade costs 100 wood and 100 metal and takes 11 turns, you don't have enough materials. Please try again later")
                      break
              elif(whatToUpgrade == 12):
                  if(wood>= 105 and metal>= 105):
                      yn = (input("This upgrade costs 105 wood and 105 metal and takes 12 turns. Are you sure you would like to buy this? ") + " ")[0]
                      toBreak = True
                      if(yn.lower() == "y"):
                          wood = wood -105
                          metal = metal - 105
                          turnAmount = 12
                          for i in range(len(tasks)):
                              if(tasks[i][2] == "Researching #B"):
                                  if(tasks[i][3] <= 1):
                                      researchBools[11] = True
                                      #here
                                  apend = False
                                  tasks[i][3] = tasks[i][3]-1
                          if(apend):
                              tasks.append([int(where[0]), int(where[1]), "Researching #B", 12])
                          break
                      elif(yn.lower() == "n"):
                          end = True
                          break
                      else:
                          print("Only write 'yes' or 'no'")
                         
                  else:
                      print("This upgrade costs 105 wood and 105 metal and takes 12 turns, you don't have enough materials. Please try again later")
                      break
              elif(whatToUpgrade == 13):
                  if(wood>= 110 and metal>= 110):
                      yn = (input("This upgrade costs 110 wood and 110 metal and takes 13 turns. Are you sure you would like to buy this? ") + " ")[0]
                      toBreak = True
                      if(yn.lower() == "y"):
                          wood = wood -110
                          metal = metal - 110
                          turnAmount = 13
                          for i in range(len(tasks)):
                              if(tasks[i][2] == "Researching #C"):
                                  if(tasks[i][3] <= 1):
                                      researchBools[12] = True
                                      #here
                                  apend = False
                                  tasks[i][3] = tasks[i][3]-1
                          if(apend):
                              tasks.append([int(where[0]), int(where[1]), "Researching #C", 13])
                          break
                      elif(yn.lower() == "n"):
                          end = True
                          break
                      else:
                          print("Only write 'yes' or 'no'")
                         
                  else:
                      print("This upgrade costs 110 wood and 110 metal and takes 13 turns, you don't have enough materials. Please try again later")
                      break
              else:
                  print("There is no avalible option for the entered number, please try again")
                  break
          except:
              if(whatToUpgrade.lower() == "cancel"):
                  end = True
                  toBreak = True
                  break
              elif(whatToUpgrade.lower() == "c"):
                  whatToUpgrade = 13
              elif(whatToUpgrade.lower() == "b"):
                  whatToUpgrade = 12
              elif(whatToUpgrade.lower() == "a"):
                  whatToUpgrade = 11
              elif(whatToUpgrade == "!"):
                  whatToUpgrade = 10
              else:
                  print("that was not a valid option")
                  break
      if(toBreak):
          break
  if(not end):
      whatLab = -1
      for i in range(len(researchAndFarm)):
          if(researchAndFarm[i][0] == int(where[0]) and researchAndFarm[i][1] == int(where[1]) and researchAndFarm[i][2] == "researching"):
              whatLab = i
      if(whatLab == -1):
          researchAndFarm.append([int(where[0]), int(where[1]), "researching", peoplePerLab - 1])
      else:
          researchAndFarm[whatLab][3] = researchAndFarm[whatLab][3] - 1
      people[who][1] = "busy"

def demolition():
  global materialRefundDivision
  global rowData
  global people
  global metal
  global wood
  
  end = False
    
  peepstr = "Age " + str(people[0][0]) + ", is " + str(people[0][1])
  print("You can get rid of Labs, Docks, Houses, and Fields. ")
  while(True):
      who = input("\nWho do you want to have destroy? Enter the number that the person appears in the list that says 'the people of your country:'.\nRight now if you were to enter 1 you would get " + str(peepstr) + ". Enter 'cancel' to cancel. ")
      try:
          who = int(who)-1
          if(who<len(people) and who>=0):
              if(people[who][1] == "unemployed"):
                  break
              else:
                  print("Currently that person is " + str(people[who][1]) + ". They must be unemployed to build.")
          else:
              print("Please choose a person that actually exists. ")
      except:
          if(who.lower() == "cancel"):
              end = True
              break
          else:
              print("Please enter numbers only")
    
  while(not(end)):
      where = input("\nAt what spot do you want this person to destroy? Right now 2,2 is " + str(rowData[1][avalibleToReal(2, 2)]) + ". Enter 'cancel' to cancel. ")
      if("," in where):
          where = where.split(",")
          if(type(avalibleToReal(int(where[0]), int(where[1]))) == int):
              where = str(int(where[0])-1) +","+ str(avalibleToReal(int(where[0]), int(where[1])))
              where = where.split(",")
              if((rowData[int(where[0])][int(where[1])] == "H")):
                  if(materialRefundDivision<100):
                      wood = wood + int(100/(100 - materialRefundDivision))
                  else:
                      wood = wood + 100
                  rowData[int(where[0])][int(where[1])] = "G"
                  break
              elif(rowData[int(where[0])][int(where[1])] == "L"):
                  if(materialRefundDivision<200):
                      metal = metal + int(200/(200 - materialRefundDivision))
                  else:
                      metal = metal + 200
                  rowData[int(where[0])][int(where[1])] = "G"
                  break
              elif(rowData[int(where[0])][int(where[1])] == "D"):
                  if(materialRefundDivision<150):
                      wood = wood + int(150/(150 - materialRefundDivision))
                  else:
                      wood = wood + 150
                  rowData[int(where[0])][int(where[1])] = "W"
                  break
              elif(rowData[int(where[0])][int(where[1])] == "F"):
                  if(materialRefundDivision<50):
                      wood = wood + int(50/(50 - materialRefundDivision))
                  else:
                      wood = wood + 50
                  rowData[int(where[0])][int(where[1])] = "G"
                  break
      else:
          if(where.lower() == "cancel"):
              end = True
              break
          else:
              print("Please make sure to enter two numbers separated by a comma")
  if(not end):
      people[who][1] = "busy"
      
def hiring():
  global people
  global researchBools
  peepstr = "Age " + str(people[0][0]) + ", is " + str(people[0][1])
  end = False
  
  while(True):
      who = input("\nWho do you want to hire? Enter the number that the person appears in the list that says 'the people of your country:'.\nRight now if you were to enter 1 you would get " + str(peepstr) + ". Enter 'cancel' to cancel. ")
      try:
          who = int(who)-1
          if(who<len(people) and who>=0):
              if(people[who][1] == "unemployed"):
                  break
              else:
                  print("Currently that person is " + str(people[who][1]) + ". They must be unemployed to be hired.")
          else:
              print("Please choose a person that actually exists. ")
      except:
          if(who.lower() == "cancel"):
              end = True
              break
          else:
              print("Please enter numbers only")
  while(not end):
      hireAsWhat = input("What do you want to hire this person as? (Tree worker, Mountain worker, Builder, Farmer, or Mater) ")
      if(hireAsWhat.lower() == "mountain worker" and researchBools[2]):
          people[who][1] = "mountain worker"
          break
      elif(hireAsWhat.lower() == "tree worker" and researchBools[10]):
          people[who][1] = "tree worker"
          break
      elif(hireAsWhat.lower() == "builder" and researchBools[11]):
          while(True):
              kindOfBuilder = input("What kind of builder do you want to hire? (L, F, H, or D) ")
              if(kindOfBuilder.upper() == "L"):
                  people[who][1] = "lab builder"
                  break
              elif(kindOfBuilder.upper() == "F"):
                  people[who][1] = "farm builder"
                  break
              elif(kindOfBuilder.upper() == "H"):
                  people[who][1] = "house builder"
                  break
              elif(kindOfBuilder.upper() == "D"):
                  people[who][1] = "dock builder"
                  break
              elif(kindOfBuilder.lower() == "cancel"):
                  end = True
                  break
              else:
                  print("You can't hire that kind of builder")
          break
      elif(hireAsWhat.lower() == "farmer" and researchBools[9]):
          people[who][1] = "farmer"
          break
      elif(hireAsWhat.lower() == "mater" and researchBools[12]):
          people[who][1] = "mater"
          break
      elif(hireAsWhat.lower() == "cancel"):
          end = True
          break
      else:
          print("Either you still have to research that hiring ability or you choose an option that doesn't exist.")
          

def doJobs():
  global tasks
  global people
  global researchAndFarm
  global metal
  global wood
  global food
  global metalIncreaseAmount
  global woodIncreaseAmount
  global rowData
  global peoplePerFarm
  num = 0
  
  for i in range(len(people)):
      if(people[i][1] == "mountain worker"):
          num = 1
          for a in range(len(tasks)):
              if(tasks[i][2] == "mountain"):
                  num = 0
                  metal = metal + metalIncreaseAmount
                  rowData[tasks[i][0]][tasks[i][1]] = "G"
                  tasks.pop(i)
          if(num == 1):
              for a in range(len(rowData)):
                  for b in range(len(rowData[a])):
                      if(rowData[a][b] == "M"):
                          num = 0
                          tasks.append([a, b, "mountain", 1])
                          break
                  if(num == 0):
                      break
      elif(people[i][1] == "tree worker"):
          num = 1
          for a in range(len(rowData)):
              for b in range(len(rowData[a])):
                  if(rowData[a][b] == "T"):
                      num = 0
                      wood = wood + woodIncreaseAmount
                      rowData[a][b] = "G"
                      break
              if(num == 0):
                  break
      elif(people[i][1] == "farmer"):
          num = 1
          for a in range(len(rowData)):
              for b in range(len(rowData[a])):
                  for c in range(len(researchAndFarm)):
                      if(researchAndFarm[c][3] != 0 and researchAndFarm[c][0] == a and researchAndFarm[c][1] == b and rowData[a][b] == "F"):
                          food = food + 5
                          num = 0
                          researchAndFarm[c][3] = researchAndFarm[c][3] - 1
                          break
                  if(num == 0):
                      break
                  if(rowData[a][b] == "F"):
                      food = food + 5
                      num = 0
                      researchAndFarm.append([a, b, "farming", peoplePerFarm-1])
              if(num == 0):
                  break
      elif(people[i][1] == "mater"):
          num = 1
          
          for a in range(len(rowData)):
              for b in range(len(rowData[a])):
                  if((not isTaskInProgress(a, b)) and rowData[a][b] == "H"):
                      num = 0
                      tasks.append([a, b, "new life", 2])
                      break
              if(num == 0):
                  break
      elif(people[i][1] == "lab builder"):
          num = 0 
          for a in range(len(rowData)):
              for b in range(len(rowData[a])):
                  if(isTaskInProgress(a, b)):
                      for c in range(len(tasks)):
                          if(tasks[c][2] == "building lab"):
                              tasks[c][3] = tasks[c][3] - 1
                              metal = metal - 200
                              num = 1
                              if(tasks[c][3]<=0):
                                  rowData[a][b] = "L"
                              break
                      break
                  if(num == 1):
                      break
                  if(rowData[a][b] == "G" and metal>=200):
                      num = 1
                      metal = metal - 200
                      tasks.append([a, b, "building lab", 20])
                      break
              if(num == 1):
                  break
      elif(people[i][1] == "farm builder"):
          num = 0 
          for a in range(len(rowData)):
              for b in range(len(rowData[a])):
                  
                  if(isTaskInProgress(a, b)):
                      for c in range(len(tasks)):
                          if(tasks[c][2] == "building fields"):
                              tasks[c][3] = tasks[c][3] - 1
                              num = 1
                              if(tasks[c][3]<=0):
                                  rowData[a][b] = "F"
                              break
                      break
                  if(num == 1):
                      break
                  
                  if(rowData[a][b] == "G" and wood>=50 and num != 1):
                      num = 1
                      wood = wood - 50
                      tasks.append([a, b, "building fields", 3])
                      break
              if(num == 1):
                  break
      elif(people[i][1] == "dock builder"):
          num = 0 
          for a in range(len(rowData)):
              for b in range(len(rowData[a])):
                  if(isTaskInProgress(a, b)):
                      for c in range(len(tasks)):
                          if(tasks[c][2] == "building docks"):
                              tasks[c][3] = tasks[c][3] - 1
                              num = 1
                              if(tasks[c][3]<=0):
                                  rowData[a][b] = "D"
                              break
                      break
                  if(num == 1):
                      break
                  if(rowData[a][b] == "G" and wood>=150 and num != 1):
                      num = 1
                      wood = wood - 150
                      tasks.append([a, b, "building docks", 3])
                      break
              if(num == 1):
                  break
      elif(people[i][1] == "house builder"):
          num = 0 
          for a in range(len(rowData)):
              for b in range(len(rowData[a])):
                  if(isTaskInProgress(a, b)):
                      for c in range(len(tasks)):
                          if(tasks[c][2] == "building house"):
                              tasks[c][3] = tasks[c][3] - 1
                              num = 1
                              if(tasks[c][3]<=0):
                                  rowData[a][b] = "H"
                              break
                      break
                  if(num == 1):
                      break
                  if(rowData[a][b] == "G" and wood>=100 and num != 1):
                      num = 1
                      wood = wood - 100
                      tasks.append([a, b, "building house", 3])
                      break
              if(num == 1):
                  break

def firing():
  global people
  
  peepstr = "Age " + str(people[0][0]) + ", is " + str(people[0][1])
  end = False
  
  while(True):
      who = input("\nWho do you want to hire? Enter the number that the person appears in the list that says 'the people of your country:'.\nRight now if you were to enter 1 you would get " + str(peepstr) + ". Enter 'cancel' to cancel. ")
      try:
          who = int(who)-1
          if(who<len(people) and who>=0):
              if(people[who][1] != "busy" and people[who][1] != "pregnant"):
                  break
              else:
                  print("Currently that person is " + str(people[who][1]) + ". They must be unemployed to be hired.")
          else:
              print("Please choose a person that actually exists. ")
      except:
          if(who.lower() == "cancel"):
              end = True
              break
          else:
              print("Please enter numbers only")
  if(not end):
      people[who][1] = "unemployed"

def loadData():
    global data
    global rowData
    global people
    global food
    global name
    global tasks
    global wood
    global metal
    global woodIncreaseAmount
    global metalIncreaseAmount
    global maxAge
    global peoplePerFarm
    global researchBools
    global peoplePerLab
    global treeRespawnChance
    global chanceOfTwins
    global materialRefundDivision
    rtof = False
    
    try:
        with open("townGameData.json", "r") as f:
            if(input("It seems like you have played before, would you like to continue? Saying no will delete the old save file ") != "no"):
                data = json.load(f)
                rtof = True
            else:
                rtof = False
    except:
        rtof = False
        
    rowData = data["rowData"]
    people = data["people"]
    food = data["food"]
    name = data["name"]
    tasks = data["tasks"]
    wood = data["wood"]
    metal = data["metal"]
    woodIncreaseAmount = data["woodIncreaseAmount"]
    metalIncreaseAmount = data["metalIncreaseAmount"]
    maxAge = data["maxAge"]
    peoplePerFarm = data["peoplePerFarm"]
    researchBools = data["researchBools"]
    peoplePerLab = data["peoplePerLab"]
    treeRespawnChance = data["treeRespawnChance"]
    chanceOfTwins = data["chanceOfTwins"]
    materialRefundDivision = data["materialRefundDivision"]
    return rtof
    
def saveData():
    global data
    global name
    global wood
    global food
    data["food"] = food
    data["wood"] = wood
    data["name"] = name
    
    with open("townGameData.json", "w") as f:
        json.dump(data, f)

main()
