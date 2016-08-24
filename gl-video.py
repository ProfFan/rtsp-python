from OpenGL.GL import *
from OpenGL.GLUT import *

import sys
sys.path.append(os.getcwd())
import TextureGL
from gi.repository import Gst
tex = 0
mipmap = 0

def display_func():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)

    # Enable texture map
    glEnable(GL_TEXTURE_2D)
    
    #glBindTexture(GL_TEXTURE_2D, tex)
    receiver.updateTexture()

    
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(8.0, -4.5, -0.0)

    glTexCoord2f(0.0, 1.0)
    glVertex3f(-8.0, -4.5, 0.0)

    glTexCoord2f(0.0, 0.0)
    glVertex3f(-8.0, 4.5, 0.0)

    glTexCoord2f(1.0, 0.0)
    glVertex3f(8.0, 4.50, -0.0)
    glEnd()

    glFlush()
    glutPostRedisplay()
def reshape_func(width, height):
    
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity();
    glOrtho(-8.0, 8.0, -4.50, 4.50, -1.0, 1.0);
    glMatrixMode(GL_MODELVIEW)

def main():
    Gst.init([])
    global tex
    global mipmap
    global receiver
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(600, 600)
    glutCreateWindow(u"Sample 9")
    glutDisplayFunc(display_func)
    glutReshapeFunc(reshape_func)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    tex = glGenTextures(1)
    receiver = TextureGL.Receiver(tex, "rtspsrc location=rtsp://"+"10.1.201.223"+
        "/profile?token=media_profile1&SessionTimeout=600000 latency=0 droponlatency=1 ! rtph264depay ! decodebin ! videoconvert ! video/x-raw,format=RGB,framerate=0/1 ! fakesink")

    glutMainLoop()

if __name__ == '__main__':
    main()
