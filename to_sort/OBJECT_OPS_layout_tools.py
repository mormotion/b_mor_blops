import bpy
from bpy.props import *
from mathutils import Vector
from math import floor, ceil
import bpy
from bpy.props import IntProperty, FloatProperty
from mathutils import Vector
from math import floor, ceil


def grid_layout_objects(objects, padding, rows):
    """ Layout objects in a grid, split into rows """
    dimensions = [o.dimensions for o in objects]
    columns = ceil(len(objects) / rows)
    x_step_size = max([dim.x for dim in dimensions]) + padding
    y_step_size = max([dim.y for dim in dimensions]) + padding
    x_total = x_step_size * columns

    for i, obj in enumerate(objects):
        x = 0 + ((x_step_size * i) % x_total)
        y_scaler = floor(i / columns) if i > 0 else 0
        y = 0 + (y_step_size * y_scaler)

        obj.location = Vector((x, y, 0))
    
    x_values = sorted([obj.location.x for obj in objects])
    y_values = sorted([obj.location.y for obj in objects])
    offset = Vector((x_values[-1] * 0.5,
                     y_values[-1] * 0.5,
                     0))
    for obj in objects:
        obj.location -= offset


class OBJECT_OT_grid_distribute_selected(bpy.types.Operator):
    bl_idname = 'object.grid_distribute_selected'
    bl_label = 'Grid Layout Objects'
    bl_description = 'Grid Layout Objects'
    bl_options = {"REGISTER", "UNDO"}

    padding = FloatProperty(name='Padding', default=0)
    rows = IntProperty(name='Rows', default=1, min=1)
    index_offset = IntProperty(name='Index Offset', default=0)

    @classmethod
    def poll(self, context):
        return len(context.selected_objects) > 0

    def execute(self, context):
        # Offset object list position
        objects = context.selected_objects[:]
        for i in range(self.index_offset):
            b = objects.pop()
            objects.insert(0, b)

        # Do layout
        grid_layout_objects(objects, self.padding, self.rows)
        return{'FINISHED'}



class OBJECT_OT_linearly_distribute_selected(bpy.types.Operator):
    bl_idname = "object.linearly_distribute_selected"
    bl_label = "Distibute Objects in a Line"
    bl_description = "Distribute selected object in a line"
    bl_options = {"REGISTER", "UNDO"}

    step_size = FloatProperty(name='Step Size', default=1.0)

    @classmethod
    def poll(cls, context):
        if context.selected_objects != 0:
            return True

    def execute(self, context):
        for i, obj in enumerate(context.selected_objects):
            obj.location.x = self.step_size * i
        
        return {"FINISHED"}

