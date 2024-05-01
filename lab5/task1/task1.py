from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
from PyQt5.QtCore import QTimer, Qt
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image


def draw_sphere(radius, slices, stacks):
    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluSphere(quadric, radius, slices, stacks)

# def draw_sphere(radius, slices, stacks):
#     for i in range(stacks):
#         lat0 = pi * (-0.5 + (i) / stacks)
#         z0 = sin(lat0)
#         zr0 = cos(lat0)
#
#         lat1 = pi * (-0.5 + (i + 1) / stacks)
#         z1 = sin(lat1)
#         zr1 = cos(lat1)
#
#         # Start drawing strips
#         glBegin(GL_QUAD_STRIP)
#         for j in range(slices + 1):
#             lng = 2 * pi * (j - 1) / slices
#             x = cos(lng)
#             y = sin(lng)
#
#             glTexCoord2f((j - 1) / slices, i / stacks)
#             glVertex3f(x * zr0 * radius, y * zr0 * radius, z0 * radius)
#
#             glTexCoord2f((j - 1) / slices, (i + 1) / stacks)
#             glVertex3f(x * zr1 * radius, y * zr1 * radius, z1 * radius)
#
#         glEnd()


def load_texture(file_path):
    image = Image.open(file_path)
    width, height = image.size
    image_data = image.tobytes("raw", "RGBX", 0, -1)
    texture_id = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texture_id)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    return texture_id


def load_texture_skybox(filename):
    image = Image.open(filename)
    width, height = image.size
    side_length = width // 4
    textures = []

    for i in range(6):
        left = side_length * i
        top = 0
        right = side_length * (i + 1)
        bottom = side_length
        texture_image = image.crop((left, top, right, bottom))
        texture_data = texture_image.tobytes("raw", "RGBX", 0, -1)
        texture_id = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, texture_id)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, side_length, side_length, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        textures.append(texture_id)

    return textures


class SolarSystemWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.sun_angle = 7.25
        self.earth_angle = 23.5
        self.moon_angle = 0
        self.camera_distance = 10.0
        self.camera_angle_x = 0.0
        self.camera_angle_y = 0.0
        self.last_mouse_pos = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(30)
        self.sun_texture = None
        self.earth_texture = None
        self.moon_texture = None
        self.skybox_textures = None
        self.skybox_size = 50.0

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, self.width() / self.height(), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

        self.sun_texture = load_texture(r"Textures\sun.png")
        self.earth_texture = load_texture(r"Textures\earth.png")
        self.moon_texture = load_texture(r"Textures\moon.jpg")
        self.skybox_textures = load_texture_skybox(r"Textures\skybox.jpg")

        for texture_id in self.skybox_textures:
            glBindTexture(GL_TEXTURE_2D, texture_id)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        light_position = [0.0, 0.0, 0.0, 1.0]
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)

        light_ambient = [0.0, 0.0, 0.0, 1.0]
        glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)

        light_diffuse = [1.0, 1.0, 1.0, 1.0]
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)

        light_specular = [1.0, 1.0, 1.0, 1.0]
        glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        self.draw_skybox()
        # Moving camera
        glTranslatef(0.0, 0.0, -self.camera_distance)
        glRotatef(self.camera_angle_x, 1.0, 0.0, 0.0)
        glRotatef(self.camera_angle_y, 0.0, 1.0, 0.0)

        # Sun
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.sun_texture)
        glColor3f(1.0, 1.0, 1.0)
        draw_sphere(1.0, 50, 50)
        glDisable(GL_TEXTURE_2D)

        # Earth
        glPushMatrix()
        glRotatef(self.sun_angle, 0.0, 1.0, 0.0)
        glTranslatef(5.0, 0.0, 0.0)
        glRotatef(self.earth_angle, 0.0, 1.0, 0.0)

        earth_ambient = [0.1, 0.1, 0.1, 1.0]
        earth_diffuse = [0.5, 0.5, 0.5, 1.0]
        earth_specular = [0.5, 0.5, 0.5, 1.0]
        earth_shininess = 50.0
        glMaterialfv(GL_FRONT, GL_AMBIENT, earth_ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, earth_diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, earth_specular)
        glMaterialf(GL_FRONT, GL_SHININESS, earth_shininess)

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.earth_texture)
        glColor3f(1.0, 1.0, 1.0)
        draw_sphere(0.5, 50, 50)

        # Moon
        glPushMatrix()
        glRotatef(self.moon_angle, 0.0, 1.0, 0.0)
        glTranslatef(1.0, 0.0, 0.0)

        moon_ambient = [0.1, 0.1, 0.1, 1.0]
        moon_diffuse = [0.3, 0.3, 0.3, 1.0]
        moon_specular = [0.3, 0.3, 0.3, 1.0]
        moon_shininess = 20.0
        glMaterialfv(GL_FRONT, GL_AMBIENT, moon_ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, moon_diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, moon_specular)
        glMaterialf(GL_FRONT, GL_SHININESS, moon_shininess)

        glBindTexture(GL_TEXTURE_2D, self.moon_texture)
        draw_sphere(0.2, 50, 50)

        glPopMatrix()
        glPopMatrix()

    def draw_skybox(self):
        glPushMatrix()

        glLoadIdentity()
        glTranslatef(0, 0, -self.camera_distance)
        glRotatef(self.camera_angle_x, 1, 0, 0)
        glRotatef(self.camera_angle_y, 0, 1, 0)

        glDisable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)

        # Front side
        glBindTexture(GL_TEXTURE_2D, self.skybox_textures[0])
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(-50, -50, -50)
        glTexCoord2f(1, 0)
        glVertex3f(50, -50, -50)
        glTexCoord2f(1, 1)
        glVertex3f(50, 50, -50)
        glTexCoord2f(0, 1)
        glVertex3f(-50, 50, -50)
        glEnd()

        # Back side
        glBindTexture(GL_TEXTURE_2D, self.skybox_textures[1])
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(-50, -50, 50)
        glTexCoord2f(1, 0)
        glVertex3f(50, -50, 50)
        glTexCoord2f(1, 1)
        glVertex3f(50, 50, 50)
        glTexCoord2f(0, 1)
        glVertex3f(-50, 50, 50)
        glEnd()

        # Upper side
        glBindTexture(GL_TEXTURE_2D, self.skybox_textures[2])
        glBegin(GL_QUADS)
        glTexCoord2f(0, 1)
        glVertex3f(-50, 50, -50)
        glTexCoord2f(0, 0)
        glVertex3f(-50, 50, 50)
        glTexCoord2f(1, 0)
        glVertex3f(50, 50, 50)
        glTexCoord2f(1, 1)
        glVertex3f(50, 50, -50)
        glEnd()

        # Downside
        glBindTexture(GL_TEXTURE_2D, self.skybox_textures[3])
        glBegin(GL_QUADS)
        glTexCoord2f(1, 1)
        glVertex3f(-50, -50, -50)
        glTexCoord2f(1, 0)
        glVertex3f(50, -50, -50)
        glTexCoord2f(0, 0)
        glVertex3f(50, -50, 50)
        glTexCoord2f(0, 1)
        glVertex3f(-50, -50, 50)
        glEnd()

        # Left side
        glBindTexture(GL_TEXTURE_2D, self.skybox_textures[4])
        glBegin(GL_QUADS)
        glTexCoord2f(1, 1)
        glVertex3f(-50, -50, -50)
        glTexCoord2f(0, 1)
        glVertex3f(-50, -50, 50)
        glTexCoord2f(0, 0)
        glVertex3f(-50, 50, 50)
        glTexCoord2f(1, 0)
        glVertex3f(-50, 50, -50)
        glEnd()

        # Right side
        glBindTexture(GL_TEXTURE_2D, self.skybox_textures[5])
        glBegin(GL_QUADS)
        glTexCoord2f(0, 1)
        glVertex3f(50, -50, -50)
        glTexCoord2f(1, 1)
        glVertex3f(50, -50, 50)
        glTexCoord2f(1, 0)
        glVertex3f(50, 50, 50)
        glTexCoord2f(0, 0)
        glVertex3f(50, 50, -50)
        glEnd()

        glEnable(GL_DEPTH_TEST)
        glDisable(GL_TEXTURE_2D)

        glPopMatrix()

    def update_animation(self):
        self.sun_angle += 0.1
        self.earth_angle += 1.0
        self.update()

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.last_mouse_pos = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            if self.last_mouse_pos:
                delta = event.pos() - self.last_mouse_pos
                self.camera_angle_y += delta.x() / 5.0
                self.camera_angle_x += delta.y() / 5.0
                self.last_mouse_pos = event.pos()
                self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_mouse_pos = None

    def wheelEvent(self, event):
        delta = event.angleDelta().y() / 120.0
        self.camera_distance -= delta
        self.update()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Sun, earth and moon")
        self.central_widget = SolarSystemWidget(self)
        self.setCentralWidget(self.central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
