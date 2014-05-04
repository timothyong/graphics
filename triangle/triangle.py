import math
import sys
from copy import deepcopy

trans_mat = [ [ 0 for x in range(4) ] for y in range(4) ]
for x in range(4):
	for y in range(4):
		if x == y:
			trans_mat[x][y] = 1
trig_mat = []

max_width = 500
max_height= 500

xleft = 0
xright = 0
ybottom = 0
ytop = 0

pic = [["0 0 0 " for y in range(max_height)] for x in range(max_width)]

def parse():
    global trans_mat
    global trig_mat
    global xleft,xright,ybottom,ytop,pic
    global max_height, max_width
    f = open(sys.argv[1], "r")
    lines = f.readlines()
    f.seek(0)
    i = 0
    while i < len(lines):
        line = f.readline().replace("\n","")
        parts = line.split()
        if parts[0] == "screen":
            xleft = float(parts[1])
            ybottom = float(parts[2])
            xright = float(parts[3])
            ytop = float(parts[4])
        elif parts[0] == "pixels":
            max_height = int(parts[2])
            max_width = int(parts[1])
            pic = [["0 0 0 " for y in range(max_height)] for x in range(max_width)]
        elif parts[0] == "box-t":
            add_box(float(parts[1]),float(parts[2]),float(parts[3]),float(parts[4]),float(parts[5]),float(parts[6]),
                    float(parts[7]),float(parts[8]),float(parts[9]))
        elif parts[0] == "identity":
            trans_mat = make_iden(trans_mat)
        elif parts[0] == "move":
            translate(float(parts[1]),float(parts[2]),float(parts[3]))
        elif parts[0] == "scale":
            scale(float(parts[1]),float(parts[2]),float(parts[3]))
        elif parts[0] == "rotate-x":
            rotate_x(int(parts[1]))
        elif parts[0] == "rotate-y":
            rotate_y(int(parts[1]))
        elif parts[0] == "rotate-z":
            rotate_z(int(parts[1]))
        elif parts[0] == "render-parallel":
            render_parallel()
        elif parts[0] == "sphere-t":
            add_sphere(float(parts[1]),float(parts[2]),float(parts[3]),float(parts[4]),float(parts[5]),float(parts[6]),
                       float(parts[7]),float(parts[8]),float(parts[9]))
        elif parts[0] == "render-perspective-cyclops":
            render_perspective_cyclops(float(parts[1]),float(parts[2]),float(parts[3]),"255 255 255 ")
        elif parts[0] == "render-perspective-stereo":
            render_perspective_stereo(float(parts[1]), float(parts[2]), float(parts[3]), 
                                      float(parts[4]), float(parts[5]), float(parts[6]))
        elif parts[0] == "clear-triangles":
            clear_trig()
        elif parts[0] == "clear-pixels":
            clear_pix()
        elif parts[0] == "file":
            file(parts[1])
        elif parts[0] == "end":
            f.close()
            break

def file(name):
    global max_height, max_width
    output = open(name, "w")
    output.write("P3 %s %s 255 "%(max_width, max_height))
    for x in pic:
        for y in x:
            output.write(y)
    output.close()

def draw_line(color,x1,y1,x2,y2):
    x1 = int(x1)
    x2 = int(x2)
    y1 = int(y1)
    y2 = int(y2)
    if x1 == x2 and y1 == y2:
        pic[y1][x1] = color
    elif x1 == x2:
        if y1 > y2:
            x1,y1,x2,y2 = x2,y2,x1,y1
        x = x1
        y = y1
        while y <= y2:
            pic[y][x] = color
            y += 1
    elif y1 == y2:
        if x1 > x2:
            x1,y1,x2,y2 = x2,y2,x1,y1
        x = x1
        y = y1
        while x <= x2:
            pic[y][x] = color
            x += 1
    elif math.fabs(x1-x2) >= math.fabs(y1-y2):
        #x-major   
        if x1 >= x2:
            x1,y1,x2,y2 = x2,y2,x1,y1
        if y2 > y1:
            #up                                                                      
            x = x1
            y = y1
            acc = 0
            while (x < x2):
                x += 1
                acc += (y2 - y1)
                if acc >= x2 - x1:
                    y += 1
                    acc -= (x2 - x1)
                pic[y][x] = color
            #end up                  
        else:
            #down    
            x = x1
            y = y1
            acc = 0
            while (x < x2):
                x += 1
                acc += (y1 - y2)
                if acc >= x2 - x1:
                    y -= 1
                    acc -= (x2 - x1)
                pic[y][x] = color
            #end down
        #end x-major
    else:
        if y1 >= y2:
            x1,y1,x2,y2 = x2,y2,x1,y1
        if x2 > x1:
            x = x1
            y = y1
            acc = 0
            while (y < y2):
                y += 1
                acc += (x2 - x1)
                if acc >= y2 - y1:
                    x += 1
                    acc -= (y2 - y1)
                pic[y][x] = color
        else:
            x = x1
            y = y1
            acc = 0
            while (y < y2):
                y += 1
                acc += (x1 - x2)
                if acc >= y2 - y1:
                    x -= 1
                    acc -= (y2 - y1)
                pic[y][x] = color


def add_box(sx,sy,sz, rx,ry,rz, mx,my,mz):
    global trig_mat
    box = [[-0.5,-0.5,0.5,1], [0.5,-0.5,0.5,1], [0.5,0.5,0.5,1], [-0.5,-0.5,0.5,1], [0.5,0.5,0.5,1], [-0.5,0.5,0.5,1],
           [-0.5,0.5,0.5,1], [0.5,0.5,0.5,1], [0.5,0.5,-0.5,1], [-0.5,0.5,0.5,1], [0.5,0.5,-0.5,1], [-0.5,0.5,-0.5,1],
           [-0.5,0.5,-0.5,1], [0.5,0.5,-0.5,1], [0.5,-0.5,-0.5,1], [-0.5,0.5,-0.5,1], [0.5,-0.5,-0.5,1], [-0.5,-0.5,-0.5,1],
           [-0.5,-0.5,0.5,1], [0.5,-0.5,0.5,1], [0.5,-0.5,-0.5,1], [-0.5,-0.5,0.5,1], [0.5,-0.5,-0.5,1], [-0.5,-0.5,-0.5,1],
           [0.5,-0.5,0.5,1], [0.5,-0.5,-0.5,1], [0.5,0.5,-0.5,1], [0.5,-0.5,0.5,1], [0.5,0.5,-0.5,1], [0.5,0.5,0.5,1],
           [-0.5,-0.5,0.5,1], [-0.5,0.5,0.5,1], [-0.5,-0.5,-0.5,1], [-0.5,-0.5,-0.5,1], [-0.5,0.5,0.5,1], [-0.5,0.5,-0.5,1]]
    for x in range(36):
        box[x][0] = box[x][0] * sx
        box[x][1] = box[x][1] * sy
        box[x][2] = box[x][2] * sz

    rotatex = [ [0 for x in range(4)] for y in range(4)]
    rotatex = make_iden(rotatex)
    rotatex[1][1] = math.cos(math.radians(rx))
    rotatex[1][2] = 0 - math.sin(math.radians(rx))
    rotatex[2][1] = math.sin(math.radians(rx))
    rotatex[2][2] = math.cos(math.radians(rx))
    mult(rotatex, box)

    rotatey = [ [0 for x in range(4)] for y in range(4)]
    rotatey = make_iden(rotatey)
    rotatey[0][0] = math.cos(math.radians(ry))
    rotatey[0][2] = math.sin(math.radians(ry))
    rotatey[2][0] = 0 - math.sin(math.radians(ry))
    rotatey[2][2] = math.cos(math.radians(ry))
    mult(rotatey, box)

    rotatez = []
    rotatez = [ [0 for x in range(4)] for y in range(4)]
    rotatez = make_iden(rotatez)
    rotatez[0][0] = math.cos(math.radians(rz))
    rotatez[0][1] = 0 - math.sin(math.radians(rz))
    rotatez[1][0] = math.sin(math.radians(rz))
    rotatez[1][1] = math.cos(math.radians(rz))
    mult(rotatez, box)

    for x in range(36):
        box[x][0] = box[x][0] + mx
        box[x][1] = box[x][1] + my
        box[x][2] = box[x][2] + mz
        
    mult(trans_mat, box)

    print box

    for x in range(36):
        trig_mat.append(box[x])

def make_sphere(sx,sy,sz, rx,ry,rz, mx,my,mz):
    global trig_mat
    circlematrix = []
    phi = 0
    while phi <= 2 * math.pi:
        circleset = []
        theta = 0
        while theta <= 2 * math.pi:
            pointlist = []
            pointlist.append(x + r*math.sin(theta)*math.cos(phi))
            pointlist.append(y + r*math.sin(theta)*math.sin(phi))
            pointlist.append(z + r*math.cos(theta))
            circleset.append(pointlist)
            theta += math.pi * 2 / 36
        circlematrix.append(circleset)
        phi += math.pi * 2 / 36

    circlematrix = mult(circlematrix, trans_mat)

    for i in range(35):
        for j in range(35):
            if i != 0:
                trig_mat.append(circlematrix[i+1][j+1])
                trig_mat.append(circlematrix[i][j+1])
                trig_mat.append(circlematrix[i][j])
                trig_mat.append(circlematrix[i+1][j+1])
                trig_mat.append(circlematrix[i][j])
                trig_mat.append(circlematrix[i+1][j])

def make_iden(mat):
    for x in range(4):
        for y in range(4):
            if x == y:
                mat[x][y] = 1
    return mat

def mult(mat,mat2):
    new_mat = [ [ 0 for x in range(4) ] for y in range(len(mat2)) ]
    for col in range(len(mat2)):
        for row in range(4):
            new_mat[col][row] = (mat[0][row]*mat2[col][0] + 
                                 mat[1][row]*mat2[col][1] + 
                                 mat[2][row]*mat2[col][2] + 
                                 mat[3][row]*mat2[col][3])
    return new_mat

def translate(x,y,z):
    global trans_mat
    new_mat = [ [ 0 for x in range(4) for y in range(4)] ]
    new_mat = make_iden(new_mat)
    translation = [x,y,z]
    for x in range(3):
        new_mat[x][3] = translation[x]
    trans_mat = mult(trans_mat, new_mat)

def rotate_x(degrees):
    global trans_mat
    new_mat = [ [ 0 for x in range(4) ] for y in range(4) ]
    new_mat = make_iden(new_mat)
    new_mat[1][1] = math.cos(math.radians(degrees))
    new_mat[1][2] = 0 - math.sin(math.radians(degrees))
    new_mat[2][1] = math.sin(math.radians(degrees))
    new_mat[2][2] = math.cos(math.radians(degrees))
    trans_mat = mult(trans_mat, new_mat)

def rotate_y(degrees):
    global trans_mat
    new_mat = [ [ 0 for x in range(4) ] for y in range(4) ]
    new_mat = make_iden(new_mat)
    new_mat[0][0] = math.cos(math.radians(degrees))
    new_mat[0][2] = math.sin(math.radians(degrees))
    new_mat[2][0] = 0 - math.sin(math.radians(degrees))
    new_mat[2][2] = math.cos(math.radians(degrees))
    trans_mat = mult(trans_mat, new_mat)

def rotate_z(degrees):
    global trans_matrix
    new_mat = [ [ 0 for x in range(4) ] for y in range(4) ]
    new_mat = make_iden(new_mat)
    new_mat[0][0] = math.cos(math.radians(degrees))
    new_mat[0][1] = 0 - math.sin(math.radians(degrees))
    new_mat[1][0] = math.sin(math.radians(degrees))
    new_mat[1][1] = math.cos(math.radians(degrees))
    trans_mat = mult(trans_mat, new_mat)

def clear_trig():
    global trig_mat
    trig_mat = 0
    
def clear_pic():
    global pic
    pic = [["0 0 0 " for y in range(max_height)] for x in range(max_width)]

def convert_points(matrix):
    global xleft, xright, ytop, ybottom
    global max_height, max_width
    for point in matrix:
        point[0] = int(round(max_width * (point[0] - xleft)/(abs(xleft) + abs(xright))))
        point[1] = int(round(max_height * (ytop -  point[1])/(abs(ybottom) + abs(ytop))))
    return matrix

def cross(mat1, mat2):
    new_mat = []
    new_mat.append(mat1[1]*mat2[2] - mat1[2]*mat2[1])
    new_mat.append(mat1[2]*mat2[0] - mat1[0]*mat2[2])
    new_mat.append(mat1[0]*mat2[1] - mat1[1]*mat2[0])
    return new_mat

def dot(mat1, mat2):
    return mat1[0]*mat2[0] + mat1[1]*mat2[1] + mat1[2]*mat2[2]

def render_parallel():
    global trig_mat
    new_mat = trig_mat
    new_mat = convert_points(deepcopy(trig_mat))
    for x in range(len(new_mat) / 3):
        t1 = [new_mat[3*x+1][0] - new_mat[3*x][0], new_mat[3*x+1][1] - new_mat[3*x][1], new_mat[3*x+1][2] - new_mat[3*x][2], 1]
        t2 = [new_mat[3*x+2][0] - new_mat[3*x+1][0], new_mat[3*x+2][1] - new_mat[3*x+1][1], new_mat[3*x+2][2] - new_mat[3*x+1][2], 1]
        s = [ new_mat[3*x][0], new_mat[3*x][1], new_mat[3*x][2], 1 ]
        result = cross(t1, t2)
        result1 = dot(s, result)
        if result1 < 0:
            draw_line("255 255 255 ", new_mat[3*x][0], new_mat[3*x][1], new_mat[3*x+1][0], new_mat[3*x+1][1])
            draw_line("255 255 255 ", new_mat[3*x+1][0], new_mat[3*x+1][1], new_mat[3*x+2][0], new_mat[3*x+2][1])
            draw_line("255 255 255 ", new_mat[3*x+2][0], new_mat[3*x+2][1], new_mat[3*x][0], new_mat[3*x][1])
        
def render_perspective_cyclops(ex,ey,ez,color):
    global trig_mat
    new_mat = deepcopy(trig_mat)
    print trig_mat
    print new_mat
    for i in range(len(new_mat)):
        new_mat[i][0] = ex-(ez * (trig_mat[i][0] - ex) / (trig_mat[i][2] - ez))
        new_mat[i][1] = ey-(ez * (trig_mat[i][1] - ey) / (trig_mat[i][2] - ez))
    new_mat = convert_points(new_mat)
    print new_mat
    eye = [[ex,ey,ez,1]]
    eye = convert_points(eye)
    for x in range(len(new_mat) / 3):
        t1 = [new_mat[3*x+1][0] - new_mat[3*x][0], new_mat[3*x+1][1] - new_mat[3*x][1], new_mat[3*x+1][2] - new_mat[3*x][2]]
        t2 = [new_mat[3*x+2][0] - new_mat[3*x+1][0], new_mat[3*x+2][1] - new_mat[3*x+1][1], new_mat[3*x+2][2] - new_mat[3*x+1][2]]
        s = [ new_mat[3*x][0] - eye[0][0], new_mat[3*x][1] - eye[0][1], new_mat[3*x][2] - eye[0][2] ]
        
	result = cross(t1, t2)
        result1 = dot(s, result)
        if result1 < 0:
            print new_mat[3*x], new_mat[3*x+1], new_mat[3*x+2]
            draw_line(color, new_mat[3*x][0], new_mat[3*x][1], new_mat[3*x+1][0], new_mat[3*x+1][1])
            draw_line(color, new_mat[3*x+1][0], new_mat[3*x+1][1], new_mat[3*x+2][0], new_mat[3*x+2][1])
            draw_line(color, new_mat[3*x][0], new_mat[3*x][1], new_mat[3*x+2][0], new_mat[3*x+2][1])

def render_perspective_stereo(ex1,ey1,ez1,ex2,ey2,ez2):
    render_perspective_cyclops(ex1,ey1,ez1,"255 0 0 ")
    render_perspective_cyclops(ex2,ey2,ez2,"0 255 255 ")

parse()
