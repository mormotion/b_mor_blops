import bpy
from bpy.props import *
from mathutils import Vector
from math import floor, ceil
import bpy
from bpy.props import IntProperty, FloatProperty
from mathutils import Vector
from math import floor, ceil


class OBJECT_OT_grid_distribute_selected(bpy.types.Operator):
    bl_idname = 'object.distribute_selected_grid'
    bl_label = 'Grid Layout Objects'
    bl_description = 'Grid Layout Objects'
    bl_options = {"REGISTER", "UNDO"}

    padding = FloatProperty(name='Padding', default=0)
    rows = IntProperty(name='Rows', default=1, min=1)
    index_offset = IntProperty(name='Index Offset', default=0)

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) > 0

    def execute(self, context):
        # Offset object list position
        target_objects = context.selected_objects[:]
        for i in range(self.index_offset):
            b = target_objects.pop()
            target_objects.insert(0, b)

        # Do layout
        dimensions = [o.dimensions for o in target_objects]

        columns = ceil(len(target_objects) / self.rows)
        x_step_size = max([dim.x for dim in dimensions]) + self.padding
        y_step_size = max([dim.y for dim in dimensions]) + self.padding
        x_total = x_step_size * columns

        for i, obj in enumerate(target_objects):
            x = 0 + ((x_step_size * i) % x_total)
            y_scaler = floor(i / columns) if i > 0 else 0
            y = 0 + (y_step_size * y_scaler)

            obj.location = Vector((x, y, 0))
        
        x_values = sorted([obj.location.x for obj in target_objects])
        y_values = sorted([obj.location.y for obj in target_objects])
        offset = Vector((x_values[-1] * 0.5,
                        y_values[-1] * 0.5,
                        0))

        for obj in target_objects:
            obj.location -= offset

        return{'FINISHED'}


class OBJECT_OT_linearly_distribute_selected(bpy.types.Operator):
    bl_idname = "object.distribute_selected_linear"
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
            obj.location = Vector((
                                  self.step_size * i,
                                  0,
                                  0
                                  ))
        
        return {"FINISHED"}


classes = [
    OBJECT_OT_grid_distribute_selected,
    OBJECT_OT_linearly_distribute_selected,
    ]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)