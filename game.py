from arcade.experimental.shapes_perf import TITLE

from constants import LEVEL_MAP, TILE_SIZE,WINDOW_WIDTH,WINDOW_HEIGHT
import arcade
from characters import Player, Enemy, Coin, Wall
"""
מודול הלוגיקה הראשית של משחק הפקמן.
מכיל את המחלקה:
- PacmanGame: ניהול מצב המשחק, ציור, עדכון ותשובת מקלדת.
"""


class PacmanGame(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.BLACK
        self.start_x = 0
        self.start_y = 0
        self.game_over = False
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.ghost_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.player=None

    def setup(self):
        flag = False

        rows = len(LEVEL_MAP)
        for row_idx, row in enumerate(LEVEL_MAP):
            for col_idx, cell in enumerate(row):
                x = col_idx * TILE_SIZE + TILE_SIZE / 2
                y = (rows - row_idx - 1) * TILE_SIZE + TILE_SIZE / 2
                current = LEVEL_MAP[row_idx][col_idx]
                if current == '#':
                    current = Wall(x, y)
                    self.wall_list.append(current)
                elif current == '.':
                    current = Coin(x, y)
                    self.coin_list.append(current)
                elif current == 'P':
                    current = Player(x, y, 5)
                    self.player = current
                    self.player_list.append(current)
                elif current == 'G':
                    current = Enemy(x,y, 5)
                    self.ghost_list.append(current)

    def on_draw(self):
        self.clear()
        self.wall_list.draw()
        self.coin_list.draw()
        self.ghost_list.draw()
        self.player_list.draw()
        arcade.draw_text(self.player.score,50,WINDOW_HEIGHT-TILE_SIZE,arcade.color.YELLOW,TILE_SIZE-TILE_SIZE//4)
        arcade.draw_text(self.player.lives,50,WINDOW_HEIGHT-TILE_SIZE*2,arcade.color.RED,TILE_SIZE-TILE_SIZE//4)

        if self.player.lives==0:
            self.game_over=True
            arcade.draw_text("You Lost ",WINDOW_WIDTH//2,WINDOW_HEIGHT//2,arcade.color.YELLOW,WINDOW_WIDTH//5)

    def on_key_press(self,key,modifiers):
        if key==arcade.key.UP:
            self.player.change_y=1
        if key==arcade.key.DOWN:
            self.player.change_y=-1
        if key==arcade.key.LEFT:
            self.player.change_x=-1
        if key==arcade.key.RIGHT:
            self.player.change_x=-1

        if self.game_over==True:
            if key==arcade.key.SPACE:
                self.setup()

    def on_key_release(self,key,modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change.y = 0
        if key == arcade.key.RIGHT or key == arcade.key.LEFT:
            self.player.change.x = 0


    def on_update(self, delta_time):
        if self.game_over == True:
            return

        current_x = self.player.center_x
        current_y = self.player.center_y
        self.player.move()
        wall_collision_list = arcade.check_for_collision_with_list(self.player, self.wall_list)

        for wall in wall_collision_list:
            if self.player.center_x == wall.center_x and self.player.center_y == wall.center_y:
                self.player.center_x, self.player_list.center_y = current_x, current_y

        for ghost in self.ghost_list:
            ghost_x = ghost.center_x
            ghost_y = ghost.center_y
            ghost.update_place(delta_time)
            for wall in wall_collision_list:
                 if ghost.center_y == wall.center_x and ghost.center_y == wall.center_y:
                    ghost.center_x = ghost_x
                    ghost.center_y = ghost_y
                    ghost.pick_new_direction()

        coin_collision_list = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for coin in coin_collision_list:
            if self.player.center_x == coin.center_x and self.player.center_y and coin.center_y:
                coin.remove_from_sprite_lists()
                self.player.score += coin.value

        ghost_collision_list = arcade.check_for_collision_with_list(self.player, self.ghost_list)
        for ghost in ghost_collision_list:
            if self.player.center_x == ghost.center_x and self.player.center_y == ghost.center_y:
                self.player.lives -= 1
                self.player.center_x, self.player.center_y = TILE_SIZE, TILE_SIZE
                self.player.speed = 1
        if self.player.lives == 0:
            self.game_over = True