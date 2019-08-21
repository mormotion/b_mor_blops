import bpy


class MeshToObjectName(bpy.types.Operator):
    bl_idname = "object.mesh_to_object_name"
    bl_label = "Rename Mesh to Object Name"
    bl_description = "Rename selected objects mesh data to match name"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if len(context.selected_objects) == 0:
            return False
        return True

    def execute(self, context):
        # Rename mesh data names to match their user
        objects = context.selected_objects
        objects = [i for i in objects if i.type == 'MESH'] 
        for o in objects:
            mesh = o.data
            mesh.name = o.name
        return {"FINISHED"}


def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()