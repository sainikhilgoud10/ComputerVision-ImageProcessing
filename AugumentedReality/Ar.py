from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import cv2
from PIL import Image
from webcam import Webcam
from detection import Detection
from threading import Thread
class HandTracker:
    def __init__(self):
        self.webcam = Webcam()
        self.webcam.start()
        if self.webcam != None:
            self.detection = Detection(self.webcam)
        self.x_axis = 0.0
        self.z_axis = 0.0
        self.show_cube = False
        self.texture_background = None
        self.texture_cube = None
        self.tx, self.ty = (0,0)
    def _init_gl(self,width,Height):
        self.Width = width
        self.Height = Height
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(self.Width)/float(self.Height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

          # enable texture
        glEnable(GL_TEXTURE_2D)
        self.texture_background = glGenTextures(1)
        self.texture_cube = glGenTextures(1)
        image = Image.open("file.jpg")
        ix = image.size[0]
        iy = image.size[1]
        image = image.tobytes("raw", "RGBX", 0, -1)
 
        glBindTexture(GL_TEXTURE_2D, self.texture_cube)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)            
    def _draw_scene(self):
        self._handle_gesture()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()        

         # draw background
        glBindTexture(GL_TEXTURE_2D, self.texture_background)
        glPushMatrix()
        glTranslatef(0.0,0.0,-11.2)
        self._draw_background()
        glPopMatrix()
        if self.show_cube:
            glColor4f(1.0,1.0,1.0,1.0)
            glBlendFunc(GL_SRC_ALPHA,GL_ONE)
            glEnable(GL_BLEND)
            glDisable(GL_DEPTH_TEST)
            glBindTexture(GL_TEXTURE_2D, self.texture_cube)
            glPushMatrix()
            glTranslatef(self.tx/20,self.ty,-7.0)
            glRotatef(self.x_axis,1.0,0.0,0.0)
            glRotatef(0.0,0.0,1.0,0.0)
            glRotatef(self.z_axis,0.0,0.0,1.0)
            self._draw_cube()
            glPopMatrix()
            glDisable(GL_BLEND)
            glEnable(GL_DEPTH_TEST)
            self.x_axis = self.x_axis - 1
            self.z_axis = self.z_axis - 1
        glutSwapBuffers()
    def _handle_gesture(self):
         # get image from webcam 
        image = self.webcam.get_current_frame()
        face = self.detection.is_face("haarcascade_frontalface_alt.xml")
        if face:
            self.show_cube = True
        else:
            self.show_cube = False
        # convert image to OpenGL texture format
        image = cv2.flip(image, 0)
        gl_image = Image.fromarray(image)     
        ix = gl_image.size[0]
        iy = gl_image.size[1]
        gl_image = gl_image.tobytes("raw", "BGRX", 0, -1)
  
        #create background texture
        glBindTexture(GL_TEXTURE_2D, self.texture_background)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, gl_image)
        
        
        
    def _draw_background(self):
        # draw background
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0); glVertex3f(-4.0, -3.0, 4.0)
        glTexCoord2f(1.0, 1.0); glVertex3f( 4.0, -3.0, 4.0)
        glTexCoord2f(1.0, 0.0); glVertex3f( 4.0,  3.0, 4.0)
        glTexCoord2f(0.0, 0.0); glVertex3f(-4.0,  3.0, 4.0)
        glEnd( )
    def _draw_cube(self):
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)
        glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0,  1.0)
        glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0,  1.0)
        glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0,  1.0)
        glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0, -1.0)
        glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0, -1.0)
        glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0, -1.0)
        glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0, -1.0)
        glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0)
        glTexCoord2f(0.0, 0.0); glVertex3f(-1.0,  1.0,  1.0)
        glTexCoord2f(1.0, 0.0); glVertex3f( 1.0,  1.0,  1.0)
        glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0)
        glTexCoord2f(1.0, 1.0); glVertex3f(-1.0, -1.0, -1.0)
        glTexCoord2f(0.0, 1.0); glVertex3f( 1.0, -1.0, -1.0)
        glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0)
        glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)
        glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0, -1.0)
        glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0)
        glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0,  1.0)
        glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0)
        glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0, -1.0)
        glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)
        glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0,  1.0)
        glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0)
        glEnd()
    def KeyPressed(self,*args):
        if args[0] == '\x08':
            #self.keyCache = self.keyCache[:-1]
            pass
        elif args[0] == '\x1b':
            sys.exit()
        elif args[0] == 'm':
            print "Now meteoring otherwise peaceful teapot"
            self.tx += 2
    def MouseClicked(self,button, buttonState, x, y):
        if buttonState == GLUT_DOWN:
            print "clicked"

        #else:
            #self.keyCache += args[0]
        #sys.stdout.write(self.keyCache +"                                                  \r")#print "keypress: <",self.keyCache,">"
        #sys.stdout.flush()
    def main(self):
        enable = bool(glutInit())
        if enable:
            glutInit()
            glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
            glutInitWindowSize(640, 480)
            glutInitWindowPosition(0, 0)
            self.window = glutCreateWindow("OpenGL Hand Tracker")
            glutDisplayFunc(self._draw_scene)
            glutIdleFunc(self._draw_scene)
            glutKeyboardFunc (self.KeyPressed)
            glutMouseFunc(self.MouseClicked)
            self._init_gl(640, 480)
            glutMainLoop()

handtracker = HandTracker()
handtracker.main()
        











        
