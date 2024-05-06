from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget, QLabel
from PyQt5.QtCore import QTimer, pyqtSignal, Qt
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image
import random

class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.openglWidget = None
        self.rotation_label = None
        self.setWindowTitle("Memory Trainer 3D")
        self.setGeometry(100, 100, 800, 600)

        self.init_ui()

    def init_ui(self):
        self.openglWidget = MyOpenGLWidget(self)
        self.setCentralWidget(self.openglWidget)

        self.rotation_label = QLabel(self)
        self.rotation_label.setGeometry(10, 30, 200, 40)
        self.rotation_label.setStyleSheet("background-color: rgba(255, 255, 255, 0.5);"
                                          "border: 2px solid black;"
                                          "color: black;")
        self.rotation_label.setFont(QFont("Arial", 16))
        self.rotation_label.setAlignment(Qt.AlignCenter)
        self.rotation_label.setText("Rotations: 0")

        menubar = self.menuBar()
        game_menu = menubar.addMenu('Game Mode')

        easy_action = game_menu.addAction('Easy (4x3)')
        easy_action.triggered.connect(lambda: self.openglWidget.set_game_mode(4, 3))

        medium_action = game_menu.addAction('Medium (6x5)')
        medium_action.triggered.connect(lambda: self.openglWidget.set_game_mode(6, 5))

        hard_action = game_menu.addAction('Hard (8x7)')
        hard_action.triggered.connect(lambda: self.openglWidget.set_game_mode(8, 7))

        self.openglWidget.rotation_count_changed.connect(self.update_rotation_label)

    def update_rotation_label(self, count):
        self.rotation_label.setText(f"Rotations: {count}")


class MyOpenGLWidget(QOpenGLWidget):
    rotation_count_changed = pyqtSignal(int)

    def __init__(self, parent):
        super().__init__(parent)
        self.grid_width = 4
        self.grid_height = 3
        self.texture_id = None
        self.tile_states = [[False for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.clicked_tile = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.close_tiles)
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.animate_tile_rotation)
        self.animation_angle = 0
        self.animation_duration = 500  # Duration of animation
        self.animation_frame_interval = 16  # Frame moment
        self.animation_frame_count = int(self.animation_duration / self.animation_frame_interval)
        self.current_animation_frame = 0
        self.tile_textures = {}
        self.tile_numbers = {}
        self.rotation_counts = {
            (4, 3): 0,
            (6, 5): 0,
            (8, 7): 0
        }

    def load_all_tile_textures(self):
        self.tile_textures = {}

        for i in range(1, 17):
            texture_path = f"Textures/tile_{i}.png"
            texture_id = self.load_texture(texture_path)
            if texture_id is not None:
                self.tile_textures[f"tile_{i}"] = texture_id
                self.tile_numbers[(i // 2, (i - 1) % 2)] = i
            else:
                print(f"Не удалось загрузить текстуру: {texture_path}")

    def initializeGL(self):
        glClearColor(0.2, 0.2, 0.2, 1.0)
        glEnable(GL_DEPTH_TEST)

        self.texture_id = self.load_texture("Textures/back.png")
        self.load_all_tile_textures()

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect_ratio = width / height
        gluPerspective(45, aspect_ratio, 0.1, 100)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.5, -10.0)
        glRotatef(-30, 1, 0, 0)

        tile_size = 1.0
        gap = 0.1

        grid_width = self.grid_width
        grid_height = self.grid_height

        if grid_width > self.width() or grid_height > self.height():
            scale_factor = min(self.width() / grid_width, self.height() / grid_height)
            tile_size *= scale_factor
            gap *= scale_factor

        start_pos_x = -((tile_size + gap) * grid_width) / 2.0
        start_pos_y = -((tile_size + gap) * grid_height) / 2.0

        glEnable(GL_TEXTURE_2D)

        for i in range(grid_height):
            for j in range(grid_width):
                glPushMatrix()
                if self.tile_states[i][j]:
                    if (i, j) in self.tile_textures:
                        glBindTexture(GL_TEXTURE_2D, self.tile_textures[(i, j)])
                    else:
                        glBindTexture(GL_TEXTURE_2D, self.texture_id)

                    if self.clicked_tile == (i, j):
                        # If tile open then use texture tile (doesn't work)
                        # TODO: fix
                        glBindTexture(GL_TEXTURE_2D, self.tile_textures[f"tile_{self.tile_numbers[(i, j)]}"])

                        glTranslatef(start_pos_x + j * (tile_size + gap) + tile_size / 2,
                                     start_pos_y + i * (tile_size + gap) + tile_size / 2, 0)
                        glRotatef(self.animation_angle, 0, 1, 0)
                        glTranslatef(-start_pos_x - j * (tile_size + gap) - tile_size / 2,
                                     -start_pos_y - i * (tile_size + gap) - tile_size / 2, 0)
                else:
                    glBindTexture(GL_TEXTURE_2D, self.texture_id)

                glBegin(GL_QUADS)
                glTexCoord2f(0.0, 0.0)
                glVertex3f(start_pos_x + j * (tile_size + gap), start_pos_y + i * (tile_size + gap), 0.0)
                glTexCoord2f(1.0, 0.0)
                glVertex3f(start_pos_x + (j + 1) * tile_size + j * gap, start_pos_y + i * (tile_size + gap), 0.0)
                glTexCoord2f(1.0, 1.0)
                glVertex3f(start_pos_x + (j + 1) * tile_size + j * gap, start_pos_y + (i + 1) * tile_size + i * gap,
                           0.0)
                glTexCoord2f(0.0, 1.0)
                glVertex3f(start_pos_x + j * (tile_size + gap), start_pos_y + (i + 1) * tile_size + i * gap, 0.0)
                glEnd()
                glPopMatrix()

        glDisable(GL_TEXTURE_2D)

    def generate_image_deck(self, size):
        num_tiles = size[0] * size[1]
        num_pairs = num_tiles // 2

        all_images = [f'Textures/tile_{i}.png' for i in range(1, num_pairs + 1)]
        image_deck = all_images * 2

        random.shuffle(image_deck)

        return image_deck

    def set_game_mode(self, width, height):
        self.grid_width = width
        self.grid_height = height
        self.tile_states = [[False for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.rotation_counts[(self.grid_width, self.grid_height)] = 0
        self.rotation_count_changed.emit(self.rotation_counts[(self.grid_width, self.grid_height)])
        self.clicked_tile = None
        self.timer.stop()
        self.animation_timer.stop()
        self.update()

    def load_texture(self, file_path):
        img = Image.open(file_path)
        img_data = img.convert("RGBA").tobytes("raw", "RGBA")
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        return texture_id

    def mousePressEvent(self, event):
        x = event.x()
        y = event.y()

        viewport = glGetIntegerv(GL_VIEWPORT)
        win_x = x
        win_y = viewport[3] - y
        z = glReadPixels(win_x, win_y, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)

        win_x = x
        win_y = viewport[3] - y
        model_view = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection_view = glGetDoublev(GL_PROJECTION_MATRIX)
        obj_x, obj_y, obj_z = gluUnProject(win_x, win_y, z[0][0], model_view, projection_view, viewport)

        tile_size = 0.13
        gap = 0.1

        start_pos_x = -((tile_size + gap) * self.grid_width) / 2.0
        start_pos_y = -((tile_size + gap) * self.grid_height) / 2.0

        i = int((obj_y - start_pos_y) / (tile_size + gap))
        j = int((obj_x - start_pos_x) / (tile_size + gap))

        if 0 <= i < self.grid_height and 0 <= j < self.grid_width:
            if not self.tile_states[i][j]:
                # Если плитка не открыта, открываем ее
                # TODO: fix cause it does'nt show when it has status open
                self.rotation_counts[(self.grid_width, self.grid_height)] += 1
                self.rotation_count_changed.emit(self.rotation_counts[(self.grid_width, self.grid_height)])
                self.tile_states[i][j] = True
                self.clicked_tile = (i, j)
                self.animation_angle = 0
                self.animation_timer.start(self.animation_frame_interval)
                self.update()
            else:
                # Если плитка уже открыта, закрываем ее
                # TODO: fix
                self.tile_states[i][j] = False
                self.clicked_tile = None
                self.current_animation_frame = 0
                self.update()

    def open_tile(self, i, j):
        # Открывает плитку с координатами (i, j) и устанавливает соответствующую текстуру
        # TODO: fix
        self.rotation_counts[(self.grid_width, self.grid_height)] += 1
        self.rotation_count_changed.emit(self.rotation_counts[(self.grid_width, self.grid_height)])
        self.tile_states[i][j] = True
        self.clicked_tile = (i, j)
        self.animation_angle = 0
        self.animation_timer.start(self.animation_frame_interval)
        self.update()

    def animate_tile_rotation(self):
        self.animation_angle += 180 / self.animation_frame_count
        self.current_animation_frame += 1
        self.update()

        if self.current_animation_frame >= self.animation_frame_count:
            self.animation_timer.stop()
            self.close_tiles()

    def close_tiles(self):
        if self.clicked_tile:
            self.tile_states[self.clicked_tile[0]][self.clicked_tile[1]] = False
            self.clicked_tile = None
            self.current_animation_frame = 0
            self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec_())
