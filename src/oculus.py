from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import pyrift
import time

class Oculus(object):
  def __init__(self, width, height)
    pyrift.initialize()
    self.width = width
    self.height = height

  def setViewing(self, transArgs):
    glTranslate(*transArgs)
    

  def drawLeft(self, poseOps, args):
    glScissor(0, 0, width/2, height)
    glEnable(GL_SCISSOR_TEST)

    if(args is not None):
      poseOps(*args)
    else:
      poseOps()

    (r, p, y) = pyrift.get_orientation()
    glRotatef(y, 1, 0, 0)
    glRotatef(p, 0, 1, 0)
    glRotatef(r, 0, 0, 1)

    glDisable(GL_SCISSOR_TEST)

  def drawRight(self, poseOps, args):
    glScissor(width/2, 0, width/2, height)
    glEnable(GL_SCISSOR_TEST)

    if(args is not None):
      poseOps(*args)
    else:
      poseOps()

    (r, p, y) = pyrift.get_orientation()
    glRotatef(y, 1, 0, 0)
    glRotatef(p, 0, 1, 0)
    glRotatef(r, 0, 0, 1)

    glDisable(GL_SCISSOR_TEST)
