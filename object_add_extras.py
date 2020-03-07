import bpy
from pathlib import Path

ADDON_DIR = Path(__name__).resolve().parent
ASSET_DIR = Path(ADDON_DIR, 'assets')


class OBJECT_OT_Add_Shaderball(bpy.types.Operator):
    bl_idname = 'object.add_shaderball'
    bl_label = 'Add Shaderball'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def execute(self, context):
        src_blend = Path(ASSET_DIR, 'shaderball.blend')

        with bpy.data.libraries.load(str(src_blend)) as (data_from , data_to):
            data_to.collections = ['Shaderball']
        context.scene.collection.children.link(data_to.collections[0])
        return {'FINISHED'}


classes = [
    OBJECT_OT_Add_Shaderball,
    ]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)