import math
import sys
from copy import deepcopy

def parser():
    global f,number,frames
    f.seek(0)
    vars = []
    while i < len(lines):
        line = f.readline().replace("\n","")
        parts = line.split()
        if parts[0] == "frames":
            frames = int(parts[2])
        elif parts[0] == "vary":
            vars.append([parts[1],int(parts[2]),int(parts[3]),int(parts[4]),int(parts[5])])
        elif parts[0] == "files":
            file_name = parts[1]
    while number < frames:
        f.seek(0)
        for x in range(len(vars)):
            f.seek(0)
            line = f.readline()
            if line.find(vars[x][1]):
                if number < vars[x][5] and number > vars[x][4]:
                    try:
                        line.replace(vars[x][1], vars[x][2] + (number * vars[x][3] / frames))
                    except: 
                        pass
        parse()
        number = number + 1

def parse():
    global f,width,height,w_trans,h_trans,w_scale,h_scale
    f.seek(0)
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
            width = int(parts[1])
            height = int(parts[2])
            pixels = [["0 0 0 " for x in range(width)] for y in range(height)]
            w_trans = xright
            h_trans = ytop
            w_scale = width / (xright - xleft)
            h_scale = height / (ytop - y_bottom)
        elif parts[0] == "box-t":
            add_box(float(parts[1]),float(parts[2]),float(parts[3]),float(parts[4]),float(parts[5]),float(parts[6]),
                    float(parts[7]),float(parts[8]),float(parts[9]))
        elif parts[0] == "sphere-t":
            add_sphere(float(parts[1]),float(parts[2]),float(parts[3]),float(parts[4]),float(parts[5]),float(parts[6]),
                       float(parts[7]),float(parts[8]),float(parts[9]))
        elif parts[0] == "identity":
            trans_mat = deepcopy(saved['ident'])
        elif parts[0] == "move":
            m = move(float(parts[1]),float(parts[2]),float(parts[3]))
            trans_mat = matrix_mult(m, trans_mat)
        elif parts[0] == "scale":
            s = scale(float(parts[1]),float(parts[2]),float(parts[3]))
            trans_mat = matrix_mult(s, trans_mat)
        elif parts[0] == "rotate-x":
            rx = rotate_x(float(parts[1]))
            trans_mat = matrix_mult(rx, trans_mat)
        elif parts[0] == "rotate-y":
            ry = rotate_y(float(parts[1]))
            trans_mat = matrix_mult(ry, trans_mat)
        elif parts[0] == "rotate-z":
            rz = rotate_z(float(parts[1]))
            trans_mat = matrix_mult(rz, trans_mat)
        elif parts[0] == "render-parallel":
            render_parallel()
        elif parts[0] == "render-perspective-cyclops":
            render_perspective_cyclops(float(parts[1]),float(parts[2]),float(parts[3]),"255 255 255 ")
        elif parts[0] == "render-perspective-stereo":
            render_perspective_cyclops(float(parts[1]),float(parts[2]),float(parts[3]),"255 0 0 ")
            render_perspective_cyclops(float(parts[4]),float(parts[5]),float(parts[6]),"0 180 180 ")
        elif parts[0] == "save":
            saved[parts[1]] = deepcopy(trans_mat)
        elif parts[0] == "restore":
            trans_mat = deepcopy(saved[parts[1]])
        elif parts[0] == "files":
            strnum = ""
            if number < 10:
                strnum = "00" + str(number)
            elif number < 100:
                strnum = "0" +str(number)
            else: 
                strnum = str(number)
            output = open(file_name + strnum, "w")
            output.write("P3 %s %s 255 "%(width, height))
            for x in pic:
                for y in x:
                    output.write(y)
            output.close()

def render_parallel():
    x = 0
    while x < len(trig_mat) - 2:
        t1 = [trig_mat[x+1][0] - trig_mat[x][0], 
              trig_mat[x+1][1] - trig_mat[x][1], 
              trig_mat[x+1][2] - trig_mat[x][2]]
        t2 = [trig_mat[x+2][0] - trig_mat[x+1][0],
              trig_mat[x+2][1] - trig_mat[x+1][1],
              trig_mat[x+2][2] - trig_mat[x+1][2]]
        s = [trig_mat[x][0],
             trig_mat[x][1],
             trig_mat[x][2] - 1]
        n = [t1[1]*t2[2]-t1[2]*t2[1], t1[2]*t2[0]-t1[0]*t2[2], t1[0]*t2[1]-t1[1]*t2[0]]
        dot = n[0]*s[0]+n[1]*s[1]+n[2]*s[2]
        if dot < 0:
            draw_line((trig_mat[x][0] + w_move) * w_scale,
                      (trig_mat[x][1] + h_move) * h_scale,
                      (trig_mat[x+1][0] + w_move) * w_scale,
                      (trig_mat[x+1][1] + h_move) * h_scale, "0 0 0 ")
            draw_line((trig_mat[x+1][0] + w_move) * w_scale,
                      (trig_mat[x+1][1] + h_move) * h_scale,
                      (trig_mat[x+2][0] + w_move) * w_scale,
                      (trig_mat[x+2][1] + h_move) * h_scale, "0 0 0 ")
            draw_line((trig_mat[x+2][0] + w_move) * w_scale,
                      (trig_mat[x+2][1] + h_move) * h_scale,
                      (trig_mat[x][0] + w_move) * w_scale,
                      (trig_mat[x][1] + h_move) * h_scale, "0 0 0 ")
        x += 3

def render_perspective_cyclops(ex,ey,ez):
    x = 0
    while x < len(trig_mat) - 2:
        t1 = [trig_mat[x+1][0] - trig_mat[x][0],
              trig_mat[x+1][1] - trig_mat[x][1],
              trig_mat[x+1][2] - trig_mat[x][2]]
        t2 = [trig_mat[x+2][0] - trig_mat[x+1][0],
              trig_mat[x+2][1] - trig_mat[x+1][1],
              trig_mat[x+2][2] - trig_mat[x+1][2]]
        s = [trig_mat[x][0] - ex,
             trig_mat[x][1] - ey,
             trig_mat[x][2] - ez]
        n = [t1[1]*t2[2]-t1[2]*t2[1], t1[2]*t2[0]-t1[0]*t2[2], t1[0]*t2[1]-t1[1]*t2[0]]
        dot = n[0]*s[0]+n[1]*s[1]+n[2]*s[2]
        if dot < 0:
            draw_line(trig_mat[x][0],trig_mat[x][1],trig_mat[x][2],
                      trig_mat[x+1][0],trig_mat[x+1][1],trig_mat[x+1][2], "0 0 0 ")
            draw_line(trig_mat[x+1][0],trig_mat[x+1][1],trig_mat[x+1][2],
                      trig_mat[x+2][0],trig_mat[x+2][1],trig_mat[x+2][2], "0 0 0 ")
            draw_line(trig_mat[x+2][0],trig_mat[x+2][1],trig_mat[x+2][2],
                      trig_mat[x][0],trig_mat[x][1],trig_mat[x][2], "0 0 0 ")
            x += 3

def box_t(sx,sy,sz,rx,ry,rz,mx,my,mz):
    global trig_mat
    box = [[-0.5,-0.5,0.5,1], [0.5,-0.5,0.5,1], [0.5,0.5,0.5,1], [-0.5,-0.5,0.5,1], [0.5,0.5,0.5,1], [-0.5,0.5,0.5,1],
           [-0.5,0.5,0.5,1], [0.5,0.5,0.5,1], [0.5,0.5,-0.5,1], [-0.5,0.5,0.5,1], [0.5,0.5,-0.5,1], [-0.5,0.5,-0.5,1],
           [-0.5,0.5,-0.5,1], [0.5,0.5,-0.5,1], [0.5,-0.5,-0.5,1], [-0.5,0.5,-0.5,1], [0.5,-0.5,-0.5,1], [-0.5,-0.5,-0.5,1],
           [-0.5,-0.5,0.5,1], [0.5,-0.5,0.5,1], [0.5,-0.5,-0.5,1], [-0.5,-0.5,0.5,1], [0.5,-0.5,-0.5,1], [-0.5,-0.5,-0.5,1],
           [0.5,-0.5,0.5,1], [0.5,-0.5,-0.5,1], [0.5,0.5,-0.5,1], [0.5,-0.5,0.5,1], [0.5,0.5,-0.5,1], [0.5,0.5,0.5,1],
           [-0.5,-0.5,0.5,1], [-0.5,0.5,0.5,1], [-0.5,-0.5,-0.5,1], [-0.5,-0.5,-0.5,1], [-0.5,0.5,0.5,1], [-0.5,0.5,-0.5,1]]
    box = matrix_mult(scale(sx,sy,sz), box)
    box = matrix_mult(rotate_x(rx), box)
    box = matrix_mult(rotate_y(ry), box)
    box = matrix_mult(rotate_z(rz), box)
    box = matrix_mult(move(mx,my,mz), box)
    box = matrix_mult(trans_mat, box)
    for x in range(len(box)):
        trig_mat.append(box[x])

def sphere_t(sx,sy,sz,rx,ry,rz,mx,my,mz):
    

def new_matrix(rows = 4, cols = 4):
    m = []
    for c in range( cols ):
        m.append( [] )
        for r in range( rows ):
            m[c].append( 0 )
    return m

def matrix_mult( m1, m2 ):
    product = [[0 for x in range(4)] for y in range(len(m2))]
    for row in range(4):
        for col in range(len(m2[0])):
            product[row][col] = (m1[row][0]*m2[0][col] + 
                                 m1[row][1]*m2[1][col] + 
                                 m1[row][2]*m2[2][col] + 
                                 m1[row][3]*m2[3][col])
    return product

def move( x, y, z ):
    t = new_matrix()
    t = deepcopy(saved['ident'])
    t[3][0] = x
    t[3][1] = y
    t[3][2] = z
    return t

def scale( x, y, z ):
    s = new_matrix()
    s = deepcopy(saved['ident'])
    s[0][0] = x
    s[1][1] = y
    s[2][2] = z
    return s
    
def rotate_x( theta ):    
    rx = new_matrix()
    rx = deepcopy(saved['ident'])
    theta = math.radians(theta)
    rx[1][1] = math.cos( theta )
    rx[2][1] = -1 * math.sin( theta )
    rx[1][2] = math.sin( theta )
    rx[2][2] = math.cos( theta )
    return rx

def rotate_y( theta ):
    ry = new_matrix()
    ry = deepcopy(saved['ident'])
    theta = math.radians(theta)
    ry[0][0] = math.cos( theta )
    ry[2][0] = -1 * math.sin( theta )
    ry[0][2] = math.sin( theta )
    ry[2][2] = math.cos( theta )
    return ry

def rotate_z( theta ):
    rz = new_matrix()
    rz = deepcopy(saved['ident'])
    theta = math.radians(theta)
    rz[0][0] = math.cos( theta )
    rz[1][0] = -1 * math.sin( theta )
    rz[0][1] = math.sin( theta )
    rz[1][1] = math.cos( theta )
    return rz

saved = {'ident':[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]}
trans_mat = deepcopy(saved['ident'])
pixels = []
trig_mat = []
height = 0
width = 0
w_trans = 0
h_trans = 0
w_scale = 1
h_scale = 1
file_name = ""
number = 0
frames = 0
f = open(sys.argv[1], "r")
lines = f.readlines()
f.seek(0)
i = 0
