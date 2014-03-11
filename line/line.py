import math
import sys

color = "0 0 0 "
pic = [[color for y in range(500)] for x in range(500)]

def readfile():
    f = open(sys.argv[1], "r")
    lines = f.readlines()
    f.seek(0)
    i = 0
    while i < len(lines):
        line = f.readline().replace("\n","")
        if line[0:1] == "c":
            color = f.readline().replace("\n"," ")
        elif line[0:1] == "l":
            coordinates = f.readline().replace("/n", "")
            listcoor = coordinates.split()
            print listcoor
            drawLine(color, int(listcoor[0]), int(listcoor[1]), int(listcoor[2]), int(listcoor[3]))
        elif line[0:1] == "g":
            fileoutput = f.readline().replace("\n", "")
            output = open(fileoutput, "w")
            output.write("P3 500 500 255 ")
            for x in pic:
                for y in x:
                    output.write(y)
            output.close()
        elif line[0:1] == "q":
            f.close()
            break

def drawLine(color, x1, y1, x2, y2):
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
            pic[y][x] =color
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
readfile()

