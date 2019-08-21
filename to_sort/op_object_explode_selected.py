import bpy
import math
from bpy.props import BoolProperty, FloatProperty


class Radial_Explode(bpy.types.Operator):
    bl_idname = "object.radial_explode_selected"
    bl_label = "Radial Explode Selected"
    bl_description = "Description that shows in blender tooltips"
    bl_options = {"REGISTER", "UNDO"}

    radius = FloatProperty(name="radius",
                           description="displacement scaler",
                           default=1.0)

    @classmethod
    def poll(cls, context):
        if len(context.selected_objects) == 0:
            return False
        return True

    def execute(self, context):
        objects = context.selected_objects
        count = len(objects)
        step_size = (math.pi * 2) / count
        for i, obj in enumerate(objects):
            angle = step_size * i
            obj.location.x = math.sin(angle) * self.radius
            obj.location.y = math.cos(angle) * self.radius
        return {"FINISHED"}


def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()