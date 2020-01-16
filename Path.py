'''
Compute the path based on stream vectors
'''
from Derivative import *

def Path(dX, dY, x0, y0, pathSet=set()) :

    done=False
    x = x0
    y = y0

    lastX = x
    lastY = y

    #pathSet = set()
    path = []
    oldLen = len(path)
    while done==False:

        print('pathSet', pathSet)

        #We need a unique value so we can test if the path overlaps.
        pathSet.add(str(x)+','+str(y))

        #If the path intersects itself we need to stop 
        if oldLen == len(pathSet) :
            path.append([x,y])
            print('x,y',x,y)
            done = True
            break

        #otherwise add the new element
        path.append([x,y])

        oldLen = len(pathSet)

        #compute the next cell in the path
        tx, ty = nextBest(dX, dY, x, y, lastX, lastY)
        
        lastX=x 
        lastY=y
        
        x=tx 
        y=ty
    
    return path

def nextBest(dX, dY, x, y, lastX, lastY) :
    
    dx = dX[y,x]
    dy = dY[y,x]

    print('dxdy',dx,dy)

    d = np.sqrt(dX*dX+dY*dY)

    #these are the non corner values
    tx = x
    ty = y

    #this will be the diagonal values
    ox = x
    oy = y

    if dx==0 and dy==0 :
        a = [{'d' : d[y+1,x], 'p' : [x,y+1] }, {'d' : d[y-1,x],'p': [x,y-1]}, {'d': d[y,x+1],'p':[y,x+1]}, {'d':d[y,x-1],'p':[y,x-1]}] 
        a.sort(key = lambda val : val['d'], reverse=True )
        
        #Try something else we didn't try
        result = a[0]
        print('a[0]',a[0]['p'])
        if a[0]['p'][0]==lastX and a[0]['p'][1]==lastY :
            result = a[1]

        ox = result['p'][0]
        oy = result['p'][1]
        tx=ox
        ty=oy

    elif dx >=0 and dy>=0 :
        ox = x+1
        oy = y+1
        if abs(dx)>abs(dy) :
            tx = x + 1
        elif abs(dy)>abs(dx) :
            ty = y + 1
        else :
            tx = ox
            ty = oy
        print('in 1')
    elif dx>=0 and dy<=0 :
        ox = x+1
        oy = y-1
        if abs(dx)>abs(dy) :
            tx = x + 1
        else :
            ty = y - 1
        #else :
        #    tx=ox
        #    ty=oy

        print('in 2',dx,dy)
    elif dx<=0 and dy>=0 :
        ox = x-1
        oy = y+1
        if abs(dx)>abs(dy) :
            tx = x - 1
        elif abs(dy)>abs(dx):
            ty = y + 1
        else :
            tx=ox
            ty=oy

        print('in 3',dx,dy,d[oy,ox],d[tx,tx])
    elif dx<=0 and dy<=0 :
        ox = x-1
        oy = y-1
        if abs(dx)>abs(dy) :
            tx = x - 1
        else :
            ty = y - 1
        print('in 4')

    shape = dX.shape
    if ox>=shape[1] or ox<0 :
        return x, y
    if oy>=shape[0] or oy<0 :
        return x, y

    fx = tx
    fy = ty
    if d[oy,ox] > d[ty,tx] :
        fx = ox
        fy = oy
    print('fx,fy',fx,fy)
    return fx, fy

'''
Compute the absolute gradient for every cell and store
in the list with the largest gradient first.
'''
def sortAbs(image) :

    d = gradientMagnitudeCentral(image)
    shape = d.shape

    a = []
    for i in range(0, shape[0]) :
        for j in range(0, shape[0]) :
            a.append({'pos' : [j,i], 'd' : abs(d[i,j])})

    a.sort(key = lambda x : x['d'], reverse=True )
    
    return a