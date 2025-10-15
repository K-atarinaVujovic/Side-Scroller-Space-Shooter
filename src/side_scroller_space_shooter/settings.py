from pygame import font

class GameSettings:
    """Game settings"""

    def __init__(self):
        """Init game settings"""
        # Screen
        self.screen_width = 500
        self.screen_height = 360
        self.bg_image = "assets/background.png"
        self.scroll_speed = 1

        # Text
        self.default_font = font.SysFont("Arial", 30)
        self.default_font_color = (255, 255, 255)

        # FPS
        self.fps = 60

class PlayerSettings:
    """Player settings"""
    def __init__(self):
        self.sprite_img = "assets/ship.png"
        self.speed = 5

        self.bullet_speed = 5
        self.bullet_width, self.bullet_height = 4, 4
        self.bullet_color = (233, 255, 26)
        self.fire_rate = 250

class AsteroidSettings:
    """Asteroid settings"""
    def __init__(self):
        self.sprite_img = "assets/asteroid.png"
        self.speed = 2
        self.cooldown = 1200