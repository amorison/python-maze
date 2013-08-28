import pygame as pg
from pygame.locals import *
import random
import time
from sys import argv

WIDTH , HEIGHT = 20 , 20
CRD=(0,0,150)
WAL=(0,175,0)

def calcMaze(w,h):
    visitedCells=[[False for i in range(h)] for j in range(w)] #bool True if x,y already visited
    unvisitedCells=w*h
    currentCell=(0,0)
    walls=[[[True,True,True,True] for i in range(h)] for j in range(w)] #U D L R
    bridge=[[0 for i in range(h)] for j in range(w)] #1:vertical bridge   2:horizontal bridge
    stackCells=[]
    otherD=[1,0,3,2]
    while unvisitedCells:
        x,y=currentCell
        if not visitedCells[x][y]:
            unvisitedCells-=1
        nb = []
        if x!=0:
            if not visitedCells[x-1][y]:nb.append((0,x-1,y,2)) #type (0:cell is next  1:need bridge) , xN, yN, direction
            elif x!=1 and not visitedCells[x-2][y] and walls[x-1][y]==[False,False,True,True]:nb.append((1,x-2,y,2))
        if x!=w-1:
            if not visitedCells[x+1][y]:nb.append((0,x+1,y,3))
            elif x!=w-2 and not visitedCells[x+2][y] and walls[x+1][y]==[False,False,True,True]:nb.append((1,x+2,y,3))
        if y!=0 and (x,y)!=(w-1,h-1):
            if not visitedCells[x][y-1]:nb.append((0,x,y-1,0))
            elif y!=1 and not visitedCells[x][y-2] and walls[x][y-1]==[True,True,False,False]:nb.append((1,x,y-2,0))
        if y!=h-1 and (x,y)!=(w-1,h-2):
            if not visitedCells[x][y+1]:nb.append((0,x,y+1,1))
            elif y!=h-2 and not visitedCells[x][y+2] and walls[x][y+1]==[True,True,False,False]:nb.append((1,x,y+2,1))
        visitedCells[x][y]=True
        if nb:
            t,a,b,d = random.choice(nb)
            stackCells.append(currentCell)
            walls[x][y][d]=False
            if d<2:y+=1 if d==1 else -1
            else: x+=1 if d==3 else -1
            if t : bridge[x][y]=1 if d<2 else 2 # vert or horiz bridge
            d=otherD[d]
            walls[a][b][d]=False
            currentCell=(a,b)
        else:
            currentCell=stackCells.pop(0)
    return walls,bridge

def drawMaze():
    for x in range(WIDTH):
        for y in range(HEIGHT):
            drawWalls(walls,x,y)
            drawBridge(bridge,x,y)
    pg.display.flip()

def drawWalls(wa,x,y):
    pg.draw.rect(surf,CRD,[x*10+3,y*10+3,4,4])
    pg.draw.rect(surf,WAL,[x*10+2,y*10+2,6,6],1)
    if not wa[x][y][0]:
        pg.draw.rect(surf,CRD, [x*10+3,y*10,4,3])
        pg.draw.line(surf,WAL,[x*10+2,y*10],[x*10+2,y*10+2])
        pg.draw.line(surf,WAL,[x*10+7,y*10],[x*10+7,y*10+2])
    if not wa[x][y][1]:
        pg.draw.rect(surf,CRD, [x*10+3,y*10+7,4,3])
        pg.draw.line(surf,WAL,[x*10+2,y*10+7],[x*10+2,y*10+9])
        pg.draw.line(surf,WAL,[x*10+7,y*10+7],[x*10+7,y*10+9])
    if not wa[x][y][2]:
        pg.draw.rect(surf,CRD, [x*10,y*10+3,3,4])
        pg.draw.line(surf,WAL,[x*10,y*10+2],[x*10+2,y*10+2])
        pg.draw.line(surf,WAL,[x*10,y*10+7],[x*10+2,y*10+7])
    if not wa[x][y][3]:
        pg.draw.rect(surf,CRD, [x*10+7,y*10+3,3,4])
        pg.draw.line(surf,WAL,[x*10+7,y*10+2],[x*10+9,y*10+2])
        pg.draw.line(surf,WAL,[x*10+7,y*10+7],[x*10+9,y*10+7])

def drawBridge(br,x,y):
    if br[x][y]==1:
        pg.draw.rect(surf,CRD,[x*10+3,y*10,4,10])
        pg.draw.line(surf,WAL,[x*10+2,y*10],[x*10+2,y*10+9])
        pg.draw.line(surf,WAL,[x*10+7,y*10],[x*10+7,y*10+9])
    if br[x][y]==2:
        pg.draw.rect(surf,CRD,[x*10,y*10+3,10,4])
        pg.draw.line(surf,WAL,[x*10,y*10+2],[x*10+9,y*10+2])
        pg.draw.line(surf,WAL,[x*10,y*10+7],[x*10+9,y*10+7])

def moves(k):
    li=[K_UP,K_DOWN,K_LEFT,K_RIGHT]
    if not k in li:
        return xP,yP,sP
    d=li.index(k)
    xN,yN,sN=xP,yP,sP
    if (sP==0 and not walls[xP][yP][d]) or (sP==1 and d<2 and bridge[xP][yP]==1) or (sP==1 and d>1 and bridge[xP][yP]==2):
        if d<2:yN+=1 if d==1 else -1
        else:xN+=1 if d==3 else -1
        if d<2 and bridge[xN][yN]==1:sN=1
        elif d>1 and bridge[xN][yN]==2:sN=1
        else:sN=0
    drawWalls(walls,xP,yP)
    drawBridge(bridge,xP,yP)
    drawPlayer(xN,yN,sN)
    return xN,yN,sN

def drawPlayer(x,y,s):
    drawWalls(walls,x,y)
    if not s:pg.draw.rect(surf,(255,55,55),[x*10+3,y*10+3,4,4])
    drawBridge(bridge,x,y)
    if s:pg.draw.rect(surf,(255,55,55),[x*10+3,y*10+3,4,4])
    pg.display.flip()


pg.init()
try:
    if len(argv)>=3:HEIGHT=int(argv[2])
    if HEIGHT<=0:raise ValueError
except ValueError:
    HEIGHT=20
try:
    if len(argv)>=2:WIDTH=int(argv[1])
    if WIDTH<=0:raise ValueError
except ValueError:
    WIDTH=20
surf = pg.display.set_mode((10*WIDTH,10*HEIGHT))
pg.display.set_caption("Maze")
pg.key.set_repeat(80,20)
walls,bridge = calcMaze(WIDTH,HEIGHT)
xP,yP=(0,0)#player position
sP=0 #1 if player on bridge
drawPlayer(xP,yP,sP)
ok=True
while ok:
    time.sleep(0.01)
    for evt in pg.event.get():
        if evt.type == QUIT:
            ok = False
        elif evt.type == KEYDOWN:
            k=evt.key
            if k==K_d:
                drawMaze()
                drawPlayer(xP,yP,sP)
            xP,yP,sP=moves(k)
            if (xP,yP)==(WIDTH-1,HEIGHT-1):
                walls,bridge=calcMaze(WIDTH,HEIGHT)
                surf.fill((0,0,0))
                xP,yP,sP=0,0,0
                drawPlayer(xP,yP,sP)
