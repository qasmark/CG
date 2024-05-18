from __future__ import annotations

from vector import Vector


class Light:
    __slots__ = ('direction', 'strength', 'diffuse_color', 'specular_color', 'ambient_color')

    def __init__(self, direction: Vector, strength: float, diffuse_color: Vector, specular_color: Vector,
                 ambient_color: Vector):
        self.direction = direction.normalize()
        self.strength = strength
        self.diffuse_color = diffuse_color
        self.specular_color = specular_color
        self.ambient_color = ambient_color

    def __repr__(self) -> str:
        return f"Light(direction: {self.direction})"
