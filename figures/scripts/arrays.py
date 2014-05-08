import node_order

# height = 8
# find = 201
# height = 7
# find = 55

height = 9
find = 243
#find = 427
blocksize = 4

nodewidth = 0.25
nodeheight = 0.25

coloredge = 'gray'
colormiss = 'red!60!white'
coloraccess = 'green'
colorcache = 'yellow!40!white'
colornone = 'white'

poslabel = 'node (LAST) [midway, draw, circle, inner sep = 0, minimum size=2, fill=black] {}'

offstep = 0.125

sep = nodeheight*2+offstep*height

bfs = node_order.get_root(height)
node_order.order_naive(bfs)
veb = node_order.get_root(height)
node_order.order_veb(veb, height)

def setkey(v, q, off):
    if v is not None:
        v.key = off + q//2
        if q > 1:
            setkey(v.left, q//2, off)
            setkey(v.right, q//2, off + q//2)

setkey(bfs, 2**height, 0)
setkey(veb, 2**height, 0)

def treesearch(v, key):
    loaded = []
    accessed = []
    miss = []

    while v is not None:
        accessed.append(v.order)
        if v.order not in loaded:
            miss.append(v.order)
            for i in range(blocksize):
                loaded.append(v.order + i)
        if v.key == key:
            break
        if v.key < key:
            v = v.right
        else:
            v = v.left
    return (accessed, loaded, miss)

array = range(1, 2**height)

def binsearch(arr, key):
    loaded = []
    accessed = []
    miss = []

    left = 0
    right = len(arr)
    while True:
        mid = (left+right) // 2
        accessed.append(mid)
        if mid not in loaded:
            miss.append(mid)
            for i in range(blocksize):
                loaded.append(mid + i)

        #print(mid, left, right)
        if left == right:
            break

        if arr[mid] == key:
            break
        elif arr[mid] < key:
            left = mid
        else:
            right = mid
    #print(accessed, loaded, miss)
    return (accessed, loaded, miss)

def drawnode(order, key, info, y, meh=False):
    accessed, loaded, miss = info

    if order in miss:
        col = colormiss
    elif order in accessed:
        col = coloraccess
    elif order in loaded:
        col = colorcache
    else:
        col = colornone
    if meh: order = order - 1
    x = nodewidth*(order // blocksize)
    y = y + nodeheight*(order % blocksize)
    out = r'\draw [color={}, fill = {}] ({}, {}) rectangle ({}, {})'.format(coloredge, col, x, y, x+nodewidth, y+nodeheight)
    #out += 'node [midway] {' + str(key) + '};'

    if key == find:
        out += poslabel
    elif order in accessed:
        out += 'node [midway] (A{}) {{}}'.format(accessed.index(order))

    print(out + ';')

def drawtree(v, y, info):
    if v is None:
        return

    drawnode(v.order, v.key, info, y, True)
    drawtree(v.left, y, info)
    drawtree(v.right, y, info)

def drawarray(arr, y, info):
    for i in range(len(arr)):
        drawnode(i, arr[i], info, y)

def printarrows(accessed, y):
    for i in range(len(accessed)-1):
        sx = nodewidth*(accessed[i] // blocksize) + nodewidth*0.5
        sy = y + nodeheight*(accessed[i] % blocksize) + nodeheight*0.5
        ex = nodewidth*(accessed[i+1] // blocksize) + nodewidth*0.5
        ey = y + nodeheight*(accessed[i+1] % blocksize) + nodeheight*0.5

        off = (len(accessed)-i-1) * offstep

        #out = '\\draw [>->] '
        #out += '({}, {}) '.format(sx, y+nodeheight)
        #out += ' -- ({}, {}) -- '.format(sx, y+nodeheight+off)
        # if (abs(sx-ex) > nodesize):
        #     out += 'node [midway, fill = white] {' + str(i+1) + '} '
        # else:
        #     out += 'node [midway, above] {' + str(i+1) + '} '
        #out += '({}, {}) --'.format(ex, y+nodeheight+off)
        #out += '({}, {});'.format(ex, y+nodeheight)
        #out = r'\draw ({0}, {1}) .. controls ({0}, {2}) and ({3}, {2}) ..     ({3}, {1});'.format(sx, y+nodeheight, y+nodeheight+off, ex)
        out = r'\draw [->] ({0}, {1}) to ({2}, {3});'.format(sx, sy, ex, ey)
        print(out)

def printblocks(blocks, y):
    for i,b in enumerate(blocks):
        sx = b*nodewidth
        ex = (b+blocksize)*nodewidth

        out = r'\draw [|-|, shorten <=1pt, shorten >= 1pt] ({}, {}) -- ({}, {});'.format(sx, y-offstep, ex, y-offstep)
        print(out)

def printtree(tree, y=0):
    info = treesearch(tree, find)

    drawtree(tree, y, info)

    accessed, _, blocks = info
    #printarrows(accessed, y)
    #printblocks(blocks, y)

def printarray(arr, y=0):
    info = binsearch(arr, find)
    drawarray(arr, y, info)
    accessed, _, blocks = info
    #printarrows(accessed, y)
    #printblocks(blocks, y)

def printall():
    print('% height={}, finding={}, blocksize={}'.format(height, find, blocksize))
    print()

    print('% Binary search')
    printarray(array, 0)
    print()

    print('% BFS tree')
    printtree(bfs, -1*sep)
    print()

    print('% vEB tree')
    printtree(veb, -2*sep)
    print()

print(r"""
\documentclass[tikz, border=10pt]{standalone}
\begin{document}
\begin{tikzpicture}
""")
printall()
print(r"""
\end{tikzpicture}
\end{document}
""")