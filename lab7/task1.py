from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtOpenGL import QGLWidget
from OpenGL.GL import *
from OpenGL.GLUT import *
import math

vertex_shader_source = """
#version 330 core

in vec4 position;
out vec4 fragColor;

float CalculateRadius(float x)
{
    return (1.0 + sin(x)) *
           (1.0 + 0.9 * cos(8.0*x)) *
           (1.0 + 0.1 * cos(24.0 * x)) *
           (0.5 + 0.05 * cos(140.0 * x));
}

void main()
{
    float x = position.x;
    float R = CalculateRadius(x);
    
    vec4 newPosition;
    newPosition.x = R * cos(x) * 0.5;
    newPosition.y = R * sin(x) * 0.5;
    newPosition.z = position.z;
    newPosition.w = position.w;
    
   
    gl_Position = newPosition;
}

"""

fragment_shader_source = """
#version 330 core
out vec4 fragColor;

void main()
{
    float x = gl_FragCoord.x / 1600.0;
    x = fract(x);
    vec3 color = vec3(1.0 - x, 0.0, x);
    fragColor = vec4(color, 1.0);
}
"""


class GLWidget(QGLWidget):
    def initializeGL(self):
        self.program = glCreateProgram()
        vertex_shader = glCreateShader(GL_VERTEX_SHADER)
        fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)

        glShaderSource(vertex_shader, vertex_shader_source)
        glShaderSource(fragment_shader, fragment_shader_source)

        glCompileShader(vertex_shader)
        if not glGetShaderiv(vertex_shader, GL_COMPILE_STATUS):
            print("Vertex shader compilation error:", glGetShaderInfoLog(vertex_shader).decode())

        glCompileShader(fragment_shader)
        if not glGetShaderiv(fragment_shader, GL_COMPILE_STATUS):
            print("Fragment shader compilation error:", glGetShaderInfoLog(fragment_shader).decode())

        glAttachShader(self.program, vertex_shader)
        glAttachShader(self.program, fragment_shader)

        glLinkProgram(self.program)

        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.program)

        glBegin(GL_LINE_STRIP)
        for i in range(1000):
            glVertex2f(i * (2 * math.pi / 1000), 0.0)
        glEnd()

        glUseProgram(0)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        aspect_ratio = w / h

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if aspect_ratio > 1:
            glOrtho(-2.5 * aspect_ratio, 2.5 * aspect_ratio, -2.5, 2.5, -1.0, 1.0)
        else:
            glOrtho(-2.5, 2.5, -2.5 / aspect_ratio, 2.5 / aspect_ratio, -1.0, 1.0)

        glMatrixMode(GL_MODELVIEW)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        central_widget = QWidget()
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.glWidget = GLWidget()
        layout.addWidget(self.glWidget)

        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.setGeometry(100, 100, 800, 600)
    mainWindow.setWindowTitle("Curved Line Shader")
    mainWindow.show()
    sys.exit(app.exec_())
