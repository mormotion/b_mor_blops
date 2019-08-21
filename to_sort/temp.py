import bpy
from math import radians
from mathutils import *

def rotate_objects_around_median(rot):
    selected_objects = bpy.context.selected_objects
    origins = [object.location for object in selected_objects]
    sum_locations = Vector((0,0,0))
    for origin in origins:
        sum_locations += origin
    pivot = sum_locations / len(origins)
    #m = rot.to_matrix().to_4x4()
    #m.normalize()

    # This is a shitty solution
    t, f = True, False
    bpy.ops.transform.rotate(value=rot[0], constraint_axis=(t,f,f))
    bpy.ops.transform.rotate(value=rot[1], constraint_axis=(f,t,f))
    bpy.ops.transform.rotate(value=rot[2], constraint_axis=(f,f,t))
    
        
rotate_objects_around_median(Vector((radians( 0),
                                     radians( 0),
                                     radians( 10))
                                    ))