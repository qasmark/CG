import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import pi

class PieChartWidget(QOpenGLWidget):
    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 1.33, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)

        radius = 1.0
        slices = 5
        colors = [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0), (1.0, 1.0, 0.0), (1.0, 0.0, 1.0)]
        angles = [2 * pi / slices] * slices

        glLoadIdentity()
        glTranslatef(0.0, 0.0, -5.0)

        for i in range(slices):
            glColor3f(*colors[i])
            glBegin(GL_TRIANGLE_FAN)
            glVertex3f(0.0, 0.0, 0.0)
            for j in range(int(360 / 5)):
                glVertex3f(radius * np.sin(j * angles[i]), radius * np.cos(j * angles[i]), 0.0)
            glEnd()
            radius -= 0.2

        glDisable(GL_DEPTH_TEST)

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Pie Chart")
        self.setGeometry(100, 100, 800, 600)
        self.chart_widget = PieChartWidget(self)
        self.setCentralWidget(self.chart_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
