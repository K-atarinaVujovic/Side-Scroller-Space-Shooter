class GameSettings:
    """Game settings"""

    def __init__(self):
        """Init game settings"""
        # Screen
        self.screen_width = 800
        self.screen_height = 360
        self.bg_image = "assets/background.png"
        self.scroll_speed = 1

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