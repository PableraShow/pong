# Pong

import simplegui
import random

# initialize globals, constant values (uppercase)
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
GUTTER_LEFT = PAD_WIDTH
GUTTER_RIGHT = WIDTH - PAD_WIDTH

# initialize globals
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0, 0]
paddle1_pos = 100
paddle2_pos = 100
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0
direction = 'left'


def spawn_ball(direction):
    """New ball position/velocity when its start a new game"""
    global ball_pos, ball_vel # these are vectors stored as lists

    # Ball position
    ball_pos[0] = WIDTH / 2
    ball_pos[1] = HEIGHT / 2

    # Velocity
    # if direction is right, the ball's velocity is upper right, else upper left
    if direction == 'right':
        ball_vel[0] = random.randrange(120, 240) // 60
        ball_vel[1] = - random.randrange(60, 180) // 60 # the same that: -1 * random.randrange(60, 180) // 60
    elif direction == 'left':
        ball_vel[0] = - random.randrange(60, 180) // 60 # -1 * random.randrange(60, 180) // 60
        ball_vel[1] = - random.randrange(120, 240) // 60 # -1 * random.randrange(120, 240) // 60

# Event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    spawn_ball(direction)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, direction

    # draw midle line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, 'White')
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, 'White')
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, 'White')

    # update ball
    ball_pos[0] = ball_pos[0] + ball_vel[0]
    ball_pos[1] = ball_pos[1] + ball_vel[1]

    # check collisions up and down
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1] # the same that: -1 * ball_vel[1]

    elif ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1] # -1 * ball_vel[1]

    # check paddle bounce
    if (
        (ball_pos[1] >= paddle2_pos and
        ball_pos[1] < paddle2_pos + PAD_HEIGHT and
        ball_pos[0] + BALL_RADIUS >= GUTTER_RIGHT)
        or 
        (ball_pos[1] >= paddle1_pos and
        ball_pos[1] < paddle1_pos + PAD_HEIGHT and
        ball_pos[0] - BALL_RADIUS <= GUTTER_LEFT)
        ):
        ball_vel[0] = -1.1 * ball_vel[0] # with -1.1 we are incrementing the ball velocity before impact with the paddle

    # goal to player 2
    elif ball_pos[0] + BALL_RADIUS >= GUTTER_RIGHT:
        score1 += 1
        direction = 'left'
        new_game()

    # goal to player 1
    elif ball_pos[0] - BALL_RADIUS <= GUTTER_LEFT:
        score2 += 1
        direction = 'right'
        new_game()

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, 'Red', 'White')

    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel

    if paddle1_pos < 0:
        paddle1_pos = 0

    if paddle2_pos < 0:
        paddle2_pos = 0

    if paddle1_pos > HEIGHT - PAD_HEIGHT:
        paddle1_pos = HEIGHT - PAD_HEIGHT

    if paddle2_pos > HEIGHT - PAD_HEIGHT:
        paddle2_pos = HEIGHT - PAD_HEIGHT

    # Draw paddles
    # Left paddle
    canvas.draw_polygon([
       (0, paddle1_pos), 
       (GUTTER_LEFT,paddle1_pos), 
       (GUTTER_LEFT,paddle1_pos + PAD_HEIGHT), 
       (0, paddle1_pos + PAD_HEIGHT)], 1, 'White', 'White')

    # Right paddle
    canvas.draw_polygon([
        (WIDTH, paddle2_pos), 
        (GUTTER_RIGHT, paddle2_pos),
        (GUTTER_RIGHT, paddle2_pos + PAD_HEIGHT),
        (WIDTH, paddle2_pos + PAD_HEIGHT)], 1, 'White', 'White')

    # draw scores
    canvas.draw_text('%d' % score1, (WIDTH // 2 - 100, 100), 56, 'silver', 'sans-serif')
    canvas.draw_text('%d' % score2, (WIDTH // 2 + 66, 100), 56, 'silver', 'sans-serif')

def keydown(key):
    global paddle1_vel, paddle2_vel
    
    PAD_VEL = 5 # constant paddles speed

    if key == simplegui.KEY_MAP['down']:
        paddle2_vel = PAD_VEL

    if key == simplegui.KEY_MAP['s']:
        paddle1_vel = PAD_VEL

    if key == simplegui.KEY_MAP['up']:
        paddle2_vel = - PAD_VEL

    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = - PAD_VEL

def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['up'] or key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP['w'] or key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0

def restart():
    global score1, score2, ball_pos
    score1 = score2 = 0
    new_game()


# create frame
frame = simplegui.create_frame('Pong. The game.', WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart', restart, 80)


# start frame
new_game()
frame.start()