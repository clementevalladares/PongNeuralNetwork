import parameters as p
import pygame

class Paddle():

    def __init__(self, x: int, y: int, width: int, height: int, speed: int):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.up = False
        self.down = False

    def move(self) -> int:
        """
        moves the paddle up or down, returns final "y" position
        
        :param self: Description
        :String direction: "up" or "down
        """
        if self.up:
            new_y = self.y - self.speed
            if new_y < 0:
                self.y = 0
            else:
                self.y = new_y
            
        if self.down:
            new_y = self.y + self.speed
            if new_y + self.height > p.SCREEN_HEIGHT:
                self.y = p.SCREEN_HEIGHT - self.height
            else:
                self.y = new_y


class Ball():

    def __init__(self, x: int, y: int, width: int, height: int, x_speed: int, y_speed: int):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.x_speed = x_speed
        self.y_speed = y_speed

    def restart_position(self, side: int):
        """
        Docstring for restart
        
        :param self: Description
        :param side: Indicates the side in which the ball starts moving 1 for right - 1 for left 
        :type side: int
        """
        self.x = p.BALL_START_X
        self.y = p.BALL_START_Y
        self.width = p.BALL_WIDTH
        self.height = p.BALL_HEIGHT
        self.x_speed =  -p.BALL_STARTING_X_SPEED if side == 1 else p.BALL_STARTING_X_SPEED
        self.y_speed = p.BALL_STARTING_Y_SPEED
      

    def check_collition(self, paddle: Paddle):
        
        # Collition on right paddle
        if self.x_speed > 0:
            if (self.x + self.width >= paddle.x) and (self.x <= paddle.x + paddle.width):
                if (self.y + self.y_speed >= paddle.y) and (self.y + self.y_speed <= paddle.y + paddle.height):
                    return True
        
        # Collition on left paddle
        elif self.x_speed < 0:
            if (self.x <= paddle.x + paddle.width) and (self.x >= paddle.x):
                if (self.y +self.y_speed >= paddle.y and self.y + self.y_speed <= paddle.y + paddle.height):
                    return True

        return False

    def move(self, paddles: list[Paddle, Paddle]) -> tuple[int, bool]:
 
        hit= 0

        for paddle in paddles:
            collition = self.check_collition(paddle)
            if collition:
                hit += 1
                if self.x_speed > 0:
                    self.x = paddle.x - self.width
                elif self.x_speed < 0:
                    self.x = paddle.x + self.width

                self.x_speed *= - (1 + p.BALL_SPEED_INCREASE)


        # Collition with Ground and Roof
        if self.y <= 0 or self.y + self.height >= p.SCREEN_HEIGHT:
            self.y_speed *= -1

        self.x += self.x_speed
        self.y += self.y_speed

        # Out of Bounds
        if self.x < 0:
            return 1, hit
        elif self.x > p.SCREEN_WIDTH:
            return 2, hit
        else:
            return 0, hit

class Controls():
    
    def __init__(self):
        # Check if up or down are pressed
        self.pressed_left = None
        self.pressed_right = None


    def process_movement(self, event) -> tuple[str, int]:
        
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                return "up", 0
            elif event.key == pygame.K_s:
                self.pressed_right
                return "down", 0
            elif event.key == pygame.K_UP:
                return "up", 1
            elif event.key == pygame.K_DOWN:
                return "down", 1
        return None, None


