# Implementation of classic arcade game Pong

import simpleguitk as simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 15
PAD_WIDTH = 8
PAD_HEIGHT = 80
score1=score2=0
paddle1_vel = 0
paddle2_vel = 0
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [0,0]

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_vel = [0,0]
    ball_pos = [WIDTH/2, HEIGHT/2]
    
    if direction == RIGHT:
        ball_vel = [random.randrange(90,180)/60, -random.randrange(60,120)/60]
    else:
        ball_vel = [-random.randrange(90,180)/60, -random.randrange(60,120)/60]

    

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    score1 = 0
    score2 = 0
    
    paddle1_pos = HEIGHT/ 2
    paddle2_pos = HEIGHT/ 2
    
    paddle1_vel = 0
    paddle2_vel = 0
    r=random.randrange(2)
    if r==0:
        spawn_ball(LEFT)
    else:
        spawn_ball(RIGHT)
    
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global paddle1_vel, paddle2_vel        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] = ball_pos[0] + ball_vel[0]
    ball_pos[1] = ball_pos[1] + ball_vel[1]
        
    """If the ball touches the ceiling and floor"""
    if ball_pos[1]<=(BALL_RADIUS+5) or ball_pos[1]>=HEIGHT-(BALL_RADIUS+5):
        ball_vel[1]=-ball_vel[1]


    
    """If the ball touches the gutters or padel"""
    if (ball_pos[1]<=(paddle1_pos-HALF_PAD_HEIGHT) or ball_pos[1]>=(paddle1_pos+HALF_PAD_HEIGHT)) and ball_pos[0]<=(BALL_RADIUS+PAD_WIDTH+8):
        score2+=1
        spawn_ball(RIGHT)
    if (ball_pos[1]<=(paddle2_pos-HALF_PAD_HEIGHT) or ball_pos[1]>=(paddle2_pos+HALF_PAD_HEIGHT)) and ball_pos[0]>=WIDTH-(BALL_RADIUS+PAD_WIDTH+8):
        score1+=1
        spawn_ball(LEFT)

    if ball_pos[0]<=(BALL_RADIUS+PAD_WIDTH+8) or ball_pos[0]>=WIDTH-(BALL_RADIUS+PAD_WIDTH+8):
        ball_vel[0]=-ball_vel[0]

    
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 12, "white", "white")
    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos < (HALF_PAD_HEIGHT) and paddle1_vel < 0:
        paddle1_vel = 0
    elif paddle1_pos > (HEIGHT - (HALF_PAD_HEIGHT)) and paddle1_vel > 0:
        paddle1_vel = 0
    if paddle2_pos < (HALF_PAD_HEIGHT) and paddle2_vel < 0:
        paddle2_vel = 0
    elif paddle2_pos > (HEIGHT - (HALF_PAD_HEIGHT)) and paddle2_vel > 0:
        paddle2_vel = 0

    
    # draw paddles
    paddle1_pos+=paddle1_vel
    paddle2_pos+=paddle2_vel
    canvas.draw_line([0,paddle1_pos + HALF_PAD_HEIGHT], [0,paddle1_pos - HALF_PAD_HEIGHT], 18, "Red")
    canvas.draw_line([WIDTH,paddle2_pos+HALF_PAD_HEIGHT], [WIDTH,paddle2_pos - HALF_PAD_HEIGHT], 18, "Red")

    
    # draw scores
    canvas.draw_text(str(score1),[130,80],36,"White")
    canvas.draw_text(str(score2),[430,80],36,"White")

    
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -3
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 3
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -3
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 3
    
    
    
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game, 100)

# start frame
new_game()
frame.start()
