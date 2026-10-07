"""
GameEngine: owns the player and all coins.

Starter version: one coin type, no obstacles, no timer yet. Coin
collection also has a known bug (see how `update` uses check_collection
below) that Task 1 asks you to fix - collected coins are never removed,
so standing on one keeps awarding points every frame.
"""

import random
import pygame

from game.player import Player
from game.coin import Coin
from game.collection import check_collection
from game.renderer import WIDTH, HEIGHT

NUM_COINS = 6
COIN_TYPES = {
    "bronze": (1, (205, 127, 50)),
    "silver": (3, (192, 192, 192)),
    "gold": (5, (255, 215, 0)),
}


class GameEngine:
    def __init__(self):
        self.player = Player(x=WIDTH / 2, y=HEIGHT / 2)
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

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.player, self.coins)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
