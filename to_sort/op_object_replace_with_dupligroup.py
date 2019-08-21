import bpy
from bpy.props import (EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )


# Warning: Needs cleanup


def replace_selected_with_dupli_group(group):
    deleteList = []
    
    # Create Instances
    for object in bpy.context.selected_objects:
        newInstance = create_instance_at_object(object, group)
        deleteList.append(object)
    
    # Remove Original Objects
    for object in deleteList:
        bpy.context.scene.objects.unlink(object)
        bpy.data.objects.remove(object)

    
def create_instance_at_object(targetObject, replacementGroup):
    name = replacementGroup  + '_instance'
    loc = targetObject.location
    rot = targetObject.rotation_euler
    scale = targetObject.scale
    
    new_null = bpy.data.objects.new(name, None)
    bpy.context.scene.objects.link(new_null)
    new_null.location = loc
    new_null.rotation_euler = rot
    new_null.scale = scale
    
    new_null.dupli_type = 'GROUP'
    new_null.dupli_group = bpy.data.groups[replacementGroup]
    
    return new_null
    

# ------------------------------------------------------------------------
#    Store properties in scene
# ------------------------------------------------------------------------

def get_file_groups(scene, context):
    groups = ([g.name for g in bpy.data.groups])
    return [(y, y, "", x) for x, y in enumerate(groups)]


class MySettings(PropertyGroup):

    groups = EnumProperty(
        name="Groups",
        description="",
        items=get_file_groups
        )

# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------

class ReplaceWithDupligroup(Operator):
    """Tooltip"""
    bl_idname = "object.replace_with_dupli_group"
    bl_label = "Replace Selected with Dupligroup"
    bl_property = "groups"

    groups = MySettings.groups

    def execute(self, context):
        #self.report({'INFO'}, "You've selected: %s" % self.groups)
        replace_selected_with_dupli_group(self.groups)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.invoke_search_popup(self)
        return {'FINISHED'}


# ------------------------------------------------------------------------
#   Registration
# ------------------------------------------------------------------------

def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.my_tool = PointerProperty(type=MySettings)

def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.my_tool

if __name__ == "__main__":
    register()


