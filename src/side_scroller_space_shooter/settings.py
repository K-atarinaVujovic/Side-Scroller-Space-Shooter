from pygame import font
import random

class GameSettings:
    """Game settings"""

    def __init__(self):
        """Init game settings"""
        # Screen
        self.screen_width = 500
        self.screen_height = 360
        self.bg_image = "side_scroller_space_shooter/assets/background.png"
        self.scroll_speed = 1

        # Text
        self.default_font = font.SysFont("Arial", 30)
        self.default_font_color = (255, 255, 255)

        # FPS
        self.fps = 60

class PlayerSettings:
    """Player settings"""
    def __init__(self):
        self.sprite_img = "side_scroller_space_shooter/assets/ship.png"
        self.speed = 6

        self.bullet_speed = 5
        self.bullet_width, self.bullet_height = 30, 4
        self.bullet_color = (233, 255, 26)
        self.fire_rate = 400

class EnemySettings:
    """Enemy settings"""

    def __init__(self):
        self.sprite_img = "side_scroller_space_shooter/assets/enemy.png"
        self.speed = 2

        self.bullet_speed = 5
        self.bullet_width, self.bullet_height = 20, 4
        self.bullet_color = (255, 102, 102)

    def calculate_spawn_cooldown(self):
        return random.randint(2000, 4000)
    
    def calculate_bullet_cooldown(self):
        return random.randint(700, 1000)
    
    def calculate_direction_cooldown(self):
        return random.randint(400, 3000)

class AsteroidSettings:
    """Asteroid settings"""
    def __init__(self):
        self.sprite_img = "side_scroller_space_shooter/assets/asteroid.png"
        self.speed = 2
        self.spawn_cooldown = 1500