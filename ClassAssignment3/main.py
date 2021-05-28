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

drawFlag = False

# constant of channel
XPOSITION = 0
YPOSITION = 1
ZPOSITION = 2
XROTATION = 3
YROTATION = 4
ZROTATION = 5

offsets = []
channels = []
frames = []
joint_stack = []
frame_cnt = 0
curr_frame = 1

animationObject = []

# True: perspective projection, False: orthogonal projection
projection = True
# True: solid mode, False: wireframe
filled = True
# True: animation on, False: animation off
animate = False
# True: smooth shading, False: using vn in obj file
shading = False

def render():
    global u, v, w
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    if filled:
        glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )
    else:
        glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
        
    glLoadIdentity()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # toggle perspective/orthogonal projection by pressing 'v' key
    if projection == True:
        # Zooming on Perspective projection
        gluPerspective(zoom, 1, 5, 1000)
    else:
        # Zooming on Orthogonal projection
        glOrtho(-.14 * zoom, .14 * zoom, -.14 * zoom, .14 * zoom, 5, 1000)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

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

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_NORMALIZE)

    lightPos0 = (5., 5., 5., 1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos0)

    lightColor0 = (1., 1., 0., 1.)
    ambientLightColor0 = (.1, .1, 0., 1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor0)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor0)

    lightPos1 = (-5., 5., -5., 1.)
    glLightfv(GL_LIGHT1, GL_POSITION, lightPos1)

    lightColor1 = (0., 1., 1., 1.)
    ambientLightColor1 = (0., .1, .1, 1.)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lightColor1)
    glLightfv(GL_LIGHT1, GL_SPECULAR, lightColor1)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor1)

    objectColor = (1., 1., 1., 1.)
    specularObjectColor = (1., 1., 1., 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    
    drawObject()
    
    glDisable(GL_LIGHTING)

def drawObject():
    global curr_frame
    offset_index = 0
    channel_index = 0
    for i in range(len(joint_stack)):
        if joint_stack[i] == '{':
            glPushMatrix()

            offset = np.array(offsets[offset_index])
            offset_index += 1

            if i != 0:
                # glBegin(GL_LINES)
                glColor3ub(0, 255, 255)
                # glVertex3fv(np.array([0, 0, 0]))
                # glVertex3fv(offset)
                # glEnd()
                drawCube(offset)
            
            glTranslatef(offset[0], offset[1], offset[2])

            if joint_stack[i + 1] == '}':
                continue
            
            xpos = 0; ypos = 0; zpos = 0
            for j in range(len(channels[channel_index])):
                if channels[channel_index][j][0] == XPOSITION:
                    xpos = channels[channel_index][j][curr_frame]
                elif channels[channel_index][j][0] == YPOSITION:
                    ypos = channels[channel_index][j][curr_frame]
                elif channels[channel_index][j][0] == ZPOSITION:
                    zpos = channels[channel_index][j][curr_frame]

            if xpos != 0 and ypos != 0 and zpos != 0:
                glTranslatef(xpos, ypos, zpos)

            for j in range(len(channels[channel_index])):
                if channels[channel_index][j][0] == XROTATION:
                    glRotatef(channels[channel_index][j][curr_frame], 1, 0, 0)
                elif channels[channel_index][j][0] == YROTATION:
                    glRotatef(channels[channel_index][j][curr_frame], 0, 1, 0)
                elif channels[channel_index][j][0] == ZROTATION:
                    glRotatef(channels[channel_index][j][curr_frame], 0, 0, 1)

            channel_index += 1

        elif joint_stack[i] == '}':
            glPopMatrix()

    if animate == True:
        curr_frame = (curr_frame + 1) % (frame_cnt + 1)
        if curr_frame == 0:
            curr_frame += 2

def drawCube(offset):
    origin = np.array([0., 0., 0.])

    v1 = origin - offset
    v1 = v1 / (np.sqrt(np.dot(v1, v1)))

    v2 = np.cross(v1, np.array([0., 1., 0.]))
    if v2[0] == 0 and  v2[1] == 0 and v2[2] == 0:
        v2 = np.cross(v1, np.array([0., 0., 1.]))
    v2 = v2 / (np.sqrt(np.dot(v2, v2)))
    v2 *= .05

    v3 = np.cross(v1, v2)
    v3 = v3 / (np.sqrt(np.dot(v3, v3)))
    v3 *= .05

    up = v3
    height = v2

    glBegin(GL_QUADS)
    n1 = offset - origin
    n2 = up
    n = np.cross(n1, n2)
    n = n / np.sqrt(np.dot(n, n))
    glNormal3fv(n)
    glVertex3fv(origin + up - height)
    glVertex3fv(origin - up - height)
    glVertex3fv(offset - up - height)
    glVertex3fv(offset + up - height)

    n1 = offset - origin
    n2 = origin - up
    n = np.cross(n1, n2)
    n = n / np.sqrt(np.dot(n, n))
    glNormal3fv(n)
    glVertex3fv(origin - up + height)
    glVertex3fv(origin + up + height)
    glVertex3fv(offset + up + height)
    glVertex3fv(offset - up + height)

    n1 = height
    n2 = origin - up
    n = np.cross(n1, n2)
    n = n / np.sqrt(np.dot(n, n))
    glNormal3fv(n)
    glVertex3fv(origin - up + height)
    glVertex3fv(origin - up - height)
    glVertex3fv(origin + up - height)
    glVertex3fv(origin + up + height)

    n1 = up
    n2 = origin - height
    n = np.cross(n1, n2)
    n = n / np.sqrt(np.dot(n, n))
    glNormal3fv(n)
    glVertex3fv(offset - up - height)
    glVertex3fv(offset - up + height)
    glVertex3fv(offset + up + height)
    glVertex3fv(offset + up - height)

    n1 = origin - height
    n2 = offset - origin
    n = np.cross(n1, n2)
    n = n / np.sqrt(np.dot(n, n))
    glNormal3fv(n)
    glVertex3fv(origin + up + height)
    glVertex3fv(origin + up - height)
    glVertex3fv(offset + up - height)
    glVertex3fv(offset + up + height)

    n1 = origin - height
    n2 = origin - offset
    n = np.cross(n1, n2)
    n = n / np.sqrt(np.dot(n, n))
    glNormal3fv(n)
    glVertex3fv(origin - up - height)
    glVertex3fv(origin - up + height)
    glVertex3fv(offset - up + height)
    glVertex3fv(offset - up - height)
    glEnd()

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
    glVertex3fv(np.array([0.,0.,0.]))
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
    global projection, animate, curr_frame
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key == glfw.KEY_V:
            if projection == True:
                projection = False
            else:
                projection = True
        if key == glfw.KEY_SPACE:
            if animate == True:
                animate = False
                curr_frame = 1
            else:
                animate = True

def drop_callback(window, paths):
    global offsets, channels, frames, joint_stack, frame_cnt
    (offsets, channels, frames, joint_stack, frame_cnt) = bvh_parse(paths[0])

def bvh_parse(path):
    offsets = []
    channels = []
    frames = []
    joint_stack = []
    frame_cnt = 0

    joint_names = []
    channel_cnt = 0
    FPS = 0

    with open(path, "r") as f:
        fileName = path.split("\\")[-1]

        while True:
            line = f.readline()
            if not line:
                break

            partition = line.split()
            if not partition:
                continue
            
            if partition[0] == "HIERARCHY" or partition[0] == "MOTION":
                continue

            # HIERARCHY
            elif partition[0] == "ROOT" or partition[0] == "JOINT":
                joint_names.append(partition[1])
            elif partition[0] == "End":
                continue
            elif partition[0] == '{' or partition[0] == '}':
                joint_stack.append(partition[0])

            elif partition[0] == "OFFSET":
                offsets.append(tuple(map(float, (partition[1], partition[2], partition[3]))))
            
            elif partition[0] == "CHANNELS":
                channel = []
                channel_cnt += int(partition[1])

                for i in range(2, len(partition)):
                    if partition[i] == "XPOSITION":
                        channel.append([XPOSITION, 0.0])
                    elif partition[i] == "YPOSITION":
                        channel.append([YPOSITION, 0.0])
                    elif partition[i] == "ZPOSITION":
                        channel.append([ZPOSITION, 0.0])
                    elif partition[i] == "XROTATION":
                        channel.append([XROTATION, 0.0])
                    elif partition[i] == "YROTATION":
                        channel.append([YROTATION, 0.0])
                    elif partition[i] == "ZROTATION":
                        channel.append([ZROTATION, 0.0])
                channels.append(channel)

            # MOTION
            elif partition[0] == "Frames:":
                frame_cnt = int(partition[1])

            elif partition[0] == "Frame":
                FPS = 1 / float(partition[2])
            
            else:
                t = 0
                for i in range(len(channels)):
                    for j in range(len(channels[i])):
                        channels[i][j].append(float(partition[t]))
                        t += 1
    
    print("File name: ", fileName)
    print("Number of frames: ", frame_cnt)
    print("FPS: ", FPS)
    print("Number of joins: ", len(joint_names))
    print("List of all joint names: ", ' '.join(joint_names), end="\n\n")

    return (offsets, channels, frames, joint_stack, frame_cnt)

def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(640,640,"Bvh viewer", None,None)
    if not window:
        glfw.terminate()
        return
    
    # Make the window's context current
    glfw.make_context_current(window)
    glfw.set_cursor_pos_callback(window, cursor_position_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_key_callback(window, key_callback)
    glfw.set_drop_callback(window, drop_callback)
    glfw.swap_interval(1)

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