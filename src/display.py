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

  clearColor = (0.5, 0.5, 0.5, 0.5)
  defaultColor = (1, 1, 1)
  
  def initGL(self):
    glClearColor(*Display.clearColor)

  def initGLUT(self):
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(*Display.frameSize)
    glutCreateWindow(Display.frameName)
  
    glutDisplayFunc(self.drawWrapper)
    glutIdleFunc(self.drawWrapper)
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

    # Set up colors and clear buffers
    glClearColor(*Display.clearColor)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(*Display.defaultColor)
    glLoadIdentity()
   
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Degree of FOV, width / height ratio, min dist, max dist
    gluPerspective(60, float(self.width) / self.height, 0.2, 1000)
    glMatrixMode(GL_MODELVIEW)
    #gluLookAt(1, 1, .6, 0, 0, 0, 0, 0, 1)

  def postGL(self):
    glutSwapBuffers()
    time.sleep(0.042)
  
  def timerFired(self, value):
    glutTimerFunc(Display.timerDelay, self.timerFired, value)

  def mouse(self, mouseButton, buttonState, x, y):
    pass

  def keyboard(self, key, x, y):
    self.oculus.calibrate()

  def specialKeys(self, key, x, y):
    pass

  def draw(self):
    self.pos = (0, 0, 0)
    glutWireCube(0.1)

  def drawWrapper(self):
    self.preGL()
    #self.draw()
    self.oculus.draw(self.draw, self.pos)
    self.postGL()

  def reshape(self, width, height):
    if(self.width != width or self.height != height):
      glutReshapeWindow(self.width, self.height)
      self.oculus.width = width
      self.oculus.height = height

  def close(self):
    pass

  def __init__(self):
    self.initGL()
    self.initGLUT()

    self.pos = (0, 0, 0)
    self.oculus = oculus.Oculus(Display.width, Display.height)

  def start(self):
    # Blocks 
    glutMainLoop()
