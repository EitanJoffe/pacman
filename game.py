from constants import LEVEL_MAP, TILE_SIZE,WINDOW_WIDTH,WINDOW_HEIGHT
import arcade
from characters import Player, Enemy, Coin, Wall, Apple
import time

"""
מודול הלוגיקה הראשית של משחק הפקמן.
מכיל את המחלקה:
- PacmanGame: ניהול מצב המשחק, ציור, עדכון ותשובת מקלדת.
"""


class PacmanGame(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.BLACK
        self.start_x = TILE_SIZE * 1.5
        self.start_y = TILE_SIZE * 1.5
        self.game_over = False
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.ghost_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.apple_list = arcade.SpriteList()
        self.player=None
        self.speed_boost_active = False
        self.speed_boost_start = 0
        self.speed_boost_score = 300

    def setup(self):
        self.game_over = False
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.ghost_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.apple_list = arcade.SpriteList()

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
                    current = Player(x, y, 2)
                    self.player = current
                    self.player_list.append(current)
                elif current == 'G':
                    current = Enemy(x,y, 1.8)
                    self.ghost_list.append(current)
                elif cell == 'A':
                    self.apple_list.append(Apple(x, y))

        if self.player is None:
            player =  Player(self.start_x, self.start_y, 2)
            self.player = player
            self.player_list.append(player)


    def on_draw(self):
        self.clear()
        self.wall_list.draw()
        self.coin_list.draw()
        self.apple_list.draw()
        self.ghost_list.draw()
        self.player_list.draw()
        arcade.draw_text(self.player.score,TILE_SIZE,WINDOW_HEIGHT-TILE_SIZE,arcade.color.YELLOW,TILE_SIZE-TILE_SIZE//4)
        arcade.draw_text(self.player.lives,TILE_SIZE,WINDOW_HEIGHT-TILE_SIZE*2,arcade.color.RED,TILE_SIZE-TILE_SIZE//4)

        if self.player.lives==0:
            self.game_over=True
            arcade.draw_text("You Lost ",WINDOW_WIDTH//4,WINDOW_HEIGHT//2,arcade.color.RED,WINDOW_WIDTH//8)

        if len(self.coin_list) == 0:
            self.game_over = True
            arcade.draw_text("You Won! ", WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2, arcade.color.YELLOW, WINDOW_WIDTH // 8)

    def on_key_press(self,key,modifiers):
        if key==arcade.key.UP or key==arcade.key.W:
            self.player.change_y=1
        if key==arcade.key.DOWN or key == arcade.key.S:
            self.player.change_y=-1
        if key==arcade.key.LEFT or key==arcade.key.A:
            self.player.change_x=-1
        if key==arcade.key.RIGHT or key==arcade.key.D:
            self.player.change_x=1

        if self.game_over:
            if key==arcade.key.SPACE:
                self.setup()
            return

    def on_key_release(self,key,modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN or key==arcade.key.W or key==arcade.key.S:
            self.player.change_y = 0
        if key == arcade.key.RIGHT or key == arcade.key.LEFT or key==arcade.key.A or key==arcade.key.D:
            self.player.change_x = 0

    def activate_speed_boost(self):
        self.player.speed = 4
        self.speed_boost_active = True
        self.speed_boost_start = time.time()

    def on_update(self, delta_time):
        if self.game_over:
            return

        current_x = self.player.center_x
        current_y = self.player.center_y
        self.player.move()
        wall_collision_with_player_list = arcade.check_for_collision_with_list(self.player, self.wall_list)

        for wall in wall_collision_with_player_list:
            if arcade.check_for_collision(self.player, wall):
                self.player.center_x, self.player.center_y = current_x, current_y

        for ghost in self.ghost_list:
            ghost_x = ghost.center_x
            ghost_y = ghost.center_y
            ghost.update_place(delta_time)
            wall_collision_with_ghost_list = arcade.check_for_collision_with_list(ghost, self.wall_list)
            for wall in wall_collision_with_ghost_list:
                 if arcade.check_for_collision(ghost, wall):
                    ghost.center_x = ghost_x
                    ghost.center_y = ghost_y
                    ghost.pick_new_direction()

        coin_collision_list = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for coin in coin_collision_list:
            if arcade.check_for_collision(self.player, coin):
                coin.remove_from_sprite_lists()
                self.player.score += coin.value
                if self.player.score >= self.speed_boost_score:
                    self.activate_speed_boost()
                    self.speed_boost_score += 300

        for apple in arcade.check_for_collision_with_list(self.player, self.apple_list):
            apple.remove_from_sprite_lists()
            self.player.score += apple.value

        ghost_collision_list = arcade.check_for_collision_with_list(self.player, self.ghost_list)
        for ghost in ghost_collision_list:
            if arcade.check_for_collision(self.player, ghost):
                if self.speed_boost_active:
                    self.player.speed = 2
                    self.speed_boost_active = False
                    self.player.color = arcade.color.YELLOW
                self.player.lives -= 1
                self.player.center_x, self.player.center_y = self.start_x, self.start_y
                self.player.speed = 2
        if self.player.lives == 0:
            self.game_over = True

        if self.speed_boost_active:
            self.player.color = arcade.color.GREEN
            if time.time() - self.speed_boost_start >= 5:
                self.player.speed = 2
                self.speed_boost_active = False
                self.player.color = arcade.color.YELLOW

        if self.player.center_x<0:
            self.player.center_x=WINDOW_WIDTH
        if self.player.center_x>WINDOW_WIDTH:
            self.player.center_x=0

        for ghost in self.ghost_list:
            if ghost.center_x<0:
                ghost.center_x=WINDOW_WIDTH
            if ghost.center_x>WINDOW_WIDTH:
                ghost.center_x=0


