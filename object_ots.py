import bpy
import bpy_extras


class OBJECT_OT_add_target(bpy.types.Operator):
    bl_idname = "object.add_target_for_selected"
    bl_label = "add target for selected"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        obj = context.active_object
        track_to = bpy.context.active_object.constraints.new('TRACK_TO')
        obj_target = bpy_extras.object_utils.object_data_add(context, obdata=None, operator=None, name=obj.name + '_target')
        track_to.target = obj_target
        track_to.track_axis = 'TRACK_NEGATIVE_Z'
        track_to.up_axis = 'UP_Y'
        return {'FINISHED'}