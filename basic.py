import random
class Coin:
    def __init__(self, x_center, y_center, value=10):
        self.x_center = x_center
        self.y_center = y_center
        self.value = value


class Character:
    def __init__(self, speed, x_center, y_center):
        self.x_center = x_center
        self.x_center = y_center
        self.speed = speed
        self.x_change = 0
        self.y_change = 0


class Player(Character):
    def __init__(self, x_center, y_center, speed):
        super().__init__(x_center, y_center, speed)
        self.score = 0
        self.lives = 3

    def move(self, change_x, change_y):
        self.x_center += change_x * self.speed
        self.y_center += change_y * self.speed


class Enemy(Character):
    def __init__(self, x_center, y_center, speed):
        super().__init__(x_center, y_center, speed)
        self.time_to_change_direction = 0

    def direction_new_pick(self):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)]
        rnd = random.choice(directions)
        self.x_change = rnd[0]
        self.y_change = rnd[1]
        self.direction_change_to_time = random.next(0.3, 1.0)
    def update(self, time_delta=1/60):
        self.direction_change_to_time -= time_delta

        if self.direction_change_to_time <= 0:
            self.direction_new_pick()

        self.x_center += self.x_change * self.speed
        self.y_center += self.y_change * self.speed

class wall():
    def __init__(self, center_x, center_y):
        self.center_x = center_x
        self.center_y = center_y
