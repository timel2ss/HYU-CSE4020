import glfw
import numpy as np
from OpenGL.GL import *

angles = np.linspace(0, 2 * np.pi, 13)
positions = [(np.cos(angles[i]), np.sin(angles[i])) for i in range(len(angles))]

# 12 o'clock
hourHand = 3

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(GL_LINE_LOOP)
    for i in range(len(angles)):
        glVertex2f(positions[i][0], positions[i][1])
    glEnd()
    
    glBegin(GL_LINES)
    glVertex2f(0, 0)
    glVertex2f(positions[hourHand][0], positions[hourHand][1])
    glEnd()


def key_callback(window, key, scancode, action, mods):
    global hourHand
    if key==glfw.KEY_1:
        if action==glfw.PRESS:
            # 1 o'clock
            hourHand = 2
    if key==glfw.KEY_2:
        if action==glfw.PRESS:
            # 2 o'clock
            hourHand = 1
    if key==glfw.KEY_3:
        if action==glfw.PRESS:
            # 3 o'clock
            hourHand = 0
    if key==glfw.KEY_4:
        if action==glfw.PRESS:
            # 4 o'clock
            hourHand = 11
    if key==glfw.KEY_5:
        if action==glfw.PRESS:
            # 5 o'clock
            hourHand = 10
    if key==glfw.KEY_6:
        if action==glfw.PRESS:
            # 6 o'clock
            hourHand = 9
    if key==glfw.KEY_7:
        if action==glfw.PRESS:
            # 7 o'clock
            hourHand = 8
    if key==glfw.KEY_8:
        if action==glfw.PRESS:
            # 8 o'clock
            hourHand = 7
    if key==glfw.KEY_9:
        if action==glfw.PRESS:
            # 9 o'clock
            hourHand = 6
    if key==glfw.KEY_0:
        if action==glfw.PRESS:
            # 10 o'clock
            hourHand = 5
    if key==glfw.KEY_Q:
        if action==glfw.PRESS:
            # 11 o'clock
            hourHand = 4
    if key==glfw.KEY_W:
        if action==glfw.PRESS:
            # 12 o'clock
            hourHand = 3
    
        
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
