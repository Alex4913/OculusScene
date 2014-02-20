from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import time

from src import oculus

class Display(object):
  (width, height) = (1280, 720)
  frameSize = (width, height)
  frameName = "Oculus"
  timerDelay = 20

  clearColor = (0, 0, 0, 0)
  
  def initGL(self):
    glClearColor(*Display.clearColor)

  def initGLUT(self):
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(*Display.frameSize)
    glutCreateWindow(Display.frameName)
  
    glutDisplayFunc(self.drawWrapper)
    glutIdleFunc(self.draw)
    glutTimerFunc(Display.timerDelay, self.timerFired, 0)
    glutMouseFunc(self.mouse)
    glutKeyboardFunc(self.keyboard)
    glutSpecialFunc(self.specialKeys)
    glutReshapeFunc(self.reshape)

    try:
      glutCloseFunc(self.close)
    except:
      glutWMCloseFunc(self.close)

  def preGL(self):
    glShadeModel(GL_FLAT)
    glEnable(GL_DEPTH_TEST)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

  def postGL(self):
    glutSwapBuffers()
    time.sleep(0.042)
  
  def timerFired(self, value):
    glutTimerFunc(Display.timerDelay, self.timerFired, value)

  def mouse(self, mouseButton, buttonState, x, y):
    pass

  def keyboard(self, key, x, y):
    pass

  def specialKeys(self, key, x, y):
    pass

  def draw(self):
    self.oculus.drawLeft()
    self.oculus.drawRight()

  def drawWrapper(self):
    self.preGL()
    self.draw()
    self.postGL()

  def reshape(self, width, height):
    if(self.width != width or self.height != height):
      glutReshapeWindow(self.width, self.height)

  def close(self):
    pass

  def __init__(self):
    self.initGL()
    self.initGLUT()
    self.oculus = oculus.Oculus(width, height)

  def start(self):
    # Blocks 
    glutMainLoop()
