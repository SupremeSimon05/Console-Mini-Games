import math
import random
playerChips = 20
playerCards = []
botChips = 20
botCards = []
allCards = [[1, "diamonds"],[1, "hearts"],[1, "clubs"],[1, "spades"],[2, "diamonds"],[2, "hearts"],[2, "clubs"],[2, "spades"],[3, "diamonds"],[3, "hearts"],[3, "clubs"],[3, "spades"],[4, "diamonds"],[4, "hearts"],[4, "clubs"],[4, "spades"],[5, "diamonds"],[5, "hearts"],[5, "clubs"],[5, "spades"],[6, "diamonds"],[6, "hearts"],[6, "clubs"],[6, "spades"],[7, "diamonds"],[7, "hearts"],[7, "clubs"],[7, "spades"],[8, "diamonds"],[8, "hearts"],[8, "clubs"],[8, "spades"],[9, "diamonds"],[9, "hearts"],[9, "clubs"],[9, "spades"],[10, "diamonds"],[10, "hearts"],[10, "clubs"],[10, "spades"],[11, "diamonds"],[11, "hearts"],[11, "clubs"],[11, "spades"],[12, "diamonds"],[12, "hearts"],[12, "clubs"],[12, "spades"],[13, "diamonds"],[13, "hearts"],[13, "clubs"],[13, "spades"]]
round = 0
pot = 0
highestBet = 0
playerBet = 0
botBet = 0
PlayerEnded = False
botEnded = False
playerTotalBet = 0
botTotalBet = 0


'''
to do list

'''

def main():
    #a ton of initialization 
    global playerChips
    global playerCards
    global botChips
    global botCards
    global allCards
    global round
    global pot
    global PlayerEnded
    global botEnded
    anteNum = 0
	
	#some important stuffs
    print("5 Card Poker!")
    onlyForYNRN = str(input("Would you like to play? ")).lower()
    while((onlyForYNRN + "yes")[0] != "n"):
        while(True):
            try:
                startTotal = int(input("How many chips do you want to start the game with? "))
                if(startTotal>0):
                    break
                print("You have to start with more than 0 chips ")
            except:
                print("Please enter a real integer ")
        playerChips = startTotal
        botChips = startTotal
        round = 0
        print("Time to play!")
        while(True):
            if(playerChips<1 or botChips<1):
                break
            PlayerEnded = False
            botEnded = False
            playerCards = []
            botCards = []
            allCards = [['A', "diamonds"],['A', "hearts"],['A', "clubs"],['A', "spades"],[2, "diamonds"],[2, "hearts"],[2, "clubs"],[2, "spades"],[3, "diamonds"],[3, "hearts"],[3, "clubs"],[3, "spades"],[4, "diamonds"],[4, "hearts"],[4, "clubs"],[4, "spades"],[5, "diamonds"],[5, "hearts"],[5, "clubs"],[5, "spades"],[6, "diamonds"],[6, "hearts"],[6, "clubs"],[6, "spades"],[7, "diamonds"],[7, "hearts"],[7, "clubs"],[7, "spades"],[8, "diamonds"],[8, "hearts"],[8, "clubs"],[8, "spades"],[9, "diamonds"],[9, "hearts"],[9, "clubs"],[9, "spades"],[10, "diamonds"],[10, "hearts"],[10, "clubs"],[10, "spades"],['J', "diamonds"],['J', "hearts"],['J', "clubs"],['J', "spades"],['Q', "diamonds"],['Q', "hearts"],['Q', "clubs"],['Q', "spades"],['K', "diamonds"],['K', "hearts"],['K', "clubs"],['K', "spades"]]
            round = round + 1
            if(botChips - int(math.sqrt(round))>=0 and playerChips - int(math.sqrt(round))>=0):
                pot = int(math.sqrt(round)) + int(math.sqrt(round))
                botChips = int(botChips - int(math.sqrt(round)))
                playerChips = int(playerChips - int(math.sqrt(round)))
            elif(botChips - int(math.sqrt(round))<=0):
                pot = botChips * 2
                botChips = 0
                playerChips = playerChips - botChips
            elif(playerChips - int(math.sqrt(round))<=0):
                pot = playerChipsChips * 2
                botChips = botChips - playerChips
                playerChips = 0
                
            cardToAdd = []
			
			
			#the actual game
            dealCards(1)
            print("Your hand: " + str(playerCards))
            bets()
            if((not PlayerEnded) and (not botEnded)):
                dealCards(2, "player")
                dealCards(2, "bot")
                bets(2)
            if(not(PlayerEnded) and not(botEnded)):
                print("Your cards: " + str(playerCards))
                print("Their cards: " + str(botCards))
                if(compareCards() == "player"):
                    playerChips = pot + playerChips
                    print("You won this hand! You now have " + str(playerChips) + " chips.")
                elif(compareCards() == "bot"):
                    botChips = pot + botChips
                    print("You didn't win this one, but you'll get em next time. ")
                else:
                    print("You and the bot tied. You had the hand: " + str(playerCards) + " and the bot had the hand: " + str(botCards))
                    botChips = int(botChips + pot/2)
                    playerChips = int(playerChips + pot/2)
            elif(botEnded):
                playerChips = pot + playerChips
            elif(PlayerEnded):
                botChips = pot + botChips
            if(playerChips>1 and botChips>1):
                print("New hand starting. ")
        if(botChips>playerChips):
            print("Sorry but the bot won the overall game. You can try again if you would like though... ")
        elif(playerChips>botChips):
            print("You won the overall game. Great work! If you want you can test you luck again... ")
        onlyForYNRN = str(input("Would you like to play again? ")).lower()
    print("Thanks for playing! I hope you had fun. ")
            
	

def CTPCTTIC(players, inputed):
    inputed = str(inputed)
    if(str(str(players[0]) + str(players[1][0])).lower() == inputed.lower()):
        return True
    else:
        return False
    

def dealCards(time, a = "bot"):
    global playerCards
    global botCards
    
    cardToTrade = []
    numCardsToTrade = 0
    num = 0
    aced = False
    
    if(time == 1):
        for i in range (5):
            cardToAdd = allCards[random.randrange(0, len(allCards)-1)]
            playerCards.append(cardToAdd)
            allCards.remove(cardToAdd)
        for i in range (5):
            cardToAdd = allCards[random.randrange(0, len(allCards)-1)]
            allCards.remove(cardToAdd)
            botCards.append(cardToAdd)
    else:
        if(a == "player"):
            while(True):
                try:
                    while(True):
                        numCardsToTrade = input("How many cards do you want to trade in? ")
                        if(int(numCardsToTrade) >= 0 and (int(numCardsToTrade) < 4 or (hasCard("player", 'A') and int(numCardsToTrade) == 4))):
                            break
                        print("You can't trade in that many cards ")
                except:
                    print("Please enter a real integer ")
                    continue
                break
            numCardsToTrade = int(numCardsToTrade)
            if(numCardsToTrade == 4):
                cardToTrade = []
                for i in range(5):
                    if('A' in playerCards[i]):
                        playerCards = [playerCards[i]]
                        break
            else:
                i = 0
                while(True and numCardsToTrade != 0):
                    num = 0
                    cardToTrade = input("What card do you want to trade? " + str(playerCards) + " are your current cards. Enter 'cancel' to cancel. Please type it like '3C' for 3 of clubs or 'AS' for ace of spades.  ")
                    for p in range(len(playerCards)):
                        if(CTPCTTIC(playerCards[p], cardToTrade)):
                            playerCards.pop(p)
                            break
                        else:
                            num = num + 1
                    if(num == 5 and not(str(cardToTrade + " ")[0] == 'C' or str(cardToTrade + " ")[0] == 'c' or cardToTrade == None)):
                        print("You don't have that card, please try again or cancel the trade. \n(Problems to check for: Make sure you only input one card at a time and make sure you don't actually put the quotes around the card)")
                        i = i - 1
                    if(str(cardToTrade + " ")[0] == 'C' or cardToTrade + " "[0] == 'c' or cardToTrade == None):
                        print("Card trade cancelled ")
                        numCardsToTrade = numCardsToTrade - 1
                    i = i + 1
                    if(i>=numCardsToTrade):
                        break
            for i in range(numCardsToTrade):
                cardToAdd = allCards[random.randrange(0, len(allCards)-1)]
                playerCards.append(cardToAdd)
                allCards.remove(cardToAdd)
            print("Your cards now: " + str(playerCards))
        else:
            if(hasAlmostFlush("bot")):
                if(hasMultipleSuits("hearts", 4)):
                    for i in range(5):
                        if(botCards[i][1] != "hearts"):
                            cardToTrade.append(botCards[i])
                if(hasMultipleSuits("diamonds", 4)):
                    for i in range(5):
                        if(botCards[i][1] != "diamonds"):
                            cardToTrade.append(botCards[i])
                if(hasMultipleSuits("clubs", 4)):
                    for i in range(5):
                        if(botCards[i][1] != "clubs"):
                            cardToTrade.append(botCards[i])
                if(hasMultipleSuits("spades", 4)):
                    for i in range(5):
                        if(botCards[i][1] != "spades"):
                            cardToTrade.append(botCards[i])
            if(hasFourOfKind("bot")):
                for c in range(9):
                    if(hasMultipleCards(c+1, 4)):
                        for i in range(5):
                            if(botCards[i][0] != c+1):
                                cardToTrade.append(botCards[i])
                if(hasMultipleCards('A', 4)):
                    for i in range(5):
                        if(botCards[i][0] != 'A'):
                            cardToTrade.append(botCards[i])
                if(hasMultipleCards('J', 4)):
                    for i in range(5):
                        if(botCards[i][0] != 'J'):
                            cardToTrade.append(botCards[i])
                if(hasMultipleCards('Q', 4)):
                    for i in range(5):
                        if(botCards[i][0] != 'Q'):
                            cardToTrade.append(botCards[i])
                if(hasMultipleCards('K', 4)):
                    for i in range(5):
                        if(botCards[i][0] != 'K'):
                            cardToTrade.append(botCards[i])
            if(hasTwoPair("bot")):
                if(hasMultipleCards('A', 2) and hasMultipleCards(2, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 'A' and  botCards[i][0] != 2):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards('A', 2) and hasMultipleCards(3, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 'A' and  botCards[i][0] != 3):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards('A', 2) and hasMultipleCards(4, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 'A' and  botCards[i][0] != 4):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards('A', 2) and hasMultipleCards(5, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 'A' and  botCards[i][0] != 5):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards('A', 2) and hasMultipleCards(6, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 'A' and  botCards[i][0] != 6):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards('A', 2) and hasMultipleCards(7, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 'A' and  botCards[i][0] != 7):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards('A', 2) and hasMultipleCards(8, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 'A' and  botCards[i][0] != 8):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards('A', 2) and hasMultipleCards(9, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 'A' and  botCards[i][0] != 9):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards('A', 2) and hasMultipleCards(10, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 'A' and  botCards[i][0] != 10):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards('A', 2) and hasMultipleCards('J', 2)):
                    for i in range(5):
                        if(botCards[i][0] != 'A' and  botCards[i][0] != 'J'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards('A', 2) and hasMultipleCards('Q', 2)):
                    for i in range(5):
                        if(botCards[i][0] != 'A' and  botCards[i][0] != 'Q'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards('A', 2) and hasMultipleCards('K', 2)):
                    for i in range(5):
                        if(botCards[i][0] != 'A' and  botCards[i][0] != 'K'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(2, 2) and hasMultipleCards(3, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 2 and  botCards[i][0] != 3):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(2, 2) and hasMultipleCards(4, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 2 and  botCards[i][0] != 4):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(2, 2) and hasMultipleCards(5, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 2 and  botCards[i][0] != 5):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(2, 2) and hasMultipleCards(6, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 2 and  botCards[i][0] != 6):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(2, 2) and hasMultipleCards(7, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 2 and  botCards[i][0] != 7):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(2, 2) and hasMultipleCards(8, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 2 and  botCards[i][0] != 8):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(2, 2) and hasMultipleCards(9, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 2 and  botCards[i][0] != 9):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(2, 2) and hasMultipleCards(10, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 2 and  botCards[i][0] != 10):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(2, 2) and hasMultipleCards('J', 2)):
                    for i in range(5):
                        if(botCards[i][0] != 2 and  botCards[i][0] != 'J'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(2, 2) and hasMultipleCards('Q', 2)):
                    for i in range(5):
                        if(botCards[i][0] != 2 and  botCards[i][0] != 'Q'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(2, 2) and hasMultipleCards('K', 2)):
                    for i in range(5):
                        if(botCards[i][0] != 2 and  botCards[i][0] != 'K'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(3, 2) and hasMultipleCards(4, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 3 and  botCards[i][0] != 4):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(3, 2) and hasMultipleCards(5, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 3 and  botCards[i][0] != 5):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(3, 2) and hasMultipleCards(6, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 3 and  botCards[i][0] != 6):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(3, 2) and hasMultipleCards(7, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 3 and  botCards[i][0] != 7):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(3, 2) and hasMultipleCards(8, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 3 and  botCards[i][0] != 8):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(3, 2) and hasMultipleCards(9, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 3 and  botCards[i][0] != 9):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(3, 2) and hasMultipleCards(10, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 3 and  botCards[i][0] != 10):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(3, 2) and hasMultipleCards('J', 2)):
                    for i in range(5):
                        if(botCards[i][0] != 3 and  botCards[i][0] != 'J'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(3, 2) and hasMultipleCards('Q', 2)):
                    for i in range(5):
                        if(botCards[i][0] != 3 and  botCards[i][0] != 'Q'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(3, 2) and hasMultipleCards('K', 2)):
                    for i in range(5):
                        if(botCards[i][0] != 3 and  botCards[i][0] != 'K'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(4, 2) and hasMultipleCards(5, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 4 and  botCards[i][0] != 5):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(4, 2) and hasMultipleCards(6, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 4 and  botCards[i][0] != 6):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(4, 2) and hasMultipleCards(7, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 4 and  botCards[i][0] != 7):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(4, 2) and hasMultipleCards(8, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 4 and  botCards[i][0] != 8):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(4, 2) and hasMultipleCards(9, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 4 and  botCards[i][0] != 9):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(4, 2) and hasMultipleCards(10, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 4 and  botCards[i][0] != 10):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(4, 2) and hasMultipleCards('J', 2)):
                    for i in range(5):
                        if(botCards[i][0] != 4 and  botCards[i][0] != 'J'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(4, 2) and hasMultipleCards('Q', 2)):
                    for i in range(5):
                        if(botCards[i][0] != 4 and  botCards[i][0] != 'Q'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(4, 2) and hasMultipleCards('K', 2)):
                    for i in range(5):
                        if(botCards[i][0] != 4 and  botCards[i][0] != 'K'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(5, 2) and hasMultipleCards(6, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 5 and  botCards[i][0] != 6):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(5, 2) and hasMultipleCards(7, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 5 and  botCards[i][0] != 7):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(5, 2) and hasMultipleCards(8, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 5 and  botCards[i][0] != 8):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(5, 2) and hasMultipleCards(9, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 5 and  botCards[i][0] != 9):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(5, 2) and hasMultipleCards(10, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 5 and  botCards[i][0] != 10):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(5, 2) and hasMultipleCards('J', 2)):
                    for i in range(5):
                        if(botCards[i][0] != 5 and  botCards[i][0] != 'J'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(5, 2) and hasMultipleCards('Q', 2)):
                    for i in range(5):
                        if(botCards[i][0] != 5 and  botCards[i][0] != 'Q'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(5, 2) and hasMultipleCards('K', 2)):
                    for i in range(5):
                        if(botCards[i][0] != 5 and  botCards[i][0] != 'K'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(6, 2) and hasMultipleCards(7, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 6 and  botCards[i][0] != 7):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(6, 2) and hasMultipleCards(8, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 6 and  botCards[i][0] != 8):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(6, 2) and hasMultipleCards(9, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 6 and  botCards[i][0] != 9):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(6, 2) and hasMultipleCards(10, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 6 and  botCards[i][0] != 10):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(6, 2) and hasMultipleCards('J', 2)):
                    for i in range(5):
                        if(botCards[i][0] != 6 and  botCards[i][0] != 'J'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(6, 2) and hasMultipleCards('Q', 2)):
                    for i in range(5):
                        if(botCards[i][0] != 6 and  botCards[i][0] != 'Q'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(6, 2) and hasMultipleCards('K', 2)):
                    for i in range(5):
                        if(botCards[i][0] != 6 and  botCards[i][0] != 'K'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(7, 2) and hasMultipleCards(8, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 7 and  botCards[i][0] != 8):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(7, 2) and hasMultipleCards(9, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 7 and  botCards[i][0] != 9):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(7, 2) and hasMultipleCards(10, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 7 and  botCards[i][0] != 10):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(7, 2) and hasMultipleCards('J', 2)):
                    for i in range(5):
                        if(botCards[i][0] != 7 and  botCards[i][0] != 'J'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(7, 2) and hasMultipleCards('Q', 2)):
                    for i in range(5):
                        if(botCards[i][0] != 7 and  botCards[i][0] != 'Q'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(7, 2) and hasMultipleCards('K', 2)):
                    for i in range(5):
                        if(botCards[i][0] != 7 and  botCards[i][0] != 'K'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(8, 2) and hasMultipleCards(9, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 8 and  botCards[i][0] != 9):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(8, 2) and hasMultipleCards(10, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 8 and  botCards[i][0] != 10):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(8, 2) and hasMultipleCards('J', 2)):
                    for i in range(5):
                        if(botCards[i][0] != 8 and  botCards[i][0] != 'J'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(8, 2) and hasMultipleCards('Q', 2)):
                    for i in range(5):
                        if(botCards[i][0] != 8 and  botCards[i][0] != 'Q'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(8, 2) and hasMultipleCards('K', 2)):
                    for i in range(5):
                        if(botCards[i][0] != 8 and  botCards[i][0] != 'K'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(9, 2) and hasMultipleCards(10, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 9 and  botCards[i][0] != 10):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(9, 2) and hasMultipleCards('J', 2)):
                    for i in range(5):
                        if(botCards[i][0] != 9 and  botCards[i][0] != 'J'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(9, 2) and hasMultipleCards('Q', 2)):
                    for i in range(5):
                        if(botCards[i][0] != 9 and  botCards[i][0] != 'Q'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(9, 2) and hasMultipleCards('K', 2)):
                    for i in range(5):
                        if(botCards[i][0] != 9 and  botCards[i][0] != 'K'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(10, 2) and hasMultipleCards('J', 2)):
                    for i in range(5):
                        if(botCards[i][0] != 10 and  botCards[i][0] != 'J'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(10, 2) and hasMultipleCards('Q', 2)):
                    for i in range(5):
                        if(botCards[i][0] != 10 and  botCards[i][0] != 'Q'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(10, 2) and hasMultipleCards('K', 2)):
                    for i in range(5):
                        if(botCards[i][0] != 10 and  botCards[i][0] != 'K'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards('J', 2) and hasMultipleCards('Q', 2)):
                    for i in range(5):
                        if(botCards[i][0] != 'J' and  botCards[i][0] != 'Q'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards('J', 2) and hasMultipleCards('K', 2)):
                    for i in range(5):
                        if(botCards[i][0] != 'J' and  botCards[i][0] != 'K'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards('Q', 2) and hasMultipleCards('K', 2)):
                    for i in range(5):
                        if(botCards[i][0] != 'Q' and  botCards[i][0] != 'K'):
                            cardToTrade.append(botCards[i])
            elif(hasThreeOfKind("bot")):
                if(hasMultipleCards('A', 3)):
                    for i in range(5):
                        if(botCards[i][0] != 'A'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(2, 3)):
                    for i in range(5):
                        if(botCards[i][0] != 2):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(3, 3)):
                    for i in range(5):
                        if(botCards[i][0] != 3):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(4, 3)):
                    for i in range(5):
                        if(botCards[i][0] != 4):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(5, 3)):
                    for i in range(5):
                        if(botCards[i][0] != 5):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(6, 3)):
                    for i in range(5):
                        if(botCards[i][0] != 6):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(7, 3)):
                    for i in range(5):
                        if(botCards[i][0] != 7):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(8, 3)):
                    for i in range(5):
                        if(botCards[i][0] != 8):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(9, 3)):
                    for i in range(5):
                        if(botCards[i][0] != 9):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(10, 3)):
                    for i in range(5):
                        if(botCards[i][0] != 10):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards('J', 3)):
                    for i in range(5):
                        if(botCards[i][0] != 'J'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards('Q', 3)):
                    for i in range(5):
                        if(botCards[i][0] != 'Q'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards('K', 3)):
                    for i in range(5):
                        if(botCards[i][0] != 'K'):
                            cardToTrade.append(botCards[i])
            elif(hasPair("bot")):
                if(hasMultipleCards('A', 2)):
                    for i in range(5):
                        if(botCards[i][0] != 'A'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(2, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 2):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(3, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 3):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(4, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 4):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(5, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 5):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(6, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 6):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(7, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 7):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(8, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 8):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(9, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 9):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards(10, 2)):
                    for i in range(5):
                        if(botCards[i][0] != 10):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards('J', 2)):
                    for i in range(5):
                        if(botCards[i][0] != 'J'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards('Q', 2)):
                    for i in range(5):
                        if(botCards[i][0] != 'Q'):
                            cardToTrade.append(botCards[i])
                elif(hasMultipleCards('K', 2)):
                    for i in range(5):
                        if(botCards[i][0] != 'K'):
                            cardToTrade.append(botCards[i])
            elif(hasCard("bot", 'A')):
                for i in range(5):
                    if(botCards[i][0] != 'A'):
                        cardToTrade.append(botCards[i])
            else:
                for i in range(3):
                    nextCardNum = highestCardNum("bot", 5-i)
                    for d in range(5):
                        if(nextCardNum == botCards[d][0]):
                            cardToTrade.append(botCards[d])
            zzz = botsTradeAmount()
            if(zzz!=1):
                print("The bot traded in " + str(zzz) + " cards. ")
            else:
                print("The bot traded in 1 card. ")
            for i in range(zzz):
                botCards.remove(cardToTrade[zzz-(i+1)])
            for i in range(zzz):
                cardToAdd = allCards[random.randrange(0, len(allCards)-1)]
                botCards.append(cardToAdd)
                allCards.remove(cardToAdd)
                                
def hasMultipleCards(card, amount, a = "bot"):
    global botCards
    num = 0
    
    if(a == "player"):
        for i in range (5):
            if(playerCards[i][0] == card):
                num = num+1
        if(num == amount):
            return True
        else: 
            return False
    else:
        for i in range (5):
            if(botCards[i][0] == card):
                num = num+1
        if(num == amount):
            return True
        else: 
            return False

def hasSuit(suit):
    global botCards
    num = 0
    
    for i in range(5):
        if(botCards[i][1] == suit):
            return True
        else:
            num = num +1
    if(num == 5):
        return False
        
def hasMultipleSuits(suit, amount):
    global botCards
    num = 0 
    
    for i in range(5):
        if(botCards[i][1] == suit):
            num = num + 1
    if(num == amount):
        return True
    else:
        return False


def hasCardWSuit(card):
    global botCards
    num = 0
    
    for i in range(5):
        if(botCards[i] == card):
            return True
        else:
            num = num + 1
    if(num == 5):
        return False

def bets(time = 0):
    global pot
    global playerTotalBet
    global botTotalBet
    botTotalBet = 0
    playerTotalBet = 0
    rk = False
    
    while(True):
        oneBet("player", time)
        if((rk and botTotalBet == playerTotalBet) or PlayerEnded or botEnded):
            break
        rk=True
        oneBet("bot", time)
        if(botTotalBet == playerTotalBet or PlayerEnded or botEnded):
            break
    pot = pot + playerTotalBet + botTotalBet
    
    
    

def oneBet(a, time = 1):
    global PlayerEnded
    global botEnded
    global playerChips
    global pot
    global botCards
    global botChips
    global highestBet
    global botBet
    global playerBet
    global playerTotalBet
    global botTotalBet
    
    if(a == "player"):
        playerBet = int(playerChips+1)
        while(True):
            try:
                while(True):
                    playerBet = input("How much do you want to bet? You have " + str(playerChips) + " chips, the pot so far is " + str(pot + playerTotalBet + botTotalBet) + " chips, and the least you can bet to stay in is " + str(botTotalBet - playerTotalBet) + " chips. The bot has " + str(botChips) + " chips. Enter 'f' or 'fold' to fold. ")
                    playerBet = int(playerBet)
                    if((playerBet <= playerChips and playerTotalBet + playerBet >= botTotalBet) or PlayerEnded or botEnded):
                        break
                    print("You can't bet that much ")
                break
            except:
                try:
                    if(playerBet[0] == 'f'):
                        PlayerEnded = True
                        print("You folded, which means the bot won with the cards " + str(botCards))
                        break
                    else:
                        print("Please enter a valid response ")
                except:
                    print("Please enter a valid response ")
        try:
            if(playerBet>botChips + (botTotalBet - playerTotalBet)):
                print("You bet more than the bot has. Your bet has been set back to an amount that the bot can match")
                playerBet = botChips
            if((not botEnded)):
                playerTotalBet = playerTotalBet + playerBet
                playerChips = playerChips - playerBet
                print("You now have " + str(playerChips) + " chips")
        except:
            pass
    else:
        try:
            botBet = int(botChips+1)
            if(hasRoyalFlush("bot")):
                botBet = int(botChips - random.randrange(0, int(botChips/10)))
            elif(hasStraight("bot") and hasFlush("bot")):
                botBet = int(botChips - random.randrange(int(botChips/20), int(botChips/9)))
            elif(hasFourOfKind("bot")):
                botBet = int(botChips - random.randrange(int(botChips/19), int(botChips/8)))
            elif(hasFullHouse("bot")):
                botBet = int(botChips - random.randrange(int(botChips/18), int(botChips/7)))
            elif(hasFlush("bot")):
                botBet = int(botChips - random.randrange(int(botChips/17), int(botChips/6)))
            elif(hasStraight("bot")):
                botBet = int(botChips - random.randrange(int(botChips/16), int(botChips/5)))
            elif(hasThreeOfKind("bot")):
                botBet = int(botChips - random.randrange(int(botChips/15), int(botChips/4)))
            elif(hasTwoPair("bot")):
                botBet = int(botChips - random.randrange(int(botChips/2), int(botChips)))
            elif(hasPair("bot")):
                botBet = int(botChips - random.randrange(int(botChips/2), int(botChips-botChips/10)))
            elif(hasCard("bot", 'A')):
                if(time == 1):
                    botBet = int(botChips/10 + random.randrange(0, int(botChips/11 + botChips/12)))
                else:
                    botBet = int(botChips/10 + random.randrange(0, int(botChips/11)))
            else:
                if(time == 1):
                    botBet = int(random.randrange(0, int(botChips/11 + botChips/12)))
                else:
                    botBet = int(random.randrange(0, int(botChips/11)))
            if(botBet+botTotalBet<playerTotalBet):
                if(hasRoyalFlush("bot")):
                    botBet = botBet + int(random.randrange(0, int(botChips/2)))
                elif(hasStraight("bot") and hasFlush("bot")):
                    botBet = botBet + int(random.randrange(0, int(botChips/3)))
                elif(hasFourOfKind("bot")):
                    botBet = botBet + int(random.randrange(0, int(botChips/4)))
                elif(hasFullHouse("bot")):
                    botBet = botBet + int(random.randrange(0, int(botChips/5)))
                elif(hasFlush("bot")):
                    botBet = botBet + int(random.randrange(0, int(botChips/6)))
                elif(hasStraight("bot")):
                    botBet = botBet + int(random.randrange(0, int(botChips/7)))
                elif(hasThreeOfKind("bot")):
                    botBet = botBet + int(random.randrange(0, int(botChips/8)))
                elif(hasTwoPair("bot")):
                    botBet = botBet + int(random.randrange(0, int(botChips/9)))
                elif(hasPair("bot")):
                    botBet = botBet + int(random.randrange(0, int(botChips/10)))
                elif(hasCard("bot", 'A')):
                    if(time == 1):
                        botBet = botBet + int(random.randrange(0, int(botChips/11 + botChips/12)))
                    else:
                        botBet = botBet + int(random.randrange(0, int(botChips/11)))
                else:
                    if(time == 1):
                        botBet = botBet + int(random.randrange(0, int(botChips/11 + botChips/12)))
                    else:
                        botBet = botBet + int(random.randrange(0, int(botChips/11)))
        except:
            botBet = 0
        if(playerTotalBet >= botChips and (hasPair("bot") or hasFlush("bot") or hasStraight("bot")) and random.randrange(0, 2) == 1):
            botBet = botChips
        if(botBet > botChips):
            botBet = botChips
        elif(botBet > playerChips - (botTotalBet - playerTotalBet)):
            botBet = playerChips
        if(playerTotalBet + playerBet == 0 and botBet <= 0):
            botBet = playerBet
        if(botBet + botTotalBet < playerTotalBet):
            print("The bot has folded. You won this hand with a pot of " + str(pot + playerTotalBet + botTotalBet) + " chips!")
            botEnded = True
            botBet = 0
        else:
            if(botBet + botTotalBet >playerTotalBet):
                print("The bot raised... ")
            botTotalBet = botTotalBet + botBet
            botChips = botChips - botBet
        
    
    
    
def hasPair(a):
	global playerCards
	global botCards
	
	if(a == "player"):
		if(playerCards[0][0] == playerCards[1][0] or playerCards[0][0] == playerCards[2][0] or playerCards[0][0] == playerCards[3][0] or playerCards[0][0] == playerCards[4][0] or playerCards[1][0] == playerCards[2][0] or playerCards[1][0] == playerCards[3][0] or playerCards[1][0] == playerCards[4][0] or playerCards[2][0] == playerCards[3][0] or playerCards[2][0] == playerCards[4][0] or playerCards[3][0] == playerCards[4][0]):
			return True
		else:
			return False
	else:
		if(botCards[0][0] == botCards[1][0] or botCards[0][0] == botCards[2][0] or botCards[0][0] == botCards[3][0] or botCards[0][0] == botCards[4][0] or botCards[1][0] == botCards[2][0] or botCards[1][0] == botCards[3][0] or botCards[1][0] == botCards[4][0] or botCards[2][0] == botCards[3][0] or botCards[2][0] == botCards[4][0] or botCards[3][0] == botCards[4][0]):
			return True
		else:
			return False

def hasTwoPair(a):
	global playerCards
	global botCards
	
	if(a == "player"):
		if((playerCards[0][0] == playerCards[1][0] and playerCards[2][0] == playerCards[3][0]) or (playerCards[0][0] == playerCards[1][0] and playerCards[2][0] == playerCards[4][0]) or (playerCards[0][0] == playerCards[1][0] and playerCards[3][0] == playerCards[4][0]) or (playerCards[0][0] == playerCards[2][0] and playerCards[1][0] == playerCards[3][0]) or (playerCards[0][0] == playerCards[2][0] and playerCards[1][0] == playerCards[4][0]) or (playerCards[0][0] == playerCards[2][0] and playerCards[3][0] == playerCards[4][0]) or (playerCards[0][0] == playerCards[3][0] and playerCards[1][0] == playerCards[2][0]) or (playerCards[0][0] == playerCards[3][0] and playerCards[1][0] == playerCards[4][0]) or (playerCards[0][0] == playerCards[3][0] and playerCards[2][0] == playerCards[4][0]) or (playerCards[0][0] == playerCards[4][0] and playerCards[1][0] == playerCards[2][0]) or (playerCards[0][0] == playerCards[4][0] and playerCards[1][0] == playerCards[3][0]) or (playerCards[0][0] == playerCards[4][0] and playerCards[2][0] == playerCards[3][0]) or (playerCards[1][0] == playerCards[2][0] and playerCards[3][0] == playerCards[4][0]) or (playerCards[1][0] == playerCards[3][0] and playerCards[2][0] == playerCards[4][0]) or (playerCards[1][0] == playerCards[4][0] and playerCards[2][0] == playerCards[3][0])):
			return True
		else:
			return False
	else:
		if((botCards[0][0] == botCards[1][0] and botCards[2][0] == botCards[3][0]) or (botCards[0][0] == botCards[1][0] and botCards[2][0] == botCards[4][0]) or (botCards[0][0] == botCards[1][0] and botCards[3][0] == botCards[4][0]) or (botCards[0][0] == botCards[2][0] and botCards[1][0] == botCards[3][0]) or (botCards[0][0] == botCards[2][0] and botCards[1][0] == botCards[4][0]) or (botCards[0][0] == botCards[2][0] and botCards[3][0] == botCards[4][0]) or (botCards[0][0] == botCards[3][0] and botCards[1][0] == botCards[2][0]) or (botCards[0][0] == botCards[3][0] and botCards[1][0] == botCards[4][0]) or (botCards[0][0] == botCards[3][0] and botCards[2][0] == botCards[4][0]) or (botCards[0][0] == botCards[4][0] and botCards[1][0] == botCards[2][0]) or (botCards[0][0] == botCards[4][0] and botCards[1][0] == botCards[3][0]) or (botCards[0][0] == botCards[4][0] and botCards[2][0] == botCards[3][0]) or (botCards[1][0] == botCards[2][0] and botCards[3][0] == botCards[4][0]) or (botCards[1][0] == botCards[3][0] and botCards[2][0] == botCards[4][0]) or (botCards[1][0] == botCards[4][0] and botCards[2][0] == botCards[3][0])):
			return True
		else:
			return False

def hasFourOfKind(a):
	global playerCards
	global botCards
	
	if(a == "player"):
		if((playerCards[0][0] == playerCards[1][0] and playerCards[1][0] == playerCards[2][0] and playerCards[2][0] == playerCards[3][0]) or (playerCards[0][0] == playerCards[1][0] and playerCards[1][0] == playerCards[2][0] and playerCards[2][0] == playerCards[4][0]) or (playerCards[0][0] == playerCards[1][0] and playerCards[1][0] == playerCards[3][0] and playerCards[3][0] == playerCards[4][0]) or (playerCards[0][0] == playerCards[2][0] and playerCards[2][0] == playerCards[3][0] and playerCards[3][0] == playerCards[4][0]) or (playerCards[1][0] == playerCards[2][0] and playerCards[2][0] == playerCards[3][0] and playerCards[3][0] == playerCards[4][0])):
			return True
		else:
			return False
	else:
		if((botCards[0][0] == botCards[1][0] and botCards[1][0] == botCards[2][0] and botCards[2][0] == botCards[3][0]) or (botCards[0][0] == botCards[1][0] and botCards[1][0] == botCards[2][0] and botCards[2][0] == botCards[4][0]) or (botCards[0][0] == botCards[1][0] and botCards[1][0] == botCards[3][0] and botCards[3][0] == botCards[4][0]) or (botCards[0][0] == botCards[2][0] and botCards[2][0] == botCards[3][0] and botCards[3][0] == botCards[4][0]) or (botCards[1][0] == botCards[2][0] and botCards[2][0] == botCards[3][0] and botCards[3][0] == botCards[4][0])):
			return True
		else:
			return False
	
def hasThreeOfKind(a):
	global playerCards 
	global botCards
	
	if(a == "player"):
		if((playerCards[0][0] == playerCards[1][0] and playerCards[1][0] == playerCards[2][0]) or (playerCards[0][0] == playerCards[1][0] and playerCards[1][0] == playerCards[3][0]) or (playerCards[0][0] == playerCards[1][0] and playerCards[1][0] == playerCards[4][0]) or (playerCards[0][0] == playerCards[2][0] and playerCards[2][0] == playerCards[3][0]) or (playerCards[0][0] == playerCards[2][0] and playerCards[2][0] == playerCards[4][0]) or (playerCards[0][0] == playerCards[3][0] and playerCards[3][0] == playerCards[4][0]) or (playerCards[1][0] == playerCards[2][0] and playerCards[2][0] == playerCards[3][0]) or (playerCards[1][0] == playerCards[2][0] and playerCards[2][0] == playerCards[4][0]) or (playerCards[1][0] == playerCards[3][0] and playerCards[3][0] == playerCards[4][0]) or (playerCards[2][0] == playerCards[3][0] and playerCards[3][0] == playerCards[4][0])):
			return True
		else:
			return False
	else:
		if((botCards[0][0] == botCards[1][0] and botCards[1][0] == botCards[2][0]) or (botCards[0][0] == botCards[1][0] and botCards[1][0] == botCards[3][0]) or (botCards[0][0] == botCards[1][0] and botCards[1][0] == botCards[4][0]) or (botCards[0][0] == botCards[2][0] and botCards[2][0] == botCards[3][0]) or (botCards[0][0] == botCards[2][0] and botCards[2][0] == botCards[4][0]) or (botCards[0][0] == botCards[3][0] and botCards[3][0] == botCards[4][0]) or (botCards[1][0] == botCards[2][0] and botCards[2][0] == botCards[3][0]) or (botCards[1][0] == botCards[2][0] and botCards[2][0] == botCards[4][0]) or (botCards[1][0] == botCards[3][0] and botCards[3][0] == botCards[4][0]) or (botCards[2][0] == botCards[3][0] and botCards[3][0] == botCards[4][0])):
			return True
		else:
			return False

def hasFlush(a):
    global playerCards
    global botCards
	
    if(a == "player"):
        if(playerCards[0][1] == playerCards[1][1] and playerCards[0][1] == playerCards[2][1] and playerCards[0][1] == playerCards[3][1] and playerCards[0][1] == playerCards[4][1]):
            return True
        else:
            return False
    else:
        if(botCards[0][1] == botCards[1][1] and botCards[0][1] == botCards[2][1] and botCards[0][1] == botCards[3][1] and botCards[0][1] == botCards[4][1] and botCards[0][1] == botCards[5][1]):
            return True
        else:
            return False
			
def hasFullHouse(a):
    global playerCards
    global botCards
    
    if(a == "player"):
        if((playerCards[0][0] == playerCards[1][0] and playerCards[2][0] == playerCards[3][0] and playerCards[3][0] == playerCards[4][0]) or (playerCards[0][0] == playerCards[2][0] and playerCards[1][0] == playerCards[3][0] and playerCards[3][0] == playerCards[4][0]) or (playerCards[0][0] == playerCards[3][0] and playerCards[1][0] == playerCards[2][0] and playerCards[2][0] == playerCards[4][0]) or (playerCards[0][0] == playerCards[4][0] and playerCards[1][0] == playerCards[2][0] and playerCards[2][0] == playerCards[3][0]) or (playerCards[1][0] == playerCards[2][0] and playerCards[0][0] == playerCards[3][0] and playerCards[3][0] == playerCards[4][0]) or (playerCards[1][0] == playerCards[2][0] and playerCards[0][0] == playerCards[2][0] and playerCards[2][0] == playerCards[4][0]) or (playerCards[1][0] == playerCards[4][0] and playerCards[0][0] == playerCards[2][0] and playerCards[2][0] == playerCards[3][0]) or (playerCards[2][0] == playerCards[3][0] and playerCards[0][0] == playerCards[1][0] and playerCards[1][0] == playerCards[4][0]) or (playerCards[2][0] == playerCards[4][0] and playerCards[0][0] == playerCards[1][0] and playerCards[1][0] == playerCards[3][0]) or (playerCards[3][0] == playerCards[4][0] and playerCards[0][0] == playerCards[1][0] and playerCards[1][0] == playerCards[2][0])):
            return True
        else:
            return False
    else:
        if((botCards[0][0] == botCards[1][0] and botCards[2][0] == botCards[3][0] and botCards[3][0] == botCards[4][0]) or (botCards[0][0] == botCards[2][0] and botCards[1][0] == botCards[3][0] and botCards[3][0] == botCards[4][0]) or (botCards[0][0] == botCards[3][0] and botCards[1][0] == botCards[2][0] and botCards[2][0] == botCards[4][0]) or (botCards[0][0] == botCards[4][0] and botCards[1][0] == botCards[2][0] and botCards[2][0] == botCards[3][0]) or (botCards[1][0] == botCards[2][0] and botCards[0][0] == botCards[3][0] and botCards[3][0] == botCards[4][0]) or (botCards[1][0] == botCards[2][0] and botCards[0][0] == botCards[2][0] and botCards[2][0] == botCards[4][0]) or (botCards[1][0] == botCards[4][0] and botCards[0][0] == botCards[2][0] and botCards[2][0] == botCards[3][0]) or (botCards[2][0] == botCards[3][0] and botCards[0][0] == botCards[1][0] and botCards[1][0] == botCards[4][0]) or (botCards[2][0] == botCards[4][0] and botCards[0][0] == botCards[1][0] and botCards[1][0] == botCards[3][0]) or (botCards[3][0] == botCards[4][0] and botCards[0][0] == botCards[1][0] and botCards[1][0] == botCards[2][0])):
            return True
        else:
            return False

def hasStraight(a):
    global playerCards
    global botCards
    nums = []
    
    
    if(a == "player"):
        for i in range(len(playerCards)):
            if(playerCards[i][0] == "J"):
                nums.append(11)
            elif(playerCards[i][0] == "Q"):
                nums.append(12)
            elif(playerCards[i][0] == "K"):
                nums.append(13)
            elif(playerCards[i][0] == "A"):
                nums.append(1)
            elif(type(playerCards[i][0]) != int):
                print("problem with program. For some reason " + str(playerCards[i]) + " exists")
            else:
                nums.append(playerCards[i][0])
        if((not hasPair("player")) and max(nums) - min(nums) == 4):
            return True
        elif((not hasPair("player")) and hasCard("player", 'A') and hasCard("player", 'K') and hasCard("player", 'Q') and hasCard("player", 'J') and hasCard("player", 10)): 
            return True
        else:
            return False
    else:
        for i in range(len(botCards)):
            if(botCards[i][0] == "J"):
                nums.append(11)
            elif(botCards[i][0] == "Q"):
                nums.append(12)
            elif(botCards[i][0] == "K"):
                nums.append(13)
            elif(botCards[i][0] == "A"):
                nums.append(1)
            else:
                nums.append(botCards[i][0])
        if(not hasPair("bot") and max(nums) - min(nums) == 4):
            return True
        elif((not hasPair("player")) and hasCard("player", 'A') and hasCard("player", 'K') and hasCard("player", 'Q') and hasCard("player", 'J') and hasCard("player", 10)):
            return True
        else:
            return False
            
def hasCard(a, cardToCheck):
    global playerCards
    global botCards
    num = 0
    
    if(a == "player"):
        for i in range(5):
            if(cardToCheck == playerCards[i][0]):
                return True
            else:
                num = num+1
        if(num==5):
            return False
    else:
        for i in range(5):
            if(cardToCheck == botCards[i][0]):
                return True
            else:
                num = num+1
        if(num==5):
            return False
            
def hasRoyalFlush(a):
    global playerCards
    global botCards
    
    if(a == "player"):
        if(hasCard("player", 'A') and hasCard("player", 'J') and hasCard("player", 'Q') and hasCard("player", 'K') and hasCard("player", '10') and hasFlush("player")):
            return True
        else:
            return False
    else:
        if(hasCard("bot", 'A') and hasCard("bot", 'J') and hasCard("bot", 'Q') and hasCard("bot", 'K') and hasCard("bot", '10') and hasFlush("bot")):
            return True
        else:
            return False

def compareCards():
    global playerCards
    global botCards

    if(hasRoyalFlush("player") and (not(hasRoyalFlush("bot")))):
        return "player"
    elif((not hasRoyalFlush("player")) and hasRoyalFlush("bot")):
        return "bot"
    elif(hasRoyalFlush("player") and hasRoyalFlush("bot")):
        if(highestCardNum("player") > highestCardNum("bot")):
            return "player"
        elif(highestCardNum("player") < highestCardNum("bot")):
            return "bot"
        else:
            if(highestCardNum("player", 2) > highestCardNum("bot", 2)):
                return "player"
            elif(highestCardNum("player", 2) < highestCardNum("bot", 2)):
                return "bot"
            else:
                if(highestCardNum("player", 3) > highestCardNum("bot", 3)):
                    return "player"
                elif(highestCardNum("player", 3) < highestCardNum("bot", 3)):
                    return "bot"
                else:
                    if(highestCardNum("player", 4) > highestCardNum("bot", 4)):
                        return "player"
                    elif(highestCardNum("player", 4) < highestCardNum("bot", 4)):
                        return "bot"
                    else:
                        if(highestCardNum("player", 5) > highestCardNum("bot", 5)):
                            return "player"
                        elif(highestCardNum("player", 5) < highestCardNum("bot", 5)):
                            return "bot"
                        else:
                            return "tie"
    elif((hasStraight("player") and hasFlush("player")) and not (hasFlush("bot") and hasStraight("bot"))):
        return "player"
    elif((not(hasStraight("player") and hasFlush("player"))) and (hasFlush("bot") and hasStraight("bot"))):
        return "bot"
    elif(hasStraight("player") and  hasStraight("bot")):
        if(highestCardNum("player") > highestCardNum("bot")):
            return "player"
        elif(highestCardNum("player") < highestCardNum("bot")):
            return "bot"
        else:
            if(highestCardNum("player", 2) > highestCardNum("bot", 2)):
                return "player"
            elif(highestCardNum("player", 2) < highestCardNum("bot", 2)):
                return "bot"
            else:
                if(highestCardNum("player", 3) > highestCardNum("bot", 3)):
                    return "player"
                elif(highestCardNum("player", 3) < highestCardNum("bot", 3)):
                    return "bot"
                else:
                    if(highestCardNum("player", 4) > highestCardNum("bot", 4)):
                        return "player"
                    elif(highestCardNum("player", 4) < highestCardNum("bot", 4)):
                        return "bot"
                    else:
                        if(highestCardNum("player", 5) > highestCardNum("bot", 5)):
                            return "player"
                        elif(highestCardNum("player", 5) < highestCardNum("bot", 5)):
                            return "bot"
                        else:
                            return "tie"
    elif(hasFourOfKind("player") and not hasFourOfKind("bot")):
        return "player"
    elif((not hasFourOfKind("player")) and hasFourOfKind("bot")):
        return "bot"
    elif(hasFourOfKind("player") and hasFourOfKind("bot")):
        if(hasMultipleCards("A", 4, "player")):
            return "player"
        elif(hasMultipleCards("A", 4, "bot")):
            return "bot"
        elif(hasMultipleCards("K", 4, "player")):
            return "player"
        elif(hasMultipleCards("K", 4, "bot")):
            return "bot"
        elif(hasMultipleCards("Q", 4, "player")):
            return "player"
        elif(hasMultipleCards("Q", 4, "bot")):
            return "bot"
        elif(hasMultipleCards("J", 4, "player")):
            return "player"
        elif(hasMultipleCards("J", 4, "bot")):
            return "bot"
        elif(hasMultipleCards(10, 4, "player")):
            return "player"
        elif(hasMultipleCards(10, 4, "bot")):
            return "bot"
        elif(hasMultipleCards(9, 4, "player")):
            return "player"
        elif(hasMultipleCards(9, 4, "bot")):
            return "bot"
        elif(hasMultipleCards(8, 4, "player")):
            return "player"
        elif(hasMultipleCards(8, 4, "bot")):
            return "bot"
        elif(hasMultipleCards(7, 4, "player")):
            return "player"
        elif(hasMultipleCards(7, 4, "bot")):
            return "bot"
        elif(hasMultipleCards(6, 4, "player")):
            return "player"
        elif(hasMultipleCards(6, 4, "bot")):
            return "bot"
        elif(hasMultipleCards(5, 4, "player")):
            return "player"
        elif(hasMultipleCards(5, 4, "bot")):
            return "bot"
        elif(hasMultipleCards(4, 4, "player")):
            return "player"
        elif(hasMultipleCards(4, 4, "bot")):
            return "bot"
        elif(hasMultipleCards(3, 4, "player")):
            return "player"
        elif(hasMultipleCards(3, 4, "bot")):
            return "bot"
        elif(hasMultipleCards(2, 4, "player")):
            return "player"
        elif(hasMultipleCards(1, 4, "bot")):
            return "bot"
        elif(highestCardNum("player") > highestCardNum("bot")):
            return "player"
        elif(highestCardNum("player") < highestCardNum("bot")):
            return "bot"
        else:
            if(highestCardNum("player", 2) > highestCardNum("bot", 2)):
                return "player"
            elif(highestCardNum("player", 2) < highestCardNum("bot", 2)):
                return "bot"
            else:
                if(highestCardNum("player", 3) > highestCardNum("bot", 3)):
                    return "player"
                elif(highestCardNum("player", 3) < highestCardNum("bot", 3)):
                    return "bot"
                else:
                    if(highestCardNum("player", 4) > highestCardNum("bot", 4)):
                        return "player"
                    elif(highestCardNum("player", 4) < highestCardNum("bot", 4)):
                        return "bot"
                    else:
                        if(highestCardNum("player", 5) > highestCardNum("bot", 5)):
                            return "player"
                        elif(highestCardNum("player", 5) < highestCardNum("bot", 5)):
                            return "bot"
                        else:
                            return "tie"
    elif(hasFullHouse("player") and not hasFullHouse("bot")):
        return "player"
    elif((not hasFullHouse("player")) and hasFullHouse("bot")):
        return "bot"
    elif(hasFullHouse("player") and hasFullHouse("bot")):
        if(hasMultipleCards('A', 3, "player")):
            return "player"
        elif(hasMultipleCards('A', 3, "bot")):
            return "bot"
        elif(hasMultipleCards('K', 3, "player")):
            return "player"
        elif(hasMultipleCards('K', 3, "bot")):
            return "bot"
        elif(hasMultipleCards('Q', 3, "player")):
            return "player"
        elif(hasMultipleCards('Q', 3, "bot")):
            return "bot"
        elif(hasMultipleCards('J', 3, "player")):
            return "player"
        elif(hasMultipleCards('J', 3, "bot")):
            return "bot"
        elif(hasMultipleCards(10, 3, "player")):
            return "player"
        elif(hasMultipleCards(10, 3, "bot")):
            return "bot"
        elif(hasMultipleCards(9, 3, "player")):
            return "player"
        elif(hasMultipleCards(9, 3, "bot")):
            return "bot"
        elif(hasMultipleCards(8, 3, "player")):
            return "player"
        elif(hasMultipleCards(8, 3, "bot")):
            return "bot"
        elif(hasMultipleCards(7, 3, "player")):
            return "player"
        elif(hasMultipleCards(7, 3, "bot")):
            return "bot"
        elif(hasMultipleCards(6, 3, "player")):
            return "player"
        elif(hasMultipleCards(6, 3, "bot")):
            return "bot"
        elif(hasMultipleCards(5, 3, "player")):
            return "player"
        elif(hasMultipleCards(5, 3, "bot")):
            return "bot"
        elif(hasMultipleCards(4, 3, "player")):
            return "player"
        elif(hasMultipleCards(4, 3, "bot")):
            return "bot"
        elif(hasMultipleCards(3, 3, "player")):
            return "player"
        elif(hasMultipleCards(3, 3, "bot")):
            return "bot"
        elif(hasMultipleCards(2, 3, "player")):
            return "player"
        elif(hasMultipleCards(2, 3, "bot")):
            return "bot"
        elif(hasMultipleCards('A', 2, "player")):
            return "player"
        elif(hasMultipleCards('A', 2, "bot")):
            return "bot"
        elif(hasMultipleCards('K', 2, "player")):
            return "player"
        elif(hasMultipleCards('K', 2, "bot")):
            return "bot"
        elif(hasMultipleCards('Q', 2, "player")):
            return "player"
        elif(hasMultipleCards('Q', 2, "bot")):
            return "bot"
        elif(hasMultipleCards('J', 2, "player")):
            return "player"
        elif(hasMultipleCards('J', 2, "bot")):
            return "bot"
        elif(hasMultipleCards(10, 2, "player")):
            return "player"
        elif(hasMultipleCards(10, 2, "bot")):
            return "bot"
        elif(hasMultipleCards(9, 2, "player")):
            return "player"
        elif(hasMultipleCards(9, 2, "bot")):
            return "bot"
        elif(hasMultipleCards(8, 2, "player")):
            return "player"
        elif(hasMultipleCards(8, 2, "bot")):
            return "bot"
        elif(hasMultipleCards(7, 2, "player")):
            return "player"
        elif(hasMultipleCards(7, 2, "bot")):
            return "bot"
        elif(hasMultipleCards(6, 2, "player")):
            return "player"
        elif(hasMultipleCards(6, 2, "bot")):
            return "bot"
        elif(hasMultipleCards(5, 2, "player")):
            return "player"
        elif(hasMultipleCards(5, 2, "bot")):
            return "bot"
        elif(hasMultipleCards(4, 2, "player")):
            return "player"
        elif(hasMultipleCards(4, 2, "bot")):
            return "bot"
        elif(hasMultipleCards(3, 2, "player")):
            return "player"
        elif(hasMultipleCards(3, 2, "bot")):
            return "bot"
        elif(hasMultipleCards(2, 2, "player")):
            return "player"
        elif(hasMultipleCards(2, 2, "bot")):
            return "bot"
        elif(highestCardNum("player") > highestCardNum("bot")):
            return "player"
        elif(highestCardNum("player") < highestCardNum("bot")):
            return "bot"
        else:
            if(highestCardNum("player", 2) > highestCardNum("bot", 2)):
                return "player"
            elif(highestCardNum("player", 2) < highestCardNum("bot", 2)):
                return "bot"
            else:
                if(highestCardNum("player", 3) > highestCardNum("bot", 3)):
                    return "player"
                elif(highestCardNum("player", 3) < highestCardNum("bot", 3)):
                    return "bot"
                else:
                    if(highestCardNum("player", 4) > highestCardNum("bot", 4)):
                        return "player"
                    elif(highestCardNum("player", 4) < highestCardNum("bot", 4)):
                        return "bot"
                    else:
                        if(highestCardNum("player", 5) > highestCardNum("bot", 5)):
                            return "player"
                        elif(highestCardNum("player", 5) < highestCardNum("bot", 5)):
                            return "bot"
                        else:
                            return "tie"
    elif(hasFlush("player") and not hasFlush("bot")):
        return "player"
    elif((not hasFlush("player")) and hasFlush("bot")):
        return "bot"
    elif(hasFlush("player") and hasFlush("bot")):
        if(highestCardNum("player") > highestCardNum("bot")):
            return "player"
        elif(highestCardNum("player") < highestCardNum("bot")):
            return "bot"
        else:
            if(highestCardNum("player", 2) > highestCardNum("bot", 2)):
                return "player"
            elif(highestCardNum("player", 2) < highestCardNum("bot", 2)):
                return "bot"
            else:
                if(highestCardNum("player", 3) > highestCardNum("bot", 3)):
                    return "player"
                elif(highestCardNum("player", 3) < highestCardNum("bot", 3)):
                    return "bot"
                else:
                    if(highestCardNum("player", 4) > highestCardNum("bot", 4)):
                        return "player"
                    elif(highestCardNum("player", 4) < highestCardNum("bot", 4)):
                        return "bot"
                    else:
                        if(highestCardNum("player", 5) > highestCardNum("bot", 5)):
                            return "player"
                        elif(highestCardNum("player", 5) < highestCardNum("bot", 5)):
                            return "bot"
                        else:
                            return "tie"
    elif(hasStraight("player") and not hasStraight("bot")):
        return "player"
    elif((not hasStraight("player")) and hasStraight("bot")):
        return "bot"
    elif(hasStraight("player") and hasStraight("bot")):
        if(highestCardNum("player") > highestCardNum("bot")):
            return "player"
        elif(highestCardNum("player") < highestCardNum("bot")):
            return "bot"
        else:
            if(highestCardNum("player", 2) > highestCardNum("bot", 2)):
                return "player"
            elif(highestCardNum("player", 2) < highestCardNum("bot", 2)):
                return "bot"
            else:
                if(highestCardNum("player", 3) > highestCardNum("bot", 3)):
                    return "player"
                elif(highestCardNum("player", 3) < highestCardNum("bot", 3)):
                    return "bot"
                else:
                    if(highestCardNum("player", 4) > highestCardNum("bot", 4)):
                        return "player"
                    elif(highestCardNum("player", 4) < highestCardNum("bot", 4)):
                        return "bot"
                    else:
                        if(highestCardNum("player", 5) > highestCardNum("bot", 5)):
                            return "player"
                        elif(highestCardNum("player", 5) < highestCardNum("bot", 5)):
                            return "bot"
                        else:
                            return "tie"
    elif(hasThreeOfKind("player") and not hasThreeOfKind("bot")):
        return "player"
    elif((not hasThreeOfKind("player")) and hasThreeOfKind("bot")):
        return "bot"
    elif(hasThreeOfKind("player") and hasThreeOfKind("bot")):
        if(hasMultipleCards('A', 3, "player")):
            return "player"
        elif(hasMultipleCards('A', 3, "bot")):
            return "bot"
        elif(hasMultipleCards('K', 3, "player")):
            return "player"
        elif(hasMultipleCards('K', 3, "bot")):
            return "bot"
        elif(hasMultipleCards('Q', 3, "player")):
            return "player"
        elif(hasMultipleCards('Q', 3, "bot")):
            return "bot"
        elif(hasMultipleCards('J', 3, "player")):
            return "player"
        elif(hasMultipleCards('J', 3, "bot")):
            return "bot"
        elif(hasMultipleCards(10, 3, "player")):
            return "player"
        elif(hasMultipleCards(10, 3, "bot")):
            return "bot"
        elif(hasMultipleCards(9, 3, "player")):
            return "player"
        elif(hasMultipleCards(9, 3, "bot")):
            return "bot"
        elif(hasMultipleCards(8, 3, "player")):
            return "player"
        elif(hasMultipleCards(8, 3, "bot")):
            return "bot"
        elif(hasMultipleCards(7, 3, "player")):
            return "player"
        elif(hasMultipleCards(7, 3, "bot")):
            return "bot"
        elif(hasMultipleCards(6, 3, "player")):
            return "player"
        elif(hasMultipleCards(6, 3, "bot")):
            return "bot"
        elif(hasMultipleCards(5, 3, "player")):
            return "player"
        elif(hasMultipleCards(5, 3, "bot")):
            return "bot"
        elif(hasMultipleCards(4, 3, "player")):
            return "player"
        elif(hasMultipleCards(4, 3, "bot")):
            return "bot"
        elif(hasMultipleCards(3, 3, "player")):
            return "player"
        elif(hasMultipleCards(3, 3, "bot")):
            return "bot"
        elif(hasMultipleCards(2, 3, "player")):
            return "player"
        elif(hasMultipleCards(2, 3, "bot")):
            return "bot"
        elif(highestCardNum("player") > highestCardNum("bot")):
            return "player"
        elif(highestCardNum("player") < highestCardNum("bot")):
            return "bot"
        else:
            if(highestCardNum("player", 2) > highestCardNum("bot", 2)):
                return "player"
            elif(highestCardNum("player", 2) < highestCardNum("bot", 2)):
                return "bot"
            else:
                if(highestCardNum("player", 3) > highestCardNum("bot", 3)):
                    return "player"
                elif(highestCardNum("player", 3) < highestCardNum("bot", 3)):
                    return "bot"
                else:
                    if(highestCardNum("player", 4) > highestCardNum("bot", 4)):
                        return "player"
                    elif(highestCardNum("player", 4) < highestCardNum("bot", 4)):
                        return "bot"
                    else:
                        if(highestCardNum("player", 5) > highestCardNum("bot", 5)):
                            return "player"
                        elif(highestCardNum("player", 5) < highestCardNum("bot", 5)):
                            return "bot"
                        else:
                            return "tie"
    elif(hasTwoPair("player") and not hasTwoPair("bot")):
        return "player"
    elif((not hasTwoPair("player")) and hasTwoPair("bot")):
        return "bot"
    elif(hasTwoPair("player") and hasPair("bot")):
        if(hasMultipleCards('A', 2, "player") and not(hasMultipleCards('A', 2, "bot"))):
            return "player"
        elif((not hasMultipleCards('A', 2, "player")) and hasMultipleCards('A', 2, "bot")):
            return "bot"
        elif(hasMultipleCards('K', 2, "player") and not(hasMultipleCards('K', 2, "bot"))):
            return "player"
        elif((not hasMultipleCards('K', 2, "player")) and hasMultipleCards('K', 2, "bot")):
            return "bot"
        elif(hasMultipleCards('Q', 2, "player") and not(hasMultipleCards('Q', 2, "bot"))):
            return "player"
        elif((not hasMultipleCards('Q', 2, "player")) and hasMultipleCards('Q', 2, "bot")):
            return "bot"
        elif(hasMultipleCards('J', 2, "player") and not(hasMultipleCards('J', 2, "bot"))):
            return "player"
        elif((not hasMultipleCards('J', 2, "player")) and hasMultipleCards('J', 2, "bot")):
            return "bot"
        elif(hasMultipleCards(10, 2, "player") and not(hasMultipleCards(10, 2, "bot"))):
            return "player"
        elif((not hasMultipleCards(10, 2, "player")) and hasMultipleCards(10, 2, "bot")):
            return "bot"
        elif(hasMultipleCards(9, 2, "player") and not(hasMultipleCards(9, 2, "bot"))):
            return "player"
        elif((not hasMultipleCards(9, 2, "player")) and hasMultipleCards(9, 2, "bot")):
            return "bot"
        elif(hasMultipleCards(8, 2, "player") and not(hasMultipleCards(8, 2, "bot"))):
            return "player"
        elif((not hasMultipleCards(8, 2, "player")) and hasMultipleCards(8, 2, "bot")):
            return "bot"
        elif(hasMultipleCards(7, 2, "player") and not(hasMultipleCards(7, 2, "bot"))):
            return "player"
        elif((not hasMultipleCards(7, 2, "player")) and hasMultipleCards(7, 2, "bot")):
            return "bot"
        elif(hasMultipleCards(6, 2, "player") and not(hasMultipleCards(6, 2, "bot"))):
            return "player"
        elif((not hasMultipleCards(6, 2, "player")) and hasMultipleCards(6, 2, "bot")):
            return "bot"
        elif(hasMultipleCards(5, 2, "player") and not(hasMultipleCards(5, 2, "bot"))):
            return "player"
        elif((not hasMultipleCards(5, 2, "player")) and hasMultipleCards(5, 2, "bot")):
            return "bot"
        elif(hasMultipleCards(4, 2, "player") and not(hasMultipleCards(4, 2, "bot"))):
            return "player"
        elif((not hasMultipleCards(4, 2, "player")) and hasMultipleCards(4, 2, "bot")):
            return "bot"
        elif(hasMultipleCards(3, 2, "player") and not(hasMultipleCards(3, 2, "bot"))):
            return "player"
        elif((not hasMultipleCards(3, 2, "player")) and hasMultipleCards(3, 2, "bot")):
            return "bot"
        elif(hasMultipleCards(2, 2, "player") and not(hasMultipleCards(2, 2, "bot"))):
            return "player"
        elif((not hasMultipleCards(2, 2, "player")) and hasMultipleCards(2, 2, "bot")):
            return "bot"
        elif(highestCardNum("player") > highestCardNum("bot")):
            return "player"
        elif(highestCardNum("player") < highestCardNum("bot")):
            return "bot"
        else:
            if(highestCardNum("player", 2) > highestCardNum("bot", 2)):
                return "player"
            elif(highestCardNum("player", 2) < highestCardNum("bot", 2)):
                return "bot"
            else:
                if(highestCardNum("player", 3) > highestCardNum("bot", 3)):
                    return "player"
                elif(highestCardNum("player", 3) < highestCardNum("bot", 3)):
                    return "bot"
                else:
                    if(highestCardNum("player", 4) > highestCardNum("bot", 4)):
                        return "player"
                    elif(highestCardNum("player", 4) < highestCardNum("bot", 4)):
                        return "bot"
                    else:
                        if(highestCardNum("player", 5) > highestCardNum("bot", 5)):
                            return "player"
                        elif(highestCardNum("player", 5) < highestCardNum("bot", 5)):
                            return "bot"
                        else:
                            return "tie"
    elif(hasPair("player") and not hasPair("bot")):
        return "player"
    elif((not hasPair("player")) and hasPair("bot")):
        return("bot")
    elif(hasPair("player") and hasPair("bot")):
        if(hasMultipleCards('A', 2, "player")):
            return "player"
        elif(hasMultipleCards('A', 2, "bot")):
            return "bot"
        elif(hasMultipleCards('K', 2, "player")):
            return "player"
        elif(hasMultipleCards('K', 2, "bot")):
            return "bot"
        elif(hasMultipleCards('Q', 2, "player")):
            return "player"
        elif(hasMultipleCards('Q', 2, "bot")):
            return "bot"
        elif(hasMultipleCards('J', 2, "player")):
            return "player"
        elif(hasMultipleCards('J', 2, "bot")):
            return "bot"
        elif(hasMultipleCards(10, 2, "player")):
            return "player"
        elif(hasMultipleCards(10, 2, "bot")):
            return "bot"
        elif(hasMultipleCards(9, 2, "player")):
            return "player"
        elif(hasMultipleCards(9, 2, "bot")):
            return "bot"
        elif(hasMultipleCards(8, 2, "player")):
            return "player"
        elif(hasMultipleCards(8, 2, "bot")):
            return "bot"
        elif(hasMultipleCards(7, 2, "player")):
            return "player"
        elif(hasMultipleCards(7, 2, "bot")):
            return "bot"
        elif(hasMultipleCards(6, 2, "player")):
            return "player"
        elif(hasMultipleCards(6, 2, "bot")):
            return "bot"
        elif(hasMultipleCards(5, 2, "player")):
            return "player"
        elif(hasMultipleCards(5, 2, "bot")):
            return "bot"
        elif(hasMultipleCards(4, 2, "player")):
            return "player"
        elif(hasMultipleCards(4, 2, "bot")):
            return "bot"
        elif(hasMultipleCards(3, 2, "player")):
            return "player"
        elif(hasMultipleCards(3, 2, "bot")):
            return "bot"
        elif(hasMultipleCards(2, 2, "player")):
            return "player"
        elif(hasMultipleCards(2, 2, "bot")):
            return "bot"
        elif(highestCardNum("player") > highestCardNum("bot")):
            return "player"
        elif(highestCardNum("player") < highestCardNum("bot")):
            return "bot"
        else:
            if(highestCardNum("player", 2) > highestCardNum("bot", 2)):
                return "player"
            elif(highestCardNum("player", 2) < highestCardNum("bot", 2)):
                return "bot"
            else:
                if(highestCardNum("player", 3) > highestCardNum("bot", 3)):
                    return "player"
                elif(highestCardNum("player", 3) < highestCardNum("bot", 3)):
                    return "bot"
                else:
                    if(highestCardNum("player", 4) > highestCardNum("bot", 4)):
                        return "player"
                    elif(highestCardNum("player", 4) < highestCardNum("bot", 4)):
                        return "bot"
                    else:
                        if(highestCardNum("player", 5) > highestCardNum("bot", 5)):
                            return "player"
                        elif(highestCardNum("player", 5) < highestCardNum("bot", 5)):
                            return "bot"
                        else:
                            return "tie"
    else:
        if(highestCardNum("player") > highestCardNum("bot")):
            return "player"
        elif(highestCardNum("player") < highestCardNum("bot")):
            return "bot"
        else:
            if(highestCardNum("player", 2) > highestCardNum("bot", 2)):
                return "player"
            elif(highestCardNum("player", 2) < highestCardNum("bot", 2)):
                return "bot"
            else:
                if(highestCardNum("player", 3) > highestCardNum("bot", 3)):
                    return "player"
                elif(highestCardNum("player", 3) < highestCardNum("bot", 3)):
                    return "bot"
                else:
                    if(highestCardNum("player", 4) > highestCardNum("bot", 4)):
                        return "player"
                    elif(highestCardNum("player", 4) < highestCardNum("bot", 4)):
                        return "bot"
                    else:
                        if(highestCardNum("player", 5) > highestCardNum("bot", 5)):
                            return "player"
                        elif(highestCardNum("player", 5) < highestCardNum("bot", 5)):
                            return "bot"
                        else:
                            return "tie"



def highestCardNum(a, _higestNum = 1):
    global playerCards
    global botCards
    numsToSort = []
    
    if(a == "player"):
        for i in range(5):
            if(playerCards[i][0] == 'A'):
                numsToSort.append(14)
            elif(playerCards[i][0] == 'K'):
                numsToSort.append(13)
            elif(playerCards[i][0] == 'Q'):
                numsToSort.append(12)
            elif(playerCards[i][0] == 'J'):
                numsToSort.append(11)
            else:
                numsToSort.append(playerCards[i][0])
        return (sort(numsToSort))[5-_higestNum]
    else:
        for i in range(5):
            if(botCards[i][0] == 'A'):
                numsToSort.append(14)
            elif(botCards[i][0] == 'K'):
                numsToSort.append(13)
            elif(botCards[i][0] == 'Q'):
                numsToSort.append(12)
            elif(botCards[i][0] == 'J'):
                numsToSort.append(11)
            else:
                numsToSort.append(botCards[i][0])
        return (sort(numsToSort))[5-_higestNum]

def botsTradeAmount():
    global botCards
    
    if(hasStraight("bot") or hasFlush("bot") or (hasFourOfKind("bot") and hasCard("bot", 'A')) or hasFullHouse("bot")):
        return 0
    elif(hasFourOfKind("bot") or hasTwoPair("bot")):
        return 1
    elif(hasThreeOfKind("bot")):
        return 2
    elif(hasPair("bot")):
        return 3
    elif(hasCard("bot", 'A')):
        return 4 
    elif(hasAlmostFlush("bot")):
        return 1
    else:
        return 3
        
def hasAlmostFlush(a):
    global botCards
    global playerCards
    
    if(a == "player"):
        if((playerCards[0][1] == playerCards[1][1] and playerCards[1][1] == playerCards[2][1] and playerCards[2][1] == playerCards[3][1]) or (playerCards[0][1] == playerCards[1][1] and playerCards[1][1] == playerCards[2][1] and playerCards[2][1] == playerCards[4][1]) or (playerCards[0][1] == playerCards[1][1] and playerCards[1][1] == playerCards[3][1] and playerCards[3][1] == playerCards[4][1]) or (playerCards[0][1] == playerCards[2][1] and playerCards[2][1] == playerCards[3][1] and playerCards[3][1] == playerCards[4][1]) or (playerCards[1][1] == playerCards[2][1] and playerCards[2][1] == playerCards[3][1] and playerCards[3][1] == playerCards[4][1])):
            return True
        else:
            return False
    else:
        if((botCards[0][1] == botCards[1][1] and botCards[1][1] == botCards[2][1] and botCards[2][1] == botCards[3][1]) or (botCards[0][1] == botCards[1][1] and botCards[1][1] == botCards[2][1] and botCards[2][1] == botCards[4][1]) or (botCards[0][1] == botCards[1][1] and botCards[1][1] == botCards[3][1] and botCards[3][1] == botCards[4][1]) or (botCards[0][1] == botCards[2][1] and botCards[2][1] == botCards[3][1] and botCards[3][1] == botCards[4][1]) or (botCards[1][1] == botCards[2][1] and botCards[2][1] == botCards[3][1] and botCards[3][1] == botCards[4][1])):
            return True
        else:
            return False
    
def sort(array):
    newArray = []
    array = arrayDestroyer(array)
    while(True):
        if(array[0]<array[1] and array[1]<array[2] and array[2]<array[3] and array[3]<array[4]):
            break
        else:
            array = arrayDestroyer(array)
    return array

def arrayDestroyer(array):
    newArray = []
    rk = False
    
    for i in range(5):
        theNum = random.randrange(0, len(array))
        newArray.append(array[theNum])
        array.remove(array[theNum])
        rk = True
    return newArray
    

main()
