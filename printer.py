def print_b(blocks):
    for i in range(len(blocks)):
        for j in range(len(blocks[0])):
            print blocks[i][j],
        print ""

def print_gg(gg):
    for j in range(len(gg.is_path[0])):
        for i in range(len(gg.is_path)):
            if gg.is_path[i][j]:
                print "O",
            elif gg.is_used_wall[i][j]:
                print "U",
            else:
                print "X",
        print ""

def print_3d_list(list):
    width = len(list)
    height = len(list[0])
    for i in range(width):
        for j in range(height):
            if len(list[i][j]) > 0:
                print (i,j),
                print ": ",
                print list[i][j]
