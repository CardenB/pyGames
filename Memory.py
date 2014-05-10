# implementation of card game - Memory

import lib.simpleguitk.simpleguitk as simplegui
import random
import math

#keep track of the number of turns used to discover all cards
TURN_COUNT = 0
#number range of cards
cardRange = range(8)
#global list for deck of cards
deck = []
#global list for cards that have been exposed
exposed = []
STATE_NUM = 0
#last card that was exposed
last_exposed = [None, None]

#size of each card
CARD_WIDTH = 50
CARD_HEIGHT = 100

#size of the card numbers
TEXT_SIZE = 50

def shuffleDeck():
    global deck
    random.shuffle(deck)
    
# helper function to initialize globals
def new_game():
    global deck, TURN_COUNT, exposed
    
    #reset turn count
    TURN_COUNT = 0
    
    #clear the deck
    deck = []
    exposed = []
    
    #Add cards in [0, 8) to the deck two times
    random.shuffle(cardRange)
    deck.extend(cardRange)
    random.shuffle(cardRange)
    deck.extend(cardRange)
    
    #fill out the list of exposed cards, set to false
    for card in deck:
        exposed.append(False)
    
    #shuffle the deck
    shuffleDeck()
     
# define event handlers
def mouseclick(pos):
    global exposed, STATE_NUM, last_exposed, TURN_COUNT
    
    card_index = int(math.floor(pos[0]/CARD_WIDTH))
    #make sure you aren't clicking on an exposed card
    if exposed[card_index]:
        return
    
    #expose new card
    exposed[card_index] = True
    
    if STATE_NUM == 0:
        last_exposed[STATE_NUM] = card_index
        STATE_NUM = 1
        
    elif STATE_NUM == 1:
        last_exposed[STATE_NUM] = card_index
        TURN_COUNT += 1
        STATE_NUM = 2

    elif STATE_NUM == 2:
        if deck[last_exposed[0]] == deck[last_exposed[1]]:
            #if match, leave cards exposed, reset last pair
            last_exposed = [card_index, None]
        else:
            #if last exposed pair are not matched
            exposed[last_exposed[0]] = False
            exposed[last_exposed[1]] = False
            last_exposed = [card_index, None]
        
        STATE_NUM = 1

def get_card_midpoint(card, text_width, cardInt):
    x = CARD_WIDTH*(cardInt + 0.5) - text_width/2
    y = CARD_HEIGHT/2 + TEXT_SIZE/2
    return (x, y)
                        
def draw_card_back(canvas, card_index):
    card_left_x = CARD_WIDTH*card_index
    card_right_x = card_left_x + CARD_WIDTH
    
    top_left = (card_left_x, 0)
    top_right = (card_right_x, 0)
    bottom_left = (card_left_x, CARD_HEIGHT)
    bottom_right = (card_right_x, CARD_HEIGHT)
    
    point_list = [top_left, bottom_left, bottom_right, top_right]
    line_width = 10
    line_color = "Brown"
    fill_color = "Green"
    
    canvas.draw_polygon(point_list, line_width, line_color, fill_color)
    
    
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global label
    label.set_text("Turns = " + str(TURN_COUNT))
    for i in range(len(deck)):
        if exposed[i]:
            card = str(deck[i])
            textWidth = frame.get_canvas_textwidth(card, TEXT_SIZE)
        
            point = get_card_midpoint(card, textWidth, i)
            canvas.draw_text(str(deck[i]), point, TEXT_SIZE, 'White')
            
        elif not exposed[i]:
            draw_card_back(canvas, i)
            
    if all(exposed_card == True for exposed_card in exposed):# and STATE_NUM == 1:
        you_win = "YOU WIN!"
        you_win_coord_x = (CARD_WIDTH*len(deck) - frame.get_canvas_textwidth(you_win, CARD_HEIGHT))/2
        you_win_coord_y = CARD_HEIGHT
        you_win_coord = (you_win_coord_x, you_win_coord_y)
        canvas.draw_text(you_win, you_win_coord, CARD_HEIGHT, 'Red')
    
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", CARD_WIDTH*16, CARD_HEIGHT)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

new_game()

# Always remember to review the grading rubric
