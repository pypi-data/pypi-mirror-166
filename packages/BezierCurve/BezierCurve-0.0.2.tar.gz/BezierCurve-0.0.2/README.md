# Bezier Curve 

This is a simple Bezier Curve package for robot trajectory generation.
For more information please visit [https://github.com/tjdalsckd/BezierCurve](https://github.com/tjdalsckd/BezierCurve)

## Example Code
```bash
import matplotlib.pyplot as plt
import numpy as np
from math import *
from BezierCurve import *
# 3-points example x=[0, 1, 2] y=[0 ,1,0]
Points=np.array([[0,0],[1,1],[2,0]])
weights= [1,1.5,1]
# number of points
number = 1000;
# generate BezierCurve
bc = BezierCurve(Points,weights,number)
P,first_derivative_P,second_derivative_P= bc.get_bazier_curve()
ax1 = plt.subplot(1, 1, 1)
ax1.plot(Points[:,0],Points[:,1],'ro',Points[:,0],Points[:,1],'r:')
ax1.plot(P[:,0],P[:,1])
ax1.set_aspect('equal')
plt.show()
```
## Example Code 
```bash
ax1 = plt.subplot(1, 1, 1)
ax1.plot(Points[:,0],Points[:,1],'ro',Points[:,0],Points[:,1],'r:')
ax1.plot(P[:,0],P[:,1],'k-',alpha=.2)
point_number = 20
dt = 1/number*point_number*1.5;
arrowprops={"facecolor":"yellow",
            "edgecolor":"black",
            "headwidth":5,
            "headlength":5,
            "width":2,
            "linewidth":1,
            "alpha":0.8}
for j in range(0,number,int(number/point_number)):
    ax1.plot(P[j,0],P[j,1],'b.', markersize=5)
    ax1.annotate('',xy=(P[j,0]+first_derivative_P[j,0]*dt,P[j,1]+first_derivative_P[j,1]*dt)
                   ,xytext=(P[j,0],P[j,1])
                   ,arrowprops=arrowprops)
ax1.set_aspect('equal')
plt.show()
```
