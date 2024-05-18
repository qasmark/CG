from __future__ import annotations

from random import uniform
from math import tan, radians, sqrt
from vector import Vector
from ray import Ray


class Camera:
    __slots__ = ('position', 'screen_size', 'fov', 'focus_distance', 'aperture')

    def __init__(self, position: Vector, screen_size: Vector, fov: int | float = 60.0, focus_distance: float = 10.0,
                 aperture: float = 0.1):
        self.position = position
        self.screen_size = screen_size
        self.fov = fov
        self.focus_distance = focus_distance
        self.aperture = aperture

    def __repr__(self) -> str:
        return f"Camera(position: {self.position}, screen_size: {self.screen_size}, fov: {self.fov}, focus_distance: " \
               f"{self.focus_distance}, aperture: {self.aperture})"

    def get_direction(self, x_y: Vector) -> Ray:
        # Original direction calculation
        xy = x_y - self.screen_size / 2
        z = self.screen_size.y / tan(radians(self.fov) / 2)
        direction = Vector(xy.x, xy.y, -z).normalize()

        # Random point within aperture
        if self.aperture > 0:
            rd = Vector(uniform(-1, 1), uniform(-1, 1), 0).normalize() * (self.aperture / 2)
            focal_point = self.position + direction * self.focus_distance
            direction = (focal_point - (self.position + rd)).normalize()
            origin = self.position + rd
        else:
            origin = self.position

        return Ray(origin, direction)
