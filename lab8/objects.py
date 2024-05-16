from __future__ import annotations

from math import sqrt

from vector import Vector
from ray import Ray


class Tetrahedron:
    __slots__ = ('left_point', 'right_point', 'back_point', 'upper_point','color')

    def __init__(self, left_point: Vector, right_point: Vector, back_point: Vector, upper_point: Vector, color: Vector):
        self.left_point = left_point
        self.right_point = right_point
        self.back_point = back_point
        self.upper_point = upper_point
        self.color = color

    def __repr__(self) -> str:
        return f"Tetrahedron(left_point: {self.left_point}, right_point: {self.right_point},\n" \
               f" back_point: {self.back_point}, back_point: {self.back_point}"

    def intersection(self, ray: Ray) -> bool | Vector:
        pass



class Sphere:
    __slots__ = ('center', 'radius', 'color')

    def __init__(self, center: Vector, radius: int | float, color: Vector):
        self.center = center
        self.radius = radius
        self.color = color

    def __repr__(self) -> str:
        return f"Sphere(center: {self.center}, radius: {self.radius}, color: {self.color})"

    def intersection(self, ray: Ray) -> bool | Vector:
        l = self.center - ray.origin # вектор от начала луча до сцены
        adj = l.dot(ray.direction) # проекция вектора на направление луча
        d2 = l.dot(l) - (adj * adj) # раст. от центра луча до сферы (квадрат)
        radius2 = self.radius * self.radius # квадрат радиуса сферы
        if d2 > radius2:
            return False
        thc = sqrt(radius2 - d2)
        t0 = adj - thc # расстояние от начала луча до точек пересечения
        t1 = adj + thc
        if t0 < 0 and t1 < 0:
            return False
        distance = t0 if t0 < t1 else t1 # возвращаем ближайшую
        return ray.origin + ray.direction * distance

    def get_color(self, hit_position: Vector) -> Vector:
        return self.color

    def get_normal(self, hit_position: Vector) -> Vector:
        return (hit_position - self.center).normalize()


class InfinityChessBoard:
    __slots__ = ('y', 'color1', 'color2')

    def __init__(self, y: int | float, color1: Vector, color2: Vector):
        self.y = y
        self.color1 = color1
        self.color2 = color2

    def __repr__(self) -> str:
        return f"Checkerboard(y: {self.y}, color1: {self.color1}, color2: {self.color2})"

    def intersection(self, ray: Ray) -> bool | Vector:
        if ray.direction.y < 0:
            return False
        distance = self.y - ray.origin.y
        steps = distance / ray.direction.y
        return ray.origin + ray.direction * steps

    def get_color(self, hit_position: Vector) -> Vector:
        if round(hit_position.x) % 6 <= 2 and round(hit_position.z) % 6 <= 2 or \
                round(hit_position.x) % 6 >= 3 and round(hit_position.z) % 6 >= 3:
            return self.color2
        return self.color1

    def get_normal(self, hit_position: Vector) -> Vector:
        return Vector(0, -1, 0)