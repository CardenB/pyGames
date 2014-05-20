# Mini-project #6 - Blackjack

import simpleguitk as simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = [73, 98]
CARD_CENTER = [36.5, 49]
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = [71, 96]
CARD_BACK_CENTER = [35.5, 48]
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
playerPrompt = "Hit or Stand?"
score = 0
gameDeck = None
playerHand = None
dealerHand = None
playerBust = "Player Bust."
dealerBust = "Dealer Bust."
playerWin = "Player Wins!"
dealerWin = "Dealer Wins!"
drawOutcome = "It's a draw!"
playerScore = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
            self.show_back = False
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):

        if self.show_back:
            card_loc = [CARD_BACK_CENTER[0], CARD_BACK_CENTER[1]]
            canvas.draw_image(card_back, card_loc, CARD_BACK_SIZE, [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
        else:
            card_loc = [CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                        CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit)]
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cardList = []

    def __str__(self):
        return "".join(str(card) + ", " for card in self.cardList)

    def add_card(self, card):
        self.cardList.append(card)

    def get_value(self):
        value = 0
        aceCount = 0
        for card in self.cardList:
            rank = card.get_rank()
            if rank == 'A':
                value += VALUES[card.get_rank()]
                aceCount += 1
            else:
                value += VALUES[card.get_rank()]
        for i in range(aceCount):
            tempValue = value + 10
            if tempValue <= 21:
                value = tempValue
        return value
   
    def draw(self, canvas, pos):
        for i in range(len(self.cardList)):
            cardPos = []
            cardSize = CARD_SIZE
            cardCenter = CARD_CENTER
            if self.cardList[i].show_back:
                cardSize = CARD_BACK_SIZE
                cardCenter = CARD_BACK_CENTER
            cardPos = [pos[0] + i*(cardSize[0] + cardCenter[0]), pos[1]]
            self.cardList[i].draw(canvas, cardPos)
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.cardList = []
        for suit in SUITS:
            for rank in RANKS:
                self.cardList.append(Card(suit, rank))

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.cardList)

    def deal_card(self):
        return self.cardList.pop()
    
    def __str__(self):
        return "".join(str(card) + ", " for card in self.cardList)



#define event handlers for buttons
def deal():
    global outcome, in_play, gameDeck, playerHand, dealerHand, playerScore

    # your code goes here
    
    if in_play:
        playerScore -= 1
        
    in_play = True
    outcome = ""
    playerPrompt = "Hit or Stand?"
    gameDeck = Deck()
    gameDeck.shuffle()
    
    dealerHand = Hand()
    playerHand = Hand()
    
    firstDealerCard = gameDeck.deal_card()
    firstDealerCard.show_back = True
    
    dealerHand.add_card( firstDealerCard )
    dealerHand.add_card( gameDeck.deal_card())
    playerHand.add_card( gameDeck.deal_card())
    playerHand.add_card( gameDeck.deal_card())
    
def decideOutcome():
    global outcome, in_play, playerHand, dealerHand, playerScore
    # assign a message to outcome, update in_play and score
    if playerHand.get_value() <= 21 and playerHand.get_value() > dealerHand.get_value():
        outcome = playerWin
        playerScore += 1
    elif dealerHand.get_value() <= 21 and dealerHand.get_value() > playerHand.get_value():
        outcome = dealerWin
        playerScore -= 1
        
    if playerHand.get_value() > 21:
        outcome = playerBust + " " + dealerWin
        playerScore -= 1
       
    elif dealerHand.get_value() > 21:
        outcome = dealerBust + " " + playerWin
        playerScore += 1
    
    if playerHand.get_value() == dealerHand.get_value():
        outcome = drawOutcome
        
    in_play = False

def hit():
    global outcome, in_play, gameDeck, playerHand, dealerHand
 
    # if the hand is in play, hit the player
    if in_play:
        playerHand.add_card( gameDeck.deal_card() )
    # if busted, assign a message to outcome, update in_play and score
    if playerHand.get_value() > 21:
        decideOutcome()
       
def stand():
    global outcome, in_play, gameDeck, playerHand, dealerHand
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while dealerHand.get_value() < 17:
            dealerHand.add_card( gameDeck.deal_card() )
        for card in dealerHand.cardList:
            if card.show_back:
                card.show_back = False
    decideOutcome()
        
# draw handler    
def draw(canvas):
    global outcome, playerPrompt, playerScore
    FONT_SIZE = 40
    # test to make sure that card.draw works, replace with your code below
    dealerHand.draw(canvas, [100, 3*600/6 - CARD_SIZE[1] ])
    playerHand.draw(canvas, [100, 5*600/6 - CARD_SIZE[1] ])
    canvas.draw_text("Dealer", [100, 3*600/6 - CARD_SIZE[1] - int(FONT_SIZE*0.5) ], FONT_SIZE, "Black")
    canvas.draw_text("Player", [100, 5*600/6 - CARD_SIZE[1] - int(FONT_SIZE*0.5) ], FONT_SIZE, "Black")
    if in_play:
        playerPrompt = "Hit or Stand?"
    else:
        playerPrompt = "New Deal?"

    canvas.draw_text(playerPrompt, [300, 5*600/6 - CARD_SIZE[1] - int(FONT_SIZE*0.5) ], FONT_SIZE, "Black")
    canvas.draw_text(outcome, [300, 3*600/6 - CARD_SIZE[1] - int(FONT_SIZE*0.5) ], FONT_SIZE, "Black")        
    canvas.draw_text("Score: " + str(playerScore), [600, 0 + int(FONT_SIZE*1.5) ], int(FONT_SIZE*1.25), "Black")
    canvas.draw_text( "Blackjack", [100, 0 + int(FONT_SIZE*1.5) ], int(FONT_SIZE*1.5), "Blue")

    
def printStatus():
    global outcome, in_play, gameDeck, playerHand, dealerHand
    
    status = "dealerHand: " + str(dealerHand) + str(dealerHand.get_value()) + \
    ",\nplayerHand: " + str(playerHand) + str(playerHand.get_value()) + \
    ",\noutcome: " + outcome
    print status

# initialization frame
frame = simplegui.create_frame("Blackjack", 900, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()
