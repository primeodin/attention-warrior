#!/usr/bin/env python3
import math
def softmax(xs):
    m=max(xs); ex=[math.exp(x-m) for x in xs]; s=sum(ex); return [x/s for x in ex]
query=[1,0,1]; keys=[[1,0,0],[0,1,0],[1,0,1]]; values=["strike","wait","teach"]
scores=[sum(a*b for a,b in zip(query,k))/math.sqrt(3) for k in keys]
for v,w in zip(values,softmax(scores)): print(v, round(w,3))
print("attention is rage with a lantern")
