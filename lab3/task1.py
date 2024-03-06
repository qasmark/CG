import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
from PyQt5.QtCore import Qt


class OpenGLWidget(QOpenGLWidget):
    def __init__(self):
        super().__init__()

        self.control_points = [(0, 0), (2, 5), (4, -3), (6, 2)]  # Example control points
        self.selected_point_index = None

    def initializeGL(self):
        glClearColor(1, 1, 1, 1)

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(-10, 10, -10, 10)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)

        # Draw axes
        glColor3f(0, 0, 0)  # Black color
        glBegin(GL_LINES)
        glVertex2f(-10, 0)
        glVertex2f(10, 0)
        glVertex2f(0, -10)
        glVertex2f(0, 10)
        glEnd()

        # Draw Bezier curve
        glColor3f(0, 0, 1)  # Blue color
        glBegin(GL_LINE_STRIP)
        for t in range(0, 101):
            point = self.compute_bezier_point(t / 100)
            glVertex2f(*point)
        glEnd()

        # Draw control points
        glColor3f(0, 0, 0)
        glPointSize(5)
        glBegin(GL_POINTS)
        for point in self.control_points:
            glVertex2f(*point)
        glEnd()

        # Draw dotted lines connecting control points
        glEnable(GL_LINE_STIPPLE)
        glLineStipple(1, 0xAAAA)
        glColor3f(0, 0, 0)
        glBegin(GL_LINES)
        for i in range(len(self.control_points) - 1):
            glVertex2f(*self.control_points[i])
            glVertex2f(*self.control_points[i + 1])
        glEnd()
        glDisable(GL_LINE_STIPPLE)

    def compute_bezier_point(self, t):
        n = len(self.control_points) - 1
        x = 0
        y = 0
        for i, (px, py) in enumerate(self.control_points):
            coefficient = math.comb(n, i) * (1 - t) ** (n - i) * t ** i
            x += px * coefficient
            y += py * coefficient
        return x, y

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            x = event.pos().x()
            y = event.pos().y()
            normalized_x = -10 + 20 * (x / self.width())
            normalized_y = -10 + 20 * (1 - y / self.height())
            for i, point in enumerate(self.control_points):
                distance = ((normalized_x - point[0]) ** 2 + (normalized_y - point[1]) ** 2) ** 0.5
                if distance < 0.5:  # Clicked within 0.5 units from the point
                    self.selected_point_index = i
                    break
            if self.selected_point_index is None:  # If no point selected, add a new point
                self.control_points.append((normalized_x, normalized_y))
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.selected_point_index is not None:
            x = event.pos().x()
            y = event.pos().y()
            normalized_x = -10 + 20 * (x / self.width())
            normalized_y = -10 + 20 * (1 - y / self.height())
            self.control_points[self.selected_point_index] = (normalized_x, normalized_y)
            self.update()

    def mouseReleaseEvent(self, event):
        self.selected_point_index = None


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OpenGL Bezier Curve")
        self.setGeometry(100, 100, 800, 600)

        self.glWidget = OpenGLWidget()
        self.setCentralWidget(self.glWidget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
