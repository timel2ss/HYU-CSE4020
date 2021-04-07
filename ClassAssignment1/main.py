import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

x_rotate = 0
y_rotate = 0
x_pos = 0
y_pos = 0
x_translate = 0
y_translate = 0
azimuth = 0
elevation = 0
distance = 0
zoom = 50

width = 600
height = 600
near = 5
far = 1000

leftMouse = False
rightMouse = False

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

    glRotatef(y_rotate, 1., 0., 0.)
    glRotatef(x_rotate, 0., 1., 0.)
    glTranslatef(x_translate, 0, 0)
    glTranslatef(0, y_translate, 0)

    gluLookAt(5, 10, 5, 0,0,0, 0,1,0)

    drawFrame()
    drawGridOnXZplane()

def drawGridOnXZplane():
    glBegin(GL_LINES)
    glColor3ub(255, 255, 255)
    for i in range(-5, 6):
        glVertex3fv(np.array([i, 0, 5]))
        glVertex3fv(np.array([i, 0, -5]))
        glVertex3fv(np.array([5, 0, i]))
        glVertex3fv(np.array([-5, 0, i]))
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

def cursor_position_callback(window, xpos, ypos):
    global leftMouse, rightMouse, azimuth, elevation
    global x_pos, y_pos, x_rotate, y_rotate, x_translate, y_translate
    if leftMouse == True:
        # TODO: fix orbit (arcball?)
        x_rotate -= xpos - x_pos
        y_rotate -= ypos - y_pos
    elif rightMouse == True:
        x_translate += .02 * (xpos - x_pos)
        y_translate -= .02 * (ypos - y_pos)
    x_pos = xpos
    y_pos = ypos

def mouse_button_callback(window, button, action, mods):
    global leftMouse, rightMouse
    if button == glfw.MOUSE_BUTTON_LEFT:
        if action == glfw.PRESS or action == glfw.REPEAT:
            leftMouse = True
        elif action == glfw.RELEASE:
            leftMouse = False
    elif button == glfw.MOUSE_BUTTON_RIGHT:
        if action == glfw.PRESS or action == glfw.REPEAT:
            rightMouse = True
        elif action == glfw.RELEASE:
            rightMouse = False


def scroll_callback(window, xoffset, yoffset):
    global zoom
    zoom -= yoffset
    if zoom < 5:
        zoom = 5
    

def key_callback(window, key, scancode, action, mods):
    global toggle
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key == glfw.KEY_V:
            if toggle == True:
                toggle = False
            else:
                toggle = True


def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(640,640,"OpenGL viewer", None,None)
    if not window:
        glfw.terminate()
        return
    
    # Make the window's context current
    glfw.make_context_current(window)
    glfw.set_cursor_pos_callback(window, cursor_position_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_key_callback(window, key_callback)

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
