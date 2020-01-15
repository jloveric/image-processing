'''
Compute the path based on stream vectors
'''
from Derivative import *

def Path(dX, dY, x0, y0) :

    done==False
    x = x0
    y = y0

    pathSet = {}
    path = []
    oldLen = len(path)
    while done==False:

        #We need a unique value so we can test if the path overlaps.
        pathSet.add(str(x)+','+str(y))

        #If the path intersects itself we need to stop 
        if oldLen == len(path) :
            done = True
            break

        #otherwise add the new element
        path.append([x,y])

        oldLen = len(path)

        #compute the next cell in the path
        x, y = nextBest(dX, dY, x, y)
    
    return path


def nextBest(dX, dY, x, y) :
    
    dx = dX[x,y]
    dy = dY[x,y]

    if dx >0 and dy>0 :
        if(abs(dx)>abs(dy)) :
            x = x + 1
        else :
            y = y + 1 
    elif dx>0 and dy<0 :
        if(abs(dx)>abs(dy)) :
            x = x + 1
        else :
            y = y - 1
    elif dx<0 and dy>0 :
        if(abs(dx)>abs(dy)) :
            x = x - 1
        else
            y = y + 1
    elif dx<0 and dy<0 :
        if(abs(dx)>abs(dy)) :
            x = x - 1
        else
            y = y - 1

    return x, y

'''
Compute the absolute gradient for every cell and store
in the list with the largest gradient first.
'''
def sortAbs(image) :

    d = gradientMagnitude(image)
    shape = d.shape

    a = []
    for i in range(0, shape[0]) :
        for j in range(0, shape[0]) :
            a.append({pos : [i,j], d : abs(d[i,j])})

    a.sort(key = lambda x : x.d, reverse=True )
    
    return a