import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

gCamAng = 0
gCamHeight = 1.

def createVertexAndIndexArrayIndexed():
    varr = np.array([
            (0, 0, 0),      # v0
            (1.5, 0, 0),    # v1
            (1.5, 1.5, 0),  # v2
            (0, 1.5, 0),    # v3
            (0, 0, 1.5),    # v4
            (1.5, 0, 1.5),  # v5
            (1.5, 1.5, 1.5),    # v6
            (0, 1.5, 1.5)   # v7
            # ( -1.5 ,  1.5 ,  1.5 ), # v0
            # (  1.5 ,  1.5 ,  1.5 ), # v1
            # (  1.5 , -1.5 ,  1.5 ), # v2
            # ( -1.5 , -1.5 ,  1.5 ), # v3
            # ( -1.5 ,  1.5 , -1.5 ), # v4
            # (  1.5 ,  1.5 , -1.5 ), # v5
            # (  1.5 , -1.5 , -1.5 ), # v6
            # ( -1.5 , -1.5 , -1.5 ), # v7
            ], 'float32')
    iarr = np.array([
            (0, 3, 2, 1),
            (0, 1, 5, 4),
            (1, 2, 6, 5),
            (2, 3, 7, 6),
            (0, 4, 7, 3),
            (4, 5, 6, 7)

            # (0,2,1),
            # (0,3,2),
            # (4,5,6),
            # (4,6,7),
            # (0,1,5),
            # (0,5,4),
            # (3,6,2),
            # (3,7,6),
            # (1,2,6),
            # (1,6,5),
            # (0,7,3),
            # (0,4,7),
            ])
    return varr, iarr

def render():
    global gCamAng, gCamHeight
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )

    glLoadIdentity()
    gluPerspective(45, 1, 1,10)
    gluLookAt(5*np.sin(gCamAng),gCamHeight,5*np.cos(gCamAng), 0,0,0, 0,1,0)

    drawFrame()
    glColor3ub(255, 255, 255)
    
    drawCube_glDrawElements()

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

def drawCube_glDrawElements():
    global gVertexArrayIndexed, gIndexArray
    varr = gVertexArrayIndexed
    iarr = gIndexArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(3, GL_FLOAT, 3*varr.itemsize, varr)
    glDrawElements(GL_QUADS, iarr.size, GL_UNSIGNED_INT, iarr)

def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key==glfw.KEY_2:
            gCamHeight += .1
        elif key==glfw.KEY_W:
            gCamHeight += -.1

gVertexArrayIndexed = None
gIndexArray = None

def main():
    global gVertexArrayIndexed, gIndexArray
    
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

    gVertexArrayIndexed, gIndexArray = createVertexAndIndexArrayIndexed()

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
