import random
import re

def maxi(l):
    res=0
    for i in l:
        if i>res:
            res=i
    return res

def tri(l):
    m=maxi(l)
    res=[]
    dico={i:0 for i in range(m+1)}
    for i in l:
        dico[i]+=1
        
    # res=[i for i in range(m+1) if dico[i]!=0]
    
    for i in range(m+1):
        if dico[i]!=0:
            for k in range(dico[i]):
                res.append(i)
    
    return res

def genere_liste(n):
    res=[]
    for _ in range(n):
        res.append(random.randint(0,100))
    return res
    

# print(tri(genere_liste(100)))

import time
l=genere_liste(5000000)

td=time.time()
tri(l)
print('Mon temps',time.time()-td)

td=time.time()
sorted(l)
print('Son temps',time.time()-td)




