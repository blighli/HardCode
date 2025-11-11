from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from OpenGL.GL import *

class GraphicsWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super(GraphicsWidget, self).__init__(parent)

    def initializeGL(self):
        # Initialize OpenGL settings here
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glEnable(GL_COLOR_MATERIAL)
        glClearColor(0.0, 0.0, 0.0, 1.0)  # Set clear color to black
        # glClearColor(1.0, 1.0, 1.0, 1.0)  # Set clear color to white

        # Get OpenGL version information
        vendor = glGetString(GL_VENDOR).decode('utf-8')
        renderer = glGetString(GL_RENDERER).decode('utf-8')
        version = glGetString(GL_VERSION).decode('utf-8')
        shader_version = glGetString(GL_SHADING_LANGUAGE_VERSION).decode('utf-8')

        print(f"OpenGL Vendor: {vendor}")
        print(f"OpenGL Renderer: {renderer}")
        print(f"OpenGL Version: {version}")
        print(f"GLSL Version: {shader_version}")


    def resizeGL(self, w: int, h: int):
        # Handle resizing of the OpenGL viewport here
        glViewport(0, 0, w, h)

    def paintGL(self):
        # Render OpenGL content here
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glBegin(GL_TRIANGLES)
        glColor3f(1.0, 0.0, 0.0)  # 红色
        glVertex3f(-0.5, -0.5, 0.0)
        glColor3f(0.0, 1.0, 0.0)  # 绿色
        glVertex3f(0.5, -0.5, 0.0)
        glColor3f(0.0, 0.0, 1.0)  # 蓝色
        glVertex3f(0.0, 0.5, 0.0)
        glEnd()

