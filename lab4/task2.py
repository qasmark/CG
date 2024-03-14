import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
from PyQt5.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


class GLWidget(QOpenGLWidget):
    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        light_position = [10.0, 10.0, 10.0, 0.0]
        light_ambient = [0.2, 0.2, 0.2, 1.0]
        light_diffuse = [1.0, 1.0, 1.0, 1.0]
        light_specular = [1.0, 1.0, 1.0, 1.0]

        glLightfv(GL_LIGHT0, GL_POSITION, light_position)
        glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
        glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glMaterialf(GL_FRONT, GL_SHININESS, 100.0)

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect_ratio = width / height
        gluPerspective(45, aspect_ratio, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0, 0, 10, 0, 0, 0, 0, 1, 0)

        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)

        radius_major = 2.0
        radius_minor = 1.0
        num_segments_major = 50
        num_segments_minor = 25
# передеать в параметры через класс, не через константы
# сделать два тора
        for i in range(num_segments_major):
            glBegin(GL_TRIANGLE_STRIP)
            for j in range(num_segments_minor + 1):
                theta_major = 2.0 * math.pi * i / num_segments_major
                theta_minor = 2.0 * math.pi * j / num_segments_minor

                x = (radius_major + radius_minor * math.cos(theta_major)) * math.cos(theta_minor)
                y = (radius_major + radius_minor * math.cos(theta_major)) * math.sin(theta_minor)
                z = radius_minor * math.sin(theta_major)

                normal_x = math.cos(theta_major) * math.cos(theta_minor)
                normal_y = math.cos(theta_major) * math.sin(theta_minor)
                normal_z = math.sin(theta_major)

                glNormal3f(normal_x, normal_y, normal_z)
                glVertex3f(x, y, z)

                theta_major_next = 2.0 * math.pi * (i + 1) / num_segments_major
                theta_minor_next = 2.0 * math.pi * (j + 1) / num_segments_minor

                x_next = (radius_major + radius_minor * math.cos(theta_major_next)) * math.cos(theta_minor_next)
                y_next = (radius_major + radius_minor * math.cos(theta_major_next)) * math.sin(theta_minor_next)
                z_next = radius_minor * math.sin(theta_major_next)

                normal_x_next = math.cos(theta_major_next) * math.cos(theta_minor_next)
                normal_y_next = math.cos(theta_major_next) * math.sin(theta_minor_next)
                normal_z_next = math.sin(theta_major_next)

                glNormal3f(normal_x_next, normal_y_next, normal_z_next)
                glVertex3f(x_next, y_next, z_next)
            glEnd()

    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)
        self.rotation_x = 0
        self.rotation_y = 0

    def mouseMoveEvent(self, event):
        dx = event.x() - self.last_pos.x()
        dy = event.y() - self.last_pos.y()

        if event.buttons() & Qt.LeftButton:
            self.rotation_x += dy / 2
            self.rotation_y += dx / 2

        self.last_pos = event.pos()
        self.update()

    def mousePressEvent(self, event):
        self.last_pos = event.pos()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.glWidget = GLWidget()
        self.setCentralWidget(self.glWidget)
        self.setWindowTitle("Torus")
        self.resize(800, 600)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

class GLWidget(QOpenGLWidget):
    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        light_position = [10.0, 10.0, 10.0, 0.0]
        light_ambient = [0.2, 0.2, 0.2, 1.0]
        light_diffuse = [1.0, 1.0, 1.0, 1.0]
        light_specular = [1.0, 1.0, 1.0, 1.0]

        glLightfv(GL_LIGHT0, GL_POSITION, light_position)
        glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
        glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glMaterialf(GL_FRONT, GL_SHININESS, 100.0)

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect_ratio = width / height
        gluPerspective(45, aspect_ratio, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0, 0, 10, 0, 0, 0, 0, 1, 0)

        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)

        # Draw torus with smooth shading and calculated normals
        radius_major = 2.0  # Major radius of the torus
        radius_minor = 1.0  # Minor radius of the torus
        num_segments_major = 50  # Number of segments along the major circle
        num_segments_minor = 25  # Number of segments along the minor circle

        for i in range(num_segments_major):
            glBegin(GL_TRIANGLE_STRIP)
            for j in range(num_segments_minor + 1):
                theta_major = 2.0 * math.pi * i / num_segments_major
                theta_minor = 2.0 * math.pi * j / num_segments_minor

                x = (radius_major + radius_minor * math.cos(theta_major)) * math.cos(theta_minor)
                y = (radius_major + radius_minor * math.cos(theta_major)) * math.sin(theta_minor)
                z = radius_minor * math.sin(theta_major)

                glNormal3f(2 * math.cos(theta_major) * math.cos(theta_minor),
                           2 * math.cos(theta_major) * math.sin(theta_minor),
                           2 * math.sin(theta_major))
                glVertex3f(x, y, z)

                theta_major_next = 2.0 * math.pi * (i + 1) / num_segments_major
                theta_minor_next = 2.0 * math.pi * (j + 1) / num_segments_minor

                x_next = (radius_major + radius_minor * math.cos(theta_major_next)) * math.cos(theta_minor_next)
                y_next = (radius_major + radius_minor * math.cos(theta_major_next)) * math.sin(theta_minor_next)
                z_next = radius_minor * math.sin(theta_major_next)

                glNormal3f(2 * math.cos(theta_major_next) * math.cos(theta_minor_next),
                           2 * math.cos(theta_major_next) * math.sin(theta_minor_next),
                           2 * math.sin(theta_major_next))
                glVertex3f(x_next, y_next, z_next)
            glEnd()

    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)
        self.rotation_x = 0
        self.rotation_y = 0

    def mouseMoveEvent(self, event):
        dx = event.x() - self.last_pos.x()
        dy = event.y() - self.last_pos.y()

        if event.buttons() & Qt.LeftButton:
            self.rotation_x += dy / 2
            self.rotation_y += dx / 2

        self.last_pos = event.pos()
        self.update()

    def mousePressEvent(self, event):
        self.last_pos = event.pos()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.glWidget = GLWidget()
        self.setCentralWidget(self.glWidget)
        self.setWindowTitle("Torus with Lighting")
        self.resize(800, 600)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
