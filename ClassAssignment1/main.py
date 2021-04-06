import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

gCamAng = 0
gCamHeight = 1.

azimuth = 0
elevation = 0
distance = 0
zoom = 50

width = 600
height = 600
near = 5
far = 1000

# True: perspective projection, False: orthogonal projection
toggle = True

def render():
    global gCamAng, gCamHeight, toggle
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )

    glLoadIdentity()

    if toggle == True:
        gluPerspective(zoom, width / height, near, far)
    else:
        tmp = .05 * zoom
        glOrtho(-tmp, tmp, -tmp, tmp, near, far)

    gluLookAt(5*np.sin(gCamAng),gCamHeight,5*np.cos(gCamAng), 0,0,0, 0,1,0)

    drawFrame()
    drawGridOnXZplane()

def drawGridOnXZplane():
    glBegin(GL_LINES)
    glColor3ub(255, 255, 255)
    for i in range(-10, 11):
        glVertex3fv(np.array([i, 0, 10]))
        glVertex3fv(np.array([i, 0, -10]))
        glVertex3fv(np.array([10, 0, i]))
        glVertex3fv(np.array([-10, 0, i]))
    glEnd()

def drawFrame():
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

def scroll_callback(window, xoffset, yoffset):
    global zoom
    zoom -= yoffset
    if zoom < 5:
        zoom = 5
    

def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight, toggle
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key==glfw.KEY_2:
            gCamHeight += .1
        elif key==glfw.KEY_W:
            gCamHeight += -.1
        elif key == glfw.KEY_V:
            if toggle == True:
                toggle = False
            else:
                toggle = True



def main():
    
    
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(480,480,"OpenGL viewer", None,None)
    if not window:
        glfw.terminate()
        return
    
    # Make the window's context current
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_scroll_callback(window, scroll_callback)

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
