import glfw
from OpenGL.GL import *
import random
import numpy as np

# Параметры окна
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900

# Параметры частиц
PARTICLE_RADIUS = 10
PARTICLE_COLOR_POSITIVE = (1.0, 0.0, 0.0)  # Красный
PARTICLE_COLOR_NEGATIVE = (0.0, 0.0, 1.0)  # Синий

# Константы для сил Кулона
K_COULOMB = 0.0001  # Коэффициент силы Кулона
MAX_FORCE_DISTANCE = 100  # Максимальное расстояние, на котором действует отталкивание

particles = []  # Список частиц


def compute_forces():
    for i, particle in enumerate(particles):
        particle['force'] = np.array([0.0, 0.0])
        for j, other_particle in enumerate(particles):
            if i != j:
                # Расчет силы Кулона
                distance = np.linalg.norm(particle['position'] - other_particle['position'])
                force_magnitude = K_COULOMB * (1 / distance ** 2)
                force_direction = (other_particle['position'] - particle['position']) / distance
                force = force_magnitude * force_direction

                # Добавляем отталкивание на коротком расстоянии
                if distance < MAX_FORCE_DISTANCE or particle['charge'] * other_particle['charge'] > 0:
                    force += force_direction * 10 / distance
                particle['force'] += force


def update_particles(delta_time):
    compute_forces()
    for particle in particles:
        # Применение силы к частице
        acceleration = particle['force'] / particle['mass']
        particle['velocity'] += acceleration * delta_time
        particle['position'] += particle['velocity'] * delta_time


def draw_circle(position, radius, color):
    num_segments = 30
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(*color)
    glVertex2f(position[0], position[1])
    for i in range(num_segments + 1):
        angle = i * (2.0 * np.pi / num_segments)
        x = position[0] + radius * np.cos(angle)
        y = position[1] + radius * np.sin(angle)
        glVertex2f(x, y)
    glEnd()


def draw_plus(position, size, color):
    glPushMatrix()
    glTranslatef(position[0], position[1], 0.0)
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2f(-size, size / 4)
    glVertex2f(size, size / 4)
    glVertex2f(size, -size / 4)
    glVertex2f(-size, -size / 4)
    glVertex2f(size / 4, size)
    glVertex2f(size / 4, -size)
    glVertex2f(-size / 4, -size)
    glVertex2f(-size / 4, size)
    glEnd()
    glPopMatrix()


def draw_minus(position, size, color):
    glPushMatrix()
    glTranslatef(position[0], position[1], 0.0)
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2f(-size, size / 4)
    glVertex2f(size, size / 4)
    glVertex2f(size, -size / 4)
    glVertex2f(-size, -size / 4)
    glEnd()
    glPopMatrix()


def draw_particles():
    for particle in particles:
        position = particle['position']
        if particle['charge'] > 0:
            draw_circle(position, PARTICLE_RADIUS, PARTICLE_COLOR_POSITIVE)
            draw_plus(position, PARTICLE_RADIUS / 2, (1.0, 1.0, 1.0))
        else:
            draw_circle(position, PARTICLE_RADIUS, PARTICLE_COLOR_NEGATIVE)
            draw_minus(position, PARTICLE_RADIUS / 2, (1.0, 1.0, 1.0))


def on_mouse_button(window, button, action, mods):
    if action == glfw.PRESS:
        window_x, window_y = glfw.get_window_pos(window)
        width, height = glfw.get_framebuffer_size(window)
        x, y = glfw.get_cursor_pos(window)
        #x = (x - window_x) / width * WINDOW_WIDTH
        #y = (height - (y - window_y)) / height * WINDOW_HEIGHT
        if button == glfw.MOUSE_BUTTON_LEFT:
            particles.append({'position': np.array([x, y]), 'velocity': np.array([0.0, 0.0]), 'mass': 1.0, 'charge': 1})
        elif button == glfw.MOUSE_BUTTON_RIGHT:
            particles.append({'position': np.array([x, y]), 'velocity': np.array([0.0, 0.0]), 'mass': 1.0, 'charge': -1})
        elif button == glfw.MOUSE_BUTTON_MIDDLE:
            particles_to_remove = []
            for particle in particles:
                distance = np.linalg.norm(np.array([x, y]) - particle['position'])
                if distance < PARTICLE_RADIUS:
                    particles_to_remove.append(particle)
            for particle in particles_to_remove:
                particles.remove(particle)



def on_key(window, key, scancode, action, mods):
    if action == glfw.PRESS:
        if key == glfw.KEY_DELETE:
            particles.clear()


def main():
    if not glfw.init():
        return

    window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Charged Particles Simulation", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_mouse_button_callback(window, on_mouse_button)
    glfw.set_key_callback(window, on_key)

    glOrtho(0, WINDOW_WIDTH, WINDOW_HEIGHT, 0, -1, 1)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT)

        update_particles(0.01)
        draw_particles()

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
#    random_positions = [(random.uniform(0, WINDOW_WIDTH), random.uniform(0, WINDOW_HEIGHT)) for _ in range(20)]
#    for position in random_positions:
#        charge = random.choice([1, -1])  # Случайно выбираем заряд частицы
#        particles.append(
#            {'position': np.array(position), 'velocity': np.array([0.0, 0.0]), 'mass': 1.0, 'charge': charge})
    main()
