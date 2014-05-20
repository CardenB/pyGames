import simpleguitk as simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
PADDLE_VEL = 5
TEXT_WIDTH = 20

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = (WIDTH/2, HEIGHT/2)
    
    #canvas updates at 60 fps
    xvel = random.randrange(2, 5)
    yvel = random.randrange(1, 4)
    if direction:
        ball_vel = (xvel, -yvel)
    else:
        ball_vel = (-xvel, -yvel)
        
def draw_paddles(canvas):
    canvas.draw_polygon( [(paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT),
                          (paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT),
                          (paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT),
                          (paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT)],
                          1, 'White', 'White')
    
    canvas.draw_polygon( [(paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT),
                          (paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT),
                          (paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT),
                          (paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT)],
                          1, 'White', 'White')

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    spawn_ball(RIGHT)
    paddle1_pos = (HALF_PAD_WIDTH, HEIGHT/2)
    paddle2_pos = (WIDTH - HALF_PAD_WIDTH, HEIGHT/2)
    
    paddle1_vel = 0
    paddle2_vel = 0
    
    score1 = 0
    score2 = 0
    

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    new_x = ball_pos[0] + ball_vel[0]
    new_y = ball_pos[1] + ball_vel[1]
    
    paddle1Collision = new_x - BALL_RADIUS/2 + HALF_PAD_WIDTH < paddle1_pos[0] \
    and new_y < paddle1_pos[1] + HALF_PAD_HEIGHT \
    and new_y > paddle1_pos[1] - HALF_PAD_HEIGHT
    
    paddle2Collision = new_x + BALL_RADIUS/2 - HALF_PAD_WIDTH > paddle2_pos[0] \
    and new_y < paddle2_pos[1] + HALF_PAD_HEIGHT \
    and new_y > paddle2_pos[1] - HALF_PAD_HEIGHT
    
    if paddle1Collision or paddle2Collision:
        ball_vel = (-ball_vel[0]*1.1, ball_vel[1]*1.1)
        
    #keep ball within top and bottom of board
    if new_y + BALL_RADIUS > HEIGHT or new_y - BALL_RADIUS < 0:
        ball_vel = (ball_vel[0], -ball_vel[1])
    
    #check if ball goes into gutter
    if new_x > WIDTH - PAD_WIDTH and not paddle2Collision :
        spawn_ball(LEFT)
        score1 += 1
        
    elif new_x < 0 + PAD_WIDTH and not paddle1Collision:
        spawn_ball(RIGHT)
        score2 += 1
        
    else:
        ball_pos = (new_x, new_y)
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, 'White', 'White')
    
    # update paddle's vertical position, keep paddle on the screen
    new_paddle1_pos = (paddle1_pos[0], paddle1_pos[1]+paddle1_vel)
    if new_paddle1_pos[1] - HALF_PAD_HEIGHT > 0 and new_paddle1_pos[1] + HALF_PAD_HEIGHT < HEIGHT:
        paddle1_pos = new_paddle1_pos
        
    new_paddle2_pos = (paddle2_pos[0], paddle2_pos[1]+paddle2_vel)
    if new_paddle2_pos[1] - HALF_PAD_HEIGHT > 0 and new_paddle2_pos[1] + HALF_PAD_HEIGHT < HEIGHT:
        paddle2_pos = new_paddle2_pos
    
    # draw paddles
    draw_paddles(canvas)
    
    # draw scores
    
    scoreString = "Player 1: %d / Player 2: %d" % (score1, score2)
    canvas.draw_text(scoreString, 
                     (WIDTH - frame.get_canvas_textwidth(scoreString, TEXT_WIDTH) - 2*PAD_WIDTH, 
                      0 + TEXT_WIDTH), 
                      TEXT_WIDTH, 'White')
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel = PADDLE_VEL
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = -PADDLE_VEL
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = PADDLE_VEL
    elif key == simplegui.KEY_MAP['w']:
        paddle1_vel = -PADDLE_VEL
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['down'] or key == simplegui.KEY_MAP['up']:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP['s'] or key == simplegui.KEY_MAP['w']:
        paddle1_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Reset", new_game)


# start frame
new_game()
frame.start()
