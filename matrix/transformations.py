import math

trans_mat = [ [ 0 for x in range(4) ] for y in range(4) ]
edge_mat = []

max_width = 500
max_height= 500

wmove_pix = 0
wscale = 1
hmove_pix = 0
hscale = 1

pixels = [["0 0 0 " for y in range(max_height)] for x in range(max_width)]

def render_parallel():
    new_mat = trans_mat
    for x in range(len(edge_mat[0])):
        new_mat[x][0] = (edge_mat[x][0] + wmove_pix) * wscale
        new_mat[x][1] = (edge_mat[x][1] + hmove_pix) * hscale
    for x in range(len(new_mat[0]) / 2):
        draw_line(new_mat[2*x][0], new_mat[2*x][1], new_mat[2*x+1][0], new_mat[2*x+1][1])

def world_to_render(xleft, ybottom, xright, ytop, width, height):
    pixels = [["0 0 0 " for y in range(height)] for x in range(width)]
    max_width = width
    max_height= height
    wmove_pix = 0 - xleft
    hmove_pix = 0 - ybottom
    wscale = width / (xright - xleft)
    hscale = height / (ytop - ybottom)

def clear_edge():
    edge_mat = []

def clear_pix():
    pixels = [["0 0 0 " for y in range(max_height)] for x in range(max_width)]

def add_line(x1,y1,z1,x2,y2,z2):
    length = len(point_mat)
    points = [[x1,y1,z1,1],[x2,y2,z2,1]]
    for x in range(2):
        edge_mat.append(points[x])

def make_iden(mat):
    for x in range(4):
        for y in range(4):
            if x == y:
                mat[x][y] = 1

def transform(x1,y1,z1):
    new_mat = [ [ 0 for x in range(4) ] for y in range(4) ]
    new_mat = make_iden(new_mat)
    values = [x1,y1,z1,1]
    for x in range(4):
        new_mat[x][4] = values[x]
    mult(new_mat)

def scale(x1,y1,z1):
    new_mat = [ [ 0 for x in range(4) ] for y in range(4) ]
    new_mat = make_iden(new_mat)
    values = [x1,y1,z1,1]
    for x in range(4):
        new_mat[x][x] =values[x]
    mult(new_mat)

def rotate_x(rx):
    new_mat = [ [ 0 for x in range(4) ] for y in range(4) ]
    new_mat = make_iden(new_mat)
    new_mat[1][1] = math.cos(math.radians(rx))
    new_mat[1][2] = 0 - math.sin(math.radians(rx))
    new_mat[2][1] = math.sin(math.radians(rx))
    new_mat[2][2] = math.cos(math.radians(rx))
    mult(new_mat)

def rotate_y(ry):
    new_mat = [ [ 0 for x in range(4) ] for y in range(4) ]
    new_mat = make_iden(new_mat)
    new_mat[0][0] = math.cos(math.radians(ry))
    new_mat[0][2] = math.sin(math.radians(ry))
    new_mat[2][0] = 0 - math.sin(math.radians(ry))
    new_mat[2][2] = math.cos(math.radians(ry))
    mult(new_mat)

def rotate_z(rz):
    new_mat = [ [ 0 for x in range(4) ] for y in range(4) ]
    new_mat = make_iden(new_mat)
    new_mat[0][0] = math.cos(math.radians(rz))
    new_mat[0][1] = 0 - math.sin(math.radians(rz))
    new_mat[1][0] = math.sin(math.radians(rz))
    new_mat[1][1] = math.cos(math.radians(rz))
    mult(new_mat)

def mult(mat,mat2):
    new_mat = [ [ 0 for x in range(4) ] for y in range(len(mat2[0])) ]
    for row in range(4):
        for col in range(len(mat2[0])):
            new_mat[row][col] = (mat[row][0]*mat2[0][col] + 
                                 mat[row][1]*mat2[1][col] + 
                                 mat[row][2]*mat2[2][col] + 
                                 mat[row][3]*mat2[3][col])
