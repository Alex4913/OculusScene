from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import pyrift
import time, math

class Oculus(object):
  eyeDx = 0.01

  def __init__(self, width, height):
    pyrift.initialize()
    self.width = width
    self.height = height
    self.calibPoint = (0, 0, 0)

  def calibrate(self):
    self.calibPoint = pyrift.get_orientation()

  def getOrientation(self):
    rpy = map(lambda (x, y):y-x, zip(self.calibPoint, pyrift.get_orientation()))
    return rpy

  def preGL(self):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Degree of FOV, width / height ratio, min dist, max dist
    gluPerspective(60, (self.width/2.0) / self.height, 0.2, 1000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClear(GL_DEPTH_BUFFER_BIT)

  def draw(self, drawFunc, pos):
    rpy = self.getOrientation()

    self.leftEye(pos, rpy, drawFunc)
    self.rightEye(pos, rpy, drawFunc)

  def leftEye(self, pos, rpy, drawFunc):
    (x, y, z) = pos
    (roll, pitch, yaw) = rpy

    glPushMatrix()
    glViewport(0, 0, self.width/2, self.height)
    self.preGL()

    # Do translations for correct Oculus Viewing
    glRotatef((pitch * 360) / (2 * math.pi), 1, 0, 0)
    glRotatef((roll * 360) / (2 * math.pi), 0, 1, 0)
    lookX = math.cos(yaw) + x
    lookY = math.sin(yaw) + y
    offsetX = Oculus.eyeDx * math.cos((math.pi / 2) - yaw)
    offsetY = Oculus.eyeDx * math.sin((math.pi / 2) - yaw)
    gluLookAt(lookX+offsetX, lookY+offsetY, z, x+offsetX, y+offsetY, z, 0, 0, 1)

    drawFunc()

    glDisable(GL_SCISSOR_TEST)
    glPopMatrix()

  def rightEye(self, pos, rpy, drawFunc):
    (x, y, z) = pos
    (roll, pitch, yaw) = rpy

    glPushMatrix()
    glViewport(self.width/2, 0, self.width/2, self.height)
    self.preGL()

    # Do translations for correct Oculus Viewing
    glRotatef((pitch * 360) / (2 * math.pi), 1, 0, 0)
    glRotatef((roll * 360) / (2 * math.pi), 0, 1, 0)
    lookX = math.cos(yaw) + x
    lookY = math.sin(yaw) + y
    offsetX = -Oculus.eyeDx * math.cos((math.pi / 2) - yaw)
    offsetY = -Oculus.eyeDx * math.sin((math.pi / 2) - yaw)
    gluLookAt(lookX+offsetX, lookY+offsetY, z, x+offsetX, y+offsetY, z, 0, 0, 1)

    drawFunc()

    glPopMatrix()

