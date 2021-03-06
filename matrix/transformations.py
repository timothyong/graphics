import math
import sys

trans_mat = [ [ 0 for x in range(4) ] for y in range(4) ]
edge_mat = []

max_width = 500
max_height= 500

wmove_pix = 0
wscale = 1
hmove_pix = 0
hscale = 1

pic = [["0 0 0 " for y in range(max_height)] for x in range(max_width)]

def parse():
    global trans_mat
    global edge_mat
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
            line = f.readline().replace("\n","")
            parts = line.split()
            world_to_render(xleft,ybottom,xright,ytop,int(parts[1]), int(parts[2]))
            
        elif parts[0] == "line":
            add_line(float(parts[1]),float(parts[2]),float(parts[3]),float(parts[4]),float(parts[5]),float(parts[6]))
        elif parts[0] == "identity":
            trans_mat = make_iden(trans_mat)
        elif parts[0] == "move":
            transform(float(parts[1]),float(parts[2]),float(parts[3]))
        elif parts[0] == "scale":
            scale(float(parts[1]),float(parts[2]),float(parts[3]))
        elif parts[0] == "rotate-x":
            rotate_x(int(parts[1]))
        elif parts[0] == "rotate-y":
            rotate_y(int(parts[1]))
        elif parts[0] == "rotate-z":
            rotate_z(int(parts[1]))
        elif parts[0] == "transform":
            edge_mat = mult(trans_mat, edge_mat)
        elif parts[0] == "render-parallel":
            render_parallel()
        elif parts[0] == "sphere":
            sphere(float(parts[1]),float(parts[2]),float(parts[3]),float(parts[4]))
        elif parts[0] == "render-perspective-cyclops":
            render_perspective_cyclops(float(parts[1]),float(parts[2]),float(parts[3]),"255 255 255 ")
        elif parts[0] == "render-perspective-stereo":
            new_edge = []
            for x in range(len(edge_mat)):
                new_edge.append(edge_mat[x])
            ex = float(parts[1])
            ey = float(parts[2])
            ez = float(parts[3])
            ax = float(parts[4])
            ay = float(parts[5])
            az = float(parts[6])
            new_mat = new_edge
            for x in range(len(new_mat) / 2):
                draw_line("255 0 0 ", 
                          ((ex-(ez * (new_edge[2*x][0] - ex) / (new_edge[2*x][2] - ez))) + wmove_pix) * wscale,
                          ((ey-(ez * (new_edge[2*x][1] - ey) / (new_edge[2*x][2] - ez))) + hmove_pix) * hscale,
                          ((ex-(ez * (new_edge[2*x+1][0] - ex) / (new_edge[2*x+1][2] - ez))) + wmove_pix) * wscale,
                          ((ey-(ez * (new_edge[2*x+1][1] - ey) / (new_edge[2*x+1][2] - ez))) + hmove_pix) * hscale)
                draw_line("0 180 180 ",
                          ((ax-(az * (new_edge[2*x][0] - ax) / (new_edge[2*x][2] - az))) + wmove_pix) * wscale,
                          ((ay-(az * (new_edge[2*x][1] - ay) / (new_edge[2*x][2] - az))) + hmove_pix) * hscale,
                          ((ax-(az * (new_edge[2*x+1][0] - ax) / (new_edge[2*x+1][2] - az))) + wmove_pix) * wscale,
                          ((ay-(az * (new_edge[2*x+1][1] - ay) / (new_edge[2*x+1][2] - az))) + hmove_pix) * hscale)
        elif parts[0] == "clear-edges":
            clear_edge()
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

def render_parallel():
    new_mat = edge_mat
    for x in range(len(edge_mat)):
        new_mat[x][0] = (edge_mat[x][0] + wmove_pix) * wscale
        new_mat[x][1] = (edge_mat[x][1] + hmove_pix) * hscale
    for x in range(len(new_mat) / 2):
        draw_line("255 255 255 ", new_mat[2*x][0], new_mat[2*x][1], new_mat[2*x+1][0], new_mat[2*x+1][1])

def render_perspective_cyclops(ex,ey,ez,color):
    new_mat = edge_mat
    for x in range(len(edge_mat)):
        new_mat[x][0] = ((ex-(ez * (edge_mat[x][0] - ex) / (edge_mat[x][2] - ez))) + wmove_pix) * wscale
        new_mat[x][1] = ((ey-(ez * (edge_mat[x][1] - ey) / (edge_mat[x][2] - ez))) + hmove_pix) * hscale
    for x in range(len(new_mat) / 2):
        draw_line(color, new_mat[2*x][0], new_mat[2*x][1], new_mat[2*x+1][0], new_mat[2*x+1][1])

def world_to_render(xleft, ybottom, xright, ytop, width, height):
    global pic
    global wmove_pix, hmove_pix, wscale, hscale
    global max_width, max_height
    max_width = width
    max_height= height
    pic = [["0 0 0 " for y in range(width)] for x in range(height)]
    wmove_pix = 0 - xleft
    hmove_pix = 0 - ybottom
    wscale = int(width / (xright - xleft))
    hscale = int(height / (ytop - ybottom))

def clear_edge():
    global edge_mat
    edge_mat = []

def clear_pic():
    global pic
    pic = [["0 0 0 " for y in range(max_height)] for x in range(max_width)]

def sphere(r, x, y, z):
    global edge_matrix
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
        print circlematrix
    for i in range(36):
        for j in range(36):
            if i != 0:
                add_line(circlematrix[i][j][0], circlematrix[i][j][1], circlematrix[i][j][2],
                         circlematrix[i-1][j][0], circlematrix[i-1][j][1], circlematrix[i-1][j][2])
            if j != 0:
                add_line(circlematrix[i][j][0], circlematrix[i][j][1], circlematrix[i][j][2],
                         circlematrix[i][j-1][0], circlematrix[i][j-1][1], circlematrix[i][j-1][2])
                        
def add_line(x1,y1,z1,x2,y2,z2):
    global edge_mat
    length = len(edge_mat)
    points = [[0-x1,0-y1,z1,1],[0-x2,0-y2,z2,1]]
    for x in range(2):
        edge_mat.append(points[x])

def make_iden(mat):
    for x in range(4):
        for y in range(4):
            if x == y:
                mat[x][y] = 1
    return mat

def transform(x1,y1,z1):
    global trans_mat
    new_mat = [ [ 0 for x in range(4) ] for y in range(4) ]
    new_mat = make_iden(new_mat)
    values = [0-x1,0-y1,z1,1]
    for x in range(4):
        new_mat[3][x] = values[x]
    trans_mat = mult(new_mat,trans_mat)

def scale(x1,y1,z1):
    global trans_mat
    new_mat = [ [ 0 for x in range(4) ] for y in range(4) ]
    new_mat = make_iden(new_mat)
    values = [x1,y1,z1,1]
    for x in range(4):
        new_mat[x][x] =values[x]
    trans_mat = mult(new_mat,trans_mat)

def rotate_x(rx):
    global trans_mat
    new_mat = [ [ 0 for x in range(4) ] for y in range(4) ]
    new_mat = make_iden(new_mat)
    new_mat[1][1] = math.cos(math.radians(0-rx))
    new_mat[1][2] = 0 - math.sin(math.radians(0-rx))
    new_mat[2][1] = math.sin(math.radians(0-rx))
    new_mat[2][2] = math.cos(math.radians(0-rx))
    trans_mat = mult(new_mat,trans_mat)

def rotate_y(ry):
    global trans_mat    
    new_mat = [ [ 0 for x in range(4) ] for y in range(4) ]
    new_mat = make_iden(new_mat)
    new_mat[0][0] = math.cos(math.radians(0-ry))
    new_mat[0][2] = math.sin(math.radians(0-ry))
    new_mat[2][0] = 0 - math.sin(math.radians(0-ry))
    new_mat[2][2] = math.cos(math.radians(0-ry))
    trans_mat = mult(new_mat,trans_mat)

def rotate_z(rz):
    global trans_mat
    new_mat = [ [ 0 for x in range(4) ] for y in range(4) ]
    new_mat = make_iden(new_mat)
    new_mat[0][0] = 0-math.cos(math.radians(0-rz))
    new_mat[0][1] = 0 - math.sin(math.radians(0-rz))
    new_mat[1][0] = math.sin(math.radians(0-rz))
    new_mat[1][1] = 0-math.cos(math.radians(0-rz))
    trans_mat = mult(new_mat,trans_mat)

def mult(mat,mat2):
    new_mat = [ [ 0 for x in range(4) ] for y in range(len(mat2)) ]
    for col in range(len(mat2)):
        for row in range(4):
            new_mat[col][row] = (mat[0][row]*mat2[col][0] + 
                                 mat[1][row]*mat2[col][1] + 
                                 mat[2][row]*mat2[col][2] + 
                                 mat[3][row]*mat2[col][3])
    return new_mat

parse()
sphere(5,1,1,1)
