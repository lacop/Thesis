class Node:
    up, left, right, height = None, None, None, None
    order = None
    def __init__(self, left, right):
        if left is None:
            self.height = 1
        else:
            self.left = left
            self.right = right
            left.up = self
            right.up = self
            self.height = left.height + 1

def get_root(height):
    nodes = [Node(None, None) for _ in range(2**(height-1))]
    while len(nodes) > 1:
        newnodes = []
        for i in range(len(nodes)//2):
            newnodes.append(Node(nodes[2*i], nodes[2*i+1]))
        nodes = newnodes

    return nodes[0]

def order_naive(v, i=1):
    if v is not None:
        v.order = i
        order_naive(v.left, 2*i)
        order_naive(v.right, 2*i+1)

def order_veb(v, height, i = 1):
    if height <= 2:
        v.order = i
        i+=1
        if height == 2 and v.left is not None:
            v.left.order = i
            i += 1
            v.right.order = i
            i += 1
        return i
    else:
        bottom = 1
        while bottom*2 < height:
            bottom *= 2
        top = height - bottom
        i = order_veb(v, top, i)

        q = [v]
        while len(q) > 0:
            x = q.pop(0)
            if x.height == v.height - top:
                i = order_veb(x, bottom, i)
            else:
                if x.left is not None:
                    q.append(x.left)
                    q.append(x.right)
        return i

# def get_tikz(v, tab='  '):
#     out = 'node [circle,draw] {' + str(v.order) + '}'
#     if v.left is not None:
#         out += '\n' + tab + 'child { ' + get_tikz(v.left, tab+'  ') + ' }'
#         out += '\n' + tab + 'child { ' + get_tikz(v.right, tab+'  ') + ' }'
#     return out
#
# def full_tikz(root):
#     return '\\' + get_tikz(root) + ';'

def get_tikz(v, tab='  ', name='T'):
    out = '[.\\node (' + name + ') {' + str(v.order) + '}; '
    if v.left is not None:
        out += '\n' + tab + get_tikz(v.left, tab+'  ', name+'L')
        out += '\n' + tab + get_tikz(v.right, tab+'  ', name+'R')
    out += ']'
    return out

def full_tikz(root):
    return '\\Tree ' + get_tikz(root)


def generate(type, height):
    root = get_root(height)
    if type == 'naive':
        order_naive(root)
    elif type == 'veb':
        order_veb(root, height)
    else:
        return "Unknown"

    print(full_tikz(root))

from itertools import product

def vebbox(name, height, sep, sepstep):
    if height < 2:
        print('\\node[draw, rectangle, fit = ({0}), inner sep = {1}] {{}};'.format(name, sep))
    elif height == 2:
        print('\\node[draw, rectangle, fit = ({0})({0}L)({0}R), inner sep = {1}] {{}};'.format(name, sep))
    else:
        print('\\node[draw, rectangle, thick, fit = ({0})({0}{1})({0}{2}), inner sep = {3}] {{}};'.format(name, 'L'*(height-1), 'R'*(height-1), sep))

        bottom = 1
        while bottom*2 < height:
            bottom *= 2
        top = height - bottom
        vebbox(name, top, sep - sepstep, sepstep)

        for p in product('LR', repeat=top):
            vebbox(name + ''.join(p), bottom, sep - sepstep, sepstep)

def numtoname(i):
    name = ''
    while i > 1:
        if i % 2 == 0:
            name += 'L'
        else:
            name += 'R'
        i //=2
    name += 'T'
    return name[::-1]

def naivearrows(height, shorten='3pt', control='(5, -1)'):
    wrap = 1
    for i in range(1, 2**height-1):
        out = '\\draw [->, shorten >= {0}, shorten <= {0}] '.format(shorten)
        this = numtoname(i)
        next = numtoname(i+1)

        if i == wrap:
            wrap = 2*wrap + 1
            out += '({0}.east) .. controls ($({0}) + {2}$) and ($({1}) - {2}$) .. ({1}.west);'.format(this, next, control)
        else:
            out += '({0}) to ({1});'.format(this, next)

        print(out)
