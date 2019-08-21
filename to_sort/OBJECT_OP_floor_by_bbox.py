import bpy
from mathutils import Vector
from bpy.props import BoolProperty
from bpy.props import EnumProperty


### TODO: add enum prop flooring by alternative axis/floors 


def floor_objects_by_lowest(context):
    """ Floor selected objects by the lowest """
    selected_objects = context.selected_objects
    z_values = []
    for obj in selected_objects:
        matrix = obj.matrix_world
        bbox = obj.bound_box
        world_bbox = [matrix * Vector(corner) for corner in bbox]
        for v in world_bbox:    
            z_values.append(v[2])
    z_values.sort()
    z_offset = z_values[0]
    
    for obj in selected_objects:
        obj.location[2] -= z_offset


def floor_individual_objects(context):
    """ Floor each selected object individually """
    objects = context.selected_objects
    for obj in objects:
        matrix = obj.matrix_world
        bbox = obj.bound_box
        world_bbox = [matrix * Vector(corner) for corner in bbox]
        z_values = []
        for v in world_bbox:    
            z_values.append(v[2])
        z_values.sort()
        z_offset = z_values[0]
        obj.location.z -= z_offset



class OBJECT_OT_floor_by_bbox(bpy.types.Operator):
    """Floor Selected objects based on lowest bbox point"""
    bl_idname = "object.floor_objects_by_bbox"
    bl_label = "Floor Objects by BBox"
    bl_options = {"REGISTER", "UNDO"}

    individual_objects = BoolProperty(name="Individual Object",
                                      default=True)

    @classmethod
    def poll(cls, context):
        if context.selected_objects != 0:
            return True

    def execute(self, context):
        if not self.individual_objects:
            floor_objects_by_lowest(context)
        else:
            floor_individual_objects(context)
        return {'FINISHED'}
