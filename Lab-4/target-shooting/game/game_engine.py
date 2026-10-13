"""
GameEngine: owns the targets, handles clicks, tracks score, and runs a
30-second timed round.

Scoring:
- Each hit adds the current multiplier to the score.
- After a hit, the multiplier goes up by 1 (the combo grows).
- A miss resets the multiplier to 1.

Timer:
- The round uses elapsed real time (time.monotonic), not frame counts.
- When time runs out, clicks and movement stop and the final score shows.
"""

import math
import random
import time

from game.target import Target
from game.hit_detection import check_hit
from game.renderer import WIDTH, HEIGHT

NUM_TARGETS = 3
TARGET_RADIUS = 28
ROUND_SECONDS = 30

SLOW_SPEED = (1, 2)   # pixels per frame, chosen at random in this range
FAST_SPEED = (4, 6)


class GameEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        """Start a new round: clear score, combo, timer, and targets."""
        self.targets = [self._random_target() for _ in range(NUM_TARGETS)]
        self.hits = 0
        self.misses = 0
        self.score = 0
        self.multiplier = 1
        self.start_time = time.monotonic()

    def time_left(self):
        """Seconds remaining in the round, never below zero."""
        elapsed = time.monotonic() - self.start_time
        return max(0.0, ROUND_SECONDS - elapsed)

    def is_over(self):
        return self.time_left() <= 0

    def _random_target(self):
        x = random.randint(TARGET_RADIUS + 10, WIDTH - TARGET_RADIUS - 10)
        y = random.randint(TARGET_RADIUS + 10, HEIGHT - TARGET_RADIUS - 10)

        # Pick a speed group, then a random speed and direction within it
        low, high = random.choice([SLOW_SPEED, FAST_SPEED])
        speed = random.uniform(low, high)
        angle = random.uniform(0, 2 * math.pi)
        vx = speed * math.cos(angle)
        vy = speed * math.sin(angle)

        return Target(x, y, radius=TARGET_RADIUS, vx=vx, vy=vy)

    def handle_click(self, pos):
        if self.is_over():
            return  # round finished: ignore all clicks

        target = check_hit(self.targets, pos)
        if target is not None:
            # Hit: add points at the current multiplier, then grow the combo
            self.hits += 1
            self.score += self.multiplier
            self.multiplier += 1
            self.targets.remove(target)
            self.targets.append(self._random_target())
        else:
            # Miss: reset the combo
            self.misses += 1
            self.multiplier = 1

    def update(self):
        if self.is_over():
            return  # targets stop moving when the round ends
        for target in self.targets:
            target.update(WIDTH, HEIGHT)

    def draw(self, surface, font):
        from game import renderer

        if self.is_over():
            renderer.draw_text(surface, font, "Round over!", (WIDTH // 2 - 120, HEIGHT // 2 - 60))
            renderer.draw_text(surface, font, f"Final score: {self.score}",
                               (WIDTH // 2 - 120, HEIGHT // 2 - 20))
            renderer.draw_text(surface, font, "Press R to play again",
                               (WIDTH // 2 - 120, HEIGHT // 2 + 20))
            return

        renderer.draw_scene(surface, self.targets)
        renderer.draw_text(surface, font,
                           f"Hits: {self.hits}  Misses: {self.misses}", (10, 10))
        renderer.draw_text(surface, font,
                           f"Score: {self.score}  Combo x{self.multiplier}", (10, 35))
        renderer.draw_text(surface, font,
                           f"Time: {math.ceil(self.time_left())}", (WIDTH - 130, 10))