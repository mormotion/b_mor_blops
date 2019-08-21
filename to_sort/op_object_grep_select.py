import bpy
from bpy.props import StringProperty, BoolProperty
from fnmatch import fnmatch


def select_object_using_grep(context, grep_string: str, append_existing: bool):
    existing_selection = context.selected_objects
    if not append_existing:
        for obj in existing_selection:
            obj.select = False
    scene_objects = context.screen.scene.objects
    object_names = [i.name for i in scene_objects]

    for name in object_names:
        if fnmatch(name, grep_string):
            context.screen.scene.objects[name].select = True



class SelectObjectsUsingGrep(bpy.types.Operator):
    bl_idname = "object.select_objects_using_grep"
    bl_label = "Select Grep Object Matches"
    bl_description = "Select objects using a grep string"
    bl_options = {"REGISTER", "UNDO"}

    grep_string = StringProperty(name="Grep", default="")    
    append_existing = BoolProperty(name="Append Selection", default=False)

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        select_object_using_grep(context, self.grep_string, self.append_existing)
        return {"FINISHED"}


def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
