import random

WIDTH = 16
HEIGHT = 16
N = 10

# # - SOLID
# H - HAZARD
# P - START
# E - END

f = open("levels_10.txt", "w")

for a in range(N):

    level = [[' '] * HEIGHT for _ in range(WIDTH)]

    row=0
    col=0
    # Add platforms
    while row < HEIGHT:
        if random.random() > 0.9:
            row += 1
            continue
        print("row")
        col = 0
        while col < WIDTH:
            if random.random() < 0.2:
                p = random.randint(2,4)
                print("plt, " + str((row,col,p)))
                for i in range(p):
                    try:
                        level[row][col+i] = '#'
                    except:
                        break
                col += p+1
            else:
                col += 1
        row += 2

    # Add hazards and border
    for row in range(HEIGHT):
        for col in range(WIDTH):
            if row == 0 or row == (HEIGHT-1):
                level[row][col] = '#'
                continue
            if col == 0 or col == (WIDTH-1):
                level[row][col] = '#'
                continue
            if random.random() < 1/40:
                level[row][col] = 'H'

    # S & E
    level[1][WIDTH-2] = 'E'
    level[HEIGHT-2][1] = 'S'

    for row in range(HEIGHT):
        r = ""
        for col in range(WIDTH):
            r += level[row][col]
        r+='\n'
        f.write(r)

f.close()