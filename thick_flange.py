## For more details on this algorithm, see page 668 of Twists, Tilings and
## Tesselations by Robert J Lang
import numpy as np
import matplotlib.pyplot as pl

#constants
m = 6 #number of gores
N = 50 #number of points in each line

def unit_circle(theta):
    return np.array([np.cos(theta),np.sin(theta)])

def rotate_point(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.
    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + np.cos(angle) * (px - ox) - np.sin(angle) * (py - oy)
    qy = oy + np.sin(angle) * (px - ox) + np.cos(angle) * (py - oy)
    return qx, qy

def rotate_line(origin, points_x, points_y, angle):
    rotated_points_x = []
    rotated_points_y = []
    for point in zip(points_x, points_y):
        px, py = rotate_point(origin, point, angle)
        rotated_points_x.append(px)
        rotated_points_y.append(py)
    return np.array(rotated_points_x), np.array(rotated_points_y)

def surface_profile():
    theta = np.linspace(0.3,np.pi,N)
    z = np.cos(theta)+1.
    x = 1.5*np.sin(theta)
    return np.flip(x), np.flip(z)

def purple_and_black_vase():
    """Exhibited at PCOC 2019"""
    #(z+1)^2 / 1 + (x)^2 / (3^2)  =  1
    NN = int(N/2)
    z = np.linspace(0,1.9,NN)
    x = np.sqrt((1-np.power(z-1,2))*4.)
    scaleX = .5
    scaleZ = .2
    zz = np.linspace(max(z),max(z)+scaleZ,NN)
    xx = np.linspace(x[NN-1],x[NN-1]+scaleX,NN)
    return np.concatenate((x,xx)), np.concatenate((z,zz))

def distance(p1,p2):
    return np.sqrt((p1[0]-p2[0])**2. +
                   (p1[1]-p2[1])**2.)

def plot(x_in,y_in,linetype):
    x = []
    y = []
    for i in range(N):
        x.append(x_in[i])
        y.append(y_in[i])
    pl.plot(x,y,linetype)

x, z = purple_and_black_vase()
r=[]
for i in range(N):
    if i == 0:
        r.append(0.0)
    else:
        r.append(r[i-1] + np.sqrt((x[i] - x[i-1])**2.0 + (z[i]-z[i-1])**2.0))

r = np.array(r)
w = x*np.tan(np.pi/m)

a = np.array([
    r[i]*unit_circle(0.0) for i in range(N)
])

b = np.array([
    a[i] + w[i]*unit_circle(np.pi/2) for i in range(N)
])

c = np.array([
    b[i] + 0.5*(r[i]*np.tan(np.pi/m)-w[i]) * unit_circle(np.pi/2.0) for i in range(N)
])

f = np.array([
    r[i]*unit_circle(2*np.pi/m) for i in range(N)
])

e = np.array([
    f[i] + w[i]*unit_circle(2*np.pi/m - np.pi/2) for i in range(N)
])

d = np.array([
    e[i] + 0.5*(r[i]*np.tan(np.pi/m)-w[i]) * unit_circle(2*np.pi/m - np.pi/2.0) for i in range(N)
])

for i in range(m):
    for line, colour in zip([b,c,d,e],["blue","red","red","blue"]):
        rotated_points_x, rotated_points_y = rotate_line((0,0), line[:,0], line[:,1], 2*np.pi/m*i)
        plot(rotated_points_x,rotated_points_y,colour)
pl.axis('equal')
maximum = max(a[:,0])
pl.xlim(-maximum,maximum)
pl.ylim(-maximum,maximum)
frame1 = pl.gca()
frame1.axes.get_xaxis().set_visible(False)
frame1.axes.get_yaxis().set_visible(False)
fig = pl.gcf()
fig.set_size_inches(8,8)
pl.savefig("crease_pattern_thick_flange.svg")
