import bpy

class SceneObjectIdEnumerate(bpy.types.Operator):
    bl_idname = "object.scene_object_id_enumerate"
    bl_label = "Scene Object Id Enumerate"
    bl_description = "Loop over scene object and assign unique ids"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        for i, obj in enumerate(bpy.context.scene.objects):
            obj.pass_index = i
        return {"FINISHED"}

class MaterialIdEnumerate(bpy.types.Operator):
    bl_idname = "material.material_id_enumerate"
    bl_label = "Material Id Enumerate"
    bl_description = "Loop over materials and assign unique ids"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        for i, material in enumerate(bpy.data.materials):
            material.pass_index = i
        return {"FINISHED"}


def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()