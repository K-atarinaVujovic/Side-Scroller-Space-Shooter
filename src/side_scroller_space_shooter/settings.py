class GameSettings:
    """Game settings"""

    def __init__(self):
        """Init game settings"""
        # Screen
        self.screen_width = 800
        self.screen_height = 360
        self.bg_image = "assets/background.png"
        self.scroll_speed = 1

        # Other
        self.fps = 60

class PlayerSettings:
    """Player settings"""
    def __init__(self):
        self.sprite_img = "assets/ship.png"
        self.speed = 5