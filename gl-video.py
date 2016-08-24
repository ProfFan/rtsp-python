from OpenGL.GL import *
from OpenGL.GLU import *

import sys,os
sys.path.append(os.getcwd())
import TextureGL
from gi.repository import Gst
import pygame

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

def reshape_func(width, height):
    screen=pygame.display.set_mode((width,height),pygame.OPENGL|pygame.DOUBLEBUF|pygame.RESIZABLE)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity();
    glOrtho(-8.0, 8.0, -4.50, 4.50, -1.0, 1.0);
    glMatrixMode(GL_MODELVIEW)

def main():
    Gst.init([])
    # Get Pygame ready
    pygame.init()

    global screen
    # Set the width and height of the screen [width,height]
    size = (1024,576)
    video_flags = pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE
    screen = pygame.display.set_mode(size, video_flags)

    # Create an OpenGL viewport
    reshape_func(size[0],size[1])

    global tex
    global mipmap
    global receiver
#    glutInit(sys.argv)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    tex = glGenTextures(1)
    receiver = TextureGL.Receiver(tex, "rtspsrc location=rtsp://"+"10.1.201.205"+
        "/profile?token=media_profile1&SessionTimeout=600000 latency=0 droponlatency=1 ! rtph264depay ! decodebin ! videoconvert ! video/x-raw,format=RGB,framerate=0/1 ! fakesink")

    done = False

    while not done:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.VIDEORESIZE:
            reshape_func(event.w, event.h)
        display_func()
        pygame.display.flip()

if __name__ == '__main__':
    main()
