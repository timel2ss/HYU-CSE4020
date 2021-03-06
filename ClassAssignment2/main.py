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
gIndexArray3vnCal = None
gIndexArray4vnCal = None
gIndexArrayPolynCal = None


animationObject = []

# True: perspective projection, False: orthogonal projection
projection = True
# True: solid mode, False: wireframe
filled = False
# True: animation on, False: animation off
hierarchy = False
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
    
    if hierarchy == True:
        drawAnimation()
    if drawFlag == True:
        drawObject((gIndexArray3v, gIndexArray3vn, gIndexArray4v, gIndexArray4vn, gIndexArrayPolygon, gIndexArrayPolygonn, gIndexArray3vnCal, gIndexArray4vnCal, gIndexArrayPolynCal))
    
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
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd()

def drawObject(drawElement):
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)

    if shading == False:
        glNormalPointer(GL_FLOAT, 3*drawElement[1].itemsize, drawElement[1])
    else:
        glNormalPointer(GL_FLOAT, 3*drawElement[6].itemsize, drawElement[6])
    glVertexPointer(3, GL_FLOAT,3*drawElement[0].itemsize, drawElement[0])
    glDrawArrays(GL_TRIANGLES, 0, int(drawElement[0].size/3))

    if shading == False:
        glNormalPointer(GL_FLOAT, 3*drawElement[3].itemsize, drawElement[3])
    else:
        glNormalPointer(GL_FLOAT, 3*drawElement[7].itemsize, drawElement[7])
    glVertexPointer(3, GL_FLOAT, 3*drawElement[2].itemsize, drawElement[2])
    glDrawArrays(GL_QUADS, 0, int(drawElement[2].size/3))

    for i in range(len(drawElement[4])):
        if shading == False:
            glNormalPointer(GL_FLOAT, 3*drawElement[5][i].itemsize, drawElement[5][i])
        else:
            glNormalPointer(GL_FLOAT, 3*drawElement[8].itemsize, drawElement[8])
        glVertexPointer(3, GL_FLOAT, 3*drawElement[4][i].itemsize, drawElement[4][i])
        glDrawArrays(GL_POLYGON, 0, int(drawElement[4][i].size/3))

def drawAnimation():
    t = glfw.get_time()
    glPushMatrix()
    glRotatef(t * (180 / np.pi), 0, 1, 0)

    glPushMatrix()
    glScalef(100, 100, 100)
    drawObject(animationObject[0])
    glPopMatrix()

    glPushMatrix()
    glTranslatef(3, 1.5, 0)
    glRotatef(t * (180/np.pi), 0, 1, 0)

    glPushMatrix()
    glScalef(.02, .02, .02)
    glRotatef(-90, 1, 0, 0)
    drawObject(animationObject[1])
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 1.5, 0)
    glRotatef(-50, 1, 0, 0)
    glRotatef(t * (180/np.pi), 0, 0, 1)
    drawObject(animationObject[2])
    glPopMatrix()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-3, 1.5, 0)
    glRotatef(t * (180/np.pi), 0, 1, 0)

    glPushMatrix()
    glScalef(.02, .02, .02)
    glRotatef(-90, 1, 0, 0)
    drawObject(animationObject[1])
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 1.5, 0)
    glRotatef(-50, 1, 0, 0)
    glRotatef(t * (180/np.pi), 0, 0, 1)
    drawObject(animationObject[2])
    glPopMatrix()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 1.5, 3)
    glRotatef(t * (180/np.pi), 0, 1, 0)

    glPushMatrix()
    glScalef(.02, .02, .02)
    glRotatef(-90, 1, 0, 0)
    drawObject(animationObject[1])
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 1.5, 0)
    glRotatef(-50, 1, 0, 0)
    glRotatef(t * (180/np.pi), 0, 0, 1)
    drawObject(animationObject[2])
    glPopMatrix()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 1.5, -3)
    glRotatef(t * (180/np.pi), 0, 1, 0)

    glPushMatrix()
    glScalef(.02, .02, .02)
    glRotatef(-90, 1, 0, 0)
    drawObject(animationObject[1])
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 1.5, 0)
    glRotatef(-50, 1, 0, 0)
    glRotatef(t * (180/np.pi), 0, 0, 1)
    drawObject(animationObject[2])
    glPopMatrix()
    glPopMatrix()

    glPopMatrix()

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
    global projection, filled, hierarchy, drawFlag, animationObject, shading
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
        if key == glfw.KEY_H:
            if hierarchy == True:
                hierarchy = False
                animationObject = []
            else:
                hierarchy = True
                drawFlag = False
                animationObject.append(obj_parse("Plate.obj"))
                animationObject.append(obj_parse("Spinning_Teacup.obj"))
                animationObject.append(obj_parse("spoon.obj"))
        if key == glfw.KEY_S:
            if shading == True:
                shading = False
            else:
                shading = True

def drop_callback(window, paths):
    global gIndexArray3v, gIndexArray3vn, gIndexArray4v, gIndexArray4vn, gIndexArrayPolygon, gIndexArrayPolygonn, gIndexArray3vnCal, gIndexArray4vnCal, gIndexArrayPolynCal, drawFlag, hierarchy
    gIndexArray3v, gIndexArray3vn, gIndexArray4v, gIndexArray4vn, gIndexArrayPolygon, gIndexArrayPolygonn, gIndexArray3vnCal, gIndexArray4vnCal, gIndexArrayPolynCal = obj_parse(paths[0])
    drawFlag = True
    hierarchy = False

def obj_parse(path):
    global shading
    vertex_array = []
    normal_array = []
    index_3v_array = []
    index_3vn_array = []
    index_4v_array = []
    index_4vn_array = []
    index_polygon_array = []
    index_polygonn_array = []
    iarr3v = []
    iarr4v = []
    iarrPoly = []
    normal_cal = []
    normal_cal_3v = []
    normal_cal_4v = []
    normal_cal_poly = []

    total_face = 0
    face_3v = 0
    face_4v = 0
    face_over_4 = 0

    with open(path, "r") as f:
        fileName = path.split("\\")[-1]

        while True:
            line = f.readline()
            if not line:
                break
            if line.startswith('#'):
                continue

            partition = line.split()
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

                tempI = []
                tempN = []
                tempV = []

                for i in partition[1:]:
                    face_parse = i.split('/')
                    index_normal = normal_array[int(face_parse[-1]) - 1]
                    index_vertex = vertex_array[int(face_parse[0]) - 1]

                    if length == 3:
                        iarr3v.append(int(face_parse[0]) - 1)
                        index_3vn_array.append(index_normal)
                        index_3v_array.append(index_vertex)
                    elif length == 4:
                        iarr4v.append(int(face_parse[0]) - 1)
                        index_4vn_array.append(index_normal)
                        index_4v_array.append(index_vertex)
                    elif length > 4:
                        tempI.append(int(face_parse[0]) - 1)
                        tempN.append(index_normal)
                        tempV.append(index_vertex)
                        if len(tempV) == length:
                            tempN = np.array(tempN, 'float32')
                            tempV = np.array(tempV, 'float32')

                            iarrPoly.append(tempI)
                            index_polygonn_array.append(tempN)
                            index_polygon_array.append(tempV)

                            tempI = []
                            tempN = []
                            tempV = []

        adjacent = [[] for i in range(len(vertex_array))]
        index_3v_array = np.array(index_3v_array, 'float32')
        index_4v_array = np.array(index_4v_array, 'float32')


        for i in range(0, len(index_3v_array), 3):
            v1 = index_3v_array[i + 1] - index_3v_array[i]
            v2 = index_3v_array[i + 2] - index_3v_array[i]

            n = np.cross(v1, v2)
            n = n / np.sqrt(np.dot(n, n))
            for j in range(3):
                adjacent[iarr3v[i + j]].append(n)
        

        for i in range(0, len(index_4v_array), 4):
            v1 = index_4v_array[i + 1] - index_4v_array[i]
            v2 = index_4v_array[i + 3] - index_4v_array[i]
            
            n = np.cross(v1, v2)
            n = n / np.sqrt(np.dot(n, n))

            for j in range(4):
                adjacent[iarr4v[i + j]].append(n)

        for i in range(len(index_polygon_array)):
            for j in range(0, i, len(index_polygon_array[i])):
                v1 = index_polygon_array[i][j + 1] - index_polygon_array[i][j]
                v2 = index_polygon_array[i][j + len(index_polygon_array[i]) - 1] - index_polygon_array[i][j]
                
                n = np.cross(v1, v2)
                n = n / np.sqrt(np.dot(n, n))

                for k in range(len(index_polygon_array[i])):
                    adjacent[iarrPoly[i][j + k]].append(n)
        
        for i in range(len(adjacent)):
            sum = np.array([0, 0, 0], 'float32')
            for j in range(len(adjacent[i])):
                sum += adjacent[i][j]
            sum = sum / np.sqrt(np.dot(sum, sum))
            normal_cal.append(sum)

        for i in iarr3v:
            normal_cal_3v.append(normal_cal[i])
        for i in iarr4v:
            normal_cal_4v.append(normal_cal[i])
        for i in iarrPoly:
            tempN = []
            for j in i:
                tempN.append(normal_cal[j])
            tempN = np.array(tempN, 'float32')
            normal_cal_poly.append(tempN)

    gIndexArray3v = np.array(index_3v_array, 'float32')
    gIndexArray3vn = np.array(index_3vn_array, 'float32')
    gIndexArray4v = np.array(index_4v_array, 'float32')
    gIndexArray4vn = np.array(index_4vn_array, 'float32')
    gIndexArrayPolygon = index_polygon_array
    gIndexArrayPolygonn = index_polygonn_array
    gIndexArray3vnCal = np.array(normal_cal_3v, 'float32')
    gIndexArray4vnCal = np.array(normal_cal_4v, 'float32')
    gIndexArrayPolynCal = np.array(normal_cal_poly, 'float32')
    
    print("File name: ", fileName)
    print("Total number of faces: ", total_face)
    print("Number of faces with 3 vertices: ", face_3v)
    print("Number of faces with 4 vertices: ", face_4v)
    print("Number of faces with more than 4 vertices: ", face_over_4, end="\n\n")

    return (gIndexArray3v, gIndexArray3vn, gIndexArray4v, gIndexArray4vn, gIndexArrayPolygon, gIndexArrayPolygonn, gIndexArray3vnCal, gIndexArray4vnCal, gIndexArrayPolynCal)

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