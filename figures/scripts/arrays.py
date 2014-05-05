import node_order

height = 5
find = 15
blocksize = 4

nodesize = 0.5
colormiss = 'red!60!white'
coloraccess = 'yellow'
colorcache = 'green!40!white'
colornone = 'white'

offstep = 0.25

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

array = list(range(2**height + 1))[1:-1]

def binsearch(arr, key):
    loaded = []
    accessed = []
    miss = []

    left = 0
    right = len(arr)
    while True:
        mid = (left+right) // 2
        accessed.append(mid+1)
        if mid+1 not in loaded:
            miss.append(mid+1)
            for i in range(blocksize):
                loaded.append(mid + 1 + i)

        #print(mid, left, right)
        if left == right:
            break

        if arr[mid] == key:
            break
        elif arr[mid] < key:
            left = mid
        else:
            right = mid

    return (accessed, loaded, miss)

def drawnode(order, key, info, y):
    accessed, loaded, miss = info

    out = '\\draw [fill = '
    if order in miss:
        out += colormiss
    elif order in accessed:
        out += coloraccess
    elif order in loaded:
        out += colorcache
    else:
        out += colornone
    out += '] '

    x = nodesize*order
    out += '({}, {}) rectangle ({}, {}) '.format(x, y, x+nodesize, y+nodesize)


    out += 'node [midway] {' + str(key) + '};'

    print(out)

def drawtree(v, y, info):
    if v is None:
        return

    drawnode(v.order, v.key, info, y)

    drawtree(v.left, y, info)
    drawtree(v.right, y, info)

def drawarray(arr, y, info):
    for i in range(len(arr)):
        drawnode(i+1, arr[i], info, y)

def printarrows(accessed, y):
    for i in range(len(accessed)-1):
        sx = accessed[i]*nodesize + nodesize*0.75
        ex = accessed[i+1]*nodesize + nodesize*0.25

        off = (len(accessed)-i-1) * offstep

        out = '\\draw [>->] '
        out += '({}, {}) '.format(sx, y+nodesize)
        out += ' -- ({}, {}) -- '.format(sx, y+nodesize+off)
        if (abs(sx-ex) > nodesize):
            out += 'node [midway, fill = white] {' + str(i+1) + '} '
        else:
            out += 'node [midway, above] {' + str(i+1) + '} '
        out += '({}, {}) --'.format(ex, y+nodesize+off)
        out += '({}, {});'.format(ex, y+nodesize)
        print(out)

def printblocks(blocks, y):
    for i,b in enumerate(blocks):
        sx = b*nodesize
        ex = (b+blocksize)*nodesize

        out = '\\draw [|-|, shorten <=1pt, shorten >= 1pt] '
        out += '({}, {}) -- ({}, {}) '.format(sx, y-offstep, ex, y-offstep)
        out += 'node [midway, fill = white] {' + str(i+1) + '};'
        print(out)

def printtree(tree, y=0):
    info = treesearch(tree, find)

    drawtree(tree, y, info)

    accessed, _, blocks = info
    printarrows(accessed, y)
    printblocks(blocks, y)

def printarray(arr, y=0):
    info = binsearch(arr, find)

    drawarray(arr, y, info)

    accessed, _, blocks = info
    printarrows(accessed, y)
    printblocks(blocks, y)

def printall():
    print('% height={}, finding={}, blocksize={}'.format(height, find, blocksize))
    print()

    print('% Binary search')
    printarray(array, 0)
    print()

    print('% BFS tree')
    printtree(bfs, -3)
    print()

    print('% vEB tree')
    printtree(veb, -6)
    print()