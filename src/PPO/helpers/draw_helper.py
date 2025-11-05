import pygame

class DrawHelper:
    """Class with helper functions for drawing"""
    def __init__(self, game):
        self.game = game

    def draw_info(self, episode, episode_reward, step_count, total_reward, total_steps):
        """Draw current and total training info."""
        info_font = pygame.font.SysFont("Arial", 15)
        # Write current episode info
        text = f"Ep: {episode}    Rew: {episode_reward:10.3f}    Steps: {step_count:6}"
        x, y = self.game.settings.screen_width - 8, 8
        self.game.draw.draw_text(text, x, y, topright=True, font=info_font)
        # Write total info
        text = f"Total rew: {total_reward:20.3f}    Total steps: {total_steps:10}"
        x, y = self.game.settings.screen_width - 8, self.game.settings.screen_height - 8
        self.game.draw.draw_text(text, x, y, bottomright=True, font=info_font)