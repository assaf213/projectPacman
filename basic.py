import random
import arcade

"""
מודול קבועים עבור משחק פקמן.

מכיל:
- הגדרות חלון (רוחב, גובה, כותרת)
- גודל אריח בודד במפה
- מפה לוגית (LEVEL_MAP) שמגדירה קירות, מטבעות, פקמן ורוחות.
"""

# הגדרות חלון
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Pacman Arcade Example"

# גודל אריח במפה (בפיקסלים)
TILE_SIZE = 32

# מפה:
# # - קיר
# . - מטבע
# P - פקמן (נקודת התחלה לשחקן)
# G - רוח
LEVEL_MAP = [
    "########################",
    "#..........##..........#",
    "#.####.###.##.###.####.#",
    "#P....................G#",
    "########################",
]

speed_enemy = 1
speed_player = 1


class Coin(arcade.Sprite):
    def __init__(self, x_center, y_center, value=10):
        super().__init__()
        self.x_center = x_center
        self.y_center = y_center
        self.value = value
        radius = TILE_SIZE // 2 - 2
        texture = arcade.make_circle_texture(radius * 2, arcade.color.GOLD)
        self.texture = texture
        self.width = texture.width - 15
        self.height = texture.height - 15


class Character(arcade.Sprite):
    def __init__(self, speed, x_center, y_center):
        super().__init__()
        self.x_center = x_center
        self.y_center = y_center
        self.speed = speed
        self.x_change = 0
        self.y_change = 0
        radius = TILE_SIZE // 2 - 2
        texture = arcade.make_circle_texture(radius * 2, arcade.color.YELLOW)
        self.texture = texture
        self.width = texture.width - 9
        self.height = texture.height - 9


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
        self.time_to_change_direction = 0.0
        radius = TILE_SIZE // 2 - 2
        texture = arcade.make_circle_texture(radius * 2, arcade.color.BLUE)
        self.texture = texture
        self.width = texture.width - 11
        self.height = texture.height - 11

    def direction_new_pick(self):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)]
        rnd = random.choice(directions)
        self.x_change = rnd[0]
        self.y_change = rnd[1]
        self.time_to_change_direction = random.uniform(0.3, 1.0)

    def update_ghost_direction(self, time_delta=1 / 60):
        self.time_to_change_direction -= time_delta

        if self.time_to_change_direction <= 0:
            self.direction_new_pick()

        self.x_center += self.x_change * self.speed
        self.y_center += self.y_change * self.speed


class Wall(arcade.Sprite):
    def __init__(self, center_x, center_y):
        super().__init__(center_x, center_y)
        self.center_x = center_x
        self.center_y = center_y
        texture = arcade.make_soft_square_texture(TILE_SIZE, arcade.color.WHITE)
        self.texture = texture
        self.width = texture.width
        self.height = texture.height


class PacmanGame(arcade.View):
    def __init__(self):

        super().__init__()
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.ghost_list = arcade.SpriteList()
        self.player = None
        self.game_over = False
        self.background_color = arcade.color.BLACK
        self.start_x = 0
        self.start_y = 0

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.ghost_list = arcade.SpriteList()
        self.game_over = False
        self.player = None
        rows = len(LEVEL_MAP)
        for row_idx, row in enumerate(LEVEL_MAP):
            for col_idx, cell in enumerate(row):
                x = col_idx * TILE_SIZE / 2
                y = (rows - row_idx) * TILE_SIZE + TILE_SIZE / 2
                match cell:
                    case ".":
                        self.coin_list.append(Coin(x, y))
                    case "#":
                        self.wall_list.append(Wall(x, y))
                    case "G":
                        self.ghost_list.append(Enemy(x, y, speed_enemy))
                    case "P":
                        self.player_list.append(Player(x, y, speed_player))

    def on_draw(self):
        self.clear()
        self.wall_list.draw()
        self.player_list.draw()
        self.coin_list.draw()
        self.ghost_list.draw()
        rows = len(LEVEL_MAP)
        arcade.draw_text(
            f"{self.player.score} \n {self.player.lives}",
            start_x=TILE_SIZE / 2,
            start_y=(rows - 1) * TILE_SIZE / 2,
            color=arcade.color.WHITE,
            font_size=20,
            anchor_x="center"
        )

        if self.game_over:
            arcade.draw_text(
                f"Game over!",
                start_x=TILE_SIZE / 2,
                start_y=(rows / 2) * TILE_SIZE / 2,  # צריך לבדוק איך לממצוא את הY האחרון
                color=arcade.color.RED,
                font_size=20,
                anchor_x="center"
            )

    def on_key_press(self, key, modifiers):
        match key:
            case arcade.key.UP:
                self.player.x_change = 0
                self.player.y_change = 1
            case arcade.key.DOWN:
                self.player.x_change = 0
                self.player.y_change = -1
            case arcade.key.LEFT:
                self.player.x_change = -1
                self.player.y_change = 0
            case arcade.key.RIGHT:
                self.player.x_change = 1
                self.player.y_change = 0

        if self.player.lives == 0 and key == arcade.key.SPACE:
            self.setup()

    def on_key_release(self, key, modifiers):
        ...

    def on_update(self, delta_time):
        ghost_BooM = arcade.check_for_collision_with_list(self.player_list[0], self.ghost_list)
        if len(ghost_BooM) >= 1:
            self.player.lives -= 1


window = arcade.Window(800, 600, "check")
arcade.run()
