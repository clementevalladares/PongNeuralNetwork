import pygame
import game
import parameters as p
import sensor
import network
import random

screen = pygame.display.set_mode((p.SCREEN_WIDTH, p.SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Left and Right Paddles
paddles = [game.Paddle(p.PADDLE_INDENT, 
                       p.PADDLE_Y_START, 
                       p.PADDLE_WIDTH, 
                       p.PADDLE_HEIGHT, 
                       p.PADDLE_SPEED),
           game.Paddle(p.SCREEN_WIDTH - p.PADDLE_INDENT - p.PADDLE_WIDTH, 
                       0, 
                       p.PADDLE_WIDTH, 
                       p.SCREEN_HEIGHT, # We set this ant SCREEN_HEIGHT for Training
                       p.PADDLE_SPEED)]

ball = game.Ball(p.BALL_START_X, p.BALL_START_Y, p.BALL_WIDTH, p.BALL_HEIGHT,
                        p.BALL_STARTING_X_SPEED, p.BALL_STARTING_Y_SPEED)

controls = game.Controls()
sensor = sensor.Sensor(paddles[0], ball, p.NUMBER_OF_RAYS)

network2 = network.Brain(sensor, paddles[0], ball, p.NUMBER_OF_LEVELS, p.NUMBER_OF_NEURONS)
if p.LOAD_NETWORK:
    network2.load_network(p.NETWORK_PATH)


playing = True
restart = 2

# Keep track of previous hits to improve Network
hits = 0
prev_hits = network2.hits
print("Previous Hits:", prev_hits)
while playing:

    # Set starting params
    if restart:
        
        if not p.TICK:
            network2.new_hits(hits)

        hits = 0
        start_y = random.randint(0, 1)
        start_y = -1 if start_y == 0 else 1
        ball.restart_position(start_y)

        paddles[0].y = p.PADDLE_Y_START
        for paddle in paddles:
            paddle.up = False
            paddle.down = False

        restart = False

    # Fill background
    screen.fill(p.BLACK)

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            playing = False

        elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            # Move Paddles
            movement, side = controls.process_movement(event)
            if movement == "down":
                paddles[side].down = False if paddles[side].down else True
            if movement == "up":
                paddles[side].up = False if paddles[side].up else True
    
    # Move Paddles
    for p_ in paddles:
        p_.move()
    # Move Ball, if Out of Bounds it returns the winner (1 or 2)
    restart, hit = ball.move(paddles)
    hits += hit

      
    # Draw Paddles
    for p_ in paddles:
        pygame.draw.rect(screen, p.WHITE, (p_.x, p_.y, p_.width, p_.height))
    # Draw Ball
    pygame.draw.rect(screen, p.WHITE, (ball.x, ball.y, ball.width, ball.height))

    # Draw Rays
    sensor.cast_rays()
    for ray in sensor.collitions:
        pygame.draw.line(screen, p.WHITE, (sensor.x_start, sensor.y_start), (ray[0], ray[1]), 1)

    # send = network.read()
    send = network2.read()
    
    if send[0] == 1:
        paddles[0].down = True
    if send[0] == -1:
        paddles[0].down = False
    if send[1] == 1:
        paddles[0].up = True
    if send[1] == -1:
        paddles[0].up = False
    

    # Update Screen
    pygame.display.flip()

    if p.TICK:
        clock.tick(p.FPS)

# network.save_network('save.json')
pygame.quit()