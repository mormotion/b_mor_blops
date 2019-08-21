import bpy

class OBJECT_OT_child_selected_to_new_empty(bpy.types.Operator):
    bl_idname = 'object.child_selected_to_new_empty'
    bl_label = 'child_selected_to_new_empty'
    bl_description = 'child_selected_to_new_empty'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) is not 0

    def execute(self, context):
        new_empty = bpy.data.objects.new(name='NewParent', object_data=None)
        context.scene.objects.link(new_empty)
        for o in context.selected_objects:
            o.parent = new_empty
        return {'FINISHED'}