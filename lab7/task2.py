import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram


class OpenGLWidget(QOpenGLWidget):

    def initializeGL(self):
        vertex_shader = """
        #version 330
        in vec3 position;
        void main()
        {
            gl_Position = vec4(position, 1.0);
        }
        """

        fragment_shader = """
        #version 330
        uniform vec2 center;
        out vec4 fragColor;
        void main()
        {
            float radius = 0.5;
            float thickness = 0.025;
            vec2 center = vec2(1.15, 1.15);
            float dist = distance(center, gl_FragCoord.xy / 400.0);

            if (dist > radius - thickness && dist < radius + thickness) 
            {
                fragColor = vec4(0.0, 0.0, 0.0, 1.0);
            } 
            else if (dist < radius) 
            {
                fragColor = vec4(1.0, 1.0, 1.0, 1.0);
            } 
            else 
            {
                discard;
            }
        }
        """

        self.program = compileProgram(
            compileShader(vertex_shader, GL_VERTEX_SHADER),
            compileShader(fragment_shader, GL_FRAGMENT_SHADER)
        )

        glClearColor(1.0, 1.0, 1.0, 1.0)

        vertices = [
            -1.0, -1.0, 0.0,
             1.0, -1.0, 0.0,
             1.0,  1.0, 0.0,
            -1.0,  1.0, 0.0
        ]
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, len(vertices) * 4, (GLfloat * len(vertices))(*vertices), GL_STATIC_DRAW)

        position = glGetAttribLocation(self.program, "position")
        glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(position)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glUseProgram(self.program)
        center_location = glGetUniformLocation(self.program, "center")
        glUniform2f(center_location, 0.0, 0.0)
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
        glBindVertexArray(0)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ring Visualization")
        self.setGeometry(100, 100, 900, 900)

        self.glWidget = OpenGLWidget(self)
        self.setCentralWidget(self.glWidget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
