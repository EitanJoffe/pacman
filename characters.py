import random
import arcade
from constants import TILE_SIZE

"""
מודול הדמויות (Sprites) במשחק פקמן.

מכיל את המחלקות:
- Character: מחלקת בסיס לדמויות (שיתוף שדה speed וכו')
- Pacman: השחקן הראשי
- Ghost: רוחות שנעות בצורה רנדומלית
- Coin: מטבעות לאיסוף
- Wall: קירות שחוסמים תנועה
"""

class Character(arcade.Sprite):
    def __init__(self, center_x, center_y, speed, color):
        super().__init__()
        radius = TILE_SIZE // 2 - 2
        texture = arcade.make_circle_texture(radius * 2, color)
        self.texture = texture
        self.center_x = center_x
        self.center_y = center_y
        self.width = texture.width
        self.height = texture.height
        self.speed = speed
        self.change_x = 0
        self.change_y = 0

class Player(Character):
    def __init__(self, center_x, center_y, speed):
        super().__init__(center_x, center_y, speed, arcade.color.YELLOW)
        self.score = 0
        self.lives = 3

    def move(self):
        self.center_x += self.change_x * self.speed
        self.center_y += self.change_y * self.speed

class Enemy(Character):
    def __init__(self, center_x, center_y, speed):
        super().__init__(center_x, center_y, speed, arcade.color.RED)
        self.time_to_change_direction = 0

    def pick_new_direction(self):
        directions = [(0,1), (0,-1), (1,0), (-1,0), (0,0)]
        self.change_x, self.change_y = random.choice(directions)
        self.time_to_change_direction = random.uniform(0.3, 1.0)

    def update_place(self, delta_time = 1 / 60):
        self.time_to_change_direction -= delta_time
        if self.time_to_change_direction <= 0:
            self.pick_new_direction()

        self.center_x += self.change_x * self.speed
        self.center_y += self.change_y * self.speed

class Coin(arcade.Sprite):
    def __init__(self, center_x, center_y):
        super().__init__()
        radius = TILE_SIZE // 2 - 10
        texture = arcade.make_circle_texture(radius * 2, arcade.color.YELLOW)
        self.texture = texture
        self.width = texture.width
        self.height = texture.height
        self.center_x = center_x
        self.center_y = center_y
        self.value = 10

class Wall(arcade.Sprite):
    def __init__(self, center_x, center_y):
        super().__init__()
        texture = arcade.make_soft_square_texture(TILE_SIZE,arcade.color.BLUE,TILE_SIZE // 2)
        self.texture = texture
        self.width = texture.width
        self.height = texture.height
        self.center_x = center_x
        self.center_y = center_y