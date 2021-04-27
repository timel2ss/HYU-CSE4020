import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

gCamAng = 0
gComposedM = np.identity(4)

def render(M, camAng):
    # enable depth test
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glLoadIdentity()

    # use orthogonal projection
    glOrtho(-1,1, -1,1, -1,1)

    # rotate "camera" position to see this 3D space better
    gluLookAt(.1*np.sin(camAng),.1, .1*np.cos(camAng), 0,0,0, 0,1,0)

    # draw coordinate: x in red, y in green, z in blue
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd()

    # draw triangle
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex3fv((M @ np.array([.0,.5,0.,1.]))[:-1])
    glVertex3fv((M @ np.array([.0,.0,0.,1.]))[:-1])
    glVertex3fv((M @ np.array([.5,.0,0.,1.]))[:-1])
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global gCamAng, gComposedM
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key==glfw.KEY_Q:
            newM = np.identity(4)
            newM[:3, 3] = np.array([-.1, 0., 0.])
            gComposedM = newM @ gComposedM
        elif key==glfw.KEY_E:
            newM = np.identity(4)
            newM[:3, 3] = np.array([.1, 0., 0.])
            gComposedM = newM @ gComposedM
        elif key==glfw.KEY_A:
            t = np.radians(-10)
            newM = np.identity(4)
            newM[:3, :3] = np.array([[np.cos(t), 0., np.sin(t)],
                                     [0., 1., 0.],
                                     [-np.sin(t), 0., np.cos(t)]])
            gComposedM = gComposedM @ newM
        elif key==glfw.KEY_D:
            t = np.radians(10)
            newM = np.identity(4)
            newM[:3, :3] = np.array([[np.cos(t), 0., np.sin(t)],
                                     [0., 1., 0.],
                                     [-np.sin(t), 0., np.cos(t)]])
            gComposedM = gComposedM @ newM
        elif key==glfw.KEY_W:
            t = np.radians(-10)
            newM = np.identity(4)
            newM[:3, :3] = np.array([[1., 0., 0.],
                                     [0., np.cos(t), -np.sin(t)],
                                     [0., np.sin(t), np.cos(t)]])
            gComposedM = gComposedM @ newM
        elif key==glfw.KEY_S:
            t = np.radians(10)
            newM = np.identity(4)
            newM[:3, :3] = np.array([[1., 0., 0.],
                                     [0., np.cos(t), -np.sin(t)],
                                     [0., np.sin(t), np.cos(t)]])
            gComposedM = gComposedM @ newM


def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(480,480,"2019054957", None,None)
    if not window:
        glfw.terminate()
        return
    
    # Make the window's context current
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll events
        glfw.poll_events()
                      
        # Render here, e.g. using pyOpenGL
        render(gComposedM, gCamAng)

        # Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
