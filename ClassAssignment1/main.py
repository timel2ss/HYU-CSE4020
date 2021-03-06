import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

x_pos = 0
y_pos = 0

azimuth = 45
elevation = 45
distance = 15
zoom = 30

up = np.array([0., 1., 0.])
u = np.array([1., 0., 0.])
v = np.array([0., 1., 0.])
w = np.array([0., 0., 1.])
origin = np.array([0., 0., 0.])

leftMouse = False
rightMouse = False

# True: perspective projection, False: orthogonal projection
toggle = True

def render():
    global u, v, w
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )

    glLoadIdentity()

    # toggle perspective/orthogonal projection by pressing 'v' key
    if toggle == True:
        # Zooming on Perspective projection
        gluPerspective(zoom, 1, 5, 1000)
    else:
        # Zooming on Orthogonal projection
        glOrtho(-.14 * zoom, .14 * zoom, -.14 * zoom, .14 * zoom, 5, 1000)

    # Panning and Orbit
    x_angle = np.radians(azimuth)
    y_angle = np.radians(elevation)

    w = np.array([np.cos(x_angle) * np.cos(y_angle), np.sin(y_angle), np.sin(x_angle) * np.cos(y_angle)])
    u = np.cross(up, w) / np.sqrt(np.dot(np.cross(up, w), np.cross(up, w)))
    v = np.cross(u, w) / np.sqrt(np.dot(np.cross(u, w), np.cross(u, w)))

    pos = [distance * w[0] + origin[0], distance * w[1] + origin[1], distance * w[2] + origin[2]]
    gluLookAt(pos[0], pos[1], pos[2], origin[0], origin[1], origin[2], up[0], up[1], up[2])

    drawFrame()
    drawGridOnXZplane()

def drawGridOnXZplane():
    glBegin(GL_LINES)
    glColor3ub(255, 255, 255)
    for i in range(-30, 31):
        glVertex3fv(np.array([i, 0, 30]))
        glVertex3fv(np.array([i, 0, -30]))
        glVertex3fv(np.array([30, 0, i]))
        glVertex3fv(np.array([-30, 0, i]))
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
    global origin, up, azimuth, elevation, x_pos, y_pos
    if leftMouse == True:
        # Orbit
        azimuth += .4 * (xpos - x_pos)
        elevation += .4 * (ypos - y_pos)

        if np.cos(np.radians(elevation)) < 0:
            up = np.array([0., -1., 0.])
        else:
            up = np.array([0., 1., 0.])

    elif rightMouse == True:
        # Panning
        x_translate = .02 * (xpos - x_pos)
        y_translate = .02 * (ypos - y_pos)
        origin -= x_translate * u + y_translate * v

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