import tty, sys, termios, threading


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

def gotoXY(x, y):
    print("\033["+ str(y) +";" + str(x)+"f", end="")
    
class col:
    black  = "\033[0;30m"
    blue = "\033[0;34m"
    green  = "\033[0;32m"
    cyan = "\033[0;36m"
    red = "\033[0;31m"
    purple = "\033[0;35m"
    brown  = "\033[0;33m"
    gray = "\033[0;37m"
    darkGray = "\033[1;30m"
    lightBlue = "\033[1;34m"
    lightGreen = "\033[1;32m"
    lightCyan = "\033[1;36m"
    lightRed = "\033[1;31m"
    lightPurple = "\033[1;35m"
    yellow = "\033[1;33m"
    white = "\033[1;37m"

class reset:
    reset = "\u001b[0m"
    
class bak:
    gray='\033[40m'
    grey='\033[40m'
    red='\033[41m'
    green='\033[42m'
    yellow='\033[43m'
    blue='\033[44m'
    purple='\033[45m'
    cyan='\033[46m' 
    white='\033[47m'


def setScreen(this = "so"):
    screen = []
    for y in range(30):
        screen.append([])
        for x in range(50):
            screen[y].append([])
            if(this == "so"):
                screen[y][x].append(col.white)
                screen[y][x].append(bak.gray)
                screen[y][x].append(" ")
            elif(this == "not"):
                screen[y][x].append(col.red)
                screen[y][x].append(bak.gray)
                screen[y][x].append(" ")
    return screen
            
            
def upScreen():
    main.screen = setScreen()
    main.oldScreen = setScreen("not")
    while(True):
        if(main.screen!=main.oldScreen):
            for y in range(30):
                if(main.screen[y]!=main.oldScreen[y]):
                    for x in range(50):
                        gotoXY(x+1, y+1)
                        print(main.screen[y][x][0]+main.screen[y][x][1]+main.screen[y][x][2])
                        main.oldScreen[y][x][0] = main.screen[y][x][0]
                        main.oldScreen[y][x][1] = main.screen[y][x][1]
                        main.oldScreen[y][x][2] = main.screen[y][x][2]
        
        
    
class keyThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        keycode.keyCollecter()
    
class screenThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        upScreen()

class enemyThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        enemyMovements()

def enemyMovements():
    pass

class player:
    posX = 25 
    posy = 15
    
    def jump():
        if(player.position[0]-)


class main:
    oldScreen = []
    screen = []
    def main():
        keys = keyThread()
        keys.start()
        screen = screenThread()
        enems = enemyThread()
        enems.start()
        print("Welcome to the boss battle.\n(Press space to start or t for tutorial)")
        while(1):
            if(keycode.keydown(" ")):
                break
            elif(keycode.keydown("t") or keycode.keydown("T")):
                print("The point is to defeat the big guy in the background. His hands and head are in the foreground. To defeat him, hit his head by throwing mini\nenemies at him.")
                while(1):
                    if(keycode.keydown(" ")):
                        break
                break
        screen.start()
        while(True):
            if(keycode.keydown("upAr")):
                player.jump()
            elif(keycode.keydown("rightAr")):
                player.right()
            elif(keycode.keydown("leftAr")):
                player.left()
            elif(keycode.keydown(" ")):
                if(player.holding[1]):
                    player.throw()
                else:
                    player.grab()
            
        
            
main.main()
