import bpy

class OBJECT_OT_Push_Transform(bpy.types.Operator):
    bl_idname = 'object.push_transform'
    bl_label = 'Push selected transform'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) > 0 

    def execute(self, context):
        # Push transform into new custom properties of selected objects
        for obj in context.selected_objects:
            obj['stored_loc'] = obj.location
            obj['stored_rot'] = obj.rotation_euler
            obj['stored_scale'] = obj.scale
        return {'FINISHED'}

class OBJECT_OT_Pop_Transform(bpy.types.Operator):
    bl_idname = 'object.pop_transform'
    bl_label = 'Pop selected transform'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) > 0 

    def execute(self, context):
        # Resore previous pushed transforms to selected objects
        for obj in context.selected_objects:
            if not obj.get('stored_loc'):
                continue
            obj.location = obj['stored_loc']
            obj.rotation_euler = obj['stored_rot']
            obj.scale = obj['stored_scale']
        return {'FINISHED'}


classes = [
    OBJECT_OT_Push_Transform,
    OBJECT_OT_Pop_Transform,
    ]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
