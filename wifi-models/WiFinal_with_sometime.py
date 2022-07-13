from numpy import *
from numpy.linalg import solve
import matplotlib.pyplot as plt
import matplotlib.animation as animation


#______________Room Params, still need frequency
L=21

lamda = 6
Lsquared = L**2
KnotSquared = (2*pi/lamda)**2


#_________________Router position
Rx = int((L-1)/2)
Ry = Rx


#____index
Indexroom = zeros([L,L])#needs to be an array

#____the room
room = zeros([L,L])

#____Del, J
EquationMatrix = zeros([Lsquared, Lsquared])
JMatrix = zeros([Lsquared,1])

#______Initialize J

IndexMatrix = zeros([Lsquared,1])

for i in range(L):  
    for j in range(L):
        
        if 2<i<L-3 and 2<j<L-3:
            Indexroom[i,j] = 1
        
        else:
            Indexroom[i,j] = 1.6
            
        IndexMatrix[i*L + j] = (Indexroom[i,j])**2

#________Fill out Del Matrix
for j in range(Lsquared):
    for i in range(Lsquared):
        if i == j == 0:   
            EquationMatrix[i,j] = -2+KnotSquared*IndexMatrix[j]**2 
            EquationMatrix[i,j+1] = 1 
            EquationMatrix[i,j+L] = 1 
        
        if 0<i==j<L-1:
            EquationMatrix[i,j] = -3+KnotSquared*IndexMatrix[j]**2
            EquationMatrix[i,j+L] = 1
            EquationMatrix[i,j+1] = 1 
            EquationMatrix[i,j-1] = 1 
            
        if i==j== L-1:
            EquationMatrix[i,j] = -2+KnotSquared*IndexMatrix[j]**2 
            EquationMatrix[i,j+L] = 1 
            EquationMatrix[i,j-1] = 1 
          
        if L-1<i==j<Lsquared-L:
            EquationMatrix[i,j] = -4+KnotSquared*IndexMatrix[j]**2 
            EquationMatrix[i,j+L] = 1 
            EquationMatrix[i,j+1] = 1 
            EquationMatrix[i,j-1] = 1 
            EquationMatrix[i,j-L] = 1 
            
        if i == j == Lsquared-L:   
            EquationMatrix[i,j] = -2+KnotSquared*IndexMatrix[j]**2 
            EquationMatrix[i,j+1] = 1 
            EquationMatrix[i,j-L] = 1 
        
        if Lsquared-L<i==j<Lsquared-1:
            EquationMatrix[i,j] = -3+KnotSquared*IndexMatrix[j]**2 
            EquationMatrix[i,j-L] = 1 
            EquationMatrix[i,j+1] = 1 
            EquationMatrix[i,j-1] = 1 
            
        if i==j==Lsquared-1:
            EquationMatrix[i,j] = -2+KnotSquared*IndexMatrix[j]**2 
            EquationMatrix[i,j-L] = 1 
            EquationMatrix[i,j-1] = 1 
          

#_____________Solve for E values

t=0

JMatrix[Rx*L+Ry]  = cos(t)
EfieldMatrix = solve(EquationMatrix,JMatrix)

#________Translate into Room    
for x in range(L):
    for y in range(L):
        room[x,y] = EfieldMatrix[x*L + y]
    
fig=plt.figure()            
im =plt.imshow(room,cmap=plt.get_cmap('jet'))

def updateroom(*args):
        global t
        JMatrix[Rx*L+Ry]  = cos(t)
        t += pi/16
        EfieldMatrix = solve(EquationMatrix,JMatrix)
        for x in range(L):
            for y in range(L):

                room[x,y] = EfieldMatrix[x*L + y]
                im.set_array(room)
            
        return im
        
ani = animation.FuncAnimation(fig, updateroom, interval=5)

plt.show()

