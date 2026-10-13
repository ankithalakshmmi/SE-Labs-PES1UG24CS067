"""
Target: a circular target the player clicks on. (x, y) is the CENTER
of the circle - this matters for how it's drawn vs. how it's hit-tested.
"""

import pygame


class Target:
    def __init__(self, x, y, radius=28, color=(230, 90, 70), vx=0, vy=0):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vx = vx  # horizontal speed in pixels per frame
        self.vy = vy  # vertical speed in pixels per frame

    def update(self, width, height):
        """Move the target and bounce it off the edges of the play area.
        Because x and y are the centre, the edge checks use the radius:
        the centre must stay at least 'radius' away from each wall."""
        self.x += self.vx
        self.y += self.vy

        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx = abs(self.vx)
        elif self.x + self.radius > width:
            self.x = width - self.radius
            self.vx = -abs(self.vx)

        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy = abs(self.vy)
        elif self.y + self.radius > height:
            self.y = height - self.radius
            self.vy = -abs(self.vy)

    def get_bounding_rect(self):
        """A square bounding box around the circle - NOT the same
        shape as the actual circle, and easy to build incorrectly."""
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                           self.radius * 2, self.radius * 2)
