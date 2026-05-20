import parameters as p
import game
import math

class Sensor():

    def __init__(self, paddle: game.Paddle, ball: game.Ball, number_of_rays: int):

        self.x_start = paddle.x + paddle.width
        self.y_start = paddle.y + paddle.height // 2
        self.paddle = paddle
        self.ball = ball
        self.number_of_rays = number_of_rays

        # Finds the rotation to make the angle spread symetric
        self.angle_rotation =  (p.SENSOR_DEGREE_OPENING / 2)
        # Finds the separation degree between rays
        self.degree_spread = p.SENSOR_DEGREE_OPENING / self.number_of_rays 

        self.cast_rays()

    def cast_rays(self):

        self.x_start = self.paddle.x + self.paddle.width
        self.y_start = self.paddle.y + self.paddle.height // 2
        self.rays = []
        self.t_values = []
        self.collitions = []
        for ray in range(self.number_of_rays + 1):
            # Gets the angle from the bottom of the raycast to the ray.
            angle = self.degree_spread * ray - self.angle_rotation
            angle = math.radians(angle)
            # Get the x and y values for the given angle
            x = math.cos(angle) * p.RAY_LENGTH
            y = math.sin(angle) * p.RAY_LENGTH
            # Adjustment for current position of the Paddle
            x = x + self.x_start
            y = y + self.y_start

            dx = x - self.x_start
            dy = y - self.y_start


            self.rays.append([x, y])
            t_value = self.get_ball_collition([x, y], self.ball)
            self.t_values.append(t_value)
            if t_value != 0:
                self.collitions.append([self.x_start + dx * t_value, self.y_start + dy * t_value])
            else:
                self.collitions.append([x, y])
            


    def get_ball_collition(self,ray: list[int, int], ball: game.Ball) -> float :
        """
            Detects if the ray collides with the ball
            returns bool and t value
            
            :param ray: list including [x, y] of the ray maximum reach
            :type ray: list[int, int]
            :param ball: Ball object
            :type ball: game.Ball
            :return: t value
            :rtype: float
            """
            
        # Ray Positions
        A_x0 = self.x_start
        A_y0 = self.y_start
        A_x1 = ray[0]
        A_y1 = ray[1]
        # Ball Positions
        B_x0 = ball.x
        B_y0 = ball.y
        B_x1 = ball.x + ball.width
        B_y1 = ball.y + ball.height

        # We define the vector
        dx = A_x1 - A_x0
        if dx == 0:
            if A_x0 < B_x0 or A_x0 > B_x1:
                # return None
                return 0
            tMinX = -float("inf")
            tMaxX = float("inf")
        else:
            tx0 = (B_x0 - A_x0) / dx
            tx1 = (B_x1 - A_x0) / dx
            tMinX, tMaxX = min(tx0, tx1), max(tx0, tx1)

        dy = A_y1 - A_y0 

        if dy == 0:
            if A_y0 < B_y0 or A_y0 > B_y1:
                # return None
                return 0
            tMinY = -float("inf")
            tMaxY = float("inf")
        else:
            ty0 = (B_y0 - A_y0) / dy
            ty1 = (B_y1 - A_y0) / dy
            tMinY, tMaxY = min(ty0, ty1), max(ty0, ty1)


        # We get where the ray enters and exits 
        t_enters = max(tMinX, tMinY) 
        # It is the max value because it enters when both conditions (inside X range and inside y range) are met.
        t_exits = min(tMaxX, tMaxY)
        # It is the min value because it exits when one of the conditions is not met

        if t_exits < t_enters or t_exits < 0:
           #  return None
           return 0

        if t_enters >= 0 and t_enters <= 1:
            return t_enters
        else:
            # return None
            return 0

    