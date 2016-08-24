from OpenGL.GL import *
from OpenGL.GLU import *

import sys, os
sys.path.append(os.getcwd())
import TextureGL
from gi.repository import Gst
import pygame

urls = []
tex = []
players = []


def draw_rect(x, y, w, h, tex_id):
    # Enable texture map
    glEnable(GL_TEXTURE_2D)

    #glBindTexture(GL_TEXTURE_2D, tex)
    players[tex_id].updateTexture()

    glBindTexture(GL_TEXTURE_2D, tex[tex_id])
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(x + w, y, -0.0)

    glTexCoord2f(0.0, 1.0)
    glVertex3f(x, y, 0.0)

    glTexCoord2f(0.0, 0.0)
    glVertex3f(x, y + h, 0.0)

    glTexCoord2f(1.0, 0.0)
    glVertex3f(x + w, y + h, -0.0)
    glEnd()


def display_func():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)
    #print(urls)
    step_x = 16 / 6
    step_y = 9 / 4
    j = -1
    for i in range(len(urls)):
        if (i) % 6 == 0:
            j += 1
        draw_rect(-8.0 + step_x *
                  (i % 6), -4.5 + step_y * j, step_x, step_y, i)

    glFlush()


def reshape_func(width, height):
    screen = pygame.display.set_mode(
        (width, height), pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-8.0, 8.0, -4.50, 4.50, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)


def main():
    Gst.init([])
    # Get Pygame ready
    pygame.init()

    global screen
    # Set the width and height of the screen [width,height]
    size = (3008, 1200)
    video_flags = pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE
    screen = pygame.display.set_mode(size, video_flags)
    pygame.display.set_caption("Realtime RTSP")
    # Create an OpenGL viewport
    reshape_func(size[0], size[1])

    global tex
    global urls
    global players
    #    glutInit(sys.argv)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)

    urls = sys.argv[1:]

    for i in range(len(urls)):
        print("Init Pipeline:" + urls[i])
        tex_name = glGenTextures(1)
        tex.append(tex_name)
        player = TextureGL.Receiver(
            tex_name, "rtspsrc location=rtsp://" + urls[i] +
            "/profile?token=media_profile1&SessionTimeout=600000 latency=0 droponlatency=1 ! rtph264depay ! queue max-size-buffers=0 max-size-bytes=0 max-size-time=0 ! h264parse ! avdec_h264 ! videoconvert ! video/x-raw,format=RGB,framerate=0/1 ! fakesink sync=1 name=display%s"
            % tex_name)
        players.append(player)
        print("INIT_SUCCESS")

    for i in range(len(urls)):
        players[i].start_pipeline()
    done = False

    while not done:
        event = pygame.event.poll()

        display_func()
        pygame.display.flip()
        if event.type == pygame.QUIT:
            done = True
            for i in range(len(urls)):
                players[i].stop_pipeline()
        if event.type == pygame.VIDEORESIZE:
            reshape_func(event.w, event.h)
    pygame.quit()


if __name__ == '__main__':
    main()
