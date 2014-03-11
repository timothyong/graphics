first =  open("first.ppm", "w")

first.write("P3 500 500 255 ")
i = 0
j = 0

while i < 500:
    j = 0
    while j < 500:
        a = "%i %i %i "
        b = a%((i+j)%256, (i % 255, 255 - i %256)
        print b
        first.write(b)
        j = j + 1
    i = i + 1
