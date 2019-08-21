import bpy
from bpy.props import StringProperty


class MyClassName(bpy.types.Operator):
    bl_idname = "object.rename_selected_object"
    bl_label = "Rename Active Object"
    bl_description = "Rename Active Object"
    bl_options = {"REGISTER", "UNDO"}

    new_name = StringProperty(name="Rename", default="")    

    @classmethod
    def poll(cls, context):
        return True
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        context.active_object.name = self.new_name
        return {"FINISHED"}

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()