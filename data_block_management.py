import bpy
import bpy_extras


class OBJECT_OT_object_name_to_data_block(bpy.types.Operator):
    bl_idname = "object.object_name_to_data_block"
    bl_label = "Rename Data to Match Object"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None

    def execute(self, context):
        for obj in context.selected_objects:
            print(obj)
            if not obj.data:
                continue
            obj.data.name = obj.name
        return {'FINISHED'}


def VIEW_MT_object_data_management(self, context):
    layout = self.layout
    layout.separator()
    layout.operator(OBJECT_OT_object_name_to_data_block.bl_idname)


classes = [
    OBJECT_OT_object_name_to_data_block,
    ]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.VIEW3D_MT_object.append(VIEW_MT_object_data_management)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    bpy.types.VIEW3D_MT_object.remove(VIEW_MT_object_data_management)