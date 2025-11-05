from PPO.utils.utils import normalize

class RewardHelper:
    """Class with helper functions for calculating reward value"""
    def __init__(self, game):
        self.game = game
        self.screen_width = game.settings.screen_width
        self.screen_height = game.settings.screen_height

    def calculate_reward(self):
        """Calculate reward.
        
        Rewards for shooting enemies and shooting close to enemies.
        Punishes for standing still and losing the game.
        """
        reward = 0
        max_diagonal_distance = (self.screen_width**2 + self.screen_height**2)**0.5
        
        # Reward for shooting enemy
        if self.game.shot_enemy:
            reward += 550.0

        # Reward for bullet close to enemy
        if self.game.enemy_bullets:
            min_bullet_to_enemy_distance = self._get_min_bullet_to_enemy_distance()
            normalized_distance = normalize(min_bullet_to_enemy_distance, max_diagonal_distance)
            reward += 1.6 / (1 + normalized_distance)**2

        # Punish for losing
        if self.game.game_over:
            reward -= 400.0

        # Punish for being close to enemy
        if self.game.enemy_sprites:
            min_distance = self._get_player_to_group_distance(self.game.enemy_sprites)
            normalized_distance = normalize(min_distance, max_diagonal_distance)
            reward -= 0.5 / (1 + normalized_distance)**2

        # Punish for being close to asteroid
        if self.game.asteroid_sprites:
            min_distance = self._get_player_to_group_distance(self.game.asteroid_sprites)
            normalized_distance = normalize(min_distance, max_diagonal_distance)
            reward -= 1.2 / (1 + normalized_distance)**2

        # Punsh for being close to bullet
        if self.game.enemy_bullets:
            min_distance = self._get_player_to_group_distance(self.game.enemy_bullets)
            normalized_distance = normalize(min_distance, max_diagonal_distance)
            reward -= 1 / (1 + normalized_distance)**2

        return reward
        
    def _get_min_bullet_to_enemy_distance(self):
        """Calculate smallest distance between player bullets and an enemy"""
        bullets = self.game.player_bullets
        enemies = self.game.enemy_sprites

        # Initialize min distance
        min_distance = self.screen_width

        # If no bullets are shot or no enemies are on screen, return max distance
        if not bullets or not enemies:
            return min_distance

        for bullet in bullets:
            for enemy in enemies:
                dx = bullet.rect.centerx - enemy.rect.centerx
                dy = bullet.rect.centery - enemy.rect.centery
                distance = (dx**2 + dy**2)**0.5

                if distance < min_distance:
                    min_distance = distance

        return min_distance
    
    def _get_player_to_group_distance(self, group):
        """Calculate smallest distance between player and group"""
        player = self.game.player_sprite

        # Initialize min distance
        min_distance = self.screen_width

        # If no bullets are shot or no group are on screen, return max distance
        if not group:
            return min_distance

        for sprite in group:
            dx = player.rect.centerx - sprite.rect.centerx
            dy = player.rect.centery - sprite.rect.centery
            distance = (dx**2 + dy**2)**0.5

            if distance < min_distance:
                # If sprite is behind player, ignore
                if sprite.rect.centerx <= player.rect.centerx - 30:
                    continue
                else:
                    min_distance = distance

        return min_distance