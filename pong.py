# classic arcade game Pong

import simplegui
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
POS_SHIFT = HALF_PAD_HEIGHT + BALL_RADIUS

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2,HEIGHT/2]
    ball_vel = [0,0]
    if direction:
        balldir = 1
    else:
        balldir = -1
    ball_vel[0] = balldir * random.randrange(120, 240) // 60
    ball_vel[1] = -random.randrange(60, 180)  // 60

# update ball position and scores
def update_ball_pos():
    global score_left,score_right

    # update ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # when ball hits the horizontal borders
    if (ball_pos[1] >= (HEIGHT-1) - BALL_RADIUS) or (ball_pos[1] <= BALL_RADIUS):
        ball_vel[1] = - ball_vel[1]

    # when ball hits the vertical borders
    # when ball hits the right gutter
    elif (ball_pos[0] >= (WIDTH-PAD_WIDTH-1) - BALL_RADIUS):
        # when ball hits the gutter
        if (ball_pos[1] <= paddle2_pos[1]+POS_SHIFT) and (ball_pos[1] >= paddle2_pos[1]-POS_SHIFT):
            ball_vel[0] = - ball_vel[0] * 1.1
            ball_vel[1] = ball_vel[1] * 1.1
        else:
            score_left = score_left + 1
            spawn_ball(LEFT)

    # when ball hits the left gutter
    elif(ball_pos[0] <= BALL_RADIUS + PAD_WIDTH):
        # when ball hits the gutter
        if (ball_pos[1] <= paddle1_pos[1]+POS_SHIFT) and (ball_pos[1] >= paddle1_pos[1]-POS_SHIFT):
            ball_vel[0] = - ball_vel[0] * 1.1
            ball_vel[1] = ball_vel[1] * 1.1
        else:
            score_right = score_right + 1
            spawn_ball(RIGHT)

# update paddle position when hitting the horizontal borders
def paddle_pos_check(paddle_pos):
    # when paddle hits the upper border
    if paddle_pos <= HALF_PAD_HEIGHT:
        paddle_pos = HALF_PAD_HEIGHT

    # when paddle hits the bottom border
    elif paddle_pos >= HEIGHT-1-HALF_PAD_HEIGHT:
        paddle_pos = HEIGHT-1-HALF_PAD_HEIGHT

    return paddle_pos

# update paddle position
def update_paddle_pos():

    # update position based on vertical velocity
    paddle1_pos[1] += paddle1_vel[1]
    paddle2_pos[1] += paddle2_vel[1]

    # when left paddle hits the horizontal borders
    paddle1_pos[1] = paddle_pos_check(paddle1_pos[1])

    # when right paddle hits the horizontal borders
    paddle2_pos[1] = paddle_pos_check(paddle2_pos[1])

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    global score_left, score_right
    score_left = 0
    score_right = 0
    paddle1_pos = [HALF_PAD_WIDTH,HEIGHT/2]
    paddle2_pos = [WIDTH-1-HALF_PAD_WIDTH,HEIGHT/2]
    paddle1_vel = [0,0]
    paddle2_vel = [0,0]
    # initialize the game with random direction
    spawn_ball(random.choice([LEFT,RIGHT]))

def reset():
    new_game()

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel

    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update ball
    update_ball_pos()

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS,2, 'White','White')

    # update paddle's vertical position, keep paddle on the screen
    update_paddle_pos()

    # draw paddles
    # draw left-side paddle
    paddle_left1 = [0,paddle1_pos[1]-HALF_PAD_HEIGHT]
    paddle_left2 = [PAD_WIDTH,paddle1_pos[1]-HALF_PAD_HEIGHT]
    paddle_left3 = [PAD_WIDTH,paddle1_pos[1]+HALF_PAD_HEIGHT]
    paddle_left4 = [0,paddle1_pos[1]+HALF_PAD_HEIGHT]
    canvas.draw_polygon([paddle_left1,paddle_left2,paddle_left3,paddle_left4], 1, 'White', 'White')

    # draw right-side paddle
    paddle_right1 = [WIDTH-PAD_WIDTH,paddle2_pos[1]-HALF_PAD_HEIGHT]
    paddle_right2 = [WIDTH,paddle2_pos[1]-HALF_PAD_HEIGHT]
    paddle_right3 = [WIDTH,paddle2_pos[1]+HALF_PAD_HEIGHT]
    paddle_right4 = [WIDTH-PAD_WIDTH,paddle2_pos[1]+HALF_PAD_HEIGHT]
    canvas.draw_polygon([paddle_right1,paddle_right2,paddle_right3,paddle_right4], 1, 'White', 'White')

    # draw scores
    canvas.draw_text(str(score_left), (150, 100), 50, 'White')
    canvas.draw_text(str(score_right), (420, 100), 50, 'White')

def keydown(key):
    global paddle1_vel, paddle2_vel
    vel = 5
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel[1] -= vel
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel[1] += vel
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel[1] -= vel
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel[1] += vel

def keyup(key):
    global paddle1_vel, paddle2_vel
    # when key w or s is up
    if (key == simplegui.KEY_MAP["w"]) or (key == simplegui.KEY_MAP["s"]):
        paddle1_vel[1] = 0
    # when key up or down is up
    if (key == simplegui.KEY_MAP["up"]) or (key == simplegui.KEY_MAP["down"]):
        paddle2_vel[1] = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.add_label('The game: PONG')
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
reset_button = frame.add_button('reset PONG', reset, 200)

# start frame
new_game()
frame.start()
