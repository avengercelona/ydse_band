import numpy as np
import math as m
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
import time as t

fig,ax=plt.subplots()

st=t.time()
lmb=[700*(10**-9),550*(10**-9),475*(10**-9)]
i=0.2 #intenisity in watt/m2
s=0.00002 #slit sepr in metres
d=50 #screen distance in metres
y_lim=100
spc=0.075#y intervals
bh=0.2#height of spectral band width
y=np.arange(-y_lim,y_lim,spc)
ints_r,ints_g,ints_b=[],[],[]
print(t.time()-st)
st=t.time()

for x in y:
    d1=m.sqrt(d**2 + (x-s/2)**2)
    d2=m.sqrt(d**2 + (x+s/2)**2)
    pathdif=abs(d1-d2)

    phi_r=2*(np.pi)*pathdif/lmb[0]
    ints_r.append(4*i*(np.cos(phi_r/2)**2))

    phi_g=2*(np.pi)*pathdif/lmb[1]
    ints_g.append(4*i*(np.cos(phi_g/2)**2))

    phi_b=2*(np.pi)*pathdif/lmb[2]
    ints_b.append(4*i*(np.cos(phi_b/2)**2))

    ax.add_patch(Rectangle((x,-bh),spc*0.9,bh*0.9,
    color=(ints_r[-1]/0.8,ints_g[-1]/0.8,ints_b[-1]/0.8)))
print(t.time()-st)
st=t.time()
ax.plot(y,ints_r,c=(0.8,0,0))
ax.plot(y,ints_g,c=(0,0.8,0))
ax.plot(y,ints_b,c=(0,0,0.8))
plt.show()
