import bpy
import math
import itertools
import json
def create_basis(x,y,z):
    bpy.ops.object.empty_add(type='SPHERE', radius=0.03, view_align=False, location=(x, y, z), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))

def remove_points():
    for i in ['EMPTY','MESH']:
        bpy.ops.object.select_by_type(type=i)
        bpy.ops.object.delete()

def add_tetrahedron():
    l=1
    n=l*math.sqrt(3/8)
    bpy.ops.mesh.primitive_solid_add(size=n)
    bpy.context.object.location = (l/2, (l*math.sqrt(3))/6, 1/(2*math.sqrt(6)))
    bpy.context.object.rotation_euler=(0,0,math.radians(90))

pointcache=None
try:
    pointcache = json.load(open('steinhaus-3d-tetrahedron.pointcache.json'))
except FileNotFoundError:
    pointcache={}
print(pointcache)

def save_pointcache():
    json.dump(pointcache, open('steinhaus-3d-tetrahedron.pointcache.json','w'))

points = []
def add_points(points):
    for i in itertools.permutations(points):
        a,b,c,d,l=i
        key=' '.join((a,b,c,d,l))
        if ' '.join((a,b,c,d,l)) in pointcache:
            x,y,z=pointcache[' '.join((a,b,c,d,l))]
        else:
            a=int(a)
            b=int(b)
            c=int(c)
            d=int(d)
            l=int(l)
            a/=l
            b/=l
            c/=l
            d/=l
            l=1
            x=((a**2)-(b**2)+(l**2))/((2*l))
            y=((a**2)+(b**2)-(2*(c**2))+(l**2))/(a*math.sqrt(3)*l)
            z=((a**2)+(b**2)+(c**2)+(l**2)-(3*(d**2)))/(2*math.sqrt(6)*l)
        if (x,y,z) in points and False:
            pointcache.update({key:None})
        else:
            pointcache.update({key:(x,y,z)})
            points.append((x,y,z))
            create_basis(x,y,z)
            save_pointcache()

remove_points()
with open('/home/danya/slon-2018-steinhaus/3d/steinhaus-3d-tetrahedron') as o:
    for i,j in enumerate(o):
        print(i)
        if i==10:break
        add_points(j.strip().split())

add_tetrahedron()