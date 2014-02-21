from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import pyrift
import time, math

class Oculus(object):
  eyeDx = 0.25

  def __init__(self, width, height):
    pyrift.initialize()
    self.width = width
    self.height = height
    self.calibPoint = (0, 0, 0)

  def calibrate(self):
    self.calibPoint = pyrift.get_orientation()

  def draw(self, drawFunc, pos):
    rpy = map(lambda (x, y):y-x, zip(self.calibPoint, pyrift.get_orientation()))
    print rpy

    self.leftEye(pos, rpy, drawFunc)
    self.rightEye(pos, rpy, drawFunc)

  def leftEye(self, pos, rpy, drawFunc):
    (x, y, z) = pos
    (roll, pitch, yaw) = rpy

    glPushMatrix()
    glEnable(GL_SCISSOR_TEST)
    glScissor(0, 0, self.width/2, self.height)

    glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT)
     
    # Do translations for correct Oculus Viewing
    glRotatef((pitch * 360) / (2 * math.pi), 1, 0, 0)
    glRotatef((roll * 360) / (2 * math.pi), 0, 1, 0)
    lookX = math.cos(yaw) + x
    lookY = math.sin(yaw) + y
    offsetX = Oculus.eyeDx * math.cos((math.pi / 2) - yaw)
    offsetY = Oculus.eyeDx * math.sin((math.pi / 2) - yaw)
    gluLookAt(lookX+offsetX, lookY+offsetY, z, x+offsetX, y+offsetY, z, 0, 0, 1)

    glColor3f(0, 1, 0)
    drawFunc()

    glDisable(GL_SCISSOR_TEST)
    glPopMatrix()

  def rightEye(self, pos, rpy, drawFunc):
    (x, y, z) = pos
    (roll, pitch, yaw) = rpy

    glPushMatrix()
    glEnable(GL_SCISSOR_TEST)
    glScissor(self.width/2, 0, self.width/2, self.height)

    glClearColor(1, 1, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT)

    # Do translations for correct Oculus Viewing
    glRotatef((pitch * 360) / (2 * math.pi), 1, 0, 0)
    glRotatef((roll * 360) / (2 * math.pi), 0, 1, 0)
    lookX = math.cos(yaw) + x
    lookY = math.sin(yaw) + y
    offsetX = -Oculus.eyeDx * math.cos((math.pi / 2) - yaw)
    offsetY = -Oculus.eyeDx * math.sin((math.pi / 2) - yaw)
    gluLookAt(lookX+offsetX, lookY+offsetY, z, x+offsetX, y+offsetY, z, 0, 0, 1)

    glColor3f(0, 0, 1)
    drawFunc()

    glDisable(GL_SCISSOR_TEST)
    glPopMatrix()

