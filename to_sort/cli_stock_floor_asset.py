import bpy
from mathutils import *

def find_asset_root():
    bpy.ops.object.select_all(action='SELECT')
    objects = bpy.context.screen.scene.objects
    for object in objects:
        if object.parent is None:
            object.select = False
        
    selected_objects = bpy.context.selected_objects
    z_values = []
    for object in selected_objects:
        matrix = object.matrix_world
        bbox = object.bound_box
        world_bbox = [matrix * Vector(corner) for corner in bbox]
        for v in world_bbox:    
            z_values.append(v[2])
    z_values.sort()
    z_offset = z_values[0]
    
    for object in selected_objects:
        object.location[2] -= z_offset

    bpy.ops.wm.save_mainfile()


if __name__ == '__main__':
    print(find_asset_root())