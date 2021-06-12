'''
Compute the path based on stream vectors
'''
from . Derivative import *


class PathData:

    def __init__(self, pathObj):
        self.visited = np.zeros(pathObj.shape)

    '''
    Compute a parameterization that follows the stream vectors
    from a give starting point.
    '''

    def Path(self, dX, dY, x0, y0, pathSet=set()):

        done = False
        x = x0
        y = y0

        lastX = x
        lastY = y

        path = []
        oldLen = len(path)
        while done == False:

            # We need a unique value so we can test if the path overlaps.
            pathSet.add(str(x)+','+str(y))

            # If the path intersects itself we need to stop
            if oldLen == len(pathSet):
                path.append([x, y])
                self.visited[y, x] = 1
                done = True
                break

            # otherwise add the new element
            self.visited[y, x] = 1
            path.append([x, y])

            oldLen = len(pathSet)

            # compute the next cell in the path
            tx, ty = self.nextBest(dX, dY, x, y, lastX, lastY)

            lastX = x
            lastY = y

            x = tx
            y = ty

        return path

    '''
    Find the next best cell in the path
    '''

    def nextBest(self, dX, dY, x, y, lastX, lastY):

        shape = dX.shape

        dx = dX[y, x]
        dy = dY[y, x]

        d = np.sqrt(dX*dX+dY*dY)

        # these are the non corner values
        tx = x
        ty = y

        # this will be the diagonal values
        ox = x
        oy = y

        if dx == 0 and dy == 0:

            # Construct an array with all the neighbors and make a choice based on which has the largest gradient magnitude.
            a = []
            if y+1 < shape[0]:
                a.append({'d': d[y+1, x], 'p': [x, y+1]})
            if y-1 >= 0:
                a.append({'d': d[y-1, x], 'p': [x, y-1]})
            if x+1 < shape[1]:
                a.append({'d': d[y, x+1], 'p': [y, x+1]})
            if x-1 >= 0:
                a.append({'d': d[y, x-1], 'p': [y, x-1]})

            a.sort(key=lambda val: val['d'], reverse=True)

            # Try something else we didn't try
            result = a[0]

            if a[0]['p'] == [lastX, lastY]:
                result = a[1]

            ox = result['p'][0]
            oy = result['p'][1]
            tx = ox
            ty = oy

        elif dx >= 0 and dy >= 0:
            ox = x+1
            oy = y+1
            if abs(dx) > abs(dy):
                tx = x + 1
            else:
                ty = y + 1

            #print('in 1')
        elif dx >= 0 and dy <= 0:
            ox = x+1
            oy = y-1
            if abs(dx) > abs(dy):
                tx = x + 1
            else:
                ty = y - 1

            #print('in 2',dx,dy)
        elif dx <= 0 and dy >= 0:
            ox = x-1
            oy = y+1
            if abs(dx) > abs(dy):
                tx = x - 1
            else:
                ty = y + 1

            #print('in 3',dx,dy,d[oy,ox],d[tx,tx])
        elif dx <= 0 and dy <= 0:
            ox = x-1
            oy = y-1
            if abs(dx) > abs(dy):
                tx = x - 1
            else:
                ty = y - 1
            #print('in 4')

        shape = dX.shape
        if ox >= shape[1] or ox < 0:
            return x, y
        if oy >= shape[0] or oy < 0:
            return x, y

        fx = tx
        fy = ty
        if d[oy, ox] > d[ty, tx]:
            fx = ox
            fy = oy
        # print('fx,fy',fx,fy)
        return fx, fy

    '''
    Compute the absolute gradient for every cell and store
    in the list with the largest gradient first.  This is used
    to compute the starting point for computing stream vectors.
    '''

    def sortAbs(self, image):

        d = gradient_magnitude_tvd(image)
        shape = d.shape
        print('gradient mag.shape', shape)
        a = []
        for i in range(0, shape[0]):
            for j in range(0, shape[1]):
                a.append({'pos': [j, i], 'd': abs(d[i, j])})

        a.sort(key=lambda x: x['d'], reverse=True)

        return a

    def constructPathList(self, X0, maxPaths=1):

        # TODO These probably shouldn't be in here since we are duplicating work.
        dX, dY = stream_vectors_central(X0)
        d = gradient_magnitude_central(X0)

        # Compute the location of the maximum gradients
        #pathData = PathData(d)
        gradList = self.sortAbs(X0)

        pathList = []
        count = 0
        index = 0
        while count < maxPaths:
            # using the first element in the dictionary follow the streamvectors
            pos = gradList[index]['pos']
            index = index+1

            # Try and parametrize the image starting at the given position.
            # Yes, the reversal of x and y is correct. I need to fix this, but the display actually has y as the first variable and x as second!
            if self.visited[pos[1], pos[0]] == 1:
                continue

            path = self.Path(dX, dY, pos[0], pos[1])

            path = np.array(path)
            pathList.append(path)
            count = count+1
            print('count', count)

        return pathList
