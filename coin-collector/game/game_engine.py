"""
GameEngine: owns the player, coins, and obstacles.
"""

import random
import pygame

from game.player import Player
from game.coin import Coin
from game.collection import check_collection
from game.renderer import WIDTH, HEIGHT

NUM_COINS = 6
NUM_LIVES = 3
COIN_TYPES = {
    "bronze": (1, (205, 127, 50)),
    "silver": (3, (192, 192, 192)),
    "gold": (5, (255, 215, 0)),
}


class GameEngine:
    def __init__(self):
        self.player = Player(x=WIDTH / 2, y=HEIGHT / 2)
        self.obstacles = [
            pygame.Rect(90, 100, 80, 30),
            pygame.Rect(520, 110, 30, 85),
            pygame.Rect(140, 350, 100, 30),
            pygame.Rect(500, 360, 90, 30),
        ]
        self.lives = NUM_LIVES
        self._player_touching_obstacle = False
        self.coins = [self._random_coin(coin_type) for coin_type in COIN_TYPES.values()]
        self.coins.extend(
            self._random_coin()
            for _ in range(NUM_COINS - len(self.coins))
        )
        random.shuffle(self.coins)
        self.score = 0

    def _random_coin(self, coin_type=None):
        x = random.randint(30, WIDTH - 30)
        y = random.randint(30, HEIGHT - 30)
        if coin_type is None:
            coin_type = random.choice(tuple(COIN_TYPES.values()))
        value, color = coin_type
        return Coin(x=x, y=y, radius=12, value=value, color=color)

    def handle_input(self, keys_pressed):
        dx = dy = 0
        if keys_pressed[pygame.K_UP]:
            dy -= self.player.speed
        if keys_pressed[pygame.K_DOWN]:
            dy += self.player.speed
        if keys_pressed[pygame.K_LEFT]:
            dx -= self.player.speed
        if keys_pressed[pygame.K_RIGHT]:
            dx += self.player.speed
        self.player.move(dx, dy, WIDTH, HEIGHT)

    def update(self):
        collected = check_collection(self.player, self.coins)
        for coin in collected:
            self.score += coin.value
            self.coins.remove(coin)

        player_rect = self.player.get_rect()
        touching_obstacle = any(
            player_rect.colliderect(obstacle) for obstacle in self.obstacles
        )
        if touching_obstacle and not self._player_touching_obstacle:
            self.lives = max(0, self.lives - 1)
        self._player_touching_obstacle = touching_obstacle

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.player, self.coins, self.obstacles)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(surface, font, f"Lives: {self.lives}", (10, 38))
