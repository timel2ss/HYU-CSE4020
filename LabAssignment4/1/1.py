import glfw
import numpy as np
from OpenGL.GL import *

gComposedM = np.identity(4)

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    # draw cooridnates
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()

    glColor3ub(255, 255, 255)
    
    glMultMatrixf(gComposedM.T)

    drawTriangle()

def drawTriangle(): 
    glBegin(GL_TRIANGLES)
    glVertex2fv(np.array([0.,.5]))
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([.5,0.]))
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global gComposedM
    if key==glfw.KEY_Q:
        if action==glfw.PRESS or action==glfw.REPEAT:
            newM = np.identity(4)
            newM[:3, 3] = np.array([-.1, 0., 0.])
            gComposedM = newM @ gComposedM
    if key==glfw.KEY_E:
        if action==glfw.PRESS or action==glfw.REPEAT:
            newM = np.identity(4)
            newM[:3, 3] = np.array([.1, 0., 0.])
            gComposedM = newM @ gComposedM
    if key==glfw.KEY_A:
        if action==glfw.PRESS or action==glfw.REPEAT:
            t = np.radians(10)
            newM = np.identity(4)
            newM[:3, :3] = np.array([[np.cos(t), -np.sin(t), 0.],
                                     [np.sin(t), np.cos(t), 0.],
                                     [0., 0., 1.]])
            gComposedM = newM @ gComposedM
    if key==glfw.KEY_D:
        if action==glfw.PRESS or action==glfw.REPEAT:
            t = np.radians(10)
            newM = np.identity(4)
            newM[:3, :3] = np.array([[np.cos(t), np.sin(t), 0.],
                                     [-np.sin(t), np.cos(t), 0.],
                                     [0., 0., 1.]])
            gComposedM = newM @ gComposedM
    if key==glfw.KEY_1:
        if action==glfw.PRESS or action==glfw.REPEAT:
            gComposedM = np.identity(4)


def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(480,480,"2019054957", None,None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)
    
    # Make the window's context current
    glfw.make_context_current(window)


    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll events
        glfw.poll_events()
                      
        # Render here, e.g. using pyOpenGL
        render()

        # Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
