from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
window = 0
counter = 0
posX = 10
posY = 10
flag =0
width, height = 500, 400
def draw_rect(x,y,width,height):
    time.sleep(0.01)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x+width, y)
    glVertex2f(x+width, y+height)
    glVertex2f(x, y+height)
    glEnd()
def refresh2d(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
def draw():
    global counter
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    refresh2d(width, height)
    if counter < 500:
        counter += 1
    glColor3f(0.0, 0.0, 1.0)
    draw_rect(posX, posY, counter, 10)
    #draw rectangle
    glutSwapBuffers()
glutInit()
glutInitDisplayMode(GLUT_RGBA|GLUT_DOUBLE|GLUT_ALPHA|GLUT_DEPTH)
glutInitWindowSize(width,height)
glutInitWindowPosition(0,0)
window = glutCreateWindow("this is a test")
glutDisplayFunc(draw)
glutIdleFunc(draw)
glutMainLoop()
