from numpy import *
from numpy.linalg import solve
import matplotlib.pyplot as plt

#______________Room Params, still need frequency
L= 101

lamda = 12.5
Lsquared = L**2
KnotSquared = (2*pi/lamda)**2


#_________________Router position
Rx = (L-1)/2
Ry = Rx


#____index
Indexroom = zeros([L,L])#needs to be an array

#____the room
room = zeros([L,L])

#____Del, J
EquationMatrix = zeros([Lsquared, Lsquared])
JMatrix = zeros([Lsquared,1])
IndexMatrix = zeros([Lsquared,1])

#______Initialize J
JMatrix[Rx*L+Ry]  = 1
IndexMatrix = zeros([Lsquared,1])

for i in range(L):  
    for j in range(L):
        
        if 10<i<20 and 10<j<L-11:
            Indexroom[i,j] = 3.2
        
        elif 1<i<L-2 and 1<j<L-2:
            Indexroom[i,j] = 1
        
        else:
            Indexroom[i,j] = 2
            
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
EfieldMatrix = solve(EquationMatrix,JMatrix)


#________Translate into Room
for x in range(L):
    for y in range(L):
        room[x,y] = EfieldMatrix[x*L + y]

plt.figure()            
plt.imshow(room,cmap=plt.get_cmap('jet'))
plt.contour(Indexroom,8)
plt.show()
