import math
import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
import numpy as np

class GLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)
        self.setMinimumSize(800, 600)
        self.resize(600, 800)
        self.angleX = 0
        self.angleY = 0
        self.lastPos = None
        self.colors = []

    def initializeGL(self):
        glClearColor(0.2, 0.2, 0.2, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        light_position = [4.0, 0.0, 0.0, 1.0]
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

        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.generate_colors()

    def generate_colors(self):
        self.colors = []
        for _ in range(20):
            color = [random.random() for _ in range(3)] + [0.5]
            self.colors.append(color)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / h, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -5.0)
        glRotatef(self.angleX, 1.0, 0.0, 0.0)
        glRotatef(self.angleY, 0.0, 1.0, 0.0)


        glEnable(GL_CULL_FACE)


        glCullFace(GL_FRONT)
        glColor3f(0.0, 0.0, 0.0)
        self.draw_icosahedron()

        glCullFace(GL_BACK)
        self.draw_icosahedron()

        glDisable(GL_CULL_FACE)



    def draw_icosahedron(self):
        t = (1.0 + math.sqrt(5.0)) / 2.0
        vertices = [
            (-1, t, 0), (1, t, 0), (-1, -t, 0), (1, -t, 0),
            (0, -1, t), (0, 1, t), (0, -1, -t), (0, 1, -t),
            (t, 0, -1), (t, 0, 1), (-t, 0, -1), (-t, 0, 1)
        ]
        faces = [
            (0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11),
            (1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6), (7, 1, 8),
            (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9),
            (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1)
        ]
        edges = [
            (0, 11), (0, 5), (5, 11),
            (0, 1), (1, 5),
            (1, 7), (0, 7),
            (0, 10), (7, 10), (10, 11),
            (1, 9), (5, 9),
            (4, 5), (4, 11),
            (2, 11), (2, 10),
            (6, 10), (6, 7),
            (1, 8), (7, 8),
            (3, 4), (3, 9), (4, 9),
            (2, 3), (2, 4),
            (3, 6), (2, 6),
            (3, 8), (6, 8),
            (8, 9)
        ]

        glBegin(GL_TRIANGLES)
        for i, face in enumerate(faces):
            color = self.colors[i]

            v0 = np.array(vertices[face[0]])
            v1 = np.array(vertices[face[1]])
            v2 = np.array(vertices[face[2]])
            normal = np.cross(v1 - v0, v2 - v0)
            normal /= np.linalg.norm(normal)
            glNormal3fv(normal)

            glColor4fv(color)
            for vertexIndex in face:
                glVertex3fv(vertices[vertexIndex])
        glEnd()

        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_LINES)
        for edge in edges:
            for vertexIndex in edge:
                glVertex3fv(vertices[vertexIndex])
        glEnd()

    def mousePressEvent(self, event):
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        if self.lastPos:
            dx = event.x() - self.lastPos.x()
            dy = event.y() - self.lastPos.y()
            self.angleX += dy
            self.angleY += dx
            self.update()
            self.lastPos = event.pos()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.glWidget = GLWidget()
        self.setWindowTitle("Icosahedron")
        self.setCentralWidget(self.glWidget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
