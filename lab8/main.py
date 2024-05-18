from sys import exit
import pygame as pg
from datetime import datetime

from objects import Sphere, InfinityChessBoard
from camera import Camera
from skybox import Skybox
from vector import Vector
from light import Light
from ray import Ray
import random

pg.init()
pg.display.init()

screen_size = Vector(1440, 850)
shadow_bias = 0.0001
max_reflections = 6
samples_per_pixel = 10

display = pg.display.set_mode((screen_size.x, screen_size.y))
pg.display.set_caption("Python Raytracer")

pixel_array = pg.PixelArray(display)

camera = Camera(Vector(0, 0, 5), screen_size, 60, focus_distance=15.0, aperture=0.5)
skybox = Skybox("skybox.png")

objects = [
    Sphere(Vector(0, -2, -10), 2, Vector(1, 0, 0), Vector(1, 1, 1), Vector(0.1, 0.1, 0.1), 32),
    Sphere(Vector(5,-2, -15), 2, Vector(0, 1, 0), Vector(1, 1, 1), Vector(0.1, 0.1, 0.1), 32),
    Sphere(Vector(-5, 0, -15), 2, Vector(0, 0, 1), Vector(1, 1, 1), Vector(0.1, 0.1, 0.1), 32),
    InfinityChessBoard(2, Vector(0, 0, 0), Vector(1, 1, 1))
]

light = Light(Vector(-1, 1, -1), 1, Vector(1, 1, 1), Vector(1, 1, 1), Vector(0.2, 0.2, 0.2))


def trace_ray(ray: Ray) -> Vector:
    color = Vector(0, 0, 0)
    intersect, obj = ray.cast(objects)
    normal = False
    if intersect:
        normal = obj.get_normal(intersect)

        # Ambient component
        ambient = obj.ambient_color * light.ambient_color

        # Diffuse component
        light_dir = -light.direction.normalize()
        diffuse_intensity = max(0, normal.dot(light_dir)) * light.strength
        diffuse = obj.diffuse_color * light.diffuse_color * diffuse_intensity

        # Specular component
        view_dir = (camera.position - intersect).normalize()
        reflect_dir = (normal * (2 * normal.dot(light_dir))) - light_dir
        specular_intensity = max(0, view_dir.dot(reflect_dir)) ** obj.shininess
        specular = obj.specular_color * light.specular_color * specular_intensity

        # Combine all components
        color = ambient + diffuse + specular

        # Calculate shadows
        light_ray = Ray(intersect + normal * shadow_bias, light_dir)
        light_intersect, _ = light_ray.cast(objects)
        if light_intersect:
            color *= 0.1 / light.strength
        else:
            color *= normal.dot(-light.direction * light.strength)

    else:
        color = skybox.get_image_coords(ray.direction)
    return color, intersect, normal


for y in range(pg.display.get_window_size()[1]):
    for x in range(pg.display.get_window_size()[0]):
        color_sum = Vector(0, 0, 0)
        for _ in range(samples_per_pixel):
            ray = camera.get_direction(Vector(x + random.uniform(-0.5, 0.5), y + random.uniform(-0.5, 0.5)))
            color, intersect, normal = trace_ray(ray)
            if intersect:
                reflection_ray = Ray(intersect + ray.direction.reflect(normal) * shadow_bias, ray.direction.reflect(normal))
                reflection_color = Vector(0, 0, 0)
                reflection_times = 0
                for reflection in range(max_reflections):
                    new_color, intersect, normal = trace_ray(reflection_ray)
                    if intersect and not isinstance(object,
                                                    InfinityChessBoard):  # Пропускаем отражение от шахматной доски
                        reflection_color += new_color
                        reflection_times += 1
                        reflection_ray = Ray(intersect + reflection_ray.direction.reflect(normal) * shadow_bias,
                                             reflection_ray.direction.reflect(normal))
                    else:
                        break
                color += reflection_color / reflection_times
            color_sum += color
        avg_color = color_sum / samples_per_pixel
        pixel_array[x, y] = avg_color.to_rgb()

    pg.display.flip()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            current_time = datetime.now().strftime("%d%m%Y%H%M%S")
            file_name = f"file_{current_time}.png"
            pg.image.save(display, file_name)
            pg.quit()
            exit()