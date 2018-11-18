def printB(blocks):
    for i in range(len(blocks)):
        for j in range(len(blocks[0])):
            print blocks[i][j],
        print ""

def printGG(gg):
    for j in range(len(gg.is_path[0])):
        for i in range(len(gg.is_path)):
            if gg.is_path[i][j]:
                print "O",
            elif gg.is_used_wall[i][j]:
                print "U",
            else:
                print "X",
        print ""
