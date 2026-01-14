import arcade
from constants import WINDOW_WIDTH, WINDOW_TITLE, WINDOW_HEIGHT
from game import PacmanGame
"""
נקודת הכניסה למשחק פקמן.

אחראית על:
- יצירת חלון Arcade
- יצירת אובייקט PacmanGame
- אתחול המשחק
- הרצת לולאת המשחק
"""

def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    game = PacmanGame()
    game.setup()
    window.show_view(game)
    arcade.run()

    """פונקציית main שמריצה את המשחק."""


if __name__ == "__main__":
    main()
