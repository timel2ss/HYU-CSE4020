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
gIndexArray3v = None
gIndexArray3vn = None
gIndexArray3v = None
gIndexArray4vn = None
gIndexArrayPolygon = None
gIndexArrayPolygonn = None

# True: perspective projection, False: orthogonal projection
projection = True
# True: solid mode, False: wireframe
filled = False

def render():
    global u, v, w
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    if filled:
        glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )
    else:
        glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )

    glLoadIdentity()

    # toggle perspective/orthogonal projection by pressing 'v' key
    if projection == True:
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

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_NORMALIZE)

    lightPos0 = (5., 5., 5., 1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos0)

    lightColor0 = (1., 1., 0., 1.)
    ambientLightColor0 = (.1, .1, .1, 1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor0)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor0)

    lightPos1 = (-5., 10., -5., 1.)
    glLightfv(GL_LIGHT1, GL_POSITION, lightPos1)

    lightColor1 = (0., 1., 1., 1.)
    ambientLightColor1 = (.1, .1, .1, 1.)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lightColor1)
    glLightfv(GL_LIGHT1, GL_SPECULAR, lightColor1)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor1)

    objectColor = (1., 1., 1., 1.)
    specularObjectColor = (1., 1., 1., 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    
    if drawFlag:
        glColor3ub(0,0,255)
        drawElements()
    
    glDisable(GL_LIGHTING)

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

def drawElements():
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)

    glNormalPointer(GL_FLOAT, 3*gIndexArray3vn.itemsize, gIndexArray3vn)
    glVertexPointer(3, GL_FLOAT,3*gIndexArray3v.itemsize, gIndexArray3v)
    glDrawArrays(GL_TRIANGLES, 0, int(gIndexArray3v.size/3))

    glNormalPointer(GL_FLOAT, 3*gIndexArray4vn.itemsize, gIndexArray4vn)
    glVertexPointer(3, GL_FLOAT, 3*gIndexArray4v.itemsize, gIndexArray4v)
    glDrawArrays(GL_QUADS, 0, int(gIndexArray4v.size/3))

    for i in range(len(gIndexArrayPolygon)):
        glNormalPointer(GL_FLOAT, 3*gIndexArrayPolygonn[i].itemsize, gIndexArrayPolygonn[i])
        glVertexPointer(3, GL_FLOAT, 3*gIndexArrayPolygon[i].itemsize, gIndexArrayPolygon[i])
        glDrawArrays(GL_POLYGON, 0, int(gIndexArrayPolygon[i].size/3))

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
    global projection, filled
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key == glfw.KEY_V:
            if projection == True:
                projection = False
            else:
                projection = True
        if key == glfw.KEY_Z:
            if filled == True:
                filled = False
            else:
                filled = True

def drop_callback(window, paths):
    global gIndexArray3v, gIndexArray3vn, gIndexArray4v, gIndexArray4vn, gIndexArrayPolygon, gIndexArrayPolygonn, drawFlag

    vertex_array = []
    normal_array = []
    index_3v_array = []
    index_3vn_array = []
    index_4v_array = []
    index_4vn_array = []
    index_polygon_array = []
    index_polygonn_array = []

    total_face = 0
    face_3v = 0
    face_4v = 0
    face_over_4 = 0

    with open(paths[0], "r") as f:
        fileName = paths[0].split("\\")[-1]

        while True:
            line = f.readline()
            partition = line.split(" ")

            if line.startswith('#'):
                continue
            if not partition:
                continue

            if partition[0] == 'v':
                vertex_array.append(tuple(map(float,(partition[1], partition[2], partition[3]))))
            if partition[0] == 'vn':
                normal_array.append(tuple(map(float,(partition[1], partition[2], partition[3]))))
            if partition[0] == 'f':
                total_face += 1

                length = len(partition) - 1
                if length == 3:
                    face_3v += 1
                elif length == 4:
                    face_4v += 1
                elif length > 4:
                    face_over_4 += 1

                #TODO: refactoring
                tempN = []
                tempV = []

                for i in partition[1:]:
                    index_normal = normal_array[int(i.split("/")[-1]) - 1]
                    index_vertex = vertex_array[int(i.split("/")[0]) - 1]

                    if length == 3:
                        index_3vn_array.append(index_normal)
                        index_3v_array.append(index_vertex)
                    elif length == 4:
                        index_4vn_array.append(index_normal)
                        index_4v_array.append(index_vertex)
                    elif length > 4:
                        tempN.append(index_normal)
                        tempV.append(index_vertex)
                        if len(tempV) == length:
                            tempN = np.array(tempN, 'float32')
                            tempV = np.array(tempV, 'float32')
                            
                            index_polygonn_array.append(tempN)
                            index_polygon_array.append(tempV)
                            
                            tempN = []
                            tempV = []
                            
            if not line:
                break

    gIndexArray3v = np.array(index_3v_array, 'float32')
    gIndexArray3vn = np.array(index_3vn_array, 'float32')
    gIndexArray4v = np.array(index_4v_array, 'float32')
    gIndexArray4vn = np.array(index_4vn_array, 'float32')
    gIndexArrayPolygon = index_polygon_array
    gIndexArrayPolygonn = index_polygonn_array
    drawFlag = True

    print("File name: ", fileName)
    print("Total number of faces: ", total_face)
    print("Number of faces with 3 vertices: ", face_3v)
    print("Number of faces with 4 vertices: ", face_4v)
    print("Number of faces with more than 4 vertices: ", face_over_4, end="\n\n")

def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(640,640,"Obj viewer", None,None)
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