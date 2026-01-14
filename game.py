from constants import LEVEL_MAP, TILE_SIZE,WINDOW_WIDTH,WINDOW_HEIGHT
import arcade
from characters import Player, Enemy, Coin, Wall
"""
מודול הלוגיקה הראשית של משחק הפקמן.

מכיל את המחלקה:
- PacmanGame: ניהול מצב המשחק, ציור, עדכון ותשובת מקלדת.
"""


class PacmanGame(arcade.View()):
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

        wall_list = arcade.SpriteList()
        coin_list = arcade.SpriteList()
        ghost_list = arcade.SpriteList()
        player_list = arcade.SpriteList()

        rows = len(LEVEL_MAP)
        for row_idx, row in enumerate(LEVEL_MAP):
            for col_idx, cell in enumerate(row):
                x = col_idx * TILE_SIZE + TILE_SIZE / 2
                y = (rows - row_idx - 1) * TILE_SIZE + TILE_SIZE / 2
                current = LEVEL_MAP[x][y]
                if current == '#':
                    current = Wall(x, y)
                    wall_list.append(current)
                elif current == '.':
                    current = Coin(x, y)
                    coin_list.append(current)
                elif current == 'P':
                    current = Player(x, y, 5)
                    player_list.append(current)
                elif current == 'G':
                    current = Enemy(x,y, 5)
                    ghost_list.append(current)

    def on_draw(self):
        self.clear()
        self.wall_list.draw()
        self.coin_list.draw()
        self.ghost_list.draw()
        self.player_list.draw()
        arcade.draw_text(self.player.score,0,WINDOW_HEIGHT,arcade.color.YELLOW,TILE_SIZE//2)
        arcade.draw_text(self.player.lives,0,WINDOW_HEIGHT-TILE_SIZE,arcade.color.RED,TILE_SIZE//2)

        if self.player.lives==0:
            self.game_over=True
            arcade.draw_text("You Lost ",WINDOW_WIDTH//2,WINDOW_HEIGHT//2,arcade.color.YELLOW,WINDOW_WIDTH//5)
