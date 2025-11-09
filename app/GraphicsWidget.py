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

