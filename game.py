from constants import LEVEL_MAP, TILE_SIZE
import arcade
from characters import Player, Enemy, Coin, Wall
"""
מודול הלוגיקה הראשית של משחק הפקמן.

מכיל את המחלקה:
- PacmanGame: ניהול מצב המשחק, ציור, עדכון ותשובת מקלדת.
"""
class PacmanGame(arcade.View()):
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


