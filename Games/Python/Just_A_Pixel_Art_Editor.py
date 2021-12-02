#Formatted for https://www.onlinegdb.com/ with output screen up all the way, for chromebooks press search key+9 to run.
#~~~~~Pixel art editor~~~~~#
#version 1.0

import tty, sys, termios, threading, time

#returns all points between two points in a rectangle
#points must be in this format [x, y], [x, y].
def between(pointA, pointB):
    #starts array so points can be added to it
    betweens = []
    #gets the size of the rectangle so it can loop through a range of it later
    #uses if statement so the points can be in order of either 
    #([higher, lower], [lower, higher]), ([higher, higher], [lower, lower]), ([lower, lower] , [higher, higher]), or ([lower, higher], [higher, lower])
    if(pointA[1]>pointB[1]):
        Ysize = pointA[1]-pointB[1]+1
    else:
        Ysize = pointB[1]-pointA[1]+1
    
    if(pointA[0]>pointB[0]):
        Xsize = pointA[0]-pointB[0]+1
    else:
        Xsize = pointB[0]-pointA[0]+1
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #loops through ysize and xsize to add to the betweens array
    for y in range(Ysize):
        for x in range(Xsize):
            #again makes it so the points can be in either order
            if(pointA[0]>pointB[0]):
                if(pointA[1]>pointB[1]):
                    betweens.append([pointB[0]+x, pointB[1]+y])
                else:
                    betweens.append([pointB[0]+x, pointA[1]+y])
            else:
                if(pointA[1]>pointB[1]):
                    betweens.append([pointA[0]+x, pointB[1]+y])
                else:
                    betweens.append([pointA[0]+x, pointA[1]+y])
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    return betweens

#this makes the keys run simultaneously to the rest of the engine
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
    #we do not disclude here
    gray='\033[40m'
    grey='\033[40m'
    #~~~~~~~~~~~~~~~~~~~~~~~
    red='\033[41m'
    green='\033[42m'
    yellow='\033[43m'
    blue='\033[44m'
    purple='\033[45m'
    cyan='\033[46m' 
    white='\033[47m'
    black="\u001b[0m"
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#changes cursor location using escape code
def goto_xy(x, y):
    print("\033["+ str(y) +";" + str(x)+"f", end="")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   
#Makes an area clickable, really just a button
class clickable:
    #makes it so you can loop through all clickable objects
    allAreas = []
    def __init__(self, pointA, pointB, condition, func, *args):
        #pointA and pointB decide the size/location of the clickable area. condition tells it if it is active or not
        #func is the function that is run when the area is clicked. args is the arguments that are used for each function
        self.args = args
        self.area = []
        self.func = func
        self.area = between(pointA, pointB)
        self.condition = condition
        #adds the object to the allAreas variable
        clickable.allAreas.append(self)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    

#is a graphics like object
class rect:
    def __init__(self, xs, ys, posx, posy, color):
        #xs is horrizontal size, ys is vertical size, posx is horrizontal position, posy is vertical position
        #color is well, color
        self.xs = xs
        self.ys = ys
        self.color = color
        self.posy = posy
        self.posx = posx
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~

class text:
    #string is the text to add to the screen, posx is the horrizontal position, posy is the vertical position
    def __init__(self, string, posx, posy):
        #self.string is a lot of things, it is a 2d array of chars and chars' locations 
        #"abc": [[a, 0],[b, 1],[c, 2]]
        self.string = []
        for i in range(len(string)):
            self.string.append([string[i], i])
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.posx = posx
        self.posy = posy
        
#returns a 3D array of the screen based off of the rectang and text objects
def setScreen(rectangs = [], texts = []):
    #screen is [0]: colors, and [1], text. defaults " " and color.black
    screen = [[],[]]
    
    
    #~~~~~~~~~~~~~~~~~~
    #size the array to fit the screen
    for a in range(32):
        screen[0].append([])
        for b in range(144):
            screen[0][a].append(color.black)
    for a in range(32):
        screen[1].append([])
        for b in range(144):
            screen[1][a].append(" ")
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #sets up colors
    for obj in rectangs:
        for line in range(obj.ys):
            for char in range(obj.xs):
                screen[0][line+obj.posy][char+obj.posx] = obj.color
    #~~~~~~~~~~~~~~
    #sets up text
    for text in texts:
        for char in text.string:
            screen[1][text.posy][text.posx+char[1]] = char[0]
    #~~~~~~~~~~~~
    return screen
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#same as setscreen but keeps everything you don't overlap.
def changeScreen(screen, rectangs = [], texts = [], destroyers = []):
    #sets up destroyers
    for destroyer in destroyers:
        for line in range(destroyer.ys):
            for char in range(destroyer.xs):
                screen[0][line+destroyer.posy][char+destroyer.posx] = color.black
                screen[1][line+destroyer.posy][char+destroyer.posx] = " "
    #~~~~~~~~~~~~~~~~~~
    #sets up retangles
    for obj in rectangs:
        for line in range(obj.ys):
            for char in range(obj.xs):
                screen[0][line+obj.posy][char+obj.posx] = obj.color
    #~~~~~~~~~~~~~~~~~
    #sets up text
    for text in texts:
        for char in text.string:
            screen[1][text.posy][text.posx+char[1]] = char[0]
    #~~~~~~~~~~~~
    return screen
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#reprints screen but only where oldScreen does not equal newScreen
#if everything was updated, the cursor would not have time to update the bottom half of the screen, only the top
def updateScreen(oldScreen, newScreen):
    #loops through 2d array
    if(oldScreen!=newScreen):
        for y in range(32):
            if(oldScreen[0][y]!=newScreen[0][y] or oldScreen[1][y]!=newScreen[1][y]):
                for x in range(144):
                    #checks if newScreen at certain location is equal to oldScreen at the same location,
                    #if nothing has changed, update, else do nothing
                    if(newScreen[0][y][x] != oldScreen[0][y][x] or newScreen[1][y][x] != oldScreen[1][y][x]):
                        #cursor goes to the position where newScreen doesn't equal oldScreen
                        goto_xy(x+1,y+1)
                        #prints the color at that location with the characters at that location
                        print(newScreen[0][y][x]+newScreen[1][y][x], end = "")
                        #makes oldScreen equal to newScreen so it doesn't want to "over update"
                        main.oldScreen[0][y][x] = newScreen[0][y][x]
                        main.oldScreen[1][y][x] = newScreen[1][y][x]
    #~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#because we use keyboard input and it messed up something, we can't use the input function
#for this reason, we made this class.
class inputField:
    #same with buttons we save the objects
    allAreas = []
    def __init__(self, condition, posx, posy, size, towhat):
        #condition is if the input field is active, posx is the horrizontal location, posy is vertical location
        #size is the horrizontal size, the vertical size is always 1, towhat is what variable gets set to the input
        self.size = size
        self.posx = posx
        self.posy = posy
        self.area = between([posx, posy], [posx+size, posy])
        self.condition = condition
        self.towhat = towhat
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #self.inputted is to track what is currently being inputted into the input field
        self.inputted = ""
        #this adds the object to the allAreas variable.
        inputField.allAreas.append(self)
    
    #runs when clicked
    def beingUsed(self):
        #inputField changes color when clicked, for this reason, we save the colors underneath it
        underneathField = []
        print(color.white)
        for i in range(self.size):
            underneathField.append(main.screen[0][self.posy][self.posx+i])
            goto_xy(self.posx+i+1, self.posy+1)
            print(" ")
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #controls should stop working when using input field, so we make a loop
        while(1):
            #returns controls to normal after arrow keys or enter is pressed
            if(keycode.keydown("upAr") or keycode.keydown("downAr") or keycode.keydown("leftAr") or keycode.keydown("rightAr")):
                print(color.black)
                main.screen = changeScreen(main.screen, [rect(self.size, 1, self.posx, self.posy, color.black)], [])
                break
            if(keycode.keydown("enter")):
                print(color.black)
                main.screen = changeScreen(main.screen, [rect(self.size, 1, self.posx, self.posy, color.black)], [])
                #makes towhat into the inputted value, uses exec because there are no pointers in python
                #at least not that I know of
                exec(self.towhat+"=self.inputted")
                break
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            if(keycode.key == "backspace"):
                #if there is more inputted than the size of the input field, everything moves forward 1 when backspace is pressed 
                if(len(self.inputted)>=self.size):
                    #removes 1 character from inputted variable
                    #inputtedHelper is just a variable that makes it so things aren't 
                    #completely changed when you loop through the inputted variable
                    inputtedHelper = ""
                    for i in range(len(self.inputted)-1):
                        inputtedHelper = inputtedHelper+self.inputted[i]
                    self.inputted = inputtedHelper
                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    #Only so many characters are shown, we save that to a variable, but to save it there we have to only
                    #find the last so many couple characters. to do this we work backwards on the sring, but backwards is
                    #not right so we loop through to fix it. opShows is backwards, shows is normal
                    opShows = ""
                    for i in range(self.size):
                        opShows = opShows+self.inputted[len(self.inputted)-i-1]
                    shows = ""
                    for i in range(len(shows)):
                        shows = shows+opShows[self.size-i-1]
                        goto_xy(self.posx+i+1, self.posy+1)
                        print(shows[i])
                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                else:
                    shows = ""
                    inputtedHelper = ""
                    #removes 1 character from inputted variable
                    for i in range(len(self.inputted)-1):
                        inputtedHelper = inputtedHelper+self.inputted[i]
                    self.inputted = inputtedHelper
                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    #shows isn't flipped so it is directly equal to self.inputted
                    shows = self.inputted
                #this clears the input field so the deleted character can update
                closeShow = " "
                for i in range(self.size):
                    closeShow = closeShow + " "
                    goto_xy(self.posx+i+1, self.posy+1)
                    print(" ")
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                for i in range(len(shows)):
                    goto_xy(self.posx+i+1, self.posy+1)
                    print(shows[i])
                keycode.key = ""
                
            elif(keycode.key!=""):
                #inputted gets larger as you input more keys
                self.inputted = self.inputted+keycode.key
                #if theres more inputted than can fit in the box, the last keys show up but not the rest
                if(len(self.inputted)>=self.size):
                    #again it gets the last keys and has to flip
                    opShows = ""
                    for i in range(self.size):
                        opShows = opShows+self.inputted[len(self.inputted)-i-1]
                    shows = ""
                    for i in range(self.size):
                        shows = shows+opShows[self.size-i-1]
                        goto_xy(self.posx+i+1, self.posy+1)
                        print(shows[i])
                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                else:
                    #if its a normal size then it should directly equal the stuff inputted
                    shows = self.inputted
                    for i in range(len(self.inputted)):
                        goto_xy(self.posx+i+1, self.posy+1)
                        print(shows[i])
                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                #adds last size characters of inputted string to input field.
                main.screen = changeScreen(main.screen, [], [text(shows, self.posx, self.posy)])
                keycode.key = ""
            #because we are in a loop, we must still update the screen, although I don't understand why oldscreen
            #doen't need to be updated to reprint it. 
            #updateScreen(main.oldScreen, main.screen)
        #when we are done with the inputting we restore the fields previous colors
        for i in range(self.size):
            main.screen[0][self.posy][self.posx+i] = underneathField[i]
        for i in range(self.size):
            goto_xy(self.posx+i+1, self.posy+1)
            print(main.screen[0][self.posy][self.posx+i]+" ")
        updateScreen(main.oldScreen, main.screen)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~~~~~~~~~~~~~~~
          
#fits with destroyer in the setScreen and changeScreen. its a rectangle that effects text as well as color
#it only changes them to black and empty though
class emptyArea:
    #same arguments as rect but without the color.
    def __init__(self, xs, ys, posx, posy):
        self.xs = xs
        self.ys = ys
        self.posx = posx
        self.posy = posy

def newImage(args):
    #deactivates the new Image and old image button until red button is pressed
    main.newImageButton.condition = False
    main.oldImageButton.condition = False
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    #sets up the screen so it includes the new box
    main.screen = changeScreen(main.screen, destroyers = [emptyArea(9, 7, main.cursor.posx-1, main.cursor.posy-1)])
    main.screen = changeScreen(main.screen, [rect(9,9, main.cursor.posx-1, main.cursor.posy-1, color.black), rect(7,7, main.cursor.posx, main.cursor.posy, color.grey), \
        rect(4,1, main.cursor.posx+2, main.cursor.posy+1, color.black), rect(4,1, main.cursor.posx+2, main.cursor.posy+3, color.black), \
        rect(1,1, main.cursor.posx+2, main.cursor.posy+5, color.red), rect(1,1, main.cursor.posx+5, main.cursor.posy+5, color.green)],\
        [text("X", main.cursor.posx+1, main.cursor.posy+1), text("Y", main.cursor.posx+1, main.cursor.posy+3)])
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    #repositions input fields and activates them
    main.newImageXInputField.posx = main.cursor.posx+2
    main.newImageXInputField.posy = main.cursor.posy+1
    main.newImageXInputField.condition = True
    main.newImageXInputField.area = between([main.newImageXInputField.posx, main.newImageXInputField.posy], [main.newImageXInputField.posx+main.newImageXInputField.size, main.newImageXInputField.posy])
    main.newImageYInputField.posx = main.cursor.posx+2
    main.newImageYInputField.posy = main.cursor.posy+3
    main.newImageYInputField.condition = True
    main.newImageYInputField.area = between([main.newImageYInputField.posx, main.newImageYInputField.posy], [main.newImageYInputField.posx+main.newImageYInputField.size, main.newImageYInputField.posy])
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #repositions and activates green and red buttons
    main.newImageCancelButton.area = [[main.cursor.posx+2, main.cursor.posy+5]]
    main.newImageContinueButton.area = [[main.cursor.posx+5, main.cursor.posy+5]]
    main.newImageCancelButton.condition = True
    main.newImageContinueButton.condition = True
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
#activates when oldImageButton is pressed
def oldImage(args):
    #deactivates old and new image button
    main.newImageButton.condition = False
    main.oldImageButton.condition = False
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    main.screen = changeScreen(main.screen, [rect(7,7, main.cursor.posx, main.cursor.posy, color.grey), rect(5, 1, main.cursor.posx+1, main.cursor.posy+3, color.black),\
        rect(1, 1, main.cursor.posx+1, main.cursor.posy+5, color.red), rect(1, 1, main.cursor.posx+5, main.cursor.posy+5, color.green)],\
        destroyers = [emptyArea(9,9, main.cursor.posx-1, main.cursor.posy-1)], texts = [text("What", main.cursor.posx+1, main.cursor.posy+1), text("File?", main.cursor.posx+1, main.cursor.posy+2)])
    #repositions and activates input field
    main.oldImageInputField.condition = True
    main.oldImageInputField.posy = main.cursor.posy+3
    main.oldImageInputField.posx = main.cursor.posx+1
    main.oldImageInputField.area = between([main.oldImageInputField.posx, main.oldImageInputField.posy], [main.oldImageInputField.posx+main.oldImageInputField.size, main.oldImageInputField.posy])
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #repositions and activates green and red continue/cancel buttons
    main.oldImageContinueButton.condition = True
    main.oldImageContinueButton.area = [[main.cursor.posx+5, main.cursor.posy+5]]
    main.oldImageCancelButton.condition = True
    main.oldImageCancelButton.area = [[main.cursor.posx+1, main.cursor.posy+5]]
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#green and red buttons that show up after pressing newImageButton or oldImageButton
def continueNewImage(args):
    #gets rid of the spot under the cursor
    main.underCurs = color.black
    #deactivates cancel and continue buttons
    main.newImageCancelButton.condition = False
    main.newImageContinueButton.condition = False
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #activates the save image button
    changeScreen(main.screen, destroyers = [emptyArea(10, 1, 97, 0)], rectangs = [rect(10, 2, 97, 0, color.grey)], texts = [text("save", 100, 1)])
    main.saveImageButton.condition = True
    #tells the main that you are making an image
    main.paintingImageCondition = True
    #someone could enter anything into the input field, for this reason we 
    #fix X and Y current image sizes
    try:
        if(int(main.currentImageYS)<=0):
            main.currentImageYS = 26
        elif(int(main.currentImageYS)>26):
            main.currentImageYS = 26
        else:
            main.currentImageYS = int(main.currentImageYS)
    except:
        main.currentImageYS = 26
    try:
        if(int(main.currentImageXS)<=0):
            main.currentImageXS = 131
        elif(int(main.currentImageXS)>131):
            main.currentImageXS = 131
        else:
            main.currentImageXS = int(main.currentImageXS)
    except:
        main.currentImageXS = 131
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #sizes array to fit image sizes
    for y in range(main.currentImageYS):
        main.currentImageColors.append([])
        for x in range(main.currentImageXS):
            main.currentImageColors[y].append(color.black)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #changes the screen to erase new/old image buttons as well as add image grid
    main.screen = changeScreen(main.screen, destroyers = [emptyArea(133, 28, 11,4)], rectangs = [rect(main.currentImageXS+2, main.currentImageYS+2, 11, 4, color.gray), rect(main.currentImageXS, main.currentImageYS, 12, 5, color.black)])
    #activates all color chooser buttons
    main.colorButtonGreen.condition = True
    main.colorButtonRed.condition = True
    main.colorButtonPurple.condition = True
    main.colorButtonYellow.condition = True
    main.colorButtonCyan.condition = True
    main.colorButtonBlue.condition = True
    main.colorButtonBlack.condition = True
    main.colorButtonWhite.condition = True
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    
def cancelNewImage(args):
    #gets rid of the spot under the cursor
    main.underCurs = color.black
    #deactivates cancel and continue buttons
    main.newImageCancelButton.condition = False
    main.newImageContinueButton.condition = False
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #activates the new Image and old image button
    main.newImageButton.condition = True
    main.oldImageButton.condition = True 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #gets rid of the box and readds the newImageButton to the screen
    main.screen = changeScreen(main.screen, [rect(11, 5, 34, 15, color.grey)], [text("new image", 35, 17)], [emptyArea(18, 15, 33, 14)])
    

def continueOldImage(args):
    #gets rid of the spot under the cursor
    main.underCurs = color.black
    #deactivates cancel and continue buttons
    main.oldImageCancelButton.condition = False
    main.oldImageContinueButton.condition = False
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #activates the save image button
    changeScreen(main.screen, destroyers = [emptyArea(10, 1, 97, 0)], rectangs = [rect(10, 2, 97, 0, color.grey)], texts = [text("save", 100, 1)])
    main.saveImageButton.condition = True
    #tells the main that you are making an image
    main.paintingImageCondition = True
    #sets current image sizes to saved image sizes
    oldImageData = []
    with open(main.oldImageFile, "r") as f:
        oldImageData = [line for line in f.readlines()]
    exec("main.currentImageColors = " + oldImageData[0])
    main.currentImageXS = int(oldImageData[1])
    main.currentImageYS = int(oldImageData[2])
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #changes the screen to erase new/old image buttons as well as add image grid
    main.screen = changeScreen(main.screen, destroyers = [emptyArea(133, 28, 11,4)], rectangs = [rect(main.currentImageXS+2, main.currentImageYS+2, 11, 4, color.gray), rect(main.currentImageXS, main.currentImageYS, 12, 5, color.black)])
    #activates all color chooser buttons
    main.colorButtonGreen.condition = True
    main.colorButtonRed.condition = True
    main.colorButtonPurple.condition = True
    main.colorButtonYellow.condition = True
    main.colorButtonCyan.condition = True
    main.colorButtonBlue.condition = True
    main.colorButtonBlack.condition = True
    main.colorButtonWhite.condition = True
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
def cancelOldImage(args):
    #gets rid of the spot under the cursor
    main.underCurs = color.black
    #deactivates cancel and continue buttons
    main.oldImageCancelButton.condition = False
    main.oldImageContinueButton.condition = False
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #activates the new Image and old image button
    main.newImageButton.condition = True
    main.oldImageButton.condition = True 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #gets rid of the box and readds the oldImageButton to the screen
    main.screen = changeScreen(main.screen, [rect(11, 5, 94, 15, color.grey)], [text("old image", 95, 17)], [emptyArea(18, 17, 93, 14)])
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#sets the color you are currently painting with
def setPaintColor(args):
    col = args[0]
    main.currentPaintColor = col
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""some vocab for some reason
cursor is like the mouse but you can't use the mouse only the keyboard 
the "graphic" objects are all creator only objects just used to speed up the prosess of designing the screen
sentences are like gameobjects in unity
words are elements for the sentences, like a script that controls the sentence
characters are like the variables that go on the script word

"""
"""lots to do...
    set up sentence objects (game objects but because text baced we are cooler)
    *set up script editor
    animator
    files
    putting all aspects into one script (finishing game)
    main screen setup

probably more but I can't think of anything.

"""

def save(args):
    main.underCurs = color.black
    main.saveImageButton.condition = False
    main.screen = changeScreen(main.screen, destroyers = [emptyArea(4, 1, 100, 1)], texts = [text("What File?", 97, 0)])
    updateScreen(main.oldScreen, main.screen)
    main.saveImageToInputField.condition = True
    
def reset(args):
    #deletes all button areas
    clickable.allAreas = []
    #does main before main loop
    main.underCurs = color.grey
    count = 0
    main.cursor = rect(1,1, 0,0, color.white)
    main.newImageButton = clickable([34, 15], [45, 20], True, newImage)
    main.oldImageButton = clickable([94, 15], [105, 20], True, oldImage)
    main.newImageContinueButton = clickable([0, 0], [0, 0], False, continueNewImage)
    main.newImageCancelButton = clickable([0, 0], [0, 0], False, cancelNewImage)
    main.oldImageContinueButton = clickable([0, 0], [0, 0], False, continueOldImage)
    main.oldImageCancelButton = clickable([0, 0], [0, 0], False, cancelOldImage)
    main.colorButtonGreen = clickable([1, 9], [9, 11], False, setPaintColor, color.green)
    main.colorButtonRed = clickable([1, 6], [9, 8], False, setPaintColor, color.red)
    main.colorButtonBlue = clickable([1, 12], [9, 14], False, setPaintColor, color.blue)
    main.colorButtonYellow = clickable([1, 15], [9, 17], False, setPaintColor, color.yellow)
    main.colorButtonPurple = clickable([1, 21], [9, 23], False, setPaintColor, color.purple)
    main.colorButtonCyan = clickable([1, 18], [9, 20], False, setPaintColor, color.cyan)
    main.colorButtonBlack = clickable([1, 24], [9, 26], False, setPaintColor, color.black)
    main.colorButtonWhite = clickable([1, 27], [9, 29], False, setPaintColor, color.white)
    main.newImageXInputField = inputField(False, 0, 0, 4, "main.currentImageXS")
    main.newImageYInputField = inputField(False, 0, 0, 4, "main.currentImageYS")
    main.oldImageInputField = inputField(False, 0, 0, 4, "main.oldImageFile")
    main.oldImageFile = ""
    main.saveImageButton = clickable([100, 1], [104, 1], False, save)
    main.saveImageToInputField = inputField(False, 100, 1, 4, "main.saveImageTo")
    main.saveImageTo = ""
    main.reset = clickable([50, 1], [55, 1], True, reset)
    main.currentImageXS = 0
    main.currentImageYS = 0
    main.paintingImageCondition = False
    main.currentPaintColor = color.black
    main.currentImageColors = []
    print(color.black+"\u001b[2J")
    main.oldScreen = setScreen([], [])
    main.screen = setScreen([rect(144, 3, 0, 0, color.grey), rect(13, 1, 29, 1, color.black), rect(10, 28, 0, 4, color.grey), rect(133, 28, 11, 4, color.grey), rect(131, 26, 12, 5, color.black), \
        rect(11, 5, 34, 15, color.grey), rect(11, 5, 94, 15, color.grey), \
        rect(8, 2, 1, 6, color.red), rect(8, 2, 1, 9, color.green), rect(8, 2, 1, 12, color.blue), rect(8, 2, 1, 15, color.yellow), rect(8, 2, 1, 18, color.cyan), rect(8, 2, 1, 21, color.purple), rect(8, 2, 1, 24, color.black), rect(8, 2, 1, 27, color.white)], \
        [text("sprite editor", 29, 1), text("reset", 50, 1), text("new image", 35, 17), text("old image", 95, 17)])
    updateScreen(main.oldScreen, main.screen)
    main.oldScreen = setScreen([], [])
    goto_xy(1,1)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~



#the size of the screen is 32 lines, 144 characters

class main:
    def main():
        #cursor blinks, this is the color under the cursor
        main.underCurs = color.grey
        #count has to do with blinking
        count = 0
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #makes a rectangle that represents the cursor
        main.cursor = rect(1,1, 0,0, color.white)
        #~~~~~~~~~~~~~~~~~~~~~~~~
        #sprite editor buttons
        main.newImageButton = clickable([34, 15], [45, 20], True, newImage)
        main.oldImageButton = clickable([94, 15], [105, 20], True, oldImage)
        #buttons that show up after clicking new or old image
        main.newImageContinueButton = clickable([0, 0], [0, 0], False, continueNewImage)
        main.newImageCancelButton = clickable([0, 0], [0, 0], False, cancelNewImage)
        main.oldImageContinueButton = clickable([0, 0], [0, 0], False, continueOldImage)
        main.oldImageCancelButton = clickable([0, 0], [0, 0], False, cancelOldImage)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #buttons that choose the color
        main.colorButtonGreen = clickable([1, 9], [9, 11], False, setPaintColor, color.green)
        main.colorButtonRed = clickable([1, 6], [9, 8], False, setPaintColor, color.red)
        main.colorButtonBlue = clickable([1, 12], [9, 14], False, setPaintColor, color.blue)
        main.colorButtonYellow = clickable([1, 15], [9, 17], False, setPaintColor, color.yellow)
        main.colorButtonPurple = clickable([1, 21], [9, 23], False, setPaintColor, color.purple)
        main.colorButtonCyan = clickable([1, 18], [9, 20], False, setPaintColor, color.cyan)
        main.colorButtonBlack = clickable([1, 24], [9, 26], False, setPaintColor, color.black)
        main.colorButtonWhite = clickable([1, 27], [9, 29], False, setPaintColor, color.white)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #~~~~~~~~~~~~~~~~~~~~~
        #sprite editor new image input fields
        main.newImageXInputField = inputField(False, 0, 0, 4, "main.currentImageXS")
        main.newImageYInputField = inputField(False, 0, 0, 4, "main.currentImageYS")
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #sprite editor old image file vars
        main.oldImageInputField = inputField(False, 0, 0, 4, "main.oldImageFile")
        main.oldImageFile = ""
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #sprite editor save image vars
        main.saveImageButton = clickable([100, 1], [104, 1], False, save)
        main.saveImageToInputField = inputField(False, 100, 1, 4, "main.saveImageTo")
        main.saveImageTo = ""
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #this button lets you restart
        main.reset = clickable([50, 1], [55, 1], True, reset)
        #sprite editor other variables
        #the size of the image you are working on
        main.currentImageXS = 0
        main.currentImageYS = 0
        main.paintingImageCondition = False
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #the color you are currently using
        main.currentPaintColor = color.black
        #an array of the image you are currently working on
        main.currentImageColors = []
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        #sets old and new screen then prints newScreen
        main.oldScreen = setScreen([], [])
        main.screen = setScreen([rect(144, 3, 0, 0, color.grey), rect(13, 1, 29, 1, color.black), rect(10, 28, 0, 4, color.grey), rect(133, 28, 11, 4, color.grey), rect(131, 26, 12, 5, color.black), \
            rect(11, 5, 34, 15, color.grey), rect(11, 5, 94, 15, color.grey), \
            rect(8, 2, 1, 6, color.red), rect(8, 2, 1, 9, color.green), rect(8, 2, 1, 12, color.blue), rect(8, 2, 1, 15, color.yellow), rect(8, 2, 1, 18, color.cyan), rect(8, 2, 1, 21, color.purple), rect(8, 2, 1, 24, color.black), rect(8, 2, 1, 27, color.white)], \
            [text("sprite editor", 29, 1), text("reset", 50, 1), text("new image", 35, 17), text("old image", 95, 17)])
        updateScreen(main.oldScreen, main.screen)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #sets the cursor location so the screen doesn't expand
        goto_xy(1,1)
        #threads in keys so they run simultaneously
        thread1 = myThread()
        thread1.start()
        #~~~~~~~~~~~~~~~
        
        while(True):
            #hide default cursor
            print("\x1b[?25l", end = "")
            
            #cursor movements
            if(keycode.keydown("leftAr") and main.cursor.posx>0):
                main.screen[0][main.cursor.posy][main.cursor.posx] = main.underCurs
                main.cursor.posx = main.cursor.posx-1
                main.underCurs = main.screen[0][main.cursor.posy][main.cursor.posx]
            if(keycode.keydown("rightAr") and main.cursor.posx<143):
                main.screen[0][main.cursor.posy][main.cursor.posx] = main.underCurs
                main.cursor.posx = main.cursor.posx+1
                main.underCurs = main.screen[0][main.cursor.posy][main.cursor.posx]
            if(keycode.keydown("upAr") and main.cursor.posy>0):
                main.screen[0][main.cursor.posy][main.cursor.posx] = main.underCurs
                main.cursor.posy = main.cursor.posy-1
                main.underCurs = main.screen[0][main.cursor.posy][main.cursor.posx]
            if(keycode.keydown("downAr") and main.cursor.posy<31):
                main.screen[0][main.cursor.posy][main.cursor.posx] = main.underCurs
                main.cursor.posy = main.cursor.posy+1
                main.underCurs = main.screen[0][main.cursor.posy][main.cursor.posx]
            #~~~~~~~~~~~~~~~~
            #no click so instad we use space
            if(keycode.keydown(" ")):
                #looks through all clickable areas and runs their func when space is pressed
                for area in clickable.allAreas:
                    if([main.cursor.posx, main.cursor.posy] in area.area):
                        if(area.condition):
                            area.func(area.args)
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                #looks through all input fields and sets their variable to what is inputted when space is pressed
                for area in inputField.allAreas:
                    if([main.cursor.posx, main.cursor.posy] in area.area and area.condition):
                        area.beingUsed()
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                #checks to see if we are currently painting an image
                if(main.paintingImageCondition):
                    if([main.cursor.posx, main.cursor.posy] in between([12,5], [11+main.currentImageXS, 4+main.currentImageYS])):
                        main.currentImageColors[main.cursor.posy-5][main.cursor.posx-12] = main.currentPaintColor
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            #shows the image you are currently painting
            if(main.paintingImageCondition):
                for y in range(main.currentImageYS):
                    for x in range(main.currentImageXS):
                        main.screen[0][y+5][x+12] = main.currentImageColors[y][x]
                
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            #saves the image you painted and adds it to metadataFile
            if(main.saveImageTo !=""):
                with open(main.saveImageTo, "w") as f:
                    f.write(str(main.currentImageColors)+"\n"+str(main.currentImageXS)+"\n"+str(main.currentImageYS))
                main.saveImageTo = ""
                main.saveImageToInputField.inputted = ""
                main.saveImageToInputField.condition = False
                changeScreen(main.screen, destroyers = [emptyArea(10, 1, 97, 0)], rectangs = [rect(10, 2, 97, 0, color.grey)], texts = [text("save", 100, 1)])
                main.saveImageButton.condition = True
                
                    
            #count increases to make cursor blink
            count = count+1
            #The blinking of the cursor
            if(count>30):
                if(main.screen[0][main.cursor.posy][main.cursor.posx] == color.white):
                    main.screen[0][main.cursor.posy][main.cursor.posx] = main.underCurs
                else:
                    main.screen[0][main.cursor.posy][main.cursor.posx] = color.white
                    count = 0
            #~~~~~~~~~~~~~~~~~~~~~~~~~~
            #reprints screen
            updateScreen(main.oldScreen, main.screen)
main.main()
